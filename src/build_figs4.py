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
      (31.8869, 35.2164, 'TELL en-NASBEH', 'A village on the edge of al-Bīra, 3 km from<br>Ramallah’s centre — Late Chalcolithic / EB I.', 3.0, 'chal', 14, 40, 'start'),
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
        s.append(txt(x + dx, y + dy + 12, f'{km} km', 8.6, GREY, anc, '400', 'italic'))
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
