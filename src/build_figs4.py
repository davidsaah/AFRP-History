# -*- coding: utf-8 -*-
"""Fourth figure library, for the deep past and the branch at Eber:
   fig_peopling  — the earliest dated sites in and around the Ramallah district
   fig_layers    — the land drawn as a tell section: fifteen thousand years of layering
   fig_branch    — Genesis 10–11: where our line splits from Abraham's, and where Moses sits
"""
import math
import build_recon as R

txt, esc = R.txt, R.esc
GREEN, RUST, PLUM = '#007A3D', '#A85210', '#6D4E9E'
GOLD, GREY, RULE, FOLIO = '#B98A4E', '#77726A', '#DCD6C9', '#9A958C'
INK, BODY, DARK = '#1A1A1A', '#46423B', '#004A26'
SURF, SEA, LAND, TAN = '#FCFBF8', '#E7EFF2', '#F3EFE4', '#D4B483'

# The centre of present-day Ramallah. Every distance printed on a plate in this
# library is COMPUTED from this point and the site's own plotted coordinates, so
# a label can never drift away from the dot it belongs to.
RAM_LAT, RAM_LON = 31.8996, 35.2042


def _km(lat, lon, lat0=RAM_LAT, lon0=RAM_LON):
    """Great-circle kilometres, rounded the way the book prints them."""
    R = 6371.0
    p1, p2 = math.radians(lat0), math.radians(lat)
    dp, dl = p2 - p1, math.radians(lon - lon0)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def _kmlab(lat, lon):
    d = _km(lat, lon)
    return ('%.1f km' % d) if d < 10 else ('%d km' % round(d))


def _head(s, W, H, kicker, sub, aria):
    s.append(f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{aria}">')
    s.append(f'<rect width="{W}" height="{H}" fill="{SURF}"/>')
    s.append(txt(40, 32, kicker, 11, GOLD, 'start', '700', 'normal', '1.4'))
    s.append(txt(40, 50, sub, 10.5, GREY, 'start', '400', 'italic'))


# ═════════════════════ 1. the earliest dated ground around Ramallah
def fig_peopling():
    W, H = 860, 560
    lon0, lon1, lat0, lat1 = 34.98, 35.50, 31.74, 32.06
    def P(lat, lon):
        return (66 + (lon - lon0) / (lon1 - lon0) * (W - 150),
                92 + (lat1 - lat) / (lat1 - lat0) * (H - 210))
    # (lat, lon, name, what, km from Ramallah, kind, dx, dy, anchor)
    SITES = [
      (31.9819, 35.0436, 'SHUQBA CAVE', 'Wādī an-Naṭūf — the cave the Natufian is named after.<br>A Neanderthal child’s tooth below; Natufian burials above.', 17.7, 'pal', 10, -16, 'start'),
      (31.8711, 35.4442, 'TELL es-SULTAN', 'Jericho — permanent settlement from c. 9600 BC;<br>the stone tower c. 9000 BC. UNESCO, 2023.', 25.4, 'neo', -14, -46, 'end'),
      (31.8869, 35.2164, 'TELL en-NASBEH', 'A village on the edge of al-Bīra, under two<br>kilometres from Ramallah — Late Chalcolithic / EB I.', 0, 'chal', 14, 40, 'start'),
      (31.9169, 35.2569, 'et-TELL (Ai)', 'Early Bronze town, 3200–2400 BC.<br>No Chalcolithic phase beneath it.', 5.3, 'eb', 13, -26, 'start'),
      (31.9700, 35.3200, 'ʿAIN SAMIYA', 'Intermediate Bronze shaft-tomb cemetery —<br>the ʿAin Samiya goblet. 2300–2000 BC.', 13.2, 'eb', 12, 0, 'start'),
      (31.7933, 35.1533, 'MOTZA', 'A Pre-Pottery Neolithic “megasite”,<br>c. 7000–6400 BC.', 12.5, 'neo', 12, 6, 'start'),
      (31.8058, 35.1044, 'ABU GHOSH', 'Pre-Pottery Neolithic B village.', 13.9, 'neo', -12, -6, 'end'),
    ]
    REF = [(31.8996, 35.2042, 'RAMALLAH'), (31.7780, 35.2354, 'Jerusalem')]
    KIND = {'pal': ('#6D4E9E', 'Palaeolithic &amp; Natufian'),
            'neo': (GREEN, 'Neolithic'),
            'chal': ('#A85210', 'Chalcolithic'),
            'eb': ('#B98A4E', 'Bronze Age')}
    s = []
    _head(s, W, H, 'THE OLDEST GROUND WITHIN A MORNING’S WALK OF RAMALLAH',
          'Every dot is a site with a published excavation and a date. Distances are measured from the centre of Ramallah.',
          'Map of the earliest excavated sites around Ramallah')
    s.append(f'<rect x="40" y="70" width="{W-80}" height="{H-190}" fill="{LAND}" opacity=".45" rx="4"/>')
    # the ridge road, north-south through al-Bira
    ridge = [(31.74, 35.215), (31.80, 35.228), (31.90, 35.222), (32.00, 35.235), (32.06, 35.245)]
    pts = ' '.join('%.1f,%.1f' % P(a, b) for a, b in ridge)
    s.append(f'<polyline points="{pts}" fill="none" stroke="{TAN}" stroke-width="7" opacity=".85"/>')
    rx, ry = P(32.03, 35.238)
    s.append(txt(rx + 8, ry, 'the watershed ridge road', 9, '#9A7A45', 'start', '400', 'italic'))
    # the Jordan rift, east edge
    jx, _ = P(31.9, 35.47)
    s.append(f'<rect x="{jx:.0f}" y="70" width="{40+W-80-jx:.0f}" height="{H-190}" fill="{SEA}" opacity=".55"/>')
    s.append(txt(jx + 10, 88, 'the Jordan valley', 9, '#7C99A6', 'start', '400', 'italic'))
    for la, lo, nm in REF:
        x, y = P(la, lo)
        big = nm == 'RAMALLAH'
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{8 if big else 4}" fill="none" '
                 f'stroke="{INK if big else GREY}" stroke-width="{2 if big else 1.4}"/>')
        if big:
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.5" fill="{INK}"/>')
        s.append(txt(x - (14 if big else 0), y + (4 if big else -9), nm, 11.5 if big else 9.4,
                     INK if big else GREY, 'end' if big else 'middle', '700' if big else '400',
                     'normal' if big else 'italic', '1.2' if big else '0'))
    for la, lo, nm, what, km, k, dx, dy, anc in SITES:
        x, y = P(la, lo)
        col = KIND[k][0]
        rx0, ry0 = P(31.8996, 35.2042)
        s.append(f'<line x1="{rx0:.1f}" y1="{ry0:.1f}" x2="{x:.1f}" y2="{y:.1f}" '
                 f'stroke="{col}" stroke-width=".9" stroke-dasharray="3 3" opacity=".45"/>')
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{col}" stroke="#FFFFFF" stroke-width="1.6"/>')
        s.append(txt(x + dx, y + dy, nm, 9.8, col, anc, '700', 'normal', '.6'))
        s.append(txt(x + dx, y + dy + 12, _kmlab(la, lo), 8.6, GREY, anc, '400', 'italic'))
        for i, ln in enumerate(what.split('<br>')):
            s.append(txt(x + dx, y + dy + 24 + i * 10.5, ln, 8.4, BODY, anc))
    ly = H - 96
    for i, (k, (col, lab)) in enumerate(KIND.items()):
        lx = 44 + i * 196
        s.append(f'<circle cx="{lx}" cy="{ly}" r="5.5" fill="{col}"/>')
        s.append(txt(lx + 12, ly + 4, lab, 9.4, BODY))
    s.append(f'<line x1="40" y1="{ly+18}" x2="{W-40}" y2="{ly+18}" stroke="{RULE}"/>')
    for i, ln in enumerate([
      'The Natufian — the first culture anywhere to build regularly in stone and hold a base camp through the year — is named after a wadi in',
      'the Ramallah and al-Bīra governorate, and its type site is a cave eighteen kilometres from the town. The oldest thing in this book is local.',
      'Note what the map cannot show: these highlands are thinly excavated compared with the coast and the Jordan valley. The blank spaces are gaps in the survey record, not gaps in the past.']):
        s.append(txt(40, ly + 36 + i * 15, ln, 9.8, BODY, 'start', '700' if i < 2 else '400',
                     'normal' if i < 2 else 'italic'))
    s.append('</svg>')
    return ''.join(s)


# ═════════════════════ 2. the land as a tell section — the layering
def fig_layers():
    # (label, dates, who/what, colour, height weight, note)
    L = [
      ('TODAY', '1994 →', 'A Palestinian city and the seat of an authority. 43,880 people.', '#0E5C33', 1.0, ''),
      ('MANDATE, JORDAN, OCCUPATION', '1917–1994', 'The town is tripled by nine thousand refugees in 1948.', '#12703E', 1.0, ''),
      ('OTTOMAN', '1517–1917', 'The Ḥaddādīn arrive c. 1562 and are named in the register of 1596. <b>This is the layer our own family enters.</b>', GREEN, 1.5, 'us'),
      ('MAMLUK', '1250–1517', 'The name Rām Allāh is written down in a sultan’s endowment deed, 1279.', '#2E8B57', 1.0, ''),
      ('CRUSADER &amp; AYYUBID', '1099–1250', 'Franks settle al-Bīra as Magna Mahumeria and leave again — the one arrival that did not stay.', PLUM, 0.85, ''),
      ('EARLY ISLAMIC', '638–1099', 'The rulers change; the villages do not. A church is rebuilt at ʿAbūd in 1058.', '#3E9464', 1.0, ''),
      ('BYZANTINE', '324–638', 'The whole country turns Christian without anybody arriving. Churches at Khirbet et-Tireh, ʿAbūd, Ṭaybeh.', '#5FA97F', 1.1, ''),
      ('ROMAN', '63 BC – 324 AD', 'Gophna is the second city of Judaea. The ridge road is paved and milestoned.', '#79B491', 1.0, ''),
      ('HELLENISTIC &amp; PERSIAN', '539–63 BC', 'Four empires; the same villages. The Samaritans separate and are still here.', '#93C0A4', 1.0, ''),
      ('IRON AGE', '1200–539 BC', 'Philistines on the coast, Moab and Edom across the river, Aramaeans inland — every one absorbed.', '#A9CDB8', 1.15, ''),
      ('BRONZE AGE', '3300–1200 BC', 'et-Tell and ʿAin Samiya. Canaanite city-states write to Egypt in Akkadian. <b>Present-day Lebanese draw more than ninety per cent of their ancestry from this layer.</b>', '#C3D9CB', 1.5, 'base'),
      ('CHALCOLITHIC', '4500–3300 BC', 'A village at Tell en-Naṣba, three kilometres from Ramallah’s centre.', '#D2E2D7', 0.9, ''),
      ('NEOLITHIC', '9600–4500 BC', 'Jericho: permanent settlement, a stone tower, a wall. Motza and Abu Ghosh are day-walks away.', '#DFEAE2', 1.15, ''),
      ('NATUFIAN', '13,000–9600 BC', 'Shuqba cave, in this governorate: the first people here to build in stone and stay. The culture is named after their wadi.', '#E8EFE9', 1.25, 'nat'),
      ('PALAEOLITHIC', 'before 13,000 BC', 'A Neanderthal child’s tooth in the same cave — the southernmost Neanderthal yet identified.', '#EFF2ED', 0.9, ''),
    ]
    W = 860
    unit = 40
    top = 96
    H = top + int(sum(x[4] for x in L) * unit) + 108
    s = []
    _head(s, W, H, 'THE LAND, DRAWN AS A TELL — FIFTEEN THOUSAND YEARS OF LAYERING',
          'Read it from the bottom, the way a section is dug. Nothing here replaces the layer beneath it; every layer is built on the one before.',
          'The history of Palestine drawn as an archaeological section')
    x0, wide = 40, 250
    y = top
    for lab, dates, note, col, wt, tag in L:
        h = wt * unit
        s.append(f'<rect x="{x0}" y="{y:.1f}" width="{wide}" height="{h:.1f}" fill="{col}"/>')
        dark = col in (GREEN, '#0E5C33', '#12703E', '#2E8B57', PLUM, '#3E9464')
        tc = '#FFFFFF' if dark else INK
        s.append(txt(x0 + 12, y + h / 2 - 2, lab, 9.2, tc, 'start', '700', 'normal', '.9'))
        s.append(txt(x0 + 12, y + h / 2 + 11, dates, 9, tc, 'start', '400', 'italic'))
        if tag == 'us':
            s.append(f'<rect x="{x0}" y="{y:.1f}" width="{wide}" height="{h:.1f}" fill="none" stroke="{GOLD}" stroke-width="3"/>')
            s.append(txt(x0 + wide + 10, y + 13, '◀ WE ARRIVE HERE', 9.4, GOLD, 'start', '700', 'normal', '1.1'))
            s.append(txt(x0 + wide + 10, y + 27, note.replace('<b>', '').replace('</b>', ''), 9.6, BODY))
        else:
            nl = max(1, int(h // 13))
            wrapped = _wrap(note.replace('<b>', '').replace('</b>', ''), 74)[:nl]
            for i, ln in enumerate(wrapped):
                s.append(txt(x0 + wide + 10, y + h / 2 - 3 - (len(wrapped) - 1) * 6 + i * 12, ln, 9.6,
                             INK if tag in ('base', 'nat') else BODY, 'start',
                             '700' if tag in ('base', 'nat') else '400'))
        s.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{W-40}" y2="{y:.1f}" stroke="#FFFFFF" stroke-width=".8" opacity=".7"/>')
        y += h
    s.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{W-40}" y2="{y:.1f}" stroke="{RULE}"/>')
    for i, ln in enumerate([
      'Fifteen thousand years of human presence in this district, and not one layer in which the people of this land were replaced by another people.',
      'The family arrives four layers from the top, into a district lived in — site by site, not always the same site — for more than eleven thousand years.',
      'Layer thicknesses are drawn for legibility, not to scale in time. Every date is calibrated and sourced in the entries around this figure.']):
        s.append(txt(40, y + 24 + i * 16, ln, 10.2, BODY, 'start', '700' if i < 2 else '400',
                     'normal' if i < 2 else 'italic'))
    s.append('</svg>')
    return ''.join(s)


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


# ═════════════════════ 3. the branch at Eber — Genesis 10 and 11
def fig_branch():
    # Sized for reading, not for fitting. The names carry the argument, so they
    # are set at body size; the four notes are wrapped rather than run off the
    # right edge of the plate, which is what they used to do.
    W = 860
    cx = W / 2
    trunk = ['Adam', 'Seth', 'Enosh', 'Kenan', 'Mahalalel', 'Jared', 'Enoch', 'Methuselah',
             'Lamech', 'Noah', 'Shem', 'Arpachshad', '(Kainan)', 'Shelah', 'ʿĀBIR / EBER']
    left = [('Peleg', 'Gen 11:18'), ('Reu', 'Gen 11:20'), ('Serug', 'Gen 11:22'),
            ('Nahor', 'Gen 11:24'), ('Terah', 'Gen 11:26'), ('ABRAHAM', 'Gen 11:26'),
            ('Isaac', ''), ('Jacob', ''), ('Levi', 'Exod 6:16'), ('Kohath', 'Exod 6:18'),
            ('Amram', 'Exod 6:20'), ('MOSES', 'Exod 6:20')]
    right = [('Almodad', ''), ('Sheleph', ''), ('HAZARMAVETH', '= Ḥaḍramawt'), ('Jerah', ''),
             ('Hadoram', ''), ('Uzal', ''), ('Diklah', ''), ('Obal', ''), ('Abimael', ''),
             ('SHEBA', '= Sabaʾ'), ('Ophir', 'disputed'), ('Havilah', 'disputed'), ('Jobab', '')]
    NOTES = [
      ('The split is three generations after the Flood — four in the Septuagint, which inserts Kainan — and six generations before Abraham. Moses is seven names from Abraham, and stands on the other branch.', '700', 'normal'),
      ('So the answer to “where do we leave the line of Abraham and Moses?” is: we never joined it. We share Noah, Shem and Eber with them, and part company at Eber’s two sons.', '700', 'normal'),
      ('Ḥaḍramawt and Sabaʾ are secure; Ophir, Havilah and Uzal are generally placed in South Arabia too, though argued over. Every identification that can be made points to one country.', '400', 'italic'),
      ('The Masoretic text gives fourteen names from Adam to Eber; the Septuagint gives fifteen, inserting Kainan, and Luke 3:36 follows the Septuagint.', '400', 'italic')]

    TR, BR = 25, 24                              # row pitch, trunk and branches
    ty = 96
    by = ty + 34 + (len(trunk) - 1) * TR + 16    # the branch point
    ly = by + 66
    nlines = [_wrap(n, 128) for n, _, _ in NOTES]
    yb = ly + 34 + (max(len(left), len(right)) - 1) * BR + 40
    H = yb + 26 + sum(len(L) for L in nlines) * 17 + 22

    s = []
    _head(s, W, H, 'THE BRANCH AT EBER — WHERE THIS LINE LEAVES ABRAHAM’S',
          'Genesis 10:25 gives Eber two sons. One is the line to Abraham and Moses. The other is ours. We do not descend from Abraham — we branch off six generations before him.',
          'Genesis genealogy showing the split at Eber between Peleg and Joktan')

    # ── the shared trunk, Adam to Eber
    s.append(f'<rect x="{cx-150:.0f}" y="{ty-10}" width="300" height="{34+(len(trunk)-1)*TR+18}" '
             f'fill="#D5E9DF" stroke="#A9CDB8" rx="7"/>')
    s.append(txt(cx, ty + 9, 'GENESIS 5 AND 11 — THE SHARED TRUNK', 9.6, '#2F6B48', 'middle', '700', 'normal', '1.2'))
    for i, n in enumerate(trunk):
        last = i == len(trunk) - 1
        lxx = n.startswith('(')
        s.append(txt(cx, ty + 34 + i * TR, esc(n), 14 if last else 12.4,
                     GREY if lxx else INK, 'middle', '700' if last else '400',
                     'italic' if lxx else 'normal'))
        if lxx:
            s.append(txt(cx + 104, ty + 34 + i * TR, 'LXX only', 8.8, GREY, 'start', '400', 'italic'))

    # ── the fork
    s.append(f'<line x1="{cx:.0f}" y1="{by}" x2="{cx:.0f}" y2="{by+28}" stroke="{GOLD}" stroke-width="2.6"/>')
    s.append(f'<line x1="{cx-258:.0f}" y1="{by+28}" x2="{cx+258:.0f}" y2="{by+28}" stroke="{GOLD}" stroke-width="2.6"/>')
    for sx in (cx - 258, cx + 258):
        s.append(f'<line x1="{sx:.0f}" y1="{by+28}" x2="{sx:.0f}" y2="{by+56}" stroke="{GOLD}" stroke-width="2.6"/>')
    s.append(f'<rect x="{cx-186:.0f}" y="{by+18}" width="372" height="20" fill="{SURF}"/>')
    s.append(txt(cx, by + 33, 'GENESIS 10:25 — “and the name of his brother was Joktan”', 10.4, GOLD, 'middle', '700', 'italic'))

    # ── the two branches
    for names, ox, fill, edge, head, accent, big_fs in (
            (left,  -258, '#EDE7F4', '#C7B8DE', 'PELEG’S LINE — NOT OURS',     '#4A3A7A', 13.6),
            (right,  258, '#F6EEDF', '#E0CFAE', 'JOKTAN’S THIRTEEN SONS — OURS', '#8A5A1E', 13.2)):
        bxc = cx + ox
        s.append(f'<rect x="{bxc-144:.0f}" y="{ly-12}" width="288" height="{34+(len(names)-1)*BR+20}" '
                 f'fill="{fill}" stroke="{edge}" rx="7"/>')
        s.append(txt(bxc, ly + 7, head, 9.6, accent, 'middle', '700', 'normal', '1.2'))
        for i, (n, ref) in enumerate(names):
            bigname = n.isupper()
            s.append(txt(bxc - 10, ly + 34 + i * BR, esc(n), big_fs if bigname else 12.2,
                         accent if bigname else INK, 'end', '700' if bigname else '400'))
            if ref:
                s.append(txt(bxc + 4, ly + 34 + i * BR, esc(ref), 9.2,
                             GREY if ref == 'disputed' else accent, 'start', '400',
                             'italic' if ref.startswith(('Gen', 'Exod', 'dis')) else 'normal'))

    s.append(f'<line x1="40" y1="{yb}" x2="{W-40}" y2="{yb}" stroke="{RULE}"/>')
    yy = yb + 24
    for lines, (_, wt, st) in zip(nlines, NOTES):
        for ln in lines:
            s.append(txt(40, yy, esc(ln), 10.6, BODY if wt == '700' else GREY, 'start', wt, st))
            yy += 17
        yy += 5
    s.append('</svg>')
    return ''.join(s)


# ═════════════════════ the ladder that fills in as you read ═══════════
# The thirty-six named generations, set out as the family chart sets them out,
# and printed at the head of every era with the generations reached so far in
# full colour and the rest still ghosted. It grows as the book is read.
_LADDER_KIND = {'s': ('#D5E9DF', '#A9CDB8', INK), 'j': ('#8FBFA6', '#3E9464', INK),
                'c': ('#A9CDB8', '#79B491', INK), 'g': ('#79B491', '#3E9464', INK),
                'a': ('#3E9464', '#007A3D', '#FFFFFF'), 'v': ('#FDF6EC', '#E0CFAE', '#8A5A1E'),
                'n': ('#F6EEDF', '#C9A96A', INK),
                'f': ('#DCEDE3', '#7FB79A', INK),
                'd': (GREEN, GREEN, '#FFFFFF')}

# the chart's own English, shortened to fit a column and lightly regularised
_NAMES = {
 1: 'Adam & Eve', 2: 'Sheath (Seth)', 3: 'Anoosh (Enosh)', 4: 'Qinan (Kenan)',
 5: 'Mihlaʾel', 6: 'Elizad (Jared)', 7: 'Akhnoukh (Enoch)', 8: 'Matoushlekh',
 9: 'Noah', 10: 'Sam (Shem)', 11: 'Arfakhshid', 12: 'Shaleikh (Shelah)',
 13: 'ʿĀbir (Eber)', 14: 'Qaḥṭān (Joktan)', 15: 'Yaʿrub', 16: 'Yashjub',
 17: 'Sabaʾ', 18: 'Kahlān', 19: 'Zayd', 20: 'Mālik', 21: 'Nabt', 22: 'al-Ghawth',
 23: 'al-Azd', 24: 'Māzin al-Azd', 25: 'Thaʿlaba b. Māzin', 26: 'ʿAmr al-Qays',
 27: 'Ḥāritha al-Ghiṭrīf', 28: 'ʿĀmir Māʾ al-Samāʾ', 29: 'ʿAmr Muzayqiyāʾ',
 30: 'Jafna', 31: 'Thaʿlaba b. Jafna', 32: 'al-Ḥārith b. Thaʿlaba',
 33: 'Jabala b. al-Ḥārith', 34: 'al-Ḥārith b. Jabala', 35: 'UNKNOWN — the void',
 36: 'Rāshid al-Ḥaddādīn',
}
# retained for fig_peopling and the older figures; the ladder uses _LGLOSS
_GLOSS = {13: 'the branch', 14: 'the join', 29: 'the name enters', 34: '528–569, in Greek',
          35: '931 years', 36: 'fl. c. 1500'}

# the chart prints the full nasab; a column will not hold it, so the Arabic is
# shortened to the distinguishing element and the chart is cited for the rest
_AR = {29: 'عمرو مزيقياء', 30: 'جفنة', 31: 'ثعلبة بن جفنة', 32: 'الحارث بن ثعلبة',
       33: 'جبلة بن الحارث', 34: 'الحارث بن جبلة', 35: 'مجهول', 36: 'راشد الحدادين',
       25: 'ثعلبة بن مازن', 26: 'عمرو القيس', 27: 'حارثة الغطريف', 28: 'عامر ماء السماء',
       24: 'مازن الأزد', 2: 'شيث', 3: 'أنوش', 4: 'قينان', 5: 'مهلائيل', 6: 'إليزاد',
       7: 'أخنوخ', 8: 'متوشلخ', 9: 'نوح', 10: 'سام', 11: 'أرفخشد', 12: 'شالخ',
       13: 'عابر', 14: 'قحطان', 15: 'يعرب', 16: 'يشجب', 17: 'سبأ', 18: 'كهلان',
       19: 'زيد', 20: 'مالك', 21: 'نبت', 22: 'الغوث', 23: 'الأزد'}


# ── the ladder's own list. It is NOT the thirty-six rows of the co-authors'
# earlier chart.
#
# That chart's generation 35 is one line standing for the 931 years between
# al-Ḥārith's death in 569 and Rāshid's floruit about 1500. At thirty years to a
# generation that stretch is thirty-one generations, not one — and not the
# forty-five the chart prints. So the ladder shows it as thirty-one, numbered 35
# to 65, of which the last, generation 65, carries a name: Ṣaqr, from the Karak
# wheel. Rāshid is therefore generation 66 of sixty-six, of which thirty-six have
# names and thirty have none.
_LADDER = None


def _ladder_rows():
    global _LADDER
    if _LADDER is not None:
        return _LADDER
    import build_recon as _R
    rows = []
    for n, en, ar, k in _R.GENS[:34]:
        rows.append((str(n), _NAMES[n], _AR.get(n, ar), k, n))
    rows.append(('35–64', 'thirty, no names', '٣٠ جيلاً بلا اسم', 'v', 35))
    rows.append(('65', 'Ṣaqr', 'صقر', 'n', 65))
    rows.append(('66', 'Rāshid al-Ḥaddādīn', 'راشد الحدادين', 'd', 66))
    # ── and on to today. Below Rāshid the line stops being one man to a row:
    # it is five sons, then eight clans, then a town. The tail is kept because
    # a line that stops at 1500 looks like a line that ended.
    rows.append(('67', 'his five sons', 'أبناؤه الخمسة', 'f', 67))
    rows.append(('68', 'the eight clans', 'الحمايل الثماني', 'f', 68))
    rows.append(('69–83', 'fifteen, all in documents', '١٥ جيلاً موثقاً', 'f', 69))
    rows.append(('84', 'this morning', 'اليوم', 'f', 84))
    _LADDER = rows
    return rows


_LGLOSS = {13: 'the branch', 14: 'the join', 29: 'the name enters',
           34: '528–569, in Greek', 35: '931 years', 65: 'one witness', 66: 'fl. c. 1500'}


def fig_ladder(upto, W=780):
    """`upto` is the last generation the line has reached, in this book's own
    numbering of sixty-six — not the chart's thirty-six."""
    rows_l = _ladder_rows()
    rows, cols = 11, 4
    cw = (W - 16) / cols
    rh = 21.5
    top = 42
    H = top + rows * rh + 44
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" '
         f'aria-label="The named line: generation {upto} of sixty-six reached">']
    s.append(txt(8, 15, 'THE NAMED LINE, SO FAR', 8.4, GOLD, 'start', '700', 'normal', '1.5'))
    cur = next((r for r in rows_l if r[4] == upto), None)
    if cur is None:
        head = 'past the end of the line'
    elif cur[3] == 'v':
        head = 'generations 35–64 of 66 — no name survives for any of them'
    elif cur[3] == 'f':
        head = f'past Rāshid — generation {cur[0]}, {cur[1]}'
    else:
        head = f'generation {upto} of 66 — {cur[1]}'
    s.append(txt(8, 31, head, 10.4, INK, 'start', '700'))
    s.append(txt(W - 8, 31, 'in colour = reached · faint = still ahead', 8.6, FOLIO, 'end', '400', 'italic'))
    s.append(f'<line x1="8" y1="{top-8}" x2="{W-8}" y2="{top-8}" stroke="{RULE}"/>')
    for idx, (lab, en_s, ar_s, k, gnum) in enumerate(rows_l):
        c, r = divmod(idx, rows)
        x = 8 + c * cw
        y = top + r * rh
        fill, edge, tc = _LADDER_KIND[k]
        on = gnum <= upto
        op = '1' if on else '.2'
        dash = ' stroke-dasharray="3 2"' if k == 'n' else ''
        s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cw-6:.1f}" height="{rh-2.5:.1f}" '
                 f'fill="{fill}" stroke="{edge}" stroke-width=".7"{dash} rx="2.5" opacity="{op}"/>')
        if k == 'v' and on:
            s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cw-6:.1f}" height="{rh-2.5:.1f}" '
                     f'fill="url(#lhatch)" rx="2.5"/>')
        if gnum == upto:
            s.append(f'<rect x="{x-1.6:.1f}" y="{y-1.6:.1f}" width="{cw-2.8:.1f}" '
                     f'height="{rh+0.6:.1f}" fill="none" stroke="{GOLD}" stroke-width="2" rx="3.5"/>')
        nfs = 7.6 if len(lab) <= 2 else 6.6
        s.append(f'<text x="{x+7:.1f}" y="{y+13.4:.1f}" font-size="{nfs}" fill="{tc}" '
                 f'font-family="Times New Roman, Times, serif" opacity="{op}">{esc(lab)}</text>')
        xoff = 21 if len(lab) <= 2 else 34
        avail = cw - 6 - xoff - 62
        fs = 9.2 if len(en_s) <= 17 else (8.4 if len(en_s) <= 21 else 7.7)
        s.append(f'<text x="{x+xoff:.1f}" y="{y+13.4:.1f}" font-size="{fs}" fill="{tc}" '
                 f'font-weight="{"700" if gnum in _LGLOSS else "400"}" '
                 f'font-family="Times New Roman, Times, serif" opacity="{op}">{esc(en_s)}</text>')
        afs = 9.2 if len(ar_s) <= 18 else 7.4
        s.append(f'<text x="{x+cw-11:.1f}" y="{y+13.6:.1f}" font-size="{afs}" fill="{tc}" '
                 f'text-anchor="end" font-family="Times New Roman, Times, serif" '
                 f'xml:lang="ar" opacity="{op if on else ".14"}">{ar_s}</text>')
    yb = top + rows * rh + 6
    s.append(f'<line x1="8" y1="{yb}" x2="{W-8}" y2="{yb}" stroke="{RULE}"/>')
    for i, ln in enumerate(_wrap('Read down each column. Sixty-six generations from Adam to Rāshid, thirty-six of them named; the dashed cell has one witness only. Below Rāshid the line stops being one man to a row — it is five sons, eight clans and a town — and every step of it is in documents.', 150)):
        s.append(txt(8, yb + 16 + i * 12, ln, 8.6, GREY, 'start', '400', 'italic'))
    s.append('<defs><pattern id="lhatch" width="5" height="5" patternTransform="rotate(45)" '
             'patternUnits="userSpaceOnUse"><line x1="0" y1="0" x2="0" y2="5" '
             'stroke="#E0CFAE" stroke-width="1.2" opacity=".7"/></pattern></defs>')
    s.append('</svg>')
    return ''.join(s)


# ═══════════ the Karak wheel, redrawn so it can be read ═══════════════
def fig_karak_wheel():
    """The El-Ḥaddādīn of Karak chart, redrawn.

    The original is a hand-drawn wheel of about one hundred and sixty names in
    six concentric rings, every label set on the curve. Its core — the hub, the
    two sons, and the two lines that leave it — is what bears on Rāshid, and that
    core is drawn here straight, at a size that can be read. Nothing is added and
    nothing is corrected; the outer rings, which carry the modern Karak clan, are
    summarised rather than transcribed.
    """
    W, H = 860, 548
    s = []
    _head(s, W, H, 'THE KARAK WHEEL, REDRAWN — WHAT IT SAYS ABOUT RĀSHID',
          'The hub of the Ḥaddādīn chart of al-Karak, set straight. Ṣaqr at the centre; one son keeps Karak, one son goes to Ramallah.',
          'The Karak Haddadin genealogical wheel redrawn as two horizontal lines of descent from Saqr')

    BW, BH, GAP = 76, 38, 10
    PITCH = BW + GAP
    hubx, huby = 44, 196
    uy, ly = 96, 306

    def cell(x, y, en, ar, fill='#FFFFFF', edge='#B4A88C', tc=INK, fs=10.6, afs=10):
        s.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{BW}" height="{BH}" fill="{fill}" '
                 f'stroke="{edge}" stroke-width="1.3" rx="3"/>')
        s.append(txt(x + BW / 2, y + 15, esc(en), fs, tc, 'middle', '700'))
        s.append(f'<text x="{x+BW/2:.0f}" y="{y+30:.0f}" font-size="{afs}" fill="{tc}" '
                 f'text-anchor="middle" font-family="Times New Roman, Times, serif" '
                 f'xml:lang="ar">{ar}</text>')

    def link(x1, y1, x2, y2, col='#3E9464', w=2.2):
        s.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" '
                 f'stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>')

    # ── the hub
    s.append(f'<rect x="{hubx-4}" y="{huby-4}" width="{BW+8}" height="{BH+8}" '
             f'fill="none" stroke="{GOLD}" stroke-width="2.2" rx="6"/>')
    cell(hubx, huby, 'ṢAQR', 'صقر', fill='#EFF6F1', edge='#3E9464', fs=11.6)
    s.append(txt(hubx + BW / 2, huby + BH + 16, '“ عام ١٥٦١ ”', 10.4, '#8A5A1E', 'middle', '700'))
    s.append(txt(hubx + BW / 2, huby + BH + 29, 'the year at the hub', 8.6, GREY, 'middle', '400', 'italic'))

    # ── the elbow
    ex = hubx + BW + 18
    tx = ex + 20
    link(hubx + BW, huby + BH / 2, ex, huby + BH / 2)
    link(ex, uy + BH / 2, ex, ly + BH / 2)
    link(ex, uy + BH / 2, tx, uy + BH / 2)
    link(ex, ly + BH / 2, tx, ly + BH / 2)

    # ── the upper track: Ṣabra keeps Karak
    s.append(txt(tx, uy - 30, 'ONE SON KEEPS KARAK', 9.2, '#3E9464', 'start', '700', 'normal', '1.2'))
    s.append(txt(tx, uy - 16, 'the line the diwan then traces, generation by generation, to the present day',
                 9.4, GREY, 'start', '400', 'italic'))
    KARAK = [('Ṣabra', 'صبرة'), ('Ṣaqr', 'صقر'), ('Ṣabra', 'صبرة'), ('ʿĪsā', 'عيسى'),
             ('Jiryis', 'جريس'), ('Mūsā', 'موسى'), ('Sālim', 'سالم')]
    for i, (en, ar) in enumerate(KARAK):
        x = tx + i * PITCH
        if i:
            link(x - GAP, uy + BH / 2, x, uy + BH / 2)
        cell(x, uy, en, ar, fill='#EFF6F1', edge='#79B491')
    xe = tx + (len(KARAK) - 1) * PITCH + BW
    link(xe, uy + BH / 2, xe + 12, uy + BH / 2, col=GREY, w=1.4)
    s.append(txt(xe + 16, uy + 12, 'and about', 8.8, GREY, 'start', '400', 'italic'))
    s.append(txt(xe + 16, uy + 24, '150 more', 9.4, BODY, 'start', '700'))
    s.append(txt(xe + 16, uy + 35, 'names', 9.4, BODY, 'start', '700'))

    # ── the lower track: Rāshid goes to Ramallah
    s.append(txt(tx, ly - 30, 'ONE SON GOES TO RAMALLAH', 9.2, '#8A5A1E', 'start', '700', 'normal', '1.2'))
    s.append(txt(tx, ly - 16, 'the chart writes his destination under his name, records his five sons, and stops there',
                 9.4, GREY, 'start', '400', 'italic'))
    cell(tx, ly, 'RĀSHID', 'راشد', fill='#F6EEDF', edge=GOLD, fs=11.6)
    s.append(f'<rect x="{tx+BW+6}" y="{ly+8}" width="56" height="22" fill="{GOLD}" rx="3"/>')
    s.append(f'<text x="{tx+BW+34}" y="{ly+24}" font-size="10.4" fill="#FFFAF0" text-anchor="middle" '
             f'font-family="Times New Roman, Times, serif" xml:lang="ar">رام الله</text>')
    SONS = [('Ḥaddād', 'حداد'), ('Ibrāhīm', 'ابراهيم'), ('Jiryis', 'جريس'),
            ('Shuqayr', 'شقير'), ('Ḥasan', 'حسن')]
    sx = tx + BW + 76
    link(tx + BW + 62, ly + BH / 2, sx, ly + BH / 2, col=GOLD, w=2.2)
    for i, (en, ar) in enumerate(SONS):
        x = sx + i * PITCH
        if i:
            link(x - GAP, ly + BH / 2, x, ly + BH / 2, col=GOLD, w=1.5)
        cell(x, ly, en, ar, edge=GOLD, tc='#8A5A1E')
    s.append(f'<line x1="{sx}" y1="{ly+BH+9}" x2="{sx+4*PITCH+BW}" y2="{ly+BH+9}" '
             f'stroke="{GOLD}" stroke-width="1.2"/>')
    s.append(txt(tx, ly + BH + 26, 'The five fifths of Ramallah — the same five names, in the same order, as the',
                 9.8, BODY, 'start', '700'))
    s.append(txt(tx, ly + BH + 39, 'Ramallah tradition’s own division of the land among Rāshid’s sons.',
                 9.8, BODY, 'start', '700'))

    yb = H - 104
    s.append(f'<line x1="40" y1="{yb}" x2="{W-40}" y2="{yb}" stroke="{RULE}"/>')
    yy = yb + 20
    for txtline, wt, st, fs in [
        ('The Karak side, writing about itself, names Rāshid’s father, his brother, his destination and his five sons.', '700', 'normal', 10.4),
        ('Redrawn from the radial chart in the Ḥaddādīn of al-Karak presentation, plate 84. The slide credits “Dr Munther Haddadeen, El-Haddadeen Tribe, Origins and Branches, Warda Books, 2025”; that attribution is wrong on author, publisher and year — see the note in the text.', '400', 'italic', 9.4),
        ('The original is a wheel of about one hundred and sixty names in six rings. Its outer rings carry the modern Karak clan and are not transcribed here; nothing in the core has been altered.', '400', 'italic', 9.4)]:
        for ln in _wrap(txtline, 150 if wt == '700' else 166):
            s.append(txt(40, yy, esc(ln), fs, BODY if wt == '700' else GREY, 'start', wt, st))
            yy += 14
    s.append('</svg>')
    return ''.join(s)


# ═════════════ the two registers, name against name ══════════════════
def fig_registers():
    """John Mogannam's two transliterations set side by side and counted.

    The point of the plate is one number: how many of the thirty-six households
    the register finds at Bayt Jālā in 1553 are still there, under the same name
    and the same father, in the Ramallah register of 1562.
    """
    import build_defters as DF
    W = 860
    A = DF.BAYT_JALA_1553
    B = DF.RAMALLAH_1562_CHRISTIAN
    hits = {(DF._norm(n), DF._norm(f)) for n, f in DF.matches()}

    LH = 14.6
    arows, acols = 18, 2
    brows, bcols = 24, 3
    top = 112
    H = top + max(arows, brows) * LH + 132
    s = []
    _head(s, W, H, 'THE SAME PEOPLE, NINE YEARS APART',
          'Every household head the Ottoman clerks wrote down at Bayt Jālā in 1553 and at Ramallah in 1562 — and the nineteen who appear in both, name and father alike.',
          'The 1553 Bayt Jala and 1562 Ramallah register names compared')

    def panel(x, w, title, sub, items, rows, cols, kind):
        s.append(f'<rect x="{x}" y="{top-34}" width="{w}" height="{rows*LH+46}" '
                 f'fill="#FFFFFF" stroke="{RULE}" rx="4"/>')
        s.append(txt(x + 12, top - 18, title, 9.4, GOLD, 'start', '700', 'normal', '1.2'))
        s.append(txt(x + 12, top - 6, sub, 8.6, GREY, 'start', '400', 'italic'))
        cw = (w - 20) / cols
        for i, it in enumerate(items):
            n, f = it[0], it[1]
            bach = len(it) > 2 and it[2]
            c, r = divmod(i, rows)
            cx = x + 10 + c * cw
            cy = top + 12 + r * LH
            key = (DF._norm(n), DF._norm(f))
            on = key in hits
            if on:
                s.append(f'<rect x="{cx-3:.1f}" y="{cy-9:.1f}" width="{cw-6:.1f}" height="{LH-1:.1f}" '
                         f'fill="#E4F0E8" stroke="#A9CDB8" stroke-width=".6" rx="2"/>')
            col = '#1A6B3C' if on else (FOLIO if bach else INK)
            nm = f'{n} · {f}'
            if bach:
                nm += ' ✻'
            fs = 8.2 if len(nm) <= 26 else (7.4 if len(nm) <= 32 else 6.8)
            s.append(txt(cx, cy, esc(nm), fs, col, 'start', '700' if on else '400'))
        return x + w

    panel(40, 288, 'BAYT JĀLĀ · 1553–54 · REGISTER 289',
          'the 36 Christian households the clerk calls al-Kasābra', A, arows, acols, 'a')
    panel(348, 472, 'RAMALLAH · 1562–63 · REGISTER 516',
          '63 Christian households and 8 bachelors, nine years later', B, brows, bcols, 'b')

    yb = top + max(arows, brows) * LH + 26
    s.append(f'<line x1="40" y1="{yb}" x2="{W-40}" y2="{yb}" stroke="{RULE}"/>')
    stats = [('19 of 36', 'households at Bayt Jālā reappear at Ramallah, same name and same father', GREEN),
             ('0', 'household heads at Ramallah in 1562 are named Rāshid', RUST),
             ('0', 'household heads at Ramallah in 1562 are the son of a Rāshid', RUST)]
    sx = 40
    for big, lab, col in stats:
        s.append(txt(sx, yb + 26, big, 15, col, 'start', '700'))
        for j, ln in enumerate(_wrap(lab, 34)):
            s.append(txt(sx, yb + 40 + j * 11.5, ln, 8.8, BODY, 'start'))
        sx += 268
    s.append(txt(40, H - 30, '✻ marks the bachelors. John Mogannam flags seven; the register’s own total is eight.', 8.8, GREY, 'start', '400', 'italic'))
    s.append(txt(40, H - 16, 'Transliterated by John Mogannam from Registers 289 and 516; query marks and alternative readings are his, and are kept.', 8.8, GREY, 'start', '400', 'italic'))
    s.append('</svg>')
    return ''.join(s)


# ═════════════════════ 6. the terraces, and the towers standing in them
def _rng(seed):
    """A tiny deterministic generator, so the plate is byte-identical every build."""
    st = [seed & 0xFFFFFFFF]
    def nxt(lo, hi):
        st[0] = (1103515245 * st[0] + 12345) & 0x7FFFFFFF
        return lo + (st[0] >> 8) % max(1, int((hi - lo) * 100) + 1) / 100.0
    return nxt


def fig_terraces():
    """A hillside in section: the dry-stone terraces and one watchtower.

    The plate carries one count — 167 towers over some three thousand dunums in
    al-Tireh quarter and ʿAin Qinia village — and one fact about how they are
    built, which is that they are not built with anything.
    """
    W, H = 860, 548
    s = []
    _head(s, W, H, 'THE OLDEST TECHNOLOGY IN THIS DISTRICT, AND IT IS STILL IN USE',
          'A hillside above Ramallah drawn in section: the dry-stone terraces, and one of the '
          'one hundred and sixty-seven watchtowers still standing in al-Tireh and ʿAin Qinia.',
          'A cross-section of a terraced hillside above Ramallah with a dry-stone watchtower, '
          'a cutaway of its corbelled roof, and the three watch seasons of the year')

    rnd = _rng(1562)
    STONE, EDGE = '#EDE7DA', '#CFC6B2'
    xL, xR, yB, yT = 56, 540, 336, 120
    N = 7
    sw, sh = (xR - xL) / N, (yB - yT) / N

    # ── the ground itself, drawn as a stepped profile and filled
    prof = [(xL - 16, yB + 18), (xL - 16, yB)]
    for i in range(N):
        x0 = xL + i * sw
        y = yB - i * sh
        prof += [(x0, y), (x0 + sw, y), (x0 + sw, y - sh)]
    prof += [(xR + 24, yT - sh), (xR + 24, yB + 18)]
    s.append('<polygon points="' + ' '.join(f'{x:.1f},{y:.1f}' for x, y in prof) +
             f'" fill="{LAND}" stroke="none"/>')

    # ── the risers: every one of them a wall of stones fitted without mortar
    for i in range(N):
        xw = xL + (i + 1) * sw
        ytop, ybot = yB - (i + 1) * sh, yB - i * sh
        cy = ybot
        while cy > ytop + 1.0:
            ch = min(rnd(4.6, 6.6), cy - ytop)
            cx = xw - 13 - rnd(0.0, 3.0)
            while cx < xw + 13:
                bw = rnd(5.5, 11.0)
                s.append(f'<rect x="{max(cx, xw-13):.1f}" y="{cy-ch:.1f}" '
                         f'width="{min(bw, xw+13-max(cx, xw-13)):.1f}" '
                         f'height="{ch:.1f}" fill="{STONE}" stroke="{EDGE}" stroke-width=".55"/>')
                cx += bw
            cy -= ch
        s.append(f'<line x1="{xw:.1f}" y1="{ytop:.1f}" x2="{min(xw+sw, xR+24):.1f}" '
                 f'y2="{ytop:.1f}" stroke="{TAN}" stroke-width="1.1"/>')

    # ── olives on the treads
    def olive(x, y, r=9.0):
        s.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{y-r*0.9:.1f}" '
                 f'stroke="{BODY}" stroke-width="1.4"/>')
        for a in (-0.9, 0.0, 0.9):
            s.append(f'<circle cx="{x + a*r*0.60:.1f}" cy="{y - r*1.22 - (0 if a else 3):.1f}" '
                     f'r="{(0.78 if a else 1.0)*r*0.60:.1f}" fill="#DDE6D8" '
                     f'stroke="#8FA98C" stroke-width=".7"/>')
    for i, k in ((0, 0.40), (1, 0.32), (1, 0.70), (3, 0.28), (3, 0.66),
                 (4, 0.42), (5, 0.34), (5, 0.72), (6, 0.48)):
        olive(xL + (i + k) * sw, yB - i * sh)

    # ── the tower, standing on the third terrace
    tx, ty = xL + 2.46 * sw, yB - 2 * sh
    tw, th = 33.0, 40.0
    s.append(f'<path d="M{tx-tw/2:.1f} {ty:.1f} L{tx-tw/2:.1f} {ty-th:.1f} '
             f'Q{tx:.1f} {ty-th-18:.1f} {tx+tw/2:.1f} {ty-th:.1f} L{tx+tw/2:.1f} {ty:.1f} Z" '
             f'fill="{STONE}" stroke="{GREY}" stroke-width="1.1"/>')
    cy = ty
    while cy > ty - th:
        cx = tx - tw / 2 - rnd(0.0, 3.0)
        while cx < tx + tw / 2:
            bw = rnd(4.5, 8.5)
            xa = max(cx, tx - tw / 2)
            s.append(f'<rect x="{xa:.1f}" y="{cy-5.0:.1f}" '
                     f'width="{min(bw, tx+tw/2-xa):.1f}" height="5.0" fill="none" '
                     f'stroke="{EDGE}" stroke-width=".55"/>')
            cx += bw
        cy -= 5.0
    s.append(f'<path d="M{tx-5.5:.1f} {ty:.1f} L{tx-5.5:.1f} {ty-14:.1f} Q{tx:.1f} {ty-20:.1f} '
             f'{tx+5.5:.1f} {ty-14:.1f} L{tx+5.5:.1f} {ty:.1f} Z" fill="{DARK}" opacity=".82"/>')
    s.append(txt(tx, ty - th - 30, 'a watchtower', 9.2, PLUM, 'middle', '700'))
    s.append(txt(tx, ty - th - 19, '<tspan class="ar">قصر · منطرة</tspan>', 9.6, PLUM, 'middle'))
    s.append(f'<line x1="{tx:.1f}" y1="{ty-th-15:.1f}" x2="{tx:.1f}" y2="{ty-th-24:.1f}" '
             f'stroke="{PLUM}" stroke-width=".8"/>')

    s.append(txt(xR + 22, yT - sh + 16, 'the ridge, and the village on it', 9.0, GREY, 'end', '400', 'italic'))
    s.append(txt(xL, yB + 38, 'Every riser is a wall; every tread is a field.', 9.4, GOLD, 'start', '700'))
    s.append(txt(xL, yB + 52,
                 'The walls are called <tspan class="ar">سناسل</tspan>, and nothing holds them up but their own weight.',
                 8.8, GREY, 'start', '400', 'italic'))

    # ── the cutaway, right-hand panel
    px, py, pw, ph = 588, 94, 232, 268
    s.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="#FFFFFF" '
             f'stroke="{RULE}" rx="4"/>')
    s.append(txt(px + 12, py + 20, 'HOW THE ROOF CLOSES', 9.4, GOLD, 'start', '700', 'normal', '1.2'))
    s.append(txt(px + 12, py + 33, 'a section through the hut — no mortar anywhere in it',
                 8.4, GREY, 'start', '400', 'italic'))
    cx0, base = px + pw / 2, py + 168
    OUT, CHAM = 47.0, 27.0
    courses, chh = 12, 11.0
    for i in range(courses):
        t = i / (courses - 1.0)
        inner = CHAM * (1.0 - t ** 2.3)
        yy = base - i * chh
        for sgn in (-1, 1):
            xa = cx0 + sgn * inner
            xb = cx0 + sgn * OUT
            lo, hi = min(xa, xb), max(xa, xb)
            cx = lo
            while cx < hi - 0.5:
                bw = min(rnd(7.0, 16.0), hi - cx)
                s.append(f'<rect x="{cx:.1f}" y="{yy-chh:.1f}" width="{bw:.1f}" '
                         f'height="{chh-1:.1f}" fill="{STONE}" stroke="{GREY}" '
                         f'stroke-width=".7"/>')
                cx += bw
    s.append(f'<rect x="{cx0-7:.1f}" y="{base-26:.1f}" width="14" height="26" fill="{DARK}" opacity=".82"/>')
    s.append(f'<line x1="{px+16}" y1="{base:.1f}" x2="{px+pw-16}" y2="{base:.1f}" '
             f'stroke="{BODY}" stroke-width="1.2"/>')
    for j, line in enumerate([
            'Each course oversails the one below until the last',
            'two stones meet. The stones are rubble — irregular,',
            'polygonal, fitted to their own shape, not cut to a course.']):
        s.append(txt(px + 12, base + 20 + j * 12, line, 8.3, BODY, 'start'))
    for j, line in enumerate([
            'A farmer could build one. Several usually did,',
            'together, and the owner of the ground fed them.']):
        s.append(txt(px + 12, base + 62 + j * 12, line, 8.3, BODY, 'start', '400', 'italic'))

    # ── the watch seasons
    yc = 420
    s.append(txt(40, yc - 12, 'WHEN THE TOWER IS OCCUPIED', 9.4, GOLD, 'start', '700', 'normal', '1.2'))
    s.append(txt(W - 40, yc - 12, 'seven months of the year, somebody sleeps in the field',
                 8.8, GREY, 'end', '400', 'italic'))
    m0, mw = 40, (W - 80) / 12.0
    for i, m in enumerate(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']):
        s.append(f'<rect x="{m0+i*mw:.1f}" y="{yc:.1f}" width="{mw-2:.1f}" height="16" '
                 f'fill="#F4F1E8" stroke="{RULE}" stroke-width=".6"/>')
        s.append(txt(m0 + i * mw + mw / 2 - 1, yc + 12, m, 8.6, FOLIO, 'middle'))
    for j, (a, b, lab, col) in enumerate([(4, 6, 'grain, and the early fruit', GREEN),
                                          (6, 9, 'figs and grapes', RUST),
                                          (9, 11, 'the olives', PLUM)]):
        yy = yc + 21 + j * 17
        s.append(f'<rect x="{m0+a*mw:.1f}" y="{yy:.1f}" width="{(b-a)*mw-2:.1f}" height="13" '
                 f'fill="{col}" opacity=".16" stroke="{col}" stroke-width=".8" rx="2"/>')
        s.append(txt(m0 + a * mw + 6, yy + 10, lab, 8.4, col, 'start', '700'))

    # ── the count
    yb2 = 500
    s.append(f'<line x1="40" y1="{yb2}" x2="{W-40}" y2="{yb2}" stroke="{RULE}"/>')
    stats = [('167', 'watchtowers standing,', 'and counted, one by one', GREEN),
             ('3,000', 'dunums of terrace', 'they stand in', GOLD),
             ('2', 'places: al-Tireh quarter', 'and ʿAin Qinia village', PLUM),
             ('0', 'grams of mortar', 'in any of them', RUST)]
    for k, (v, l1, l2, col) in enumerate(stats):
        sx = 40 + k * 205
        s.append(txt(sx, yb2 + 26, v, 19, col, 'start', '700'))
        off = 14 + 10.5 * len(v)
        s.append(txt(sx + off, yb2 + 19, l1, 8.4, BODY, 'start'))
        s.append(txt(sx + off, yb2 + 30, l2, 8.4, BODY, 'start'))
    s.append('</svg>')
    return ''.join(s)


# ═════════════════════ 7. Riyam 2006-17 — twelve lands, in the order he crossed them
def fig_riyam_road():
    """The itinerary of a Sabaean envoy, c. 260–280, exactly as the stone gives it.

    The point of the plate is position: the land of the Azd is the first stop and
    the land of Ghassān is the ninth, with Palmyra, the Nabataeans, Rome and
    Lakhm in between. In the third century they are already two different places.
    """
    W, H = 860, 520
    s = []
    _head(s, W, H, 'TWELVE LANDS, IN THE ORDER HE CROSSED THEM',
          'Riyam 2006-17: a Sabaean envoy is sent north, comes home, and has the road carved '
          'into a dedication to Taʾlab Riyām. Third century AD, probably c. 260–280.',
          'The twelve lands named in the Sabaic inscription Riyam 2006-17 in the order the envoy crossed them')

    # (sabaic-as-given, what it is, kind)
    STOPS = [
        ('Asdan',      'al-Asd — the Azd,<br>the family’s own tribe', 'us'),
        ('Nizārum',    'Nizār', ''),
        ('Tanūkh',     'Tanūkh —<br>lower Mesopotamia', ''),
        ('Liḥyān',     'Liḥyān — Dedan,<br>al-ʿUlā', ''),
        ('Tadmurum',   '<tspan font-weight="700">Palmyra</tspan>', 'big'),
        ('Nabaṭum',    'the Nabataeans —<br>Petra, and this country', 'big'),
        ('Rumān',      '<tspan font-weight="700">Rome</tspan>', 'big'),
        ('Lakhmum',    'Lakhm — al-Ḥīra,<br>the Persian client', ''),
        ('Ghassān',    'GHASSĀN —<br>already a land of its own', 'us'),
        ('Maʿaddum',   'Maʿadd', ''),
        ('Ṭayyum',     'Ṭayyiʾ', ''),
        ('Khaṣaṣatan', 'Khaṣaṣat', ''),
    ]

    x0, x1 = 62, W - 62
    per = 6
    rowy = [150, 300]
    dx = (x1 - x0) / (per - 1)

    def place(i):
        r, c = divmod(i, per)
        return (x0 + c * dx) if r == 0 else (x1 - c * dx), rowy[r]

    # the road itself
    for r in range(2):
        s.append(f'<line x1="{x0}" y1="{rowy[r]}" x2="{x1}" y2="{rowy[r]}" '
                 f'stroke="{TAN}" stroke-width="3" stroke-linecap="round"/>')
    s.append(f'<path d="M{x1} {rowy[0]} q 34 0 34 34 t -34 34" fill="none" '
             f'stroke="{TAN}" stroke-width="3"/>')

    s.append(txt(x0 - 6, rowy[0] + 44, 'HE SETS OUT FROM SABAʾ', 9.2, GOLD, 'start', '700', 'normal', '1.2'))
    s.append(txt(x0 - 6, rowy[0] + 56, 'the highlands of Yemen', 8.6, GREY, 'start', '400', 'italic'))
    s.append(txt(x0 - 6, rowy[1] + 96, 'AND TAʾLAB RIYĀM BROUGHT HIM BACK', 9.2, GOLD, 'start', '700', 'normal', '1.2'))
    s.append(txt(x0 - 6, rowy[1] + 108, '“from the land of the North”', 8.6, GREY, 'start', '400', 'italic'))

    for i, (name, what, kind) in enumerate(STOPS):
        cx, cy = place(i)
        up = (i // per) == 0
        us = kind == 'us'
        big = kind == 'big'
        rad = 15 if us else (12 if big else 9)
        fill = '#E4F0E8' if us else ('#FFFFFF' if big else SURF)
        edge = GREEN if us else (GOLD if big else FOLIO)
        s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rad}" fill="{fill}" '
                 f'stroke="{edge}" stroke-width="{2.0 if us else 1.2}"/>')
        s.append(txt(cx, cy + 3.4, str(i + 1), 9.4 if us else 8.6,
                     GREEN if us else (GOLD if big else FOLIO), 'middle', '700'))
        ny = cy - rad - 12 if up else cy + rad + 16
        s.append(txt(cx, ny, esc(name), 10.4 if us else 9.6,
                     DARK if us else INK, 'middle', '700' if us else '600'))
        for k, line in enumerate(what.split('<br>')):
            yy = (ny - 11 - (len(what.split('<br>')) - 1 - k) * 10.5) if up else (ny + 12 + k * 10.5)
            s.append(txt(cx, yy, line, 8.3, GREEN if us else GREY, 'middle',
                         '700' if us else '400', 'normal' if us else 'italic'))

    # the reading
    yb = 448
    s.append(f'<line x1="40" y1="{yb}" x2="{W-40}" y2="{yb}" stroke="{RULE}"/>')
    s.append(txt(40, yb + 22, 'THE AZD ARE STOP ONE. GHASSĀN IS STOP NINE.',
                 11, GOLD, 'start', '700', 'normal', '1.2'))
    s.append(txt(40, yb + 38,
                 'In the third century AD they are two different lands, and the road between them runs past '
                 'Palmyra, the Nabataeans, Rome and al-Ḥīra.',
                 9.4, BODY, 'start'))
    s.append(txt(40, yb + 52,
                 'The dam’s first recorded breach is in 455 — a hundred and seventy-five years after this stone was cut.',
                 9.4, RUST, 'start', '700'))
    s.append('</svg>')
    return ''.join(s)


# ═════════════════════ 8. who was on this ridge in the Iron Age
# ═════════════════════ 8. who was on this ridge in the Iron Age
def fig_iron_ridge():
    """The excavated Iron Age sites within a morning's walk of Ramallah — and the
    hole in the middle of them where Ramallah is not.

    The sites cluster inside four kilometres, so every label lives in a gutter
    with a leader line to its dot; nothing is placed free-hand near the map.
    """
    W, H = 860, 600
    MX0, MX1, MY0, MY1 = 296, 566, 122, 470
    lon0, lon1, lat0, lat1 = 35.13, 35.33, 31.79, 32.08
    def P(lat, lon):
        return (MX0 + (lon - lon0) / (lon1 - lon0) * (MX1 - MX0),
                MY0 + (lat1 - lat) / (lat1 - lat0) * (MY1 - MY0))

    # (lat, lon, name, dist, note, side, label-y, approximate?)
    SITES = [
      (32.0556, 35.2894, 'KHIRBET SEILŪN', '19 km',
       'SHILOH — 1 Samuel 1–4.<br>The highland sanctuary of the Iron I period.', 'R', 150, False),
      (31.9275, 35.2367, 'BEITIN', '4.4 km',
       'BETHEL — Genesis 28:10–19.<br>Jacob’s ladder, on the ridge road.', 'L', 168, False),
      (31.9169, 35.2569, 'et-TELL (Ai)', '5.3 km',
       'AI — Joshua 7–8. The name means “the ruin.”<br>An Iron I village on the ruined Early Bronze town.', 'R', 268, False),
      (31.9083, 35.2050, 'KHIRBET RADDANA', 'inside al-Bīra',
       'A farming village of the 12th–11th<br>centuries BC — pillared houses, silos,<br>'
       'a spring. Dug 1969–74; now almost<br>entirely under the streets of al-Bīra.', 'R', 366, True),
      (31.8869, 35.2164, 'TELL en-NAṢBEH', '3 km',
       'MIZPAH — 1 Samuel 10:17–24.<br>Where Saul was chosen king. Badè, 1926–35.', 'L', 282, False),
      (31.8464, 35.1847, 'al-JIB', '6.2 km',
       'GIBEON — Joshua 9–10. Sixty jar handles<br>found here are inscribed with the name.', 'L', 400, False),
    ]
    s = []
    _head(s, W, H, 'THE RIDGE IN THE IRON AGE — every excavated site, and the gap in the middle',
          'About 1000 BC. Each dot is a site with a published excavation. Distances are measured '
          'from the centre of present-day Ramallah.',
          'Map of excavated Iron Age sites around Ramallah with the site of Ramallah itself unoccupied')

    s.append(f'<rect x="{MX0-26}" y="{MY0-30}" width="{MX1-MX0+52}" height="{MY1-MY0+38}" '
             f'fill="{LAND}" opacity=".5" rx="4"/>')
    ridge = [(31.79, 35.198), (31.87, 35.208), (31.93, 35.220), (32.01, 35.240), (32.08, 35.252)]
    s.append('<polyline points="' + ' '.join('%.1f,%.1f' % P(a, b) for a, b in ridge) +
             f'" fill="none" stroke="{TAN}" stroke-width="6.5" opacity=".9"/>')
    s.append(txt(MX0 - 20, MY0 - 12, 'the watershed ridge road', 8.8, '#9A7A45', 'start', '400', 'italic'))

    for la, lo, nm, dist, note, side, ly, approx in SITES:
        x, y = P(la, lo)
        gx = 258 if side == 'L' else 604
        anc = 'end' if side == 'L' else 'start'
        s.append(f'<path d="M{x:.1f} {y:.1f} L{(gx+14) if side=="L" else (gx-14):.1f} {ly-4:.1f}" '
                 f'fill="none" stroke="{FOLIO}" stroke-width=".8" opacity=".7"/>')
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6.2" fill="{GREEN}" stroke="#FFFFFF" '
                 f'stroke-width="1.8"' + (' stroke-dasharray="2.5 2"' if approx else '') + '/>')
        s.append(txt(gx, ly, nm, 9.8, DARK, anc, '700', 'normal', '.6'))
        s.append(txt(gx, ly + 12, _kmlab(la, lo) + ('  · position approximate' if approx else ''),
                     8.6, GREY, anc, '400', 'italic'))
        for i, ln in enumerate(note.split('<br>')):
            s.append(txt(gx, ly + 25 + i * 10.5, ln, 8.4, BODY, anc))

    # Ramallah — the hole in the middle
    x, y = P(31.8996, 35.2042)
    s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="16" fill="#FFFAF0" stroke="{RUST}" '
             f'stroke-width="2.1" stroke-dasharray="4 3.5"/>')
    s.append(txt(x, y + 34, 'RAMALLAH', 11, RUST, 'middle', '700', 'normal', '1.2'))
    s.append(txt(x, y + 46, 'no Iron Age settlement', 8.6, RUST, 'middle', '400', 'italic'))
    s.append(txt(x, y + 56, 'founded AD 1562', 8.6, RUST, 'middle', '400', 'italic'))

    fx, fy = P(31.80, 35.202)
    s.append(f'<path d="M{fx:.1f} {fy-14:.1f} L{fx:.1f} {fy:.1f} M{fx-4:.1f} {fy-5:.1f} '
             f'L{fx:.1f} {fy:.1f} L{fx+4:.1f} {fy-5:.1f}" fill="none" stroke="{GREY}" stroke-width="1.2"/>')
    s.append(txt(fx, fy + 13, 'the road continues to Jerusalem — 13.8 km', 8.6, GREY, 'middle', '400', 'italic'))

    yb = H - 118
    s.append(f'<line x1="40" y1="{yb}" x2="{W-40}" y2="{yb}" stroke="{RULE}"/>')
    s.append(txt(40, yb + 22, 'THE RIDGE WAS FULL. THE TOWN WAS NOT ON IT.',
                 11, GOLD, 'start', '700', 'normal', '1.2'))
    for i, ln in enumerate([
      'Every village here is within an hour or two of the future town, and every one was inhabited while Ramallah’s own hilltop was empty ground.',
      '<tspan font-weight="700">Khirbet Raddana lies inside al-Bīra</tspan> — a farming village of the twelfth and eleventh centuries BC, on the doorstep, excavated in the 1960s and',
      'since built over by the town’s own growth. The people in those houses are the population this book has followed since the Chalcolithic.',
      'What changes across the Iron Age is not who lives on this ridge. It is what they are called.']):
        s.append(txt(40, yb + 42 + i * 15, ln, 9.4, BODY, 'start'))
    s.append('</svg>')
    return ''.join(s)


# ═════════════════════ 9. the highland fill-up, counted
def fig_highland_fill():
    """Late Bronze to Iron I in the central highlands, drawn as one dot per site."""
    W, H = 860, 596
    s = []
    _head(s, W, H, 'THE HIGHLANDS FILL UP — one dot for every settlement found',
          'Archaeological survey of the central hill country: the Late Bronze Age against the Iron I '
          'period that follows it. The coast and the valleys show no comparable jump.',
          'Dot chart comparing about 25 Late Bronze Age highland sites with about 250 in Iron Age I')

    def block(x0, y0, n, cols, col, r=4.6, gap=13.5):
        out = []
        for i in range(n):
            c, rr = i % cols, i // cols
            out.append(f'<circle cx="{x0+c*gap:.1f}" cy="{y0+rr*gap:.1f}" r="{r}" fill="{col}"/>')
        return ''.join(out), (n + cols - 1) // cols

    # left — Late Bronze
    s.append(txt(56, 108, 'LATE BRONZE AGE', 10.2, GREY, 'start', '700', 'normal', '1.2'))
    s.append(txt(56, 124, 'c. 1400–1200 BC', 9, FOLIO, 'start', '400', 'italic'))
    b, rows = block(62, 148, 25, 5, '#B9B3A6')
    s.append(b)
    s.append(txt(56, 148 + rows * 13.5 + 16, 'about 25 settlements', 11, INK, 'start', '700'))

    # right — Iron I
    s.append(txt(300, 108, 'IRON AGE I', 10.2, DARK, 'start', '700', 'normal', '1.2'))
    s.append(txt(300, 124, 'c. 1200–1000 BC', 9, FOLIO, 'start', '400', 'italic'))
    b2, rows2 = block(306, 148, 250, 22, GREEN)
    s.append(b2)
    s.append(txt(300, 148 + rows2 * 13.5 + 16, 'about 250 settlements — roughly 45,000 people',
                 11, DARK, 'start', '700'))

    yb = 392
    s.append(f'<line x1="40" y1="{yb}" x2="{W-40}" y2="{yb}" stroke="{RULE}"/>')
    s.append(txt(40, yb + 24, 'AND HERE IS WHAT THE JUMP IS NOT', 11, GOLD, 'start', '700', 'normal', '1.2'))
    NOTS = [
      ('No destruction layer', 'The highland villages are new foundations on empty hilltops, not '
       'burnt towns rebuilt by somebody else.'),
      ('No new pottery tradition', 'The cooking pots continue the local Late Bronze repertoire. '
       'A population arriving from outside brings its own kitchen; this one did not.'),
      ('No arrival visible anywhere else', 'The coast and the Jordan valley show no matching '
       'emptying-out. Nobody moved from there to here in numbers.'),
    ]
    for i, (h, d) in enumerate(NOTS):
        y = yb + 46 + i * 34
        s.append(f'<circle cx="47" cy="{y-4}" r="3.2" fill="{RUST}"/>')
        s.append(txt(60, y, h, 9.8, INK, 'start', '700'))
        s.append(txt(60, y + 13, d, 9.2, BODY, 'start'))
    s.append(f'<line x1="40" y1="{H-52}" x2="{W-40}" y2="{H-52}" stroke="{RULE}"/>')
    s.append(txt(40, H - 30,
                 'The people filling these hills were already in the country. What the Iron Age adds to this ridge is a name, not a population.',
                 10.4, DARK, 'start', '700'))
    s.append('</svg>')
    return ''.join(s)


# ═════════════════════ 10. the Bible as a map of this district
def fig_bible_ridge():
    """Biblical places within a day's walk, and the Arabic village each survived as.

    The right-hand grade is for the identification itself, not for the scripture:
    whether the ground has confirmed the name, merely agrees with it, or is argued.
    """
    W = 860
    ROWS = [
      # (biblical, village today, arabic, km, scripture, dug, grade)
      ('BEEROTH', 'al-Bīra', 'البيرة', 'next door',
       'Joshua 9:17 · Ezra 2:25 · Nehemiah 7:29',
       'Ramallah’s own twin town. Robinson’s identification, and philologists doubt it: al-Bīra most '
       'likely comes from Aramaic bīrāh, “fortress,” not the Hebrew for “wells.” Six candidates have been '
       'proposed and none is secure. The town is built over; nothing can be dug to settle it.', 'c'),
      ('MIZPAH', 'Tell en-Naṣbeh', '—', '1.8 km',
       '1 Samuel 7:5–6 · 1 Samuel 10:17–24 · Jeremiah 40–41',
       'Where Samuel is said to have judged Israel and Saul to have been chosen king; and where '
       'Gedaliah governed after 586. Badè, five seasons, 1926–35.', 's'),
      ('BETHEL', 'Beitin', 'بيتين', '4.4 km',
       'Genesis 12:8 · Genesis 28:10–19',
       'Abram pitches his tent between Bethel and Ai; Jacob dreams of the ladder and names the '
       'place. Excavated by Albright and Kelso.', 's'),
      ('AI', 'et-Tell', 'التل', '5.3 km',
       'Joshua 7–8',
       'Hebrew <tspan font-style="italic">ha-ʿAi</tspan> means “the ruin” — and the ground agrees. An Early Bronze '
       'town destroyed c. 2400 BC, then empty a thousand years, then an Iron I village built on the '
       'mound without resistance. Marquet-Krause, Callaway, Nur el-Din.', 's'),
      ('GIBEON', 'al-Jib', 'الجيب', '6.2 km',
       'Joshua 9–10 · 2 Samuel 2:12–17',
       'Pritchard, 1956–59, found <tspan font-weight="700">more than sixty jar handles inscribed גבען — Gibeon</tspan>, in '
       'eighth- and seventh-century Hebrew script. The site says its own name.', 'n'),
      ('MICHMASH', 'Mukhmās', 'مخماس', '7.5 km',
       '1 Samuel 13–14',
       'The pass where Jonathan crossed between the two crags. The name came through unbroken; '
       'the site is surveyed rather than excavated.', 's'),
      ('BAAL-HAZOR', 'Tell ʿAṣūr', 'تل عاصور', '11 km',
       '2 Samuel 13:23',
       'Absalom’s sheep-shearing. The highest summit of the central highlands, and the horizon '
       'from Ramallah’s own rooftops.', 's'),
      ('EPHRAIM', 'eṭ-Ṭaybeh', 'الطيبة', '11 km',
       'John 11:54',
       'Where the Gospel says Jesus withdrew with his disciples. Still today an entirely Christian '
       'town, with a Byzantine church in it. Already an entry in this book.', 's'),
      ('SHILOH', 'Khirbet Seilūn', 'خربة سيلون', '19 km',
       '1 Samuel 1–4 · Jeremiah 7:12',
       'Hannah’s prayer, Eli, and the Ark before Jerusalem. Excavated by Danish and later '
       'expeditions.', 's'),
    ]
    RH = 72
    top = 132
    H = top + len(ROWS) * RH + 104
    s = []
    _head(s, W, H, 'THE BIBLE IS A MAP OF THIS DISTRICT',
          'Every one of these places is within a day’s walk of Ramallah, and every one of them is '
          'still called, in Arabic, what it was called three thousand years ago.',
          'Table of biblical places near Ramallah with their modern Arabic village names, scripture references and excavations')

    GR = {'n': (GREEN, '#E4F0E8', 'NAMED ON SITE'),
          's': (GOLD,  '#F6EEDF', 'SECURE'),
          'c': (RUST,  '#F7E7DC', 'CONTESTED')}

    s.append(txt(40, top - 14, 'IN SCRIPTURE', 8.6, FOLIO, 'start', '700', 'normal', '1.4'))
    s.append(txt(252, top - 14, 'ON THE GROUND TODAY', 8.6, FOLIO, 'start', '700', 'normal', '1.4'))
    s.append(txt(W - 40, top - 14, 'THE IDENTIFICATION', 8.6, FOLIO, 'end', '700', 'normal', '1.4'))
    s.append(f'<line x1="40" y1="{top-6}" x2="{W-40}" y2="{top-6}" stroke="{RULE}"/>')

    for i, (bib, vil, ar, km, scr, dug, g) in enumerate(ROWS):
        y = top + i * RH
        col, bg, lab = GR[g]
        if i % 2 == 0:
            s.append(f'<rect x="40" y="{y-2}" width="{W-80}" height="{RH-6}" fill="{SURF}" rx="3"/>')
        s.append(txt(52, y + 18, bib, 11.4, DARK, 'start', '700', 'normal', '.8'))
        s.append(txt(52, y + 32, scr, 8.4, GOLD, 'start', '400', 'italic'))
        s.append(txt(252, y + 18, vil, 10.6, INK, 'start', '700'))
        if ar != '—':
            s.append(txt(252, y + 33, f'<tspan class="ar">{ar}</tspan>', 10.2, GREY, 'start'))
        s.append(txt(376, y + 18, km, 8.8, GREY, 'start', '400', 'italic'))
        # the note, wrapped
        words, line, lines = dug.split(' '), '', []
        for w in words:
            t = (line + ' ' + w).strip()
            if len(t) > 76 and line:
                lines.append(line); line = w
            else:
                line = t
        lines.append(line)
        for k, ln in enumerate(lines[:4]):
            s.append(txt(444, y + 12 + k * 11, ln, 8.3, BODY, 'start'))
        bw = 96
        s.append(f'<rect x="{W-40-bw}" y="{y+6}" width="{bw}" height="15" rx="7.5" fill="{bg}" '
                 f'stroke="{col}" stroke-width=".8"/>')
        s.append(txt(W - 40 - bw / 2, y + 16.6, lab, 7.4, col, 'middle', '700', 'normal', '.9'))

    yb = top + len(ROWS) * RH + 8
    s.append(f'<line x1="40" y1="{yb}" x2="{W-40}" y2="{yb}" stroke="{RULE}"/>')
    s.append(txt(40, yb + 24, 'THE NAMES ARE THE EVIDENCE.', 11, GOLD, 'start', '700', 'normal', '1.2'))
    for i, ln in enumerate([
      'Not one of these places was located by reading the Bible. They were located by asking the people who lived on them what they called home —',
      'and the answers had been carried, in Arabic, by farming families on these hills for three thousand years. <tspan font-weight="700">The Palestinian village names are why',
      'the biblical map can be read at all.</tspan> Where the ground has been dug it has agreed with them, and at al-Jib it agreed in writing.']):
        s.append(txt(40, yb + 44 + i * 15, ln, 9.4, BODY, 'start'))
    s.append('</svg>')
    return ''.join(s)


# ═════════════════════ 11. the roads he used, and this ridge under them
def fig_jesus_road():
    """Where the Gospels put him, drawn against the ridge Ramallah would be built on.

    Left: the country, and the two roads between Galilee and Jerusalem — the
    watershed ridge through Samaria, and the Jordan valley through Jericho.
    Centre: the district, with everything the Gospels name inside a day's walk.
    Right: the numbered key, so no label has to be crowded onto the map.
    Markers are graded on the identification of the place, never on the verse.
    """
    W, H = 880, 790
    s = []
    _head(s, W, H, 'THE ROADS HE USED — and the ridge they run along',
          'The Gospel places, at their real coordinates, against the hill Ramallah would be founded on '
          'fifteen centuries later. Distances are measured from the centre of the present town.',
          'Map of the places named in the Gospels in relation to the site of Ramallah')

    # ─────────── left panel: the country, and the two roads
    AX0, AX1, AY0, AY1 = 62, 232, 126, 520
    def PA(lat, lon):
        return (AX0 + (lon - 35.00) / 0.68 * (AX1 - AX0),
                AY0 + (32.95 - lat) / 1.33 * (AY1 - AY0))
    s.append(f'<clipPath id="clipJA"><rect x="{AX0-16}" y="{AY0-16}" '
             f'width="{AX1-AX0+34}" height="{AY1-AY0+32}"/></clipPath>')
    s.append(f'<rect x="{AX0-16}" y="{AY0-16}" width="{AX1-AX0+34}" height="{AY1-AY0+32}" '
             f'fill="{LAND}" opacity=".45" rx="4"/>')
    s.append(txt(AX0 - 16, AY0 - 24, 'GALILEE TO JERUSALEM', 9.4, GOLD, 'start', '700', 'normal', '.7'))

    s.append('<g clip-path="url(#clipJA)">')
    gx, gy = PA(32.83, 35.58)
    s.append(f'<ellipse cx="{gx:.1f}" cy="{gy:.1f}" rx="8" ry="13" fill="{SEA}" stroke="#BBCBD2" stroke-width=".8"/>')
    jordan = [(32.70, 35.575), (32.45, 35.535), (32.10, 35.545), (31.86, 35.545), (31.70, 35.510)]
    s.append('<polyline points="' + ' '.join('%.1f,%.1f' % PA(a, b) for a, b in jordan) +
             '" fill="none" stroke="#BBCBD2" stroke-width="2.4"/>')
    ridge_rd = [(32.702, 35.298), (32.560, 35.300), (32.460, 35.300), (32.330, 35.290),
                (32.210, 35.284), (32.085, 35.226), (31.960, 35.235), (31.900, 35.213),
                (31.840, 35.220), (31.778, 35.230)]
    valley_rd = [(32.702, 35.298), (32.600, 35.430), (32.497, 35.501), (32.300, 35.538),
                 (32.050, 35.543), (31.900, 35.518), (31.871, 35.444), (31.820, 35.330),
                 (31.778, 35.230)]
    s.append('<polyline points="' + ' '.join('%.1f,%.1f' % PA(a, b) for a, b in ridge_rd) +
             f'" fill="none" stroke="{TAN}" stroke-width="4.6" opacity=".95" stroke-linejoin="round"/>')
    s.append('<polyline points="' + ' '.join('%.1f,%.1f' % PA(a, b) for a, b in valley_rd) +
             f'" fill="none" stroke="{FOLIO}" stroke-width="2" stroke-dasharray="5 3.5" '
             f'opacity=".9" stroke-linejoin="round"/>')
    s.append('</g>')

    for la, lo, nm, side, dy, kind in [
      (32.702, 35.298, 'NAZARETH',  'L',  0, 'g'),
      (32.830, 35.580, 'GALILEE',   'R',  4, 'g'),
      (32.460, 35.300, 'GINAE',     'R',  3, 's'),
      (32.210, 35.284, 'SYCHAR',    'L',  0, 'g'),
      (31.871, 35.444, 'JERICHO',   'R',  0, 'g'),
      (31.778, 35.230, 'JERUSALEM', 'L',  9, 'g'),
      (31.705, 35.202, 'BETHLEHEM', 'L', 10, 'g')]:
        x, y = PA(la, lo)
        col = GREEN if kind == 'g' else FOLIO
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{4.4 if kind=="g" else 3.0}" fill="{col}" '
                 f'stroke="#FFFFFF" stroke-width="1.4"/>')
        s.append(txt(x - 9 if side == 'L' else x + 9, y + 3 + dy, nm, 8.4,
                     DARK if kind == 'g' else GREY, 'end' if side == 'L' else 'start',
                     '700' if kind == 'g' else '400', 'normal', '.5'))

    x, y = PA(31.8996, 35.2042)
    s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="#FFFAF0" stroke="{GOLD}" '
             f'stroke-width="2" stroke-dasharray="3.5 3"/>')
    s.append(txt(x - 13, y - 5, 'the ridge', 8.2, GOLD, 'end', '700', 'normal', '.4'))
    s.append(txt(x - 13, y + 5, 'Ramallah', 8.2, GOLD, 'end', '400', 'italic'))
    s.append(txt(x - 13, y + 14, 'will stand on', 8.2, GOLD, 'end', '400', 'italic'))

    ky = AY1 + 36
    s.append(f'<line x1="{AX0-16}" y1="{ky-18}" x2="{AX1+18}" y2="{ky-18}" stroke="{RULE}"/>')
    s.append(f'<line x1="{AX0-14}" y1="{ky-2}" x2="{AX0+6}" y2="{ky-2}" stroke="{TAN}" stroke-width="4.6"/>')
    s.append(txt(AX0 + 12, ky + 1, 'the ridge road, past this hill', 8.2, BODY))
    s.append(f'<line x1="{AX0-14}" y1="{ky+15}" x2="{AX0+6}" y2="{ky+15}" stroke="{FOLIO}" '
             f'stroke-width="2" stroke-dasharray="5 3.5"/>')
    s.append(txt(AX0 + 12, ky + 18, 'the valley road, up from Jericho', 8.2, BODY))
    for i, ln in enumerate([
        '“It was the custom of the Galileans, when they',
        'came to the holy city at the festivals, to take',
        'their journeys through the country of the',
        'Samaritans.”   — Josephus, Antiquities XX.118']):
        s.append(txt(AX0 - 14, ky + 40 + i * 11, ln, 8.2, BODY, 'start', '400', 'italic'))

    # ─────────── centre panel: the district
    BX0, BX1, BY0, BY1 = 352, 640, 150, 442
    def PB(lat, lon):
        return (BX0 + (lon - 35.10) / 0.36 * (BX1 - BX0),
                BY0 + (32.00 - lat) / 0.31 * (BY1 - BY0))
    s.append(f'<clipPath id="clipJB"><rect x="{BX0-16}" y="{BY0-16}" '
             f'width="{BX1-BX0+32}" height="{BY1-BY0+32}"/></clipPath>')
    s.append(f'<rect x="{BX0-16}" y="{BY0-16}" width="{BX1-BX0+32}" height="{BY1-BY0+32}" '
             f'fill="{LAND}" opacity=".45" rx="4"/>')
    s.append(txt(BX0 - 16, BY0 - 24, 'WITHIN A DAY’S WALK OF THE RIDGE', 9.4, GOLD, 'start', '700', 'normal', '.7'))

    s.append('<g clip-path="url(#clipJB)">')
    rnd = _rng(1154)
    for _ in range(130):
        wx, wy = PB(rnd(31.69, 32.00), rnd(35.335, 35.470))
        s.append(f'<circle cx="{wx:.1f}" cy="{wy:.1f}" r="{rnd(1.0, 2.1):.1f}" fill="{TAN}" opacity=".8"/>')
    rx, ry = PB(31.8996, 35.2042)
    RR = (15.0 / 111.0) * (BY1 - BY0) / 0.31
    s.append(f'<circle cx="{rx:.1f}" cy="{ry:.1f}" r="{RR:.1f}" fill="none" stroke="{GOLD}" '
             f'stroke-width="1" stroke-dasharray="3 4" opacity=".85"/>')
    rd = [(32.00, 35.246), (31.958, 35.232), (31.928, 35.229), (31.907, 35.218),
          (31.880, 35.213), (31.840, 35.219), (31.800, 35.226), (31.778, 35.230), (31.690, 35.198)]
    s.append('<polyline points="' + ' '.join('%.1f,%.1f' % PB(a, b) for a, b in rd) +
             f'" fill="none" stroke="{TAN}" stroke-width="4.6" opacity=".95" stroke-linejoin="round"/>')
    jr = [(31.778, 35.230), (31.795, 35.300), (31.822, 35.372), (31.871, 35.444)]
    s.append('<polyline points="' + ' '.join('%.1f,%.1f' % PB(a, b) for a, b in jr) +
             f'" fill="none" stroke="{FOLIO}" stroke-width="2" stroke-dasharray="5 3.5" opacity=".9"/>')
    s.append('</g>')
    wtx, wty = PB(31.735, 35.400)
    s.append(txt(wtx, wty, 'THE WILDERNESS', 8.8, '#9A7A45', 'middle', '700', 'normal', '1'))
    s.append(txt(wtx, wty + 12, '“near to the wilderness”', 8.0, '#9A7A45', 'middle', '400', 'italic'))
    s.append(txt(wtx, wty + 22, 'John 11:54', 8.0, '#9A7A45', 'middle', '400', 'italic'))

    # (lat, lon, n, name, side, dy, kind)
    BPTS = [
      (31.9497, 35.3006, '1', 'eṭ-ṬAYBEH',  'R',  0, 'g'),
      (31.9583, 35.2211, '2', 'JIFNĀ',      'L',  0, 's'),
      (31.9275, 35.2367, '3', 'BEITIN',     'R',  0, 's'),
      (31.9075, 35.2200, '4', 'al-BĪRA',    'R', 13, 't'),
      (31.8400, 35.1369, '5', 'al-QUBEIBA', 'L',  0, 't'),
      (31.7784, 35.2297, '6', 'JERUSALEM',  'L',  0, 'g'),
      (31.7714, 35.2617, '7', 'BETHANY',    'R',  8, 'g'),
      (31.8709, 35.4441, '8', 'JERICHO',    'L',  0, 'g'),
      (31.7054, 35.2024, '9', 'BETHLEHEM',  'L',  8, 'g'),
    ]
    KIND = {'g': (GREEN, '700'), 's': (GREY, '700'), 't': (PLUM, '400')}
    for la, lo, n, nm, side, dy, kind in BPTS:
        x, y = PB(la, lo)
        col, wt = KIND[kind]
        dash = ' stroke-dasharray="2.5 2"' if kind == 't' else ''
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.2" fill="{"#FFFAF0" if kind=="t" else col}" '
                 f'stroke="{col if kind=="t" else "#FFFFFF"}" stroke-width="{2 if kind=="t" else 1.6}"{dash}/>')
        s.append(txt(x - 9 if side == 'L' else x + 9, y + 3 + dy, n + ' · ' + nm, 8.8,
                     col if kind != 'g' else DARK, 'end' if side == 'L' else 'start', wt, 'normal', '.5'))

    x, y = PB(31.8996, 35.2042)
    s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="12" fill="#FFFAF0" stroke="{RUST}" '
             f'stroke-width="2.1" stroke-dasharray="4 3.5"/>')
    s.append(txt(x - 16, y - 1, 'RAMALLAH', 9.8, RUST, 'end', '700', 'normal', '.9'))
    s.append(txt(x - 16, y + 10, 'empty ground, AD 30', 8.0, RUST, 'end', '400', 'italic'))

    # ─────────── right panel: the numbered key
    KX = 662
    s.append(txt(KX, BY0 - 24, 'WHAT THE GOSPELS SAY IS HERE', 9.4, GOLD, 'start', '700', 'normal', '.7'))
    ENTRIES = [
      ('1', 'eṭ-ṬAYBEH', _kmlab(31.9497, 35.3006), 'g',
       'EPHRAIM. “He withdrew to a city called Ephraim, and there continued with his disciples.” '
       'John 11:54. Still the last entirely Christian town in Palestine.'),
      ('2', 'JIFNĀ', _kmlab(31.9583, 35.2211), 's',
       'GOPHNA. The Roman capital of this district. Titus held Jerusalem’s surrendered priests here in AD 70.'),
      ('3', 'BEITIN', _kmlab(31.9275, 35.2367), 's',
       'BETHEL. Taken and garrisoned by Vespasian in AD 69, with Ephraim, on his way to Jerusalem.'),
      ('4', 'al-BĪRA', _kmlab(31.9075, 35.2200), 't',
       'Luke 2:44 — the day’s journey. A Crusader church of 1128; by the 1300s the Latins held this was '
       'where they missed him. Tradition, not evidence.'),
      ('5', 'al-QUBEIBA', _kmlab(31.8400, 35.1369), 't',
       'EMMAUS? Luke 24:13. One of four candidates, adopted by pilgrims only in the 1200s.'),
      ('6', 'JERUSALEM', _kmlab(31.7784, 35.2297), 'g', 'The festivals — Luke 2:41. And the last week — Mark 11–15.'),
      ('7', 'BETHANY', _kmlab(31.7714, 35.2617), 'g', 'al-ʿAyzariyya. John 11 — Lazarus, Martha and Mary.'),
      ('8', 'JERICHO', _kmlab(31.8709, 35.4441), 'g', 'Luke 19:1, Zacchaeus. Luke 10:30, the road down from Jerusalem.'),
      ('9', 'BETHLEHEM', _kmlab(31.7054, 35.2024), 'g', 'Luke 2, Matthew 2.'),
    ]
    yy = BY0 - 2
    for n, nm, dist, kind, gloss in ENTRIES:
        col, wt = KIND[kind]
        s.append(f'<circle cx="{KX+5}" cy="{yy-3}" r="5.2" fill="{"#FFFAF0" if kind=="t" else col}" '
                 f'stroke="{col if kind=="t" else "#FFFFFF"}" stroke-width="{2 if kind=="t" else 1.6}"'
                 + (' stroke-dasharray="2.5 2"' if kind == 't' else '') + '/>')
        s.append(txt(KX + 17, yy, n + ' · ' + nm, 9, col if kind != 'g' else DARK, 'start', wt, 'normal', '.5'))
        s.append(txt(W - 40, yy, dist, 8.2, GREY, 'end', '400', 'italic'))
        for ln in _wrap(gloss, 48):
            yy += 10.6
            s.append(txt(KX + 17, yy, ln, 8.2, BODY))
        yy += 20

    # ─────────── the key to the grades, and the closing band
    gy2 = BY1 + 34
    for i, (col, dash, lab) in enumerate([
        (GREEN, '', 'named in the Gospels · the site securely identified'),
        (GREY, '', 'named in Josephus or the Roman record, not in the Gospels'),
        (PLUM, ' stroke-dasharray="2.5 2"', 'medieval pilgrim tradition only — printed, and graded as such')]):
        s.append(f'<circle cx="{BX0-10}" cy="{gy2+i*15-3}" r="5" fill="{"#FFFAF0" if col==PLUM else col}" '
                 f'stroke="{col if col==PLUM else "#FFFFFF"}" stroke-width="{2 if col==PLUM else 1.6}"{dash}/>')
        s.append(txt(BX0 + 3, gy2 + i * 15, lab, 8.4, BODY))
    s.append(f'<circle cx="{BX0-10}" cy="{gy2+42}" r="6" fill="none" stroke="{GOLD}" '
             f'stroke-width="1" stroke-dasharray="3 4"/>')
    s.append(txt(BX0 + 3, gy2 + 45, 'the dashed circle: fifteen kilometres — half a day’s walk from the ridge',
                 8.4, BODY))

    yb = H - 118
    s.append(f'<line x1="40" y1="{yb}" x2="{W-40}" y2="{yb}" stroke="{RULE}"/>')
    s.append(txt(40, yb + 22, 'THE GOSPELS ARE SET IN THIS DISTRICT, NOT NEAR IT.',
                 11, GOLD, 'start', '700', 'normal', '1.2'))
    for i, ln in enumerate([
      'The one town the Gospels name on this ridge is <tspan font-weight="700">Ephraim</tspan> — eṭ-Ṭaybeh, eleven kilometres out. John calls it a city “near to the wilderness,” and the map shows',
      'why that is exactly right: Ṭaybeh sits on the last inhabited edge of the ridge, with the desert falling away east of it. <tspan font-weight="700">Everything else here is road.</tspan> The Galilee',
      'pilgrims came down the watershed past this hill three times a year, and Josephus says so plainly. Whoever was working these terraces in AD 30 watched that traffic pass —',
      'and within forty years the Romans had taken this district, garrisoned Bethel and Ephraim, and were holding Jerusalem’s surrendered priests at Jifnā, six kilometres away.']):
        s.append(txt(40, yb + 42 + i * 15, ln, 9.4, BODY, 'start'))
    s.append('</svg>')
    return ''.join(s)
