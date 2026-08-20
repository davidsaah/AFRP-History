# -*- coding: utf-8 -*-
"""Second figure library for the documented history: the movement maps, the
confluence of peoples, and the arithmetic of the void."""
import math
import build_recon as R

txt = R.txt
GREEN, RUST, PLUM = '#007A3D', '#A85210', '#6D4E9E'
GOLD, GREY, RULE, FOLIO = '#B98A4E', '#77726A', '#DCD6C9', '#9A958C'
INK, BODY, DARK = '#1A1A1A', '#46423B', '#004A26'
SURF, SEA, LAND = '#FCFBF8', '#E7EFF2', '#F3EFE4'
TAN = '#D4B483'


def _head(s, W, H, kicker, sub, aria):
    s.append(f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{aria}">')
    s.append(f'<rect width="{W}" height="{H}" fill="{SURF}"/>')
    s.append(txt(40, 32, kicker, 11, GOLD, 'start', '700', 'normal', '1.4'))
    s.append(txt(40, 50, sub, 10.5, GREY, 'start', '400', 'italic'))


def _strip(s, y, cols, W=860):
    """A three- or four-column evidence strip under a map."""
    s.append(f'<line x1="40" y1="{y}" x2="{W-40}" y2="{y}" stroke="{RULE}"/>')
    n = len(cols)
    w = (W - 80) / n
    for i, (head, lines) in enumerate(cols):
        x = 40 + i * w
        s.append(txt(x, y + 20, head, 9.6, GOLD, 'start', '700', 'normal', '1.2'))
        for j, ln in enumerate(lines):
            s.append(txt(x, y + 36 + j * 13, ln, 9.2, BODY))


# ═════════════════════════ the Roman and Byzantine district
def fig_map_roman():
    W, H = 860, 790
    lat0, lat1 = 31.76, 32.26
    lon0 = 34.84
    y0, y1 = 96, 540
    sy = (y1 - y0) / (lat1 - lat0)
    sx = sy * math.cos(math.radians(32.0))
    xc = 424 - (35.19 - lon0) * sx
    px = lambda lon: xc + (lon - lon0) * sx
    py = lambda lat: y0 + (lat1 - lat) * sy

    # lat, lon, label, note, kind, dx, dy, anchor
    PLACES = [
        (32.221, 35.261, 'NEAPOLIS', 'Nablus — the northern end of the road', 'city', 12, -2, 'start'),
        (32.055, 35.289, 'Silo', 'Shiloh — “twelve miles from Neapolis”', 'town', 12, -2, 'start'),
        (31.968, 35.219, 'GOPHNA', 'Jifnā — <b>the second city of Judaea</b>', 'city', -13, -6, 'end'),
        (31.927, 35.238, 'Baithel', 'Beitin — “twelve miles from Jerusalem, to the', 'town', 14, 20, 'start'),
        (31.951, 35.302, 'Ephron, also Ephraia', 'Ṭaybeh — “where the Lord went”', 'town', 12, -2, 'start'),
        (32.026, 35.065, 'Armathem', 'Rantis — Arimathea', 'town', -12, -2, 'end'),
        (31.872, 35.114, 'Bethoron', 'Bayt ʿŪr', 'town', -12, 48, 'end'),
        (31.780, 35.230, 'AELIA CAPITOLINA', 'Jerusalem', 'city', 12, 2, 'start'),
        (31.951, 34.891, 'Diospolis', 'Lydda', 'town', 12, -12, 'start'),
    ]
    ROAD = [(31.780, 35.230), (31.900, 35.222), (31.927, 35.238), (31.968, 35.219),
            (32.055, 35.270), (32.140, 35.265), (32.221, 35.261)]

    s = []
    _head(s, W, H, 'THE DISTRICT WHEN ROME WROTE IT DOWN',
          'Every place on this map is named in a Roman or Byzantine text. One of them is not.',
          'Map of the Ramallah district in the Roman and Byzantine periods showing the Jerusalem to Neapolis road')
    s.append(f'<path d="M{px(35.13):.0f} {py(32.26):.0f} C {px(35.33):.0f} {py(32.08):.0f}, '
             f'{px(35.12):.0f} {py(31.94):.0f}, {px(35.30):.0f} {py(31.76):.0f} '
             f'L {px(35.42):.0f} {py(31.76):.0f} L {px(35.42):.0f} {py(32.26):.0f} Z" '
             f'fill="{LAND}" opacity=".5"/>')
    s.append(txt(px(35.395), py(31.86), 'the central', 9.4, TAN, 'middle', '700'))
    s.append(txt(px(35.395), py(31.845), 'ridge', 9.4, TAN, 'middle', '700'))
    d = 'M' + ' L'.join(f'{px(lo):.1f} {py(la):.1f}' for la, lo in ROAD)
    s.append(f'<path d="{d}" fill="none" stroke="{RUST}" stroke-width="4" opacity=".9"/>')
    s.append(f'<path d="{d}" fill="none" stroke="{SURF}" stroke-width="1.1" stroke-dasharray="2 7"/>')
    for la, lo, n in [(31.826, 35.227, 'V'), (31.900, 35.222, 'X'),
                      (32.108, 35.270, 'XXII'), (32.200, 35.262, 'XXVIII')]:
        s.append(f'<circle cx="{px(lo):.1f}" cy="{py(la):.1f}" r="8" fill="{SURF}" stroke="{RUST}" stroke-width="1.4"/>')
        s.append(txt(px(lo), py(la) + 3.4, n, 7.6, RUST, 'middle', '700'))
    s.append(txt(px(35.33), py(32.15), 'the Roman road,', 10.2, RUST, 'start', '700'))
    s.append(txt(px(35.33), py(32.127), 'Aelia Capitolina to Neapolis —', 10.2, RUST, 'start', '700'))
    s.append(txt(px(35.33), py(32.104), 'milestones counted in Roman miles', 9.4, RUST, 'start'))

    for la, lo, lab, note, kind, dx, dy, anc in PLACES:
        x, y = px(lo), py(la)
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{6 if kind=="city" else 4.2}" fill="{GREEN}"/>')
        s.append(txt(x + dx, y + dy, lab, 10.6 if kind == 'city' else 9.9, INK, anc, '700'))
        bold = note.replace('<b>', '<tspan font-weight="700">').replace('</b>', '</tspan>')
        s.append(txt(x + dx, y + dy + 12, bold, 9, BODY, anc, '400', 'italic'))
    s.append(txt(px(35.238) + 14, py(31.927) + 43, 'right of the road going to Neapolis” — Eusebius', 9, BODY, 'start', '400', 'italic'))

    kx, ky = px(35.183), py(31.899)
    s.append(f'<rect x="{kx-4.5:.1f}" y="{ky-4.5:.1f}" width="9" height="9" fill="{PLUM}"/>')
    s.append(txt(kx - 12, ky + 18, 'Khirbet et-Tireh', 9.9, PLUM, 'end', '700'))
    s.append(txt(kx - 12, ky + 30, 'two churches, a monastery, an oil press,', 8.9, PLUM, 'end'))
    s.append(txt(kx - 12, ky + 41, 'mosaics, a bread stamp — and no name', 8.9, PLUM, 'end'))

    rx, ry = px(35.204), py(31.903)
    s.append(f'<circle cx="{rx:.1f}" cy="{ry:.1f}" r="15" fill="none" stroke="{GOLD}" stroke-width="1.8" stroke-dasharray="3 3"/>')
    s.append(f'<circle cx="{rx:.1f}" cy="{ry:.1f}" r="3.6" fill="{GOLD}"/>')
    s.append(txt(rx - 22, ry - 30, 'the site of Ramallah', 10.6, GOLD, 'end', '700'))
    s.append(txt(rx - 22, ry - 18, 'named in no Roman or Byzantine text —', 9.2, GOLD, 'end', '400', 'italic'))
    s.append(txt(rx - 22, ry - 7, 'and in none at all until 1279', 9.2, GOLD, 'end', '400', 'italic'))

    ly = 566
    s.append(f'<circle cx="46" cy="{ly}" r="5.6" fill="{GREEN}"/>')
    s.append(txt(58, ly + 4, 'named by Pliny, Josephus, Ptolemy, Eusebius or the Madaba mosaic', 9.8, BODY))
    s.append(f'<rect x="466" y="{ly-4.5}" width="9" height="9" fill="{PLUM}"/>')
    s.append(txt(481, ly + 4, 'excavated, but named in no surviving text', 9.8, BODY))

    _strip(s, 588, [
        ('PLINY, c. 77 CE', ['<tspan font-style="italic">Natural History</tspan> V.70 lists the ten',
                             'toparchies of Judaea. Gophna is one',
                             'of them — this district had a name',
                             'and an administration.']),
        ('JOSEPHUS, c. 75 CE', ['<tspan font-style="italic">Jewish War</tspan> III.54–55: “Gophna was',
                                'the second of those cities” after',
                                'Jerusalem. IV.551: Vespasian takes',
                                'the Gophnitick toparchy in 68 CE.']),
        ('EUSEBIUS, c. 320 CE', ['The <tspan font-style="italic">Onomasticon</tspan> measures this',
                                 'landscape in milestones along the',
                                 'Neapolis road — the same road the',
                                 'family walks up in 1562.']),
        ('THE MADABA MAP, 6th c.', ['Γοφνα · Λουζα ἡ καὶ Βεθηλ ·',
                                    'Εφρων ἡ Εφραια · Σηλω ·',
                                    'Αρμαθεμ · Βεθωρων — six of the',
                                    'neighbours, set in mosaic.']),
    ])
    s.append(txt(40, H - 40, 'The hills the family arrived on were not a wilderness. They were an imperial district with a paved highway down the middle of them, and Rome, Byzantium', 10.4, BODY, 'start', '700'))
    s.append(txt(40, H - 25, 'and the Church all wrote it down — village by village, milestone by milestone. What none of them wrote down was Ramallah.', 10.4, BODY, 'start', '700'))
    s.append(txt(40, H - 8, 'Pliny, <tspan font-style="italic">NH</tspan> V.70; Josephus, <tspan font-style="italic">BJ</tspan> III.54–55, IV.551, V.50, VI.115; Eusebius, <tspan font-style="italic">Onomasticon</tspan>, s.vv. Baithel, Silo; the Madaba mosaic; Tappy, <tspan font-style="italic">NEA</tspan> 75 (2012) on the road; al-Houdalieh on Khirbet et-Tireh.', 8.8, FOLIO, 'start', '400', 'italic'))
    s.append('</svg>')
    return ''.join(s)


# ═════════════════════════ Karak to the ridge
def fig_map_karak():
    W, H = 860, 920
    lat0, lat1 = 30.42, 32.02
    lon0 = 34.82
    y0, y1 = 96, 676
    sy = (y1 - y0) / (lat1 - lat0)
    sx = sy * math.cos(math.radians(31.6))
    xc = 418 - (35.36 - lon0) * sx
    px = lambda lon: xc + (lon - lon0) * sx
    py = lambda lat: y0 + (lat1 - lat) * sy

    s = []
    _head(s, W, H, 'THE ROAD THE FAMILY ACTUALLY WALKED',
          'Karak to the ridge, in three moves and about half a century — and every leg of it is carried by a document.',
          'Map of the family migration from Karak in Transjordan to Ramallah')
    east = [(31.77, 35.565), (31.60, 35.585), (31.45, 35.565), (31.30, 35.530),
            (31.15, 35.492), (31.05, 35.470)]
    west = [(31.05, 35.432), (31.15, 35.420), (31.30, 35.430), (31.45, 35.452),
            (31.60, 35.470), (31.77, 35.500)]
    s.append('<path d="M' + ' L'.join(f'{px(lo):.1f} {py(la):.1f}' for la, lo in east + west) +
             f' Z" fill="{SEA}" stroke="#B9CBD4" stroke-width="1"/>')
    s.append(txt(px(35.62), py(31.44), 'the', 9.2, '#7C99A6', 'start', '700', 'italic'))
    s.append(txt(px(35.62), py(31.40), 'Dead Sea', 9.2, '#7C99A6', 'start', '700', 'italic'))
    s.append(f'<path d="M{px(35.565):.1f} {py(32.02):.1f} C {px(35.50):.1f} {py(31.92):.1f}, '
             f'{px(35.56):.1f} {py(31.86):.1f}, {px(35.53):.1f} {py(31.79):.1f}" '
             f'fill="none" stroke="#B9CBD4" stroke-width="2.6"/>')
    s.append(txt(px(35.585), py(31.95), 'the Jordan', 8.8, '#7C99A6', 'start', '400', 'italic'))

    LEGS = [(31.180, 35.702, 31.600, 35.045), (31.600, 35.045, 31.716, 35.188),
            (31.716, 35.188, 31.903, 35.204)]
    s.append('<defs><marker id="arw" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" '
             f'markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{GOLD}"/></marker></defs>')
    for la1, lo1, la2, lo2 in LEGS:
        ax, ay, bx2, by2 = px(lo1), py(la1), px(lo2), py(la2)
        mx = (ax + bx2) / 2 + (by2 - ay) * .20
        my = (ay + by2) / 2 - (bx2 - ax) * .20
        s.append(f'<path d="M{ax:.1f} {ay:.1f} Q {mx:.1f} {my:.1f} {bx2:.1f} {by2:.1f}" '
                 f'fill="none" stroke="{GOLD}" stroke-width="2.8" marker-end="url(#arw)"/>')

    STOPS = [
        (31.180, 35.702, 'al-KARAK', '1596 — 103 Christian households and<br>8 bachelors (Ottoman Defter 185)', 'big', 14, -4, 'start'),
        (30.532, 35.560, 'al-Shawbak', '1321 — “most of the inhabitants<br>were Christians” (Abū al-Fidāʾ)', 'sm', 14, 4, 'start'),
        (30.780, 35.520, 'Gharandal', '<tspan font-weight="700">890 — al-Yaʿqūbī still finds Ghassān</tspan><br>living here, by name', 'key', -14, 4, 'end'),
        (31.716, 35.795, 'Mādabā · Nitl', 'a sixth-century church names<br>“Thaʿlaba, the most illustrious phylarch”', 'sm', 14, -4, 'start'),
        (31.600, 35.045, 'Kusbār', 'farmland between Ḥalḥūl and Kharās —<br>the stage the family story leaves out', 'mid', -14, 6, 'end'),
        (31.716, 35.188, 'BAYT JĀLĀ', '1553–54 — 36 Christian households,<br>the group called the Kasābra', 'big', -14, -6, 'end'),
        (31.903, 35.204, 'RAMALLAH', '1562 — 37 Christian households<br>against 10 Muslim', 'home', 17, -4, 'start'),
        (31.780, 35.230, 'Jerusalem', '', 'dot', 12, 4, 'start'),
        (31.968, 35.219, 'Jifnā', '', 'dot', -11, 4, 'end'),
        (31.530, 35.098, 'Ḥalḥūl', '', 'dot', 11, 12, 'start'),
    ]
    for la, lo, lab, note, kind, dx, dy, anc in STOPS:
        x, y = px(lo), py(la)
        col = {'home': GOLD, 'big': GREEN, 'mid': GREEN, 'sm': FOLIO, 'dot': FOLIO, 'key': RUST}[kind]
        rr = {'home': 7, 'big': 6.4, 'mid': 5, 'sm': 4, 'dot': 3.2, 'key': 5.6}[kind]
        if kind == 'home':
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="14" fill="none" stroke="{GOLD}" stroke-width="1.6" stroke-dasharray="3 3"/>')
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr}" fill="{col}"/>')
        s.append(txt(x + dx, y + dy, lab, 10.6 if kind in ('big', 'home') else 9.6, RUST if kind == 'key' else INK, anc,
                     '700' if kind in ('big', 'home', 'mid', 'key') else '400'))
        if note:
            for i, ln in enumerate(note.split('<br>')):
                s.append(txt(x + dx, y + dy + 12 + i * 11, ln, 8.9, BODY, anc, '400', 'italic'))

    # use the empty south-west of the frame for the plateau argument
    nx, ny = 62, 500
    s.append(f'<line x1="{nx}" y1="{ny-16}" x2="{nx+300}" y2="{ny-16}" stroke="{GOLD}" stroke-width="2"/>')
    s.append(txt(nx, ny, 'THE PLATEAU, 890 → 1562', 9.6, GOLD, 'start', '700', 'normal', '1.2'))
    for i, ln in enumerate([
        'Four dated records keep Christians on this plateau right',
        'across the stretch the family chart leaves blank: Ghassān',
        'named at Gharandal in 890; Christians at Shawbak when the',
        'pilgrim Thietmar passes in 1217–18; a Christian majority',
        'at Shawbak in 1321; and 103 Christian households plus',
        'eight bachelors at Karak in the register of 1596.',
        '',
        'The continuity here is of a place and a faith. What no',
        'document supplies is a line of fathers.']):
        s.append(txt(nx, ny + 20 + i * 14, ln, 9.4, BODY, 'start', '700' if i > 6 else '400'))
    _strip(s, 716, [
        ('1 · KARAK → KUSBĀR', ['Tradition, plus the documented Christian',
                                'demography of the plateau: the pilgrim',
                                'Thietmar in Shawbak’s suburb, 1217–18;',
                                'a Christian majority at Shawbak in 1321;',
                                '103 Christian households and 8 bachelors',
                                'at Karak in the register of 1596.']),
        ('2 · KUSBĀR → BAYT JĀLĀ', ['The Ottoman register of 1553–54 finds the',
                                    'group at Bayt Jālā — 36 Christian house-',
                                    'holds, eleven miles south of the ridge.',
                                    'They are not yet at Ramallah.']),
        ('3 · BAYT JĀLĀ → RAMALLAH', ['1562: twenty-seven families and eight',
                                      'unmarried men come up the ridge road.',
                                      'The site already holds ten Muslim',
                                      'households — and already has a name.']),
    ])
    s.append(txt(40, H - 42, 'The archival research puts the movers a generation lower than the family’s own telling does: it is Rāshid’s <tspan font-style="italic">grandchildren</tspan> who make the last leg, not his sons.', 10.4, BODY, 'start', '700'))
    s.append(txt(40, H - 26, 'And note what this plateau is: the one place in the world where a Ghassān population is still named in a text after the seventh century — at Gharandal, in 890.', 10.4, BODY, 'start', '700'))
    s.append(txt(40, H - 8, 'Hammoudeh, <tspan font-style="italic">Jerusalem Quarterly</tspan> 59 (2014), from the Jerusalem sharīʿa registers and the Ottoman defters; Piccirillo, <tspan font-style="italic">Liber Annuus</tspan> 51 (2001) for Nitl; al-Yaʿqūbī (d. 890) for Gharandal.', 8.8, FOLIO, 'start', '400', 'italic'))
    s.append('</svg>')
    return ''.join(s)


# ═════════════════════════ the diaspora
def fig_map_diaspora():
    W, H = 860, 520
    lonA, lonB = -126.0, 40.0
    latB = 52.0
    x0, x1 = 54, 812
    sx = (x1 - x0) / (lonB - lonA)
    sy = sx / math.cos(math.radians(35))
    ytop = 92
    px = lambda lo: x0 + (lo - lonA) * sx
    py = lambda la: ytop + (latB - la) * sy

    US = [(-124.7,48.4),(-124.2,40.4),(-120.6,34.5),(-117.1,32.5),(-114.7,32.7),(-111.0,31.3),
          (-108.2,31.3),(-106.5,31.8),(-104.0,29.5),(-99.5,27.5),(-97.2,26.0),(-95.0,29.0),
          (-90.0,29.1),(-88.0,30.3),(-84.0,29.7),(-82.7,27.0),(-80.1,25.2),(-81.5,31.0),
          (-79.0,33.5),(-75.5,36.0),(-74.0,40.5),(-70.0,43.0),(-67.0,44.8),(-71.0,45.0),
          (-79.0,43.3),(-82.5,45.3),(-88.0,48.0),(-95.0,49.0),(-123.0,49.0)]
    MEX = [(-97.2,26.0),(-94.5,18.2),(-90.6,21.0),(-86.8,21.4),(-88.3,15.6),(-83.2,9.0),
           (-79.5,9.2),(-83.6,12.6),(-87.4,16.0),(-92.2,15.0),(-96.5,15.7),(-104.0,19.0),
           (-109.5,23.0),(-112.5,27.5),(-114.7,32.7),(-108.2,31.3),(-104.0,29.5),(-99.5,27.5)]
    EUAF = [(-9.5,43.0),(-9.0,38.7),(-6.0,36.0),(0.0,39.0),(5.0,43.0),(12.0,44.0),(15.0,40.0),
            (18.5,40.5),(23.0,38.0),(26.0,39.5),(29.0,41.0),(36.0,36.6),(35.0,33.0),(34.2,31.3),
            (32.0,31.2),(25.0,31.5),(19.0,30.4),(11.0,33.9),(10.5,37.0),(3.0,36.9),(-2.0,35.2),
            (-6.0,35.8),(-9.8,31.5),(-16.0,21.0),(-17.5,14.7),(-13.5,12.0),(0.0,12.0),
            (20.0,12.0),(38.0,12.0),(38.0,42.0),(20.0,45.0),(10.0,47.5),(0.0,49.0),(-4.5,48.5),
            (-1.5,46.0),(-9.5,43.0)]

    def poly(pts, fill):
        return ('<path d="M' + ' L'.join(f'{px(lo):.1f} {py(la):.1f}' for lo, la in pts) +
                f' Z" fill="{fill}" stroke="#DDD6C6" stroke-width=".9"/>')

    s = []
    _head(s, W, H, 'WHERE RAMALLAH WENT, 1901 ONWARD',
          'The town began exporting its own people in 1901, and has lived in two places ever since.',
          'Map of the Ramallah diaspora from 1901')
    s.append(f'<rect x="{x0}" y="{ytop}" width="{x1-x0}" height="{40*sy:.0f}" fill="{SEA}" opacity=".5"/>')
    s.append(poly(US, LAND)); s.append(poly(MEX, LAND)); s.append(poly(EUAF, LAND))

    hx, hy = px(35.2), py(31.9)
    CITIES = [
        (42.33, -83.05, 'Detroit', 'the Federation’s home', 1.0, 0, -30, 'middle'),
        (41.50, -81.69, 'Cleveland', '', .55, -12, -8, 'end'),
        (41.88, -87.63, 'Chicago', '', .55, -13, 4, 'end'),
        (40.71, -74.01, 'New York', 'Huda Press, 1954', .8, 14, 16, 'start'),
        (30.33, -81.66, 'Jacksonville', '', .8, 8, 23, 'middle'),
        (33.52, -86.80, 'Birmingham', '', .55, -13, 7, 'end'),
        (37.77, -122.42, 'San Francisco', '', .7, 4, -15, 'middle'),
        (34.05, -118.24, 'Los Angeles', '', .6, -13, 9, 'end'),
        (15.50, -88.03, 'Central America', 'Honduras, El Salvador', .5, 0, 25, 'middle'),
    ]
    for la, lo, lab, note, wgt, dx, dy, anc in CITIES:
        x, y = px(lo), py(la)
        mx, my = (x + hx) / 2, min(y, hy) - 44 - wgt * 30
        s.append(f'<path d="M{hx:.1f} {hy:.1f} Q {mx:.1f} {my:.1f} {x:.1f} {y:.1f}" fill="none" '
                 f'stroke="{GOLD}" stroke-width="{0.8+wgt*1.8:.1f}" opacity=".78"/>')
    for la, lo, lab, note, wgt, dx, dy, anc in CITIES:
        x, y = px(lo), py(la)
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{3.2+wgt*2.6:.1f}" fill="{GREEN}" stroke="#fff" stroke-width="1.2"/>')
        s.append(txt(x + dx, y + dy, lab, 9.8, INK, anc, '700'))
        if note:
            s.append(txt(x + dx, y + dy + 11, note, 8.6, BODY, anc, '400', 'italic'))
    s.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="15" fill="none" stroke="{RUST}" stroke-width="1.6" stroke-dasharray="3 3"/>')
    s.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="4.6" fill="{RUST}"/>')
    s.append(txt(hx, hy + 33, 'RAMALLAH', 10.6, RUST, 'middle', '700'))

    _strip(s, H - 136, [
        ('1901', ['The first men leave for the', 'United States — the date comes', 'from Shāhīn, not from a census.']),
        ('1931', ['The census counts 1,941 men', 'against 2,345 women. The', 'emigration is in the sex ratio.']),
        ('1945 · 1951', ['The Summer Resorts Company is', 'capitalised at 50,000 dinars, mostly', 'by stockholders abroad — and it', 'brings the town its water.']),
        ('1958 / 1959', ['The Federation is incorporated in', 'Detroit. The town now has a second', 'capital, four thousand miles west.']),
    ])
    s.append(txt(40, H - 12, 'Line weight is the weight of a community in the family’s own record, not a count — the Ramallah diaspora has never been properly enumerated. Shāhīn (1982); the Federation’s own conventions.', 8.8, FOLIO, 'start', '400', 'italic'))
    s.append('</svg>')
    return ''.join(s)


# ═════════════════════════ the confluence of peoples
def fig_confluence():
    W, H = 860, 710
    x0, x1 = 268, 812

    def px(y):
        pts = [(-1600, x0), (-1000, x0 + 80), (-500, x0 + 156), (0, x0 + 226),
               (500, x0 + 296), (1000, x0 + 372), (1500, x0 + 452), (2025, x1)]
        for (a, xa), (b, xb) in zip(pts, pts[1:]):
            if y <= b:
                return xa + (xb - xa) * (y - a) / (b - a)
        return x1

    ROWS = [
        (-1600, 'CANAANITES', 'the population already here — the bed of the river', GREEN, 'base'),
        (-1200, 'Israelites', 'emerging <tspan font-style="italic">from</tspan> these highlands, not into them', '#5E9B76', 'absorbed'),
        (-1175, 'Philistines', 'a real migration — visible in the genome at Ashkelon', PLUM, 'measured'),
        (-400, 'Samaritans', 'branch away — and are on Mount Gerizim to this day', '#3F7C90', 'apart'),
        (-332, 'Greeks', 'cities, a language, and a new elite', '#9A8CC0', 'absorbed'),
        (-110, 'Idumaeans', 'joined to Judaea under the Hasmoneans; gone as a name by 70 CE', RUST, 'absorbed'),
        (106, 'Nabataeans', 'their kingdom becomes the Roman province of Arabia', '#C08A4A', 'absorbed'),
        (324, 'Romans, and the Church', 'the country turns Christian without anybody moving', '#6D4E9E', 'absorbed'),
        (636, 'ARABS — and Ghassān', '<tspan font-weight="700">the family’s own claimed stream</tspan>', GOLD, 'absorbed'),
        (1099, 'Franks', 'the one arrival that mostly leaves again', '#8A8A8A', 'leaves'),
    ]

    s = []
    _head(s, W, H, 'HOW A PEOPLE IS MADE',
          'Ten arrivals, one people. Every stream but two is still in the water — and the water was already flowing when the first of them arrived.',
          'Diagram showing successive peoples merging into the population of Palestine')

    ytop, step = 100, 40
    for yr, lab in [(-1500, '1500 BCE'), (-1000, '1000 BCE'), (-500, '500 BCE'), (0, 'CE 1'),
                    (500, '500'), (1000, '1000'), (1500, '1500'), (2025, 'today')]:
        s.append(f'<line x1="{px(yr):.1f}" y1="{ytop-16}" x2="{px(yr):.1f}" y2="{ytop+step*len(ROWS)+50}" stroke="{RULE}" stroke-width=".8"/>')
        s.append(txt(px(yr), ytop - 22, lab, 9.2, FOLIO, 'middle'))

    defs, body = ['<defs>'], []
    for i, (yr, lab, note, col, fate) in enumerate(ROWS):
        y = ytop + i * step
        bx = px(yr)
        ex = px(1291) if fate == 'leaves' else x1
        wdt = max(ex - bx, 6)
        gid = f'cf{i}'
        if fate in ('absorbed', 'measured', 'base'):
            stop = 0.10 if fate == 'base' else min(0.42, 150.0 / wdt)
            defs.append(f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">'
                        f'<stop offset="0" stop-color="{col}"/>'
                        f'<stop offset="{stop:.3f}" stop-color="{GREEN}"/>'
                        f'<stop offset="1" stop-color="{GREEN}"/></linearGradient>')
            fill = f'url(#{gid})'
        elif fate == 'leaves':
            defs.append(f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">'
                        f'<stop offset="0" stop-color="{col}"/>'
                        f'<stop offset="1" stop-color="{col}" stop-opacity=".22"/></linearGradient>')
            fill = f'url(#{gid})'
        else:
            fill = col
        body.append(f'<rect x="{bx:.1f}" y="{y-8:.1f}" width="{wdt:.1f}" height="16" fill="{fill}" rx="2"/>')
        body.append(f'<circle cx="{bx:.1f}" cy="{y:.1f}" r="5" fill="{col}" stroke="{SURF}" stroke-width="1.4"/>')
        body.append(txt(x0 - 16, y - 2, lab, 10.4, GREEN if fate == 'base' else col, 'end', '700'))
        body.append(txt(x0 - 16, y + 10, note, 8.9, BODY, 'end', '400', 'italic'))
        if fate == 'apart':
            body.append(txt(x1 - 8, y + 4, 'still here', 9.2, '#FFFFFF', 'end', '700'))
        if fate == 'leaves':
            body.append(f'<path d="M{ex:.1f} {y:.1f} l 24 -15" stroke="#8A8A8A" stroke-width="1.6" stroke-dasharray="4 3" fill="none"/>')
            body.append(txt(ex + 28, y - 16, 'and leaves, 1187–1291', 8.9, '#7A7A7A', 'start', '700'))
        if fate == 'measured':
            mx = bx + min(150.0, wdt * .42)
            body.append(f'<path d="M{bx:.1f} {y+16:.1f} L{mx:.1f} {y+16:.1f}" stroke="{PLUM}" stroke-width="1.3"/>')
            body.append(f'<path d="M{bx:.1f} {y+12:.1f} L{bx:.1f} {y+20:.1f} M{mx:.1f} {y+12:.1f} L{mx:.1f} {y+20:.1f}" stroke="{PLUM}" stroke-width="1.3"/>')
            body.append(txt(mx + 8, y + 19, 'two centuries, and undetectable', 8.4, PLUM, 'start', '700'))
    defs.append('</defs>')
    s.extend(defs); s.extend(body)

    ry = ytop + step * len(ROWS) + 4
    s.append(f'<rect x="{x0}" y="{ry}" width="{x1-x0}" height="32" fill="{GREEN}" rx="3"/>')
    s.append(txt(x0 + 12, ry + 21, 'the people of this land', 11, '#FFFFFF', 'start', '700'))
    s.append(txt(x1 - 12, ry + 21, 'PALESTINIANS', 11.5, '#FFFFFF', 'end', '700', 'normal', '.8'))
    s.append(txt(x0 - 16, ry + 15, 'and what they became', 10.2, GREEN, 'end', '700'))
    s.append(txt(x0 - 16, ry + 27, 'one people, ten arrivals', 8.9, BODY, 'end', '400', 'italic'))

    by = H - 98
    s.append(f'<line x1="40" y1="{by-16}" x2="820" y2="{by-16}" stroke="{RULE}"/>')
    s.append(txt(40, by + 2, 'The Philistine case is the one that can actually be measured, and it settles the argument:', 10.4, INK, 'start', '700'))
    s.append(txt(40, by + 18, '“Within no more than two centuries, this genetic footprint introduced during the early Iron Age is no longer detectable and seems to be diluted by a local', 10, BODY))
    s.append(txt(40, by + 32, 'Levantine related gene pool.” — Feldman et al., <tspan font-style="italic">Science Advances</tspan> 5 (2019). <tspan font-weight="700">They were not driven out. They became the neighbours.</tspan>', 10, BODY))
    s.append(txt(40, by + 52, 'And for the Levant as a whole: more than ninety per cent of present-day ancestry descends from the Bronze Age Canaanite population (Haber et al. 2017; Agranat-Tamir et al. 2020).', 10, BODY))
    s.append(txt(40, H - 10, 'The Crusaders are the exception, and are drawn as one: most Franks left or were expelled, and only a faint Y-chromosome trace survives (Haber et al. 2019).', 8.8, FOLIO, 'start', '400', 'italic'))
    s.append('</svg>')
    return ''.join(s)


# ═════════════════════════ the arithmetic of the void
def fig_void_solved():
    W, H = 860, 652
    x0, x1 = 218, 664
    t0, t1 = 500, 1560
    px = lambda y: x0 + (x1 - x0) * (y - t0) / (t1 - t0)
    band_y, band_h = 176, 78

    s = []
    _head(s, W, H, 'THE VOID, MEASURED — AND SHORTENED',
          'Generation 35 of the family chart is a single line. The arithmetic says it should be about thirty-one.',
          'Diagram measuring how many generations are missing from the family chart')

    # the arithmetic, as a header strip
    s.append(f'<rect x="40" y="70" width="780" height="34" fill="#FFFFFF" stroke="{RULE}" rx="3"/>')
    s.append(txt(52, 91, 'THE SUM', 8.8, GOLD, 'start', '700', 'normal', '1.3'))
    cells = [('569 → 1500', '931 years'), ('at 25 yrs a generation', '37'), ('at 30', '31'),
             ('at 32', '29'), ('at 35', '27'), ('the chart draws', '2'), ('so, missing', '25–35')]
    cx = 118
    for lab2, val in cells:
        s.append(txt(cx, 85, lab2, 8.4, FOLIO))
        s.append(txt(cx, 97, val, 10.4, '#8A5A1E' if lab2 == 'so, missing' else INK, 'start', '700'))
        cx += max(len(lab2) * 4.6 + 20, 62)
    s.append(f'<rect x="{px(569):.1f}" y="{band_y}" width="{px(1500)-px(569):.1f}" height="{band_h}" fill="#FDF6EC" stroke="#E8D9BE"/>')
    for yr in range(600, 1500, 30):
        s.append(f'<line x1="{px(yr):.1f}" y1="{band_y+6}" x2="{px(yr):.1f}" y2="{band_y+band_h-6}" stroke="{TAN}" stroke-width="1" opacity=".5"/>')
    s.append(f'<path d="M{px(569):.1f} {band_y-16:.0f} L{px(1500):.1f} {band_y-16:.0f}" stroke="#8A5A1E" stroke-width="1"/>')
    s.append(txt((px(569)+px(1500))/2, band_y - 24, 'THE GENEALOGICAL VOID — 931 years, about thirty-one generations, and only three of them named', 9.8, '#8A5A1E', 'middle', '700'))
    s.append(txt((px(569)+px(1500))/2, band_y + band_h/2 + 4, 'the chart draws one line across all of this', 9.6, '#8A5A1E', 'middle', '400', 'italic'))

    for yr, lab, lines, anc in [
        (569, 'GENERATION 34', ['al-Ḥārith ibn Jabala,', 'phylarch, d. 569 —', 'Procopius names him', 'in his own lifetime'], 'end'),
        (1500, 'GENERATION 36', ['Rāshid al-Ḥaddādīn,', 'fl. c. 1500. His grand-', 'children reach the ridge', 'in 1562, and are counted'], 'start')]:
        x = px(yr)
        dx = -12 if anc == 'end' else 12
        s.append(f'<line x1="{x:.1f}" y1="{band_y-6}" x2="{x:.1f}" y2="{band_y+band_h+6}" stroke="{GREEN}" stroke-width="3"/>')
        s.append(f'<circle cx="{x:.1f}" cy="{band_y+band_h/2:.0f}" r="7" fill="{GREEN}" stroke="#fff" stroke-width="2"/>')
        s.append(txt(x + dx, band_y + 6, lab, 10.2, INK, anc, '700'))
        for i, ln in enumerate(lines):
            s.append(txt(x + dx, band_y + 20 + i * 11, ln, 8.9, BODY, anc, '400', 'italic'))

    dy = band_y + band_h + 26
    s.append(f'<rect x="{px(890):.1f}" y="{dy}" width="{px(1500)-px(890):.1f}" height="24" fill="{GREEN}" opacity=".13" stroke="{GREEN}"/>')
    s.append(txt((px(890)+px(1500))/2, dy + 16, 'THE DOCUMENTARY VOID — 610 years', 9.8, DARK, 'middle', '700'))
    s.append(f'<path d="M{px(569):.1f} {dy+12:.0f} L{px(886):.1f} {dy+12:.0f}" stroke="{GREEN}" stroke-width="2.4"/>')
    s.append(txt((px(569)+px(890))/2, dy + 6, 'a Ghassān population is still named here', 8.6, DARK, 'middle', '700'))

    ax = dy + 58
    for yr in range(600, 1501, 100):
        s.append(f'<line x1="{px(yr):.1f}" y1="{ax}" x2="{px(yr):.1f}" y2="{ax+5}" stroke="{FOLIO}"/>')
        s.append(txt(px(yr), ax + 16, str(yr), 8.8, FOLIO, 'middle'))
    s.append(f'<line x1="{px(569):.1f}" y1="{ax}" x2="{px(1500):.1f}" y2="{ax}" stroke="{FOLIO}"/>')

    MARKS = [(594, 'Greek sources stop naming the Ghassanids. <tspan font-style="italic">The void has a start date.</tspan>', 'edge'),
             (684, 'Marj Rāhiṭ — a Ghassanid faction still makes a caliph, from the old capital at Jābiya', 'yes'),
             (890, '<tspan font-weight="700">al-Yaʿqūbī finds Ghassān in the Ghūṭa of Damascus — and at Gharandal, in Transjordan</tspan>', 'key'),
             (1058, 'ʿAbūd — a Syriac inscription names a patriarch, an archbishop and a priest', 'yes'),
             (1179, 'Jifnā — Ibrāhīm and his brothers, sons of Mūsā, named in stone at Choziba', 'yes'),
             (1218, 'Shawbak — the pilgrim Thietmar finds Christians in the suburbs, 1217–18', 'yes'),
             (1321, 'al-Shawbak — a Christian majority (Abū al-Fidāʾ)', 'yes'),
             (1374, 'Jifnā — Niʿma b. Bishāra, in the Ḥaram al-Sharīf documents', 'yes')]
    my = ax + 40
    for yr, lab, kind in MARKS:
        x = px(yr)
        col = GOLD if kind == 'key' else (RUST if kind == 'edge' else GREEN)
        s.append(f'<line x1="{x:.1f}" y1="{ax+2}" x2="{x:.1f}" y2="{my-6:.0f}" stroke="{col}" stroke-width="1" stroke-dasharray="2 3" opacity=".65"/>')
        s.append(f'<circle cx="{x:.1f}" cy="{my:.0f}" r="{5 if kind=="key" else 4}" fill="{col}"/>')
        s.append(txt(x + 10, my + 3, str(yr), 9.4, col, 'start', '700'))
        s.append(txt(x + 44, my + 3, lab, 9, BODY))
        my += 22

    s.append(f'<line x1="40" y1="{H-88}" x2="820" y2="{H-88}" stroke="{RULE}"/>')
    s.append(txt(40, H - 68, 'The void is not empty of evidence. It is empty of names.', 11.5, INK, 'start', '700'))
    s.append(txt(40, H - 50, 'Eight dated records fall inside the stretch the chart leaves blank — and one of them, al-Yaʿqūbī writing in the ninth century, puts a Ghassān population in Transjordan by', 10, BODY))
    s.append(txt(40, H - 36, 'name, on the very plateau the family remembers. What no source supplies is a chain of fathers. The honest correction is therefore not to invent thirty names, but to print the number.', 10, BODY))
    s.append(txt(40, H - 12, 'Procopius, <tspan font-style="italic">Wars</tspan> I.17; Serikoff (2017) for the silence after 594; Kennedy (2010) and al-Yaʿqūbī (d. 890); the ʿAbūd, Jifnā, Karak and Shawbak records as cited in Part II.', 8.8, FOLIO, 'start', '400', 'italic'))
    s.append('</svg>')
    return ''.join(s)
