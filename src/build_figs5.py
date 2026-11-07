# -*- coding: utf-8 -*-
"""v61 figures drawn directly in the family tree book's palette (green, ochre,
ink on white): the rulers of the Hellenistic centuries, the rulers and the
Christian traces of 636–1517, and the camps of 1948."""
import build_recon as R
import build_atlas as A

txt = R.txt
GREEN, DEEP, OCHRE, OCHRE_L = '#007A3D', '#004A26', '#9A6324', '#C49A5E'
INK, BODY, GREY, FOLIO, RULE = '#1A1915', '#3D3A35', '#6B6760', '#8F8A80', '#D9D4C8'
PALE_G, PALE_O, WHITE = '#DFEEE6', '#F6EFE3', '#FFFFFF'


def _plate(W, H, kicker, sub, aria):
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{aria}">',
         f'<rect width="{W}" height="{H}" fill="{WHITE}"/>',
         txt(40, 32, kicker, 11, OCHRE, 'start', '700', 'normal', '1.35'),
         txt(40, 50, sub, 10.4, GREY, 'start', '400', 'italic')]
    return s


def _foot(s, W, H, bold, note):
    s.append(f'<line x1="40" y1="{H-44}" x2="{W-40}" y2="{H-44}" stroke="{RULE}"/>')
    s.append(txt(40, H - 26, bold, 10.2, BODY, 'start', '700'))
    s.append(txt(40, H - 11, note, 9.4, GREY, 'start', '400', 'italic'))


def _band(s, x0, x1, y, h, fill, label, sub='', tc=WHITE):
    s.append(f'<rect x="{x0:.1f}" y="{y}" width="{x1-x0:.1f}" height="{h}" fill="{fill}" stroke="{WHITE}" stroke-width="1.5"/>')
    if x1 - x0 > 38:
        s.append(txt((x0 + x1) / 2, y + h / 2 + (0 if sub and x1 - x0 > 80 else 4), label, 10, tc, 'middle', '700'))
        if sub and x1 - x0 > 80:
            s.append(txt((x0 + x1) / 2, y + h / 2 + 13, sub, 8.6, tc, 'middle', '400', 'italic'))


# ══════════════════ the Hellenistic centuries: six sovereigns ══════════════
def fig_sovereigns():
    W, H = 860, 330
    s = _plate(W, H, 'SIX SOVEREIGNS OVER ONE RIDGE, 539–63 BC',
               'Who ruled these hills, reign by reign, above the people who farmed them throughout.',
               'Timeline of the rulers of the Ramallah ridge from 539 to 63 BC, over a continuous band for the villages')
    X0, X1, Y0, Y1 = 60, 820, 545, 40           # BC years: left = older

    def px(bc):
        return X0 + (Y0 - bc) / (Y0 - Y1) * (X1 - X0)
    reigns = [(539, 332, 'Persia', 'Achaemenid kings', DEEP),
              (332, 301, 'Macedon', 'Alexander, 332', OCHRE),
              (301, 200, 'Ptolemies', 'from Egypt', GREEN),
              (200, 140, 'Seleucids', 'from Syria', OCHRE),
              (140, 63, 'Hasmoneans', 'local kings', GREEN)]
    y = 82
    s.append(txt(X0, y - 8, 'WHO RULED', 8.6, FOLIO, 'start', '700', 'normal', '1.2'))
    for a, b, lab, sub, col in reigns:
        _band(s, px(a), px(b), y, 46, col, lab, sub)
    s.append(f'<rect x="{px(63):.1f}" y="{y}" width="{X1-px(63):.1f}" height="46" fill="{INK}"/>')
    s.append(txt(px(63) + 6, y + 27, 'Rome', 10, WHITE, 'start', '700'))
    # the people
    y2 = 168
    s.append(txt(X0, y2 - 8, 'WHO LIVED HERE', 8.6, FOLIO, 'start', '700', 'normal', '1.2'))
    s.append(f'<rect x="{X0}" y="{y2}" width="{X1-X0}" height="34" fill="{PALE_G}"/>')
    s.append(f'<line x1="{X0}" y1="{y2+17}" x2="{X1}" y2="{y2+17}" stroke="{GREEN}" stroke-width="3"/>')
    s.append(txt((X0 + X1) / 2, y2 + 13, 'the villages of the ridge, the same families on the same terraces', 9.6, DEEP, 'middle', '700'))
    s.append(txt((X0 + X1) / 2, y2 + 30, 'five changes of sovereign, no change of population', 9, DEEP, 'middle', '400', 'italic'))
    # axis
    ya = 222
    s.append(f'<line x1="{X0}" y1="{ya}" x2="{X1}" y2="{ya}" stroke="{FOLIO}"/>')
    for bc in (500, 400, 300, 200, 100):
        s.append(f'<line x1="{px(bc):.1f}" y1="{ya}" x2="{px(bc):.1f}" y2="{ya+5}" stroke="{FOLIO}"/>')
        s.append(txt(px(bc), ya + 16, f'{bc} BC', 8.8, FOLIO, 'middle'))
    # markers
    marks = [(538, 'edict of return, 538'), (259, 'Zenon’s journey, 259'), (63, 'Pompey, 63')]
    for bc, lab in marks:
        x = px(bc)
        s.append(f'<line x1="{x:.1f}" y1="{y}" x2="{x:.1f}" y2="{ya}" stroke="{OCHRE}" stroke-width="1" stroke-dasharray="3 3"/>')
        s.append(f'<rect x="{x-3.5:.1f}" y="{ya-3.5:.1f}" width="7" height="7" fill="{OCHRE}" transform="rotate(45 {x:.1f} {ya})"/>')
        s.append(txt(x, ya + 32, lab, 9, OCHRE, 'middle' if 100 < bc < 500 else ('start' if bc >= 500 else 'end'), '700'))
    _foot(s, W, H, 'Empires came from Persia, Macedon, Egypt and Syria; the farmers of these hills stayed where they were.',
          'Dates of rule as conventionally given; the Hasmonean start is taken as c. 140 BC. The Zenon papyri record Greek business letters from these towns in 259 BC.')
    s.append('</svg>')
    return ''.join(s)


# ══════════════════ 636–1517: who ruled, and who stayed ═════════════════════
def fig_rulers_traces():
    W, H = 860, 446
    s = _plate(W, H, 'WHO RULED, AND WHO STAYED, 636–1517',
               'The dynasties above; below, every dated trace of the ridge’s Christians that this book prints.',
               'Timeline of rulers from 636 to 1517 with dated traces of the Christian villages around Ramallah')
    X0, X1, A0, A1 = 50, 830, 620, 1530

    def px(ad):
        return X0 + (ad - A0) / (A1 - A0) * (X1 - X0)
    y = 80
    s.append(txt(X0, y - 8, 'WHO RULED', 8.6, FOLIO, 'start', '700', 'normal', '1.2'))
    reigns = [(636, 661, 'Rāshidūn', '', DEEP), (661, 750, 'Umayyads', '', GREEN),
              (750, 970, 'ʿAbbāsids', 'and their governors', DEEP), (970, 1099, 'Fāṭimids', 'Seljuks 1073–98', GREEN),
              (1099, 1187, 'Franks', '', INK), (1187, 1260, 'Ayyūbids', '', OCHRE), (1260, 1517, 'Mamlūks', '', DEEP)]
    for a, b, lab, sub, col in reigns:
        _band(s, px(a), px(b), y, 46, col, lab, sub)
    y2 = 150
    s.append(txt(X0, y2 - 8, 'WHO STAYED', 8.6, FOLIO, 'start', '700', 'normal', '1.2'))
    s.append(f'<rect x="{px(636):.1f}" y="{y2}" width="{px(1517)-px(636):.1f}" height="58" fill="{PALE_G}"/>')
    s.append(txt(px(1075), y2 + 13, 'the Christian villages of the ridge — Jifnā, ʿAbūd, al-Bīra, Bīr Zayt, al-Ṭayyiba', 9.4, DEEP, 'middle', '700'))
    yl = y2 + 40
    s.append(f'<line x1="{px(636):.1f}" y1="{yl}" x2="{px(1517):.1f}" y2="{yl}" stroke="{GREEN}" stroke-width="3"/>')
    ya = y2 + 72
    s.append(f'<line x1="{X0}" y1="{ya}" x2="{X1}" y2="{ya}" stroke="{FOLIO}"/>')
    for ad in range(700, 1501, 100):
        s.append(f'<line x1="{px(ad):.1f}" y1="{ya}" x2="{px(ad):.1f}" y2="{ya+5}" stroke="{FOLIO}"/>')
        s.append(txt(px(ad), ya + 16, str(ad), 8.8, FOLIO, 'middle'))
    traces = [(636, '636', 'Yarmūk — the conquest'),
              (684, '684', 'Marj Rāhiṭ — Ghassān still a people'),
              (890, 'c. 890', 'al-Yaʿqūbī finds Ghassān east of the Jordan'),
              (1058, '1058', 'the church at ʿAbūd rebuilt, and dated'),
              (1156, '1156', 'Magna Mahumeria: the charter names Franks only'),
              (1182, '1182', 'Raymundus de Jafenia signs a charter'),
              (1186, '1186', 'RAMALLAH first written: “qua vaditur Ramelie”'),
              (1218, '1217–18', 'Thietmar finds Christians at Shawbak'),
              (1279, '1279–80', 'Qalāwūn’s waqf: Ramallah is endowment land'),
              (1321, '1321', 'a Christian majority still at Shawbak'),
              (1391, '1391–92', 'men of Jifnā in the Ḥaram documents')]
    for n, (ad, d, note) in enumerate(traces, 1):
        x = px(ad); key = ad == 1186
        col = OCHRE if key else GREEN
        yy = yl - (11 if n % 2 else -11) * (1 if not key else 0)
        if not key:
            s.append(f'<line x1="{x:.1f}" y1="{yl}" x2="{x:.1f}" y2="{yy:.1f}" stroke="{col}" stroke-width="1"/>')
        r = 8.5 if key else 6.8
        s.append(f'<circle cx="{x:.1f}" cy="{yy:.1f}" r="{r}" fill="{col}" stroke="{WHITE}" stroke-width="1.4"/>')
        s.append(txt(x, yy + 3.2, str(n), 8.6 if key else 7.6, WHITE, 'middle', '700'))
        col_i, row = (n - 1) // 6, (n - 1) % 6
        lx, ly = 70 + col_i * 390, ya + 44 + row * 21
        s.append(f'<circle cx="{lx}" cy="{ly-3.5}" r="7" fill="{col}"/>')
        s.append(txt(lx, ly, str(n), 7.8, WHITE, 'middle', '700'))
        s.append(txt(lx + 14, ly, f'<tspan font-weight="700">{d}</tspan>  {note}', 10 if key else 9.6, OCHRE if key else INK, 'start', '700' if key else '400'))
    _foot(s, W, H, 'Seven dynasties in nine centuries. The people underneath them leave dated traces in every one.',
          'Traces are those printed in this chapter and the next, each with its own note. Reign dates as conventionally given; the Franks held Jerusalem again in 1229–44.')
    s.append('</svg>')
    return ''.join(s)


# ══════════════════ 1948: where the road stopped ════════════════════════════
def fig_camps():
    W, H = 860, 580
    s = _plate(W, H, 'WHERE THE ROAD STOPPED — LYDDA AND RAMLE TO THE CAMPS AROUND RAMALLAH, 1948–49',
               'The march east of 13 July 1948, and the five camps of this district, joined to the towns and villages their people came from.',
               'Map of the expulsion from Lydda and Ramle and the refugee camps around Ramallah')
    M = A.Sheet(*A.fit_box(34.70, 35.32, 31.74, 32.10, 772, 400), 44, 70, 772, 400)
    M.base(s, '10m'); M.graticule(s, 0.1, 0.1); M.close(s)
    camps = [(31.9055, 35.2085, 'Qaddūra · inside the town, 1948', 12, -4, 'start'),
             (31.8925, 35.2150, 'al-Amʿarī · al-Bīra, 1949', 12, 8, 'start'),
             (31.9480, 35.2100, 'al-Jalazūn · 1949', 12, 2, 'start'),
             (31.8686, 35.2240, 'Qalandiyā · 1949', 12, 10, 'start'),
             (31.9686, 35.1075, 'Dayr ʿAmmār · 1948–49', 0, -12, 'middle')]
    origins = [(31.951, 34.895, 'al-Lidd (Lydda)', -10, -10, 'end'),
               (31.927, 34.866, 'al-Ramla', -10, 14, 'end'),
               (32.050, 34.755, 'Jaffa', 10, -8, 'start'),
               (31.985, 34.948, 'Bayt Nabāla', 0, -12, 'middle'),
               (31.795, 35.197, 'Lifta', -10, 12, 'end')]
    links = [(0, 1), (0, 2), (0, 0), (1, 1), (1, 0), (2, 1), (2, 0),
             (3, 2), (3, 4), (4, 3), (4, 0)]
    for oi, ci in links:
        (ola, olo), (cla, clo) = origins[oi][:2], camps[ci][:2]
        x0, y0 = M.P(ola, olo); x1, y1 = M.P(cla, clo)
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2 - 18
        s.append(f'<path d="M{x0:.1f} {y0:.1f} Q{mx:.1f} {my:.1f} {x1:.1f} {y1:.1f}" fill="none" '
                 f'stroke="{OCHRE_L}" stroke-width="1.2" opacity=".85"/>')
    A.route(s, M, [(31.951, 34.895), (31.945, 34.97), (31.950, 35.02), (31.925, 35.10), (31.905, 35.20)],
            col=OCHRE, w=3.0, dash='8 5')
    rx, ry = M.P(31.935, 35.03)
    A.label(s, rx, ry, 'the march of 13 July, on foot (route approximate)', 0, 18, 'middle', 9.4, OCHRE, '700')
    for la, lo, nm, dx, dy, an in origins:
        x, y = A.dot(s, M, la, lo, OCHRE, 5.2)
        A.label(s, x, y, nm, dx, dy, an, 10)
    rx, ry = M.P(31.9038, 35.2034)
    for la, lo, nm, dx, dy, an in camps:
        x, y = M.P(la, lo)
        s.append(f'<rect x="{x-5:.1f}" y="{y-5:.1f}" width="10" height="10" fill="{GREEN}" stroke="{WHITE}" stroke-width="1.5" transform="rotate(45 {x:.1f} {y:.1f})"/>')
        A.label(s, x, y, nm, dx, dy, an, 9.8, DEEP)
    M.scalebar(s); M.north(s)
    A._legend(s, H - 66, [('dot', OCHRE, 'town or village the refugees came from'),
                          ('dia', GREEN, 'camp, with the year it was set up'),
                          ('line', OCHRE, 'the march east')])
    _foot(s, W, H, 'Qalandiyā holds the Jerusalem corridor; al-Amʿarī and al-Jalazūn hold Lydda, Ramle and Jaffa. The camps are where the road stopped.',
          'Origins and dates from the camp table in this chapter (UNRWA; ARIJ camp profiles, 2012). Ramallah town itself is beside Qaddūra. Natural Earth coastlines.')
    s.append('</svg>')
    return ''.join(s)
