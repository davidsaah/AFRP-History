# -*- coding: utf-8 -*-
"""v97: the film's maps and its clan tree, redrawn for the book.

David, 17 Nov 2026, on the visuals made for the film: "can you use any of
these in the book" — and "go" on the recommendation in
history/movie_to_book/README.md. The film drew these at 1920 x 1080; here they
are set again in the book's own style (docs/MAP_STYLE.md, map_style.py,
build_atlas.py): 860-unit plates with terrain, which phone_maps.py re-sets for
the phone, and one 400-unit phone-first diagram. The Acre and Safad map is
in PR 49, so it is not drawn here.

Every place, date and name on these plates is printed in the book's own text.
Where the film went further than the book (Dibbīn put in Lebanon, a Maʿalouf
family and "Bayt Jālā families" the book does not name, a Karak quotation of
1301 the book does not carry), the book wins and the extra is left out.
"""
import os
import re

import build_atlas as A
import map_style as MS
from build_atlas import Sheet, fit_box, mark, label, route, _plate, foot, plate_end, TERRAIN_SRC, txt, wrap
import build_figs6 as F6

RAM = (31.9038, 35.2034)
HERE = os.path.dirname(os.path.abspath(__file__))
REGIONAL = {'res': 1.6, 'wadi_km2': 400, 'wadi_cell': 2.5}


def _note(s, x, y, text, anchor='start', col=MS.NOTE, size=11.5):
    s.append(MS.text(x, y, text, size, col, anchor, '400', 'italic', halo=True))


def _box(s, x, y, w, h):
    s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#FFFFFF" stroke="{A.RULE}" rx="4"/>')


def _entries(s, bx, y, w, items, chars=40):
    """The evidence column: a heading per place, then its lines."""
    for head, body, col in items:
        s.append(txt(bx + 12, y, A.esc(head), 11, col, 'start', '700', 'normal', '.6'))
        y += 16
        for ln in wrap(body, chars):
            s.append(txt(bx + 12, y, A.esc(ln), 11, A.BODY))
            y += 13.5
        y += 12
    return y


# ═══════════════════════ the newcomers, about 1750 to 1880 ═══════════
NEWCOMERS = [
    # lat, lon, place, family, dates, clan on the roster, label dx, dy, anchor
    (32.33, 35.75, 'ʿAjlūn', 'the ʿAjlūnīs', 'about 1750 (Shāhīn) · 1825 (Cadora)', 'Jaghab', 10, 4, 'start'),
    (32.92, 35.07, 'Acre', 'the Hishmeh', 'about 1775, by Acre and Safad', 'ʿAwwād', -10, 4, 'end'),
    (32.22, 35.24, 'Rafīdiyā', 'the Nazzāl', 'about 1805 (Shāhīn) · 1855 (Cadora)', 'Sharaka', -10, 4, 'end'),
    (31.74, 34.97, 'Dayr Ibān', 'the ʿAraj, Zaghrūt and Shahla', 'about 1810 (Shāhīn) · 1850 (Cadora)', 'Sharaka', -10, 4, 'end'),
    (32.24, 35.82, 'Dibbīn', 'ʿAudeh al-Dibbini', '1860 (Shāhīn) · 1880 (Cadora)', 'ʿAwwād (Odeh)', 10, 4, 'start'),
]
REINA = (32.72, 35.32)


def fig_newcomers():
    W = 860
    s = _plate(W, 0, 'NEW FAMILIES ARRIVE, ABOUT 1750 TO 1880',
               'Where each newcomer family came from, when, and the clan whose roster carries it today. Where Shāhīn and Cadora give different years, both are shown.',
               'Atlas map of the families who settled in Ramallah between about 1750 and 1880 and where they came from')
    M = Sheet(*fit_box(34.62, 36.05, 31.55, 33.10, 430, 520), 44, 92, 430, 520)
    M.base(s, '10m', clipid='clip_newcomers97', terrain=dict(REGIONAL), key='newcomers97')
    M.graticule(s, 0.5, 0.5)
    M.sea(s, 32.45, 34.72, 'MEDITERRANEAN', 12, -72)
    for la, lo, *_ in NEWCOMERS:
        route(s, M, [(la, lo), RAM], col=MS.MEM, w=2.4)
    route(s, M, [(32.24, 35.82), REINA, RAM], col=MS.MEM, w=1.6, dash='3 3')
    for la, lo, place, fam, when, clan, dx, dy, an in NEWCOMERS:
        x, y = mark(s, M, la, lo, 'mem')
        label(s, x, y, place, dx, dy, an, 13)
    x, y = mark(s, M, *REINA, 'ctx')
    label(s, x, y, 'al-Reina', 9, 4, 'start', 13, MS.CONTEXT, '400')
    x, y = mark(s, M, 31.777, 35.231, 'ctx')
    label(s, x, y, 'Jerusalem', 9, 12, 'start', 13, MS.CONTEXT, '400')
    x, y = mark(s, M, *RAM, 'ram')
    label(s, x, y, 'RAMALLAH', -12, 4, 'end', 13.5, MS.RAMALLAH)
    M.scalebar(s)
    M.close(s)

    bx, bw = 494, 326
    _box(s, bx, 92, bw, M.h if M.h > 300 else 520)
    _entries(s, bx, 116, bw, [(f'{place.upper()} → {fam}', f'{when}. On the roster of {clan}.', MS.MEM)
                              for _la, _lo, place, fam, when, clan, *_r in NEWCOMERS], 44)
    yl = M.y + M.h + 30
    MS.legend(s, yl, [('mem', 'where the family remembers coming from'), ('route-mem', 'the move, as remembered'),
                      ('ctx', 'named for orientation'), ('ram', 'Ramallah')], rows=2)
    H = foot(s, W, yl + 46,
             'Each family was given land and folded into a clan, and the clan rosters still carry them. The years are family tradition, written down by Shāhīn and by Cadora, who do not agree.',
             'Shāhīn (1982), ch. 2, “Outsiders Who Settled in Ramallah”; Cadora, Remembering Ramallah (1954; English 2023), pp. 34–36; the AFRP clan rosters for the clans. '
             'Coastlines after Natural Earth; Lambert conformal conic. ' + TERRAIN_SRC)
    return plate_end(s, H)


# ═══════════════════════ five lights in the silence ════════════════════
LIGHTS = [
    (32.92, 35.94, 'al-Jābiya', '684', 'Ghassān still a people, at Marj Rāhiṭ', 10, 4, 'start'),
    (30.33, 35.60, 'Gharandal', 'about 890', 'al-Yaʿqūbī finds Ghassān here', 10, 4, 'start'),
    (32.03, 35.065, 'ʿAbūd', '1058', 'the village church is rebuilt', -10, 4, 'end'),
    (30.53, 35.56, 'al-Shawbak', '1321', '“most of its inhabitants are Christians”', 10, 4, 'start'),
]


def fig_lights():
    W = 860
    s = _plate(W, 0, 'FIVE LIGHTS IN THE SILENCE, 684 TO 1321',
               'Our line has no names between al-Ḥārith in 569 and Rāshid about 1500. The land does not go dark: these are dated records from inside the gap.',
               'Atlas map of five dated records between 684 and 1321, from al-Jābiya to al-Shawbak, inside the gap in the family line')
    M = Sheet(*fit_box(34.55, 36.35, 30.15, 33.15, 400, 560), 44, 92, 400, 560)
    M.base(s, '10m', clipid='clip_lights97', terrain=dict(REGIONAL), key='lights97')
    M.graticule(s, 0.5, 0.5)
    M.sea(s, 32.30, 34.72, 'MEDITERRANEAN', 12, -72)
    M.sea(s, 31.45, 35.48, 'DEAD SEA', 11, -78)
    for la, lo, nm, yr, what, dx, dy, an in LIGHTS:
        x, y = mark(s, M, la, lo, 'doc')
        label(s, x, y, nm, dx, dy, an, 13.5)
        _note(s, x + dx, y + dy + 15, yr, an, MS.DOC_DEEP)
    x, y = mark(s, M, *RAM, 'ram0')
    label(s, x, y, 'Ramallah', 12, 4, 'start', 13.5, MS.RAMALLAH)
    _note(s, x + 12, y + 19, '1186', 'start', MS.DOC_DEEP)
    M.scalebar(s)
    M.close(s)

    bx, bw = 464, 356
    _box(s, bx, 92, bw, 560)
    items = sorted([(yr, nm, what) for _la, _lo, nm, yr, what, *_r in LIGHTS] + [('1186', 'Ramallah', 'the name is first written, in a charter of King Guy')],
                   key=lambda r: int(re.sub(r'\D', '', r[0])))
    _entries(s, bx, 118, bw, [(f'{yr} · {nm.upper()}', what[0].upper() + what[1:] + '.', MS.DOC) for yr, nm, what in items], 50)
    yl = M.y + M.h + 30
    MS.legend(s, yl, [('doc', 'a dated record, in someone else’s document'),
                      ('ram0', 'Ramallah, before the family came')], rows=1)
    H = foot(s, W, yl + 26,
             'None of these names our family. All of them fall inside the blank our chart prints, and they show the people of these hills and of the plateau still there, still Christian, and in the case of Ghassān, still named.',
             'The Roots of Ramallah, chs. 5–6: Marj Rāhiṭ (684); al-Yaʿqūbī, about 890; the ʿAbūd church, 1058; the charter of 7 March 1186 (Strehlke 1869, no. 20); Abū al-Fidāʾ (1321) for al-Shawbak. '
             'Gharandal and al-Shawbak placed as on the book’s map of the road from Karak. Coastlines after Natural Earth; Lambert conformal conic. ' + TERRAIN_SRC)
    return plate_end(s, H)


# ═══════════════════════ June 1967 ══════════════════════════════════
# The armistice lines of 1949, simplified (the film's outline): the West Bank and Gaza.
WB = [(35.19, 32.53), (35.30, 32.55), (35.42, 32.50), (35.56, 32.39), (35.55, 32.20), (35.52, 32.00), (35.54, 31.85),
      (35.50, 31.77), (35.43, 31.70), (35.39, 31.60), (35.36, 31.49), (35.23, 31.39), (35.08, 31.35), (34.94, 31.36),
      (34.88, 31.41), (34.92, 31.52), (34.95, 31.60), (35.04, 31.66), (35.12, 31.71), (35.205, 31.775), (35.13, 31.81),
      (35.05, 31.83), (34.98, 31.85), (35.00, 31.92), (35.01, 31.98), (34.98, 32.08), (34.96, 32.18), (35.02, 32.30),
      (35.05, 32.40), (35.10, 32.47)]
GZ = [(34.22, 31.32), (34.27, 31.22), (34.37, 31.29), (34.49, 31.50), (34.57, 31.59), (34.49, 31.60), (34.37, 31.47)]
OCC = MS.ERA[1]


def _armistice():
    """The West Bank and the Gaza Strip as Natural Earth draws them (public
    domain), the same line the armistice map uses, so the two plates agree. The
    hand-simplified WB and GZ above were too coarse: the Gaza Strip came out as
    a wedge, and the West Bank lost the Latrun salient and the Jerusalem line."""
    import cartopy.io.shapereader as shp
    import shapefile
    r = shapefile.Reader(shp.natural_earth(resolution='10m', category='cultural', name='admin_0_map_units'))
    f = [x[0] for x in r.fields[1:]]
    out = {}
    for sr in r.iterShapeRecords():
        nm = dict(zip(f, sr.record)).get('NAME')
        if nm in ('West Bank', 'Gaza'):
            out[nm] = list(sr.shape.points)
    return out.get('West Bank', WB), out.get('Gaza', GZ)


def fig_june1967():
    W = 860
    s = _plate(W, 0, 'JUNE 1967: THE WEST BANK, EAST JERUSALEM AND GAZA OCCUPIED',
               'In six days the Israeli army took the West Bank, with East Jerusalem, and the Gaza Strip. Ramallah was taken on 6 June.',
               'Atlas map of the West Bank, East Jerusalem and the Gaza Strip, occupied in June 1967, with Ramallah')
    M = Sheet(*fit_box(34.15, 35.80, 31.15, 32.70, 520, 520), 44, 92, 520, 520)
    M.base(s, '10m', clipid='clip_june97', terrain=dict(REGIONAL), key='june97')
    M.graticule(s, 0.5, 0.5)
    M.sea(s, 32.00, 34.45, 'MEDITERRANEAN', 12, -72)
    M.sea(s, 31.50, 35.48, 'DEAD SEA', 11, -78)
    s.append(f'<g clip-path="url(#{M._cid})">')
    for poly in _armistice():
        d = 'M' + ' L'.join('%.1f %.1f' % M.P(la, lo) for lo, la in poly) + 'Z'
        s.append(f'<path d="{d}" fill="{OCC}" fill-opacity=".20" stroke="{OCC}" stroke-width="2" stroke-linejoin="round"/>')
    s.append('</g>')
    M.region(s, 32.30, 35.28, 'WEST BANK', 13, OCC)
    M.region(s, 31.62, 34.30, 'GAZA', 13, OCC)
    x, y = mark(s, M, 31.778, 35.235, 'era1')
    label(s, x, y, 'East Jerusalem', 10, 14, 'start', 13)
    for la, lo, nm in [(32.221, 35.262, 'Nablus'), (31.53, 35.10, 'Hebron'), (32.08, 34.78, 'Jaffa')]:
        x, y = mark(s, M, la, lo, 'ctx')
        label(s, x, y, nm, 9, 4, 'start', 13, MS.CONTEXT, '400')
    x, y = mark(s, M, *RAM, 'ram')
    label(s, x, y, 'RAMALLAH', -12, 4, 'end', 13.5, MS.RAMALLAH)
    M.scalebar(s)
    M.close(s)

    bx, bw = 584, 236
    _box(s, bx, 92, bw, M.h)
    _entries(s, bx, 116, bw, [
        ('5–10 JUNE 1967', 'The war of six days. The West Bank, East Jerusalem and Gaza are occupied.', OCC),
        ('6 JUNE · RAMALLAH', 'The Israeli army takes the town and makes the Odeh Hotel its first headquarters. Every weapon is to be handed in at al-Manāra.', MS.RAMALLAH),
        ('THE CENSUS', 'The occupier’s census of September 1967 counts only those who were there. Everyone away loses the right to live in the town.', OCC),
    ], 33)
    yl = M.y + M.h + 30
    s.append(f'<rect x="{40+8-7}" y="{yl-6}" width="14" height="12" fill="{OCC}" fill-opacity=".20" stroke="{OCC}" stroke-width="1.6"/>')
    s.append(MS.text(40 + 8 + 14, yl + 4, 'occupied in June 1967 (inside the armistice lines of 1949)', MS.T_FURN, MS.BODY))
    MS.legend(s, yl + 20, [('era1', 'East Jerusalem'), ('ctx', 'named for orientation'), ('ram', 'Ramallah')])
    H = foot(s, W, yl + 40,
             'Ramallah has been under occupation since 6 June 1967. Many of the town’s people were abroad that June, and could not come home.',
             'ARIJ for 6 June 1967; the town’s own record for the Odeh Hotel and al-Manāra; the September 1967 census, as in chapter 12. The 1949 armistice lines after Natural Earth (public domain), generalised for this scale, and not a survey. '
             'Coastlines after Natural Earth; Lambert conformal conic. ' + TERRAIN_SRC)
    return plate_end(s, H)


# ═══════════════════════ find your name ══════════════════════════════
SONS = [('Haddad', ['Jaghab', 'Yousef', 'Sharaka', 'ʿAwwād']), ('Ibrahim', ['Ibrahim']), ('Jirius', ['Jirius']),
        ('Shukair', ['Shakara']), ('Hassaan', ['Hassaan'])]


def _roster():
    """The clans and families exactly as the book's roster table prints them."""
    src = open(os.path.join(HERE, 'build_v5.py'), encoding='utf-8').read()
    m = re.search(r'THE EIGHT CLANS AND THEIR FAMILIES.*?<tbody>(.*?)</tbody>', src, re.S)
    out = {}
    for clan, fams in re.findall(r'<tr><td class="when">(.*?)</td><td>(.*?)</td></tr>', m.group(1)):
        out[re.sub(r'<span.*?</span>', '', clan).strip()] = [f.strip() for f in fams.split(',')]
    assert len(out) == 8, out.keys()
    return out


def _wrap_names(names, size, width):
    """Wrap a list of names joined by middle dots, never starting a line with a dot."""
    per = max(8, int(width / (size * 0.47)))
    lines, cur = [], ''
    for nm in names:
        nxt = (cur + ' · ' + nm) if cur else nm
        if cur and len(nxt) > per:
            lines.append(cur + ' ·')
            cur = nm
        else:
            cur = nxt
    return lines + ([cur] if cur else [])


def fig_findname():
    t, svg, W = F6.t, F6.svg, F6.W
    R = _roster()
    s = []
    s.append(f'<rect x="8" y="6" width="170" height="30" rx="15" fill="#FFFFFF" stroke="{F6.GOLD}" stroke-width="1.6"/>')
    s.append(t(93, 26, 'Rāshid al-Ḥaddādīn', F6.T_LAB, F6.INK, 'middle', '700'))
    y = 52
    joins = []
    for son, clans in SONS:
        joins.append(y)
        s.append(f'<rect x="20" y="{y}" width="{W-28}" height="2" fill="{F6.GOLD}"/>')
        hd = son + (', and his four clans, the Hadadeh' if len(clans) > 1 else '')
        s.append(t(28, y + 20, hd, F6.T_NOTE, F6.GOLD, 'start', '700' if False else '400', 'italic'))
        y += 30
        for cl in clans:
            fams = R[cl]
            s.append(f'<rect x="28" y="{y}" width="{len(cl)*8.6+22:.0f}" height="24" rx="12" fill="#EAF4EE" stroke="{MS.DOC}" stroke-width="1.4"/>')
            s.append(t(39, y + 17, cl, F6.T_LAB, MS.DOC_DEEP, 'start', '700'))
            s.append(t(W - 8, y + 17, f'{len(fams)} families', 13, F6.NOTE, 'end', '400', 'italic'))
            y += 42
            for ln in _wrap_names(fams, F6.T_LAB, W - 44):
                s.append(t(36, y, ln, F6.T_LAB, F6.BODY))
                y += 19
            y += 10
    # the comb: Rāshid's line down the left, one tooth to each son
    s.append(f'<line x1="20" y1="36" x2="20" y2="{joins[-1]+1}" stroke="{F6.GOLD}" stroke-width="2"/>')
    txt_, y = F6.para(8, y + 8, 'Every family on the AFRP rosters, under the son and the clan that carry it. A few names are on two rosters, and are shown twice, as the sheets have them. The last four sons’ clans are the Hamayel.', F6.T_NOTE)
    s.append(txt_)
    return svg(y + 4, 'Find your name: Rāshid, his five sons, the eight clans and every family on the clan rosters', ''.join(s))
