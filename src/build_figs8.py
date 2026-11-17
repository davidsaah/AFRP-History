# -*- coding: utf-8 -*-
"""v99: two figures taken from the history movie into the book.

The movie (Drive, Family Tree / Video / History – The Roots of Ramallah) drew
its frames from this book. Two of its pictures have no figure here yet: the
1561 division of the hill into thirds, and the Saah builders' road to Acre and
Safad. Both are drawn in the book's own styles, the chart as a v80 phone-first
plate (400 units, nothing under 14 units, see src/build_figs6.py) and the map
on the atlas sheets (src/build_atlas.py, docs/MAP_STYLE.md).

Every word and number on the two plates is in the book's own text: the court
record of 1 April 1561 in "The people of Ramallah speak", and Cadora's story
in "The Saah builders and Acre".
"""
from build_figs6 import W, AXIS, RULE, TINT, GOLD, T_LAB, T_NOTE, t, para, svg
from map_style import INK, BODY, NOTE, DOC, MEM
import map_style as MS
import build_atlas as A


# ───────────────────────────────────────────── one hill, in thirds and in fifths
def fig_thirds():
    """The court's thirds of 1561 against the tradition's fifths."""
    s = []
    y = 20
    s.append(t(8, y, 'In court, Jerusalem, 1 April 1561', T_LAB, INK, 'start', '700'))
    s.append(t(W - 8, y, 'documented', T_NOTE, DOC, 'end', '400', 'italic'))
    y += 12
    thirds = [('Muslim', 'ʿAlī bin Ḥasan, his brother ʿUmar,', 'Aḥmad bin Muḥammad', TINT[2], INK),
              ('Christian', 'Ghunaym', 'and his people', TINT[0], '#FFFFFF'),
              ('Christian', 'Mūsā and Isḥāq', 'and their people', TINT[0], '#FFFFFF')]
    bw = (W - 16 - 8) / 3
    bh = 92
    for i, (who, l1, l2, col, tc) in enumerate(thirds):
        x = 8 + i * (bw + 4)
        s.append(f'<rect x="{x:.1f}" y="{y}" width="{bw:.1f}" height="{bh}" fill="{col}"/>')
        s.append(t(x + bw / 2, y + 30, '⅓', 26, tc, 'middle', '700'))
        s.append(t(x + bw / 2, y + 54, who, T_NOTE, tc, 'middle', '700'))
        if i == 0:
            s.append(t(x + bw / 2, y + 72, 'ʿAlī, ʿUmar,', T_NOTE, tc, 'middle'))
            s.append(t(x + bw / 2, y + 87, 'Aḥmad', T_NOTE, tc, 'middle'))
        else:
            s.append(t(x + bw / 2, y + 72, l1, T_NOTE, tc, 'middle'))
            s.append(t(x + bw / 2, y + 87, l2.replace('and ', ''), T_NOTE, tc, 'middle'))
    y += bh + 10
    # the brace: two thirds to the newcomers, one third to the men who held it
    xa, xb = 8 + bw + 4, W - 8
    s.append(f'<path d="M{xa:.1f} {y} v8 H{xb:.1f} v-8" fill="none" stroke="{INK}" stroke-width="1.6"/>')
    s.append(t((xa + xb) / 2, y + 26, 'two thirds to the newcomers', T_NOTE, INK, 'middle', '700'))
    s.append(f'<path d="M8 {y} v8 H{8 + bw:.1f} v-8" fill="none" stroke="{AXIS}" stroke-width="1.6"/>')
    s.append(t(8 + bw / 2, y + 26, 'one third to the', T_NOTE, BODY, 'middle'))
    s.append(t(8 + bw / 2, y + 42, 'men who held it', T_NOTE, BODY, 'middle'))
    y += 66
    txt_, y = para(8, y, 'Six men of Ramallah swear to plough this hill and no other until it is all under crop, on pain of one hundred gold sulṭānī to the kitchen of Khalīl al-Raḥmān.', T_NOTE)
    s.append(txt_)

    # the tradition's fifths
    y += 18
    s.append(f'<line x1="8" y1="{y-12}" x2="{W-8}" y2="{y-12}" stroke="{RULE}"/>')
    s.append(t(8, y + 6, 'As the town remembers it', T_LAB, INK, 'start', '700'))
    s.append(t(W - 8, y + 6, 'remembered', T_NOTE, MEM, 'end', '400', 'italic'))
    y += 18
    sons = ['Haddad', 'Ibrahim', 'Jirius', 'Shukair', 'Hassaan']
    fw = (W - 16 - 4 * 4) / 5
    for i, son in enumerate(sons):
        x = 8 + i * (fw + 4)
        s.append(f'<rect x="{x:.1f}" y="{y}" width="{fw:.1f}" height="54" fill="#F6EEDF" stroke="{MEM}" stroke-width="1.2"/>')
        s.append(t(x + fw / 2, y + 23, '⅕', 20, MEM, 'middle', '700'))
        s.append(t(x + fw / 2, y + 44, son, T_NOTE, INK, 'middle', '700'))
    y += 54 + 22
    txt_, y = para(8, y, 'The tradition divides the land into fifths among Rāshid’s five sons. Both can be true: the thirds are the arrangement with the neighbours, made in court the year before the census of 1562; the fifths are the arrangement inside the family.', T_NOTE)
    s.append(txt_)
    return svg(y + 4, 'The hill of Ramallah divided into thirds in court in 1561, two thirds to the Christian newcomers and one third to the Muslims already there, beside the tradition’s fifths among Rāshid’s five sons', ''.join(s))


# ───────────────────────────────────────────── the Saah builders, Acre and Safad
ACRE = (32.923, 35.069)
SAFAD = (32.965, 35.496)
RAM = (31.9038, 35.2034)


def fig_acre():
    W8 = 860
    s = A._plate(W8, 0, 'THE SAAH BUILDERS: TO ACRE, TO SAFAD, AND HOME',
                 'The family’s story as Cadora heard it. The lines give the order of the moves, not the roads taken.',
                 'Map of the remembered moves of the Saah builders from Ramallah to Acre about 1775, then to Safad, and home after fifteen years')
    M = A.Sheet(*A.fit_box(34.62, 35.82, 31.66, 33.22, 772, 560), 44, 84, 772, 560)
    M.base(s, '10m', rivers=True, clipid='clip_acre', terrain={'res': 1.6, 'wadi_km2': 400, 'wadi_cell': 2.5}, key='acre_safad')
    M.graticule(s, 0.5, 0.5)
    M.close(s)
    M.sea(s, 32.45, 34.72, 'MEDITERRANEAN', 12, -70)
    M.sea(s, 32.80, 35.66, 'Lake Tiberias', 11, -70)
    # the three moves, all remembered
    A.route(s, M, [RAM, (32.45, 35.05), ACRE], col=MS.MEM, w=2.6)
    A.route(s, M, [ACRE, (32.97, 35.28), SAFAD], col=MS.MEM, w=2.6)
    A.route(s, M, [SAFAD, (32.45, 35.40), (32.10, 35.30), RAM], col=MS.MEM, w=2.6)
    # the stations
    x, y = A.mark(s, M, *ACRE, 'mon')
    A.label(s, x, y, 'ACRE', -12, -4, 'end', 13.5)
    A.label(s, x, y, 'al-Jazzār’s walls, 1776–1804', -12, 12, 'end', 11.5, NOTE, '400')
    x, y = A.mark(s, M, *SAFAD, 'mem')
    A.label(s, x, y, 'SAFAD', 12, -4, 'start', 13.5)
    A.label(s, x, y, 'fifteen years; Hishmeh marries Khaled', 12, 12, 'start', 11.5, NOTE, '400')
    x, y = A.mark(s, M, *RAM, 'ram')
    A.label(s, x, y, 'RAMALLAH', 12, 4, 'start', 13.5, MS.RAMALLAH)
    for la, lo, nm, dx, an in [(31.778, 35.235, 'Jerusalem', 12, 'start'),
                               (32.222, 35.262, 'Nablus', 12, 'start')]:
        x, y = A.mark(s, M, la, lo, 'ctx')
        A.label(s, x, y, nm, dx, 4, an, 13, MS.BODY, '400')
    # the move numbers
    for (la, lo), n in [((32.45, 35.05), '1'), ((32.97, 35.28), '2'), ((32.30, 35.37), '3')]:
        bx, by = M.P(la, lo)
        s.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="12.2" fill="#FFFAF0" opacity=".95"/>')
        s.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="9.6" fill="{MS.MEM}" stroke="#FFFFFF" stroke-width="1.6"/>')
        s.append(A.txt(bx, by + 3.7, n, 10.6, '#FFFFFF', 'middle', '700'))
    M.scalebar(s)
    LY = M.y + M.h + 34
    MS.legend(s, LY, [('mem', 'remembered station'),
                      ('mon', 'standing evidence: the walls of Acre'),
                      ('route-mem', 'remembered move'), ('ram', 'Ramallah')], rows=1)
    H = A.foot(s, W8, LY + 30,
               '1 · About 1775, al-Jazzār’s men take the Saah builders to rebuild the walls of Acre. 2 · When the work is done they escape, but go to Safad, not home. 3 · Fifteen years later Yaʿqūb of the Ḥaddādīn brings them back, with a new name, al-Ṣafadī.',
               'Cadora, Remembering Ramallah (1954; trans. 2023), as the families told it; al-Jazzār at Acre 1776–1804, and Buckingham (1816) on “the work of Djezzar Pasha”. Coastlines, rivers and lakes after Natural Earth; Lambert conformal conic. ' + A.TERRAIN_SRC)
    return A.plate_end(s, H)
