# -*- coding: utf-8 -*-
"""v103: charts and maps for the wars and the occupation (chapters 10 to 12).

David, 18 Nov 2026, on the wars plan: "I would also like to get a chart photos
and figures to help". Phase 1 of book_gaps/wars_visuals_plan.md (Claud_Migration).

* fig_wars_century: the table "The wars around us, 1911–2025" (modern.WARS_AROUND_US),
  drawn as one timeline. Dark bars reached the town; pale bars were felt from a distance.
* fig_settlements: the settlements around Ramallah by the year each was set down,
  from ARIJ's table of settlements in the governorate (2015 profile, table 34),
  the table the book already cites.
* fig_front1918: the front of March to September 1918 north of the town.
* fig_raids: the armistice line of 1949 and the raids across it to 1967.

Every place, year and number on these plates is printed in the book's text,
or in the ARIJ table the text cites.
"""
import re

from build_figs6 import W, AXIS, RULE, TINT, GOLD, T_LAB, T_NOTE, t, para, svg, fmt
from map_style import INK, BODY, NOTE, RAMALLAH
import map_style as MS
import build_atlas as A
import modern

RAM = (31.9038, 35.2034)


# ───────────────────────────────────────────── a century of wars around the town
def _years(when):
    ys = [int(y) for y in re.findall(r'\d{4}', when)]
    if '–' in when and len(ys) >= 2:
        return [(ys[0], ys[1])] if ',' not in when else [(ys[0], ys[1])] + [(y, y) for y in ys[2:]]
    return [(y, y) for y in ys]


def fig_wars_century():
    rows = modern.WARS_AROUND_US
    x0, x1 = 150, W - 10
    lo, hi = 1910, 2026
    X = lambda y: x0 + (y - lo) / (hi - lo) * (x1 - x0)
    s = []
    # legend
    s.append(f'<rect x="8" y="8" width="22" height="11" fill="{TINT[0]}"/>')
    s.append(t(36, 18, 'reached the town', T_NOTE, BODY))
    s.append(f'<rect x="170" y="8" width="22" height="11" fill="{TINT[2]}"/>')
    s.append(t(198, 18, 'felt from a distance', T_NOTE, BODY))
    top = 40
    rh = 27
    for yr in (1920, 1940, 1960, 1980, 2000, 2020):
        s.append(f'<line x1="{X(yr):.1f}" y1="{top-6}" x2="{X(yr):.1f}" y2="{top + len(rows)*rh}" stroke="{RULE}"/>')
    for i, (when, war, what) in enumerate(rows):
        y = top + i * rh
        far = what.startswith('Felt from a distance')
        col = TINT[2] if far else TINT[0]
        lines = [war] if len(war) <= 21 else [war[:war.rfind(';', 0, 22) + 1] or war[:21], war[war.rfind(';', 0, 22) + 2:]]
        for j, ln in enumerate(lines):
            s.append(t(8, y + (15 if len(lines) == 1 else 9 + j * 13), ln, T_NOTE if len(lines) == 1 else 12.5,
                       NOTE if far else INK, 'start', '400' if far else '700'))
        for a, b in _years(when):
            xa, xb = X(a), X(b + 1)
            s.append(f'<rect x="{xa:.1f}" y="{y+5}" width="{max(xb-xa, 3.5):.1f}" height="14" fill="{col}"/>')
    yb = top + len(rows) * rh
    s.append(f'<line x1="{x0}" y1="{yb}" x2="{x1}" y2="{yb}" stroke="{AXIS}"/>')
    for yr in (1920, 1940, 1960, 1980, 2000, 2020):
        s.append(t(X(yr), yb + 17, str(yr), T_NOTE, NOTE, 'middle'))
    # the occupation as a band under the axis
    yo = yb + 30
    s.append(f'<rect x="{X(1967):.1f}" y="{yo}" width="{X(2026)-X(1967):.1f}" height="10" fill="{MS.ERA[1]}" fill-opacity=".35"/>')
    s.append(t(X(1967) - 4, yo + 9, 'under occupation from 6 June 1967', T_NOTE, BODY, 'end', '400', 'italic'))
    far = sum(1 for r in rows if r[2].startswith('Felt from a distance'))
    NUM = {4: 'Four', 5: 'Five', 18: 'Eighteen', 17: 'Seventeen', 22: 'Twenty-two'}
    txt_, y = para(8, yo + 34, f'{NUM[len(rows)]} wars in a little over a century. {NUM[len(rows)-far]} of them reached the town, through its men, its hunger, its refugees and its curfews; {NUM[far].lower()} were felt from a distance. The years are those of the table at the end of chapter 12.', T_NOTE)
    s.append(txt_)
    return svg(y + 4, 'A timeline of the wars from 1911 to 2025, marking those that reached Ramallah and those felt from a distance', ''.join(s))


# ───────────────────────────────────────────── the settlements, by the year each was set down
# ARIJ, Ramallah Governorate profile (2015), table 34: settlement, year of establishment.
SETTLEMENTS = [
    ('Canada Park', 1968), ('Mevo Horon', 1969), ('Oasis of Peace', 1970), ('Ofra', 1975),
    ('Beit El', 1977), ('Beit Horon', 1977), ('Hallamish', 1977), ('Kfar Rut', 1977), ('Kokhav HaShahar', 1977),
    ('Rimonim', 1977), ('Shilat', 1977), ('Shilo', 1978), ('Mattityahu', 1980), ('Ateret', 1981),
    ('Beit Arye', 1981), ('Maʿale Mikhmas', 1981), ('Nili', 1981), ('Psagot', 1981), ('Makkabim', 1982),
    ('Naʿaleh', 1982), ('Dolev', 1983), ('Maʿale Levona', 1983), ('Kokhav Yaʿacov', 1984), ('Nahliel', 1984),
    ('Hashmonaim', 1985), ('Ofarim', 1988), ('Talmon', 1989), ('Modiʿin Illit', 1991), ('Mizpe Rahel', 1992),
    ('Lapid', 1996), ('Menora', 1998),
]
NAMED = {'Ofra', 'Beit El', 'Psagot', 'Kokhav Yaʿacov', 'Modiʿin Illit'}


def fig_settlements():
    s = []
    x0, x1 = 20, W - 20
    lo, hi = 1966, 2000
    X = lambda y: x0 + (y - lo) / (hi - lo) * (x1 - x0)
    base = 250
    r = 6.4
    count = {}
    pos = {}
    for nm, yr in sorted(SETTLEMENTS, key=lambda e: (e[1], e[0] in NAMED)):
        k = count.get(yr, 0)
        count[yr] = k + 1
        cx, cy = X(yr + .5), base - r - 2 - k * (2 * r + 2)
        pos[nm] = (cx, cy)
        s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{INK if nm in NAMED else TINT[1]}"/>')
    s.append(f'<line x1="{x0}" y1="{base}" x2="{x1}" y2="{base}" stroke="{AXIS}"/>')
    for yr in (1970, 1980, 1990, 2000):
        s.append(f'<line x1="{X(yr):.1f}" y1="{base}" x2="{X(yr):.1f}" y2="{base+5}" stroke="{AXIS}"/>')
        s.append(t(X(yr), base + 20, str(yr), T_NOTE, NOTE, 'middle'))
    # names for the five the book's text names, on leaders above the stacks
    labs = [('Ofra', 1975, 70), ('Beit El', 1977, 40), ('Psagot', 1981, 70), ('Kokhav Yaʿacov', 1984, 110), ('Modiʿin Illit', 1991, 150)]
    for nm, yr, ly in labs:
        cx, cy = pos[nm]
        s.append(f'<line x1="{cx:.1f}" y1="{cy-r:.1f}" x2="{cx:.1f}" y2="{ly+4}" stroke="{INK}" stroke-width=".8"/>')
        s.append(t(cx, ly, nm, T_NOTE, INK, 'middle', '700'))
    # the decades in words
    y = base + 44
    s.append(t(8, y, 'Set down: 2 in the late 1960s, 10 in the 1970s,', T_LAB, INK))
    s.append(t(8, y + 19, '15 in the 1980s, 4 in the 1990s.', T_LAB, INK))
    y += 40
    s.append(f'<line x1="8" y1="{y}" x2="{W-8}" y2="{y}" stroke="{RULE}"/>')
    y += 22
    s.append(t(8, y, 'And after', T_LAB, INK, 'start', '700'))
    y += 8
    for lab, v, mx, col in (('settlers in the governorate, 2011', 121856, 160000, TINT[1]),
                            ('settlers in the governorate, 2023', 150000, 160000, TINT[0])):
        w = (W - 16) * v / mx
        s.append(f'<rect x="8" y="{y+4}" width="{w:.1f}" height="14" fill="{col}"/>')
        s.append(t(8, y + 36, lab + (': ' + fmt(v) if v != 150000 else ': about 150,000'), T_NOTE, BODY))
        y += 46
    s.append(t(8, y + 14, '2025: fourteen new outposts in one year.', T_LAB, INK, 'start', '700'))
    txt_, y = para(8, y + 38, 'Each dot is one settlement in Ramallah and al-Bīra governorate, by the year ARIJ gives for it; two more have no year. Dark dots are those the text names. An outpost is a new hilltop camp, often a farm, set down without a government decision.', T_NOTE)
    s.append(txt_)
    return svg(y + 4, 'The thirty-one dated settlements of Ramallah governorate by the year each was set down, 1968 to 1998, with the settler population in 2011 and 2023', ''.join(s))


# ───────────────────────────────────────────── the front of 1918
FRONT = [(32.017, 35.120), (32.005, 35.200), (31.997, 35.285), (31.983, 35.300)]   # Nabī Ṣāliḥ … Tell ʿĀṣūr, Kafr Mālik


def fig_front1918():
    W8 = 860
    s = A._plate(W8, 0, 'THE FRONT, MARCH TO SEPTEMBER 1918',
                 'The British took Ramallah on 29 December 1917. From March 1918 the line ran a few kilometres north of the town, from Kafr Mālik by Tell ʿĀṣūr to Nabī Ṣāliḥ, and held until September.',
                 'Map of the First World War front line north of Ramallah, March to September 1918')
    M = A.Sheet(*A.fit_box(35.05, 35.38, 31.76, 32.10, 772, 520), 44, 92, 772, 520)
    M.base(s, '10m', rivers=False, clipid='clip_front18', terrain={'contour': 200, 'wadi_km2': 8}, key='front1918')
    M.graticule(s, 0.1, 0.1)
    d = ''.join(('M' if i == 0 else 'L') + '%.1f %.1f' % M.P(la, lo) for i, (la, lo) in enumerate(FRONT))
    s.append(f'<g clip-path="url(#{M._cid})">')
    s.append(f'<path d="{d}" fill="none" stroke="#FFFAF0" stroke-width="6" opacity=".6"/>')
    s.append(f'<path d="{d}" fill="none" stroke="{MS.LINE_ARMY}" stroke-width="2.2" stroke-dasharray="9 3"/>')
    s.append('</g>')
    x, y = M.P(32.06, 35.22)
    s.append(MS.text(x, y, 'OTTOMAN LINES', MS.T_REGION, '#8A7457', 'middle', '700', 'normal', '1.6', halo=True))
    x, y = M.P(31.93, 35.30)
    s.append(MS.text(x, y, 'BRITISH-HELD', MS.T_REGION, '#8A7457', 'middle', '700', 'normal', '1.6', halo=True))
    for la, lo, nm, dx, an in [(32.017, 35.120, 'Nabī Ṣāliḥ', -10, 'end'), (31.997, 35.285, 'Tell ʿĀṣūr', 10, 'start'),
                               (31.983, 35.300, 'Kafr Mālik', 10, 'start')]:
        x, y = A.mark(s, M, la, lo, 'doc')
        A.label(s, x, y, nm, dx, -8 if nm == 'Tell ʿĀṣūr' else 10, an, 13)
    for la, lo, nm, dx, dy, an in [(31.972, 35.195, 'Bīr Zayt', -10, 4, 'end'), (31.962, 35.215, 'Jifnā', 10, 4, 'start'),
                                   (31.911, 35.216, 'al-Bīra', 10, 6, 'start'), (31.80, 35.22, 'Jerusalem', 10, 4, 'start')]:
        x, y = A.mark(s, M, la, lo, 'ctx')
        A.label(s, x, y, nm, dx, dy, an, 13, MS.BODY, '400')
    x, y = A.mark(s, M, *RAM, 'ram')
    A.label(s, x, y, 'RAMALLAH', -12, 4, 'end', 13.5, MS.RAMALLAH)
    A.label(s, x, y, '74th Casualty Clearing Station, 1918', -12, 20, 'end', 11.5, NOTE, '400')
    M.scalebar(s)
    M.close(s)
    LY = M.y + M.h + 34
    s.append(f'<line x1="44" y1="{LY}" x2="72" y2="{LY}" stroke="{MS.LINE_ARMY}" stroke-width="2.2" stroke-dasharray="9 3"/>')
    s.append(MS.text(80, LY + 4, 'the front line, March–September 1918 (its course approximate)', MS.T_FURN, MS.BODY))
    MS.legend(s, LY + 22, [('doc', 'named in the war histories'), ('ctx', 'named for orientation'), ('ram', 'Ramallah')])
    H = A.foot(s, W8, LY + 44,
               'For nine months the war stood still within sight of the town: the British at Ramallah, the Ottoman army on the hills to the north.',
               'Cadora and Nayrūz for the town; Cyril Falls, Military Operations: Egypt and Palestine, vol. 2 (1930), for the line; Australian War Memorial H00687 for the clearing station. Lambert conformal conic; contours every 200 m. ' + A.TERRAIN_SRC)
    return A.plate_end(s, H)


# ───────────────────────────────────────────── the armistice line and the raids, 1949–1967
def _west_bank():
    import cartopy.io.shapereader as shp
    import shapefile
    r = shapefile.Reader(shp.natural_earth(resolution='10m', category='cultural', name='admin_0_map_units'))
    f = [x[0] for x in r.fields[1:]]
    for sr in r.iterShapeRecords():
        if dict(zip(f, sr.record)).get('NAME') == 'West Bank':
            return [(la, lo) for lo, la in sr.shape.points]


def fig_raids():
    W8 = 860
    s = A._plate(W8, 0, 'THE ARMISTICE LINE AND THE RAIDS, 1949–1967',
                 'From 1949 the town lay a short drive from the armistice line. Raids across it struck the villages of the district and beyond.',
                 'Map of the 1949 armistice line around the West Bank with the raids on Qibya, Qalqīliya and al-Samūʿ, and Ramallah')
    M = A.Sheet(*A.fit_box(34.70, 35.62, 31.30, 32.32, 520, 560), 44, 92, 520, 560)
    M.base(s, '10m', clipid='clip_raids', terrain={'res': 1.6, 'wadi_km2': 400, 'wadi_cell': 2.5}, key='raids4967')
    M.graticule(s, 0.25, 0.25)
    M.sea(s, 31.85, 34.80, 'MEDITERRANEAN', 12, -72)
    M.sea(s, 31.55, 35.49, 'DEAD SEA', 11, -78)
    wb = _west_bank()
    d = 'M' + ' L'.join('%.1f %.1f' % M.P(la, lo) for la, lo in wb) + 'Z'
    s.append(f'<g clip-path="url(#{M._cid})">')
    s.append(f'<path d="{d}" fill="none" stroke="#FFFAF0" stroke-width="5.5" opacity=".6"/>')
    s.append(f'<path d="{d}" fill="none" stroke="{MS.LINE_ARMY}" stroke-width="2.2"/>')
    s.append('</g>')
    M.region(s, 32.05, 35.38, 'WEST BANK', 13)
    raids = [(31.982, 35.007, 'Qibya', '14–15 October 1953: 69 killed', 'end', -12),
             (32.190, 34.970, 'Qalqīliya', '10 October 1956', 'end', -12),
             (31.400, 35.070, 'al-Samūʿ', 'November 1966', 'start', 12)]
    for la, lo, nm, note, an, dx in raids:
        x, y = A.mark(s, M, la, lo, 'doc')
        A.label(s, x, y, nm, dx, 0, an, 13.5)
        A.label(s, x, y, note, dx, 15, an, 11.5, NOTE, '400')
    x, y = A.mark(s, M, 31.948, 35.215, 'doc')
    A.label(s, x, y, 'al-Jalazūn', 10, -8, 'start', 13)
    A.label(s, x, y, 'protest put down, 1966', 10, 7, 'start', 11.5, NOTE, '400')
    for la, lo, nm in [(31.778, 35.235, 'Jerusalem'), (32.221, 35.262, 'Nablus'), (31.53, 35.10, 'Hebron')]:
        x, y = A.mark(s, M, la, lo, 'ctx')
        A.label(s, x, y, nm, 9, 4, 'start', 13, MS.BODY, '400')
    x, y = A.mark(s, M, *RAM, 'ram')
    A.label(s, x, y, 'RAMALLAH', 12, 14, 'start', 13.5, MS.RAMALLAH)
    M.scalebar(s)
    M.close(s)
    bx, bw = 584, 236
    s.append(f'<rect x="{bx}" y="92" width="{bw}" height="{M.h}" fill="#FFFFFF" stroke="{A.RULE}" rx="4"/>')
    yy = 118
    for head, body in [('QIBYA, 1953', 'A village of what is now the Ramallah governorate. On the night of 14–15 October the army blew up its houses with people inside: sixty-nine killed.'),
                       ('QALQĪLIYA, 1956', 'A raid on 10 October, days before Israel invaded Sinai, in concert with Britain and France.'),
                       ('AL-SAMŪʿ, 1966', 'A raid near Hebron in November. The camps rose; at al-Jalazūn, north of the town, the Jordanian army put the protest down.')]:
        s.append(A.txt(bx + 14, yy, head, 11.5, MS.DOC_DEEP, 'start', '700', 'normal', '.6'))
        for i, ln in enumerate(A.wrap(body, 34)):
            s.append(A.txt(bx + 14, yy + 18 + i * 15, ln, 11.5, BODY))
        yy += 40 + i * 15 + 10
    LY = M.y + M.h + 34
    s.append(f'<line x1="44" y1="{LY}" x2="72" y2="{LY}" stroke="{MS.LINE_ARMY}" stroke-width="2.2"/>')
    s.append(MS.text(80, LY + 4, 'the West Bank: the armistice line of 1949 to the west, the Jordan to the east (after Natural Earth)', MS.T_FURN, MS.BODY))
    MS.legend(s, LY + 22, [('doc', 'a raid or a protest the book records'), ('ctx', 'named for orientation'), ('ram', 'Ramallah')])
    H = A.foot(s, W8, LY + 44,
               'Between the two wars the line was never far from the town. The raids punished whole villages, and in 1966 the anger reached the camps outside Ramallah.',
               'United Nations Security Council S/3113 (1953) for Qibya and S/3670 (1956) for Qalqīliya; the Journal of Palestine Studies (2007) for al-Samūʿ and al-Jalazūn, as in chapter 11. The line after Natural Earth (public domain); Lambert conformal conic. ' + A.TERRAIN_SRC)
    return A.plate_end(s, H)
