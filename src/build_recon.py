# -*- coding: utf-8 -*-
"""The Family, Reconstructed — an illustrated, documented history from Adam to today.
Charts: inline SVG. Palette: the book's tokens; categorical triple validated
(007A3D / A85210 / 6D4E9E — all checks pass, CVD in the 6–8 band, so every
series is direct-labelled)."""
import math

from paths import out as _out
OUT = _out('The_Family_Reconstructed_v1.html')

GREEN, RUST, PLUM = '#007A3D', '#A85210', '#6D4E9E'
GOLD, GREY, RULE, FOLIO = '#B98A4E', '#77726A', '#DCD6C9', '#9A958C'
INK, BODY, DARK, CREAM = '#1A1A1A', '#46423B', '#004A26', '#FFFAF0'
RAMP = ['#D5E9DF', '#A9CDB8', '#79B491', '#3E9464', '#007A3D']
VOIDF, VOIDE, VOIDT = '#FDF6EC', '#C98B3F', '#8A5A1E'
SURF = '#FCFBF8'

# ───────────────────────────── citations
CITES = []
def c(txt):
    """register a citation, return the superscript marker"""
    CITES.append(txt)
    n = len(CITES)
    return f'<sup class="cn"><a href="#n{n}" id="r{n}">{n}</a></sup>'

# ───────────────────────────── svg helpers
def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def fig(svg, num, title, caption, source):
    return (f'<figure><div class="fignum">Figure {num}</div>'
            f'<div class="figtitle">{title}</div>'
            f'<div class="figwrap">{svg}</div>'
            f'<figcaption>{caption}<span class="src">{source}</span></figcaption></figure>')

def txt(x, y, s, size=11, fill=BODY, anchor='start', weight='400', style='normal', ls='0'):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" font-weight="{weight}" font-style="{style}" '
            f'letter-spacing="{ls}" font-family="Times New Roman, Times, serif">{s}</text>')

# ═════════════════════════════ FIGURE 1 — the master timeline
def _fitwrap(text, boxw, base, weight=0.52, maxlines=2, minsize=8.0):
    """Pick a font size and line-break that keep `text` inside `boxw`."""
    words = text.split()
    size = base
    while size >= minsize:
        cw = size * weight
        lines, cur = [], ''
        for w in words:
            t = (cur + ' ' + w).strip()
            if len(t) * cw > boxw and cur:
                lines.append(cur); cur = w
            else:
                cur = t
        if cur:
            lines.append(cur)
        if len(lines) <= maxlines and all(len(l) * cw <= boxw for l in lines):
            return size, lines
        size -= 0.5
    return minsize, [text]


def fig_master():
    W, H = 860, 330
    x0, x1 = 62, 830
    # non-linear: equal-ish bands per era, as the deck does
    eras = [
        ('Adam to Joktan', 'scripture', 'Genesis 5, 10, 11', 0.00, 0.17),
        ('Joktan to Jafna', 'classical', 'the Arab genealogists', 0.17, 0.33),
        ('The Jafnid phylarchs', 'attested', '6th century', 0.33, 0.42),
        ('Jafna to Rāshid', 'none', 'nine hundred years', 0.42, 0.63),
        ('The hills before 1562', 'attested', 'churches, a charter, a deed', 0.63, 0.76),
        ('The founding', 'documents', 'the Ottoman registers', 0.76, 0.83),
        ('Ottoman centuries', 'documents', 'jizya, court, travellers', 0.83, 0.92),
        ('1908 to today', 'documents', 'censuses', 0.92, 1.00),
    ]
    GR = {'scripture': ('#D5E9DF', '#A9CDB8', INK),
          'classical': ('#A9CDB8', '#79B491', INK),
          'attested': ('#79B491', '#3E9464', INK),
          'none': (VOIDF, VOIDE, VOIDT),
          'documents': (GREEN, GREEN, '#FFFFFF')}
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Master timeline of the story, graded by evidence">']
    s.append(f'<rect width="{W}" height="{H}" fill="{SURF}"/>')
    bt, bh = 104, 52
    for i, (name, g, sub, a, b) in enumerate(eras):
        fillc, edge, tc = GR[g]
        xa, xb = x0 + (x1 - x0) * a, x0 + (x1 - x0) * b
        w = xb - xa - 2
        s.append(f'<rect x="{xa:.1f}" y="{bt}" width="{w:.1f}" height="{bh}" fill="{fillc}" '
                 f'stroke="{edge}" stroke-width="1" rx="3"/>')
        if g == 'none':
            s.append(f'<rect x="{xa:.1f}" y="{bt}" width="{w:.1f}" height="{bh}" fill="url(#hatch)" rx="3"/>')
        cx = xa + w / 2
        fs, lines = _fitwrap(name, w - 8, 11.5, 0.53, 2, 7.5)
        y0 = bt + bh / 2 + 4 - (len(lines) - 1) * (fs * 0.62)
        for k, ln in enumerate(lines):
            s.append(txt(cx, y0 + k * (fs + 2.5), esc(ln), fs, tc, 'middle', '700'))
        # the caption below the band, staggered so neighbours never collide
        row = bt + bh + (16 if i % 2 == 0 else 30)
        fs2, l2 = _fitwrap(sub, max(w * 1.9, 90), 9.5, 0.46, 1, 7.0)
        s.append(f'<line x1="{cx:.1f}" y1="{bt+bh+3}" x2="{cx:.1f}" y2="{row-8:.1f}" stroke="{RULE}" stroke-width=".8"/>')
        s.append(txt(cx, row, esc(l2[0]), fs2, GREY, 'middle', '400', 'italic'))
        if i == 0 or eras[i - 1][1] != g:
            # only label a grade once per run, so three DOCUMENTS bands do not
            # print DOCUMENTS three times in a row
            run_end = i
            while run_end + 1 < len(eras) and eras[run_end + 1][1] == g:
                run_end += 1
            rxa = x0 + (x1 - x0) * eras[i][3]
            rxb = x0 + (x1 - x0) * eras[run_end][4]
            s.append(txt((rxa + rxb) / 2, bt - 10, g.upper(), 8, GREY, 'middle', '700', 'normal', '1.2'))
    # anchor dates below
    marks = [(0.00, 'Adam'), (0.33, 'c. 528 CE'), (0.42, 'c. 570'), (0.63, 'c. 1450'),
             (0.76, '1562'), (1.00, '2024')]
    my = bt + bh + 48
    for a, lab in marks:
        xa = x0 + (x1 - x0) * a
        s.append(f'<line x1="{xa:.1f}" y1="{my:.1f}" x2="{xa:.1f}" y2="{my+8:.1f}" stroke="{FOLIO}"/>')
        s.append(txt(xa, my + 22, lab, 9.5, FOLIO, 'middle'))
    s.append(txt(x0, 40, 'FIVE THOUSAND YEARS, AND WHERE THE RECORD BEGINS', 11, GOLD, 'start', '700', 'normal', '1.6'))
    s.append(txt(x0, 62, 'The horizontal scale is not linear — it could not be. What it shows is the order of the story,', 10.5, GREY, 'start', '400', 'italic'))
    s.append(txt(x0, 76, 'and the very late point at which documents start.', 10.5, GREY, 'start', '400', 'italic'))
    # the void call-out
    xa = x0 + (x1 - x0) * 0.42
    xb = x0 + (x1 - x0) * 0.63
    cy = my + 40
    s.append(f'<path d="M{xa:.1f} {cy:.0f} L{xa:.1f} {cy+8:.0f} L{xb:.1f} {cy+8:.0f} L{xb:.1f} {cy:.0f}" fill="none" stroke="{VOIDE}" stroke-width="1.2"/>')
    s.append(txt((xa + xb) / 2, cy + 26, 'the family’s own chart prints this gap', 10, VOIDT, 'middle', '700'))
    s.append(txt((xa + xb) / 2, cy + 40, '“Unknown Al-Ghassani — 45 generations” — this book prints about 31, in a range of 27–37', 9.4, VOIDT, 'middle', '400', 'italic'))
    s.append('<defs><pattern id="hatch" width="7" height="7" patternTransform="rotate(45)" '
             f'patternUnits="userSpaceOnUse"><line x1="0" y1="0" x2="0" y2="7" stroke="{VOIDE}" stroke-width="1.4" opacity=".5"/></pattern></defs>')
    s.append('</svg>')
    return ''.join(s)

# ═════════════════════════════ FIGURE 2 — the three chronologies
def fig_chron():
    W, H = 860, 300
    data = [('Masoretic', 1656, 292, GREEN), ('Septuagint', 2242, 1072, RUST), ('Samaritan', 1307, 942, PLUM)]
    x0, y0, plotw, ploth = 210, 70, 520, 150
    mx = 3400
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Years from creation to Abraham in three text traditions">']
    s.append(f'<rect width="{W}" height="{H}" fill="{SURF}"/>')
    s.append(txt(40, 34, 'YEARS FROM CREATION TO THE BIRTH OF ABRAHAM, BY TEXT TRADITION', 11, GOLD, 'start', '700', 'normal', '1.4'))
    s.append(txt(40, 52, 'A line to Adam implies a date for Adam — and the three surviving forms of the text disagree by 1,366 years.', 10.5, GREY, 'start', '400', 'italic'))
    bh, gap = 34, 18
    for i, (name, a, b, col) in enumerate(data):
        y = y0 + i * (bh + gap)
        s.append(txt(x0 - 14, y + 22, name, 11.5, INK, 'end', '700'))
        wa = plotw * a / mx
        wb = plotw * b / mx
        s.append(f'<rect x="{x0}" y="{y}" width="{wa:.1f}" height="{bh}" fill="{col}" rx="3"/>')
        s.append(f'<rect x="{x0+wa+2:.1f}" y="{y}" width="{wb:.1f}" height="{bh}" fill="{col}" opacity=".42" rx="3"/>')
        s.append(txt(x0 + wa / 2, y + 22, f'{a:,}', 10.5, '#FFFFFF', 'middle', '700'))
        if wb > 42:
            s.append(txt(x0 + wa + 2 + wb / 2, y + 22, f'{b:,}', 10.5, INK, 'middle', '700'))
        s.append(txt(x0 + wa + wb + 12, y + 22, f'{a+b:,} total', 10.5, BODY, 'start', '700'))
    # legend
    ly = y0 + 3 * (bh + gap) + 12
    s.append(f'<rect x="{x0}" y="{ly}" width="13" height="13" fill="{GREY}" rx="2"/>')
    s.append(txt(x0 + 20, ly + 11, 'Creation to the Flood', 10.5, BODY))
    s.append(f'<rect x="{x0+170}" y="{ly}" width="13" height="13" fill="{GREY}" opacity=".42" rx="2"/>')
    s.append(txt(x0 + 190, ly + 11, 'Flood to the birth of Abraham', 10.5, BODY))
    s.append(txt(40, ly + 44, 'The Septuagint reckoning is the inherited one for a Rūm Orthodox family — which makes the choice of text', 10.5, BODY))
    s.append(txt(40, ly + 60, 'itself a piece of family history. These are scripture, not chronology, and were never meant as chronology.', 10.5, BODY))
    s.append('</svg>')
    return ''.join(s)

# ═════════════════════════════ FIGURE 3 — the seven links
def fig_chain():
    links = [
        ('1', 'Adam to Eber', '20 generations', 'Genesis 5 and 11', 'scripture'),
        ('2', 'Eber to Joktan', '1 generation', 'Genesis 10:25–29 — Hazarmaveth is Ḥaḍramawt, Sheba is Sabaʾ', 'scripture'),
        ('3', 'Joktan = Qaḥṭān', 'the join', 'made by the Arab genealogists, stated by al-Ṭabarī c. 915', 'classical'),
        ('4', 'Qaḥṭān to Jafna', '16 generations', 'Yaʿrub → Yashjub → Sabaʾ → Kahlān → al-Azd → Ghassān → Jafna', 'classical'),
        ('5', 'The Jafnid phylarchs', '6th century', 'al-Ḥārith b. Jabala, 528–569 — Procopius, and inscriptions', 'attested'),
        ('6', 'Jafna to Rāshid', '≈45 generations', 'nothing. The chart prints the void.', 'none'),
        ('7', 'Rāshid to today', '21 generations', 'Ottoman registers from 1525, parish books, living memory', 'documents'),
    ]
    GR = {'scripture': ('#D5E9DF', '#A9CDB8', INK, 'SCRIPTURE'),
          'classical': ('#A9CDB8', '#79B491', INK, 'CLASSICAL SCHOLARSHIP'),
          'attested': ('#79B491', '#3E9464', INK, 'ATTESTED HISTORY'),
          'none': (VOIDF, VOIDE, VOIDT, 'NO EVIDENCE'),
          'documents': (GREEN, GREEN, '#FFFFFF', 'DOCUMENTS')}
    rh, top = 52, 60
    H = top + len(links) * rh + 60
    W = 860
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="The seven links of the chain and what each rests on">']
    s.append(f'<rect width="{W}" height="{H}" fill="{SURF}"/>')
    s.append(txt(40, 32, 'THE CHAIN, LINK BY LINK — AND WHAT EACH ONE RESTS ON', 11, GOLD, 'start', '700', 'normal', '1.4'))
    for i, (n, name, gen, note, g) in enumerate(links):
        y = top + i * rh
        fillc, edge, tc, lab = GR[g]
        s.append(f'<rect x="40" y="{y}" width="780" height="{rh-8}" fill="#FFFFFF" stroke="{RULE}" rx="4"/>')
        s.append(f'<rect x="40" y="{y}" width="5" height="{rh-8}" fill="{edge}" rx="2"/>')
        s.append(txt(60, y + 27, n, 15, FOLIO, 'start', '700'))
        s.append(txt(82, y + 20, esc(name), 12.5, INK, 'start', '700'))
        s.append(txt(82, y + 36, esc(gen), 10.5, GREY, 'start', '400', 'italic'))
        s.append(txt(258, y + 28, esc(note), 10.5, BODY))
        cw = 128
        s.append(f'<rect x="{820-cw-14}" y="{y+11}" width="{cw}" height="21" fill="{fillc}" stroke="{edge}" rx="10"/>')
        s.append(txt(820 - 14 - cw / 2, y + 25.5, lab, 7.6, tc, 'middle', '700', 'normal', '.9'))
    yb = top + len(links) * rh + 6
    s.append(txt(40, yb + 12, 'A sceptic aims at link 3 — but link 3 is not ours to defend: every Qaḥṭānī Arab in the world stands on it.', 10.5, BODY, 'start', '700'))
    s.append(txt(40, yb + 30, 'The real break is link 6, and the family’s own chart is the thing that says so.', 10.5, BODY, 'start', '700'))
    s.append('</svg>')
    return ''.join(s)

# ═════════════════════════════ FIGURE 4 — the arithmetic of 45
def fig_arith():
    W, H = 860, 250
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Years per generation implied by 45 generations, against the observed range">']
    s.append(f'<rect width="{W}" height="{H}" fill="{SURF}"/>')
    s.append(txt(40, 32, 'FORTY-FIVE IS THE WRONG NUMBER', 11, GOLD, 'start', '700', 'normal', '1.4'))
    s.append(txt(40, 50, 'The gap from Jafna (fl. c. 520) to Rāshid (fl. c. 1500) is about 1,000 years. Dividing it 45 ways gives a', 10.5, GREY, 'start', '400', 'italic'))
    s.append(txt(40, 64, 'male-line generation shorter than any observed population sustains.', 10.5, GREY, 'start', '400', 'italic'))
    x0, plotw = 250, 480
    lo, hi = 0, 40
    def px(v): return x0 + plotw * (v - lo) / (hi - lo)
    # observed band 30-35
    s.append(f'<rect x="{px(30):.1f}" y="96" width="{px(35)-px(30):.1f}" height="64" fill="{GREEN}" opacity=".16" rx="3"/>')
    s.append(txt((px(30)+px(35))/2, 90, 'OBSERVED RANGE FOR MALE LINES', 8.4, GREEN, 'middle', '700', 'normal', '.9'))
    rows = [('45 generations', 1000/45, RUST, 'what the chart says'),
            ('31 generations', 1000/31, GREEN, 'what 32 years a generation gives')]
    for i, (lab, v, col, note) in enumerate(rows):
        y = 106 + i * 34
        s.append(f'<rect x="{x0}" y="{y}" width="{px(v)-x0:.1f}" height="22" fill="{col}" rx="3"/>')
        s.append(txt(x0 - 14, y + 16, lab, 11.5, INK, 'end', '700'))
        s.append(txt(px(v) + 10, y + 16, f'{v:.1f} years per generation', 10.5, BODY, 'start', '700'))
        s.append(txt(px(v) + 10, y + 30, note, 9.5, GREY, 'start', '400', 'italic'))
    for v in (0, 10, 20, 30, 40):
        s.append(f'<line x1="{px(v):.1f}" y1="176" x2="{px(v):.1f}" y2="181" stroke="{FOLIO}"/>')
        s.append(txt(px(v), 194, str(v), 9.5, FOLIO, 'middle'))
    s.append(f'<line x1="{x0}" y1="176" x2="{px(40):.1f}" y2="176" stroke="{RULE}"/>')
    s.append(txt(x0 + plotw / 2, 212, 'years per generation', 10, GREY, 'middle', '400', 'italic'))
    s.append(txt(40, 232, 'The count is wrong; the gap is real. Correcting the arithmetic does not close the void — it measures it honestly.', 10.5, BODY, 'start', '700'))
    s.append('</svg>')
    return ''.join(s)

# ═════════════════════════════ FIGURE 5 — the regional map
def fig_map_region():
    """Two panels. A single equirectangular map from Ma'rib to Rusafa crushes the
    whole Levantine leg into forty pixels, so the long arc and the short one are
    drawn at their own scales, side by side."""
    W, H = 860, 600
    LW, RW = 320, 452           # panel widths
    LX, RX = 46, 386            # panel left edges
    PT, PB = 92, 452            # panel top and bottom

    # ── panel A: the whole arc, four anchors only
    alon0, alon1, alat0, alat1 = 34.0, 47.0, 14.0, 36.5
    def A(lat, lon):
        return (LX + 34 + (lon - alon0) / (alon1 - alon0) * (LW - 54),
                PT + 14 + (alat1 - lat) / (alat1 - alat0) * (PB - PT - 34))
    arc = [(15.42, 45.33, 'Maʾrib', 'trad'), (21.42, 39.83, 'the Ḥijāz', 'trad'),
           (30.33, 35.60, 'Udhruḥ', 'trad'), (31.90, 35.20, 'Ramallah', 'att')]
    # ── panel B: the Levantine leg at its own scale
    blon0, blon1, blat0, blat1 = 34.92, 37.05, 30.10, 32.95
    def B(lat, lon):
        return (RX + 30 + (lon - blon0) / (blon1 - blon0) * (RW - 52),
                PT + 14 + (blat1 - lat) / (blat1 - blat0) * (PB - PT - 34))
    # (lat, lon, name, kind, dx, dy, anchor)
    leg = [(30.33, 35.60, 'Udhruḥ', 'trad', 10, 5, 'start'),
           (30.53, 35.56, 'al-Shawbak', 'trad', -10, 1, 'end'),
           (31.18, 35.70, 'al-Karak', 'att', 10, 4, 'start'),
           (31.68, 35.73, 'Maʿīn', 'att', 10, -4, 'start'),
           (31.87, 35.53, 'the ford of al-Lisān', 'trad', 10, -6, 'start'),
           (31.72, 35.19, 'Bayt Jālā', 'att', -10, 14, 'end'),
           (31.90, 35.20, 'Ramallah', 'att', -10, -4, 'end')]
    ghassan = [(32.52, 36.48, 'Bosra / the Ḥawrān', 9, 4, 'start'),
               (31.66, 35.83, 'Nitl', 12, 14, 'start')]
    arc_gh = [(35.63, 38.75, 'Ruṣāfa'), (32.52, 36.48, 'Bosra')]

    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" '
         f'aria-label="Two-panel map of the remembered migration route from Marib to Ramallah">']
    s.append(f'<rect width="{W}" height="{H}" fill="{SURF}"/>')
    s.append(txt(40, 34, 'THE ROAD, AS THE FAMILY REMEMBERS IT — AND THE GHASSANID GROUND IT PASSES',
                 11, GOLD, 'start', '700', 'normal', '1.3'))
    s.append(txt(40, 52, 'Drawn at two scales, because one map cannot hold both legs: the whole arc on the left, '
                 'the Transjordanian leg — where every station can be checked — on the right.',
                 10.5, GREY, 'start', '400', 'italic'))
    for x0, w, ttl in ((LX, LW, 'A · THE WHOLE ARC — 2,400 km'),
                       (RX, RW, 'B · THE LEG THAT CAN BE CHECKED — 200 km')):
        s.append(f'<rect x="{x0}" y="{PT}" width="{w}" height="{PB-PT}" fill="#FFFFFF" stroke="{RULE}" rx="4"/>')
        s.append(txt(x0 + 12, PT - 8, ttl, 8.8, GOLD, 'start', '700', 'normal', '1.2'))
    # panel A graticule + route
    for lat in range(16, 37, 4):
        _, y = A(lat, alon0)
        s.append(f'<line x1="{LX+6}" y1="{y:.1f}" x2="{LX+LW-6}" y2="{y:.1f}" stroke="{RULE}" stroke-width=".6"/>')
        s.append(txt(LX + 30, y + 3, f'{lat}°N', 7.6, FOLIO, 'end'))
    pts = ' '.join('%.1f,%.1f' % A(la, lo) for la, lo, _n, _k in arc)
    s.append(f'<polyline points="{pts}" fill="none" stroke="{RUST}" stroke-width="2.4" '
             f'stroke-dasharray="7 5" stroke-linejoin="round" opacity=".85"/>')
    for la, lo, nm in arc_gh:
        x, y = A(la, lo)
        s.append(f'<rect x="{x-4:.1f}" y="{y-4:.1f}" width="8" height="8" fill="none" '
                 f'stroke="{PLUM}" stroke-width="1.6" transform="rotate(45 {x:.1f} {y:.1f})"/>')
        s.append(txt(x + 9, y + (4 if nm == 'Ruṣāfa' else -7), esc(nm), 9.4, PLUM, 'start', '700'))
    for la, lo, nm, k in arc:
        x, y = A(la, lo)
        col = GREEN if k == 'att' else RUST
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{col}" stroke="#FFFFFF" stroke-width="1.6"/>')
        s.append(txt(x + 9, y + 4, esc(nm), 10, INK, 'start', '700'))
    # the box showing what panel B magnifies
    bx0, by0 = A(blat1, blon0); bx1, by1 = A(blat0, blon1)
    s.append(f'<rect x="{bx0:.1f}" y="{by0:.1f}" width="{bx1-bx0:.1f}" height="{by1-by0:.1f}" '
             f'fill="none" stroke="{GOLD}" stroke-width="1.6" stroke-dasharray="4 3"/>')
    s.append(f'<line x1="{bx1:.1f}" y1="{by0:.1f}" x2="{RX}" y2="{PT}" stroke="{GOLD}" stroke-width=".9" stroke-dasharray="3 3" opacity=".7"/>')
    s.append(f'<line x1="{bx1:.1f}" y1="{by1:.1f}" x2="{RX}" y2="{PB}" stroke="{GOLD}" stroke-width=".9" stroke-dasharray="3 3" opacity=".7"/>')
    # panel B graticule + route
    for lat in range(31, 33):
        _, y = B(lat, blon0)
        s.append(f'<line x1="{RX+6}" y1="{y:.1f}" x2="{RX+RW-6}" y2="{y:.1f}" stroke="{RULE}" stroke-width=".6"/>')
        s.append(txt(RX + 26, y + 3, f'{lat}°N', 7.6, FOLIO, 'end'))
    jx, _ = B(31.9, 35.52)
    s.append(f'<line x1="{jx:.1f}" y1="{PT+8}" x2="{jx:.1f}" y2="{PB-8}" stroke="#D8E4E9" stroke-width="6"/>')
    s.append(txt(jx - 6, PB - 14, 'the rift — Dead Sea and Jordan', 8.6, '#7C99A6', 'end', '400', 'italic'))
    pts = ' '.join('%.1f,%.1f' % B(la, lo) for la, lo, _n, _k, _a, _b, _c in leg)
    s.append(f'<polyline points="{pts}" fill="none" stroke="{RUST}" stroke-width="2.4" '
             f'stroke-dasharray="7 5" stroke-linejoin="round" opacity=".85"/>')
    for la, lo, nm, dx, dy, anc in ghassan:
        if not (blat0 <= la <= blat1 and blon0 <= lo <= blon1):
            continue
        x, y = B(la, lo)
        s.append(f'<rect x="{x-4:.1f}" y="{y-4:.1f}" width="8" height="8" fill="none" '
                 f'stroke="{PLUM}" stroke-width="1.8" transform="rotate(45 {x:.1f} {y:.1f})"/>')
        s.append(txt(x + dx, y + dy, esc(nm), 9.8, PLUM, anc, '700'))
    for la, lo, nm, k, dx, dy, anc in leg:
        x, y = B(la, lo)
        col = GREEN if k == 'att' else RUST
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" fill="{col}" stroke="#FFFFFF" stroke-width="1.6"/>')
        s.append(txt(x + dx, y + dy, esc(nm), 10.4, INK, anc, '700'))
    ly = PB + 34
    s.append(f'<circle cx="52" cy="{ly}" r="5" fill="{RUST}"/>')
    s.append(txt(64, ly + 4, 'remembered station — tradition only', 10, BODY))
    s.append(f'<circle cx="332" cy="{ly}" r="5" fill="{GREEN}"/>')
    s.append(txt(344, ly + 4, 'attested in an Ottoman register', 10, BODY))
    s.append(f'<rect x="620" y="{ly-4}" width="8" height="8" fill="none" stroke="{PLUM}" stroke-width="1.8" transform="rotate(45 624 {ly})"/>')
    s.append(txt(636, ly + 4, 'Ghassanid site with standing evidence', 10, BODY))
    s.append(f'<line x1="40" y1="{ly+18}" x2="{W-40}" y2="{ly+18}" stroke="{RULE}"/>')
    s.append(txt(40, ly + 38, 'Nitl lies a few kilometres from Maʿīn — the best physical evidence for Ghassanid Christianity sits on the road the family remembers.', 10.4, BODY, 'start', '700'))
    s.append(txt(40, ly + 54, 'Panel A is drawn at roughly one-twelfth the scale of panel B. The gold box on A is the ground panel B enlarges.', 10.2, GREY, 'start', '400', 'italic'))
    s.append('</svg>')
    return ''.join(s)

# ═════════════════════════════ FIGURE 6 — the dam dates
def fig_dam():
    W, H = 860, 190
    x0, x1 = 90, 800
    t0, t1 = 250, 650
    def px(y): return x0 + (x1 - x0) * (y - t0) / (t1 - t0)
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="The tradition dates the departure to about 300 AD; the dam breaches are fifth and sixth century">']
    s.append(f'<rect width="{W}" height="{H}" fill="{SURF}"/>')
    s.append(txt(40, 30, 'THE DAM, AND A DATE THAT HAS TO MOVE', 11, GOLD, 'start', '700', 'normal', '1.4'))
    y = 96
    s.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{RULE}" stroke-width="2"/>')
    for yr in range(250, 651, 50):
        s.append(f'<line x1="{px(yr):.1f}" y1="{y}" x2="{px(yr):.1f}" y2="{y+6}" stroke="{FOLIO}"/>')
        s.append(txt(px(yr), y + 20, str(yr), 9.5, FOLIO, 'middle'))
    # tradition
    s.append(f'<circle cx="{px(300):.1f}" cy="{y}" r="7" fill="{RUST}" stroke="#FFFFFF" stroke-width="2"/>')
    s.append(txt(px(300), y - 34, 'the tradition', 10.5, RUST, 'middle', '700'))
    s.append(txt(px(300), y - 20, '“about 300 AD”', 10, RUST, 'middle', '400', 'italic'))
    # recorded breaches
    for a, b, lab in [(449, 450, '449–450'), (543, 548, '543–548')]:
        xa, xb = px(a), px(b)
        s.append(f'<rect x="{xa-3:.1f}" y="{y-11}" width="{max(xb-xa,6)+6:.1f}" height="22" fill="{GREEN}" rx="4"/>')
        s.append(txt((xa + xb) / 2, y + 40, lab, 10.5, GREEN, 'middle', '700'))
    s.append(txt(px(600), y + 40, 'final collapse', 10.5, GREEN, 'middle', '700'))
    s.append(f'<circle cx="{px(600):.1f}" cy="{y}" r="6" fill="{GREEN}" opacity=".5"/>')
    # abraha
    s.append(f'<line x1="{px(548):.1f}" y1="{y-11}" x2="{px(548):.1f}" y2="{y-46}" stroke="{GREEN}" stroke-width="1.2"/>')
    s.append(txt(px(548), y - 52, 'Abraha’s repair inscription, CIH 541 (548 CE)', 10, GREEN, 'middle', '700'))
    s.append(txt(40, H - 24, 'A correction, not a demolition: the migration tradition survives, and the century attached to it moves forward by 150–250 years.', 10.5, BODY, 'start', '700'))
    s.append('</svg>')
    return ''.join(s)

# ═════════════════════════════ FIGURE 7 — the district map
def fig_map_district():
    W, H = 860, 520
    lon0, lon1, lat0, lat1 = 34.98, 35.40, 31.66, 32.08
    def P(lat, lon):
        x = 70 + (lon - lon0) / (lon1 - lon0) * (W - 150)
        y = 76 + (lat1 - lat) / (lat1 - lat0) * (H - 150)
        return x, y
    sites = [
        (31.900, 35.204, 'Ramallah', 'town', 0),
        (31.910, 35.220, 'al-Bīra', 'frank', 1),
        (31.893, 35.180, 'Khirbet et-Tireh', 'dig', 0),
        (31.962, 35.220, 'Jifnā', 'insc', 1),
        (32.030, 35.070, 'ʿAbūd', 'dig', 0),
        (31.720, 35.190, 'Bayt Jālā', 'town', 0),
        (31.780, 35.220, 'Jerusalem', 'ref', 1),
        (31.925, 35.262, 'et-Tell (Ai)', 'setaside', 1),
        (31.930, 35.240, 'Beitin', 'setaside', 0),
        (32.020, 35.080, 'Dayr Ghassāna', 'throne', 1),
        (31.930, 35.110, 'Rās Karkar', 'throne', 0),
        (31.972, 35.190, 'Bīr Zayt', 'vill', 1),
        (31.950, 35.310, 'Ṭayyibat al-Ism', 'vill', 1),
    ]
    STY = {'town': (GREEN, 6.5), 'dig': (GREEN, 5.5), 'frank': (PLUM, 5.5), 'insc': (PLUM, 5),
           'throne': (RUST, 5), 'setaside': (FOLIO, 4.5), 'vill': (FOLIO, 4), 'ref': (GREY, 4)}
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Map of Ramallah and the villages of its district">']
    s.append(f'<rect width="{W}" height="{H}" fill="{SURF}"/>')
    s.append(txt(40, 34, 'THE HILLS AROUND RAMALLAH — WHAT HAS BEEN DUG, WHAT WAS WRITTEN, WHO RULED', 11, GOLD, 'start', '700', 'normal', '1.3'))
    s.append(txt(40, 52, 'The watershed ridge road runs north–south through al-Bīra; the district was administratively split along it.', 10.5, GREY, 'start', '400', 'italic'))
    # ridge road
    ridge = [(31.70, 35.20), (31.78, 35.22), (31.91, 35.222), (31.96, 35.222), (32.06, 35.24)]
    pts = ' '.join(f'{P(a,b)[0]:.1f},{P(a,b)[1]:.1f}' for a, b in ridge)
    s.append(f'<polyline points="{pts}" fill="none" stroke="{GOLD}" stroke-width="9" opacity=".22" stroke-linecap="round"/>')
    s.append(txt(P(32.06, 35.24)[0] + 6, P(32.06, 35.24)[1] - 6, 'the ridge road', 10, GOLD, 'start', '700'))
    # the 2 km circle around Ramallah
    rx, ry = P(31.900, 35.204)
    r2 = abs(P(31.900, 35.204)[0] - P(31.900, 35.225)[0])
    s.append(f'<circle cx="{rx:.1f}" cy="{ry:.1f}" r="{r2:.1f}" fill="none" stroke="{GREEN}" stroke-width="1" stroke-dasharray="4 4" opacity=".7"/>')
    for la, lo, nm, k, side in sites:
        x, y = P(la, lo)
        col, r = STY[k]
        if k == 'setaside':
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="none" stroke="{col}" stroke-width="1.6"/>')
        else:
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{col}" stroke="#FFFFFF" stroke-width="1.4"/>')
        dx, anc = (r + 6, 'start') if side == 1 else (-(r + 6), 'end')
        w = '700' if k in ('town', 'dig') else '400'
        s.append(txt(x + dx, y + 4, nm, 10.5 if k == 'town' else 10, INK if k != 'setaside' else FOLIO, anc, w))
    # legend
    ly = H - 62
    leg = [(GREEN, 'excavated by Palestinian archaeologists', 52),
           (PLUM, 'named in a medieval document or inscription', 350),
           (RUST, 'throne village — a shaykhly seat', 640)]
    for col, lab, lx in leg:
        s.append(f'<circle cx="{lx}" cy="{ly}" r="5" fill="{col}"/>')
        s.append(txt(lx + 12, ly + 4, lab, 9.6, BODY))
    s.append(f'<circle cx="52" cy="{ly+20}" r="5" fill="none" stroke="{FOLIO}" stroke-width="1.6"/>')
    s.append(txt(64, ly + 24, 'biblical-archaeology excavation — data used, framing set aside', 9.6, BODY))
    s.append(txt(350, ly + 24, 'dashed circle: two kilometres from the town centre', 9.6, GREY, 'start', '400', 'italic'))
    s.append('</svg>')
    return ''.join(s)

# ═════════════════════════════ FIGURE 8 — five datings
def fig_datings():
    W, H = 860, 350
    x0, x1 = 90, 790
    t0, t1 = 1250, 1650
    def px(y): return x0 + (x1 - x0) * (y - t0) / (t1 - t0)
    # (year, label, grade, above?, extra offset rank — keeps neighbours apart)
    items = [(1279, 'Rām Allāh is a named place with surveyed boundaries in a Qalāwūn waqf', 'documents', 0, 0),
             (1495, 'Mujīr al-Dīn does not mention it — the verified negative', 'none', 1, 1),
             (1539, 'an inhabited village of four Muslim families, in the defter', 'documents', 0, 0),
             (1562, 'Christian households recorded — the traditional founding', 'documents', 1, 0),
             (1610, 'Rāshid buys khirbat Rām Allāh from the Ghazāwina (al-Dabbāgh)', 'oral', 0, 1)]
    COL = {'documents': GREEN, 'none': VOIDE, 'oral': RUST}
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Five datings for the founding of Ramallah">']
    s.append(f'<rect width="{W}" height="{H}" fill="{SURF}"/>')
    s.append(txt(40, 32, 'FIVE DATINGS, RARELY SET AGAINST ONE ANOTHER', 11, GOLD, 'start', '700', 'normal', '1.4'))
    y = 168
    s.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{RULE}" stroke-width="2"/>')
    for yr in range(1250, 1651, 50):
        s.append(f'<line x1="{px(yr):.1f}" y1="{y}" x2="{px(yr):.1f}" y2="{y+6}" stroke="{FOLIO}"/>')
        s.append(txt(px(yr), y + 20, str(yr), 9.5, FOLIO, 'middle'))
    for yr, lab, g, up, rank in items:
        x = px(yr)
        col = COL[g]
        step = 46 * rank
        ty = (y - 30 - step) if up else (y + 44 + step)
        s.append(f'<line x1="{x:.1f}" y1="{y}" x2="{x:.1f}" y2="{ty + (10 if up else -10):.1f}" stroke="{col}" stroke-width="1.2"/>')
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{col}" stroke="#FFFFFF" stroke-width="2"/>')
        s.append(txt(x, ty - (4 if up else -4), str(yr) if yr != 1610 else 'c. 1600s', 12, col, 'middle', '700'))
        # wrap label
        words, line, lines = lab.split(), '', []
        for w in words:
            if len(line + ' ' + w) > 32:
                lines.append(line); line = w
            else:
                line = (line + ' ' + w).strip()
        lines.append(line)
        for j, ln in enumerate(lines):
            yy = ty - 18 - (len(lines) - 1 - j) * 12 if up else ty + 14 + j * 12
            s.append(txt(x, yy, esc(ln), 9.4, BODY, 'middle'))
    s.append(f'<line x1="40" y1="{H-40}" x2="{W-40}" y2="{H-40}" stroke="{RULE}"/>')
    s.append(txt(40, H - 20, 'The reconciliation: an old toponym on waqf-held ground, repopulated in stages, of which the Christian arrival of 1562 is one late layer.', 10.5, BODY, 'start', '700'))
    s.append('</svg>')
    return ''.join(s)

# ═════════════════════════════ FIGURE 9 — households 1525–1596
def fig_households():
    W, H = 860, 300
    data = [(1525, 0, 0, 'uninhabited — waqf land of the Ibrāhīmī endowment'),
            (1538, 0, 4, 'four Muslim households'),
            (1553, 0, 6, 'six Muslim households; the Kasābra counted at Bayt Jālā'),
            (1562, 37, 10, 'the Christians arrive from Bayt Jālā'),
            (1596, 71, 9, 'eighty households, seventy-one Christian')]
    x0, y0, plotw, ploth = 100, 76, 480, 150
    mx = 84
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Households at Ramallah in the Ottoman registers, 1525 to 1596">']
    s.append(f'<rect width="{W}" height="{H}" fill="{SURF}"/>')
    s.append(txt(40, 34, 'WHAT THE REGISTERS ACTUALLY SAY — HOUSEHOLDS AT RAMALLAH, 1525–1596', 11, GOLD, 'start', '700', 'normal', '1.3'))
    s.append(txt(40, 52, 'The founding is not a moment of arrival on empty ground. It is a Christian settlement onto a site the state already taxed.', 10.5, GREY, 'start', '400', 'italic'))
    bw = 52
    for i, (yr, ch, mu, note) in enumerate(data):
        x = x0 + i * (plotw / len(data))
        tot = ch + mu
        hch = ploth * ch / mx
        hmu = ploth * mu / mx
        yb = y0 + ploth
        if mu:
            s.append(f'<rect x="{x:.1f}" y="{yb-hmu:.1f}" width="{bw}" height="{hmu:.1f}" fill="{RUST}" rx="3"/>')
        if ch:
            s.append(f'<rect x="{x:.1f}" y="{yb-hmu-hch-2:.1f}" width="{bw}" height="{hch:.1f}" fill="{GREEN}" rx="3"/>')
            s.append(txt(x + bw / 2, yb - hmu - hch - 8, str(ch), 11, GREEN, 'middle', '700'))
        if mu:
            s.append(txt(x + bw / 2, yb - hmu / 2 + 4, str(mu), 10, '#FFFFFF', 'middle', '700'))
        if tot == 0:
            s.append(f'<line x1="{x:.1f}" y1="{yb:.1f}" x2="{x+bw:.1f}" y2="{yb:.1f}" stroke="{VOIDE}" stroke-width="3"/>')
            s.append(txt(x + bw / 2, yb - 8, '0', 11, VOIDT, 'middle', '700'))
        s.append(txt(x + bw / 2, yb + 18, str(yr), 10.5, INK, 'middle', '700'))
    s.append(f'<line x1="{x0-8}" y1="{y0+ploth:.1f}" x2="{x0+plotw:.1f}" y2="{y0+ploth:.1f}" stroke="{RULE}"/>')
    # legend + notes
    s.append(f'<rect x="620" y="80" width="13" height="13" fill="{GREEN}" rx="2"/>')
    s.append(txt(640, 91, 'Christian households', 10.5, BODY))
    s.append(f'<rect x="620" y="102" width="13" height="13" fill="{RUST}" rx="2"/>')
    s.append(txt(640, 113, 'Muslim households', 10.5, BODY))
    notes = ['1525 · waqf land of Hebron, 3,000 aqja,', 'no households at all',
             '1562 · 27 families and 8 unmarried men', 'come up from Bayt Jālā — the founding',
             '1596 · taxed at a quarter, 9,400 aqja']
    for j, n in enumerate(notes):
        s.append(txt(620, 146 + j * 15, esc(n), 9.6, GREY if j % 2 else BODY))
    s.append(txt(40, H - 18, 'Two corrections follow: the founding is 1562, not “about 1550” — and the movers were a generation or two below Rāshid.', 10.5, BODY, 'start', '700'))
    s.append('</svg>')
    return ''.join(s)

# ═════════════════════════════ FIGURE 10 — the 1596 neighbourhood
def fig_neighbourhood():
    W, H = 860, 400
    vills = [('Bayt Jālā', 239, 6), ('Ṭayyibat al-Ism', 23, 63), ('Ramallah', 71, 9),
             ('al-Bīra al-Kubrā', 0, 45), ('Bīr Zayt', 0, 26), ('Jifnā', 0, 21)]
    x0, y0 = 190, 78
    plotw = 470
    mx = 250
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Households by village in the register of 1596">']
    s.append(f'<rect width="{W}" height="{H}" fill="{SURF}"/>')
    s.append(txt(40, 34, 'RAMALLAH IN ITS NEIGHBOURHOOD, 1596', 11, GOLD, 'start', '700', 'normal', '1.4'))
    s.append(txt(40, 52, 'Thirty-four years after the founding, the last Ottoman register of the century counts every village in these hills.', 10.5, GREY, 'start', '400', 'italic'))
    bh, gap = 26, 12
    for i, (nm, ch, mu) in enumerate(vills):
        y = y0 + i * (bh + gap)
        wc = plotw * ch / mx
        wm = plotw * mu / mx
        s.append(txt(x0 - 14, y + 18, nm, 11, INK if nm == 'Ramallah' else BODY, 'end', '700' if nm == 'Ramallah' else '400'))
        if ch:
            s.append(f'<rect x="{x0}" y="{y}" width="{wc:.1f}" height="{bh}" fill="{GREEN}" rx="3"/>')
        if mu:
            s.append(f'<rect x="{x0+wc+(2 if ch else 0):.1f}" y="{y}" width="{wm:.1f}" height="{bh}" fill="{RUST}" rx="3"/>')
        if ch and wc > 30:
            s.append(txt(x0 + wc / 2, y + 18, str(ch), 10.5, '#FFFFFF', 'middle', '700'))
        if mu and wm > 26:
            s.append(txt(x0 + wc + wm / 2, y + 18, str(mu), 10.5, '#FFFFFF', 'middle', '700'))
        s.append(txt(x0 + wc + wm + 12, y + 18, f'{ch+mu} households', 10, GREY, 'start'))
        if nm == 'Ramallah':
            s.append(f'<rect x="{x0-150}" y="{y-4}" width="{plotw+220}" height="{bh+8}" fill="none" stroke="{GREEN}" stroke-width="1" stroke-dasharray="3 3" rx="4" opacity=".55"/>')
    ly = y0 + len(vills) * (bh + gap) + 8
    s.append(f'<rect x="{x0}" y="{ly}" width="13" height="13" fill="{GREEN}" rx="2"/>')
    s.append(txt(x0 + 20, ly + 11, 'Christian households', 10.5, BODY))
    s.append(f'<rect x="{x0+180}" y="{ly}" width="13" height="13" fill="{RUST}" rx="2"/>')
    s.append(txt(x0 + 200, ly + 11, 'Muslim households', 10.5, BODY))
    s.append(f'<line x1="40" y1="{H-54}" x2="{W-40}" y2="{H-54}" stroke="{RULE}"/>')
    s.append(txt(40, H - 30, 'Ramallah is one of only two substantially Christian villages in this stretch of hill country —', 10.5, BODY, 'start', '700'))
    s.append(txt(40, H - 14, 'and the other one is the village its settlers came from. Bayt Jālā is not a stage on the road; it is the parent community.', 10.5, BODY, 'start', '700'))
    s.append('</svg>')
    return ''.join(s)

# ═════════════════════════════ FIGURE 11 — population, log
def fig_pop():
    W, H = 860, 420
    pts = [(1596, 400, 'e'), (1838, 850, 'e'), (1870, 1100, 'e'), (1896, 2061, 'e'),
           (1922, 3104, 'c'), (1931, 4286, 'c'), (1945, 5080, 'c'), (1961, 14759, 'c'),
           (1967, 12134, 'c'), (1997, 17851, 'c'), (2007, 27460, 'c'), (2017, 38998, 'c'),
           (2024, 43880, 'p')]
    x0, x1, yb, yt = 92, 800, 316, 84
    t0, t1 = 1580, 2035
    v0, v1 = 300, 60000
    def px(y): return x0 + (x1 - x0) * (y - t0) / (t1 - t0)
    def py(v): return yb - (yb - yt) * (math.log10(v) - math.log10(v0)) / (math.log10(v1) - math.log10(v0))
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Every recorded population figure for Ramallah, 1596 to 2024, on a log scale">']
    s.append(f'<rect width="{W}" height="{H}" fill="{SURF}"/>')
    s.append(txt(40, 34, 'EVERY NUMBER ANYONE HAS EVER RECORDED, 1596–2024', 11, GOLD, 'start', '700', 'normal', '1.4'))
    s.append(txt(40, 52, 'A logarithmic scale, because the town multiplied by more than a hundred.', 10.5, GREY, 'start', '400', 'italic'))
    # era bands
    for a, b, lab in [(1917, 1948, 'British Mandate'), (1967, 1994, 'occupation before the Authority')]:
        s.append(f'<rect x="{px(a):.1f}" y="{yt}" width="{px(b)-px(a):.1f}" height="{yb-yt}" fill="{GOLD}" opacity=".10"/>')
        s.append(txt((px(a) + px(b)) / 2, yt - 6, lab, 9, GOLD, 'middle', '700'))
    for v in (500, 1000, 5000, 10000, 50000):
        s.append(f'<line x1="{x0}" y1="{py(v):.1f}" x2="{x1}" y2="{py(v):.1f}" stroke="{RULE}" stroke-width=".8"/>')
        s.append(txt(x0 - 10, py(v) + 4, f'{v:,}', 9.5, FOLIO, 'end'))
    for yr in range(1600, 2001, 100):
        s.append(txt(px(yr), yb + 20, str(yr), 9.5, FOLIO, 'middle'))
        s.append(f'<line x1="{px(yr):.1f}" y1="{yb}" x2="{px(yr):.1f}" y2="{yb+6}" stroke="{FOLIO}"/>')
    line = ' '.join(f'{px(y):.1f},{py(v):.1f}' for y, v, _ in pts)
    s.append(f'<polyline points="{line}" fill="none" stroke="{GREEN}" stroke-width="2" stroke-linejoin="round"/>')
    for y, v, k in pts:
        x, yy = px(y), py(v)
        if k == 'c':
            s.append(f'<circle cx="{x:.1f}" cy="{yy:.1f}" r="4.5" fill="{GREEN}" stroke="#FFFFFF" stroke-width="1.6"/>')
        elif k == 'e':
            s.append(f'<circle cx="{x:.1f}" cy="{yy:.1f}" r="4.5" fill="{SURF}" stroke="{GREEN}" stroke-width="2"/>')
        else:
            s.append(f'<circle cx="{x:.1f}" cy="{yy:.1f}" r="4.5" fill="{FOLIO}" stroke="#FFFFFF" stroke-width="1.6"/>')
    for y, v, lab, dy in [(1596, 400, '400', -12), (1922, 3104, '3,104', -12), (1945, 5080, '5,080', 16),
                          (1961, 14759, '14,759', -12), (1967, 12134, '12,134 — the dip is real', 22),
                          (2017, 38998, '38,998', -12)]:
        s.append(txt(px(y), py(v) + dy, lab, 10, INK, 'middle', '700'))
    ly = H - 56
    s.append(f'<circle cx="52" cy="{ly}" r="4.5" fill="{GREEN}" stroke="#FFFFFF" stroke-width="1.6"/>')
    s.append(txt(64, ly + 4, 'an enumeration', 10, BODY))
    s.append(f'<circle cx="200" cy="{ly}" r="4.5" fill="{SURF}" stroke="{GREEN}" stroke-width="2"/>')
    s.append(txt(212, ly + 4, 'an estimate, or a count of houses or taxable men', 10, BODY))
    s.append(f'<circle cx="560" cy="{ly}" r="4.5" fill="{FOLIO}"/>')
    s.append(txt(572, ly + 4, 'projection', 10, BODY))
    s.append(txt(40, H - 20, 'The 1596 figure assumes five people to a household. The 1967 fall is emigration after the occupation, not a counting error.', 10.5, BODY, 'start', '700'))
    s.append('</svg>')
    return ''.join(s)

# ═════════════════════════════ FIGURE 12 — the sex ratio
def fig_sex():
    W, H = 260, 250
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Men and women at Ramallah in the 1931 census">']
    s.append(f'<rect width="{W}" height="{H}" fill="{SURF}"/>')
    s.append(txt(20, 28, 'RAMALLAH, 1931', 10, GOLD, 'start', '700', 'normal', '1.4'))
    men, women = 1941, 2345
    mx = 2500
    bw, x0, yb = 56, 60, 190
    for i, (lab, v, col) in enumerate([('men', men, RUST), ('women', women, GREEN)]):
        h = 130 * v / mx
        x = x0 + i * 92
        s.append(f'<rect x="{x}" y="{yb-h:.1f}" width="{bw}" height="{h:.1f}" fill="{col}" rx="3"/>')
        s.append(txt(x + bw / 2, yb - h - 8, f'{v:,}', 11, INK, 'middle', '700'))
        s.append(txt(x + bw / 2, yb + 18, lab, 10.5, BODY, 'middle'))
    s.append(txt(20, 224, '404 more women than men —', 10, BODY, 'start', '700'))
    s.append(txt(20, 238, 'emigration, visible in a census table.', 10, BODY))
    s.append('</svg>')
    return ''.join(s)


# ═════════════════════════════ FIGURE A — John's thirty-six generations
GENS = [
 (1,'Adam & Eve','آدم وحواء','s'),(2,'Sheath ibn Adam','شيث بن آدم','s'),
 (3,'Anoosh ibn Sheath','أنوش بن شيث','s'),(4,'Qinan ibn Anoosh','قينان بن أنوش','s'),
 (5,'Mihla’el ibn Qinan','مهلائيل بن قينان','s'),(6,'Elizad ibn Mihla’el','إليزاد بن مهلائيل','s'),
 (7,'Akhnoukh ibn Elizad','أخنوخ بن إليزاد','s'),(8,'Matoushlekh ibn Akhnoukh','متوشلخ بن أخنوخ','s'),
 (9,'Noah ibn Matoushlekh','نوح بن متوشلخ','s'),(10,'Sam ibn Noah','سام بن نوح','s'),
 (11,'Arfakhshid ibn Sam','أرفخشد بن سام','s'),(12,'Shaleikh ibn Arfakhshid','شالخ بن أرفخشد','s'),
 (13,'Aaber ibn Shaleikh','عابر بن شالخ','s'),(14,'Kahtaan ibn Aaber','قحطان بن عابر','j'),
 (15,'Ya‘rab ibn Kahtaan','يعرب بن قحطان','c'),(16,'Yashjib ibn Ya‘rab','يشجب بن يعرب','c'),
 (17,'Saba’ ibn Yashjib','سبأ بن يشجب','c'),(18,'Kahlan ibn Saba’','كهلان بن سبأ','c'),
 (19,'Zeid ibn Kahlan','زيد بن كهلان','c'),(20,'Malek ibn Zeid','مالك بن زيد','c'),
 (21,'Nabat ibn Malek','نبت بن مالك','c'),(22,'Algouth ibn Nabat','الغوث بن نبت','c'),
 (23,'Al-Ouzd ibn Algouth','الأزد بن الغوث','c'),(24,'Mazen al-Ouzd','مازن الأزد','c'),
 (25,'Tha‘labah bin Mazen al-Ouedi','ثعلبة بن مازن الأزدي','c'),
 (26,'Amro’ al-Qeis al-Ouedi','عمرو القيس الأزدي','c'),
 (27,'Haritha al-Ghatrif','حارثة الغطريف','c'),(28,'Amer Ma’ el-Sama’','عامر ماء السماء','c'),
 (29,'Amro Mazika al-Ghassani','عمرو مزيقيا الغساني','g'),
 (30,'Jafanah al-Ghassani','جفنة الغساني','g'),
 (31,'Tha‘alabah bin Jafanah','ثعلبة بن جفنة الغساني','g'),
 (32,'Al-Harith bin Tha‘alabah','الحارث بن ثعلبة الغساني','g'),
 (33,'Jabalah bin al-Harith','جبلة بن الحارث الغساني','a'),
 (34,'Al-Harith bin Jabalah','الحارث بن جبلة الغساني','a'),
 (35,'Unknown al-Ghassani — 45 generations','مجهول الغساني','v'),
 (36,'Rashed bin Essaye bin Eyad bin Dhahdouheh al-Ghassani','راشد الحدادين الغساني','d'),
]
def fig_gens():
    KIND = {'s':('#D5E9DF','#A9CDB8',INK,'scripture'),
            'j':('#8FBFA6','#3E9464',INK,'the join'),
            'c':('#A9CDB8','#79B491',INK,'classical'),
            'g':('#79B491','#3E9464',INK,'classical'),
            'a':('#3E9464','#007A3D','#FFFFFF','attested'),
            'v':(VOIDF,VOIDE,VOIDT,'no evidence'),
            'd':(GREEN,GREEN,'#FFFFFF','documents')}
    rows_per_col = 18
    colw, rh, top, left = 392, 25, 96, 36
    W, H = 860, top + rows_per_col*rh + 76
    s=[f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="The thirty-six named generations from Adam and Eve to Rashed">']
    s.append(f'<rect width="{W}" height="{H}" fill="{SURF}"/>')
    s.append(txt(left,34,'THIRTY-SIX NAMED GENERATIONS — ADAM &amp; EVE TO RĀSHID',11,GOLD,'start','700','normal','1.4'))
    s.append(txt(left,52,'Researched and compiled by John Aziz Mogannam. Each band is coloured by what holds that stretch of the chain.',10.5,GREY,'start','400','italic'))
    for idx,(n,en,ar,k) in enumerate(GENS):
        col, row = idx//rows_per_col, idx%rows_per_col
        x = left + col*(colw+20); y = top + row*rh
        fill,edge,tc,_ = KIND[k]
        w = colw if n!=36 else colw
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{rh-4}" fill="{fill}" stroke="{edge}" stroke-width=".8" rx="3"/>')
        if k=='v':
            s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{rh-4}" fill="url(#hatch2)" rx="3"/>')
        s.append(txt(x+9,y+15,str(n),9,tc,'start','700'))
        nm = en if len(en)<40 else en[:38]+'…'
        s.append(txt(x+30,y+15,esc(nm),9.6,tc,'start','700' if k in('a','d','v') else '400'))
        s.append(f'<text x="{x+w-9}" y="{y+15}" font-size="10.5" fill="{tc}" text-anchor="end" font-family="Times New Roman, Times, serif" xml:lang="ar">{ar}</text>')
    yb = top + rows_per_col*rh + 14
    for i,(k,lab) in enumerate([('s','scripture'),('c','classical scholarship'),('a','attested history'),('v','no evidence'),('d','documents')]):
        fill,edge,tc,_=KIND[k]; lx = left + i*160
        s.append(f'<rect x="{lx}" y="{yb}" width="13" height="13" fill="{fill}" stroke="{edge}" rx="2"/>')
        s.append(txt(lx+19,yb+11,lab,9.4,BODY))
    s.append(txt(left,yb+38,'Al-Ghassānī — the tribal name that survives in the family’s own subtitle — enters at generation 29, with ‘Amr Muzayqiyāʾ.',10.5,BODY,'start','700'))
    s.append(txt(left,yb+54,'Generation 35 is the void: one line standing for nine hundred years and, by the chart’s own count, forty-five generations. This book counts it as thirty-one, which makes the line sixty-six generations, not thirty-six.',10.5,BODY,'start','700'))
    s.append('<defs><pattern id="hatch2" width="6" height="6" patternTransform="rotate(45)" '
             f'patternUnits="userSpaceOnUse"><line x1="0" y1="0" x2="0" y2="6" stroke="{VOIDE}" stroke-width="1.2" opacity=".45"/></pattern></defs>')
    s.append('</svg>')
    return ''.join(s)

# ═════════════════════════════ FIGURE B — the Ḥaddādīn of Jordan
def fig_jordan():
    W,H = 860, 430
    lon0,lon1,lat0,lat1 = 34.9,36.6,30.2,32.9
    def P(la,lo):
        return (70+(lo-lon0)/(lon1-lon0)*(W-150), 76+(lat1-la)/(lat1-lat0)*(H-160))
    pl = [(32.49,35.87,'al-Ḥuṣn',1,6),(32.53,35.86,'Aydūn',1,-8),(32.40,35.72,'Kufr ʿAwān',0,0),
          (32.04,35.73,'al-Salṭ',1,0),(31.72,35.79,'Madaba',1,-8),(31.68,35.73,'Maʿīn',0,6),
          (31.18,35.70,'al-Karak',1,0),(31.13,35.73,'Ḥamūd',0,12),(30.53,35.56,'al-Shawbak',1,0),
          (30.33,35.60,'Udhruḥ',1,0)]
    ref = [(31.90,35.20,'Ramallah'),(32.70,35.30,'Nazareth')]
    s=[f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Where the Haddadin are recorded in Jordan">']
    s.append(f'<rect width="{W}" height="{H}" fill="{SURF}"/>')
    s.append(txt(40,34,'THE ḤADDĀDĪN IN JORDAN, AS PEAKE’S CLAN REGISTER HAS THEM',11,GOLD,'start','700','normal','1.3'))
    s.append(txt(40,52,'Not one family in one town — an old lineage scattered across the length of the country, with relatives in Nazareth.',10.5,GREY,'start','400','italic'))
    jx,_=P(31.5,35.55)
    s.append(f'<line x1="{jx:.1f}" y1="80" x2="{jx:.1f}" y2="{H-80}" stroke="{RULE}" stroke-width="8" opacity=".5"/>')
    s.append(txt(jx-8,96,'the Jordan',9.5,FOLIO,'end','400','italic'))
    for la,lo,nm in ref:
        x,y=P(la,lo)
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="none" stroke="{GREY}" stroke-width="1.6"/>')
        s.append(txt(x-8,y+4,nm,9.6,GREY,'end','400','italic'))
    for la,lo,nm,side,dy in pl:
        x,y=P(la,lo)
        big = nm in ('al-Karak','Ḥamūd')
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{6 if big else 4.6}" fill="{GREEN if big else RUST}" stroke="#FFFFFF" stroke-width="1.5"/>')
        dx,anc = (10,'start') if side else (-10,'end')
        s.append(txt(x+dx,y+4+dy,nm,10.4 if big else 10,INK,anc,'700' if big else '400'))
    ly=H-56
    s.append(f'<circle cx="52" cy="{ly}" r="6" fill="{GREEN}"/>')
    s.append(txt(64,ly+4,'named in the Karak clan register: “they dwell in al-Karak and the village of Ḥamūd”',10,BODY))
    s.append(f'<circle cx="52" cy="{ly+22}" r="4.6" fill="{RUST}"/>')
    s.append(txt(64,ly+26,'a Ḥaddādīn ḥamūla also recorded here — an old, fragmented lineage',10,BODY))
    s.append(txt(40,H-14,'The clan the family descends from is documented on the other side of the Jordan, in a register kept by another state.',10.5,BODY,'start','700'))
    s.append('</svg>')
    return ''.join(s)

# ═════════════════════════════ FIGURE C — the peoples of the land
def fig_peoples():
    W,H = 860, 400
    x0,x1 = 190, 800
    t0,t1 = -2000, 2025
    def px(y): return x0+(x1-x0)*(y-t0)/(t1-t0)
    bands = [
      ('Canaanite / Amorite', -2000, -1200, '#3E9464', 'city-states of the Amarna letters'),
      ('Philistine', -1175, -600, RUST, 'European-derived ancestry, gone within two centuries'),
      ('Israelite / Judahite', -1200, -586, '#8FBFA6', ''),
      ('Samaritan', -400, 2025, PLUM, 'continuous at Nablus to this day'),
      ('Aramaic-speaking Christian', 50, 1200, '#79B491', 'the villages of these hills'),
      ('Arabic-speaking Christian', 700, 2025, GREEN, 'ʿAbūd, Jifnā, Ṭayyiba — and Ramallah from 1562'),
    ]
    s=[f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="The peoples of this land, and how they overlap in time">']
    s.append(f'<rect width="{W}" height="{H}" fill="{SURF}"/>')
    s.append(txt(40,32,'THE PEOPLES OF THIS LAND DO NOT REPLACE ONE ANOTHER — THEY OVERLAP',11,GOLD,'start','700','normal','1.3'))
    s.append(txt(40,50,'Each band is a language and an identity, not a population replacement. The genetics now say the population beneath them is largely one.',10.5,GREY,'start','400','italic'))
    bh, top = 30, 78
    for i,(nm,a,b,col,note) in enumerate(bands):
        y = top+i*(bh+10)
        s.append(txt(x0-14,y+20,nm,10.6,INK,'end','700'))
        s.append(f'<rect x="{px(a):.1f}" y="{y}" width="{px(b)-px(a):.1f}" height="{bh}" fill="{col}" rx="4" opacity=".9"/>')
        if note:
            bw_ = px(b)-px(a)
            est = len(note)*4.5
            if est < bw_-14:
                s.append(txt(px(a)+8,y+19,esc(note),9.2,'#FFFFFF','start','400'))
            elif px(b)+10+est < x1+40:
                s.append(txt(px(b)+10,y+19,esc(note),9.2,GREY,'start','400','italic'))
            else:
                s.append(txt(px(a)-4,y+19,esc(note),9.2,GREY,'end','400','italic'))
    yb = top+len(bands)*(bh+10)+6
    s.append(f'<line x1="{x0}" y1="{yb}" x2="{x1}" y2="{yb}" stroke="{RULE}"/>')
    for yr in (-2000,-1500,-1000,-500,0,500,1000,1500,2000):
        s.append(f'<line x1="{px(yr):.1f}" y1="{yb}" x2="{px(yr):.1f}" y2="{yb+6}" stroke="{FOLIO}"/>')
        lab = f'{abs(yr)} BCE' if yr<0 else ('CE 1' if yr==0 else f'{yr} CE')
        s.append(txt(px(yr),yb+20,lab,9,FOLIO,'middle'))
    s.append(f'<line x1="{px(1562):.1f}" y1="{top-8}" x2="{px(1562):.1f}" y2="{yb}" stroke="{GOLD}" stroke-width="1.4" stroke-dasharray="4 3"/>')
    s.append(txt(px(1562),top-14,'1562',9.6,GOLD,'middle','700'))
    s.append(txt(40,yb+48,'The family joins a landscape continuously inhabited for four thousand years.',10.5,BODY,'start','700'))
    s.append(txt(40,yb+64,'It does not arrive on empty ground — nobody ever did.',10.5,BODY,'start','700'))
    s.append('</svg>')
    return ''.join(s)


# ═════════════════════════════ document
FIGS = {}
FIGS['master'] = fig(fig_master(), 1, 'The whole story, graded',
    'Eight stretches, each coloured by what actually holds it up. The hatched band is the void — nine hundred years for which no record of any kind has been found.',
    'After The History of Ramallah v1, slides 3 and 49.')
FIGS['chron'] = fig(fig_chron(), 2, 'A line to Adam implies a date for Adam',
    'The three surviving forms of the Old Testament give systematically different ages for the patriarchs, and so different dates for the creation.',
    'Genesis 5 and 11 in the Masoretic, Septuagint and Samaritan recensions.')
FIGS['chain'] = fig(fig_chain(), 3, 'The chain, link by link',
    'Seven links carry the family from Adam to Ramallah. They do not rest on the same kind of thing, and one of them rests on nothing at all.',
    'Genesis; al-Ṭabarī; Ibn al-Kalbī, Ibn Ḥazm, Ibn Durayd; Procopius; the Ottoman registers.')
FIGS['arith'] = fig(fig_arith(), 4, 'Forty-five is the wrong number',
    'Before looking for the missing generations it is worth checking the count. It does not fit the gap it is meant to fill.',
    'Generational-interval range after the standard genealogical-demography literature.')
FIGS['mapreg'] = fig(fig_map_region(), 5, 'The road, and the ground it passes',
    'The remembered route from Maʾrib to the ridge, with the Ghassanid sites that have standing physical evidence marked separately.',
    'Hammoudeh, JQ 59 (2014), 43, 45 and 52 n. 57; Peake, Karak clan register; the Ghassanid inscriptions.')
FIGS['dam'] = fig(fig_dam(), 6, 'The dam, and a date that has to move',
    'The family dates the departure to the bursting of the Maʾrib dam, about 300 AD. The dam is real and its breaches are dated — and they are two centuries later.',
    'Nebes, PSAS 34 (2004), 221–230; CIH 541 in the DASI corpus.')
FIGS['mapdis'] = fig(fig_map_district(), 7, 'The hills around Ramallah',
    'What has been excavated, what was written down, and who ruled — within a few kilometres of the town.',
    'al-Houdalieh; Taha; Pringle; Bresc-Bautier; Riwaq; Conder & Kitchener.')
FIGS['datings'] = fig(fig_datings(), 8, 'Five datings for one founding',
    'Each is well-founded; they have rarely been set against one another. Read together they describe a site repopulated in stages, not founded once.',
    'Jerusalem sijill 48, p. 54; Mujīr al-Dīn; the defters; Hammoudeh; al-Dabbāgh.')
FIGS['hh'] = fig(fig_households(), 9, 'What the registers actually say',
    'Households at Ramallah across five Ottoman registers. The site is taxed before it is inhabited, inhabited before it is Christian, and Christian from 1562.',
    'Hammoudeh, “New Light on Ramallah’s Origins in the Ottoman Period,” JQ 59 (2014), 40–46.')
FIGS['nbhd'] = fig(fig_neighbourhood(), 10, 'Ramallah in its neighbourhood, 1596',
    'The last Ottoman register of the century, village by village. Note that Toledano read Jifnā’s 21 households as Christian against Hütteroth’s Muslim; the confessional column is not always reliable.',
    'Hütteroth & Abdulfattah, Historical Geography of Palestine, Transjordan and Southern Syria (Erlangen, 1977), 116 and 121.')
FIGS['pop'] = fig(fig_pop(), 11, 'Every number anyone has ever recorded',
    'Four centuries of counting, on a logarithmic scale. Hollow points are estimates or counts of houses and taxable men; solid points are enumerations.',
    'Hütteroth & Abdulfattah 1977, 121 · Robinson & Smith 1841, ii, 133–34 · Socin, ZDPV 2 (1879), 158 · Schick, ZDPV 19 (1896), 121 · Barron 1922, 16 · Mills 1931 · Village Statistics 1945 · Jordanian census 1961 · Israeli census 1967 · PCBS 1997, 2007, 2017, 2024.')
FIGS['sex'] = fig_sex()
FIGS['gens'] = fig(fig_gens(), 13, 'The thirty-six named generations',
    'John Aziz Mogannam’s chart, set out in full and coloured by the evidence behind each stretch. This is the family’s own document — the thing every other page in this history is trying to test.',
    'Researched and compiled by John Aziz Mogannam; the deep lineage after al-Suwaydī, Sabāʾik al-dhahab, and Wüstenfeld’s Genealogische Tabellen.')
FIGS['jordan'] = fig(fig_jordan(), 14, 'The Ḥaddādīn in Jordan',
    'Where the clan is actually recorded east of the river — not one family in one town, but an old lineage scattered the length of the country.',
    'F. G. Peake, Tārīkh sharqī al-Urdunn wa-qabāʾiluhā, the Karak clan register; al-ʿAzīzī, Muʿlamat al-turāth al-Urdunī.')
FIGS['peoples'] = fig(fig_peoples(), 15, 'The peoples of this land overlap',
    'Canaanite, Philistine, Israelite, Samaritan, Aramaic-Christian, Arabic-Christian — bands of language and identity, not successive populations. The 1562 line marks where this family enters a story already four thousand years old.',
    'Feldman et al., Science Advances 5:7 (2019); Agranat-Tamir et al., Cell 181 (2020); Haber et al., AJHG 101:2 (2017); Masalha, Palestine: A Four Thousand Year History (2018).')

print('figures built')

# ═════════════════════════════ narrative
def S(title, kicker, body, figkey=None, figafter=True):
    f = FIGS.get(figkey, '') if figkey else ''
    return (f'<section class="sec"><h3 class="kick">{kicker}</h3><h2>{title}</h2>'
            + (body + f if figafter else f + body) + '</section>')

PARTS = []

# ── PART ONE
PARTS.append(('One', 'The Line', 'Where the family says it comes from, who made the claim, and what a genealogy of this kind was for.', f"""
<p>The family chart begins with Adam. Before anything else is said about it, the form should be
recognised for what it is. Medieval peoples across three continents wrote their descent back to a
universal ancestor: the House of Wessex to Woden and thence to Noah in the <em>Anglo-Saxon
Chronicle</em> under the year 855{c('<em>The Anglo-Saxon Chronicle</em>, s.a. 855, the genealogy of Æthelwulf.')}; the Irish to Míl; the Georgian
kings to a grandson of Noah. <strong>What such a chart asserts is membership in the human story,
not a chain of verified fathers.</strong> Reading it as the latter and finding it wanting is a
category error.</p>

<p>Seven links carry the chart from Adam to Ramallah, and they do not rest on the same kind of thing.
The first twenty generations — Adam to Eber — are Genesis 5 and 11{c('Genesis 5:1–32; 11:10–26.')}. The three surviving
recensions of that text disagree with one another about the ages of the patriarchs, and therefore
about the date of the creation, by as much as 1,366 years (Figure 2). For a Rūm Orthodox family the
Septuagint reckoning is the inherited one, which is itself a piece of family history{c('The Byzantine <em>anno mundi</em> era, built on the Septuagint chronology, was the reckoning of the Orthodox churches; the Masoretic figures underlie the Western <em>anno mundi</em> of Ussher and others.')}.
<strong>These are scripture, not chronology, and were never intended as chronology.</strong></p>
{FIGS['chron']}
<p>The second link is the join, and it is the one a sceptic always aims at. Genesis 10:25–29 gives
Eber two sons, Peleg and Joktan, and names thirteen sons of Joktan — among them Hazarmaveth, which
is Ḥaḍramawt, and Sheba, which is Sabaʾ{c('Genesis 10:26–29. The identifications of Ḥaṣarmāweṯ with Ḥaḍramawt and Šəḇā with Sabaʾ are standard and not controversial.')}. <strong>Scripture itself places this branch in South
Arabia.</strong> The identification of Joktan with Qaḥṭān was made by the classical Arab genealogists
and stated flatly by al-Ṭabarī about 915 CE{c('al-Ṭabarī, <em>Taʾrīkh al-rusul wa-al-mulūk</em>; trans. W. M. Brinner, vol. 2 (Albany: SUNY Press, 1987).')}. It is a thousand years old and the family did not
make it. <em>Every Qaḥṭānī Arab in the world stands on that link.</em> It is not ours to defend.</p>

<h3 class="sub">Qaḥṭān to Jafna — a literary system, not a register</h3>

<p>From Qaḥṭān the chain runs Yaʿrub → Yashjub → Sabaʾ → Kahlān → al-Azd → Ghassān → Jafna.
Modern scholarship dates this system to roughly 660–900 CE{c('Peter Webb, <em>Imagining the Arabs: Arab Identity and the Rise of Islam</em> (Edinburgh: Edinburgh University Press, 2016), on the post-conquest construction of the tribal genealogical system.')}: inherited medieval learning, assembled
after Islam to order the Arab tribes into a single tree. <strong>Its weakest stretch is not the
biblical join at all — it is steps 16 to 24, Yaʿrub through al-Azd — and the Arab tradition itself
says so.</strong> The great compendia disagree with each other openly and by name: Ibn al-Kalbī
(d. 819){c('Ibn al-Kalbī, <em>Jamharat al-nasab</em>, ed. ʿĀlam al-Kutub. In the drive as <code>0819_Ibn_al-Kalbi_Jamharat_al-nasab.pdf</code>, 737 pp., with text layer.')}, Ibn Ḥazm (d. 1064){c('Ibn Ḥazm, <em>Jamharat ansāb al-ʿArab</em>, ed. ʿAbd al-Salām Hārūn (Cairo: Dār al-Maʿārif). Ghassān at p. 328; the Jafnids at p. 369. In the drive as <code>1064_Ibn_Hazm_Jamharat_ansab_al-Arab.pdf</code>.')}, Ibn Durayd (d. 933){c('Ibn Durayd, <em>al-Ishtiqāq</em>, ed. Hārūn. Free at al-Maktaba al-Shāmila, book 9211.')}, and later
the digest of al-Suwaydī{c('Abū al-Fawz Muḥammad Amīn al-Baghdādī al-Suwaydī (d. 1246 AH / 1831 CE), <em>Sabāʾik al-dhahab fī maʿrifat qabāʾil al-ʿArab</em>. A secondary digest, not an independent source; located pages in the DKI edition: Qaḥṭān p. 45, al-Azd p. 121, Ghassān pp. 273, 279, 283–284, Banū Jafna pp. 280, 284. In the drive as <code>1831_Suwaydi_Sabaik_al-Dhahab_qabail_al-Arab.pdf</code>.')}, whose pages 17–18 preserve Ibn Ḥazm’s observation that
Tanūkh, al-ʿUtq and <strong>Ghassān are composite tribes not descended from a single father</strong> —
which weakens any claim of a linear Ghassanid pedigree from inside the tradition.</p>
{FIGS['chain']}
<h3 class="sub">The family’s own chart, in full</h3>

<p>All of that is the scholarly frame. <strong>The document at the centre of it is John Aziz
Mogannam’s chart of thirty-six named generations</strong> — the one that hangs in the front of the
family’s own telling, in Arabic and English, from <span class="ar">آدم وحواء</span> to Rāshid. It
deserves to be printed in full rather than summarised, because it is the primary object of this whole
enquiry: everything else in this history is an attempt to test it fairly.{c('Chart: <em>Rashed El-Haddadeen Ancestry to Adam &amp; Eve</em> / <span class="ar">نسل راشد الحدادين إلى آدم وحواء</span>, researched and compiled by John Aziz Mogannam. Reproduced here as a data table with the evidence grading added; the original is a graphic.')}</p>
{FIGS['gens']}
<p>Read it with the grading on and the shape of the argument becomes visible at a glance.
<strong>Generations 1–13 are Genesis.</strong> <strong>Generation 14 is the join</strong> — Kahtaan
ibn Aaber, Qaḥṭān son of Eber, the single link where the Hebrew and Arabic systems are welded
together. <strong>Generations 15–32 are the classical Arab genealogists</strong>, and it is worth
noticing that the chart’s <span class="ar">الأزد</span> at 23, <span class="ar">مازن</span> at 24 and
<span class="ar">عمرو مزيقيا</span> at 29 are exactly the names Ibn Ḥazm and Ibn al-Kalbī argue about.
<strong>Generations 33–34 are attested history</strong>: Jabalah bin al-Harith and al-Harith bin
Jabalah are Procopius’s Arethas and his house, men with Byzantine offices and inscriptions.
<strong>Generation 35 is one line standing for nine hundred years.</strong> And generation 36 is
Rāshid, where the Ottoman paper begins.</p>

<p>Two observations follow, and both are gifts rather than corrections. First, <strong>the chart
itself is honest</strong> — it prints its own void, in the same typeface as everything else, and does
not pretend the gap is full. Second, <strong>the name Al-Ghassānī enters at generation 29</strong>,
with ‘Amr Muzayqiyāʾ, which is precisely where the classical sources put the naming at the
spring{c('The chart’s generations 23–29 (al-Azd → Māzin → Thaʿlaba → ʿAmr al-Qays → Ḥāritha al-Ghiṭrīf → ʿĀmir Māʾ al-Samāʾ → ʿAmr Muzayqiyāʾ) follow the standard Azdī pedigree as given in al-Suwaydī, <em>Sabāʾik al-dhahab</em>, and tabulated in Ferdinand Wüstenfeld, <em>Genealogische Tabellen der arabischen Stämme und Familien</em> (Göttingen, 1852–53), 500 pp. — both in the drive, and both named on the presentation’s own references slide.')}. The family’s chart and the ninth-century genealogists are telling the same
story in the same order. <em>That is a real finding, and it is a point in the chart’s favour.</em></p>

<p>And they disagree about something more fundamental. <strong>Ghassān is not an ancestor.
It is a spring.</strong></p>

<blockquote><span class="ar">إنما سُمّوا غسان بماء نزلوه، ليس بأب ولا أمّ</span><br>
“They named the children of Jafna ‘Ghassān’ after a water at which they alighted — it is neither a
father nor a mother. Whoever drank of this water was called Ghassānī, and the name of the water is
Ghassān.”
<span class="cite">Ibn Durayd, <em>al-Ishtiqāq</em>{c('Ibn Durayd, <em>al-Ishtiqāq</em>, s.v. Ghassān.')} — and Ibn al-Kalbī says the same, locating the water
between Zabīd and Rimaʿ{c('Ibn al-Kalbī, <em>Jamharat al-nasab</em>: <span class="ar">إنما غسان ماء شربوا منه فسُمّوا به، وهو ماء بين زبيد ورمع</span>.')}. The Ghassanids’ own poet, Ḥassān ibn Thābit:
<span class="ar">الأزد نسبتنا والماء غسّان</span> — “al-Azd is our lineage, and the water is Ghassān.”{c('Ḥassān ibn Thābit, <em>Dīwān</em>, cited in the genealogical literature s.v. Ghassān.')}</span></blockquote>

<p>Three of the tradition’s greatest authorities draw the boundary in three different places —
Ibn al-Kalbī at Māzin b. al-Azd, taking in the Anṣār of Medina; Ibn Ḥazm at only the four sons of
ʿAmr Muzayqiyāʾ who drank, excluding Aws and Khazraj by name; Ibn Durayd at the children of Jafna
alone{c('The three definitions are set out and compared in <em>The Eastern Sources</em>, the research report behind this history.')}. <strong>This does not weaken the family’s claim so much as change its kind.</strong>
Ghassanid identity was never a bloodline running out of one man. It was a people who arrived
somewhere and were named for it — which is, on reflection, exactly the sort of thing a family that
walked from Karak to a ridge in these hills ought to recognise.</p>

<h3 class="sub">The sharpest critic is inside the tradition</h3>

<p>Ibn Khaldūn (1332–1406) is the most searching sceptic of deep genealogy anyone has produced, and
he is an Arab historian writing in Arabic about Arab pedigrees{c('Ibn Khaldūn, <em>The Muqaddimah</em>, trans. Franz Rosenthal (Princeton: Princeton University Press, 1958), Book One, ch. 2. The Arabic <em>Kitāb al-ʿIbar</em>, vol. II, carries the Ghassān chapters; the indexed scan is free at archive.org (item <code>p.d.f4313</code>) but at 59 MB it resists compression and is not in the drive.')}. His argument is that lineage is a real
social fact with a short half-life: kinship binds while it is felt, and the memory of a common
ancestor beyond a handful of generations becomes an assertion rather than a knowledge. He names this
branch of the tree. <strong>The honest position holds his critique and the family’s claim at the same
time</strong> — and that is the position this history takes.</p>
{FIGS['arith']}
<p>Which brings us to a number. The chart’s own void reads “Unknown Al-Ghassani — 45 generations.”
The gap it spans runs from Jafna, floruit about 520, to Rāshid, floruit about 1500 — call it a
thousand years. <strong>Forty-five generations across a thousand years implies a male-line
generation of 22.2 years</strong>, which no observed population sustains; the range for male lines is
about 30 to 35{c('The generational interval for male lines is conventionally taken at 30–35 years; see the standard genealogical-demography literature. At 32 years, a 1,000-year gap yields roughly 31 generations, not 45.')}. At 32 years the same gap gives about 31 generations. <em>Correcting the count does
not close the void — it measures it honestly.</em></p>
"""))

# ── PART TWO
PARTS.append(('Two', 'The Road, and Nine Hundred Years of Silence',
 'The Ghassanids were real, and their one hard trace sits on the plateau the family remembers. Then the record stops.', f"""
<p>Strip away the later literature and what remains of the Ghassanids is small, hard, and more
interesting than the legend. <strong>Al-Ḥārith ibn Jabala, phylarch 528–569</strong>, is recorded by
Procopius — a contemporary who disliked him — as the man Justinian set over “as many clans as
possible” of the Arabs of the East{c('Procopius, <em>History of the Wars</em> I.17.47–48, ed. and trans. H. B. Dewing, Loeb Classical Library 48 (London: Heinemann, 1914). In the drive as <code>0550_Procopius_History_of_the_Wars_I-II_Loeb.pdf</code>, 610 pp.')}. He held the Byzantine office of phylarch and the honorific
<em>patrikios</em>: Greek titles, Roman pay. In 542 he petitioned the empress Theodora for bishops
for the persecuted Miaphysites, which produced the consecration of Jacob Baradaeus — the
best-attested fact tying the dynasty to non-Chalcedonian Christianity{c('The episode is reported by John of Ephesus and is discussed in Nöldeke and in all subsequent treatments of the dynasty.')}.</p>

<p>The rest is stones rather than chronicles: the audience hall outside Ruṣāfa with its Greek
acclamation; inscriptions at Qaṣr al-Ḥayr naming “Flavius Arethas, patrikios”; a building inscription
in the Ḥawrān; and a church at Tall al-ʿUmayrī invoking al-Mundhir{c('The Ghassanid epigraphic dossier is assembled in Theodor Nöldeke, <em>Die ghassânischen Fürsten aus dem Hause Gafna’s</em> (Berlin: Königl. Akademie der Wissenschaften, 1887), 76 pp. — in the drive as <code>1887_Noldeke_Die_ghassanischen_Fursten.pdf</code> — and revisited in the recent literature.')}. And a church at
<strong>Nitl, a few kilometres south-east of Madaba</strong> — which is to say, on the plateau the
family’s tradition names as the road. <em>The best physical evidence for Ghassanid Christianity and
the family’s remembered geography turn out to describe one landscape.</em> That is not a proof of
descent. It is a striking convergence, and it should be stated as exactly that.</p>

<p>One caution belongs here, and it comes from inside the scholarship. Much of what circulates about
the Ghassanids derives from Irfan Shahîd’s volumes{c('Irfan Shahîd, <em>Rome and the Arabs</em> (1984); <em>Byzantium and the Arabs in the Fourth Century</em> (1984); <em>…Fifth Century</em> (1989); <em>…Sixth Century</em>, vol. 1 pts 1–2 (1995) and vol. 2 pts 1–2 (2002, 2010) — all Dumbarton Oaks, Washington DC, and all released free by the publisher. Four volumes are in the drive; the fifth-century volume (113 MB) and sixth-century vol. 1 (139 and 67 MB) resist compression and remain as links.')}, and Greg Fisher’s critique is
substantial: a “kingdom” that was really a set of allied individuals; an identity read backwards from
later sources; buildings inferred from a book-list that no excavation has produced; a sedentarisation
that is not attested{c('Greg Fisher, <em>Between Empires: Arabs, Romans, and Sasanians in Late Antiquity</em> (Oxford: Oxford University Press, 2011), and “Kingdoms or Dynasties? Arabs, History, and Identity before Islam,” <em>Journal of Late Antiquity</em> 4:2 (2011).')}. <strong>No contemporary Greek, Syriac or Latin source ever uses the
word “Ghassanid.”</strong> They name individuals. Our ability to speak of a Ghassanid people at all
comes from the Arabic tradition — the same tradition that says Ghassān is a spring.</p>
{FIGS['mapreg']}
<h3 class="sub">The dam, and a date that has to move</h3>

<p>The family tradition dates the departure to the bursting of the Maʾrib dam, about 300 AD. The dam
is real, its breaches are dated, and the dates do not match: <strong>the recorded breaches are
449–450 and 543–548, with final collapse later in the sixth century.</strong> Abraha’s great
inscription of 548 CE — CIH 541 — records the repair and names the tribes and embassies present, and
it is free to read{c('Norbert Nebes, “A New ʾAbraha Inscription from the Great Dam of Mārib,” <em>Proceedings of the Seminar for Arabian Studies</em> 34 (2004), 221–230. In the drive as <code>2004_Nebes_New_Abraha_Inscription_Marib_Dam.pdf</code>.')}{c('CIH 541 and the Sabaic corpus generally are searchable free at DASI — Digital Archive for the Study of pre-Islamic Arabian Inscriptions, Università di Pisa / CNR, dasi.cnr.it.')}. This is a correction, not a demolition: the migration tradition
survives; the century attached to it moves.</p>
{FIGS['dam']}
<h3 class="sub">And then the void</h3>

<p>From the last Jafnid to the first Ḥaddādīn there is no record of any kind, and <strong>the
family’s own chart is the thing that says so.</strong> Nine hundred years. Four great chronicles that
should have caught something were searched in full, with working controls, and all four are silent:
Yaḥyā al-Anṭākī{c('Yaḥyā ibn Saʿīd al-Anṭākī, <em>Histoire</em>, ed. and trans. A. Vasiliev and I. Kratchkovsky, <em>Patrologia Orientalis</em> 18 and 23. In the drive as <code>1924_Yahya_al-Antaki_Histoire_PO18_23.pdf</code>.')}, Agapius of Manbij{c('Agapius (Maḥbūb) of Manbij, <em>Kitāb al-ʿUnwān</em>, <em>Patrologia Orientalis</em>. In the drive as <code>1909_Agapius_Kitab_al-Unwan_PO.pdf</code>.')}, Michael the Syrian{c('Michael the Syrian, <em>Chronique</em>, ed. and trans. J.-B. Chabot, t. 1. In the drive as <code>1899_Michael_the_Syrian_Chronique_t1.pdf</code>.')}, and
Bar Hebraeus{c('Bar Hebraeus, <em>Chronography</em>, trans. E. A. W. Budge. In the drive as <code>1932_Bar_Hebraeus_Chronography.pdf</code>.')}. So are Nasrallah’s survey of Melkite literature{c('Joseph Nasrallah, <em>Histoire du mouvement littéraire dans l’Église melchite du Ve au XXe siècle</em>, vols. II.2 and III.2. Both in the drive.')}, Sanjian’s
Armenian colophons{c('Avedis K. Sanjian, <em>Colophons of Armenian Manuscripts, 1301–1480</em> (Cambridge, MA: Harvard University Press, 1969), 470 pp. In the drive.')} and Agnes Smith Lewis’s Sinai catalogue{c('Agnes Smith Lewis, <em>Catalogue of the Syriac MSS. in the Convent of S. Catharine on Mount Sinai</em> (London, 1894). In the drive.')}.</p>

<p>There is a structural reason for part of that silence, and it is worth printing because it looks
like absence and is not. <strong>Empty colophons are evidence about naming, not about
population.</strong> A man of ʿAbūd who entered Mar Saba became “al-Maqdisī”; the monastery, not the
village, supplied the name{c('Miriam L. Hjälm and Peter Tarras, on early Christian Arabic colophons from the Palestinian monasteries — the naming argument. In the drive as <code>2023_Hjalm_Tarras_Palestinian_Colophons.pdf</code>.')}. The Syriac silence is structural too: the West Syrian diocesan lists
do not cover a Melkite countryside.</p>

<p>And the window is not empty — it is only anonymous. At <strong>Jifnā in 1179, nine kilometres from
Ramallah</strong>, a bilingual Greek and Arabic building inscription at the monastery of Choziba names
Ibrāhīm and his brothers, sons of Mūsā, of Jifna: ordinary laymen of a hill village, named in stone,
paying for work on a monastery in the middle of the Crusader century{c('Discussed in Denys Pringle, <em>The Churches of the Crusader Kingdom of Jerusalem: A Corpus</em>, vol. I (Cambridge: Cambridge University Press, 1993), who dates it 1179. <strong>Caution:</strong> secondary summaries of Ellenblum have been reported as tenth-century; the reading should be verified against R. Schneider’s 1931 publication before print.')}. At <strong>ʿAbūd</strong>,
a Syriac inscription of 1058 names a patriarch, an archbishop and a priest, and three of the
village’s monks appear in manuscript colophons; its church, excavated by <strong>Hamdan Taha</strong>,
has four building phases from the fifth century to the eighteenth{c('Hamdan Taha, “A Salvage Excavation at the ʿAbūdiyah Church in ʿAbūd, Samaria,” <em>Liber Annuus</em> 47 (1997).')}. In 1374 a Christian of
Jifnā, Niʿma b. Bishāra, appears in the Ḥaram al-Sharīf documents{c('Said Aljoumani, Zahir Bhalloo and Konrad Hirschler, <em>Catalogue of the New Corpus of Documents from the Ḥaram al-Sharīf in Jerusalem</em> (2024), open access. In the drive. The editors read the toponym uncertainly as <span class="ar">جفنا الجوز؟</span>; the first element is clear. The original is in the Islamic Museum, Jerusalem, and wants autopsy.')}. East of the Jordan the
community is continuous: the pilgrim Thietmar, on his journey of 1217–18, was hosted and fed at
al-Shawbak by a Frankish widow living in the suburb, where Christians and Muslims lived side by side;
Abū al-Fidāʾ records a Christian majority at Shawbak in 1321; Karak’s street
plan still carries a <em>Burj al-Naṣārā</em>{c('The Karak and Shawbak evidence is assembled in <em>The Eastern Sources</em>; al-Qalqashandī on the origin of al-Karak is at <em>Ṣubḥ al-aʿshā</em>, s.v.')}.</p>

<p><strong>None of these men is an ancestor. Together they prove that the population the family
claims to come from was here, had names, and wrote them down.</strong></p>
"""))


# ── PART THREE-A — the people of the land
PARTS.append(('Three', 'The People of the Land', 
 'Canaanites, Philistines, Samaritans — and the question of who was here before the family arrived, which turns out to have an answer.', f"""
<p>A family history that begins with Adam has to say something about the ground it ends on. The hills
around Ramallah were not empty in 1562 and were never empty; the question is what relationship the
people who walked up from Bayt Jālā have to the people who had been farming these terraces for four
thousand years. <strong>Until recently that question could only be answered rhetorically. It can now
be answered with evidence — and the evidence is unusually clear.</strong></p>

<h3 class="sub">The Canaanites, and what happened to them</h3>

<p>The city-states of this landscape are visible in the fourteenth century BCE in the
<strong>Amarna letters</strong>, the cuneiform correspondence of local rulers with the Egyptian
court — Jerusalem, Shechem, Gezer, Lachish, writing in Akkadian about their neighbours and their
troubles{c('The Tell el-Amarna correspondence, 14th century BCE. W. M. Flinders Petrie, <em>Syria and Egypt from the Tell el-Amarna Letters</em> (London, 1898), in the drive as <code>1898_Petrie_Syria_and_Egypt_from_the_Tell_el-Amarna_Letters.pdf</code>; the standard modern edition is W. L. Moran, <em>The Amarna Letters</em> (Baltimore: Johns Hopkins, 1992).')}. These are the Canaanites, and the old question was whether they were
displaced. <strong>The genomic answer is that they were not.</strong> Agranat-Tamir and colleagues
sequenced seventy-three individuals from Bronze Age sites across the southern Levant and found a
single, coherent population{c('Lily Agranat-Tamir, Shamam Waldman, Mario A. S. Martin, et al., “The Genomic History of the Bronze Age Southern Levant,” <em>Cell</em> 181:5 (2020), 1146–1157.e11, DOI 10.1016/j.cell.2020.04.024.')}; Haber and colleagues had already shown that
<strong>present-day Levantine populations derive the large majority of their ancestry from those
Bronze Age Canaanites</strong>, with continuity across five millennia{c('Marc Haber, Claude Doumet-Serhal, Christiana Scheib, et al., “Continuity and Admixture in the Last Five Millennia of Levantine History from Ancient Canaanite and Present-Day Lebanese Genome Sequences,” <em>American Journal of Human Genetics</em> 101:2 (2017), 274–282, DOI 10.1016/j.ajhg.2017.06.013.')}. The
population did not leave. <em>It changed language and religion, repeatedly, and stayed.</em></p>

<h3 class="sub">The Philistines — a two-century signal</h3>

<p>The Philistines are the best-documented case of newcomers to this coast, and their fate is the
most instructive thing in this section. Ancient DNA from Ashkelon shows a European-derived component
arriving with the early Iron Age — a real migration, visible in the genome. And then:
<strong>“within no more than two centuries, this genetic footprint introduced during the early Iron
Age is no longer detectable.”</strong>{c('Michal Feldman, Daniel M. Master, Raffaela A. Bianco, et al., “Ancient DNA sheds light on the genetic origins of early Iron Age Philistines,” <em>Science Advances</em> 5:7 (2019), eaax0061, DOI 10.1126/sciadv.aax0061. The quoted sentence is the authors’ own summary of the dilution of the European-related component.')} They did not vanish; they were absorbed. The
incomers married in, and within about eight generations the local population had simply taken them
up.</p>

<p>That is worth holding beside this family’s own story. <strong>A group arrives from elsewhere,
carrying a name and a memory, and within a few centuries is indistinguishable from the people already
there</strong> — that is not a threat to the Ghassanid claim, it is the ordinary mechanism of this
landscape, and it has happened at least four times on this ridge. The Ḥaddādīn who came up from
Bayt Jālā in 1562 were the latest instance of a very old pattern, not an exception to it.</p>

<h3 class="sub">The Samaritans — the neighbours who never left</h3>

<p>And one community did not change language or religion, and is still here: the
<strong>Samaritans of Nablus</strong>, thirty miles north of Ramallah, whose community has been
continuous on Mount Gerizim since antiquity and whose chronicles are their own historiography{c('<em>The Samaritan Chronicle, or the Book of Joshua the son of Nun</em>, trans. Oliver Turnbull Crane (New York, 1890). In the drive as <code>1890_Samaritan_Chronicle_Book_of_Joshua_Crane.pdf</code>.')}.
They matter here for two reasons. They are the living proof that continuity on this land is not a
rhetorical claim but an observable fact — a community that can be traced in place across two thousand
years. And their villages are the immediate northern neighbours of the district in which Ramallah
sits; the ridge road that carries this whole story runs from Hebron through Jerusalem and al-Bīra to
Nablus, and the Samaritan community sits at its northern end.</p>

<h3 class="sub">The place-names are the argument</h3>

<p>The most durable evidence of continuity is not in a laboratory. <strong>It is in the names of the
villages themselves.</strong> Arabic toponymy across Palestine preserves Canaanite and Aramaic
forms — the sound of a language that stopped being spoken a thousand years before Arabic arrived,
carried forward by the people who kept farming the same terraces. Nur Masalha builds his four
thousand years of Palestinian history on exactly this argument{c('Nur Masalha, <em>Palestine: A Four Thousand Year History</em> (London: Zed Books, 2018), 425 pp., on toponymic continuity and “indigenous social toponymic memory”; the toponymy discussion begins at pp. 23–24 and 32. In the drive as <code>2018_Masalha_Palestine_A_Four_Thousand_Year_History.pdf</code>.')}, and the Palestinian
gazetteer literature is what makes it checkable: Shukrī ʿArrāf’s survey of the geographical names of
Palestine{c('شكري عرّاف, <em>المواقع الجغرافية في فلسطين: الأسماء العربية والتسميات العبرية</em>, 624 pp. In the drive as <code>1974_Arraf_al-Mawaqi_al-jughrafiyya_fi_Filastin.pdf</code>.')}, al-Dabbāgh’s <em>بلادنا فلسطين</em>{c('مصطفى مراد الدباغ, <em>بلادنا فلسطين</em>, and Muḥammad Muḥammad Ḥasan Sharāb, <em>معجم بلدان فلسطين</em> — both in the drive.')}, and Muhammad Maraqten’s study
of place-name memory{c('محمد مرقطن, “ذاكرة المكان: أسماء الأماكن…”, <em>تبيّن</em> 33 (Doha Institute, 2020). In the drive as <code>2020_Doha_Institute_Palestinian_toponymy_study.pdf</code>.')}.</p>

<p>The family’s own district supplies the example. <strong><em>Rām Allāh</em> itself is built from
<span class="ar">رام</span>, a Semitic root meaning height</strong> — the same root as Hebrew
<em>rām</em> and Aramaic <em>rāmā</em>, and al-Dabbāgh says so explicitly{c('al-Dabbāgh, <em>بلادنا فلسطين</em>, viii/2, on <span class="ar">رام</span> as a Semitic root meaning height. The construction is exactly parallel to Ramat/Ramah names elsewhere in the hill country.')}. The name is not
an Arabic invention of 1562 laid over blank ground; <em>it is a Canaanite-era word for a high place,
still doing its job, in the mouths of the people who never left.</em> That the deed of 1279 already
carries the name in that form (Part Four) is the documentary end of the same argument.</p>
{FIGS['peoples']}
<p>So the honest statement of this family’s relation to the land has two halves, and both are
stronger than the usual rhetoric. <strong>By tradition, the family came from Yemen through Ghassān
and Karak, and that story is consistent with everything testable in it.</strong> <strong>By descent,
the people of these hills — including whoever the Ḥaddādīn married into over twenty-one
generations — carry the ancestry of the Bronze Age population of this same country.</strong> Both
can be true at once. Arriving from somewhere and belonging to a place are not opposites here; they
are, on this ridge, the same process seen at two different distances.</p>
"""))

# ── PART FOUR
PARTS.append(('Four', 'The Hills Before Ramallah',
 'The ground the family arrived on was not empty. It had been Christian, then Frankish, then Mamluk — and one of its churches sits two kilometres from the town centre.', f"""
<p>Ramallah sits at about 850 metres on the watershed ridge, and almost everything about its history
follows from that. The central highlands are crossed north to south by a single watershed route —
Hebron, Bethlehem, Jerusalem, al-Bīra, Nablus — and a village on that ridge is on a road whether it
wants to be or not. It also sits on a seam: <strong>the district was administratively split</strong>,
Sinjil and the eastern hills under Jerusalem, Wādī Banī Zayd and the western hills under al-Ramla,
with Ramallah’s site on the boundary{c('Mujīr al-Dīn al-ʿUlaymī, <em>al-Uns al-jalīl bi-tārīkh al-Quds wa-al-Khalīl</em> (completed 900/1495), Dandīs ed., 2/148, for the district boundary. Both volumes in the drive as <code>1495_Mujir_al-Din_al-Uns_al-jalil_v1.pdf</code> and <code>_v2.pdf</code>; Henry Sauvaire’s French translation, <em>Histoire de Jérusalem et d’Hébron</em> (1876), also in the drive.')}. <em>That is why the record here is dark.</em> The Mamluk postal system
makes the same point from the other side: there is no <em>barīd</em> station between Ludd and Jinīn,
the whole hill country bypassed{c('al-Qalqashandī, <em>Ṣubḥ al-aʿshā</em>, the <em>barīd</em> chapter at 14/418–429. Free at al-Maktaba al-Shāmila, book 9429.')}.</p>

<p>What the ground shows is continuous Christian settlement through exactly the centuries the
ancestry chart cannot document — and the excavation is Palestinian. <strong>A Byzantine church at
Khirbet et-Tireh, two kilometres from Ramallah’s centre</strong>, has been dug across a decade of
seasons by <strong>Salah Hussein al-Houdalieh</strong> of al-Quds University: the eastern church, its
mosaic pavements and their substrates, an oil-press complex, a clay bread stamp, and the agricultural
watchtowers around it{c('Salah Hussein A. al-Houdalieh, “The Byzantine Eastern Church of Khirbet et-Tireh,” <em>Archaeological Discovery</em> 4:1 (2016), 48–67, DOI 10.4236/ad.2016.41005, CC BY 4.0. In the drive as <code>2016_Houdalieh_Byzantine_Church_Khirbet_et-Tireh.pdf</code>.')}{c('Also al-Houdalieh, “The Byzantine Church of Khirbet et-Tireh,” <em>JEMAHS</em> 2:3 (2014), 188–208; with H. Bearat, “The Mosaic Pavement Substrates…,” <em>Zephyrus</em> 84 (2019), 183–203; “The Oil Press Complex of Khirbat al-Tira,” <em>Jerusalem Quarterly</em> 62 (2015), 84–97.')}. <strong>This is the closest thing the town has to a published
archaeological record of its own ground.</strong></p>
{FIGS['mapdis']}
<h3 class="sub">Yāqūt saw al-Bīra</h3>

<p>The Arabic geographical tradition names four of these villages while the imperial chancery names
none — and one entry is an eyewitness. Yāqūt describes the Palestinian al-Bīra and says plainly
<span class="ar">رأيتها</span>, <em>I saw it</em>, recording its destruction by Saladin{c('Yāqūt al-Ḥamawī, <em>Muʿjam al-buldān</em>, al-Bīra at 1/526; ʿAyn Yabrūd at 5/427; ʿAbūd at 4/64. Free at al-Maktaba al-Shāmila, book 23735. <strong>Correction established by this project:</strong> the working rule that <em>al-Bīra</em> in Arabic always denotes the Euphrates town holds only for Mujīr al-Dīn and al-Qalqashandī; Yāqūt is describing the Palestinian place from autopsy.')}. That
correction matters methodologically, and it was established by this project: the old working rule
that <em>al-Bīra</em> in Arabic always means the Euphrates town holds only for two later authors.
A second correction of the same kind: <strong>Mujīr al-Dīn has five occurrences of
<span class="ar">البيرة</span>, not six</strong> — three in his text and two editorial, one of those
Ilbīra in Spain{c('Established by direct search of the Dandīs edition; see <em>The Eastern Sources</em>.')}.</p>

<p>Two miles away, al-Bīra is the best-documented village in this hill country in the whole medieval
period — as <em>Magna Mahumeria</em>, a Frankish settlement of the Holy Sepulchre. The cartulary
charter of 11 February 1156 rolls ninety-two burgesses, with some fifty more names added over the
following three decades, implying a Frankish population of perhaps 500–700{c('Geneviève Bresc-Bautier (ed.), <em>Le Cartulaire du chapitre du Saint-Sépulcre de Jérusalem</em> (Paris: Paul Geuthner, 1984), charter no. 117, pp. 237–240 = Röhricht, <em>RRH</em> no. 302. In the drive as <code>1984_Bresc-Bautier_Cartulaire_Saint-Sepulcre.pdf</code>.')}. <strong>It names
nobody local.</strong> Pringle gives the parish church of St Mary as entry no. 66, with a restored
plan{c('Denys Pringle, <em>The Churches of the Crusader Kingdom of Jerusalem: A Corpus</em>, vol. I: A–K (Cambridge, 1993), al-Bira no. 66, pp. 161–165, fig. 48, plates CII–CVI. In the drive as <code>1993_Pringle_Churches_Crusader_Kingdom_v1.pdf</code>.')}. The Franks are documented; the villagers among whom they lived are not.</p>

<h3 class="sub">A verified negative, and then a deed</h3>

<p>In 1495 Mujīr al-Dīn finished <em>al-Uns al-jalīl</em>, the standard late-medieval topography of
the Jerusalem district. It was searched directly and in full. <strong>There is no Ramallah in
it.</strong> That negative is a finding, and it still stands.</p>

<p>And yet the name is older than the town. A boundary case heard in the Jerusalem sharīʿa court in
June 1565 turns on a Mamluk endowment deed of 678 AH — 1279 CE — in which <em>Rām Allāh</em> is
already a surveyed place.</p>

<blockquote><span class="ar">وقد أحضر حمزة جلبي كتاب الوقف المؤرخ سنة ٦٧٨ هـ وقف السلطان منصور قلاوون…</span><br>
“…and Ḥamza Chelebi produced the waqf deed dated the year 678, the endowment of Sultan al-Manṣūr
Qalāwūn… and it appeared that the boundaries of Rām Allāh are: on the south Dayr Fazṭā, on the east
the travelled road, its limit the Silsila al-Rummāniyya, running north to Burj Salmiyya, which is
the northern boundary of Rām Allāh.”
<span class="cite">Jerusalem sharīʿa register 48, p. 54 · 23 Dhū al-Qaʿda 972 / 22 June 1565{c('IRCICA, <em>Sijillāt maḥkamat al-Quds al-sharʿiyya</em>, register 48, ed. Ibrāhīm Rabāyʿah, series no. 31, open access. In the drive as <code>1565_Jerusalem_Sijill_48_IRCICA.pdf</code>, 315 pp. <strong>Not yet verified to print standard:</strong> the IRCICA PDFs use a scrambled custom font encoding that had to be reconstructed. The digits 678 and 971 are literal in the raw bytes and <em>waqf al-Khalīl</em> and <em>al-Sulṭān Manṣūr Qalāwūn</em> decode unambiguously, but p. 54 must be checked against the page images.')}.
Al-Dabbāgh, working from Arabic sources with no access to the register, records the same endowment
independently{c('Muṣṭafá Murād al-Dabbāgh, <em>بلادنا فلسطين</em>, al-juzʾ al-thāmin, al-qism al-thānī: <em>fī diyār Bayt al-Maqdis</em> (Beirut: Dār al-Ṭalīʿah, 1965–), on the Qalāwūn endowment and on <span class="ar">رام</span> as a Semitic root meaning height. In the drive as <code>1965_Dabbagh_Biladuna_Filastin_v8_pt2.pdf</code>.')}.</span></blockquote>

<p><strong>That is 283 years before the traditional founding.</strong> It does not make the founding
story wrong. It makes it one layer of a longer one.</p>
"""))

# ── PART FIVE
PARTS.append(('Five', 'The Founding',
 'For the first time the story rests on paper. The Ottoman state counted taxpayers village by village, and the registers date the founding more precisely than the family’s own account does.', f"""
<p><strong>Sameeh Hammoudeh</strong> worked through the Ottoman tax registers for Ramallah and
published the result in 2014{c('Sameeh Hammoudeh, “New Light on Ramallah’s Origins in the Ottoman Period,” <em>Jerusalem Quarterly</em> 59 (2014), 37–53, DOI 10.70190/jq.i59.p37. In the drive as <code>2014_Hammoudeh_New_Light_Ramallah_Ottoman_JQ59.pdf</code>.')}. It is the most important documentary research ever done on the
founding, and it is by a Palestinian scholar working on Palestinian ground. His monograph
<em>رام الله العثمانية: دراسات في تاريخها الاجتماعي ١٥١٧–١٩١٨</em> extends it{c('سميح حمودة, <em>رام الله العثمانية: دراسات في تاريخها الاجتماعي ١٥١٧–١٩١٨</em> (Beirut: Institute for Palestine Studies, 2017), 425 pp., ISBN 9786144480274, intro. by Salim Tamari. Ḥammūda has since died; his work should be finished rather than repeated.')}.</p>
{FIGS['hh']}
<p>The sequence runs like this. In <strong>1525–28</strong> Ramallah is uninhabited — listed as
agricultural land of the Ibrāhīmī waqf of Hebron, assessed at 3,000 <em>aqja</em>, with no households
at all. Note how that dovetails with the deed of 1279: the site is endowment land, and has been for
centuries. In <strong>1538–39</strong> four Muslim households are counted, the first people on the
site. In <strong>1553–54</strong> there are six Muslim households here — and thirty-six Christian
households at Bayt Jālā, eleven miles south, where the group called the Kasābra is registered. In
<strong>1562</strong> the Christians arrive: twenty-seven more families come up from Bayt Jālā with
eight unmarried men, about thirty-seven Christian households against ten Muslim.
<strong>That is the founding, and a document carries it.</strong> By <strong>1596–97</strong> the
village has eighty households, seventy-one of them Christian, taxed at a quarter and yielding 9,400
<em>aqja</em>{c('Wolf-Dieter Hütteroth and Kamal Abdulfattah, <em>Historical Geography of Palestine, Transjordan and Southern Syria in the Late 16th Century</em> (Erlangen: Erlanger Geographische Arbeiten, 1977), 116 and 121.')}. The registers name names: the <strong>Ḥaddādīn</strong>, al-Kasābra and al-Naqqāsh
among the Christians; al-Labūd and Abū al-Thanāyā among the Muslims.</p>
{FIGS['nbhd']}
<h3 class="sub">Two corrections, and neither one weakens the family</h3>

<p><strong>The founding is 1562, not “about 1550.”</strong> This is a promotion, not a demotion: a
document carries 1562 and nothing carries 1550. And the migrants were probably Rāshid’s sons or
grandsons rather than Rāshid himself — the register puts the movers a generation or two below him.
The family’s account is refined by the paper, not refuted by it.</p>

<h3 class="sub">The road, written down in Jordan</h3>

<p>The family remembers a route: the Ḥijāz, Udhruḥ, al-Shawbak, al-Karak, Maʿīn, and across the
Jordan. <strong>Every stage from Karak onward is attested independently, in registers kept in another
country.</strong> Karak’s Christian community is documented from the early thirteenth century and counted at
<strong>103 Christian households and 8 bachelors in the register of 1596</strong>{c('Ottoman Defter 185, the Karak register of 1596. The figure of 143 households for 1562, printed in earlier editions of this work, was carried second-hand and no folio has been produced for it; it is set aside as unverified rather than repeated. Route reconstruction: Hammoudeh, JQ 59 (2014), 43, 45 and 52 n. 57.')}. And Peake’s Karak clan register records the Ḥaddādīn directly:</p>

<blockquote><span class="ar">…وتزوج فتاة من عشيرة الحدادين، ومذهبهم روم أرثوذكس</span><br>
“…he came to al-Karak and married a girl of the Ḥaddādīn clan, and their rite is Greek Orthodox.
They dwell in al-Karak and the village of Ḥamūd, and they have relatives in Nazareth called
al-Hanādisa.”
<span class="cite">F. G. Peake, <em>تاريخ شرقي الأردن وقبائلها</em>{c('Frederick G. Peake (Peake Pasha), <em>تاريخ شرقي الأردن وقبائلها</em> / <em>A History of Jordan and Its Tribes</em>, the Karak clan register. In the drive as <code>1935_Peake_Tarikh_sharqi_al-Urdun_wa-qabailiha.pdf</code>, 609 pp.')}. The syntax matters: an incoming clan
married <em>into</em> the Ḥaddādīn, which puts the Ḥaddādīn there first.</span></blockquote>

{FIGS['jordan']}
<p>Peake also records a Ḥaddādīn <em>ḥamūla</em> scattered across al-Ḥuṣn, Aydūn, Kufr ʿAwān and
al-Salṭ — <strong>an old, fragmented lineage rather than one family.</strong> That is what the
evidence supports, and it is a more interesting fact than a single heroic migration.</p>

<h3 class="sub">The tribe that stayed</h3>

<p>This is worth dwelling on, because it is usually left out of the Ramallah telling.
<strong>The Ḥaddādīn did not all leave.</strong> The clan is a living Jordanian Christian tribe:
concentrated at al-Karak and the village of Ḥamūd, with branches at al-Ḥuṣn, Aydūn and Kufr ʿAwān in
the north, at al-Salṭ in the centre, and relatives at Nazareth called al-Hanādisa — and the Karak
Christian community from which they come is documented continuously from Thietmar’s Frankish
widow at Shawbak in 1217–18 to the 103 Christian households and 8 bachelors counted at Karak in the
register of 1596.{c('The Karak Christian community: Thietmar’s <em>Peregrinatio</em>, the journey of 1217–18 (the Shawbak stop is dated 1217 in the Transjordanian survey literature and 1218 elsewhere); Abū al-Fidāʾ on a Christian majority at Shawbak in 1321; the 1596 household count from Ottoman Defter 185. Karak’s street plan preserves a <em>Burj al-Naṣārā</em>, the tower of the Christians.')}
<em>The Ramallah branch is an emigrant fragment of a tribe that is still there.</em></p>

<p>The clan has its own historians on that side of the river, and they should be read alongside the
Ramallah ones. <strong>Munther J. Haddadin</strong> — the Jordanian water minister and negotiator —
has written both the tribal history, <em>دولة الغساسنة: أصيلها ورحيلها</em> (2024), and a full clan
volume, <em>عشيرة الحدادين: أصولها وفروعها</em> (2025){c('منذر حدادين, <em>دولة الغساسنة: أصيلها ورحيلها</em> (Amman: دار ورد الأردنية, 29 July 2024), ISBN 9789923769751; and <em>عشيرة الحدادين: أصولها وفروعها</em> (Amman: Warda Books, 2025). The second is on David’s shelf in print; neither has been found in any digital library.')}. ʿAbbās Ḥaddādīn’s clan
history, written in Jordan, records the road independently of anything in Ramallah:
<em>“they were in southern Jordan, specifically al-Shawbak, and they had holdings in Udhruḥ… the two
clans went out from al-Shawbak to al-Karak.”</em>{c('ʿAbbās Ḥaddādīn’s clan history, cited in the deck at slide 27. The convergence matters: two branches of one clan, separated for four centuries and writing in two countries, describe the same route in the same order.')} <strong>Two branches of one clan, separated for
four hundred years and writing in two countries, describe the same route in the same order.</strong>
That convergence is not proof, but it is the kind of evidence oral tradition can actually supply, and
it is stronger than either telling on its own.</p>

<p>The Palestinian side of the same literature is al-Dabbāgh’s volume on the Arab tribes and their lineages{c('مصطفى مراد الدباغ, <em>القبائل العربية وسلائلها في بلادنا فلسطين</em> (Beirut: al-Muʾassasa al-ʿArabiyya lil-Dirāsāt wa-al-Nashr), 288 pp. In the drive as <code>1979_Dabbagh_al-Qabail_al-Arabiyya_fi_Filastin.pdf</code>. <em>Note:</em> the archive.org item carrying this book was catalogued in earlier editions of the bibliography under ʿAmāri’s tribal dictionary; the correction is made here.')}, with
Kaḥḥāla’s tribal encyclopaedia{c('عمر رضا كحالة, <em>معجم قبائل العرب القديمة والحديثة</em>, vols. 4–5 in the drive.')} and al-ʿAzīzī’s Jordanian compendium{c('روكس بن زائد العزيزي, <em>معلمة للتراث الأردني</em>, 1,887 pp. In the drive as <code>1984_Azizi_Mualamat_lil-turath_al-Urduni.pdf</code>.')} beside it.</p>
{FIGS['datings']}
<h3 class="sub">Rāshid, and what a clan actually was</h3>

<p>The tradition holds that Rāshid al-Ḥaddādīn — <em>ḥaddād</em>, the blacksmith — had five sons, and
that the town’s clans descend from them: Ḥaddād, whose own five sons produced Awad, Sharaka, Yousef,
Jaghab and Azzouz; and Ḥassān, Shuqair, Ibrāhīm and Jiryis. Rafīdī joins the founder by a broken line
on the family’s own structural diagram — affiliated, not a son — and the book keeps the broken
line{c('The nine clan sections and the Rafīdī broken line are the structure of the Family Tree Book; see <em>Clan_Structure.md</em> and <em>Family_Heads_Rule.md</em> in the project documents.')}. <em>Ḥaddād</em> is an occupational surname and non-diagnostic on its own; no medieval
attestation of a Ḥaddādīn lineage was found in any corpus searched for this project — and that
negative was searched for, not assumed.</p>

<p>And a <em>ḥamūla</em> here was a residence quarter as much as a descent group: each clan held a
share of the village land, a quarter of the built-up core, and a <em>madāfa</em>, the guest house
where its men received visitors and settled disputes. <strong>Riwaq’s building survey can still map
most of those quarters on the ground.</strong>{c('Riwaq Centre for Architectural Conservation, <em>Registry of Historic Buildings in Palestine</em>, district of Ramallah: buildings.riwaq.org. See also Nazmi al-Jubeh and Khaldun Bshara, <em>Ramallah: Architecture and History</em> (Ramallah: Riwaq, 2001) — the only architectural history of the town.')} The Family Tree Project’s nine clan sections are exactly
this structure, and the printed record now runs to more than nine thousand named descendants beneath
them{c('The GEDCOM behind the book carries 28,226 people in 10,399 families across 21 generations, 9 clans, 1500–2026; the printed book at v87 runs to 796 pages and 235 trees on 141 sheets.')}. The book the whole project is built on remains ʿAzīz Shāhīn’s{c('عزيز شاهين, <em>كشف النقاب عن الجدود والأنساب في مدينة رام الله</em> (Birzeit University, 1982). <strong>Cite it by this Arabic title</strong> — the English jacket title, <em>Ramallah: Its History and Its Genealogies</em>, is why it has been so hard to find in catalogues. A full scan is in the drive as <code>1982_Shahin_Kashf_al-Niqab.pdf</code>.')}.</p>
"""))

# ── PART SIX
PARTS.append(('Six', 'The Ottoman Centuries',
 'Three hundred years in which Ramallah is a Christian village among Muslim ones — taxed by the state, ruled by shaykhs, raided in bad years, and slowly growing.', f"""
<p>For most of these three centuries Ramallah is a name in a fiscal document and very little else.
The best scholarship on the seventeenth century maps the Christian villages of the Jerusalem district
one by one from the <em>jizya</em> registers — <strong>Felicita Tramontana</strong>’s work — and
Ramallah is on the map{c('Felicita Tramontana, <em>Passages of Faith: Conversion in Palestinian Villages (17th Century)</em> (Wiesbaden: Harrassowitz, 2014); and “Trading in Spiritual and Earthly Goods: Franciscans in Semi-Rural Palestine,” in N. Amsler et al. (eds.), <em>Catholic Missionaries in Early Modern Asia</em> (Routledge, 2020), green open access. In the drive as <code>2020_Tramontana_Trading_Spiritual_Earthly_Goods.pdf</code>.')}. <strong>Dror Zeʾevi</strong>’s study of the district in the 1600s is the
other half of the picture{c('Dror Zeʾevi, <em>An Ottoman Century: The District of Jerusalem in the 1600s</em>, SUNY Series in Medieval Middle East History (Albany: State University of New York Press, 1996), xii + 258 pp., ISBN 0-7914-2916-4 — free in full. In the drive as <code>1996_Zeevi_An_Ottoman_Century.pdf</code>.')}. Between them they are the two scholars who could fill the
emptiest stretch of the whole story, and both are free.</p>

<p>The state taxed the hill country but rarely governed it directly. Between the state and the
village stood the shaykh, and Ramallah’s neighbours held the thrones — the <em>qurā al-karāsī</em>,
throne villages, whose families farmed the taxes of a group of villages and built in stone to show
it. Riwaq counts twenty-four shaykhdoms in the central highlands{c('Riwaq’s survey of the <em>qurā al-karāsī</em>; Shaykh Ṣāliḥ’s castle at Dayr Ghassāna has phases of 1602 and 1862, and al-Qāsem Palace is dated 1820.')}. <strong>Ramallah was not a throne
village. It was one of the villages the thrones taxed.</strong></p>

<p>Two corrections belong here, both established against the registers.
<strong>The Barghūthī shaykhdom is not in the sixteenth-century registers</strong> — the shaykhs of
Banī Zayd in 1563–76 are the house of Abū Rayyān, and the Barāghtha appear in 1710{c('Established from the sixteenth-century registers and from Sharāb; see <em>The Eastern Sources</em>. محمد محمد حسن شراب, <em>معجم بلدان فلسطين</em>, in the drive as <code>1987_Sharab_Mujam_Buldan_Filastin.pdf</code>, records al-Bakrī 1710 on the Barāghtha.')}. And
<strong>Banī Ḥārith is not attested in these hills before the sixteenth century.</strong> These are
exactly the details a family history gets wrong by inheriting them from later tradition. The Arabic
side of the shaykhly story is Iḥsān al-Nimr’s history of Jabal Nablus{c('إحسان النمر, <em>تاريخ جبل نابلس والبلقاء</em>. In the drive as <code>1938_Nimr_Tarikh_Jabal_Nablus_wal-Balqa.pdf</code>, 312 pp., with text layer.')}.</p>

<h3 class="sub">1799, and a family story tested the same way</h3>

<p>Napoleon marched from Cairo to Acre and back in four months in 1799. <strong>The hill country was
never touched</strong> — and the walls that stopped him at Acre were rebuilt <em>afterwards</em>.
That matters, because one Ramallah family tells this century differently: that its men were masons,
taken north to build for the pasha and fetched home to build the church. The tradition was tested
link by link. Volney describes Acre’s wall in 1785 as little better than a garden wall{c('C.-F. Volney, <em>Travels through Syria and Egypt, in the Years 1783, 1784, and 1785</em>, vol. ii, p. 227. In the drive as <code>1787_Volney_Travels_Syria_Egypt_v2.pdf</code>.')}; Buckingham
describes the walls as al-Jazzār rebuilt them, at <strong>pp. 75–76</strong> — not 73–76, as has been
printed{c('J. S. Buckingham, <em>Travels in Palestine</em> (London, 1821), pp. 75–76. An excerpt covering the title page and the Acre pages is in the drive as <code>1821_Buckingham_Travels_EXCERPT_Acre_pp73-78.pdf</code>; the full 35 MB scan is at archive.org.')}; Seetzen finds the moat in use in August 1806{c('Ulrich Jasper Seetzen, <em>Reisen durch Syrien, Palästina, Phönicien, die Transjordan-Länder, Arabia Petraea und Unter-Aegypten</em>, ed. F. Kruse, Zweiter Band (Berlin: G. Reimer, 1854), p. 98. In the drive as <code>1854_Seetzen_Reisen_durch_Syrien_Bd2.pdf</code>.')}; and Gosker’s excavation
of the Ottoman ravelin dates the fortifications archaeologically{c('Joppe Gosker, “A Ravelin Outwork Uncovered in the Ottoman Fortifications of ʿAkko,” <em>ʿAtiqot</em> 111 (2023), free PDF. In the drive. <em>The author is Joppe Gosker, not Alexander, as has been printed elsewhere.</em>')}. <em>The chronology allows the
story. No document names the men.</em> That is the honest verdict, and it is printed as such.</p>

<p>A related correction. The claim that the Orthodox church was “built to a Catholic layout” is a
folk gloss. <strong>A vaulted basilican hall was the ordinary Orthodox form</strong>, and before 1856
no non-Muslim community could lawfully raise a dome — the legal regime is the Gülhane edict of 1839
and the Hatt-ı Hümayun of 1856, whose authoritative English texts are in Hertslet{c('Sir Edward Hertslet, <em>The Map of Europe by Treaty</em>, vol. 2 (London, 1875): the Hatt-ı Sherif of Gülhane, 3 November 1839, no. 188; the Hatt-ı Hümayun, 18 February 1856, no. 263, pp. 1243–49. An excerpt with both edicts is in the drive as <code>1875_Hertslet_Map_of_Europe_v2_EXCERPT_1839_1856_edicts.pdf</code>. <strong>The Fordham Sourcebook texts of both edicts are dead links;</strong> use Hertslet.')}{c('Moshe Maʿoz, <em>Ottoman Reform in Syria and Palestine, 1840–1861: The Impact of the Tanzimat on Politics and Society</em> (Oxford, 1968), on the permit regime for churches, from p. 187. In the drive as <code>1968_Maoz_Ottoman_Reform_Syria_Palestine.pdf</code>.')}. Ramallah had no
Latin church to copy until 1913. The carved <strong>1850 portal date is solid</strong>; the “icons
dated 1830” and the “Byzantine basilica” trace only to unsourced Wikipedia and should not be
printed{c('Verified negative established by this project: neither claim could be traced to any published source.')}.</p>

<h3 class="sub">1834, and the travellers</h3>

<p>The revolt against Ibrāhīm Pasha in 1834 is the one moment in three Ottoman centuries when the
hill country north of Jerusalem enters the historical record in force — conscription, revolt, and the
defeat of the shaykhs who ruled Ramallah’s district. Four years later <strong>Edward Robinson</strong>
arrives, and from 1838 Ramallah stops being a name in a tax register and becomes a place someone
describes: he finds the inhabitants Christian, and counts 200 taxable men{c('Edward Robinson and Eli Smith, <em>Biblical Researches in Palestine, Mount Sinai and Arabia Petraea</em>, vol. ii (Boston: Crocker &amp; Brewster, 1841), 133–34; travels of 1838. In the drive as <code>1841_Robinson_Biblical_Researches_v2.pdf</code>.')}. Guérin describes it
around 1870 and counts 249 houses{c('Victor Guérin, <em>Description géographique, historique et archéologique de la Palestine</em>, Part 2 (Samarie), vol. II (Paris: Imprimerie Nationale, 1875). In the drive as <code>1875_Guerin_Description_de_la_Palestine_Samarie_II.pdf</code>.')}. Conder and Kitchener put it on a proper map in 1873, at p. 13
of the third memoir{c('C. R. Conder and H. H. Kitchener, <em>The Survey of Western Palestine: Memoirs of the Topography, Orography, Hydrography and Archaeology</em>, vol. iii (London: Palestine Exploration Fund, 1883), p. 13; fieldwork 1872–77. In the drive as <code>1883_Conder_Kitchener_Survey_of_Western_Palestine_v3.pdf</code>.')}. Socin gives a figure in 1879 and Schick another in 1896{c('A. Socin, <em>ZDPV</em> 2 (1879), 158; C. Schick, <em>ZDPV</em> 19 (1896), 121.')}.</p>

<p><strong>Between 1852 and 1913 a village of a few hundred acquires the institutional furniture of a
town.</strong> The Church of the Transfiguration in 1852; the Latin Patriarchate school in 1858; Eli
and Sybil Jones and Mariam Karam in 1869; the Girls Training Home in 1889 with fifteen students; the
Melkite church in 1895; and the Friends Boys School from 1901, its cornerstone laid in 1913{c('Rufus M. Jones, <em>Eli and Sybil Jones: Their Life and Work</em> (Philadelphia: Porter &amp; Coates, 1889), 316 pp. + plates. In the drive as <code>1889_Jones_Eli_and_Sybil_Jones.pdf</code>.')}{c('Ramallah Municipality; Latin Patriarchate of Jerusalem, Ramallah parish; Ramallah Friends School history; Philadelphia Yearly Meeting, Middle East Collaborative.')}.
<em>The Quaker schools are the hinge of modern Ramallah</em>: they produced an English-speaking,
American-connected professional class two generations before the Mandate, and they are the reason
the emigration to the United States ran through this town rather than another.</p>
"""))

# ── PART SEVEN
PARTS.append(('Seven', 'Leaving, and the Mandate',
 'From the 1870s the town begins to export its own people, and the Ramallah of the twentieth century is built as much in Detroit and Jacksonville as on the ridge.', f"""
<p>This is the part of the story most families in the American Federation know from the inside, and
it is also where the documents are richest. Emigration from the Bethlehem area began in the 1870s and
reached Ramallah shortly after. Saleh Abdel Jawad’s study of the district finds that Ramallah’s
emigration had a distinctive shape: <strong>a second, family-based wave after the First World War
that continued to 1948</strong>, where neighbouring al-Bīra’s was a single-male pattern{c('Saleh Abdel Jawad, “Landed Property, Palestinian Migration to America and the Emergence of a New Local Leadership,” <em>Jerusalem Quarterly</em> 36. <em>Not downloadable from this environment — the Institute for Palestine Studies site returns 403 to automated requests; it opens normally in a browser.</em>')}. They went to
New York, Baltimore, Chicago, Detroit and San Francisco, and later to Jacksonville, Birmingham,
Cleveland, Houston and Atlanta. <strong>The American Federation of Ramallah, Palestine was founded by
recent immigrants in 1952 and formally federated in Detroit on 7 September 1959.</strong></p>

<p>A number this history will not give: no figure could be verified for how many Ramallah people had
emigrated by 1914 or by 1948. The widely repeated claim that more Ramallawis live abroad than in the
town is plausible and uncited everywhere it appears. Lisa Taraki’s figures are the closest to hard
numbers — <strong>about 1,500 of 6,000 had left by 1946, and over 4,000 Ramallawis were living in
the United States by 1960</strong>{c('Lisa Taraki, “Ordinary Lives: A Small-town Middle Class at the Turn of the Twentieth Century,” <em>Jerusalem Quarterly</em>. <em>Blocked to automated download; opens in a browser.</em>')}. And one story not to borrow: the mother-of-pearl and
olive-wood pilgrim trade is documented for Bethlehem and Bayt Jālā and is often transferred to
Ramallah in popular accounts, with no evidence{c('Verified negative. On the Palestinian Christian trades generally see Jacob Norris, “Dragomans, tattooists, artisans: Palestinian Christians and their encounters with Catholic Europe in the seventeenth and eighteenth centuries,” <em>Journal of Global History</em> 14:1. <em>By Norris, not Tramontana, as has been printed.</em> In the drive as <code>2019_Norris_Dragomans_Tattooists_Artisans.pdf</code>.')}.</p>
{FIGS['pop']}
<p>Between 1908 and 1948 the town acquires the apparatus of modernity and, for the first time, is
counted properly. The municipality is founded in 1908. <strong>Boulos Shehadeh, born in Ramallah in
1882, founds <em>Mirʾāt al-Sharq</em> in Jerusalem on 17 September 1919</strong>; its complete run of
1,770 issues carries more than 1,500 mentions of the town, with Arabic OCR, and it is the most
under-used source in this entire bibliography{c('مجلة مرآة الشرق / <em>Mirʾāt al-Sharq</em>, 1919–1938: 494 issues 1919–29 and 1,276 issues 1930–38, each with its own PDF and Arabic OCR text, free at archive.org. The founding issue of 17 September 1919 is in the drive as <code>1919_Mirat_al-Sharq_no1_1919-09-17.pdf</code>.')}.</p>

<p>Then the censuses. Barron counts 3,104 in 1922{c('J. B. Barron (ed.), <em>Palestine: Report and General Abstracts of the Census of 1922</em> (Jerusalem: Government of Palestine, 1923), the Sub-District of Ramallah table, p. 16. In the drive as <code>1923_Barron_Palestine_Census_1922.pdf</code>; the figure 3,104 is on PDF p. 19 of that scan.')}; Mills counts 4,286 in 1931{c('E. Mills (ed.), <em>Census of Palestine 1931: Population of Villages, Towns and Administrative Areas</em> (Jerusalem: Government of Palestine, 1932), Sub-District Ramallah / <span class="ar">قضاء رام الله</span>. In the drive as <code>1932_Mills_Census_of_Palestine_1931.pdf</code>. <em>Note for citation: the held file is the 1932 preliminary tables volume, not the full two-volume 1933 report.</em>')}; the
Village Statistics of 1945 give 5,080{c('<em>Village Statistics, April 1945</em>; Sami Hadawi, <em>Village Statistics of 1945: A Classification of Land and Area Ownership in Palestine</em>. In the drive as <code>1945_Village_Statistics_Palestine.pdf</code>.')}. And inside Mills’s table is a fact worth pausing on:
<strong>1,941 men to 2,345 women</strong> — 404 more women than men.</p>

<div class="inlinefig">{FIGS['sex']}<div class="inlinecap"><strong>Figure 12.</strong> The demographic
fingerprint of male emigration to America, visible in a government census table. A town that exported
its sons shows it in the sex ratio a generation later.<span class="src">Mills, <em>Census of
Palestine 1931</em>, Sub-District Ramallah.</span></div></div>

<p>In 1948 the town was on the Arab Legion side of the line. <strong>It kept its houses and lost its
hinterland</strong>, and in a matter of days it stopped being a small Christian town: the refugee
camps — al-Amʿari, Jalazone, Qalandiya — are established from 1949 and change its composition
permanently{c('UNRWA camp profiles: al-Amʿari established 1949, 0.096 km², 15,315 registered refugees (2022).')}. The decisive event happened twenty kilometres away, and Ramallah absorbed it.
The first count after the line moved is the Jordanian census of 1961, at 14,759{c('Government of Jordan, Department of Statistics, <em>First Census of Population and Housing, 1961</em>. In the drive as <code>1961_Jordan_First_Census_of_Population_and_Housing.pdf</code>.')}.</p>
"""))

# ── PART EIGHT
PARTS.append(('Eight', 'The City',
 'Jordanian town, occupied town, and then — almost by accident — the seat of a government.', f"""
<p>Two decades under Jordan after the formal annexation of April 1950; then fifty-eight years of
occupation from 1967; and a university at Birzeit that made the town the intellectual centre of the
West Bank. The building at the centre of Ramallah tells the political story on its own: the
<strong>Muqāṭaʿa</strong> was a Tegart fort built by the British in the 1930s, then a Jordanian
headquarters, then an Israeli military government building, then the seat of the Palestinian
Authority. <strong>One compound, five governments</strong> — which is why the town became a capital
without ever being declared one.</p>

<p>The numbers for the modern town are good and recent. The PCBS census of 2017 gives Ramallah at
38,998 and al-Bīra at 45,975; the 2024 projections are 43,880 and 49,657; the governorate held
279,730 at the 2007 census and is projected at 355,202{c('Palestinian Central Bureau of Statistics, <em>Census 2017: Final Results Summary — Ramallah and al-Bireh Governorate</em> (Ramallah: PCBS, February 2019), bilingual Arabic/English. In the drive as <code>2019_PCBS_Census_2017_Ramallah_al-Bireh_Governorate.pdf</code>.')}. Christians were 32 per cent of Ramallah
in 1997; across Palestine they fell from 1.5 per cent of the population in 1997 to 1.0 at the 2017
census — about 46,850 people{c('PCBS census series 1997, 2007, 2017. Bernard Sabella estimates that some 35 per cent of Palestinian Christians emigrated after 1967. No census-grade current figure for Ramallah city alone could be verified.')}.</p>

<p><strong>What the numbers mean is contested — and the best critic is a Ramallah sociologist.</strong>
Lisa Taraki’s “Enclave Micropolis” takes the “Ramallah bubble” critique seriously — the villas of
al-Masyoun and al-Tireh against the Amʿari, Jalazon and Qalandiya camps, the NGO salaries, the rents —
and then argues that it misreads what is happening. What looks like a bubble is also genuine
urbanisation, in the only place the occupation left room for it. Her own number for the constraint:
<strong>West Bank checkpoints rose from 376 in August 2005 to 540 in December 2006</strong>{c('Lisa Taraki, “Enclave Micropolis: The Paradoxical Case of Ramallah/al-Bireh,” <em>Journal of Palestine Studies</em>. In the drive as <code>2008_Taraki_Enclave_Micropolis_Ramallah_al-Bireh.pdf</code>.')}.</p>

<p>And the history has something to say about that. <strong>Ramallah has been a substitute for
somewhere else before.</strong> It was founded by people who could not stay at Karak; refounded in
1948 by people who could not stay at Lydda; and made a capital in 1995 by a government that could not
sit in Jerusalem{c('Christopher Harker, Reema Shebeitah and Dareen Sayyad, “Ghosts of Jerusalem: Ramallah’s Haunted Urbanism,” <em>Jerusalem Quarterly</em> 58, on the town’s relationship to the city it replaced. In the drive as <code>2014_Harker_Ghosts_of_Jerusalem_JQ58.pdf</code>.')}. A town built three times by people arriving from a place they had to
leave is not an accident of the last thirty years. <em>It is the pattern of the whole story, and this
family is one of its first instances.</em></p>
"""))

# ── PART NINE
PARTS.append(('Nine', 'The Evidence',
 'What this reconstruction rests on, what it could not establish, and the five things that would change the picture.', f"""
{FIGS['master']}
<p>Reading down the story, the grades fall as Figure 1 shows. <strong>Adam to Joktan</strong> is
scripture. <strong>Joktan to Jafna</strong> is classical scholarship, datable to c. 660–900 CE:
inherited, not invented here, and not the family’s to defend. <strong>The Jafnid phylarchs</strong>
are attested history. <strong>Jafna to Rāshid</strong> is nothing at all, and the chart itself says
so. <strong>The hills before 1562</strong> are attested — excavated churches, a Frankish charter, a
waqf deed of 1279. <strong>The founding and everything after</strong> is documents.</p>

<h3 class="sub">Where the family’s own telling stands</h3>

<p>Eight claims were tested against the record, and most survive. Descent from the Ghassanid kings is
<strong>open</strong> — no evidence either way across nine hundred years, and the claim belongs to a
recognised genre. The departure “about 300 AD” is <strong>corrected</strong>. The road through the
Ḥijāz, Udhruḥ, Shawbak and Karak is <strong>consistent</strong>, and its last legs are
<strong>confirmed</strong> station by station in the registers. The founder and the date are
<strong>refined</strong>: 1562, with the movers a generation or two below Rāshid. The Patriarchate’s
grant of Khirbat Ramallah is <strong>untested</strong> — no independent documentation has been
produced, and the Jerusalem court registers survive from 1529 and have never been searched for
it{c('The Jerusalem sharīʿa sijills survive from 1529; thirty-seven volumes are published open access by IRCICA. Seven have been read for this project; volumes 43, 44, 46, 49, 51 and 54–56 cover the 1560s–70s and are unread.')}. The departure after a refused marriage proposal has <strong>no documentary trace</strong>, as
one would expect of a family reason.</p>

<h3 class="sub">Four archives and one laboratory</h3>

<p>None of this is settled for ever, and four of the five things that would change it could be
finished in a season by one person with Arabic and a library card.</p>

<ol class="actions">
<li><strong>Verify sijill 48, p. 54 against the page images.</strong> The volume is now in the drive.
This is the highest-value half-hour available to the project, and everything in Part Five above the
reconciliation depends on it.</li>
<li><strong>Open al-Bakhīt and al-Sawāriyya’s published Jerusalem registers, volume four.</strong>
They print taxpayers by name. Do the Christian household heads at Ramallah in 1562 carry the clan
names?{c('Muḥammad ʿAdnān al-Bakhīt and Nūfān Rajā al-Sawāriyya (eds.), <em>Daftar mufaṣṣal liwāʾ al-Quds al-sharīf</em>, 6 vols. (London: al-Furqān, 2005–11). Volume 4, ISBN 9781788146395, about £30 — the cheapest decisive item in the whole project.')} <em>Settles the founding.</em></li>
<li><strong>Then the Karak side.</strong> The ʿAjlūn defter of the same year, published in Amman in
1989. Are there Ḥaddādīn households at Karak or Maʿīn? <em>Settles the crossing.</em></li>
<li><strong>Then the other twenty-two IRCICA volumes</strong>, and Yāqūt’s Jerusalem-district village
roster mapped against the 1562 defter — a day’s work nobody has done. <em>Fills the emptiest
century</em>, with Tramontana and Zeʾevi beside it.</li>
<li><strong>And in parallel, the test.</strong> Sixteen men, two per clan line, plus volunteers from
the Karak Ḥaddādīn; roughly $450 each. It runs while the archives are being read. <em>The one result
nobody else can get</em> — though note its limit honestly: a Y-DNA date can tell 600 from 1500, and
it cannot tell 1200 from 1500{c('On the honest state of Levantine population genetics see Marc Haber et al., <em>PLOS Genetics</em> 9:2 (2013): e1003316, and Haber et al., <em>American Journal of Human Genetics</em> 101:2 (2017), 274–282.')}.</li>
</ol>

<p>And one that will not work: <strong>no archive will name the missing generations.</strong> That is
a fact about the record, and it is shared by every village family in Palestine.</p>

<h3 class="sub">What the story is</h3>

<p class="close">A town founded in 1562 by Christians walking up from Bayt Jālā, on a ridge that had
held a church a thousand years before they got there, by a family that remembers coming from Karak
and believes it came from Ghassān — on a piece of ground that already bore the name
<em>Rām Allāh</em> in a Mamluk deed of 1279. <strong>Most of that can be documented. One stretch of
it never will be.</strong> Printing the gap, and saying which is which, is what makes the rest of it
worth trusting.</p>
"""))

# ═════════════════════════════ assemble
CSS = """
:root{--gold:#B98A4E;--grey:#77726A;--folio:#9A958C;--ink:#1A1A1A;--body:#46423B;
 --rule:#DCD6C9;--green:#007A3D;--dark:#004A26;--lighttext:#F3ECDD;--cream:#FFFAF0;--tan:#D4B483}
*{box-sizing:border-box}
body{margin:0;background:var(--cream);color:var(--ink);
 font:17px/1.62 "Times New Roman",Times,"Liberation Serif",Georgia,serif}
.wrap{max-width:900px;margin:0 auto;padding:0 26px}
.mastrow{display:flex;justify-content:space-between;align-items:baseline;padding-top:20px;
 font:11px/1.4 "Times New Roman",Times,serif;letter-spacing:.22em;text-transform:uppercase}
.mastrow .l{color:var(--gold);font-weight:700}.mastrow .r{color:var(--grey);letter-spacing:.12em}
hr.rule{border:0;border-top:1px solid var(--rule);margin:9px 0 26px}
h1{font-size:2.6rem;line-height:1.1;margin:0 0 8px;font-weight:700}
.sub-t{color:var(--grey);font-style:italic;font-size:1.14rem;margin:0 0 14px}
.meta{color:var(--folio);font-size:.86rem;margin:0 0 30px}
.lede{font-size:1.12rem;border-left:3px solid var(--gold);padding:2px 0 2px 20px;margin:0 0 12px;color:var(--body)}
.part{background:var(--dark);color:var(--lighttext);border-radius:12px;padding:30px 34px;margin:56px 0 0}
.part .pn{font:700 .64rem/1.4 inherit;letter-spacing:.28em;color:#9BC3A8;text-transform:uppercase;display:block;margin-bottom:10px}
.part h2{font-size:2.05rem;margin:0;font-weight:700;line-height:1.14}
.part .pd{color:#CFE3D6;font-style:italic;margin:14px 0 0;font-size:1.02rem}
.part .pd::before{content:"";display:block;width:110px;border-top:3px solid #3E7A56;margin:0 0 14px}
.pbody{background:#fff;border:1px solid var(--rule);border-top:0;border-radius:0 0 12px 12px;padding:32px 36px 28px}
.pbody p{margin:0 0 15px;color:var(--body)}
.pbody p strong{color:var(--ink)}
h3.sub{font-size:1.06rem;margin:30px 0 12px;color:var(--green);font-weight:700;letter-spacing:.05em;text-transform:uppercase}
blockquote{margin:22px 0;padding:16px 22px;background:var(--cream);border-left:3px solid var(--tan);
 font-style:italic;color:var(--body);font-size:.99rem;border-radius:0 5px 5px 0}
blockquote .cite{display:block;font-style:normal;color:var(--grey);font-size:.85rem;margin-top:9px;line-height:1.5}
.ar{font-size:1.14em;direction:rtl;unicode-bidi:isolate;font-style:normal}
sup.cn{font-size:.66em;line-height:0}
sup.cn a{color:var(--green);text-decoration:none;font-weight:700;padding:0 1px}
sup.cn a:hover{text-decoration:underline}
figure{margin:26px 0;background:#FCFBF8;border:1px solid var(--rule);border-radius:8px;padding:18px 20px 14px}
.fignum{font:700 .68rem/1.4 inherit;letter-spacing:.18em;text-transform:uppercase;color:var(--gold)}
.figtitle{font-weight:700;font-size:1.06rem;margin:2px 0 12px;color:var(--ink)}
.figwrap{background:#FCFBF8;border-radius:5px;overflow:hidden}
figcaption{font-size:.88rem;color:var(--body);margin-top:12px;line-height:1.5}
figcaption .src{display:block;color:var(--folio);font-size:.82rem;font-style:italic;margin-top:6px}
.inlinefig{display:flex;gap:22px;align-items:flex-start;margin:26px 0;background:#FCFBF8;
 border:1px solid var(--rule);border-radius:8px;padding:18px 20px}
.inlinefig>svg,.inlinefig>*:first-child{flex:0 0 240px;max-width:240px}
.inlinecap{font-size:.88rem;color:var(--body);line-height:1.5}
.inlinecap .src{display:block;color:var(--folio);font-size:.82rem;font-style:italic;margin-top:6px}
ol.actions{margin:16px 0;padding-left:22px}
ol.actions li{margin-bottom:12px;color:var(--body)}
p.close{font-size:1.1rem;background:var(--cream);border-left:3px solid var(--gold);padding:16px 20px;border-radius:0 6px 6px 0}
.notes{background:#fff;border:1px solid var(--rule);border-radius:10px;padding:26px 30px;margin:56px 0 0}
.notes h2{font-size:1.4rem;margin:0 0 6px;border-bottom:2px solid var(--gold);padding-bottom:8px}
.notes p.intro{color:var(--grey);font-style:italic;font-size:.92rem;margin:10px 0 18px}
ol.notelist{margin:0;padding-left:0;list-style:none;counter-reset:n}
ol.notelist li{counter-increment:n;font-size:.87rem;color:var(--body);padding:7px 0 7px 34px;
 border-top:1px solid var(--rule);position:relative;line-height:1.5}
ol.notelist li::before{content:counter(n);position:absolute;left:0;top:7px;color:var(--green);
 font-weight:700;font-size:.8rem}
ol.notelist li:first-child{border-top:0}
ol.notelist code{font:11px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;color:#1e6b34;
 background:#F0F5F0;border-radius:3px;padding:1px 5px;word-break:break-all}
footer{margin:40px 0;color:var(--folio);font-size:.85rem;line-height:1.6}
@media print{body{background:#fff}.part{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
@media(max-width:640px){.inlinefig{flex-direction:column}.wrap{padding:0 16px}}
"""

body = []
for num, title, deck, txt_ in PARTS:
    body.append(f'<section><div class="part"><span class="pn">Part {num}</span>'
                f'<h2>{title}</h2><p class="pd">{deck}</p></div>'
                f'<div class="pbody">{txt_}</div></section>')

notes = '\n'.join(f'<li id="n{i+1}">{t} <a href="#r{i+1}" class="back">↩</a></li>'
                  for i, t in enumerate(CITES))

DOC = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Family, Reconstructed — Ramallah from Adam to today</title>
<style>{CSS}</style></head><body><div class="wrap">
<div class="mastrow"><span class="l">Ramallah Family Tree</span>
<span class="r">The family, reconstructed &middot; version 1</span></div>
<hr class="rule">
<h1>The Family, Reconstructed</h1>
<p class="sub-t">Rāshid El-Haddadeen Al-Ghassani and his descendants — the whole story from Adam and
Eve to the city of today, drawn from the eighty volumes now on the shelf.</p>
<p class="meta">American Federation of Ramallah, Palestine &middot; the Family Tree Project &middot;
16 August 2026 &middot; fifteen figures &middot; {len(CITES)} notes</p>
<p class="lede">Every stretch of this history is marked with what holds it up, and every claim carries
its source. The figures are drawn from the documents themselves — the Ottoman registers, the
censuses, the inscriptions, the deed of 1279. Where the record is empty the page says so and shows
the shape of the emptiness, because a family history that hides its gaps cannot be trusted about
anything else.</p>
{''.join(body)}
<div class="notes"><h2>Notes</h2>
<p class="intro">Sources are cited in full at first mention. A green filename means the PDF is in
<em>AFRP / Family Tree / Literature</em> and can be opened while you read; where a source is free but
could not be retrieved automatically, that is said too.</p>
<ol class="notelist">{notes}</ol></div>
<footer>
<p><strong>Corrections established by this project and carried into this text:</strong> Ghassān is a
spring, not an ancestor; Qaḥṭān to Jafna is sixteen generations, not fifteen; the “45 generations” of
the void implies an impossible generational interval; the Maʾrib breaches are 449–450 and 543–548,
not c. 300; <em>Rām Allāh</em> is a named place in 1279; the founding is 1562; Yāqūt saw the
Palestinian al-Bīra himself; Mujīr al-Dīn has five occurrences of <span class="ar">البيرة</span>, not
six; the Barghūthī shaykhdom postdates the sixteenth-century registers; Banī Ḥārith is not attested
in these hills before the sixteenth century; Buckingham on Acre is pp. 75–76; the ʿAtiqot ravelin
author is Joppe Gosker; “built to a Catholic layout” is a folk gloss; the Fordham texts of the 1839
and 1856 edicts are dead links.</p>
<p>Built on <em>The History of Ramallah</em> v1 (52 slides), the annotated bibliography, fourth
edition (379 entries in thirty sections), <em>The Eastern Sources</em>, and the four book chapters.
Chart palette validated for colour-vision deficiency; every series is direct-labelled.</p>
</footer>
</div></body></html>
"""
open(OUT, 'w', encoding='utf-8', newline='\n').write(DOC)
print('written', OUT, len(DOC), 'bytes,', len(CITES), 'citations')
