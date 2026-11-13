# -*- coding: utf-8 -*-
"""v80: the new phone-first visuals.

Every plate here is drawn 400 units wide and shown 1:1 on a phone, so a unit is
a pixel there. Nothing is set under 12 units. Colours keep their evidence
meaning from docs/MAP_STYLE.md: green = documented, ochre = remembered, grey =
context. Categories that are not evidence (Christian and Muslim households,
churches, clans) use the ink tints and the ERA violets. Every number on these
plates is printed in the book's own text or tables; the sources are given in
each figure's source line, not inside the plate.
"""
from html import escape as _esc

from map_style import (INK, BODY, NOTE, DOC, DOC_DEEP, MEM, MEM_LIGHT, CONTEXT,
                       RAMALLAH, ERA, FONT)

W = 400
AXIS = '#8F8A80'
RULE = '#D9D4C8'
TINT = ['#1A1915', '#6B6760', '#B7B2A8', '#DDD8CE']
GOLD = '#9A6324'
PAPER = '#FFFFFF'

T_LAB, T_NOTE, T_BIG = 15, 14, 17


def esc(s):
    return _esc(s, quote=False)


def t(x, y, s, size=T_LAB, fill=INK, anchor='start', weight='400', style='normal', raw=False):
    body = s if raw else esc(s)
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}" font-style="{style}" font-family="{FONT}">{body}</text>')


def wrap(s, size, width):
    """Greedy wrap for Times at about half an em a character."""
    per = max(8, int(width / (size * 0.47)))
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


def para(x, y, s, size=T_NOTE, fill=NOTE, width=W - 16, style='italic', lead=None, weight='400'):
    lead = lead or size * 1.25
    out = []
    lines = wrap(s, size, width)
    for i, ln in enumerate(lines):
        out.append(t(x, y + i * lead, ln, size, fill, 'start', weight, style))
    return ''.join(out), y + len(lines) * lead


def svg(H, label, body):
    return (f'<svg viewBox="0 0 {W} {H:.0f}" width="100%" role="img" aria-label="{esc(label)}" '
            f'class="phonefig">{body}</svg>')


def fmt(n):
    return f'{n:,}'


# ───────────────────────────────────────────── the nine links, as a ladder
LINKS = [
    ('Links one and two', 'Adam to ʿĀbir', 'scripture', 'generations 1–13'),
    ('Link three', 'Joktan is Qaḥṭān: the join', 'join', 'generation 14'),
    ('Link four', 'Qaḥṭān to al-Azd', 'classical', '15–23'),
    ('Link five', 'al-Azd to Ghassān', 'classical', '24–29'),
    ('Link six', 'the Jafnid phylarchs', 'attested', '30–34'),
    ('Link seven', 'thirty-one unnamed generations', 'none', '35–65'),
    ('Link eight', 'Rāshid al-Ḥaddādīn', 'documents', '66'),
    ('Link nine', 'five sons, eight clans, a town', 'documents', '67 to today'),
]
_GR = {'scripture': ('#D5E9DF', INK, 'scripture'), 'join': ('#8FBFA6', INK, 'the join'),
       'classical': ('#A9CDB8', INK, 'classical'), 'attested': ('#79B491', INK, 'attested'),
       'none': ('#FDF6EC', '#8A5A1E', 'no evidence'), 'documents': (DOC, '#FFFFFF', 'documents')}


def fig_ladder9(cur):
    """The family's chain as nine links, with link `cur` (0-based row) as this chapter's."""
    rh, top = 46, 8
    H = top + len(LINKS) * rh + 30
    s = []
    for i, (lk, what, g, gens) in enumerate(LINKS):
        y = top + i * rh
        fill, tc, glab = _GR[g]
        on = i <= cur
        op = '1' if on else '.32'
        dash = ' stroke-dasharray="4 3"' if g == 'none' else ''
        s.append(f'<g opacity="{op}">')
        s.append(f'<rect x="8" y="{y}" width="{W-16}" height="{rh-5}" rx="3" fill="{fill}" '
                 f'stroke="{"#C9A46A" if g == "none" else fill}"{dash}/>')
        s.append(t(18, y + 17, lk, T_NOTE, tc, 'start', '700'))
        s.append(t(W - 18, y + 17, gens, T_NOTE, tc, 'end', '400', 'italic'))
        s.append(t(18, y + 35, what, T_LAB, tc))
        s.append('</g>')
        if i == cur:
            s.append(f'<rect x="5" y="{y-3}" width="{W-10}" height="{rh+1}" rx="4" fill="none" '
                     f'stroke="{GOLD}" stroke-width="2.6"/>')
    y = top + len(LINKS) * rh + 16
    s.append(t(8, y, 'Solid: reached by this chapter. Faint: still ahead.', T_NOTE, NOTE, 'start', '400', 'italic'))
    return svg(H, 'The family chain in nine links; link %d is this chapter’s' % (cur + 1), ''.join(s))


# ───────────────────────────────────────────── churches and schools, 1776–1925
MISSION_LANES = [('Orthodox', ERA[0]), ('Protestant and Anglican', ERA[1]), ('Catholic', ERA[2]),
                 ('Friends', ERA[3]), ('German', TINT[1])]
MISSION_EVENTS = [
    ('1776–77', 0, 'The Orthodox Patriarchate’s first primary school, by the Ottoman count of 1903'),
    ('1805–06', 0, 'A second Orthodox school'),
    ('about 1848–50', 1, 'Bishop Gobat’s Protestant school'),
    ('1850', 0, 'The present Orthodox church: the datestone on its portal'),
    ('1857–58', 2, 'The Latin mission comes under Pierre Cotta, and opens its school'),
    ('1863', 1, 'A catechist settles in the town; families ask to be Protestant'),
    ('1869', 3, 'The Friends’ Hope School opens for girls, with twenty, because Miriam Karam asked'),
    ('1873', 2, 'The Sisters of St Joseph: a girls’ school and a free clinic'),
    ('1875–76', 1, 'The Protestant boys’ school'),
    ('1878', 1, '137 boys in the mission schools of Ramallah and outstations'),
    ('1887', 1, 'St Andrew’s (Kaddoura gives 1855)'),
    ('1889', 3, 'The Girls Training Home: fifteen boarders'),
    ('1890–91', 4, 'Two German girls’ schools; 82 girls by 1903'),
    ('1893', 3, 'Eight Friends day schools'),
    ('1895', 2, 'Our Lady of the Annunciation, under Fr Yaʿqūb Mogannam'),
    ('1925', 3, 'The name Friends Girls School'),
]


def fig_missions():
    s = []
    # legend, one row of chips wrapping onto two
    x, y = 8, 16
    for name, col in MISSION_LANES:
        w = 22 + len(name) * 7.2
        if x + w > W - 8:
            x, y = 8, y + 20
        s.append(f'<circle cx="{x+5}" cy="{y-4}" r="5" fill="{col}"/>')
        s.append(t(x + 15, y, name, T_NOTE, BODY))
        x += w + 10
    y += 22
    s.append(f'<line x1="8" y1="{y-8}" x2="{W-8}" y2="{y-8}" stroke="{RULE}"/>')
    xl = 112          # the spine
    s_y0 = y
    rows = []
    for when, lane, what in MISSION_EVENTS:
        lines = wrap(what, T_LAB, W - xl - 26)
        rows.append((when, lane, lines, y))
        y += max(1, len(lines)) * 18 + 12
    s.append(f'<line x1="{xl}" y1="{s_y0-2}" x2="{xl}" y2="{y-14}" stroke="{AXIS}" stroke-width="1.2"/>')
    for when, lane, lines, yy in rows:
        col = MISSION_LANES[lane][1]
        s.append(t(xl - 12, yy + 9, when, T_NOTE if len(when) > 7 else T_LAB, INK, 'end', '700'))
        s.append(f'<circle cx="{xl}" cy="{yy+5}" r="6" fill="{col}" stroke="#FFFFFF" stroke-width="1.5"/>')
        for k, ln in enumerate(lines):
            s.append(t(xl + 14, yy + 9 + k * 18, ln, T_LAB, BODY))
    return svg(y, 'Churches and schools at Ramallah, 1776 to 1925, by denomination', ''.join(s))


# ───────────────────────────────────────────── the households, 1525–1596
def fig_households2():
    H = 560
    s = []
    data = [('1525–28', 0, 0, 0), ('1538–39', 0, 0, 4), ('1553–54', 0, 0, 6),
            ('1562', 63, 8, 10), ('1596', 71, 0, 9)]
    x0, x1 = 34, W - 10
    y0, y1 = 40, 250          # plot top and baseline
    mx = 90
    sc = (y1 - y0) / mx
    # legend
    chips = [(TINT[0], 'Christian households'), (TINT[1], 'single men'), (TINT[2], 'Muslim households')]
    lx = 8
    for col, lab in chips:
        s.append(f'<rect x="{lx}" y="8" width="12" height="12" fill="{col}"/>')
        s.append(t(lx + 17, 19, lab, T_NOTE, BODY))
        lx += 30 + len(lab) * 6.8
    for v in (0, 20, 40, 60, 80):
        yy = y1 - v * sc
        s.append(f'<line x1="{x0}" y1="{yy:.1f}" x2="{x1}" y2="{yy:.1f}" stroke="{RULE if v else AXIS}"/>')
        s.append(t(x0 - 6, yy + 4, str(v), T_NOTE, NOTE, 'end'))
    bw = 44
    step = (x1 - x0) / len(data)
    for i, (yr, ch, single, mu) in enumerate(data):
        bx = x0 + i * step + (step - bw) / 2
        y = y1
        for v, col in ((mu, TINT[2]), (ch, TINT[0]), (single, TINT[1])):
            if v:
                h = v * sc
                s.append(f'<rect x="{bx:.1f}" y="{y-h:.1f}" width="{bw}" height="{h:.1f}" fill="{col}"/>')
                y -= h
        tot = ch + single + mu
        if tot:
            s.append(t(bx + bw / 2, y - 6, str(tot), T_LAB, INK, 'middle', '700'))
        else:
            s.append(t(bx + bw / 2, y1 - 6, 'none', T_NOTE, NOTE, 'middle', '400', 'italic'))
        s.append(t(bx + bw / 2, y1 + 17, yr, T_NOTE, INK, 'middle', '700'))
    # the 1562 split, said in words under the plot
    yy = y1 + 40
    txt_, yy = para(8, yy, '1562: sixty-three Christian households and eight single men, seventy-one taxpayers, beside ten Muslim households already on the hill. 1553–54: the thirty-six Kasābra households are still counted at Bayt Jālā. 1596: eighty households, seventy-one of them Christian.', T_NOTE, BODY, style='normal')
    s.append(txt_)
    # neighbours, 1596
    yy += 14
    s.append(f'<line x1="8" y1="{yy-12}" x2="{W-8}" y2="{yy-12}" stroke="{RULE}"/>')
    s.append(t(8, yy + 4, 'The neighbours in the same register, 1596', T_LAB, INK, 'start', '700'))
    yy += 18
    vills = [('Bayt Jālā', 239, 6), ('Ṭayyibat al-Ism', 23, 63), ('Ramallah', 71, 9),
             ('al-Bīra', 0, 45), ('Bīr Zayt', 0, 26), ('Jifnā', 0, 21)]
    lx0, mxv = 132, 290
    pw = W - 12 - lx0
    for nm, ch, mu in vills:
        bold = nm == 'Ramallah'
        s.append(t(lx0 - 8, yy + 13, nm, T_LAB, RAMALLAH if bold else BODY, 'end', '700' if bold else '400'))
        wc, wm = pw * ch / mxv, pw * mu / mxv
        if ch:
            s.append(f'<rect x="{lx0}" y="{yy+2}" width="{wc:.1f}" height="14" fill="{TINT[0]}"/>')
        if mu:
            s.append(f'<rect x="{lx0+wc:.1f}" y="{yy+2}" width="{wm:.1f}" height="14" fill="{TINT[2]}"/>')
        s.append(t(lx0 + wc + wm + 5, yy + 13, str(ch + mu), T_NOTE, NOTE))
        yy += 25
    txt_, yy = para(8, yy + 8, 'The published register enters Jifnā as Muslim; every sixteenth-century register has it Christian, and Robinson found it wholly Christian in 1838.', T_NOTE)
    s.append(txt_)
    return svg(yy + 4, 'Households at Ramallah in the Ottoman registers, 1525 to 1596, and its neighbours in 1596', ''.join(s))


# ───────────────────────────────────────────── Karak: the Christian share and the eight clans
def fig_karak():
    s = []
    pts = [(1596, 57, 57, 'the Ottoman register', 'doc'), (1806, 37, 40, 'Seetzen', 'doc'),
           (1812, 27, 27, 'Burckhardt', 'doc'), (1818, 50, 50, 'Irby and Mangles', 'doc'),
           (1872, 20, 20, 'Tristram, hearsay', 'ctx'), (1896, 20, 20, 'Hill', 'doc'),
           (1900, 18, 18, 'Musil', 'doc'), (1961, 22, 22, 'the Jordanian census', 'doc')]
    x0, x1, y0, y1 = 40, W - 14, 30, 220
    X = lambda yr: x0 + (yr - 1580) / (1980 - 1580) * (x1 - x0)
    Y = lambda v: y1 - v / 70 * (y1 - y0)
    s.append(t(8, 16, 'Christian share of Karak, per cent', T_LAB, INK, 'start', '700'))
    for v in (0, 20, 40, 60):
        s.append(f'<line x1="{x0}" y1="{Y(v):.1f}" x2="{x1}" y2="{Y(v):.1f}" stroke="{RULE if v else AXIS}"/>')
        s.append(t(x0 - 6, Y(v) + 4, str(v), T_NOTE, NOTE, 'end'))
    for yr in (1600, 1700, 1800, 1900):
        s.append(t(X(yr), y1 + 17, str(yr), T_NOTE, NOTE, 'middle'))
    path = ' '.join(f'{"M" if i == 0 else "L"}{X(p[0]):.1f} {Y((p[1]+p[2])/2):.1f}' for i, p in enumerate(pts))
    s.append(f'<path d="{path}" fill="none" stroke="{AXIS}" stroke-width="1.2" stroke-dasharray="3 3"/>')
    for yr, lo, hi, who, k in pts:
        cx = X(yr)
        if hi != lo:
            s.append(f'<line x1="{cx:.1f}" y1="{Y(lo):.1f}" x2="{cx:.1f}" y2="{Y(hi):.1f}" stroke="{DOC}" stroke-width="5"/>')
        if k == 'doc':
            s.append(f'<circle cx="{cx:.1f}" cy="{Y((lo+hi)/2):.1f}" r="5" fill="{DOC}"/>')
        else:
            s.append(f'<circle cx="{cx:.1f}" cy="{Y(lo):.1f}" r="5" fill="#FFFFFF" stroke="{CONTEXT}" stroke-width="2"/>')
    # labels for the points that matter
    s.append(t(X(1596) + 8, Y(57) + 4, '1596: 57%', T_LAB, INK, 'start', '700'))
    s.append(t(X(1818) + 8, Y(50) + 4, '1818: about half', T_NOTE, BODY))
    s.append(t(X(1961), Y(22) - 10, '1961: 22%', T_NOTE, BODY, 'end'))
    s.append(t(X(1900) + 4, Y(18) + 20, 'about 1900: 18–20%', T_NOTE, BODY, 'middle'))
    y = y1 + 36
    txt_, y = para(8, y, 'Green: counted or seen on the spot. Hollow: hearsay. Seetzen’s 1806 count is a range. Taxable households in 1596; families, houses or persons later.', T_NOTE)
    s.append(txt_)
    y += 12
    s.append(f'<line x1="8" y1="{y-10}" x2="{W-8}" y2="{y-10}" stroke="{RULE}"/>')
    s.append(t(8, y + 6, 'The eight Christian clans, and where each said it came from', T_LAB, INK, 'start', '700'))
    y += 12
    s.append(t(8, y + 10, 'Musil, 1896–1902', T_NOTE, NOTE, 'start', '400', 'italic'))
    y += 18
    clans = [('Ḥalasāʾ', 'Egypt; the ancestor married a Ḥaddādīn girl'), ('Ḥegāzīn', 'the Ḥijāz'),
             ('ʿAkāse', 'Kh. el-Mkhēlle, east of Wādī Mūsā'),
             ('Ḥaddādīn', 'Kh. el-Ḥaddād, a ruin on the Karak plateau'),
             ('Mdānāt', 'Middīn'), ('Zrejkāt', 'Kh. el-Mkhēlle'),
             ('Ṣunnāʿ', 'merchants of Damascus'), ('Beqāʿīn', 'el-Beqʿe')]
    for nm, frm in clans:
        hl = nm == 'Ḥaddādīn'
        s.append(t(96, y + 12, nm, T_LAB, RAMALLAH if hl else INK, 'end', '700'))
        lines = wrap(frm, T_LAB, W - 112)
        for k, ln in enumerate(lines):
            s.append(t(106, y + 12 + k * 17, ln, T_LAB, BODY))
        y += 17 * len(lines) + 6
    txt_, y = para(8, y + 10, 'About 1905 Jaussen counted eight Christian tribes, two hundred households, with the Ḥalasa first and the Ḥaddādīn eighth, under their sheikh Khalīl bin Ibrāhīm. Not one clan names Jerusalem, Bethlehem or Bayt Jālā as its origin.', T_NOTE, BODY, style='normal')
    s.append(txt_)
    return svg(y + 4, 'The Christian share of Karak from 1596 to 1961, and the eight Christian clans with the origins they gave Musil', ''.join(s))


# ───────────────────────────────────────────── the Ḥaddādīn and the Ḥalasa
HALASA = [
    ('15th–16th c.', 'both', 'mem', 'The Ḥalasa ancestor, a stranger from Egypt, marries a girl of the Ḥaddādīn at Karak. Oppenheim was told “four or five hundred years before”; Connell, after Peake, says the seventeenth century.'),
    ('about 1806', 'h', 'doc', 'Seetzen, as Chatelard reads him: Ḥaddādīn tents at Ḥumaymāt, north of Karak.'),
    ('1812', 'ctx', 'doc', 'Burckhardt counts about 150 Christian families at Karak and names no Ḥaddādīn.'),
    ('from 1867', 'ctx', 'doc', 'Karak Christians begin to resettle Maʿīn.'),
    ('about 1879', 'h', 'mem', 'The first named Ḥaddādīn at Karak: the house of Jreis Sulayman Haddadeen.'),
    ('1892', 'both', 'mem', 'The Ḥaddādīn and the Ḥalasa move to Maʿīn (1894 in a press summary of the clan history).'),
    ('four years on', 'a', 'mem', 'The Ḥalasa and some of the Ḥaddādīn go back to Karak.'),
    ('about 1901', 'h', 'mem', 'After a quarrel with the Ḥalasa, Ḥaddādīn take refuge at Maʿīn.'),
    ('about 1905', 'both', 'doc', 'Jaussen lists the Christian tribes of Karak: the Ḥalasa first, the Ḥaddādīn eighth, under Khalīl bin Ibrāhīm.'),
    ('1909', 'h', 'mem', 'The clan settles at Maʿīn for good, having gone over to the Melkite rite.'),
    ('1920s', 'h', 'doc', 'Al-Ziriklī: fifteen Greek Orthodox Ḥaddādīn houses at Karak.'),
    ('1934–35', 'both', 'doc', 'Peake: the Ḥaddādīn are “the oldest” Christian tribe of Karak and “claim to be Ghassanids”; the Ḥalasa are sons of an Egyptian who married a Ḥaddādīn girl.'),
    ('1953', 'h', 'mem', 'More than 800 Ḥaddādīn at el-ʿAzeeyyeh.'),
    ('1990s', 'both', 'doc', 'Chatelard finds the Ḥaddādīn still marrying into the Ḥalasa.'),
]


def fig_halasa():
    s = []
    lx = [(DOC, 'seen or written by an outside witness'), (MEM, 'the clan’s own history')]
    y = 14
    for col, lab in lx:
        s.append(f'<circle cx="14" cy="{y-4}" r="6" fill="{col}"/>')
        s.append(t(26, y, lab, T_NOTE, BODY))
        y += 18
    s.append(t(8, y + 2, 'H = the Ḥaddādīn · A = the Ḥalasa · both, or Karak as a whole', T_NOTE, NOTE, 'start', '400', 'italic'))
    y += 20
    s.append(f'<line x1="8" y1="{y-6}" x2="{W-8}" y2="{y-6}" stroke="{RULE}"/>')
    xl = 104
    y0 = y + 4
    rows = []
    y += 6
    for when, who, k, what in HALASA:
        lines = wrap(what, T_LAB, W - xl - 34)
        rows.append((when, who, k, lines, y))
        y += len(lines) * 18 + 10
    s.append(f'<line x1="{xl}" y1="{y0}" x2="{xl}" y2="{y-12}" stroke="{AXIS}" stroke-width="1.2"/>')
    for when, who, k, lines, yy in rows:
        col = DOC if k == 'doc' else MEM
        s.append(t(xl - 12, yy + 9, when, T_NOTE, INK, 'end', '700'))
        s.append(f'<circle cx="{xl}" cy="{yy+5}" r="6" fill="{col}" stroke="#FFFFFF" stroke-width="1.5"/>')
        tag = {'h': 'H', 'a': 'A', 'both': 'H A', 'ctx': ''}[who]
        s.append(t(W - 8, yy + 9, tag, T_NOTE, NOTE, 'end', '700'))
        for j, ln in enumerate(lines):
            s.append(t(xl + 14, yy + 9 + j * 18, ln, T_LAB, BODY))
    return svg(y, 'The Ḥaddādīn and the Ḥalasa of Karak, from the founding marriage to the 1990s', ''.join(s))


# ───────────────────────────────────────────── the emigration wave
def fig_emigration():
    s = []
    us = [(1901, 4, False), (1946, 1500, False), (1953, 2580, False), (1960, 4000, True), (1975, 10000, True)]
    home = [(1905, 3214), (1922, 3104), (1931, 4286), (1944, 4885), (1953, 4500), (1975, 2000)]
    x0, x1, y0, y1 = 46, W - 16, 34, 270
    X = lambda yr: x0 + (yr - 1900) / (1980 - 1900) * (x1 - x0)
    Y = lambda v: y1 - v / 11000 * (y1 - y0)
    s.append(f'<line x1="18" y1="12" x2="36" y2="12" stroke="{INK}" stroke-width="3"/>')
    s.append(t(42, 16, 'Ramallah people in the United States', T_NOTE, BODY))
    s.append(f'<line x1="18" y1="28" x2="36" y2="28" stroke="{TINT[2]}" stroke-width="3"/>')
    s.append(t(42, 32, 'Ramallah at home', T_NOTE, BODY))
    y0 = 50
    Y = lambda v: y1 - v / 11000 * (y1 - y0)
    for v in (0, 2500, 5000, 7500, 10000):
        s.append(f'<line x1="{x0}" y1="{Y(v):.1f}" x2="{x1}" y2="{Y(v):.1f}" stroke="{RULE if v else AXIS}"/>')
        s.append(t(x0 - 6, Y(v) + 4, fmt(v), T_NOTE, NOTE, 'end'))
    for yr in (1900, 1920, 1940, 1960, 1980):
        s.append(t(X(yr), y1 + 17, str(yr), T_NOTE, NOTE, 'middle'))
    for yr, lab, dy in ((1916, 'typhus', 0), (1948, '1948', 0), (1959, 'Federation', 16)):
        s.append(f'<line x1="{X(yr):.1f}" y1="{y0}" x2="{X(yr):.1f}" y2="{y1}" stroke="{AXIS}" stroke-dasharray="2 3"/>')
        s.append(t(X(yr) - 3, y0 + 12 + dy, lab, T_NOTE, NOTE, 'end', '400', 'italic'))
    hp = ' '.join(f'{"M" if i == 0 else "L"}{X(a):.1f} {Y(b):.1f}' for i, (a, b) in enumerate(home))
    s.append(f'<path d="{hp}" fill="none" stroke="{TINT[2]}" stroke-width="3"/>')
    up = ' '.join(f'{"M" if i == 0 else "L"}{X(a):.1f} {Y(b):.1f}' for i, (a, b, _) in enumerate(us))
    s.append(f'<path d="{up}" fill="none" stroke="{INK}" stroke-width="3"/>')
    for yr, v, plus in us:
        s.append(f'<circle cx="{X(yr):.1f}" cy="{Y(v):.1f}" r="4.5" fill="{INK}"/>')
    s.append(t(X(1901) + 8, Y(4) - 10, 'the first four, 1901', T_NOTE, INK))
    s.append(t(X(1946) - 6, Y(1500) - 10, '1,500', T_NOTE, INK, 'end', '700'))
    s.append(t(X(1953) + 8, Y(2580) + 14, '2,580', T_NOTE, INK, 'start', '700'))
    s.append(t(X(1960) + 8, Y(4000) + 4, 'over 4,000', T_NOTE, INK, 'start', '700'))
    s.append(t(X(1975) - 8, Y(10000) + 5, 'over 10,000', T_NOTE, INK, 'end', '700'))
    s.append(t(X(1975), Y(2000) + 18, 'fewer than 2,000', T_NOTE, NOTE, 'end'))
    y = y1 + 40
    txt_, y = para(8, y, 'At home: the censuses of 1905, 1922 and 1931; then natives only, from the count of 1944 and Shāhīn’s figures for 1953 (7,080 Ramallah people, 2,580 of them in America) and 1975 (fewer than 2,000 still at home). In the United States: Shāhīn’s counts.', T_NOTE)
    s.append(txt_)
    # inset: 1931
    y += 16
    s.append(f'<line x1="8" y1="{y-12}" x2="{W-8}" y2="{y-12}" stroke="{RULE}"/>')
    s.append(t(8, y + 4, 'The men who were missing: the census of 1931', T_LAB, INK, 'start', '700'))
    y += 16
    for lab, v in (('men', 1941), ('women', 2345)):
        w = (W - 120) * v / 2400
        s.append(t(64, y + 13, lab, T_LAB, BODY, 'end'))
        s.append(f'<rect x="72" y="{y+1}" width="{w:.1f}" height="16" fill="{TINT[0] if lab == "men" else TINT[1]}"/>')
        s.append(t(78 + w, y + 13, fmt(v), T_LAB, INK, 'start', '700'))
        y += 27
    txt_, y = para(8, y + 8, 'About four hundred men short, in a town of four thousand: the men who had sailed after 1901, counted by their absence.', T_NOTE)
    s.append(txt_)
    return svg(y + 4, 'Ramallah people in the United States and at home, 1901 to 1975, and the census of 1931 by sex', ''.join(s))


# ───────────────────────────────────────────── population, one honest line
def fig_population():
    s = []
    pts = [(1838, 850), (1905, 3214), (1922, 3104), (1931, 4286), (1944, 6300), (1953, 13500),
           (1961, 14759), (1967, 12134), (1997, 17851), (2007, 27460), (2017, 38998), (2021, 42122)]
    x0, x1, y0, y1 = 50, W - 14, 26, 270
    X = lambda yr: x0 + (yr - 1830) / (2030 - 1830) * (x1 - x0)
    Y = lambda v: y1 - v / 45000 * (y1 - y0)
    for v in (0, 10000, 20000, 30000, 40000):
        s.append(f'<line x1="{x0}" y1="{Y(v):.1f}" x2="{x1}" y2="{Y(v):.1f}" stroke="{RULE if v else AXIS}"/>')
        s.append(t(x0 - 6, Y(v) + 4, fmt(v), T_NOTE, NOTE, 'end'))
    for yr in (1850, 1900, 1950, 2000):
        s.append(t(X(yr), y1 + 17, str(yr), T_NOTE, NOTE, 'middle'))
    for yr, lab, dy in ((1916, 'typhus', 0), (1948, 'refugees', 16), (1967, 'occupation', 32)):
        s.append(f'<line x1="{X(yr):.1f}" y1="{y0}" x2="{X(yr):.1f}" y2="{y1}" stroke="{AXIS}" stroke-dasharray="2 3"/>')
        s.append(t(X(yr) - 3, y0 + 12 + dy, lab, T_NOTE, NOTE, 'end', '400', 'italic'))
    # 1870: estimates only
    s.append(f'<line x1="{X(1870):.1f}" y1="{Y(1100):.1f}" x2="{X(1870):.1f}" y2="{Y(2000):.1f}" stroke="{CONTEXT}" stroke-width="5"/>')
    d = ' '.join(f'{"M" if i == 0 else "L"}{X(a):.1f} {Y(b):.1f}' for i, (a, b) in enumerate(pts))
    s.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="2.4"/>')
    # natives and newcomers, 1944 and 1953
    for yr, nat, tot in ((1944, 4885, 6300), (1953, 4500, 13500)):
        s.append(f'<rect x="{X(yr)-5:.1f}" y="{Y(tot):.1f}" width="10" height="{Y(nat)-Y(tot):.1f}" fill="{TINT[2]}"/>')
        s.append(f'<rect x="{X(yr)-5:.1f}" y="{Y(nat):.1f}" width="10" height="{Y(0)-Y(nat):.1f}" fill="{TINT[1]}"/>')
    for a, b in pts:
        s.append(f'<circle cx="{X(a):.1f}" cy="{Y(b):.1f}" r="3.5" fill="{INK}"/>')
    s.append(f'<circle cx="{X(2021):.1f}" cy="{Y(42122):.1f}" r="4" fill="#FFFFFF" stroke="{INK}" stroke-width="2"/>')
    s.append(t(X(1838), Y(850) - 10, '1838: 800–900', T_NOTE, BODY))
    s.append(t(X(1953) - 8, Y(13500) - 8, '1953: 13,500', T_NOTE, INK, 'end', '700'))
    s.append(t(X(1967) + 6, Y(12134) + 16, '1967: 12,134', T_NOTE, BODY))
    s.append(t(X(2017) - 8, Y(38998) + 16, '2017: 38,998', T_NOTE, INK, 'end', '700'))
    y = y1 + 36
    chips = [(TINT[1], 'natives'), (TINT[2], 'refugees and newcomers')]
    lx = 8
    for col, lab in chips:
        s.append(f'<rect x="{lx}" y="{y-10}" width="12" height="12" fill="{col}"/>')
        s.append(t(lx + 17, y, lab, T_NOTE, BODY))
        lx += 40 + len(lab) * 6.8
    txt_, y = para(8, y + 20, 'Persons, on an ordinary scale. The grey bar at 1870 spans two estimates of the same decade. The 1967 count was taken under curfew weeks after the occupation and left out everyone then abroad. 2021 is the census bureau’s projection.', T_NOTE)
    s.append(txt_)
    return svg(y + 4, 'The population of Ramallah from 1838 to 2021 on an ordinary scale', ''.join(s))


# ───────────────────────────────────────────── five sons, eight clans
def fig_clans2():
    s = []
    sons = [('Haddad', 'the Hadadeh', [('Sharaka', 650), ('Jaghab', 675), ('Yousef', 750), ('ʿAwwaad', 625)], '2 · the Ḥaddāda, four seats'),
            ('Ibrahim', None, [('Ibrahim', 775)], '3 · Dār Ibrāhīm'),
            ('Jirius', None, [('Jirius', 550)], '1 · Dār Jiryis'),
            ('Shukair', None, [('Shakara', 660)], '4 · al-Shaqara'),
            ('Hassaan', None, [('Hassaan', 200)], '')]
    s.append(f'<rect x="132" y="6" width="136" height="30" rx="3" fill="{INK}"/>')
    s.append(t(200, 26, 'Rāshid', T_BIG, '#FFFFFF', 'middle', '700'))
    y = 56
    s.append(t(8, y, 'son', T_NOTE, NOTE, 'start', '400', 'italic'))
    s.append(t(96, y, 'clan', T_NOTE, NOTE, 'start', '400', 'italic'))
    s.append(t(W - 8, y, 'persons, 1944', T_NOTE, NOTE, 'end', '400', 'italic'))
    y += 8
    mx = 800
    bx0 = 182
    bw = W - 60 - bx0
    for son, grp, clans, dist in sons:
        top = y
        for nm, n in clans:
            w = bw * n / mx
            s.append(t(96, y + 17, nm, T_LAB, INK, 'start', '700'))
            s.append(f'<rect x="{bx0}" y="{y+5}" width="{w:.1f}" height="15" fill="{GOLD if grp else TINT[1]}"/>')
            s.append(t(bx0 + w + 5, y + 17, fmt(n), T_NOTE, INK))
            y += 27
        s.append(f'<line x1="86" y1="{top+6}" x2="86" y2="{y-4}" stroke="{GOLD if grp else TINT[2]}" stroke-width="3"/>')
        s.append(t(8, top + 17, son, T_LAB, INK, 'start', '700'))
        if grp:
            s.append(t(8, top + 33, grp, T_NOTE, GOLD, 'start', '400', 'italic'))
        if dist:
            s.append(t(96, y + 8, '1946 district ' + dist, T_NOTE, NOTE, 'start', '400', 'italic'))
            y += 18
        y += 8
        s.append(f'<line x1="8" y1="{y-4}" x2="{W-8}" y2="{y-4}" stroke="{RULE}"/>')
    txt_, y = para(8, y + 12, 'Haddad’s fifth was divided again among his sons: four clans, the Hadadeh (ochre). The other four sons’ lines are the Hamayel. ʿAwwaad includes ʿAzzouz, joined after the feud of 1820. Natives counted in 1944: 4,885. The 1946 districts are those named in the election papers.', T_NOTE)
    s.append(txt_)
    return svg(y + 4, 'Rāshid’s five sons, the eight clans, their numbers in 1944 and their election districts in 1946', ''.join(s))


# ───────────────────────────────────────────── the land's year, 1920
def fig_land():
    s = []
    crops = [('dried figs', 1_500_000), ('grapes', 1_200_000), ('olive oil', 84_000)]
    s.append(t(8, 16, 'What the land gave in 1920, in kilograms', T_LAB, INK, 'start', '700'))
    y = 30
    mx = 1_600_000
    for nm, v in crops:
        w = (W - 150) * v / mx
        s.append(t(92, y + 14, nm, T_LAB, BODY, 'end'))
        s.append(f'<rect x="100" y="{y+2}" width="{max(w,2):.1f}" height="16" fill="{TINT[0]}"/>')
        s.append(t(106 + max(w, 2), y + 14, fmt(v), T_LAB, INK, 'start', '700'))
        y += 26
    y += 10
    s.append(f'<line x1="8" y1="{y}" x2="{W-8}" y2="{y}" stroke="{RULE}"/>')
    y += 22
    s.append(t(8, y, 'The year, as Shāhīn tells it', T_LAB, INK, 'start', '700'))
    y += 10
    halves = [('Summer', 'From the fig harvest on, the family moves out to the qaṣr, the drystone tower in the groves; the figs dry below, the family sleeps above.'),
              ('Winter', 'Round the taboon, the clay oven five or six families share, heated three times a day and never let go out.')]
    for lab, what in halves:
        s.append(f'<rect x="8" y="{y+4}" width="{W-16}" height="2" fill="{GOLD}"/>')
        s.append(t(8, y + 24, lab, T_LAB, GOLD, 'start', '700'))
        lines = wrap(what, T_LAB, W - 96)
        for k, ln in enumerate(lines):
            s.append(t(82, y + 24 + k * 18, ln, T_LAB, BODY))
        y += 24 + 18 * len(lines) + 4
    txt_, y = para(8, y + 14, '“Eighty percent of the land is now uncultivated.” Shāhīn, 1982.', T_NOTE)
    s.append(txt_)
    return svg(y + 4, 'The crop of 1920 in kilograms, and the farming year at Ramallah', ''.join(s))


# ───────────────────────────────────────────── the camps, with people
def fig_camps():
    s = []
    camps = [('Qalandiyā', 8336), ('al-Jalazūn', 8201), ('al-Amʿarī', 4725), ('Qaddūra', 924)]
    s.append(t(8, 16, 'People living in each camp, 2017', T_LAB, INK, 'start', '700'))
    y = 28
    mx = 9000
    for nm, v in camps:
        w = (W - 170) * v / mx
        s.append(t(102, y + 14, nm, T_LAB, BODY, 'end'))
        s.append(f'<rect x="110" y="{y+2}" width="{w:.1f}" height="16" fill="{TINT[0]}"/>')
        s.append(t(116 + w, y + 14, fmt(v), T_LAB, INK, 'start', '700'))
        y += 26
    txt_, y = para(8, y + 12, 'The census bureau’s counts of the camp localities. UNRWA’s rolls count every registered refugee and descendant wherever they now live: al-Amʿarī, on 97 dunums, carries 15,315. Dayr ʿAmmār has no separate 2017 figure here.', T_NOTE)
    s.append(txt_)
    return svg(y + 4, 'People living in the four refugee camps by Ramallah in 2017', ''.join(s))
