# -*- coding: utf-8 -*-
"""v82: a phone plate for every drawn map.

The maps are 860-unit plates. On a phone they are shown about 328 px wide, so
their 11-13 unit names came out at four or five pixels. This module reads each
finished map on the page and sets a second, phone-first plate beside it:

* each map panel (an outer neatline) is cut out and scaled to the phone width,
  with all of its artwork: terrain, water, roads, routes and marks;
* every name inside the panel is set again at 14-15 units (11.5-12.3 px), at
  its own place, with a white halo. A name that cannot be set without covering
  another gets a lettered badge at its place and is spelled out in a key under
  the panel, so no name is lost;
* names that sat beside the panel on leader lines become lettered badges on
  their places, with their text in the key;
* the legend is set as rows, each with its own symbol cut from the plate;
* the heading, notes and source lines are set as text, as in the v80 plates.

On a phone (under 760 px) the phone plate shows and the full plate is hidden;
on a wider screen and in print the full plate shows, and the lightbox always
opens the full plate. Nothing is retyped: every word comes from the map as the
build drew it, and tools/check_redraw.py checks that every word is kept.
"""
import html as _html
import re

from build_figs6 import W, GOLD, T_NOTE
from build_figs7 import Canvas, tx, wrap, kind_of, head_and_lede, joinlines, art, PAD, CW
from map_style import INK, BODY, NOTE, RAMALLAH, FONT

FRAME = '#8A7E6A'
RULE_COL = '#D9D4C8'
INNER = W - 2 * PAD
MAX_H = 540            # tallest a panel is drawn, in phone units
DEG = re.compile(r'^\d+(\.\d+)?°[NSEW]$')
MARK = 'v82-phone-maps'


# ───────────────────────────────────────────── reading the finished map
class Live:
    def __init__(self, svg):
        self.raw = svg
        self.items = []
        for m in re.finditer(r'<text\b([^>]*)>(.*?)</text>', svg, re.S):
            a, body = m.group(1), m.group(2)
            if ' stroke=' in a:
                continue
            txt = _html.unescape(re.sub(r'<[^>]+>', '', body)).strip()
            if not txt:
                continue
            g = lambda k, d=None: (re.search(r'\b%s="([^"]*)"' % k, a) or [None, d])[1]
            rot = re.search(r'rotate\(([-\d.]+)', a)
            self.items.append(dict(
                x=float(g('x', 0)), y=float(g('y', 0)), size=float(g('font-size', 12)), fill=g('fill', INK),
                weight=g('font-weight', '400'), style=g('font-style', 'normal'), anchor=g('text-anchor', 'start'),
                ls=float(g('letter-spacing', 0) or 0), rot=float(rot.group(1)) if rot else 0,
                sc='small-caps' in a, text=txt))
        self.panels = []
        for m in re.finditer(r'<rect\b([^>]*)/?>', svg):
            a = m.group(1)
            if 'fill="none"' in a and f'stroke="{FRAME}"' in a:
                d = dict(re.findall(r'([\w-]+)="([^"]*)"', a))
                x, y, w, h = (float(d[k]) for k in ('x', 'y', 'width', 'height'))
                if w > 150:
                    self.panels.append((x, y, x + w, y + h))
        self.panels = [p for p in self.panels
                       if not any(q != p and q[0] <= p[0] and q[1] <= p[1] and q[2] >= p[2] and q[3] >= p[3]
                                  for q in self.panels)]
        self.panels.sort(key=lambda p: (int((p[1] + 40) / 300), p[0]))
        # the white tab under each scale bar
        self.tabs = []
        for m in re.finditer(r'<rect x="([-\d.]+)" y="([-\d.]+)" width="([\d.]+)" height="26" fill="#FFFFFF" opacity=".82"', svg):
            x, y, w = (float(v) for v in m.groups())
            self.tabs.append((x, y, x + w, y + 26))
        # marks: dots, rings and diamonds
        self.marks = []
        self.mfill = {}
        for m in re.finditer(r'<circle\b([^>]*)/?>', svg):
            d = dict(re.findall(r'([\w-]+)="([^"]*)"', m.group(1)))
            try:
                r = float(d.get('r', 0))
                if 2.4 <= r <= 12.5:
                    self.marks.append((float(d['cx']), float(d['cy']), r))
                    self.mfill[(float(d['cx']), float(d['cy']))] = d.get('fill', '#004A26')
            except (KeyError, ValueError):
                pass
        for m in re.finditer(r'<rect\b([^>]*)/?>', svg):
            a = m.group(1)
            if 'rotate(45' in a:
                d = dict(re.findall(r'([\w-]+)="([^"]*)"', a))
                w = float(d['width'])
                self.marks.append((float(d['x']) + w / 2, float(d['y']) + w / 2, w * .72))
        # leader lines: a two-point path or line with one end in a panel
        self.leaders = []
        for m in re.finditer(r'<path d="M([-\d.]+)[ ,]([-\d.]+) L([-\d.]+)[ ,]([-\d.]+)"([^>]*)/?>', svg):
            if 'stroke-width=".8"' in m.group(5) or 'stroke-width="0.8"' in m.group(5):
                self.leaders.append(tuple(float(v) for v in m.groups()[:4]))
        self.rule = None
        for m in re.finditer(r'<line x1="40" y1="([\d.]+)" x2="820" y2="[\d.]+" stroke="%s"' % RULE_COL, svg):
            self.rule = float(m.group(1))

    def where(self, x0=-1e9, x1=1e9, y0=-1e9, y1=1e9):
        return [i for i in self.items if x0 <= i['x'] < x1 and y0 <= i['y'] < y1]

    def inside(self, p, x, y, pad=0):
        return p[0] - pad <= x <= p[2] + pad and p[1] - pad <= y <= p[3] + pad


def width_of(s, size, kind, ls=0):
    return len(s) * size * CW[kind] * (1 + .4 * sum(ch.isupper() for ch in s) / max(1, len(s))) + ls * len(s)


def box(x, y, w, h, anchor):
    x0 = x if anchor == 'start' else (x - w if anchor == 'end' else x - w / 2)
    return (x0, y - h, x0 + w, y)


def hits(a, b, m=1.5):
    return not (a[2] + m < b[0] or b[2] + m < a[0] or a[3] + m < b[1] or b[3] + m < a[1])


def letter(n):
    return 'abcdefghijklmnopqrstuvwxyz'[n % 26] * (1 + n // 26)


def lbadge(x, y, s, fill=INK):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9.5" fill="#FFFFFF" stroke="{fill}" stroke-width="1.6"/>'
            + tx(x, y + 4.8, s, 14, fill, 'middle', '700', 'italic'))


def nbadge(x, y, s, fill):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9.5" fill="{fill}" stroke="#FFFFFF" stroke-width="1.4"/>'
            + tx(x, y + 5, s, 14, '#FFFFFF', 'middle', '700'))


def halo_tx(x, y, s, size, fill, anchor, weight, style, sc, ls=0, rot=0):
    extra = ' style="font-variant:small-caps"' if sc else ''
    if ls:
        extra += f' letter-spacing="{ls:.2f}"'
    if rot:
        extra += f' transform="rotate({rot:g} {x:.1f} {y:.1f})"'
    common = (f'x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" '
              f'font-style="{style}" font-family="{FONT}"{extra}')
    s = _html.escape(s, quote=False)
    return (f'<text {common} fill="none" stroke="#FFFFFF" stroke-width="3.4" stroke-linejoin="round" '
            f'opacity=".92">{s}</text><text {common} fill="{fill}">{s}</text>')


# ───────────────────────────────────────────── one panel
def groups_in(o, p):
    """Names in a panel, each with the smaller lines set under it."""
    its = sorted([i for i in o.items if o.inside(p, i['x'], i['y']) and not DEG.match(i['text'])],
                 key=lambda i: (i['y'], i['x']))
    used, out = set(), []
    for k, it in enumerate(its):
        if k in used:
            continue
        g = [it]
        used.add(k)
        if not it['rot']:
            for j in range(k + 1, len(its)):
                if j in used:
                    continue
                n = its[j]
                last = g[-1]
                if (0 < n['y'] - last['y'] <= max(16, last['size'] * 1.35) and n['anchor'] == it['anchor']
                        and abs(n['x'] - it['x']) < 30 and n['size'] <= it['size'] and not n['rot']
                        and (n['size'] < it['size'] or n['style'] == 'italic')):
                    g.append(n)
                    used.add(j)
        out.append(g)
    return out


def near_mark(o, it, p):
    """The mark a name belongs to: the nearest dot or diamond to its anchor."""
    best, bd = None, 1e9
    for (mx, my, r) in o.marks:
        if not o.inside(p, mx, my):
            continue
        ax = it['x']
        if it['anchor'] == 'start':
            dx = ax - mx
            if dx < -4:
                continue
        elif it['anchor'] == 'end':
            dx = mx - ax
            if dx < -4:
                continue
        else:
            dx = abs(ax - mx)
        d = (max(dx, 0) ** 2 + (it['y'] - 4 - my) ** 2) ** .5
        if d < bd:
            best, bd = (mx, my, r), d
    return best if bd < 30 else None


def panel(c, o, p, cid, keyed, callouts):
    """Draw panel p at the phone width. keyed: list the panel adds its key lines to.
    callouts: [(mark_xy, lines)] from outside the panel, lettered on their places."""
    x0, y0, x1, y1 = p
    k = min(INNER / (x1 - x0), MAX_H / (y1 - y0))
    w = (x1 - x0) * k
    left = PAD + (INNER - w) / 2
    top = c.y
    a, h = art(None, x0, y0, x1, y1, w, left, top, raw=_only(o.raw, p), cid=cid)
    c.add(a)
    c.add(f'<rect x="{left:.1f}" y="{top:.1f}" width="{w:.1f}" height="{h:.1f}" fill="none" stroke="{FRAME}"/>')
    P = lambda x, y: (left + (x - x0) * k, top + (y - y0) * k)
    frame = (left + 2, top + 2, left + w - 2, top + h - 2)
    taken = []
    for (mx, my, r) in o.marks:
        if o.inside(p, mx, my):
            X, Y = P(mx, my)
            rr = max(3, r * k)
            taken.append((X - rr, Y - rr, X + rr, Y + rr))
    tabbox = []
    for (ax, ay, bx, by) in o.tabs:
        if o.inside(p, ax, ay):
            X0, Y0 = P(ax, ay)
            X1, Y1 = P(bx, by)
            tabbox.append((X0, Y0, X1, Y1))
    out, later = [], []
    letters = []

    def put_letter(X, Y, lines):
        n = sum(1 for e in keyed if e[2] is None)
        keyed.append((letter(n), lines, None))
        letters.append((X, Y, letter(n)))

    # callouts from outside the panel first, so the names inside avoid their badges
    for (mx, my), lines in callouts:
        X, Y = P(mx, my)
        put_letter(X + 11, Y - 11, lines)
        taken.append((X, Y - 22, X + 22, Y))
    groups = groups_in(o, p)
    # badges drawn inside circles (numbered places): keep them as badges
    rest = []
    numbered = {}
    for g in groups:
        it = g[0]
        circ = None
        if len(g) == 1 and re.fullmatch(r'\d{1,2}', it['text']):
            for (mx, my, r) in o.marks:
                if abs(mx - it['x']) < r + 1 and abs(my - (it['y'] - it['size'] * .35)) < r + 1:
                    circ = (mx, my)
        if circ:
            X, Y = P(*circ)
            out.append(nbadge(X, Y, it['text'], o.mfill.get(circ, '#004A26')))
            numbered[circ] = (it['text'], o.mfill.get(circ, '#004A26'))
            taken.append((X - 10, Y - 10, X + 10, Y + 10))
        else:
            rest.append(g)
    # Ramallah first, then the larger and bolder names
    rest.sort(key=lambda g: (g[0]['rot'] != 0, g[0]['fill'] != RAMALLAH, -g[0]['size'],
                             g[0]['weight'] != '700', g[0]['y']))
    for g in rest:
        it = g[0]
        if it['rot']:
            import math
            X, Y = P(it['x'], it['y'])
            L = width_of(it['text'], 14, 'italic', it['ls'] * .6) / 2 + 2
            ca, sa = math.cos(math.radians(it['rot'])), math.sin(math.radians(it['rot']))
            dx, dy = abs(L * ca), abs(L * sa)
            X = min(max(X, frame[0] + dx + 6), frame[2] - dx - 6)
            Y = min(max(Y, frame[1] + dy + 12), frame[3] - dy - 4)
            ok = None
            for off in (0, 8, -8, 16, -16, 26, -26):
                for slide in (0, 14, -14, 28, -28):
                    XX = X + slide * ca - off * sa
                    YY = Y + slide * sa + off * ca
                    pts = [(XX + t * ca + 5 * sa, YY + t * sa - 5 * ca) for t in range(int(-L), int(L) + 1, 7)]
                    bbs = [(px - 6, py - 6, px + 6, py + 6) for px, py in pts]
                    if any(b[0] < frame[0] or b[2] > frame[2] or b[1] < frame[1] or b[3] > frame[3] for b in bbs):
                        continue
                    if any(hits(b, t, 0) for b in bbs for t in taken + tabbox):
                        continue
                    ok = (XX, YY, bbs)
                    break
                if ok:
                    break
            if not ok:
                later.append((g, None, X, Y))
                continue
            XX, YY, bbs = ok
            taken.extend(bbs)
            out.append(halo_tx(XX, YY, it['text'], 14, it['fill'], it['anchor'], it['weight'], it['style'],
                               it['sc'], it['ls'] * .6, it['rot']))
            continue
        sizes = [15 if (n['weight'] == '700' or n['size'] >= 13 or n['sc']) and j == 0 else 14
                 for j, n in enumerate(g)]
        kinds = [kind_of(n['weight'], n['style'], n['sc']) for n in g]
        lsp = [n['ls'] * .6 for n in g]
        ws = [width_of(n['text'], s, kd, l) for n, s, kd, l in zip(g, sizes, kinds, lsp)]
        hh = sum(s * 1.12 for s in sizes)
        mk = near_mark(o, it, p)
        X, Y = P(it['x'], it['y'])
        cands = [(X, Y, it['anchor'])]
        if mk:
            MX, MY = P(mk[0], mk[1])
            rr = max(3, mk[2] * k) + 4
            d0 = sizes[0] * .36
            cands += [(MX + rr, MY + d0, 'start'), (MX - rr, MY + d0, 'end'),
                      (MX, MY - rr - hh + sizes[0] - 1, 'middle'), (MX, MY + rr + sizes[0], 'middle'),
                      (MX + rr, MY - rr - hh + sizes[0] + 2, 'start'), (MX - rr, MY - rr - hh + sizes[0] + 2, 'end'),
                      (MX + rr, MY + rr + sizes[0] - 2, 'start'), (MX - rr, MY + rr + sizes[0] - 2, 'end')]
        else:
            cands += [(X, Y + dy, it['anchor']) for dy in (-8, 8, -16, 16)]
        placed = None
        ontab = any(t[0] - 2 <= it['x'] <= t[2] + 30 and t[1] <= it['y'] <= t[3] for t in o.tabs)
        if ontab:
            cands = cands[:1]                  # the scale bar's own figures sit on its tab
        for (cx, cy, an) in cands:
            bb = box(cx, cy - sizes[0] + hh, max(ws), hh, an)
            bb = (bb[0], cy - sizes[0] * .82, bb[2], cy - sizes[0] * .82 + hh)
            if bb[0] < frame[0] or bb[2] > frame[2] or bb[1] < frame[1] or bb[3] > frame[3]:
                continue
            if any(hits(bb, t) for t in taken) or (not ontab and any(hits(bb, t) for t in tabbox)):
                continue
            placed = (cx, cy, an, bb)
            break
        if not placed:
            later.append((g, mk, X, Y))
            continue
        cx, cy, an, bb = placed
        taken.append(bb)
        yy = cy
        for j, n in enumerate(g):
            out.append(halo_tx(cx, yy, n['text'], sizes[j], n['fill'], an, n['weight'], n['style'], n['sc'], lsp[j]))
            yy += sizes[j] * 1.12 if j + 1 == len(sizes) else sizes[j + 1] * 1.12
    for g, mk, X, Y in later:
        if mk and (mk[0], mk[1]) in numbered:
            num, fill = numbered[(mk[0], mk[1])]
            keyed.append((num, g, fill))
            continue
        import math
        cx_, cy_ = P(mk[0], mk[1]) if mk else (X, Y - 5)
        spots = [(cx_, cy_)] if not mk else []
        for rad in (14, 20, 27, 35, 45, 56):
            for ang in range(-45, 315, 30):
                spots.append((cx_ + rad * math.cos(math.radians(ang)), cy_ + rad * math.sin(math.radians(ang))))
        def cost(pt):
            b = (pt[0] - 10, pt[1] - 10, pt[0] + 10, pt[1] + 10)
            out_ = b[0] < frame[0] or b[2] > frame[2] or b[1] < frame[1] or b[3] > frame[3]
            return (out_, sum(hits(b, t, 0) for t in taken))
        sx, sy = min(spots, key=cost)
        taken.append((sx - 10, sy - 10, sx + 10, sy + 10))
        put_letter(sx, sy, g)
    c.add(*out)
    for (X, Y, s) in letters:
        c.add(lbadge(X, Y, s))
    # graticule values: inside the frame, at its edges, where they fit
    for it in o.items:
        if not DEG.match(it['text']):
            continue
        if x0 - 50 < it['x'] < x0 and y0 - 4 <= it['y'] <= y1 + 4 and it['anchor'] == 'end':
            X, Y = frame[0] + 2, P(0, it['y'])[1] + 4
            an = 'start'
        elif y1 < it['y'] < y1 + 26 and x0 - 4 <= it['x'] <= x1 + 4 and it['anchor'] == 'middle':
            X, Y = P(it['x'], 0)[0], frame[3] - 3
            an = 'middle'
        elif x1 < it['x'] < x1 + 50 and y0 - 4 <= it['y'] <= y1 + 4 and it['anchor'] == 'start':
            X, Y = frame[2] - 2, P(0, it['y'])[1] + 4
            an = 'end'
        elif y0 - 20 < it['y'] < y0 and x0 - 4 <= it['x'] <= x1 + 4 and it['anchor'] == 'middle':
            X, Y = P(it['x'], 0)[0], frame[1] + 14
            an = 'middle'
        else:
            continue
        bb = box(X, Y, width_of(it['text'], 14, 'normal'), 14, an)
        if bb[0] < frame[0] - 1 or bb[2] > frame[2] + 1 or any(hits(bb, t) for t in taken + tabbox):
            continue
        taken.append(bb)
        c.add(halo_tx(X, Y, it['text'], 14, NOTE, an, '400', 'normal', False))
    c.y = top + h + 10


def key_lines(c, keyed, start):
    for s, lines, fill in sorted(keyed[start:], key=lambda e: (e[2] is None, int(e[0]) if e[0].isdigit() else 0)):
        top = c.y
        c.add(nbadge(PAD + 10, top + 10, s, fill) if fill else lbadge(PAD + 10, top + 10, s))
        first = True
        lines = sorted(lines, key=lambda i: i['y'])
        for n in lines[:1] + join2(lines[1:]):
            bold = first and (n['weight'] == '700' or n['size'] >= 13 or n['sc'])
            c.para(n['text'], 15 if bold else T_NOTE, n['fill'] if bold else (NOTE if n['style'] == 'italic' else BODY),
                   n['style'] if not bold else 'normal', '700' if bold else '400', x=PAD + 26,
                   width=INNER - 26, gap=2, sc=n['sc'])
            first = False
        c.y = max(c.y, top + 22) + 4


# ───────────────────────────────────────────── outside the panels
def blocks(items, o=None):
    """Group loose lines into blocks: same column, consecutive lines. A short
    right-aligned figure on a block's line (a distance) joins that block."""
    out = []
    side = [i for i in items if i['anchor'] == 'end' and len(i['text']) <= 12]
    items = [i for i in items if not any(i is j for j in side)]
    for it in sorted(items, key=lambda i: (i['y'], i['x'])):
        for b in out:
            last = b[-1]
            ax = lambda i: (i['x'], i['anchor'])
            if (0 < it['y'] - last['y'] <= 19 and abs(it['x'] - b[0]['x']) < 40 and it['anchor'] == b[0]['anchor']
                    and not (o is not None and it['anchor'] == 'start' and _sym_near(o, it, 'circle'))):
                b.append(it)
                break
        else:
            out.append([it])
    for it in side:
        host = None
        for b in out:
            for k, ln in enumerate(b):
                if abs(ln['y'] - it['y']) < 1.5 and _left(ln) < it['x']:
                    host = (b, k)
        if host:
            b, k = host
            b.insert(k + 1, dict(it, y=b[k]['y'] + .01))
        else:
            out.append([it])
    return out


def phone_map(svg, title, slug):
    o = Live(svg)
    if not o.panels:
        return None
    c = Canvas()
    ptop = min(p[1] for p in o.panels)
    pbot = max(p[3] for p in o.panels)
    head = [i for i in o.items if i['y'] < ptop - 4 and i['y'] <= 72 and i['x'] <= 60]
    hid = {id(i) for i in head}
    # the heading of each panel: the line just above it
    heads = {}
    for i in o.items:
        if id(i) in hid:
            continue
        for n, p in enumerate(o.panels):
            if p[1] - 26 <= i['y'] < p[1] and p[0] - 12 <= i['x'] <= p[2]:
                heads.setdefault(n, []).append(i)
                hid.add(id(i))
    rule = o.rule or 1e9
    foot = [i for i in o.items if i['y'] > rule]
    hid |= {id(i) for i in foot}
    loose = [i for i in o.items if id(i) not in hid and not any(o.inside(p, i['x'], i['y']) for p in o.panels)
             and not DEG.match(i['text'])]
    # legend rows: a line with a symbol drawn just left of it, below the panels
    cand = [i for i in loose if i['y'] > pbot + 6 and i['anchor'] == 'start' and i['size'] <= 11.6
            and _sym_near(o, i)]
    legend = [i for i in cand if len(cand) == 1 or any(j is not i and (abs(j['x'] - i['x']) < 2 or abs(j['y'] - i['y']) < 1.5)
                                                       for j in cand)]
    lid = {id(i) for i in legend}
    other = [i for i in loose if id(i) not in lid]
    # callouts: loose blocks joined to a place by a leader line
    bl = blocks(other, o)
    calls = {n: [] for n in range(len(o.panels))}
    free = []
    for b in bl:
        bx0 = min(_left(i) for i in b) - 16
        bx1 = max(_right(i) for i in b) + 16
        by0, by1 = b[0]['y'] - 16, b[-1]['y'] + 6
        hit = None
        for (ax, ay, bx, by) in o.leaders:
            for (px, py, qx, qy) in ((ax, ay, bx, by), (bx, by, ax, ay)):
                if bx0 <= qx <= bx1 and by0 <= qy <= by1:
                    for n, p in enumerate(o.panels):
                        if o.inside(p, px, py):
                            hit = (n, _snap(o, px, py))
        if hit:
            calls[hit[0]].append((hit[1], b))
        else:
            free.append(b)
    head = sorted(head, key=lambda i: (i['y'], i['x']))
    if head:
        c.kicker(head[0]['text'])
        for q in join2(head[1:]):
            c.para(q['text'], T_NOTE, NOTE, 'italic', gap=6)
        c.y += 2
    keyed = []
    for n, p in enumerate(o.panels):
        for it in sorted(heads.get(n, []), key=lambda i: (i['y'], i['x'])):
            c.para(it['text'], 15, it['fill'], 'normal', '700', sc=True, gap=4)
        start = len(keyed)
        cl = sorted(calls[n], key=lambda cb: (cb[0][1], cb[0][0]))
        panel(c, o, p, '%s-p%d' % (slug, n), keyed, cl)
        key_lines(c, keyed, start)
        # loose text that sits beside or under this panel
        mine = [b for b in free if _owner(o, b) == n]
        for b in sorted(mine, key=lambda b: (b[0]['y'], b[0]['x'])):
            _block(c, b, o)
            free.remove(b)
        c.y += 6
    if legend:
        c.rule(10)
        for i in sorted(legend, key=lambda i: (i['y'], i['x'])):
            top = c.y
            sx, sy = i['x'] - 14, i['y'] - 4
            a, h = art(None, sx - 13, sy - 9, sx + 13, sy + 9, 34, PAD, top, raw=_symbol(o, sx, sy),
                       cid='%s-l%d' % (slug, len(c.o)))
            c.add(a)
            c.para(i['text'], 15, BODY, 'normal', x=PAD + 44, width=INNER - 44, gap=2)
            c.y = max(c.y, top + h) + 5
    for b in sorted(free, key=lambda b: (b[0]['y'], b[0]['x'])):
        _block(c, b, o)
    if foot:
        c.rule()
        for q in joinlines(foot):
            bold = q['weight'] == '700'
            c.para(q['text'], 15 if bold else T_NOTE, INK if bold else NOTE, 'normal' if bold else q['style'],
                   '700' if bold else '400', gap=6)
    c.para('Tap the map to see the full plate.', T_NOTE, NOTE, 'italic', gap=2)
    s = c.svg(title)
    return s.replace('class="phonefig"', 'class="phonefig phonemap"', 1)


class _Wrap:
    def __init__(self, items):
        self.items = items

    def where(self, x0=-1e9, x1=1e9, y0=-1e9, y1=1e9):
        return [i for i in self.items if x0 <= i['x'] < x1 and y0 <= i['y'] < y1]


def _left(i):
    w = len(i['text']) * i['size'] * .5
    return i['x'] if i['anchor'] == 'start' else (i['x'] - w if i['anchor'] == 'end' else i['x'] - w / 2)


def _right(i):
    return _left(i) + len(i['text']) * i['size'] * .5


def _only(raw, p):
    """The plate without the rasters of its other panels."""
    def keep(m):
        d = dict(re.findall(r'([\w-]+)="([^"]{0,40})', m.group(0)))
        try:
            x, y, w, h = (float(d[k]) for k in ('x', 'y', 'width', 'height'))
        except (KeyError, ValueError):
            return m.group(0)
        return m.group(0) if not (x + w < p[0] or x > p[2] or y + h < p[1] or y > p[3]) else ''
    return re.sub(r'<image\b[^>]*/>', keep, raw)


def _symbol(o, sx, sy):
    """Only the legend symbol drawn around (sx, sy), as a small plate."""
    out = []
    for m in re.finditer(r'<(circle|rect|line|path|polyline)\b([^>]*?)/>', o.raw):
        if _pos(m.group(1), m.group(2), sx, sy):
            out.append(m.group(0))
    return '<svg>%s</svg>' % ''.join(out)


def _pos(tag, attrs, sx, sy, rx=13, ry=9):
    d = dict(re.findall(r'([\w-]+)="([^"]*)"', attrs))
    try:
        if tag == 'circle':
            px, py = float(d['cx']), float(d['cy'])
        elif tag == 'rect':
            if float(d.get('width', 99)) > 30:
                return False
            px, py = float(d['x']) + float(d.get('width', 0)) / 2, float(d['y']) + float(d.get('height', 0)) / 2
        elif tag == 'line':
            px, py = (float(d['x1']) + float(d['x2'])) / 2, (float(d['y1']) + float(d['y2'])) / 2
        elif tag == 'polyline':
            pts = [float(v) for v in re.split(r'[ ,]+', d.get('points', '').strip()) if v]
            px, py = sum(pts[0::2]) / max(1, len(pts) // 2), sum(pts[1::2]) / max(1, len(pts) // 2)
        else:
            nums = [float(v) for v in re.findall(r'-?[\d.]+', d.get('d', ''))]
            if len(nums) < 2 or len(nums) > 40:
                return False
            px, py = sum(nums[0::2]) / len(nums[0::2]), sum(nums[1::2]) / len(nums[1::2])
    except (KeyError, ValueError, ZeroDivisionError):
        return False
    return abs(px - sx) <= rx and abs(py - sy) <= ry


def _sym_near(o, i, tags='circle|rect|line|path'):
    sx, sy = i['x'] - 14, i['y'] - 4
    for m in re.finditer(r'<(%s)\b([^>]*)/?>' % tags, o.raw):
        d = dict(re.findall(r'([\w-]+)="([^"]*)"', m.group(2)))
        try:
            if m.group(1) == 'circle':
                px, py = float(d['cx']), float(d['cy'])
            elif m.group(1) == 'rect':
                px, py = float(d['x']) + float(d.get('width', 0)) / 2, float(d['y']) + float(d.get('height', 0)) / 2
            elif m.group(1) == 'line':
                px, py = (float(d['x1']) + float(d['x2'])) / 2, (float(d['y1']) + float(d['y2'])) / 2
            else:
                mm = re.match(r'M\s*([-\d.]+)[ ,]([-\d.]+)', d.get('d', ''))
                if not mm:
                    continue
                px, py = float(mm.group(1)) + 10, float(mm.group(2))
        except (KeyError, ValueError):
            continue
        if abs(px - sx) <= 8 and abs(py - sy) <= 6:
            return True
    return False


def _snap(o, x, y):
    best = min(o.marks, key=lambda m: (m[0] - x) ** 2 + (m[1] - y) ** 2, default=None)
    if best and (best[0] - x) ** 2 + (best[1] - y) ** 2 < 15 ** 2:
        return best[0], best[1]
    return x, y


def _owner(o, b):
    x = b[0]['x']
    y = b[0]['y']
    best = min(range(len(o.panels)), key=lambda n: (0 if o.panels[n][1] - 30 <= y <= o.panels[n][3] + 30 else 1,
                                                    abs((o.panels[n][0] + o.panels[n][2]) / 2 - x)))
    return best


def join2(lines):
    """Join wrapped lines back into sentences, but only lines of one style."""
    out = []
    for it in sorted(lines, key=lambda i: i['y']):
        if out and out[-1]['style'] == it['style'] and abs(out[-1]['size'] - it['size']) < .6 \
                and out[-1]['weight'] == it['weight'] and not re.search(r'[.:!?”]$', out[-1]['text']):
            out[-1] = dict(out[-1], text=out[-1]['text'] + ' ' + it['text'])
        elif out and out[-1]['style'] == it['style'] and abs(out[-1]['size'] - it['size']) < .6 \
                and out[-1]['weight'] == it['weight'] and it['text'][:1].islower():
            out[-1] = dict(out[-1], text=out[-1]['text'] + ' ' + it['text'])
        else:
            out.append(dict(it))
    return out


def _block(c, b, o=None):
    b = sorted(b, key=lambda i: i['y'])
    lead = [b[0]] if (b[0]['weight'] == '700' or b[0]['sc']) and len(b) > 1 else []
    x, wd = PAD, INNER
    if o is not None and b[0]['anchor'] == 'start':
        sym = _symbol(o, b[0]['x'] - 14, b[0]['y'] - 4)
        if sym != '<svg></svg>':
            a, _ = art(None, b[0]['x'] - 27, b[0]['y'] - 13, b[0]['x'] - 1, b[0]['y'] + 5, 26, PAD, c.y + 1,
                       raw=sym)
            c.add(a)
            x, wd = PAD + 30, INNER - 30
    for j, q in enumerate(lead + join2(b[len(lead):])):
        bold = q['weight'] == '700' or q['sc']
        c.para(q['text'], 15 if bold else T_NOTE, q['fill'] if bold else (NOTE if q['style'] == 'italic' else BODY),
               'normal' if bold else q['style'], '700' if bold else '400', sc=q['sc'], gap=3, x=x, width=wd)
    c.y += 5


# ───────────────────────────────────────────── on the page
FIG = re.compile(r'(<div class="fignum">[^<]*Map</div><div class="figtitle">(.*?)</div><div class="figwrap"[^>]*>)'
                 r'(<svg\b.*?</svg>)', re.S)

CSS = ('<style id="%s">.figwrap svg.phonemap{display:none}'
       '@media (max-width:760px){.figwrap svg.phonemap{display:block!important;width:100%%!important;'
       'min-width:0!important;max-width:520px!important;height:auto!important;margin:0 auto}'
       '.figwrap svg.fullmap{display:none!important}}'
       '@media print{.figwrap svg.phonemap{display:none!important}.figwrap svg.fullmap{display:block!important}}'
       '</style>' % MARK)


def apply(h, report=True):
    if MARK in h:
        return h
    n = [0]

    def sub(m):
        title = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        full = m.group(3)
        n[0] += 1
        ph = phone_map(full, _html.unescape(title), 'pm%d' % n[0])
        if not ph:
            return m.group(0)
        full = re.sub(r'<svg\b', '<svg class="fullmap"', full, count=1)
        return m.group(1) + ph + full
    h = FIG.sub(sub, h)
    h = h.replace('</head>', CSS + '</head>', 1)
    if report:
        print('phone_maps: %d maps given a phone plate' % n[0])
    return h


def strip(h):
    """For print: drop the phone plates, keep the full maps."""
    h = re.sub(r'<svg viewBox="[^"]*" width="100%" role="img" aria-label="[^"]*" class="phonefig phonemap">.*?'
               r'(?=<svg class="fullmap")', '', h, flags=re.S)
    return h.replace('<svg class="fullmap"', '<svg', )
