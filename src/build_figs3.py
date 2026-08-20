# -*- coding: utf-8 -*-
"""Third figure library: the dam act, the scattering, the clan tree, the town
plan, the two-populations chart, the wages ladder, the war strip."""
import math
import build_recon as R

txt = R.txt
GREEN, RUST, PLUM = '#007A3D', '#A85210', '#6D4E9E'
GOLD, GREY, RULE, FOLIO = '#B98A4E', '#77726A', '#DCD6C9', '#9A958C'
INK, BODY, DARK = '#1A1A1A', '#46423B', '#004A26'
SURF, SEA, LAND, TAN = '#FCFBF8', '#E7EFF2', '#F3EFE4', '#D4B483'


def _head(s, W, H, kicker, sub, aria):
    s.append(f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{aria}">')
    s.append(f'<rect width="{W}" height="{H}" fill="{SURF}"/>')
    s.append(txt(40, 32, kicker, 11, GOLD, 'start', '700', 'normal', '1.4'))
    s.append(txt(40, 50, sub, 10.5, GREY, 'start', '400', 'italic'))


# ═════════════════════ the dam, as a machine
def fig_dam_eng():
    W, H = 860, 560
    s = []
    _head(s, W, H, 'THE MACHINE THAT WATERED A KINGDOM',
          'The great dam of Maʾrib: an earthen wall across the Wādī Dhana that turned flash-floods into two gardens — for more than a thousand years.',
          'Schematic of the Marib dam, its sluices and its two irrigated gardens')
    # the wadi, flowing left to right through a gap in the mountains
    s.append(f'<path d="M40 240 C 180 225, 240 250, 320 246 L 320 306 C 240 310, 180 330, 40 316 Z" fill="{SEA}" opacity=".8"/>')
    s.append(txt(52, 282, 'WĀDĪ DHANA', 9.6, '#7C99A6', 'start', '700', 'normal', '1.2'))
    s.append(txt(52, 296, 'flash-floods off the highlands,', 8.8, '#7C99A6'))
    s.append(txt(52, 308, 'twice a year', 8.8, '#7C99A6'))
    # mountains north and south of the gap
    s.append(f'<path d="M300 108 L 352 218 L 248 218 Z" fill="{TAN}" opacity=".65"/>')
    s.append(f'<path d="M300 444 L 352 330 L 248 330 Z" fill="{TAN}" opacity=".65"/>')
    s.append(txt(300, 100, 'Jabal Balaq al-Awsaṭ', 8.8, '#8A6A3A', 'middle', '700'))
    s.append(txt(300, 462, 'Jabal Balaq al-Yamanī', 8.8, '#8A6A3A', 'middle', '700'))
    # the dam wall between the peaks
    s.append(f'<rect x="316" y="218" width="18" height="112" rx="4" fill="{RUST}"/>')
    s.append(txt(346, 250, 'THE DAM', 10.5, RUST, 'start', '700', 'normal', '1.1'))
    s.append(txt(346, 265, 'an earthen wall, faced with stone —', 9, BODY))
    s.append(txt(346, 277, 'about 580 metres end to end, raised', 9, BODY))
    s.append(txt(346, 289, 'over the centuries from ~4 to ~14 m', 9, BODY))
    # sluice towers
    for y, lab in [(206, 'the northern sluice'), (336, 'the southern sluice')]:
        s.append(f'<rect x="312" y="{y}" width="26" height="14" fill="{DARK}"/>')
        s.append(txt(288, y + 10, lab, 8.6, DARK, 'end', '700'))
    # canals to the gardens
    s.append(f'<path d="M338 213 C 430 190, 520 176, 640 168" fill="none" stroke="{SEA}" stroke-width="7"/>')
    s.append(f'<path d="M338 343 C 430 366, 520 380, 640 388" fill="none" stroke="{SEA}" stroke-width="7"/>')
    # the two gardens
    for cy, lab in [(168, 'THE NORTHERN GARDEN'), (388, 'THE SOUTHERN GARDEN')]:
        s.append(f'<ellipse cx="700" cy="{cy}" rx="112" ry="52" fill="{GREEN}" opacity=".18"/>')
        s.append(f'<ellipse cx="700" cy="{cy}" rx="112" ry="52" fill="none" stroke="{GREEN}" stroke-width="1.4"/>')
        for i in range(14):
            gx = 700 - 90 + (i % 7) * 30
            gy = cy - 18 + (i // 7) * 34
            s.append(f'<circle cx="{gx}" cy="{gy}" r="3.2" fill="{GREEN}" opacity=".7"/>')
        s.append(txt(700, cy + 4, lab, 9.6, DARK, 'middle', '700', 'normal', '1.1'))
    s.append(txt(700, 262, '<tspan font-style="italic">“two gardens, on the right hand</tspan>', 10, DARK, 'middle'))
    s.append(txt(700, 276, '<tspan font-style="italic">and on the left” — Qurʾān 34:15</tspan>', 10, DARK, 'middle'))
    s.append(txt(700, 296, 'together some 9,600 hectares —', 9, BODY, 'middle'))
    s.append(txt(700, 308, 'about 24,000 acres under water control', 9, BODY, 'middle'))
    # timeline strip
    y0 = 496
    s.append(f'<line x1="40" y1="{y0-14}" x2="820" y2="{y0-14}" stroke="{RULE}"/>')
    for x, head, lines in [
        (40, '8TH–7TH c. BCE', ['Sabaean earthworks; the', 'mukarribs’ inscriptions']),
        (240, '6TH c. BCE', ['the great masonry', 'sluice towers built']),
        (420, '~1,300 YEARS', ['of continuous operation —', 'the longest-serving machine', 'in the ancient world']),
        (640, '455 → c. 575 CE', ['the dated breaches begin;', 'final collapse near 575–580']),
    ]:
        s.append(txt(x, y0 + 4, head, 9.4, GOLD, 'start', '700', 'normal', '1.2'))
        for j, ln in enumerate(lines):
            s.append(txt(x, y0 + 19 + j * 12, ln, 8.9, BODY))
    s.append('</svg>')
    return ''.join(s)


# ═════════════════════ the scattering of the Azd
def fig_scattering():
    W, H = 860, 700
    # Arabia, simple equirect
    lat0, lat1 = 12.0, 34.0
    lon0 = 34.0
    y0, y1 = 92, 560
    sy = (y1 - y0) / (lat1 - lat0)
    sx = sy * math.cos(math.radians(23.0))
    xc = 118.0
    px = lambda lon: xc + (lon - lon0) * sx
    py = lambda lat: y0 + (lat1 - lat) * sy

    s = []
    _head(s, W, H, '“THEY SCATTERED LIKE THE PEOPLE OF SABAʾ”',
          'The dispersal of the Azd — the most famous migration in Arab tradition. Every arrow became a people. One of them became this family.',
          'Map of the scattering of the Azd tribes from Marib after the dam failures')
    # coast outline of Arabia (very simplified)
    land = [(30.2,47.6),(29.0,48.0),(27.5,49.5),(26.0,51.5),(24.4,54.5),(24.0,58.0),
            (22.5,59.6),(20.5,58.5),(18.5,56.5),(17.0,55.0),(14.5,52.0),(13.0,48.5),
            (12.6,45.0),(13.5,43.2),(16.5,42.6),(19.0,41.0),(21.5,39.0),(25.0,37.0),
            (28.0,34.6),(29.5,34.9),(31.0,35.3),(33.0,36.2),(34.0,38.5),(34.0,44.0),
            (32.0,46.5)]
    s.append('<path d="M' + ' L'.join(f'{px(lo):.0f} {py(la):.0f}' for la, lo in land) +
             f' Z" fill="{LAND}" opacity=".55" stroke="#C9BFA8" stroke-width="1.2"/>')
    s.append(txt(px(48.5), py(20.5), 'A R A B I A', 13, '#C4B8A0', 'middle', '700', 'normal', '5'))
    s.append(txt(px(50.5), py(13.0), 'the Indian Ocean', 8.6, '#9BB0BA', 'start', '400', 'italic'))
    s.append(txt(px(39.4), py(16.6), 'the', 8.4, '#B6C4CB', 'middle', '400', 'italic'))
    s.append(txt(px(39.4), py(15.9), 'Red Sea', 8.4, '#B6C4CB', 'middle', '400', 'italic'))

    MA = (15.43, 45.33)
    mx, my = px(MA[1]), py(MA[0])
    # the routes
    ROUTES = [
        # (dest lat, lon, label, sub, colour, weight, curve)
        (19.5, 41.8, 'AZD AL-SARĀT', 'stay nearest — the Sarāt mountains', FOLIO, 2.2, -30),
        (21.4, 39.85, 'KHUZĀʿA', 'to Mecca — later its keepers', '#4A7C8C', 2.2, -50),
        (24.47, 39.61, 'AWS & KHAZRAJ', 'to Yathrib — the Anṣār who received the Prophet', PLUM, 2.6, -66),
        (23.1, 57.5, 'AZD ʿUMĀN', 'east to Oman — sailors and traders', '#9A8CC0', 2.2, 40),
        (32.0, 36.1, 'GHASSĀN', 'north, water by water, to the Roman frontier', GOLD, 4.2, -86),
    ]
    s.append('<defs><marker id="sc" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.6" '
             'markerHeight="5.6" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="context-stroke"/></marker></defs>')
    for la, lo, lab, sub, col, wgt, bend in ROUTES:
        x2, y2 = px(lo), py(la)
        cx1 = (mx + x2) / 2 + bend
        cy1 = (my + y2) / 2 + (20 if bend > 0 else -20)
        s.append(f'<path d="M{mx:.0f} {my:.0f} Q {cx1:.0f} {cy1:.0f} {x2:.0f} {y2:.0f}" fill="none" '
                 f'stroke="{col}" stroke-width="{wgt}" marker-end="url(#sc)" opacity=".9"/>')
        s.append(f'<circle cx="{x2:.0f}" cy="{y2:.0f}" r="4.6" fill="{col}"/>')
    # labels placed manually to avoid collisions
    s.append(txt(px(40.9), py(17.6), 'AZD AL-SARĀT', 9.6, FOLIO, 'end', '700'))
    s.append(txt(px(40.9), py(16.9), 'stay nearest — the Sarāt mountains', 8.4, BODY, 'end', '400', 'italic'))
    s.append(txt(px(38.6), py(21.9), 'KHUZĀʿA', 9.6, '#4A7C8C', 'end', '700'))
    s.append(txt(px(38.6), py(21.2), 'to Mecca — later its keepers', 8.4, BODY, 'end', '400', 'italic'))
    s.append(txt(px(38.3), py(25.6), 'AWS &amp; KHAZRAJ', 9.6, PLUM, 'end', '700'))
    s.append(txt(px(38.3), py(24.9), 'to Yathrib — the Anṣār who', 8.4, BODY, 'end', '400', 'italic'))
    s.append(txt(px(38.3), py(24.3), 'received the Prophet at Medina', 8.4, BODY, 'end', '400', 'italic'))
    s.append(txt(px(56.6), py(24.3), 'AZD ʿUMĀN', 9.8, '#9A8CC0', 'start', '700'))
    s.append(txt(px(56.6), py(23.6), 'east to Oman — sailors, traders', 8.6, BODY, 'start', '400', 'italic'))
    s.append(txt(px(37.0), py(33.2), 'GHASSĀN', 12, GOLD, 'start', '700', 'normal', '.8'))
    s.append(txt(px(37.0), py(32.5), 'north, water by water, to the Roman frontier —', 8.6, BODY, 'start', '400', 'italic'))
    s.append(txt(px(37.0), py(31.9), 'the Balqāʾ, the Golan, and a phylarchate', 8.6, BODY, 'start', '400', 'italic'))
    # Marib
    s.append(f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="8" fill="{RUST}"/>')
    s.append(f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="14" fill="none" stroke="{RUST}" stroke-width="1.4" stroke-dasharray="3 3"/>')
    s.append(txt(mx + 20, my + 4, 'MAʾRIB — the dam', 10.5, RUST, 'start', '700'))
    s.append(txt(mx + 20, my + 17, 'Sabaʾ; the two gardens', 8.8, BODY, 'start', '400', 'italic'))
    # footer
    s.append(f'<line x1="40" y1="{H-104}" x2="820" y2="{H-104}" stroke="{RULE}"/>')
    s.append(txt(40, H - 84, 'The proverb is still spoken: <tspan font-style="italic">tafarraqū aydī Sabaʾ</tspan> — “they scattered like the people of Sabaʾ.”', 10.6, INK, 'start', '700'))
    s.append(txt(40, H - 64, 'The classical genealogists trace the whole dispersal of the Azd to the failing of the dam. Each stream became a famous people: the helpers of the Prophet at Medina,', 10, BODY))
    s.append(txt(40, H - 50, 'the keepers of Mecca, the seafarers of Oman — and the kings of the north, whose road this family claims as its own. <tspan font-weight="700">One catastrophe, five destinies.</tspan>', 10, BODY))
    s.append(txt(40, H - 26, 'Ibn al-Kalbī and the Azdī pedigree tradition; al-Masʿūdī on the dispersal; Qurʾān 34:15–19 on the flood and the scattering. Ulrich (2019) cautions that the “Scattering of Azd” is itself a literary construction of the 8th–10th centuries.', 8.4, FOLIO, 'start', '400', 'italic'))
    s.append('</svg>')
    return ''.join(s)


# ═════════════════════ the clan tree
def fig_clans_tree():
    W, H = 860, 640
    s = []
    _head(s, W, H, 'ONE MAN, FIVE SONS, EIGHT CLANS — AND A TOWN',
          'The whole social structure of Ramallah descends from this diagram, and the 1944 ration-card census could still count the town by it.',
          'Family tree from Rashid through the five sons to the eight clans with their 1944 populations')
    # Rāshid
    s.append(f'<rect x="355" y="76" width="150" height="44" rx="4" fill="{DARK}"/>')
    s.append(txt(430, 95, 'RĀSHID', 12, '#F3ECDD', 'middle', '700', 'normal', '1'))
    s.append(txt(430, 110, 'al-Ḥaddādīn · generation 66', 8.4, '#9BC3A8', 'middle'))
    # five sons
    sons = [('HADDAD', 120, True), ('IBRAHIM', 290, False), ('JIRIUS', 430, False),
            ('SHUKAIR', 570, False), ('HASSAAN', 720, False)]
    sy_ = 190
    for name, x, isH in sons:
        s.append(f'<path d="M430 120 C 430 150, {x} 150, {x} {sy_}" fill="none" stroke="{GOLD}" stroke-width="2"/>')
        s.append(f'<rect x="{x-58}" y="{sy_}" width="116" height="36" rx="4" fill="{GOLD if isH else "#FFFFFF"}" '
                 f'stroke="{GOLD}" stroke-width="1.6"/>')
        s.append(txt(x, sy_ + 22, name, 10.5, '#FFFFFF' if isH else INK, 'middle', '700'))
    s.append(txt(120, 246, 'the eldest — his fifth is divided again', 8.6, BODY, 'middle', '400', 'italic'))
    s.append(txt(430, 246, 'unsatisfied with his fifth, he receives', 8.6, BODY, 'middle', '400', 'italic'))
    s.append(txt(430, 257, 'the extra parcel called Karm ʿAli', 8.6, BODY, 'middle', '400', 'italic'))
    # eight clans
    cy_ = 330
    clans = [
        ('SHARAKA', 650, 96, True, '“the easterners”'),
        ('JAGHAB', 675, 218, True, '“Drink, or I’ll break your horn!”'),
        ('YOUSEF', 750, 340, True, ''),
        ('ʿAWWAAD (+ʿAZZOUZ)', 625, 462, True, 'joined after the 1820 feud'),
        ('IBRAHIM', 775, 584, False, ''),
        ('JIRIUS', 550, 672, False, ''),
        ('SHAKARA', 660, 760, False, 'Shukair’s line — declared Yemen'),
        ('HASSAAN', 200, 760, False, ''),
    ]
    # branch lines: Haddad's four from Haddad box; other four from their fathers
    from_map = {0: 120, 1: 120, 2: 120, 3: 120, 4: 290, 5: 430, 6: 570, 7: 720}
    xs = [86, 190, 294, 398, 502, 606, 710, 796]
    for i, (name, n44, _, isH, ety) in enumerate(clans):
        fx = from_map[i]
        tx = xs[i]
        s.append(f'<path d="M{fx} {226 if i<4 else 226} C {fx} {286}, {tx} {286}, {tx} {cy_}" '
                 f'fill="none" stroke="{GOLD if isH else FOLIO}" stroke-width="1.6"/>')
        bw = 96
        s.append(f'<rect x="{tx-bw//2}" y="{cy_}" width="{bw}" height="64" rx="4" '
                 f'fill="{"#FDF9F0" if isH else "#FFFFFF"}" stroke="{GOLD if isH else FOLIO}" stroke-width="1.5"/>')
        nm = name if len(name) < 12 else name.split(' ')[0]
        s.append(txt(tx, cy_ + 20, nm, 9.2, INK, 'middle', '700'))
        if '+' in name:
            s.append(txt(tx, cy_ + 32, '+ ʿAZZOUZ', 8, INK, 'middle', '700'))
        s.append(txt(tx, cy_ + 48, f'{n44:,}', 11, GREEN, 'middle', '700'))
        s.append(txt(tx, cy_ + 59, 'in 1944', 7.4, FOLIO, 'middle'))
    # brackets
    s.append(f'<path d="M40 {cy_+84} L40 {cy_+92} L446 {cy_+92} L446 {cy_+84}" fill="none" stroke="{GOLD}" stroke-width="1.6"/>')
    s.append(txt(243, cy_ + 112, 'THE HADADEH — the four clans of Haddad’s sons', 9.6, GOLD, 'middle', '700', 'normal', '1'))
    s.append(f'<path d="M456 {cy_+84} L456 {cy_+92} L844 {cy_+92} L844 {cy_+84}" fill="none" stroke="{FOLIO}" stroke-width="1.6"/>')
    s.append(txt(650, cy_ + 112, 'THE HAMAYEL — the four clans of Haddad’s brothers', 9.6, GREY, 'middle', '700', 'normal', '1'))
    # etymologies
    ey = cy_ + 140
    s.append(f'<line x1="40" y1="{ey-8}" x2="820" y2="{ey-8}" stroke="{RULE}"/>')
    s.append(txt(40, ey + 10, 'The names keep the sixteenth century alive: the Sharaka lived in the town’s east (<tspan font-style="italic">sharq</tspan>); the Jaghab are their ancestor’s shout at a stubborn ox at the trough;', 9.6, BODY))
    s.append(txt(40, ey + 24, 'the Shakara declared themselves Yemen to protect land near Yemeni Beitunia. Total counted in 1944: <tspan font-weight="700">4,885 natives</tspan> — every one on this diagram.', 9.6, BODY))
    s.append(txt(40, ey + 44, 'Shāhīn (1982), ch. 1, with the 1944 ration-card census; the division of the land in fifths, and Karm ʿAli.', 8.6, FOLIO, 'start', '400', 'italic'))
    s.append('</svg>')
    return ''.join(s)


# ═════════════════════ the old-town plan
def fig_town_plan():
    W, H = 860, 620
    s = []
    _head(s, W, H, 'THE TOWN, AS SHĀHĪN DREW IT',
          'The principal streets of central Ramallah, after the sketch in his own book — the old village core, the two roads to Jerusalem, and the institutions the century built.',
          'Plan of central Ramallah after Shahin 1982')
    cxm, cym = 470, 300
    RD = '#B9B0A0'
    def road(d, w=5):
        s.append(f'<path d="{d}" fill="none" stroke="{RD}" stroke-width="{w}" stroke-linecap="round"/>')
        s.append(f'<path d="{d}" fill="none" stroke="{SURF}" stroke-width="1" stroke-dasharray="1 7"/>')
    # main street west-east to Bireh
    road('M120 300 L 780 268', 7)
    # el-tira road NW
    road('M120 300 C 220 268, 300 232, 392 210')
    # 'Ain Misbah St (north loop)
    road('M392 210 C 470 180, 580 176, 650 210')
    # Radio St NE
    road('M650 210 C 700 188, 740 160, 790 140')
    # to Birzeit (N)
    road('M650 210 L 668 120')
    # Bain el-Hawa S from west end
    road('M200 296 C 210 380, 220 440, 232 500')
    # Jaffa Road SW
    road('M320 292 C 300 360, 260 430, 200 480')
    # Masyoun S
    road('M420 288 C 420 380, 400 470, 380 540')
    # original Jerusalem road (SE, pre-1901)
    road('M560 276 C 590 360, 640 440, 700 520')
    s.append(txt(716, 500, 'the ORIGINAL', 8.6, '#8A6A3A', 'start', '700'))
    s.append(txt(716, 512, 'Ramallah–Jerusalem road', 8.6, '#8A6A3A', 'start'))
    s.append(txt(716, 524, '— the only way south until 1901', 8.2, BODY, 'start', '400', 'italic'))
    # present Jerusalem road via Bireh (E then S)
    road('M780 268 C 800 330, 800 400, 786 470', 6)
    s.append(txt(770, 452, 'the PRESENT', 8.6, '#8A6A3A', 'end', '700'))
    s.append(txt(770, 464, 'Jerusalem road, built 1901', 8.6, '#8A6A3A', 'end'))
    s.append(txt(770, 476, 'running through El Bireh', 8.2, BODY, 'end', '400', 'italic'))
    # old core
    s.append(f'<ellipse cx="358" cy="286" rx="96" ry="62" fill="none" stroke="{GOLD}" stroke-width="2" stroke-dasharray="6 5"/>')
    s.append(txt(358, 214, 'THE ORIGINAL VILLAGE', 9, GOLD, 'middle', '700', 'normal', '1'))
    s.append(txt(358, 226, 'the eight clans’ quarters, the guest houses', 8, BODY, 'middle', '400', 'italic'))
    # labels for roads
    s.append(txt(150, 288, 'El Tira Rd', 8.4, GREY, 'start', '400', 'italic'))
    s.append(txt(505, 170, '‘Ain Misbah St', 8.4, GREY, 'middle', '400', 'italic'))
    s.append(txt(766, 128, 'Radio St', 8.4, GREY, 'start', '400', 'italic'))
    s.append(txt(676, 118, 'to Birzeit', 8.4, GREY, 'start', '400', 'italic'))
    s.append(txt(226, 512, 'Bain El-Hawa', 8.4, GREY, 'middle', '400', 'italic'))
    s.append(txt(196, 494, 'Jaffa Rd', 8.4, GREY, 'end', '400', 'italic'))
    s.append(txt(378, 552, 'Masyoun', 8.4, GREY, 'middle', '400', 'italic'))
    s.append(txt(600, 300, 'Main St', 8.6, GREY, 'middle', '400', 'italic'))
    s.append(txt(640, 460, 'El Sharafa — where the town', 8.2, BODY, 'end', '400', 'italic'))
    s.append(txt(640, 472, 'wept its emigrants goodbye', 8.2, BODY, 'end', '400', 'italic'))
    # numbered sites
    SITES = [
        (780, 268, '1', 'Manara Square', 'end', -12, -8),
        (620, 232, '2', 'Friends Meetinghouse (1910)', 'start', 10, -4),
        (520, 246, '3', 'Roman Catholic church &amp; school', 'end', -12, -6),
        (388, 302, '4', 'Greek Orthodox church (1850)', 'end', -12, 26),
        (452, 330, '5', 'Municipality &amp; park', 'start', 10, 12),
        (492, 388, '6', 'Lutheran church &amp; school', 'start', 10, 4),
        (612, 420, '7', 'Ramallah New Hospital (1963)', 'start', 10, 4),
        (288, 346, '8', 'Friends Girls School (1869→)', 'end', -12, 12),
        (700, 190, '9', 'Friends Boys School (1919)', 'start', 10, -4),
    ]
    for x, y, n, lab, anc, dx, dy in SITES:
        s.append(f'<circle cx="{x}" cy="{y}" r="9" fill="{DARK}"/>')
        s.append(txt(x, y + 3.4, n, 9, '#F3ECDD', 'middle', '700'))
        s.append(txt(x + dx, y + dy, lab, 8.8, INK, anc, '700'))
    s.append(txt(40, H - 36, 'After the sketch map in Shāhīn (1982), p. 69, simplified; site dates from his own chapters.', 8.6, FOLIO, 'start', '400', 'italic'))
    s.append(txt(40, H - 22, 'Before 1901 the road to Jerusalem left from El Sharafa on the south-east edge — the Russian pilgrims’ bells and the emigrants’ farewells both belong to that road.', 8.6, FOLIO, 'start', '400', 'italic'))
    s.append('</svg>')
    return ''.join(s)


# ═════════════════════ two populations
def fig_two_pop():
    W, H = 860, 540
    x0, x1, yb, yt = 90, 800, 400, 90
    t0, t1 = 1898, 1982
    v1 = 16000
    px = lambda t: x0 + (x1 - x0) * (t - t0) / (t1 - t0)
    py = lambda v: yb - (yb - yt) * v / v1
    s = []
    _head(s, W, H, 'TWO POPULATIONS, ONE TOWN',
          'Ramallah natives at home against Ramallah natives in the United States. The moment the curves cross is the moment the town becomes two places.',
          'Chart of Ramallah native population at home versus in the United States, 1900 to 1980')
    for v in (2000, 4000, 6000, 8000, 10000, 12000, 14000):
        s.append(f'<line x1="{x0}" y1="{py(v):.0f}" x2="{x1}" y2="{py(v):.0f}" stroke="{RULE}" stroke-width=".8"/>')
        s.append(txt(x0 - 10, py(v) + 4, f'{v:,}', 9.5, FOLIO, 'end'))
    for yr in range(1900, 1981, 10):
        s.append(txt(px(yr), yb + 20, str(yr), 9.5, FOLIO, 'middle'))
    HOME = [(1905, 3214), (1922, 3104), (1931, 4286), (1944, 4885), (1953, 4500),
            (1961, 4200), (1975, 2000), (1980, 1800)]
    AWAY = [(1901, 4), (1914, 300), (1931, 800), (1946, 1500), (1953, 2580),
            (1960, 4000), (1975, 10000), (1980, 12000)]
    s.append('<polyline points="' + ' '.join(f'{px(t):.0f},{py(v):.0f}' for t, v in HOME) +
             f'" fill="none" stroke="{GREEN}" stroke-width="2.6" stroke-linejoin="round"/>')
    s.append('<polyline points="' + ' '.join(f'{px(t):.0f},{py(v):.0f}' for t, v in AWAY) +
             f'" fill="none" stroke="{GOLD}" stroke-width="2.6" stroke-dasharray="7 4" stroke-linejoin="round"/>')
    for t, v in HOME:
        s.append(f'<circle cx="{px(t):.0f}" cy="{py(v):.0f}" r="4" fill="{GREEN}" stroke="#fff" stroke-width="1.4"/>')
    for t, v in AWAY:
        s.append(f'<circle cx="{px(t):.0f}" cy="{py(v):.0f}" r="4" fill="{GOLD}" stroke="#fff" stroke-width="1.4"/>')
    # crossing
    s.append(f'<circle cx="{px(1957):.0f}" cy="{py(4300):.0f}" r="13" fill="none" stroke="{RUST}" stroke-width="1.8" stroke-dasharray="3 3"/>')
    s.append(txt(px(1957) + 20, py(4300) + 34, 'the mid-1950s: the curves cross', 9.6, RUST, 'start', '700'))
    s.append(txt(px(1957) + 20, py(4300) + 46, 'and never cross back', 9, RUST, 'start', '400', 'italic'))
    s.append(txt(px(1931), py(4286) - 18, 'AT HOME — natives of the eight clans', 9.8, GREEN, 'middle', '700'))
    s.append(txt(px(1966), py(7600), 'IN THE UNITED STATES', 9.8, '#8A6A3A', 'start', '700'))
    s.append(txt(px(1975), py(2000) + 20, 'fewer than 2,000 remain', 9, BODY, 'middle', '400', 'italic'))
    s.append(txt(px(1975), py(10000) - 14, '10,000+', 10, INK, 'middle', '700'))
    s.append(f'<line x1="40" y1="{H-64}" x2="820" y2="{H-64}" stroke="{RULE}"/>')
    s.append(txt(40, H - 44, '“Over 85% of Ramallah people are now in the States.” — Shāhīn, writing in 1982.', 10.6, INK, 'start', '700'))
    s.append(txt(40, H - 26, 'Home series: the censuses of 1905–1953, natives only — the 9,000 refugees of 1948 are counted in the town chart, not here. Diaspora series: Shāhīn’s own counts —', 8.4, FOLIO, 'start', '400', 'italic'))
    s.append(txt(40, H - 14, '1,500 by 1946, 2,580 in 1953, 4,000+ by 1960, 10,000+ by 1975. Both series are his; the shape, not the precision, is the finding.', 8.4, FOLIO, 'start', '400', 'italic'))
    s.append('</svg>')
    return ''.join(s)


# ═════════════════════ the wages ladder
def fig_wages_ladder():
    W, H = 860, 470
    rows = [
        ('A boy in the fields', 4, ''),
        ('A labourer', 6, 'the carriage to Jerusalem also cost 6'),
        ('A doctor’s visit', 8, 'from 6 to 10'),
        ('A craftsman', 17.5, 'from 15 to 20'),
        ('Hiring a man and mule to plow', 20, ''),
        ('A MASON', 23, 'one silver majeedy — the top of the ladder'),
        ('Hiring a man and oxen', 25, ''),
    ]
    x0, x1 = 300, 800
    vmax = 27.0
    s = []
    _head(s, W, H, 'THE LADDER OF A DAY’S WORK, ABOUT 1900–1903',
          'In piasters per day, when a piaster was worth five US cents. Building stone paid better than anything — which is why Ramallah men became masons, and why masons could afford to sail.',
          'Bar chart of daily wages in Ramallah around 1900 in piasters')
    y = 96
    for lab, v, note in rows:
        w = (x1 - x0) * v / vmax
        big = lab == 'A MASON'
        s.append(f'<rect x="{x0}" y="{y-13}" width="{w:.0f}" height="24" rx="2" '
                 f'fill="{GOLD if big else GREEN}" opacity="{1 if big else .82}"/>')
        s.append(txt(x0 - 12, y + 4, lab, 10.6 if big else 10, INK, 'end', '700' if big else '400'))
        s.append(txt(x0 + w + 10, y + 4, f'{v:g}', 10.6, INK, 'start', '700'))
        if note:
            s.append(txt(x0 + w + 34, y + 4, note, 8.8, BODY, 'start', '400', 'italic'))
        y += 44
    # majeedy reference line
    mx = x0 + (x1 - x0) * 23 / vmax
    s.append(f'<line x1="{mx:.0f}" y1="82" x2="{mx:.0f}" y2="{y-24}" stroke="{RUST}" stroke-width="1.2" stroke-dasharray="4 4"/>')
    s.append(txt(mx, 76, 'one silver majeedy = 23 piasters', 8.8, RUST, 'middle', '700'))
    s.append(f'<line x1="40" y1="{H-56}" x2="820" y2="{H-56}" stroke="{RULE}"/>')
    s.append(txt(40, H - 36, 'The Christian head-tax that bought exemption from the army: one to two majeedy a year — a mason’s day or two. After the exemption ended (c. 1905–10), buying out of', 9.8, BODY))
    s.append(txt(40, H - 22, 'service cost 50 French gold francs — about 236 days of labouring. <tspan font-weight="700">America, before 1914, required only healthy eyes.</tspan> That is the whole economics of the emigration.', 9.8, BODY))
    s.append('</svg>')
    return ''.join(s)


# ═════════════════════ the war strip
def fig_war_strip():
    W, H = 860, 400
    s = []
    _head(s, W, H, 'THE DARK HALF-DECADE, 1914–1918',
          'Four blows in five years — and the one in the middle is the largest demographic event in the town’s recorded history.',
          'Four panel strip of the war years: conscription, locusts, typhus, occupation')
    panels = [
        ('1914', 'CONSCRIPTION', ['About 30 Ramallah men die', 'in the Turkish army.', '', 'The exemption the head-tax', 'once bought is gone.'], FOLIO),
        ('1915', 'THE LOCUSTS', ['“No crops escape;', 'the economy suffers', 'greatly.”', '', 'The qasr summers end', 'in a stripped land.'], '#8A6A3A'),
        ('1916', 'TYPHUS', ['About 30% of the town', 'perishes — roughly 950', 'of 3,200 souls.', '', 'Among the dead: Hakeem', 'Abu Iskandar, the district’s', 'only doctor.'], RUST),
        ('1917', 'OCCUPATION', ['27 December: the British', 'Army takes Ramallah,', 'eighteen days after', 'Jerusalem falls.', '', 'Four centuries of Ottoman', 'rule end in an afternoon.'], '#4A7C8C'),
    ]
    pw = 186
    for i, (yr, t, lines, col) in enumerate(panels):
        x = 40 + i * (pw + 12)
        s.append(f'<rect x="{x}" y="80" width="{pw}" height="248" rx="6" fill="#FFFFFF" stroke="{RULE}"/>')
        s.append(f'<rect x="{x}" y="80" width="{pw}" height="6" rx="3" fill="{col}"/>')
        s.append(txt(x + 16, 116, yr, 17, col, 'start', '700'))
        s.append(txt(x + 16, 136, t, 9.6, col, 'start', '700', 'normal', '1.6'))
        yy = 162
        for ln in lines:
            if ln:
                s.append(txt(x + 16, yy, ln, 9.4, BODY))
            yy += 15
    # the 1916 panel gets a small human-figure ratio
    x = 40 + 2 * (pw + 12)
    for i in range(10):
        fx = x + 22 + i * 15
        dead = i < 3
        s.append(f'<circle cx="{fx}" cy="300" r="4.6" fill="{RUST if dead else RULE}"/>')
    s.append(txt(x + 16, 320, 'three of every ten', 8.4, RUST, 'start', '700'))
    s.append(f'<line x1="40" y1="{H-52}" x2="820" y2="{H-52}" stroke="{RULE}"/>')
    s.append(txt(40, H - 32, 'No census sits on either side of 1916 — Schick counted 2,061 in 1896, Barron 3,104 in 1922 — so the catastrophe is invisible in every table. It survives only because', 9.8, BODY))
    s.append(txt(40, H - 18, 'Shāhīn wrote it down, and his own doctor died in it. <tspan font-weight="700">This is why oral tradition is graded, kept, and never discarded in this book.</tspan>', 9.8, BODY))
    s.append('</svg>')
    return ''.join(s)


# ═════════════════════ THE CHAIN, REBUILT ON JOHN MOGANNAM'S CHART
# Nine links, each one a block of the thirty-six named generations, carrying its
# own span in years, what holds it up, and what would break it.
CHAIN9 = [
 ('LINK ONE', 'Genesis 5, 11', 'Adam to ʿĀbir (Eber)',
  'fourteen names in the Masoretic text, fifteen in the Septuagint · before any date a document could carry',
  'Genesis 5 and 11. The Septuagint adds Kainan; Luke 3:36 follows it.',
  'scripture',
  'Nothing a document could reach — and that is the point. This link asserts membership in the human story, not a chain of verified fathers, and the book defends it as that.'),
 ('LINK TWO', 'Genesis 10:25', 'ʿĀbir’s two sons — the branch',
  'one generation · Peleg’s line runs to Abraham and Moses; Joktan’s runs to us',
  'Genesis 10:25–29; the thirteen sons of Joktan, of whom two can be placed on a map.',
  'scripture',
  'Nothing. This is the one point in the deep line where the text is explicit, and it is explicit that the two branches part here — six generations before Abraham.'),
 ('LINK THREE', 'al-Ṭabarī, c. 915', 'Joktan is Qaḥṭān — the join',
  'one identification · made by the Arab genealogists, a thousand years ago',
  'the Arabic ansāb tradition, stated by al-Ṭabarī. A tradition, not a sound-law.',
  'join',
  'It is already known to be weak as philology: Yoqṭān → Qaḥṭān is not a regular correspondence. It is defended as a tradition every Qaḥṭānī Arab alive stands on, and as nothing more.'),
 ('LINK FOUR', 'Ibn al-Kalbī, Ibn Ḥazm', 'Qaḥṭān to al-Azd',
  'ten generations · the South Arabian kingdoms · the dam is built 8th–7th c. BC',
  'al-Hamdānī for the country; Sabaic inscriptions for the place, not the persons.',
  'classical',
  'An inscription naming any one of these men. None exists. Sabaʾ is epigraphically rich and genealogically silent — the place is proven, the persons are tradition.'),
 ('LINK FIVE', 'Ibn Durayd', 'al-Azd to Ghassān — named at a water',
  'six generations · c. 250–500 AD · the name enters the line',
  '“Ghassān is a water they drank from; it is neither a father nor a mother.”',
  'classical',
  'Proof that Ghassān is a personal name after all. Three classical authorities call it a spring, and they disagree with one another about everything else.'),
 ('LINK SIX', 'Procopius', 'The Jafnid phylarchs — Jabala, al-Ḥārith',
  'two generations · 528–569 AD · 41 years, dated to the year',
  'a Greek historian writing in al-Ḥārith’s lifetime; the Nitl mosaics; CIH 541.',
  'attested',
  'The hardest link in the chain. Breaking it would take a demonstration that the Arethas of the Greek sources is a different man.'),
 ('LINK SEVEN', 'no source', 'THE VOID',
  '931 years · 569 → c. 1500 · about 31 generations (27–37) · generations 35 to 65',
  'nothing at all. Not one named father crosses this span.',
  'none',
  'Already broken — and it is the family’s own chart that says so. Any named father inside this span would be the single most valuable document in the archive.'),
 ('LINK EIGHT', 'the Ottoman defters', 'Rāshid al-Ḥaddādīn al-Ghassānī',
  'generation 66 · fl. c. 1500 · the first ancestor a document reaches',
  'the registers of 1525–1596; Shāhīn (1982) for the two accounts of his road.',
  'documents',
  'A register naming a different founder for Ramallah. The defter of 1596 names al-Ḥaddādīn on the hill, and nothing found so far contradicts him.'),
 ('LINK NINE', 'defters to censuses', 'Rāshid to this morning',
  'about 18 generations · generations 66 to 84 · c. 1500 → 2026 · 526 years',
  'the defters, the parish books, eleven censuses, the 1944 ration cards, living memory.',
  'documents',
  'Nothing structural. Individual descents inside this link can be checked one family at a time, and routinely are — which is what a family tree book is for.'),
]


def _wrap(text, width):
    words, lines, cur = text.split(), [], ''
    for w in words:
        if len(cur) + len(w) + 1 > width and cur:
            lines.append(cur); cur = w
        else:
            cur = (cur + ' ' + w).strip()
    if cur:
        lines.append(cur)
    return lines


def fig_chain_new():
    VOIDF, VOIDE, VOIDT = '#FDF6EC', '#E0CFAE', '#8A5A1E'
    GR = {'scripture': ('#D5E9DF', '#A9CDB8', INK, 'SCRIPTURE'),
          'join':      ('#8FBFA6', '#3E9464', INK, 'THE JOIN'),
          'classical': ('#A9CDB8', '#79B491', INK, 'CLASSICAL'),
          'attested':  ('#79B491', '#3E9464', INK, 'ATTESTED'),
          'none':      (VOIDF, VOIDE, VOIDT, 'NO EVIDENCE'),
          'documents': (GREEN, GREEN, '#FFFFFF', 'DOCUMENTS')}
    rh, top, W = 96, 104, 860
    H = top + len(CHAIN9) * rh + 116
    s = []
    _head(s, W, H,
          'THE CHAIN, LINK BY LINK — BUILT FROM THE SOURCES, NOT FROM THE CHART',
          'Nine links. Each one is defined by the source that carries it, with its span in years — and what would break it.',
          'The nine links of the chain, each defined by its source')
    s.append(txt(40, 74, 'LINK', 8.4, FOLIO, 'start', '700', 'normal', '1.5'))
    s.append(txt(126, 74, 'CARRIED BY', 8.4, FOLIO, 'start', '700', 'normal', '1.5'))
    s.append(txt(240, 74, 'THE STRETCH OF THE LINE, AND WHAT IT RESTS ON', 8.4, FOLIO, 'start', '700', 'normal', '1.5'))
    s.append(txt(820, 74, 'GRADE', 8.4, FOLIO, 'end', '700', 'normal', '1.5'))
    s.append(f'<line x1="40" y1="84" x2="820" y2="84" stroke="{RULE}"/>')
    for i, (lk, gens, title, span, carries, g, breaks) in enumerate(CHAIN9):
        y = top + i * rh
        fillc, edge, tc, lab = GR[g]
        void = (g == 'none')
        s.append(f'<rect x="40" y="{y}" width="780" height="{rh-10}" fill="#FFFFFF" '
                 f'stroke="{edge if void else RULE}" stroke-width="{1.4 if void else 1}" rx="4"/>')
        s.append(f'<rect x="40" y="{y}" width="5" height="{rh-10}" fill="{edge}" rx="2"/>')
        # the connecting eye between one link and the next — it is a chain
        if i < len(CHAIN9) - 1:
            s.append(f'<line x1="70" y1="{y+rh-10}" x2="70" y2="{y+rh}" stroke="{FOLIO}" stroke-width="2"/>')
        s.append(txt(56, y + 20, lk, 8.2, GOLD, 'start', '700', 'normal', '1.3'))
        for j, gl in enumerate(_wrap(gens, 17)[:2]):
            s.append(txt(126, y + 20 + j * 12, R.esc(gl), 9.4, FOLIO, 'start', '700'))
        s.append(txt(240, y + 21, R.esc(title), 12.5, VOIDT if void else INK, 'start', '700'))
        s.append(txt(240, y + 38, R.esc(span), 10, GREY, 'start', '400', 'italic'))
        s.append(txt(240, y + 55, R.esc(carries), 9.8, BODY))
        # what would break it — wrapped, never truncated
        s.append(txt(56, y + 71, 'BREAKS IF', 7.4, RUST, 'start', '700', 'normal', '1.2'))
        for j, ln in enumerate(_wrap(breaks, 118)[:2]):
            s.append(txt(134, y + 71 + j * 13, R.esc(ln), 9.2, GREY, 'start', '400', 'italic'))
        cw = 104
        s.append(f'<rect x="{820-cw}" y="{y+9}" width="{cw}" height="20" fill="{fillc}" '
                 f'stroke="{edge}" rx="10"/>')
        s.append(txt(820 - cw / 2, y + 23, lab, 7.4, tc, 'middle', '700', 'normal', '.9'))
        if void:
            # the corrected count, printed on the diagram
            s.append(f'<rect x="{820-cw}" y="{y+34}" width="{cw}" height="36" fill="{VOIDF}" stroke="{VOIDE}" rx="4"/>')
            s.append(f'<text x="{820-cw/2:.0f}" y="{y+48}" font-size="10" fill="{GREY}" text-anchor="middle" '
                     f'font-family="Times New Roman, Times, serif" text-decoration="line-through">the chart: 45</text>')
            s.append(txt(820 - cw / 2, y + 63, '≈31 (27–37)', 10.5, VOIDT, 'middle', '700'))
    yb = top + len(CHAIN9) * rh + 12
    s.append(f'<line x1="40" y1="{yb}" x2="820" y2="{yb}" stroke="{RULE}"/>')
    for i, ln in enumerate([
        'Read down the grade column and the shape of the argument is visible without reading a word: scripture, then scholarship, then a contemporary',
        'Greek historian, then a hole, then four hundred and sixty-four years of paper.',
        'This chain is built from the sources named in the second column, not from the family chart. John Mogannam’s chart of thirty-six generations is the',
        'family’s own guide to the same line and is printed in the appendix — where the three points at which it differs from the sources are set out.',
        'The chart counts thirteen names from Adam to ʿĀbir where Genesis gives fourteen, and prints “45 generations” at link seven where the arithmetic gives about 31.']):
        s.append(txt(40, yb + 20 + i * 15, ln, 10.2, BODY, 'start',
                     '700' if i < 2 else '400', 'normal' if i < 4 else 'italic'))
    s.append('</svg>')
    return ''.join(s)
