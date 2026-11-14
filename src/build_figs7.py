# -*- coding: utf-8 -*-
"""v82: the older drawn figures, redrawn phone-first.

Up to v81 twenty-three charts, diagrams, timelines and tables were still the
860-unit drawings of v60, shown at a phone's width with their smallest text at
four to six pixels. Each is redrawn here in the style of the v80 plates
(src/build_figs6.py): 400 units wide, shown 1:1 on a phone, nothing set under
14 units, the evidence colours of docs/MAP_STYLE.md.

Nothing is retyped. Every word, number and colour is read from the drawing the
v81 book printed, frozen in data/fig_v81/ by tools/freeze_v81_figs.py, and
tools/check_redraw.py proves that every word of each old drawing is in its
redraw. Only the layout changes: wide rows become stacked cards, horizontal
time axes become vertical ones, and pictures keep their drawing with the labels
set beside them in numbered keys.
"""
import html as _html
import json
import os
import re

from build_figs6 import W, AXIS, RULE, TINT, GOLD, T_LAB, T_NOTE, esc, svg as _svg
from map_style import INK, BODY, NOTE, DOC, DOC_DEEP, MEM, MEM_LIGHT, CONTEXT, FONT

HERE = os.path.dirname(os.path.abspath(__file__))
OLD = os.path.join(os.path.dirname(HERE), 'data', 'fig_v81')
INDEX = json.load(open(os.path.join(OLD, 'INDEX.json'), encoding='utf-8'))

T_HEAD = 16
PAD = 8
CW = {'normal': .47, 'italic': .45, 'bold': .52, 'sc': .62}


# ───────────────────────────────────────────── reading a frozen drawing
class Old:
    def __init__(self, title):
        self.title = title
        self.raw = open(os.path.join(OLD, INDEX[title]['slug'] + '.svg'), encoding='utf-8').read()
        self.items = []
        seen = set()
        for m in re.finditer(r'<text\b([^>]*)>(.*?)</text>', self.raw, re.S):
            a, body = m.group(1), m.group(2)
            if ' stroke=' in a:
                continue                     # a halo copy
            txt = _html.unescape(re.sub(r'<[^>]+>', '', body)).strip()
            if not txt:
                continue
            g = lambda k, d=None: (re.search(r'\b%s="([^"]*)"' % k, a) or [None, d])[1]
            it = dict(x=float(g('x', 0)), y=float(g('y', 0)), size=float(g('font-size', 12)),
                      fill=g('fill', INK), weight=g('font-weight', '400'), style=g('font-style', 'normal'),
                      anchor=g('text-anchor', 'start'), sc='small-caps' in a, text=txt)
            key = (round(it['x']), round(it['y']), txt)
            if key in seen:
                continue
            seen.add(key)
            self.items.append(it)

    def find(self, sub, nth=0):
        hits = [i for i in self.items if sub in i['text']]
        return hits[nth]

    def where(self, x0=-1e9, x1=1e9, y0=-1e9, y1=1e9):
        return [i for i in self.items if x0 <= i['x'] < x1 and y0 <= i['y'] < y1]

    def shapes(self, tag):
        out = []
        for m in re.finditer(r'<%s\b([^>]*)/?>' % tag, self.raw):
            a = m.group(1)
            d = dict(re.findall(r'([\w-]+)="([^"]*)"', a))
            out.append(d)
        return out


def joinlines(items):
    """Old drawings wrap a sentence over several <text> lines; put them back
    together, starting a new paragraph after a full stop."""
    paras, cur = [], None
    for it in sorted(items, key=lambda i: (i['y'], i['x'])):
        if cur and not re.search(r'[.:!?”]$', cur['text']) and abs(it['size'] - cur['size']) < .6:
            cur['text'] += ' ' + it['text']
        else:
            cur = dict(it)
            paras.append(cur)
    return paras


# ───────────────────────────────────────────── drawing
def wrap(s, size, width, kind='normal'):
    f = CW[kind]
    caps = sum(ch.isupper() for ch in s) / max(1, sum(ch.isalpha() for ch in s))
    f *= 1 + .45 * caps
    per = max(6, int(width / (size * f)))
    words, lines, cur = s.split(), [], ''
    for w in words:
        if cur and len(cur) + 1 + len(w) > per:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + ' ' + w).strip()
    if cur:
        lines.append(cur)
    return lines


def tx(x, y, s, size=T_LAB, fill=INK, anchor='start', weight='400', style='normal', sc=False, ls=None):
    extra = ' style="font-variant:small-caps"' if sc else ''
    if ls is not None:
        extra += f' letter-spacing="{ls}"'
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}" font-style="{style}" font-family="{FONT}"{extra}>{esc(s)}</text>')


def kind_of(weight, style, sc):
    return 'sc' if sc else ('bold' if weight == '700' else ('italic' if style == 'italic' else 'normal'))


class Canvas:
    def __init__(self, top=6):
        self.o = []
        self.y = top

    def add(self, *s):
        self.o.extend(s)

    def para(self, s, size=T_NOTE, fill=NOTE, style='italic', weight='400', x=PAD, width=W - 2 * PAD,
             gap=8, sc=False, anchor='start', lead=1.28):
        lines = wrap(s, size, width, kind_of(weight, style, sc))
        for i, ln in enumerate(lines):
            xx = x + width / 2 if anchor == 'middle' else x
            self.add(tx(xx, self.y + size + i * size * lead, ln, size, fill, anchor, weight, style, sc))
        self.y += size * .25 + len(lines) * size * lead + gap
        return len(lines)

    def kicker(self, s, fill=GOLD, gap=6):
        self.para(s, 15, fill, 'normal', '700', sc=True, gap=gap)

    def rule(self, gap=14):
        self.add(f'<line x1="{PAD}" y1="{self.y+2:.1f}" x2="{W-PAD}" y2="{self.y+2:.1f}" stroke="{RULE}"/>')
        self.y += gap

    def item(self, it, size=None, width=W - 2 * PAD, x=PAD, gap=8, fill=None, style=None, weight=None):
        """Re-set one old text item (or a joined paragraph) at a phone size."""
        size = size or max(T_NOTE, min(17, round(it['size'] * 1.2)))
        st = style or it['style']
        wt = weight or it['weight']
        return self.para(it['text'], size, fill or it['fill'], st, wt, x=x, width=width, gap=gap, sc=it['sc'])

    def svg(self, label, bottom=4):
        return _svg(self.y + bottom, label, ''.join(self.o))


def chip(x, y, w, h, fill, stroke=None, rx=3, opacity=None, dash=None):
    a = f' stroke="{stroke}"' if stroke else ''
    a += f' opacity="{opacity}"' if opacity else ''
    a += f' stroke-dasharray="{dash}"' if dash else ''
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}"{a}/>'


def lum(hexcol):
    h = hexcol.lstrip('#')
    if len(h) != 6:
        return 1
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return .2126 * r + .7152 * g + .0722 * b


def on(fill):
    return '#FFFFFF' if lum(fill) < .5 else INK


def head_and_lede(c, o, below=70):
    """The kicker and the one-line lede most old drawings open with."""
    for k, it in enumerate(sorted(o.where(y1=below), key=lambda i: i['y'])):
        if it['sc'] or it['size'] >= 14 and it['weight'] == '700' or (k == 0 and it['y'] < 40):
            c.kicker(it['text'])
        else:
            c.item(it, T_NOTE, style='italic', fill=NOTE)
    c.y += 2


def tail(c, o, y0, rule=True):
    """The closing notes under an old drawing, as paragraphs."""
    its = o.where(y0=y0)
    if not its:
        return
    if rule:
        c.rule()
    for p in joinlines(its):
        bold = p['weight'] == '700' or p['sc'] or p['size'] >= 13.5
        c.para(p['text'], 15 if bold else T_NOTE, INK if bold else (BODY if p['style'] != 'italic' else NOTE),
               'normal' if bold else p['style'], '700' if bold else '400', sc=p['sc'], gap=6)


GRADE = {'scripture': ('#D5E9DF', INK), 'the join': ('#8FBFA6', INK), 'classical': ('#A9CDB8', INK),
         'attested': ('#79B491', INK), 'no evidence': ('#FDF6EC', '#8A5A1E'), 'documents': (DOC, '#FFFFFF')}


# ═════════════════════════════════════════════ 0.1 · the chain, link by link
def fig_chain():
    o = Old('The chain, link by link — built from the sources')
    c = Canvas()
    head_and_lede(c, o, 60)
    hdr = [i['text'] for i in sorted(o.where(y0=60, y1=80), key=lambda i: i['x'])]
    c.para('Each card: ' + ' · '.join(hdr), T_NOTE, NOTE, 'italic', gap=10)
    starts = sorted(i['y'] for i in o.items if i['x'] == 56 and i['text'].startswith('link '))
    for k, y in enumerate(starts):
        blk = o.where(y0=y - 12, y1=y + 84)
        lab = next(i for i in blk if i['x'] == 56 and i['text'].startswith('link '))
        carried = ' '.join(i['text'] for i in sorted(blk, key=lambda i: i['y']) if i['x'] == 126)
        main = sorted([i for i in blk if i['x'] == 240], key=lambda i: i['y'])
        brk = ' '.join(i['text'] for i in sorted(blk, key=lambda i: i['y']) if i['x'] == 134)
        side = sorted([i for i in blk if i['x'] >= 760], key=lambda i: i['y'])
        grade = side[0]['text']
        extra = ' · '.join(i['text'] for i in side[1:])
        fill, tc = GRADE[grade]
        top = c.y
        c.add(chip(PAD, top, W - 2 * PAD, 24, fill, '#C9A46A' if grade == 'no evidence' else None,
                   dash='4 3' if grade == 'no evidence' else None))
        c.add(tx(PAD + 10, top + 17, lab['text'], 15, tc, 'start', '700', sc=True))
        c.add(tx(W - PAD - 10, top + 17, grade, T_NOTE, tc, 'end', '400', 'italic'))
        c.y = top + 30
        c.para(main[0]['text'], 17 if main[0]['size'] < 16 else 18, INK, 'normal', '700', x=PAD + 6,
               width=W - 2 * PAD - 12, gap=4, sc=main[0]['sc'])
        c.para('carried by ' + carried, T_NOTE, DOC_DEEP, 'italic', x=PAD + 6, width=W - 2 * PAD - 12, gap=4)
        for it in main[1:]:
            c.para(it['text'], T_NOTE if it['size'] < 11.4 else 15, BODY, it['style'], x=PAD + 6,
                   width=W - 2 * PAD - 12, gap=4)
        if extra:
            c.para(extra, 15, '#8A5A1E', 'normal', '700', x=PAD + 6, width=W - 2 * PAD - 12, gap=4)
        c.y += 2
        c.add(tx(PAD + 6, c.y + 13, 'breaks if', T_NOTE, MEM, 'start', '700', sc=True))
        c.y += 2
        c.para(brk, T_NOTE, BODY, 'normal', x=PAD + 76, width=W - 2 * PAD - 82, gap=14)
    tail(c, o, 980)
    return c.svg('The family chain in nine links, each with its source, its span, its grade and what would break it')


# ═════════════════════════════════════════════ 1.1 · the three texts
def fig_adam():
    o = Old('A line to Adam implies a date for Adam')
    c = Canvas()
    head_and_lede(c, o, 60)
    bars = [r for r in o.shapes('rect') if float(r.get('height', 0)) == 34]
    rows = sorted(o.where(x0=190, x1=200, y0=80, y1=220), key=lambda i: i['y'])
    mx = 3314
    x0, x1 = PAD, W - PAD
    sc = (x1 - x0) / mx
    for i, row in enumerate(rows):
        a, b = bars[2 * i], bars[2 * i + 1]
        nums = sorted(o.where(x0=220, y0=row['y'] - 2, y1=row['y'] + 2), key=lambda j: j['x'])
        v1, v2 = (int(n['text'].replace(',', '')) for n in nums[:2])
        c.add(tx(PAD, c.y + 15, row['text'], 15, INK, 'start', '700'))
        c.add(tx(W - PAD, c.y + 15, nums[2]['text'], 15, INK, 'end', '700'))
        c.y += 22
        w1, w2 = v1 * sc, v2 * sc
        c.add(chip(x0, c.y, w1, 26, a['fill']), chip(x0 + w1 + 2, c.y, w2, 26, b['fill'], opacity=b.get('opacity')))
        c.add(tx(x0 + 8, c.y + 18, nums[0]['text'], 15, '#FFFFFF', 'start', '700'))
        c.add(tx(x0 + w1 + 2 + w2 / 2, c.y + 18, nums[1]['text'], T_NOTE, INK, 'middle', '700'))
        c.y += 38
    leg = sorted(o.where(y0=240, y1=260), key=lambda i: i['x'])
    lx = PAD
    for k, it in enumerate(leg):
        c.add(chip(lx, c.y + 3, 13, 13, '#6B6760', opacity='.42' if k else None, rx=2))
        c.add(tx(lx + 19, c.y + 14, it['text'], T_NOTE, BODY))
        lx += 34 + len(it['text']) * 6.5
        if lx > W - 150:
            lx = PAD
            c.y += 20
    c.y += 26
    tail(c, o, 270)
    return c.svg('Years from creation to Abraham in the Masoretic, Septuagint and Samaritan texts')


# ═════════════════════════════════════════════ 1.2 · the branch at ʿĀbir
def fig_branch():
    o = Old('The branch at ʿĀbir — where this line leaves Abraham’s')
    c = Canvas()
    head_and_lede(c, o, 60)
    trunk = sorted(o.where(x0=420, x1=440, y0=90, y1=540), key=lambda i: i['y'])
    lxx = o.find('LXX only')
    c.kicker(trunk[0]['text'], DOC_DEEP)
    cx = W / 2
    y0 = c.y
    for it in trunk[1:]:
        big = it['size'] >= 19
        if 'GENESIS 10:25' in it['text']:
            c.y += 4
            c.para(it['text'], T_NOTE, NOTE, 'italic', anchor='middle', gap=6)
            continue
        c.add(f'<circle cx="{cx}" cy="{c.y+9:.1f}" r="3" fill="{MEM if big else DOC}"/>')
        lab = it['text'] + ('  · ' + lxx['text'] if it['text'] == '(Kainan)' else '')
        c.add(tx(cx + 10, c.y + 14, lab, 19 if big else 15, INK, 'start', '700' if big else '400', sc=it['sc']))
        c.y += 26 if big else 21
    c.add(f'<line x1="{cx}" y1="{y0+9}" x2="{cx}" y2="{c.y-40:.1f}" stroke="{DOC}" stroke-width="1.2"/>')
    # the two branches, side by side
    c.y += 6
    colw = (W - 2 * PAD - 12) / 2
    top = c.y
    for k, (xa, xb) in enumerate(((150, 200), (670, 720))):
        col = sorted(o.where(x0=xa - 10, x1=xa + 50, y0=560, y1=900), key=lambda i: (i['y'], i['x']))
        x = PAD + k * (colw + 12)
        c.y = top
        head = col[0]
        hl = wrap(head['text'], 14, colw - 12, 'sc')
        c.add(chip(x, c.y, colw, 10 + 16 * len(hl), '#EFEBE3' if k == 0 else '#DFEEE6'))
        for j, ln in enumerate(hl):
            c.add(tx(x + 6, c.y + 18 + j * 16, ln, 14, MEM if k == 0 else DOC_DEEP, 'start', '700', sc=True))
        c.y += 34 + 16 * (len(wrap(head['text'], 14, colw - 12, 'sc')) - 1)
        rows = {}
        for it in col[1:]:
            rows.setdefault(round(it['y']), []).append(it)
        for y in sorted(rows):
            nm = [i for i in rows[y] if i['size'] >= 13]
            note = [i for i in rows[y] if i['size'] < 13]
            n = nm[0]
            big = n['size'] >= 18
            c.add(tx(x + 4, c.y + 15, n['text'], 17 if big else 15, INK, 'start', '700' if big else '400', sc=n['sc']))
            if note:
                if len(n['text']) * (10.5 if big else 7.2) + len(note[0]['text']) * 6.4 + 10 > colw:
                    c.y += 18
                c.add(tx(x + colw - 2, c.y + 15, note[0]['text'], T_NOTE, NOTE, 'end', '400', 'italic'))
            c.y += 21
        if k == 0:
            left_end = c.y
    c.y = max(c.y, left_end) + 8
    tail(c, o, 930)
    return c.svg('Genesis 5, 10 and 11: the shared line from Adam to ʿĀbir, and the two branches at his sons')


# ═════════════════════════════════════════════ 1.3 · the tell
def fig_tell():
    o = Old('The land, drawn as a tell — fifteen thousand years of layering')
    c = Canvas()
    head_and_lede(c, o, 70)
    bands = [r for r in o.shapes('rect') if r.get('x') == '40' and r.get('width') == '250' and r.get('fill', 'none') != 'none']
    mark = [r for r in o.shapes('rect') if r.get('stroke') == '#C49A5E']
    for b in bands:
        y0, h = float(b['y']), float(b['height'])
        lab = [i for i in o.where(x0=50, x1=60, y0=y0, y1=y0 + h)]
        name, date = sorted(lab, key=lambda i: i['y'])[:2]
        desc = o.where(x0=290, y0=y0 - 2, y1=y0 + h - 1)
        arrive = [i for i in desc if 'we arrive' in i['text']]
        desc = [i for i in desc if 'we arrive' not in i['text']]
        fill = b['fill']
        fg = on(fill)
        hl = any(m['y'] == b['y'] for m in mark)
        c.add(chip(PAD, c.y, W - 2 * PAD, 26, fill, '#C49A5E' if hl else None, rx=2))
        if hl:
            c.o[-1] = c.o[-1].replace('/>', ' stroke-width="3"/>')
        c.add(tx(PAD + 8, c.y + 18, name['text'], 15, fg, 'start', '700', sc=True))
        c.add(tx(W - PAD - 8, c.y + 18, date['text'], T_NOTE, fg, 'end', '400', 'italic', sc=date['sc']))
        c.y += 30
        for a in arrive:
            c.add(f'<path d="M{PAD+10} {c.y+9} l9 -6 v12 z" fill="{MEM}"/>')
            c.add(tx(PAD + 24, c.y + 14, a['text'].replace('◀', '').strip(), 15, MEM, 'start', '700', sc=True))
            c.y += 20
        for p in joinlines(desc):
            c.para(p['text'], 15, BODY, 'normal', '700' if p['weight'] == '700' else '400', x=PAD + 6,
                   width=W - 2 * PAD - 12, gap=2)
        c.y += 8
    tail(c, o, 760)
    return c.svg('The district as a dug section: fifteen layers from the Palaeolithic to today')


# ═════════════════════════════════════════════ 1.7 · how a people is made
def fig_people():
    o = Old('How a people is made')
    c = Canvas()
    head_and_lede(c, o, 60)
    ticks = sorted(o.where(y0=70, y1=85), key=lambda i: i['x'])
    tx_ = [(i['x'], i['text']) for i in ticks]
    x0, x1 = 268.0, 812.0
    X = lambda x: PAD + 4 + (x - x0) / (x1 - x0) * (W - 2 * PAD - 8)
    circles = [ci for ci in o.shapes('circle')]
    rects = [r for r in o.shapes('rect') if r.get('height') == '16']
    names = sorted([i for i in o.where(x0=250, x1=255, y0=90, y1=480) if i['size'] >= 10.5], key=lambda i: i['y'])
    notes = {round(i['y']): i for i in o.where(x0=250, x1=255, y0=90, y1=480) if i['size'] < 10.5}
    side = [i for i in o.items if i['x'] > 470 and 190 < i['y'] < 450 and i['size'] < 10.5]
    # axis on top, labels staggered over two rows
    c.add(f'<line x1="{PAD}" y1="{c.y+36:.1f}" x2="{W-PAD}" y2="{c.y+36:.1f}" stroke="{AXIS}"/>')
    for k, (xx, lab) in enumerate(tx_):
        anc = 'start' if k == 0 else ('end' if k == len(tx_) - 1 else 'middle')
        c.add(tx(X(xx), c.y + 14 + (k % 2) * 16, lab, T_NOTE, NOTE, anc))
        c.add(f'<line x1="{X(xx):.1f}" y1="{c.y+32:.1f}" x2="{X(xx):.1f}" y2="{c.y+36:.1f}" stroke="{AXIS}"/>')
    c.y += 46
    owner = {}
    for s_ in side:
        n_ = min((n for n in names if n['y'] <= s_['y'] + 6), key=lambda n: s_['y'] - n['y'])
        owner.setdefault(id(n_), []).append(s_)
    for n in names:
        ny = n['y']
        note = notes.get(round(ny + 12))
        ci = min(circles, key=lambda q: abs(float(q['cy']) - (ny + 2)) if 'cy' in q else 1e9)
        rr = min(rects, key=lambda q: abs(float(q['y']) - (ny - 6)))
        col = ci['fill']
        c.add(tx(PAD, c.y + 15, n['text'], 15, n['fill'], 'start', '700', sc=n['sc']))
        c.y += 20
        if note:
            c.para(note['text'], T_NOTE, NOTE, 'italic', gap=0, x=PAD, width=W - 2 * PAD)
        yb = c.y + 4
        bx = X(float(rr['x']))
        bw = X(float(rr['x']) + float(rr['width'])) - bx
        solid = rr['fill'].startswith('#')
        c.add(chip(bx, yb, max(bw, 4), 10, col, opacity=None if solid else '.35', rx=2))
        c.add(f'<circle cx="{bx:.1f}" cy="{yb+5:.1f}" r="6" fill="{col}" stroke="#FFFFFF" stroke-width="1.4"/>')
        for s_ in owner.get(id(n), []):
            if 'two centuries' in s_['text']:
                a_, b_ = X(324.7), X(474.7)
                c.add(f'<path d="M{a_:.1f} {yb+18:.1f} H{b_:.1f} M{a_:.1f} {yb+14:.1f} v8 M{b_:.1f} {yb+14:.1f} v8" stroke="{col}" stroke-width="1.3" fill="none"/>')
                c.add(tx(b_ + 6, yb + 23, s_['text'], T_NOTE, NOTE, 'start', '400', 'italic'))
            else:
                c.add(tx(W - PAD, yb + 27, s_['text'], T_NOTE, NOTE, 'end', '400', 'italic'))
            yb += 18
        c.y = yb + 22
    # the river
    fin = o.where(y0=510, y1=540)
    c.add(chip(PAD, c.y, W - 2 * PAD, 30, DOC))
    for it in fin:
        if it['x'] == 280:
            c.add(tx(PAD + 10, c.y + 20, it['text'], 15, '#FFFFFF', 'start', '700'))
        if it['x'] == 800:
            c.add(tx(W - PAD - 10, c.y + 20, it['text'], 15, '#FFFFFF', 'end', '700', sc=True))
    c.y += 36
    for it in sorted([i for i in fin if i['x'] == 252], key=lambda i: i['y']):
        c.para(it['text'], 15 if it['size'] > 10 else T_NOTE, DOC_DEEP if it['size'] > 10 else NOTE,
               'normal' if it['size'] > 10 else 'italic', '700' if it['size'] > 10 else '400', gap=2)
    tail(c, o, 600)
    return c.svg('Ten arrivals into one people, from the Canaanites to the Palestinians')


# ───────────────────────────────────────────── a picture kept, its labels keyed
def art(o, x0, y0, x1, y1, width=W - 2 * PAD, x=PAD, y=0):
    """The old drawing's own artwork (no text) for the box x0..x1, y0..y1, scaled to width."""
    body = re.search(r'<svg\b[^>]*>(.*)</svg>', o.raw, re.S).group(1)
    body = re.sub(r'<text\b.*?</text>', '', body, flags=re.S)
    body = re.sub(r'<rect width="860" height="[\d.]+" fill="#FFFFFF"/>', '', body)
    h = width * (y1 - y0) / (x1 - x0)
    return (f'<svg x="{x}" y="{y:.1f}" width="{width:.1f}" height="{h:.1f}" viewBox="{x0} {y0} {x1-x0} {y1-y0}" '
            f'preserveAspectRatio="xMidYMid meet" overflow="hidden">{body}</svg>'), h


def badge(x, y, n, fill=GOLD):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="10" fill="{fill}" stroke="#FFFFFF" stroke-width="1.5"/>'
            + tx(x, y + 5, str(n), T_NOTE, '#FFFFFF', 'middle', '700'))


def keyed_art(c, o, box, labels, width=W - 2 * PAD):
    """Draw the artwork in box with a numbered badge at each label's place, then the key."""
    x0, y0, x1, y1 = box
    a, h = art(o, x0, y0, x1, y1, width, PAD, c.y)
    c.add(a)
    k = (width) / (x1 - x0)
    for n, (lx, ly, _) in enumerate(labels, 1):
        c.add(badge(PAD + (lx - x0) * k, c.y + (ly - y0) * k, n))
    c.y += h + 10
    for n, (_, _, text) in enumerate(labels, 1):
        top = c.y
        c.add(badge(PAD + 10, top + 10, n))
        c.para(text, 15, BODY, 'normal', x=PAD + 26, width=W - 2 * PAD - 26, gap=6)


# ═════════════════════════════════════════════ 1.8 · the terraces
def fig_terraces():
    o = Old('The terraces, and one of the towers standing in them')
    c = Canvas()
    head_and_lede(c, o, 60)
    tower = ' '.join(i['text'] for i in o.where(x0=220, x1=230, y0=195, y1=220))
    ridge = o.find('the ridge, and the village')
    keyed_art(c, o, (36, 80, 570, 362), [(212, 196, tower), (500, 96, ridge['text'])])
    for it in sorted(o.where(x0=50, x1=60, y0=360, y1=395), key=lambda i: i['y']):
        c.item(it, 15 if it['weight'] == '700' else T_NOTE, gap=4)
    c.rule()
    # the roof section, its own drawing
    heads = sorted(o.where(x0=595, x1=605, y0=100, y1=135), key=lambda i: i['y'])
    for it in heads:
        c.item(it, 15 if it['sc'] else T_NOTE, gap=2)
    a, h = art(o, 640, 128, 780, 272, 180, (W - 180) / 2, c.y + 4)
    c.add(a)
    c.y += h + 12
    for p in joinlines(o.where(x0=595, x1=605, y0=275, y1=345)):
        c.para(p['text'], 15, BODY, p['style'], gap=4)
    c.rule()
    # the farming year
    for it in o.where(y0=400, y1=412):
        c.item(it, 15 if it['sc'] else T_NOTE, gap=2)
    c.y += 4
    months = sorted(o.where(y0=428, y1=436), key=lambda i: i['x'])
    cw = (W - 2 * PAD) / 12
    for k, m in enumerate(months):
        c.add(chip(PAD + k * cw, c.y, cw - 2, 22, '#F7F4EE', '#D9D4C8', rx=1))
        c.add(tx(PAD + k * cw + cw / 2 - 1, c.y + 16, m['text'], T_NOTE, NOTE, 'middle'))
    c.y += 28
    bars = [r for r in o.shapes('rect') if r.get('height') == '13']
    labs = sorted(o.where(y0=445, y1=490), key=lambda i: i['y'])
    for r, lab in zip(sorted(bars, key=lambda r: float(r['y'])), labs):
        m0 = round((float(r['x']) - 40) / 65)
        m1 = round((float(r['x']) + float(r['width']) - 40) / 65)
        bx, bw = PAD + m0 * cw, (m1 - m0) * cw - 2
        c.add(chip(bx, c.y, bw, 22, r['fill'], r['fill'], opacity='.2'))
        c.add(chip(bx, c.y, bw, 22, 'none', r['fill']))
        tw = len(lab['text']) * 7
        if tw < bw - 8:
            c.add(tx(bx + 6, c.y + 16, lab['text'], T_NOTE, INK, 'start', '700'))
        elif bx > W / 2:
            c.add(tx(bx - 6, c.y + 16, lab['text'], T_NOTE, INK, 'end', '700'))
        else:
            c.add(tx(bx + bw + 6, c.y + 16, lab['text'], T_NOTE, INK, 'start', '700'))
        c.y += 27
    c.rule()
    # four numbers, two by two
    nums = sorted(o.where(y0=515, y1=530, x1=700), key=lambda i: i['x'])
    nums = [i for i in nums if i['size'] > 20]
    gw = (W - 2 * PAD) / 2
    for k, n in enumerate(nums):
        gx, gy = PAD + (k % 2) * gw, c.y + (k // 2) * 62
        words = ' '.join(i['text'] for i in sorted(o.where(x0=n['x'] + 20, x1=n['x'] + 200, y0=512, y1=535), key=lambda i: i['y']))
        c.add(tx(gx, gy + 26, n['text'], 26, n['fill'], 'start', '700'))
        for j, ln in enumerate(wrap(words, T_NOTE, gw - 12)):
            c.add(tx(gx, gy + 44 + j * 16, ln, T_NOTE, BODY))
    c.y += 2 * 62 + 14
    return c.svg('A terraced hillside above Ramallah in section, with a field watchtower, its roof, and its months of use')


# ═════════════════════════════════════════════ 2.1 · the highlands fill up
def fig_highlands():
    o = Old('The highlands fill up, and nowhere else empties out')
    c = Canvas()
    head_and_lede(c, o, 60)
    dots = [ci for ci in o.shapes('circle')]
    cols = {}
    for d in dots:
        cols.setdefault('lb' if float(d['cx']) < 280 else 'ia', []).append(d)
    for key, x in (('lb', 56), ('ia', 300)):
        its = sorted(o.where(x0=x - 1, x1=x + 1, y0=90, y1=340), key=lambda i: i['y'])
        c.add(tx(PAD, c.y + 16, its[0]['text'], 16, INK, 'start', '700', sc=its[0]['sc']))
        c.add(tx(W - PAD, c.y + 16, its[1]['text'], T_NOTE, NOTE, 'end', '400', 'italic'))
        c.y += 26
        ds = cols[key]
        n = len(ds)
        per = 25
        fill = ds[0].get('fill', DOC)
        for k in range(n):
            cx, cy = PAD + 7 + (k % per) * 15.2, c.y + 7 + (k // per) * 15
            c.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="5" fill="{fill}"/>')
        c.y += ((n - 1) // per + 1) * 15 + 6
        c.para(its[2]['text'], 15, INK, 'normal', '700', gap=14)
    c.rule()
    for it in sorted(o.where(y0=400, y1=530), key=lambda i: i['y']):
        if it['sc']:
            c.kicker(it['text'], DOC_DEEP)
        elif it['size'] > 11:
            c.para(it['text'], 15, INK, 'normal', '700', gap=2)
        else:
            c.para(it['text'], T_NOTE, BODY, 'normal', gap=8)
    tail(c, o, 550)
    return c.svg('Settlements found in the central hills: about 25 in the Late Bronze Age, about 250 in Iron Age I')


# ═════════════════════════════════════════════ 2.4 · the dam of Maʾrib
def fig_dam():
    o = Old('The machine that watered a kingdom')
    c = Canvas()
    head_and_lede(c, o, 60)
    lab = lambda sub: o.find(sub)
    labels = []
    for sub, at in (('wādī dhana', None), ('Jabal Balaq al-Awsaṭ', None), ('the northern sluice', None),
                    ('the dam', None), ('the southern sluice', None), ('Jabal Balaq al-Yamanī', None),
                    ('the northern garden', None), ('the southern garden', None)):
        it = lab(sub)
        extra = [j for j in o.items if j['x'] == it['x'] and it['y'] < j['y'] <= it['y'] + 40 and j['size'] < it['size']
                 and not j['sc']]
        txt = it['text'] + ('' if not extra else ': ' + ' '.join(e['text'] for e in sorted(extra, key=lambda e: e['y'])))
        labels.append((it['x'] + (8 if it['anchor'] == 'start' else 0), it['y'] - 4, txt))
    keyed_art(c, o, (30, 84, 830, 476), labels)
    quote = sorted([i for i in o.items if i['x'] == 700 and 255 < i['y'] < 315], key=lambda i: i['y'])
    c.para(' '.join(q['text'] for q in quote[:2]), 15, DOC_DEEP, 'italic', gap=2)
    c.para(' '.join(q['text'] for q in quote[2:]), T_NOTE, BODY, 'normal', gap=10)
    c.rule()
    for x in (40, 240, 420, 640):
        its = sorted(o.where(x0=x - 1, x1=x + 1, y0=490, y1=545), key=lambda i: i['y'])
        c.para(its[0]['text'], 16, MEM, 'normal', '700', sc=its[0]['sc'], gap=0)
        c.para(' '.join(i['text'] for i in its[1:]), T_NOTE, BODY, 'normal', gap=10)
    return c.svg('The dam of Maʾrib in schematic, with its sluices and its two gardens')


# ───────────────────────────────────────────── a time strip, from the old axis
class Strip:
    """Maps the old drawing's x (its time axis, ax0..ax1) onto the phone width."""
    def __init__(self, ax0, ax1, x0=PAD, x1=W - PAD):
        self.a0, self.a1, self.x0, self.x1 = ax0, ax1, x0, x1

    def X(self, x):
        return self.x0 + (float(x) - self.a0) / (self.a1 - self.a0) * (self.x1 - self.x0)

    def ticks(self, c, items, rows=2, every=1):
        """Tick labels under the strip, staggered so none touch."""
        items = sorted(items, key=lambda i: i['x'])
        y = c.y
        last = [-1e9] * rows
        for k, it in enumerate(items):
            x = self.X(it['x'])
            w = len(it['text']) * 6.8
            for r in range(rows):
                if x - w / 2 > last[r] + 6:
                    break
            else:
                r = rows - 1
            anc = 'middle'
            xx = min(max(x, self.x0 + w / 2), self.x1 - w / 2)
            c.add(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{y+4+r*16:.1f}" stroke="{AXIS}"/>')
            c.add(tx(xx, y + 17 + r * 16, it['text'], T_NOTE, NOTE, anc))
            last[r] = xx + w / 2
        c.y += 22 + 16 * (rows - 1)


def numbered_rows(c, rows, x=PAD):
    """rows: (marker svg-maker or colour, bold text, rest text)."""
    for mk, bold, rest in rows:
        top = c.y
        c.add(mk(x + 8, top + 10))
        if bold:
            c.para(bold, 15, INK, 'normal', '700', x=x + 24, width=W - 2 * PAD - 24, gap=0)
        if rest:
            c.para(rest, T_NOTE, BODY, 'normal', x=x + 24, width=W - 2 * PAD - 24, gap=0)
        c.y = max(c.y, top + 22) + 8


def dot(col, ring=None, shape='circle'):
    if shape == 'diamond':
        return lambda x, y: f'<rect x="{x-5}" y="{y-5}" width="10" height="10" fill="{col}" transform="rotate(45 {x} {y})"/>'
    if shape == 'num':
        return lambda x, y, n=ring: badge(x, y, n, col)
    return lambda x, y: f'<circle cx="{x}" cy="{y}" r="6" fill="{col}" stroke="#FFFFFF" stroke-width="1.5"/>'


# ═════════════════════════════════════════════ 3.1 · six sovereigns
def fig_sovereigns():
    o = Old('Six sovereigns, one people')
    c = Canvas()
    head_and_lede(c, o, 60)
    st = Strip(60, 820)
    bands = [r for r in o.shapes('rect') if r.get('y') == '82']
    rows = []
    c.add(tx(PAD, c.y + 14, o.find('who ruled')['text'], 15, INK, 'start', '700', sc=True))
    c.y += 22
    for k, b in enumerate(bands):
        x0, x1 = st.X(b['x']), st.X(float(b['x']) + float(b['width']))
        c.add(chip(x0, c.y, x1 - x0, 30, b['fill'], rx=0))
        c.add(tx((x0 + x1) / 2, c.y + 20, str(k + 1), T_NOTE, '#FFFFFF', 'middle', '700'))
        cx = float(b['x']) + float(b['width']) / 2
        lab = sorted([i for i in o.where(y0=100, y1=125) if abs(i['x'] - cx) < 30], key=lambda i: i['y'])
        rows.append((b['fill'], k + 1, lab))
    c.y += 36
    c.add(chip(PAD, c.y, W - 2 * PAD, 30, '#DFEEE6', rx=0))
    c.add(tx(PAD + 6, c.y + 20, o.find('who lived here')['text'], 15, DOC_DEEP, 'start', '700', sc=True))
    c.y += 36
    ev = [r for r in o.shapes('rect') if 'rotate' in r.get('transform', '')]
    for r in ev:
        x = st.X(float(r['x']) + 3.5)
        c.add(f'<rect x="{x-5:.1f}" y="{c.y-3:.1f}" width="10" height="10" fill="{MEM}" transform="rotate(45 {x:.1f} {c.y+2:.1f})"/>')
    c.y += 10
    st.ticks(c, o.where(y0=230, y1=242), rows=1)
    for it in sorted(o.where(y0=175, y1=205), key=lambda i: i['y']):
        c.para(it['text'], 15 if it['size'] > 10.2 else T_NOTE, DOC_DEEP if it['size'] > 10.2 else NOTE,
               'normal' if it['size'] > 10.2 else 'italic', gap=2)
    c.y += 8
    numbered_rows(c, [((lambda col, n: (lambda x, y: badge(x, y, n, col)))(col, n), lab[0]['text'],
                       ' '.join(l['text'] for l in lab[1:])) for col, n, lab in rows])
    numbered_rows(c, [(dot(MEM, shape='diamond'), it['text'], '') for it in sorted(o.where(y0=248, y1=260), key=lambda i: i['x'])])
    tail(c, o, 290)
    return c.svg('The rulers of the ridge from 539 to 63 BC, above the villages that stayed')


# ═════════════════════════════════════════════ 4.2 · the dam, and a date that moves
def fig_damdate():
    o = Old('The dam, and a date that has to move')
    c = Canvas()
    st = Strip(90, 800)
    c.y += 4
    top = c.y + 6
    c.add(f'<line x1="{PAD}" y1="{top+10}" x2="{W-PAD}" y2="{top+10}" stroke="{RULE}" stroke-width="2"/>')
    for r in o.shapes('rect'):
        if r.get('height') == '22':
            x0, x1 = st.X(r['x']), st.X(float(r['x']) + float(r['width']))
            c.add(chip(x0, top, max(x1 - x0, 6), 20, r['fill'], rx=3))
    for ci in o.shapes('circle'):
        c.add(f'<circle cx="{st.X(ci["cx"]):.1f}" cy="{top+10}" r="{ci["r"]}" fill="{ci["fill"]}"'
              + (f' opacity="{ci["opacity"]}"' if 'opacity' in ci else '') + ' stroke="#FFFFFF" stroke-width="1.5"/>')
    c.y = top + 24
    st.ticks(c, o.where(y0=110, y1=120), rows=2)
    c.y += 6
    tr = sorted(o.where(x0=170, x1=190, y0=55, y1=80), key=lambda i: i['y'])
    numbered_rows(c, [
        (dot(MEM), tr[0]['text'], tr[1]['text']),
        (lambda x, y: chip(x - 4, y - 8, 8, 16, DOC), o.find('449–450')['text'], ''),
        (lambda x, y: chip(x - 4, y - 8, 8, 16, DOC), o.find('543–548')['text'], o.find('CIH 541')['text']),
        (lambda x, y: f'<circle cx="{x}" cy="{y}" r="6" fill="{DOC}" opacity=".5"/>', o.find('final collapse')['text'], ''),
    ])
    tail(c, o, 150)
    return c.svg('The tradition’s date for the dam against its dated breaches')


# ═════════════════════════════════════════════ 7.6 · five datings
def fig_datings():
    o = Old('Five datings for one town — and they are not rivals')
    c = Canvas()
    head_and_lede(c, o, 45)
    st = Strip(90, 790)
    top = c.y + 6
    c.add(f'<line x1="{PAD}" y1="{top+8}" x2="{W-PAD}" y2="{top+8}" stroke="{RULE}" stroke-width="2"/>')
    marks = [ci for ci in o.shapes('circle')]
    for k, ci in enumerate(marks):
        c.add(badge(st.X(ci['cx']), top + 8, k + 1, ci['fill']))
    c.y = top + 22
    st.ticks(c, o.where(y0=184, y1=192), rows=2)
    c.y += 6
    rows = []
    for k, ci in enumerate(marks):
        cx = float(ci['cx'])
        its = [i for i in o.items if abs(i['x'] - cx) < .5 and i['y'] not in (188.0,) and not (184 <= i['y'] <= 192)]
        yr = next(i for i in its if i['size'] >= 13)
        rest = ' '.join(i['text'] for i in sorted(its, key=lambda i: i['y']) if i is not yr)
        rows.append(((lambda col, n: (lambda x, y: badge(x, y, n, col)))(ci['fill'], k + 1), yr['text'], rest))
    numbered_rows(c, rows)
    tail(c, o, 320)
    return c.svg('Five datings for Ramallah, 1279 to the early 1600s, in order')


# ═════════════════════════════════════════════ 5.2 · who ruled and who stayed
def fig_ruled():
    o = Old('Who ruled, and who stayed, 636–1517')
    c = Canvas()
    head_and_lede(c, o, 60)
    st = Strip(63.7, 818.8)
    bands = [r for r in o.shapes('rect') if r.get('y') == '80']
    c.add(tx(PAD, c.y + 14, o.find('who ruled')['text'], 15, INK, 'start', '700', sc=True))
    c.y += 22
    rows = []
    for k, b in enumerate(bands):
        x0, x1 = st.X(b['x']), st.X(float(b['x']) + float(b['width']))
        c.add(chip(x0, c.y, x1 - x0, 30, b['fill'], rx=0))
        cx = float(b['x']) + float(b['width']) / 2
        lab = sorted([i for i in o.where(y0=100, y1=120) if abs(i['x'] - cx) < 30], key=lambda i: i['y'])
        if lab:
            n = len(rows) + 1
            c.add(tx((x0 + x1) / 2, c.y + 20, chr(64 + n), T_NOTE, '#FFFFFF', 'middle', '700'))
            rows.append((b['fill'], chr(64 + n), lab))
    c.y += 36
    c.add(tx(PAD, c.y + 14, o.find('who stayed')['text'], 15, DOC_DEEP, 'start', '700', sc=True))
    c.y += 20
    c.para(o.find('the Christian villages of the ridge')['text'], T_NOTE, DOC_DEEP, 'italic', gap=6)
    # the traces as numbered marks along the strip, two rows
    tr = sorted([i for i in o.items if i['y'] in (182.2, 204.2, 193.2)], key=lambda i: int(i['text']))
    c.add(chip(PAD, c.y, W - 2 * PAD, 76, '#DFEEE6', rx=0))
    for i in tr:
        row = {182.2: 0, 204.2: 1, 193.2: 2}[i['y']]
        c.add(badge(st.X(i['x']), c.y + 14 + row * 24, i['text'], DOC if i['y'] != 193.2 else MEM))
    c.y += 82
    st.ticks(c, o.where(y0=232, y1=242), rows=2)
    c.y += 4
    numbered_rows(c, [((lambda col, n: (lambda x, y: badge(x, y, n, col)))(col, n), lab[0]['text'],
                       ' '.join(l['text'] for l in lab[1:])) for col, n, lab in rows])
    c.rule()
    lst = []
    for k in range(1, 12):
        num = [i for i in o.items if i['text'] == str(k) and i['x'] in (70.0, 460.0)][0]
        txt = [i for i in o.items if i['y'] == num['y'] and i['x'] == num['x'] + 14][0]
        lst.append(((lambda n, col: (lambda x, y: badge(x, y, n, col)))(k, MEM if 'RAMALLAH' in txt['text'] else DOC),
                    txt['text'], ''))
    numbered_rows(c, lst)
    tail(c, o, 400)
    return c.svg('The dynasties that ruled the ridge from 636 to 1517, and the dated traces of its Christians')


# ═════════════════════════════════════════════ 5.3 · forty-five is the wrong number
def fig_fortyfive():
    o = Old('Forty-five is the wrong number')
    c = Canvas()
    for p in joinlines(o.where(y1=70)):
        c.para(p['text'], T_NOTE, NOTE, 'italic', gap=10)
    st = Strip(250, 730)
    band = [r for r in o.shapes('rect') if r.get('opacity') == '.16'][0]
    bars = [r for r in o.shapes('rect') if r.get('height') == '22']
    lab = o.find('observed range')
    c.para(lab['text'], T_NOTE, DOC_DEEP, 'italic', gap=4)
    top = c.y
    bx0, bx1 = st.X(band['x']), st.X(float(band['x']) + float(band['width']))
    names = sorted(o.where(x0=230, x1=240, y0=110, y1=170), key=lambda i: i['y'])
    vals = sorted(o.where(x0=500, x1=630, y0=110, y1=175), key=lambda i: i['y'])
    h = 2 * 64 + 6
    c.add(chip(bx0, top, bx1 - bx0, h, DOC, opacity='.16'))
    y = top + 4
    for k, b in enumerate(bars):
        c.add(tx(PAD, y + 15, names[k]['text'], 16, INK, 'start', '700'))
        bw = st.X(float(b['x']) + float(b['width'])) - PAD
        c.add(chip(PAD, y + 22, bw, 20, b['fill']))
        v = [i for i in vals if abs(i['x'] - float(b['x']) - float(b['width']) - 10) < 2]
        c.add(tx(PAD, y + 58, v[0]['text'] + ' · ' + v[1]['text'], T_NOTE, BODY, 'start', '400', 'italic'))
        y += 64
    c.y = top + h + 6
    st.ticks(c, o.where(y0=190, y1=198), rows=1)
    c.para('years per generation', T_NOTE, NOTE, 'italic', anchor='middle', gap=8)
    tail(c, o, 225)
    return c.svg('Years per generation: forty-five generations against thirty-one, beside the observed range')


# ═════════════════════════════════════════════ 4.4 · twelve lands
def fig_lands():
    o = Old('Twelve lands, in the order he crossed them')
    c = Canvas()
    head_and_lede(c, o, 60)
    circles = {(round(float(ci['cx'])), round(float(ci['cy']))): ci for ci in o.shapes('circle') if 'cx' in ci}
    start = [i for i in o.items if i['x'] == 56.0 and i['y'] < 220]
    end = [i for i in o.items if i['x'] == 56.0 and 380 < i['y'] < 420]
    for it in sorted(start, key=lambda i: i['y']):
        c.para(it['text'], 15 if it['sc'] else T_NOTE, MEM if it['sc'] else NOTE, 'normal' if it['sc'] else 'italic',
               '700' if it['sc'] else '400', sc=it['sc'], gap=2)
    c.y += 6
    y0 = c.y
    for n in range(1, 13):
        num = [i for i in o.items if i['text'] == str(n) and i['y'] in (153.4, 303.4)][0]
        col = [i for i in o.items if abs(i['x'] - num['x']) < .5 and i is not num and abs(i['y'] - num['y']) < 60]
        ci = circles.get((round(num['x']), 150 if num['y'] < 200 else 300))
        big = ci and ci['fill'] == '#E8F3ED'
        name = max(col, key=lambda i: i['size'] if not i['sc'] else 0)
        rest = ' '.join(i['text'] for i in sorted(col, key=lambda i: i['y']) if i is not name)
        top = c.y
        stroke = ci['stroke'] if ci else AXIS
        c.add(f'<circle cx="{PAD+12}" cy="{top+11}" r="{12 if big else 10}" fill="{ci["fill"] if ci else "#FFFFFF"}" stroke="{stroke}" stroke-width="{2 if big else 1.2}"/>')
        c.add(tx(PAD + 12, top + 16, str(n), T_NOTE, DOC_DEEP if big else INK, 'middle', '700'))
        c.add(tx(PAD + 32, top + 16, name['text'], 16 if big else 15, DOC_DEEP if big else INK, 'start', '700'))
        c.y = top + 20
        c.para(rest, T_NOTE, BODY, 'italic', x=PAD + 32, width=W - 2 * PAD - 32, gap=0, sc=False)
        c.y = max(c.y, top + 26) + 8
    c.add(f'<line x1="{PAD+12}" y1="{y0+24}" x2="{PAD+12}" y2="{c.y-30:.1f}" stroke="{AXIS}" stroke-dasharray="3 3"/>')
    for it in sorted(end, key=lambda i: i['y']):
        c.para(it['text'], 15 if it['sc'] else T_NOTE, MEM if it['sc'] else NOTE, 'normal' if it['sc'] else 'italic',
               '700' if it['sc'] else '400', sc=it['sc'], gap=2)
    tail(c, o, 450)
    return c.svg('The twelve lands of the Riyam inscription, in the order the envoy crossed them')


# ═════════════════════════════════════════════ 2.5 · every biblical place
def fig_bible():
    o = Old('Every biblical place within a day’s walk, and the village it survived as')
    c = Canvas()
    head_and_lede(c, o, 60)
    hdr = [i['text'] for i in sorted(o.where(y0=110, y1=125), key=lambda i: i['x'])]
    c.para('Each card: ' + ' · '.join(hdr), T_NOTE, NOTE, 'italic', gap=10)
    pills = {round(float(r['y'])): r for r in o.shapes('rect') if r.get('height') == '15'}
    starts = sorted(i['y'] for i in o.items if i['x'] == 52 and i['size'] >= 11)
    for y in starts:
        blk = o.where(y0=y - 12, y1=y + 50)
        name = next(i for i in blk if i['x'] == 52 and i['size'] >= 11)
        refs = next(i for i in blk if i['x'] == 52 and i['size'] < 11)
        place = [i for i in blk if i['x'] == 252]
        dist = next(i for i in blk if i['x'] == 376)
        desc = ' '.join(i['text'] for i in sorted([i for i in blk if i['x'] == 444], key=lambda i: i['y']))
        grade = next(i for i in blk if i['x'] == 772)
        pill = min(pills.values(), key=lambda r: abs(float(r['y']) - y + 12))
        top = c.y
        c.add(tx(PAD, top + 17, name['text'], 18, INK, 'start', '700', sc=name['sc']))
        gw = len(grade['text']) * 7.2 + 16
        c.add(chip(W - PAD - gw, top + 3, gw, 20, pill['fill'], pill['stroke'], rx=10))
        c.add(tx(W - PAD - gw / 2, top + 17, grade['text'], T_NOTE, grade['fill'], 'middle', '700', 'italic'))
        c.y = top + 24
        c.para(refs['text'], T_NOTE, NOTE, 'italic', gap=2)
        line = place[0]['text'] + '  ·  ' + dist['text']
        c.add(tx(PAD, c.y + 15, line, 15, DOC_DEEP, 'start', '700'))
        if len(place) > 1:
            c.add(tx(W - PAD, c.y + 15, place[1]['text'], 16, DOC_DEEP, 'end'))
        c.y += 22
        c.para(desc, T_NOTE, BODY, 'normal', gap=6)
        c.rule(12)
    c.o.pop()
    c.y -= 12
    tail(c, o, 800)
    return c.svg('Nine biblical places near Ramallah and the Arabic villages that kept their names')


# ═════════════════════════════════════════════ 5.4 · the void, measured
def fig_void():
    o = Old('The void, measured — and shortened')
    c = Canvas()
    head_and_lede(c, o, 60)
    # the sum, as a small table
    lab = o.find('the sum')
    c.kicker(lab['text'], MEM)
    cols = sorted([i for i in o.where(y0=80, y1=100) if i is not lab and i['x'] > 100], key=lambda i: (i['x'], i['y']))
    pairs = {}
    for i in cols:
        pairs.setdefault(i['x'], []).append(i)
    cw = (W - 2 * PAD) / 3
    for k, x in enumerate(sorted(pairs)):
        a, b = sorted(pairs[x], key=lambda i: i['y'])
        gx, gy = PAD + (k % 3) * cw, c.y + (k // 3) * 44
        c.add(tx(gx, gy + 14, a['text'], T_NOTE, NOTE, 'start', '400', 'italic'))
        c.add(tx(gx, gy + 33, b['text'], 17, b['fill'], 'start', '700'))
    c.y += ((len(pairs) - 1) // 3 + 1) * 44 + 8
    c.rule()
    # the two gaps on a strip
    st = Strip(218.0, 638.8 + 21)
    st = Strip(260.1 - 42.07, 638.8 + 0)
    g1 = o.find('THE GAP IN OUR LINE')
    c.para(g1['text'], 15, MEM, 'normal', '700', gap=4)
    for x in (235.0, 650.8):
        its = sorted([i for i in o.items if i['x'] == x], key=lambda i: i['y'])
        c.para(its[0]['text'] + ': ' + ' '.join(i['text'] for i in its[1:]), T_NOTE, BODY, 'normal', gap=4, sc=False)
    top = c.y + 4
    x0, x1 = st.X(247.0), st.X(638.7)
    c.add(chip(x0, top, x1 - x0, 30, '#FAF5EC', '#E9D7BD', rx=0))
    c.add(f'<rect x="{x0-3:.1f}" y="{top-4}" width="5" height="38" fill="{DOC}"/>')
    c.add(f'<rect x="{x1-2:.1f}" y="{top-4}" width="5" height="38" fill="{DOC}"/>')
    c.add(tx((x0 + x1) / 2, top + 20, o.find('the chart draws one line')['text'], T_NOTE, MEM, 'middle', '400', 'italic'))
    c.y = top + 42
    pop = o.find('a Ghassān population is still named here')
    c.add(f'<line x1="{x0:.1f}" y1="{c.y+6}" x2="{st.X(552.9):.1f}" y2="{c.y+6}" stroke="{DOC}" stroke-width="2.4"/>')
    c.add(chip(st.X(554.6), c.y + 1, st.X(638.8) - st.X(554.6), 12, DOC, opacity='.13', rx=0))
    c.y += 14
    c.para(pop['text'], T_NOTE, DOC_DEEP, 'italic', gap=2)
    c.para(o.find('THE GAP IN THE RECORD')['text'], 15, DOC_DEEP, 'normal', '700', gap=4)
    st.ticks(c, [i for i in o.where(y0=350, y1=358)], rows=2)
    # the eight dated records, as marks on the strip and a list
    recs = sorted([i for i in o.items if i['size'] == 9.4], key=lambda i: i['y'])
    c.add(chip(PAD, c.y, W - 2 * PAD, 2, RULE, rx=0))
    for k, r in enumerate(recs):
        col = MEM if k == 0 else (MEM_LIGHT if r['text'] == '890' else DOC)
        c.add(badge(st.X(r['x'] - 7), c.y + 14 + (k % 2) * 22, k + 1, col))
    c.y += 52
    rows = []
    for k, r in enumerate(recs):
        t_ = next(i for i in o.items if i['y'] == r['y'] and i['x'] > r['x'])
        col = MEM if k == 0 else (MEM_LIGHT if r['text'] == '890' else DOC)
        rows.append(((lambda n, cc: (lambda x, y: badge(x, y, n, cc)))(k + 1, col), r['text'], t_['text']))
    numbered_rows(c, rows)
    tail(c, o, 570)
    return c.svg('The gap in the family line, 569 to about 1500, and the shorter gap in the record of its people')


# ═════════════════════════════════════════════ 7.10 · the same people
def fig_samepeople():
    o = Old('The same people, nine years apart')
    c = Canvas()
    head_and_lede(c, o, 60)
    for side, x0, x1 in (('bj', 40, 300), ('ra', 350, 840)):
        hd = sorted(o.where(x0=x0, x1=x0 + 30, y0=85, y1=110), key=lambda i: i['y'])
        c.para(hd[0]['text'], 15, INK, 'normal', '700', sc=hd[0]['sc'], gap=0)
        c.para(hd[1]['text'], T_NOTE, NOTE, 'italic', gap=6)
        names = [i for i in o.where(x0=x0, x1=x1, y0=118, y1=470) if i['size'] < 9.6]
        # keep the clerk's order: down each column, column by column
        names.sort(key=lambda i: (round(i['x']), i['y']))
        colw = (W - 2 * PAD) / 2
        half = (len(names) + 1) // 2
        ends = []
        for col, part in enumerate((names[:half], names[half:])):
            gx, gy = PAD + col * colw, c.y
            for n in part:
                hit = n['fill'] == '#1A6B3C'
                lines = wrap(n['text'], T_NOTE, colw - 14, 'bold' if hit else 'normal')
                h = 19 + 17 * (len(lines) - 1)
                if hit:
                    c.add(chip(gx - 2, gy + 2, colw - 6, h, '#E8F3ED', rx=2))
                for j, ln in enumerate(lines):
                    c.add(tx(gx + 2 + (10 if j else 0), gy + 16 + j * 17, ln, T_NOTE, n['fill'], 'start', '700' if hit else '400'))
                gy += h + 2
            ends.append(gy)
        c.y = max(ends) + 12
    c.rule()
    nums = sorted([i for i in o.items if i['size'] > 15 and i['y'] > 500], key=lambda i: i['x'])
    for n in nums:
        words = ' '.join(i['text'] for i in sorted(o.where(x0=n['x'] - .5, x1=n['x'] + .5, y0=520, y1=556), key=lambda i: i['y']))
        top = c.y
        c.add(tx(PAD, top + 22, n['text'], 22, n['fill'], 'start', '700'))
        c.y = top + 4
        c.para(words, T_NOTE, BODY, 'normal', x=PAD + 88, width=W - 2 * PAD - 88, gap=10)
        c.y = max(c.y, top + 32)
    for it in sorted(o.where(y0=560), key=lambda i: i['y']):
        c.para(it['text'], T_NOTE, NOTE, 'italic', gap=4)
    return c.svg('Household heads at Bayt Jālā in 1553 and at Ramallah in 1562, with the nineteen found in both')


# ═════════════════════════════════════════════ 7.13 · the Karak wheel
def fig_wheel():
    o = Old('The Karak wheel, redrawn — what it says about Rāshid')
    c = Canvas()
    head_and_lede(c, o, 60)
    hub = sorted(o.where(x0=80, x1=84, y0=200, y1=270), key=lambda i: i['y'])
    top = c.y
    c.add(chip(PAD, top, 120, 54, '#F0F7F3', '#3E9464'))
    c.add(tx(PAD + 60, top + 22, hub[0]['text'], 17, INK, 'middle', '700', sc=hub[0]['sc']))
    c.add(tx(PAD + 60, top + 44, hub[1]['text'], 16, INK, 'middle'))
    c.add(tx(PAD + 132, top + 22, hub[2]['text'], 16, MEM, 'start', '700'))
    c.add(tx(PAD + 132, top + 42, hub[3]['text'], T_NOTE, NOTE, 'start', '400', 'italic'))
    c.y = top + 66

    def branch(ky, ny, names_x, colour, fill):
        k = sorted(o.where(x0=156, x1=160, y0=ky - 2, y1=ky + 16), key=lambda i: i['y'])
        c.para(k[0]['text'], 15, colour, 'normal', '700', sc=True, gap=0)
        c.para(k[1]['text'], T_NOTE, NOTE, 'italic', gap=8)
        lat = sorted([i for i in o.where(y0=ny - 14, y1=ny + 2) if i['x'] >= 190 and i['x'] < 760], key=lambda i: i['x'])
        ar = {round(i['x']): i for i in o.where(y0=ny + 10, y1=ny + 18)}
        cw = (W - 2 * PAD) / 3
        boxes = []
        for i in lat:
            a = ar.get(round(i['x']))
            boxes.append((i, a))
        for k_, (i, a) in enumerate(boxes):
            gx, gy = PAD + (k_ % 3) * cw, c.y + (k_ // 3) * 52
            big = i['size'] > 15
            c.add(chip(gx, gy, cw - 8, 46, fill if not big else '#F6EFE3', '#5DAA83' if colour == DOC_DEEP else '#C49A5E'))
            c.add(tx(gx + (cw - 8) / 2, gy + 20, i['text'], 16 if big else 15, INK, 'middle', '700', sc=i['sc']))
            if a:
                c.add(tx(gx + (cw - 8) / 2, gy + 39, a['text'], 15, BODY, 'middle'))
        c.y += ((len(boxes) - 1) // 3 + 1) * 52 + 4

    branch(66, 111, None, DOC_DEEP, '#F0F7F3')
    more = sorted([i for i in o.items if i['x'] == 766.0], key=lambda i: i['y'])
    c.para(' '.join(i['text'] for i in more), T_NOTE, NOTE, 'italic', gap=12)
    branch(276, 321, None, MEM, '#FFFFFF')
    ram = [i for i in o.items if i['text'] == 'رام الله'][0]
    c.para('→ ' + ram['text'], 16, MEM, 'normal', '700', gap=6)
    c.para(' '.join(i['text'] for i in sorted(o.where(x0=157, x1=159, y0=365, y1=390), key=lambda i: i['y'])),
           15, INK, 'normal', '700', gap=6)
    tail(c, o, 455)
    return c.svg('The hub of the Ḥaddādīn chart of al-Karak: Ṣaqr, his son who kept Karak, and Rāshid who went to Ramallah')


# ═════════════════════════════════════════════ 9.12 · the ladder of a day's work
def fig_wages():
    o = Old('The ladder of a day’s work, about 1900–1903')
    c = Canvas()
    head_and_lede(c, o, 60)
    bars = sorted([r for r in o.shapes('rect') if r.get('height') == '24'], key=lambda r: float(r['y']))
    top_note = o.find('one silver majeedy = 23')
    mx = 25.0
    x0, x1 = PAD, W - PAD - 34
    c.para(top_note['text'], T_NOTE, MEM, 'italic', gap=2)
    y_start = c.y
    rows = []
    for b in bars:
        yb = float(b['y'])
        lab = next(i for i in o.items if i['x'] == 288.0 and abs(i['y'] - yb - 17) < 2)
        val = next(i for i in o.items if i['size'] == 10.6 and abs(i['y'] - yb - 17) < 2)
        note = [i for i in o.items if i['size'] == 8.8 and abs(i['y'] - yb - 17) < 2]
        rows.append((b, lab, val, note))
    xm = x0 + 23 / mx * (x1 - x0)
    for b, lab, val, note in rows:
        v = float(val['text'])
        big = lab['size'] > 12
        c.add(tx(PAD, c.y + 15, lab['text'], 16 if big else 15, MEM if big else INK, 'start', '700' if big else '400', sc=lab['sc']))
        c.y += 20
        w = v / mx * (x1 - x0)
        c.add(chip(x0, c.y, w, 18, b['fill'], opacity=b.get('opacity') if b.get('opacity') != '1' else None, rx=2))
        c.add(tx(x0 + w + 6, c.y + 14, val['text'], 15, INK, 'start', '700'))
        c.y += 22
        for n in note:
            c.para(n['text'], T_NOTE, NOTE, 'italic', gap=0)
        c.y += 8
    c.add(f'<line x1="{xm:.1f}" y1="{y_start:.1f}" x2="{xm:.1f}" y2="{c.y:.1f}" stroke="{MEM}" stroke-width="1.2" stroke-dasharray="4 4"/>')
    tail(c, o, 420)
    return c.svg('Daily wages at Ramallah about 1900 to 1903, in piasters, from a boy in the fields to a mason')


# ═════════════════════════════════════════════ 10.10 · the dark half-decade
def fig_darkyears():
    o = Old('The dark half-decade, 1914–1918')
    c = Canvas()
    head_and_lede(c, o, 60)
    caps = [r for r in o.shapes('rect') if r.get('height') == '6']
    for r in caps:
        x = float(r['x']) + 16
        its = sorted([i for i in o.items if abs(i['x'] - x) < .5 and 100 < i['y'] < 270], key=lambda i: i['y'])
        top = c.y
        c.add(chip(PAD, top, 5, 10, r['fill'], rx=0))
        c.add(tx(PAD + 14, top + 22, its[0]['text'], 24, INK, 'start', '700'))
        c.add(tx(PAD + 86, top + 21, its[1]['text'], 17, r['fill'], 'start', '700', sc=its[1]['sc']))
        c.y = top + 30
        body = its[2:]
        paras, cur, last = [], [], None
        for i in body:
            if last is not None and i['y'] - last > 16:
                paras.append(cur)
                cur = []
            cur.append(i['text'])
            last = i['y']
        paras.append(cur)
        for p in paras:
            c.para(' '.join(p), 15, BODY, 'normal', x=PAD + 14, width=W - 2 * PAD - 14, gap=4)
        if its[0]['text'] == '1916':
            dots = [ci for ci in o.shapes('circle')]
            for k, d in enumerate(dots):
                c.add(f'<circle cx="{PAD+22+k*18}" cy="{c.y+8:.1f}" r="6" fill="{d["fill"]}"/>')
            c.add(tx(PAD + 22 + 10 * 18, c.y + 13, o.find('three of every ten')['text'], T_NOTE, MEM, 'start', '400', 'italic'))
            c.y += 22
        c.add(f'<line x1="{PAD+2}" y1="{top+10}" x2="{PAD+2}" y2="{c.y-2:.1f}" stroke="{r["fill"]}" stroke-width="2"/>')
        c.y += 12
    tail(c, o, 355)
    return c.svg('Ramallah 1914 to 1918: conscription, locusts, typhus and occupation')


# ═════════════════════════════════════════════ 12.2 · every number, on a log scale
def fig_lognumbers():
    o = Old('Every number anyone has ever recorded, 1596–2024')
    c = Canvas()
    head_and_lede(c, o, 60)
    ox0, ox1, oy0, oy1 = 92.0, 800.0, 88.0, 320.0
    px0, px1 = PAD + 44, W - PAD - 4
    top = c.y + 40
    ph = 300
    X = lambda x: px0 + (float(x) - ox0) / (ox1 - ox0) * (px1 - px0)
    Y = lambda y: top + (float(y) - oy0) / (oy1 - oy0) * ph
    bands = [r for r in o.shapes('rect') if r.get('opacity') == '.10']
    blabs = sorted([i for i in o.items if i['size'] == 9 and i['y'] < 90], key=lambda i: i['x'])
    for k, (r, lab) in enumerate(zip(sorted(bands, key=lambda r: float(r['x'])), blabs)):
        bx, bw = X(r['x']), X(float(r['x']) + float(r['width'])) - X(r['x'])
        c.add(chip(bx, top, bw, ph, r['fill'], opacity='.12', rx=0))
        ly = top - 24 + k * 16
        c.add(tx(bx + bw, ly, lab['text'], T_NOTE, MEM, 'end', '400', 'italic'))
        c.add(f'<line x1="{bx+bw-2:.1f}" y1="{ly+3}" x2="{bx+bw-2:.1f}" y2="{top}" stroke="{MEM_LIGHT}"/>')
    for ln in o.shapes('line'):
        if ln.get('x1') == '92' and ln.get('x2') == '800':
            y = Y(ln['y1'])
            c.add(f'<line x1="{px0}" y1="{y:.1f}" x2="{px1}" y2="{y:.1f}" stroke="{RULE}"/>')
    for it in o.where(x0=81, x1=83, y0=95, y1=310):
        c.add(tx(px0 - 6, Y(it['y'] - 4) + 5, it['text'], T_NOTE, NOTE, 'end'))
    for it in o.where(y0=338, y1=342):
        c.add(tx(X(it['x']), top + ph + 18, it['text'], T_NOTE, NOTE, 'middle'))
    c.add(f'<line x1="{px0}" y1="{top+ph}" x2="{px1}" y2="{top+ph}" stroke="{AXIS}"/>')
    ty = [ln for ln in o.shapes('line') if ln.get('stroke-dasharray') == '5 4'][0]
    c.add(f'<line x1="{X(ty["x1"]):.1f}" y1="{top}" x2="{X(ty["x1"]):.1f}" y2="{top+ph}" stroke="{MEM}" stroke-width="1.2" stroke-dasharray="5 4"/>')
    for pl in o.shapes('polyline'):
        pts = ' '.join('%.1f,%.1f' % (X(a), Y(b)) for a, b in (p.split(',') for p in pl['points'].split()))
        extra = ' stroke-dasharray="4 4"' if 'stroke-dasharray' in pl else ''
        c.add(f'<polyline points="{pts}" fill="none" stroke="{pl["stroke"]}" stroke-width="{pl["stroke-width"]}" stroke-linejoin="round"{extra}/>')
    pts = []
    for ci in o.shapes('circle'):
        if float(ci['cy']) > 360:
            continue
        x, y = X(ci['cx']), Y(ci['cy'])
        pts.append((x, y, ci))
        c.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{ci["fill"]}" stroke="{ci.get("stroke", "#FFFFFF")}" stroke-width="{ci.get("stroke-width", "1.4")}"/>')
    # the labelled points: text set in the empty upper left, a leader to each point
    labs = [i for i in o.items if 90 < i['y'] < 320 and i['x'] > 110 and i['size'] >= 9.4 and not (81 <= i['x'] <= 83)]
    typh = sorted([i for i in labs if i['x'] == 606.8], key=lambda i: i['y'])
    vals = sorted([i for i in labs if i['x'] != 606.8], key=lambda i: i['y'])
    ly = top + 14
    for v in vals:
        near = min(pts, key=lambda p: abs(X(v['x']) - p[0]) + abs(Y(v['y']) - p[1]) * .5)
        if v['text'] == '400':
            c.add(tx(near[0] + 2, near[1] - 10, v['text'], T_NOTE, INK, 'start', '700'))
            continue
        ax = 238
        c.add(tx(ax, ly, v['text'], T_NOTE, INK, 'end', '700'))
        c.add(f'<path d="M{ax+3} {ly-4} L{near[0]-5:.1f} {near[1]:.1f}" stroke="{AXIS}" stroke-width=".8" fill="none"/>')
        ly += 19
    ly += 6
    tp = [p for p in pts if abs(p[0] - X(611.7)) < 6] or [(X(614.8), Y(240), None)]
    for k, t_ in enumerate(typh):
        c.add(tx(238, ly + k * 17, t_['text'], T_NOTE if k else 15, MEM, 'end', '700' if not k else '400', 'italic' if k else 'normal'))
    c.add(f'<path d="M241 {ly-4} L{X(614.8)-3:.1f} {Y(232):.1f}" stroke="{MEM_LIGHT}" stroke-width=".8" fill="none"/>')
    c.y = top + ph + 30
    # legend
    leg = sorted([i for i in o.items if i['y'] == 382.0], key=lambda i: i['x'])
    marks = [lambda x, y: f'<circle cx="{x}" cy="{y}" r="5" fill="{DOC}"/>',
             lambda x, y: f'<circle cx="{x}" cy="{y}" r="5" fill="#FFFFFF" stroke="{DOC}" stroke-width="2"/>',
             lambda x, y: f'<circle cx="{x}" cy="{y}" r="5" fill="{CONTEXT}"/>',
             lambda x, y: f'<line x1="{x-9}" y1="{y}" x2="{x+9}" y2="{y}" stroke="{MEM}" stroke-width="1.6" stroke-dasharray="4 4"/>']
    for mk, it in zip(marks, leg):
        c.add(mk(PAD + 10, c.y + 9))
        c.para(it['text'], T_NOTE, BODY, 'normal', x=PAD + 26, width=W - 2 * PAD - 26, gap=2)
    c.y += 6
    tail(c, o, 390, rule=True) if False else None
    c.rule()
    for it in sorted(o.where(y0=390), key=lambda i: i['y']):
        c.para(it['text'], T_NOTE, NOTE if it['size'] < 10.4 else BODY, 'italic' if it['size'] < 10.4 else 'normal', gap=6)
    return c.svg('Ramallah’s recorded population from 1596 to 2024 on a logarithmic scale')


# ═════════════════════════════════════════════ C.1 · John Mogannam's chart
def fig_mogannam():
    o = Old('John Mogannam’s chart of thirty-six named generations')
    c = Canvas()
    head_and_lede(c, o, 60)
    bands = [r for r in o.shapes('rect') if r.get('height') == '21' and 'url' not in r.get('fill', '')]
    hatch = [r for r in o.shapes('rect') if r.get('height') == '21' and 'url' in r.get('fill', '')]
    rows = []
    for b in bands:
        bx, by = float(b['x']), float(b['y'])
        its = [i for i in o.items if bx < i['x'] < bx + 400 and by < i['y'] < by + 21]
        num = [i for i in its if i['size'] == 9]
        en = [i for i in its if i['size'] == 9.6]
        ar = [i for i in its if i['size'] == 10.5]
        rows.append((b, num, en, ar, any(h['y'] == b['y'] and h['x'] == b['x'] for h in hatch)))
    defs = ('<defs><pattern id="mhatch" width="6" height="6" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">'
            f'<line x1="0" y1="0" x2="0" y2="6" stroke="{MEM_LIGHT}" stroke-width="2"/></pattern></defs>')
    c.add(defs)
    for b, num, en, ar, hat in rows:
        lines = wrap(en[0]['text'] if en else '', 15, W - 2 * PAD - 150)
        h = 26 + 18 * (len(lines) - 1)
        fill = b['fill']
        c.add(chip(PAD, c.y, W - 2 * PAD, h, fill, b.get('stroke')))
        if hat:
            c.add(chip(PAD, c.y, W - 2 * PAD, h, 'url(#mhatch)'))
        fg = on(fill)
        if num:
            c.add(tx(PAD + 16, c.y + 18, num[0]['text'], T_NOTE, fg, 'middle', '700'))
        for j, ln in enumerate(lines):
            c.add(tx(PAD + 32, c.y + 18 + j * 18, ln, 15, fg))
        if ar:
            c.add(tx(W - PAD - 6, c.y + 18, ar[0]['text'], 15, fg, 'end'))
        c.y += h + 3
    c.y += 8
    leg = sorted([i for i in o.items if i['y'] == 571.0], key=lambda i: i['x'])
    sw = [r for r in o.shapes('rect') if r.get('height') == '13']
    for k, (it, r) in enumerate(zip(leg, sorted(sw, key=lambda r: float(r['x'])))):
        gx, gy = PAD + (k % 2) * 190, c.y + (k // 2) * 22
        c.add(chip(gx, gy + 3, 14, 14, r['fill'], r.get('stroke'), rx=2))
        c.add(tx(gx + 20, gy + 15, it['text'], T_NOTE, BODY))
    c.y += ((len(leg) - 1) // 2 + 1) * 22 + 6
    tail(c, o, 590)
    return c.svg('John Mogannam’s chart of thirty-six generations from Adam and Eve to Rāshid, coloured by evidence')


# ═════════════════════════════════════════════ B.1 · the account, tested
def fig_tested():
    o = Old('The family’s account of itself, tested')
    c = Canvas()
    head_and_lede(c, o, 60)
    bars = sorted([r for r in o.shapes('rect') if r.get('height') == '23'], key=lambda r: float(r['y']))
    mx = 15
    for b in bars:
        yb = float(b['y'])
        row = [i for i in o.items if abs(i['y'] - yb - 17) < 2]
        lab = next(i for i in row if i['x'] == 182.0)
        n = next(i for i in row if i['size'] > 16)
        note = next(i for i in row if i['x'] == 512.0)
        c.add(tx(PAD, c.y + 15, lab['text'], 15, INK, 'start', '700'))
        c.add(tx(W - PAD, c.y + 15, note['text'] if len(note['text']) < 30 else '', T_NOTE, NOTE, 'end', '400', 'italic'))
        c.y += 20
        w = int(n['text']) / mx * (W - 2 * PAD - 40)
        c.add(chip(PAD, c.y, w, 18, b['fill'], rx=2))
        c.add(tx(PAD + w + 6, c.y + 15, n['text'], 16, INK, 'start', '700'))
        c.y += 22
        if len(note['text']) >= 30:
            c.para(note['text'], T_NOTE, NOTE, 'italic', gap=0)
        c.y += 8
    tail(c, o, 300)
    return c.svg('Thirty-six claims of the family’s presentation, by verdict against Shāhīn (1982) and the record')
