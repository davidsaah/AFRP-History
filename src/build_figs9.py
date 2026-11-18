# -*- coding: utf-8 -*-
"""v104: three charts for the wars chapters (David, 18 Nov 2026: "Fold it in").

Drawn in the v80 phone-first style (400 units wide, nothing under 14 units; see
src/build_figs6.py). The numbers come from:
- the B'Tselem fatalities and demolitions exports of 17 Nov 2026, cleaned
  (Literature: 2026_BTselem_Fatalities_and_Demolitions_cleaned.xlsx). B'Tselem
  is an Israeli rights group, so these are support only, labelled as such on
  the plate; PCBS's 182 for 2000–2009 is the deciding figure and is printed on it.
- the AFRP family tree export of 17 Nov 2026 (27,794 people): everyone with
  both a birth year and a birthplace, by decade.
"""
from build_figs6 import W, AXIS, RULE, TINT, GOLD, T_LAB, T_NOTE, t, para, svg, fmt
from map_style import INK, BODY, NOTE

# Ramallah & al-Bīra district residents killed by Israeli forces or settlers, by year
# (B'Tselem; 2026 to 24 July). Second figure: children under 18.
KILLED = [(2000, 20, 8), (2001, 23, 3), (2002, 59, 12), (2003, 11, 4), (2004, 11, 2), (2005, 8, 5),
          (2006, 8, 1), (2007, 7, 4), (2008, 10, 3), (2009, 5, 3), (2010, 1, 1), (2011, 1, 0),
          (2012, 3, 0), (2013, 5, 2), (2014, 10, 4), (2015, 15, 2), (2016, 13, 4), (2017, 8, 3),
          (2018, 10, 4), (2019, 6, 1), (2020, 5, 2), (2021, 10, 2), (2022, 21, 8), (2023, 36, 9),
          (2024, 25, 8), (2025, 17, 5), (2026, 12, 4)]

# Demolitions "for lack of a permit" in Ramallah & al-Bīra district, by year (B'Tselem; 2026 to 31 Aug):
# (year, demolitions, people left homeless)
DEMOL = [(2006, 6, 0), (2007, 2, 11), (2008, 4, 103), (2009, 1, 9), (2010, 1, 2), (2011, 1, 16),
         (2012, 6, 50), (2013, 15, 63), (2014, 11, 33), (2015, 29, 116), (2016, 32, 58), (2017, 12, 21),
         (2018, 13, 0), (2019, 6, 26), (2020, 32, 33), (2021, 65, 132), (2022, 53, 95), (2023, 19, 14),
         (2024, 32, 29), (2025, 88, 176), (2026, 54, 77)]

# The family tree, people with a birth year and a birthplace: (decade, people, born abroad)
ABROAD = [(1890, 30, 1), (1900, 58, 4), (1910, 47, 12), (1920, 87, 26), (1930, 178, 54),
          (1940, 165, 50), (1950, 148, 76), (1960, 208, 159), (1970, 195, 179), (1980, 147, 125),
          (1990, 178, 169), (2000, 173, 168), (2010, 72, 68)]


def _bars(s, y0, data, vmax, h, mark=None, col=None, ticks=(), lab_every=None, label_top=()):
    """Vertical bars across the plate. data: [(label, value)]."""
    x0, x1 = 34, W - 8
    n = len(data)
    bw = (x1 - x0) / n
    for v in ticks:
        yy = y0 + h - h * v / vmax
        s.append(f'<line x1="{x0}" y1="{yy:.1f}" x2="{x1}" y2="{yy:.1f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(t(x0 - 4, yy + 5, fmt(v), T_NOTE, NOTE, 'end'))
    for i, (lab, v) in enumerate(data):
        bh = h * v / vmax
        x = x0 + i * bw
        c = (col(lab) if col else TINT[0])
        s.append(f'<rect x="{x + 1:.1f}" y="{y0 + h - bh:.1f}" width="{bw - 2:.1f}" height="{bh:.1f}" fill="{c}"/>')
        if lab in label_top:
            s.append(t(x + bw / 2, y0 + h - bh - 5, fmt(v), T_NOTE, INK, 'middle', '700'))
    s.append(f'<line x1="{x0}" y1="{y0 + h}" x2="{x1}" y2="{y0 + h}" stroke="{AXIS}" stroke-width="1.2"/>')
    for i, (lab, v) in enumerate(data):
        if lab_every and lab in lab_every:
            s.append(t(x0 + i * bw + bw / 2, y0 + h + 18, str(lab), T_NOTE, BODY, 'middle'))
    return y0 + h + 18


def fig_killed():
    s = []
    s.append(t(8, 18, 'People of Ramallah and al-Bīra district', T_LAB, INK, 'start', '700'))
    s.append(t(8, 36, 'killed by Israeli forces or settlers, by year', T_LAB, INK, 'start', '700'))
    data = [(y, v) for y, v, _ in KILLED]
    y = _bars(s, 52, data, 60, 170, ticks=(20, 40, 60), lab_every=(2000, 2005, 2010, 2015, 2020, 2025),
              col=lambda yr: GOLD if yr >= 2022 else TINT[0], label_top=(2002, 2023))
    y += 22
    s.append(t(8, y, '360 people in all, 104 of them children.', T_LAB, INK, 'start', '700'))
    txt_, y = para(8, y + 20, 'Highest in 2002, the year of the invasion; rising again since 2022 (ochre). For 2000 to 2009 the Palestinian Central Bureau of Statistics counts 182 dead from the district, 49 of them children: its count decides. The yearly bars are B’Tselem’s, an Israeli rights group, used here as support. 2026 runs to July.', T_NOTE)
    s.append(txt_)
    return svg(y + 4, 'Bar chart of people from Ramallah and al-Bīra district killed by Israeli forces or settlers each year from 2000 to 2026, highest in 2002 and rising again since 2022', ''.join(s))


def fig_demolitions():
    s = []
    s.append(t(8, 18, 'Homes and buildings demolished', T_LAB, INK, 'start', '700'))
    s.append(t(8, 36, '“for lack of a permit”, Ramallah district', T_LAB, INK, 'start', '700'))
    data = [(y, v) for y, v, _ in DEMOL]
    y = _bars(s, 52, data, 90, 160, ticks=(30, 60, 90), lab_every=(2006, 2010, 2015, 2020, 2025),
              label_top=(2021, 2025))
    y += 22
    s.append(t(8, y, '482 demolitions, 191 of them homes.', T_LAB, INK, 'start', '700'))
    s.append(t(8, y + 20, '1,064 people left homeless, 573 children.', T_LAB, INK, 'start', '700'))
    txt_, y = para(8, y + 42, 'Permits in Area C are almost never granted. Hardest hit: Shuqbā (55), al-Qābūn (35), the Bedouin of al-Muʿarrajāt (34, with 190 left homeless) and Niʿlīn (32). Count by B’Tselem, an Israeli rights group, from 2006 to August 2026; no Palestinian count by village and year has been found.', T_NOTE)
    s.append(txt_)
    return svg(y + 4, 'Bar chart of homes and buildings demolished for lack of a permit in Ramallah district each year from 2006 to 2026, highest in 2025 with 88', ''.join(s))


def fig_abroad():
    s = []
    s.append(t(8, 18, 'Share of the family tree born abroad', T_LAB, INK, 'start', '700'))
    s.append(t(8, 36, 'outside Palestine and Jordan,', T_NOTE, BODY, 'start'))
    s.append(t(8, 52, 'by decade of birth', T_NOTE, BODY, 'start'))
    data = [(d, round(100 * a / n)) for d, n, a in ABROAD]
    x0, x1 = 34, W - 8
    h, y0 = 160, 68
    for v in (25, 50, 75, 100):
        yy = y0 + h - h * v / 100
        s.append(f'<line x1="{x0}" y1="{yy:.1f}" x2="{x1}" y2="{yy:.1f}" stroke="{RULE}" stroke-width="1"/>')
        s.append(t(x0 - 4, yy + 5, f'{v}%', T_NOTE, NOTE, 'end'))
    n = len(data)
    bw = (x1 - x0) / n
    for i, (d, v) in enumerate(data):
        bh = h * v / 100
        x = x0 + i * bw
        s.append(f'<rect x="{x + 1.5:.1f}" y="{y0 + h - bh:.1f}" width="{bw - 3:.1f}" height="{bh:.1f}" fill="{TINT[0] if d < 1950 else GOLD}"/>')
    s.append(f'<line x1="{x0}" y1="{y0 + h}" x2="{x1}" y2="{y0 + h}" stroke="{AXIS}" stroke-width="1.2"/>')
    for i, (d, v) in enumerate(data):
        if d in (1890, 1920, 1950, 1980, 2010):
            s.append(t(x0 + i * bw + bw / 2, y0 + h + 18, f'{d}s', T_NOTE, BODY, 'middle'))
    # the wars, as marks above the bars they shaped
    y = y0 + h + 44
    for lab in ['Before 1914: about 1 in 20 born abroad.', '1910s–1940s, the world wars, the revolt', 'and the Nakba: about 1 in 3.', 'After 1948 and 1967 (ochre): half, then', 'three in four, then nine in ten.']:
        s.append(t(8, y, lab, T_NOTE, INK, 'start'))
        y += 18
    txt_, y = para(8, y + 6, 'The 1,689 people in the tree with both a birth year and a birthplace. The tree records the families abroad far better than those who stayed, so the bars show when families left, not how many Ramallah people live abroad.', T_NOTE)
    s.append(txt_)
    return svg(y + 4, 'Bar chart of the share of the Ramallah family tree born abroad by decade, from about 1 in 20 before 1914 to about nine in ten after 1970', ''.join(s))
