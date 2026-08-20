# -*- coding: utf-8 -*-
"""An atlas engine for the book's maps.

Real Natural Earth coastlines, lakes and rivers, drawn flat — tan land on blue
water, named seas set in the water, a scale bar in kilometres and a north arrow.
No hill shading: every mark on the page is data.

Geometry is projected, not plotted raw: a Lambert conformal conic for regional
sheets, so shapes and distances are honest at these latitudes.
"""
import math, os, functools
import shapefile                      # pyshp, pulled in by geopandas
import cartopy.io.shapereader as shpreader

import build_recon as R
txt, esc = R.txt, R.esc

GOLD, GREY, RULE, FOLIO = '#B98A4E', '#77726A', '#DCD6C9', '#9A958C'
INK, BODY, DARK = '#1A1A1A', '#46423B', '#004A26'
GREEN, RUST, PLUM = '#007A3D', '#A85210', '#6D4E9E'
SURF = '#FCFBF8'
# the atlas palette
SEA      = '#CFE0E8'
SEA_DEEP = '#B9D2DD'
SEALINE  = '#8FB2C2'
LAND     = '#F0E7D3'
LAND_HI  = '#E7DBC0'
COAST    = '#A08E6A'
RIVER    = '#8FB2C2'
GRAT     = '#DED4BE'


# ─────────────────────────────── data
@functools.lru_cache(maxsize=None)
def _shp(res, cat, name):
    return shapefile.Reader(shpreader.natural_earth(resolution=res, category=cat, name=name))


def _clip_poly(pts, box):
    """Sutherland–Hodgman against a lon/lat rectangle. The Afro-Eurasian land
    polygon is one part with eighty thousand points; without this, a map of one
    district inlines the coastline of three continents."""
    lon0, lon1, lat0, lat1 = box
    def inside(p, e):
        return (p[0] >= lon0 if e == 0 else p[0] <= lon1 if e == 1 else
                p[1] >= lat0 if e == 2 else p[1] <= lat1)
    def isect(a, b, e):
        if e in (0, 1):
            x = lon0 if e == 0 else lon1
            t = (x - a[0]) / (b[0] - a[0]) if b[0] != a[0] else 0.0
            return (x, a[1] + t * (b[1] - a[1]))
        y = lat0 if e == 2 else lat1
        t = (y - a[1]) / (b[1] - a[1]) if b[1] != a[1] else 0.0
        return (a[0] + t * (b[0] - a[0]), y)
    out = list(pts)
    for e in range(4):
        if not out:
            return []
        src, out = out, []
        prev = src[-1]
        for cur in src:
            if inside(cur, e):
                if not inside(prev, e):
                    out.append(isect(prev, cur, e))
                out.append(cur)
            elif inside(prev, e):
                out.append(isect(prev, cur, e))
            prev = cur
    return out


def _clip_line(pts, box):
    """Split an open polyline into the runs that fall inside the box."""
    lon0, lon1, lat0, lat1 = box
    runs, cur = [], []
    for p in pts:
        if lon0 <= p[0] <= lon1 and lat0 <= p[1] <= lat1:
            cur.append(p)
        else:
            if len(cur) > 1:
                runs.append(cur)
            cur = []
    if len(cur) > 1:
        runs.append(cur)
    return runs


@functools.lru_cache(maxsize=None)
def _feats(res, cat, name, bbox, poly=True):
    """Shapes clipped to a lon/lat bbox."""
    lon0, lon1, lat0, lat1 = bbox
    pad = max((lon1 - lon0), (lat1 - lat0)) * 0.04
    box = (lon0 - pad, lon1 + pad, lat0 - pad, lat1 + pad)
    out = []
    r = _shp(res, cat, name)
    for sh in r.shapes():
        bb = sh.bbox
        if bb[0] > box[1] or bb[2] < box[0] or bb[1] > box[3] or bb[3] < box[2]:
            continue
        pts = sh.points
        parts = list(sh.parts) + [len(pts)]
        for i in range(len(parts) - 1):
            seg = pts[parts[i]:parts[i + 1]]
            if len(seg) < 2:
                continue
            xs = [q[0] for q in seg]; ys = [q[1] for q in seg]
            if min(xs) > box[1] or max(xs) < box[0] or min(ys) > box[3] or max(ys) < box[2]:
                continue
            if poly:
                c = _clip_poly(seg, box)
                if len(c) > 2:
                    out.append(c)
            else:
                out.extend(_clip_line(seg, box))
    return out


def fit_box(lon0, lon1, lat0, lat1, w, h):
    """Widen or heighten a lon/lat box so its true proportions match a panel of
    w x h. Returns a new box. Prevents both letterboxing and invented ocean."""
    latm = math.radians((lat0 + lat1) / 2)
    dlon, dlat = lon1 - lon0, lat1 - lat0
    want = (w / h) * dlat / math.cos(latm)          # required lon span
    if want > dlon:
        c = (lon0 + lon1) / 2
        lon0, lon1 = c - want / 2, c + want / 2
    else:
        wantlat = (h / w) * dlon * math.cos(latm)
        c = (lat0 + lat1) / 2
        lat0, lat1 = c - wantlat / 2, c + wantlat / 2
    return lon0, lon1, lat0, lat1


# ─────────────────────────────── projection
class Sheet:
    """A Lambert conformal conic sheet with a pixel viewport."""

    def __init__(self, lon0, lon1, lat0, lat1, x, y, w, h, pad=0.0):
        self.bbox = (lon0 - pad, lon1 + pad, lat0 - pad, lat1 + pad)
        self.pathtol = 1.15
        self.x, self.y, self.w, self.h = x, y, w, h
        self.lam0 = math.radians((lon0 + lon1) / 2)
        span = lat1 - lat0
        p1, p2 = math.radians(lat0 + span / 6), math.radians(lat1 - span / 6)
        if abs(p1 - p2) < 1e-9:
            p2 = p1 + 1e-6
        self.n = (math.log(math.cos(p1) / math.cos(p2)) /
                  math.log(math.tan(math.pi / 4 + p2 / 2) / math.tan(math.pi / 4 + p1 / 2)))
        self.F = (math.cos(p1) * math.tan(math.pi / 4 + p1 / 2) ** self.n) / self.n
        self.rho0 = self.F / math.tan(math.pi / 4 + math.radians((lat0 + lat1) / 2) / 2) ** self.n
        # fit
        xs, ys = [], []
        for la in (lat0, (lat0 + lat1) / 2, lat1):
            for lo in (lon0, (lon0 + lon1) / 2, lon1):
                a, b = self._raw(la, lo); xs.append(a); ys.append(b)
        self.rx0, self.rx1 = min(xs), max(xs)
        self.ry0, self.ry1 = min(ys), max(ys)
        sx = w / (self.rx1 - self.rx0)
        sy = h / (self.ry1 - self.ry0)
        self.s = min(sx, sy)
        mw = (self.rx1 - self.rx0) * self.s
        mh = (self.ry1 - self.ry0) * self.s
        self.ox = x + (w - mw) / 2
        self.oy = y + (h - mh) / 2
        # Snap the frame to the ground actually mapped. Without this the
        # requested rectangle is wider than the projected sheet, and the margin
        # left over gets painted with the sea colour — inventing an ocean.
        self.x, self.y, self.w, self.h = self.ox, self.oy, mw, mh

    def _raw(self, lat, lon):
        rho = self.F / math.tan(math.pi / 4 + math.radians(lat) / 2) ** self.n
        th = self.n * (math.radians(lon) - self.lam0)
        return rho * math.sin(th), self.rho0 - rho * math.cos(th)

    def P(self, lat, lon):
        # SVG y grows downward, map y grows north — flip on the way out
        a, b = self._raw(lat, lon)
        return (self.ox + (a - self.rx0) * self.s, self.oy + (self.ry1 - b) * self.s)

    def km_per_px(self):
        la = (self.bbox[2] + self.bbox[3]) / 2
        x1, y1 = self.P(la, self.bbox[0]); x2, y2 = self.P(la, self.bbox[1])
        dkm = (self.bbox[1] - self.bbox[0]) * 111.32 * math.cos(math.radians(la))
        return dkm / max(1e-9, math.hypot(x2 - x1, y2 - y1))

    # ── layers ────────────────────────────────────────────────────
    def _path(self, seg, close=False, tol=None):
        # Decimate to the pixel: a 10m coastline inlined verbatim runs to tens of
        # megabytes and none of it is visible at this scale. Coordinates go out as
        # whole units — the plate is 860 units wide and is never displayed larger
        # than that, so a tenth of a unit is a tenth of a pixel nobody can see, and
        # it costs two characters on every point of every coastline.
        if tol is None:
            tol = self.pathtol
        d, lx, ly = [], None, None
        n = len(seg)
        for i, (lo, la) in enumerate(seg):
            px, py = self.P(la, lo)
            if i and i < n - 1 and lx is not None and abs(px - lx) < tol and abs(py - ly) < tol:
                continue
            d.append(('M' if not d else 'L') + '%.0f %.0f' % (px, py))
            lx, ly = px, py
        if close:
            d.append('Z')
        return ''.join(d)

    def base(self, s, res='10m', rivers=True, clipid=None):
        cid = clipid or ('clip%d' % id(self))
        s.append(f'<clipPath id="{cid}"><rect x="{self.x}" y="{self.y}" '
                 f'width="{self.w}" height="{self.h}"/></clipPath>')
        s.append(f'<g clip-path="url(#{cid})">')
        s.append(f'<rect x="{self.x}" y="{self.y}" width="{self.w}" height="{self.h}" fill="{SEA}"/>')
        for seg in _feats(res, 'physical', 'land', self.bbox):
            s.append(f'<path d="{self._path(seg, True)}" fill="{LAND}" stroke="none"/>')
        for seg in _feats(res, 'physical', 'lakes', self.bbox):
            s.append(f'<path d="{self._path(seg, True)}" fill="{SEA}" stroke="{SEALINE}" stroke-width=".7"/>')
        if rivers:
            for seg in _feats(res, 'physical', 'rivers_lake_centerlines', self.bbox, False):
                s.append(f'<path d="{self._path(seg)}" fill="none" stroke="{RIVER}" '
                         f'stroke-width="1.1" stroke-linejoin="round" opacity=".85"/>')
        for seg in _feats(res, 'physical', 'coastline', self.bbox, False):
            s.append(f'<path d="{self._path(seg)}" fill="none" stroke="{COAST}" stroke-width="1.1"/>')
        return cid

    def graticule(self, s, dlon, dlat, labels=True):
        lon0, lon1, lat0, lat1 = self.bbox
        lo = math.ceil(lon0 / dlon) * dlon
        while lo <= lon1:
            d = self._path([(lo, lat0 + i * (lat1 - lat0) / 24) for i in range(25)])
            s.append(f'<path d="{d}" fill="none" stroke="{GRAT}" stroke-width=".7"/>')
            if labels:
                px, _ = self.P(lat0, lo)
                s.append(txt(px, self.y + self.h - 5, f'{abs(lo):g}°E', 7.4, FOLIO, 'middle'))
            lo += dlon
        la = math.ceil(lat0 / dlat) * dlat
        while la <= lat1:
            d = self._path([(lon0 + i * (lon1 - lon0) / 24, la) for i in range(25)])
            s.append(f'<path d="{d}" fill="none" stroke="{GRAT}" stroke-width=".7"/>')
            if labels:
                px, py = self.P(la, lon0)
                s.append(txt(self.x + 4, py - 3, f'{abs(la):g}°N', 7.4, FOLIO, 'start'))
            la += dlat

    def close(self, s):
        s.append('</g>')
        s.append(f'<rect x="{self.x}" y="{self.y}" width="{self.w}" height="{self.h}" '
                 f'fill="none" stroke="{COAST}" stroke-width="1.2"/>')

    # ── furniture ─────────────────────────────────────────────────
    def scalebar(self, s, x=None, y=None, km=None):
        kpp = self.km_per_px()
        if km is None:
            raw = kpp * (self.w * 0.28)
            mag = 10 ** math.floor(math.log10(raw))
            km = min([m * mag for m in (1, 2, 5, 10)], key=lambda v: abs(v - raw))
        px = km / kpp
        x = self.x + 12 if x is None else x
        y = self.y + self.h - 20 if y is None else y
        s.append(f'<rect x="{x}" y="{y}" width="{px/2:.1f}" height="5" fill="{INK}"/>')
        s.append(f'<rect x="{x+px/2:.1f}" y="{y}" width="{px/2:.1f}" height="5" fill="#FFFFFF" stroke="{INK}" stroke-width=".8"/>')
        s.append(txt(x, y - 4, '0', 7.4, INK, 'middle'))
        s.append(txt(x + px, y - 4, f'{km:g} km', 7.4, INK, 'middle'))
        return km

    def north(self, s, x=None, y=None):
        x = self.x + self.w - 22 if x is None else x
        y = self.y + 24 if y is None else y
        s.append(f'<path d="M{x} {y-13} L{x+5} {y+5} L{x} {y+1} L{x-5} {y+5} Z" fill="{INK}"/>')
        s.append(txt(x, y + 16, 'N', 8.4, INK, 'middle', '700'))

    def sea(self, s, lat, lon, label, size=10, rot=0, anchor='middle'):
        px, py = self.P(lat, lon)
        tr = f' transform="rotate({rot} {px:.1f} {py:.1f})"' if rot else ''
        s.append(f'<text x="{px:.1f}" y="{py:.1f}" font-size="{size}" fill="#5E8296" '
                 f'text-anchor="{anchor}" font-style="italic" letter-spacing="1.6" '
                 f'font-family="Times New Roman, Times, serif"{tr}>{esc(label)}</text>')

    def region(self, s, lat, lon, label, size=10, fill='#B0A184', ls='2.2'):
        px, py = self.P(lat, lon)
        s.append(txt(px, py, esc(label), size, fill, 'middle', '700', 'normal', ls))


# ═══════════════════════ helpers for site marks ═══════════════════════
def dot(s, sh, lat, lon, col, r=5.5, ring='#FFFFFF'):
    x, y = sh.P(lat, lon)
    s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{col}" stroke="{ring}" stroke-width="1.7"/>')
    return x, y


def diamond(s, sh, lat, lon, col):
    x, y = sh.P(lat, lon)
    s.append(f'<rect x="{x-4.4:.1f}" y="{y-4.4:.1f}" width="8.8" height="8.8" fill="#FFFFFF" '
             f'stroke="{col}" stroke-width="2" transform="rotate(45 {x:.1f} {y:.1f})"/>')
    return x, y


def label(s, x, y, text, dx, dy, anchor='start', size=10.2, col=INK, weight='700', halo=True):
    tx, ty = x + dx, y + dy
    if halo:
        s.append(f'<text x="{tx:.1f}" y="{ty:.1f}" font-size="{size}" text-anchor="{anchor}" '
                 f'font-weight="{weight}" font-family="Times New Roman, Times, serif" '
                 f'stroke="#FFFAF0" stroke-width="3.2" stroke-linejoin="round" opacity=".92">{esc(text)}</text>')
    s.append(txt(tx, ty, esc(text), size, col, anchor, weight))


def route(s, sh, pts, col=RUST, w=2.6, dash='8 5'):
    d = ''.join(('M' if i == 0 else 'L') + '%.1f %.1f' % sh.P(la, lo)
                for i, (la, lo) in enumerate(pts))
    s.append(f'<path d="{d}" fill="none" stroke="#FFFAF0" stroke-width="{w+2.6}" opacity=".55" stroke-linejoin="round"/>')
    s.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-dasharray="{dash}" stroke-linejoin="round"/>')


def _plate(W, H, kicker, sub, aria):
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{aria}">']
    s.append(f'<rect width="{W}" height="{H}" fill="{SURF}"/>')
    s.append(txt(40, 32, kicker, 11, GOLD, 'start', '700', 'normal', '1.35'))
    s.append(txt(40, 50, sub, 10.4, GREY, 'start', '400', 'italic'))
    return s


def _legend(s, y, items, W=860):
    for i, (kind, col, lab) in enumerate(items):
        lx = 46 + i * (W - 92) / len(items)
        if kind == 'dot':
            s.append(f'<circle cx="{lx}" cy="{y}" r="5" fill="{col}"/>')
        elif kind == 'dia':
            s.append(f'<rect x="{lx-4}" y="{y-4}" width="8" height="8" fill="#FFFFFF" stroke="{col}" '
                     f'stroke-width="1.8" transform="rotate(45 {lx} {y})"/>')
        else:
            s.append(f'<line x1="{lx-7}" y1="{y}" x2="{lx+7}" y2="{y}" stroke="{col}" '
                     f'stroke-width="2.6" stroke-dasharray="6 4"/>')
        s.append(txt(lx + 13, y + 4, lab, 9.6, BODY))


# ═══════════════════════ 1 · the road out of Arabia ═══════════════════
def fig_road():
    W, H = 860, 620
    s = _plate(W, H, 'THE ROAD OUT OF ARABIA, AS THE FAMILY REMEMBERS IT',
               'Two sheets at two scales. The whole arc on the left; on the right, the Transjordanian leg where every station can be checked.',
               'Atlas map of the remembered migration route from Marib in Yemen to Ramallah')
    A = Sheet(*fit_box(33.0, 51.5, 12.0, 37.5, 350, 452), 44, 78, 350, 452)
    B = Sheet(*fit_box(34.85, 37.25, 30.00, 33.05, 392, 452), 424, 78, 392, 452)

    A.base(s, '50m', rivers=False, clipid='ca'); A.graticule(s, 5, 5); A.close(s)
    A.sea(s, 20.0, 38.6, 'RED SEA', 9.4, -62)
    A.sea(s, 13.6, 48.5, 'GULF OF ADEN', 8.6)
    A.sea(s, 27.0, 50.6, 'THE GULF', 8.6, -70)
    A.sea(s, 33.6, 33.4, 'MEDITERRANEAN', 8.6, -40)
    A.region(s, 22.5, 44.0, 'A R A B I A', 11.5)
    route(s, A, [(15.42, 45.33), (21.42, 39.83), (25.5, 37.6), (30.33, 35.60), (31.90, 35.20)])
    for la, lo, nm, k, dx, dy, an in [
            (15.42, 45.33, 'Maʾrib', 't', 9, 4, 'start'),
            (21.42, 39.83, 'the Ḥijāz', 't', 9, 4, 'start'),
            (30.33, 35.60, 'Udhruḥ', 't', -9, 10, 'end'),
            (31.90, 35.20, 'RAMALLAH', 'a', -9, -6, 'end')]:
        x, y = dot(s, A, la, lo, GREEN if k == 'a' else RUST, 5.5 if k == 'a' else 4.6)
        label(s, x, y, nm, dx, dy, an, 10 if k == 'a' else 9.4)
    for la, lo, nm in [(35.63, 38.75, 'Ruṣāfa'), (32.52, 36.48, 'Bosra')]:
        x, y = diamond(s, A, la, lo, PLUM)
        label(s, x, y, nm, 8, 3.5, 'start', 9, PLUM)
    A.scalebar(s); A.north(s)
    s.append(txt(A.x + 12, A.y - 8, 'A · THE WHOLE ARC', 8.8, GOLD, 'start', '700', 'normal', '1.2'))

    # the enlargement box, and the leaders to sheet B
    bl, bt = A.P(B.bbox[3], B.bbox[0]); br, bb = A.P(B.bbox[2], B.bbox[1])
    s.append(f'<rect x="{bl:.1f}" y="{bt:.1f}" width="{br-bl:.1f}" height="{bb-bt:.1f}" '
             f'fill="none" stroke="{GOLD}" stroke-width="1.6"/>')
    for ya, yb in ((bt, B.y), (bb, B.y + B.h)):
        s.append(f'<line x1="{br:.1f}" y1="{ya:.1f}" x2="{B.x}" y2="{yb}" stroke="{GOLD}" '
                 f'stroke-width=".9" stroke-dasharray="3 3" opacity=".75"/>')

    B.base(s, '10m', rivers=True, clipid='cb'); B.graticule(s, 1, 1); B.close(s)
    B.sea(s, 31.45, 35.47, 'DEAD SEA', 7.6, -74)
    B.sea(s, 32.55, 35.00, 'MEDITERRANEAN', 8, -52)
    B.region(s, 30.9, 36.72, 'THE PLATEAU', 9.6, '#B0A184', '2.2')
    route(s, B, [(30.33, 35.60), (30.53, 35.56), (31.18, 35.70), (31.68, 35.73),
                 (31.87, 35.53), (31.72, 35.19), (31.90, 35.20)])
    for la, lo, nm, k, dx, dy, an in [
            (30.33, 35.60, 'Udhruḥ', 't', 10, 12, 'start'),
            (30.53, 35.56, 'al-Shawbak', 't', -10, 0, 'end'),
            (31.18, 35.70, 'al-KARAK', 'a', 10, 4, 'start'),
            (31.68, 35.73, 'Maʿīn', 'a', 10, -4, 'start'),
            (31.87, 35.53, 'the ford of al-Lisān', 't', 8, -8, 'start'),
            (31.72, 35.19, 'Bayt Jālā', 'a', -10, 13, 'end'),
            (31.90, 35.20, 'RAMALLAH', 'a', -10, -5, 'end')]:
        x, y = dot(s, B, la, lo, GREEN if k == 'a' else RUST)
        label(s, x, y, nm, dx, dy, an, 10.4 if nm.isupper() else 10)
    x, y = diamond(s, B, 31.66, 35.83, PLUM)
    label(s, x, y, 'Nitl', 11, 12, 'start', 9.4, PLUM)
    x, y = diamond(s, B, 32.52, 36.48, PLUM)
    label(s, x, y, 'Bosra / the Ḥawrān', 9, 4, 'start', 9.4, PLUM)
    B.scalebar(s); B.north(s)
    s.append(txt(B.x + 12, B.y - 8, 'B · THE LEG THAT CAN BE CHECKED', 8.8, GOLD, 'start', '700', 'normal', '1.2'))

    _legend(s, H - 74, [('dot', RUST, 'remembered station — tradition only'),
                        ('dot', GREEN, 'attested in a document'),
                        ('dia', PLUM, 'Ghassanid site with standing evidence')])
    s.append(f'<line x1="40" y1="{H-56}" x2="{W-40}" y2="{H-56}" stroke="{RULE}"/>')
    s.append(txt(40, H - 36, 'Nitl lies a few kilometres from Maʿīn — the mosaics there are the most important Jafnid-associated monument in Jordan, and they sit on the road the family remembers.', 10.2, BODY, 'start', '700'))
    s.append(txt(40, H - 20, 'Sheet A is drawn at roughly one-eighth the scale of sheet B. Coastlines, rivers and lakes after Natural Earth; Lambert conformal conic projection.', 9.8, GREY, 'start', '400', 'italic'))
    s.append('</svg>')
    return ''.join(s)


class Flat:
    """Equirectangular with a cosine correction — for world sheets, where a
    conic would fold. Same interface as Sheet."""
    def __init__(self, lon0, lon1, lat0, lat1, x, y, w, h):
        self.bbox = (lon0, lon1, lat0, lat1)
        # a continent at 772px: two units of slack on the coast is invisible
        self.pathtol = 2.4
        self.x, self.y, self.w, self.h = x, y, w, h
        self.k = math.cos(math.radians((lat0 + lat1) / 2))
        self.sx = w / ((lon1 - lon0) * self.k)
        self.sy = h / (lat1 - lat0)
        self.s = min(self.sx, self.sy)
        self.ox = x + (w - (lon1 - lon0) * self.k * self.s) / 2
        self.oy = y + (h - (lat1 - lat0) * self.s) / 2

    def P(self, lat, lon):
        lon0, lon1, lat0, lat1 = self.bbox
        return (self.ox + (lon - lon0) * self.k * self.s,
                self.oy + (lat1 - lat) * self.s)

    km_per_px = Sheet.km_per_px
    _path = Sheet._path
    base = Sheet.base
    graticule = Sheet.graticule
    close = Sheet.close
    scalebar = Sheet.scalebar
    north = Sheet.north
    sea = Sheet.sea
    region = Sheet.region


# ═══════════════════════ 2 · the Roman district ═══════════════════════
def fig_roman():
    W, H = 860, 540
    s = _plate(W, H, 'THE DISTRICT WHEN ROME WROTE IT DOWN',
               'Every green dot is a place named in a surviving classical text. The gold ring is the site of Ramallah — named in none of them, and in nothing at all until 1279.',
               'Atlas map of the Roman and Byzantine district around Ramallah')
    M = Sheet(*fit_box(34.88, 35.62, 31.62, 32.18, 772, 372), 44, 78, 772, 372)
    M.base(s, '10m'); M.graticule(s, 0.25, 0.25); M.close(s)
    M.sea(s, 31.70, 35.50, 'DEAD SEA', 7.6, -80)
    # the imperial road, Aelia to Neapolis
    route(s, M, [(31.70, 35.22), (31.78, 35.225), (31.91, 35.222), (31.96, 35.222),
                 (32.10, 35.24), (32.22, 35.26)], col='#9A7A45', w=5.0, dash='none')
    rx, ry = M.P(32.11, 35.245)
    label(s, rx, ry, 'the road to Neapolis', 10, 0, 'start', 9, '#8A6A3A', '400')
    for la, lo, nm, dx, dy, an in [
            (31.9603, 35.2158, 'Gophna / Jifnā', 10, -5, 'start'),
            (31.9280, 35.2200, 'Bethel / Beitin', 10, 12, 'start'),
            (32.0300, 35.0700, 'ʿAbūd', -10, 4, 'end'),
            (31.9500, 35.3100, 'Ephraim / Ṭaybeh', 10, 4, 'start'),
            (31.8930, 35.1800, 'Khirbet et-Tireh', -10, 14, 'end'),
            (31.7780, 35.2354, 'AELIA CAPITOLINA', 10, 12, 'start'),
            (31.7050, 35.2030, 'Bethlehem', 10, 4, 'start')]:
        x, y = dot(s, M, la, lo, GREEN, 5.2)
        label(s, x, y, nm, dx, dy, an, 10 if nm.isupper() else 9.8)
    x, y = M.P(31.9038, 35.2034)
    s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="none" stroke="{GOLD}" stroke-width="2.4"/>')
    s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="{GOLD}"/>')
    label(s, x, y, 'the site of RAMALLAH', -13, -8, 'end', 10.4, '#8A6A3A')
    label(s, x, y, 'named in no classical text', -13, 5, 'end', 8.8, GREY, '400')
    M.scalebar(s); M.north(s)
    _legend(s, H - 62, [('dot', GREEN, 'named in a surviving classical text'),
                        ('line', '#9A7A45', 'the milestoned imperial road'),
                        ('dot', GOLD, 'the site of Ramallah')])
    s.append(f'<line x1="40" y1="{H-44}" x2="{W-40}" y2="{H-44}" stroke="{RULE}"/>')
    s.append(txt(40, H - 24, 'When the family walks up this ridge in 1562, and when the first emigrants ride down it in 1901, they are using a road Rome paved.', 10.2, BODY, 'start', '700'))
    s.append(txt(40, H - 10, 'Coastlines and drainage after Natural Earth; Lambert conformal conic. Sites after Pliny, Josephus, Eusebius and the Madaba mosaic.', 9.6, GREY, 'start', '400', 'italic'))
    s.append('</svg>')
    return ''.join(s)


# ═══════════════════════ 3 · the hills around Ramallah ════════════════
def fig_district():
    W, H = 860, 560
    s = _plate(W, H, 'THE HILLS AROUND RAMALLAH — WHAT HAS BEEN DUG, WHAT WAS WRITTEN, WHO RULED',
               'Everything within a few kilometres of the town, on one sheet: the excavated sites, the Frankish settlement, the throne villages, and the watershed road all of it hangs off.',
               'Atlas map of the villages and excavated sites around Ramallah')
    M = Sheet(*fit_box(34.98, 35.42, 31.66, 32.08, 772, 392), 44, 78, 772, 392)
    M.base(s, '10m'); M.graticule(s, 0.1, 0.1); M.close(s)
    route(s, M, [(31.66, 35.20), (31.78, 35.222), (31.91, 35.222), (31.97, 35.222), (32.08, 35.24)],
          col='#9A7A45', w=5.0, dash='none')
    rx, ry = M.P(32.045, 35.235)
    label(s, rx, ry, 'the watershed ridge road', 9, 0, 'start', 9, '#8A6A3A', '400')
    SITES = [(31.9038, 35.2034, 'RAMALLAH', 'town', -11, -6, 'end'),
             (31.9100, 35.2200, 'al-Bīra', 'frank', 11, -4, 'start'),
             (31.8930, 35.1800, 'Khirbet et-Tireh', 'dig', -11, 12, 'end'),
             (31.9603, 35.2158, 'Jifnā', 'insc', 11, -4, 'start'),
             (32.0300, 35.0700, 'ʿAbūd', 'dig', 11, 4, 'start'),
             (31.7200, 35.1900, 'Bayt Jālā', 'town', 11, 4, 'start'),
             (31.9250, 35.2620, 'et-Tell (Ai)', 'set', 11, 4, 'start'),
             (32.0200, 35.0800, 'Dayr Ghassāna', 'throne', -11, 14, 'end'),
             (31.9300, 35.1100, 'Rās Karkar', 'throne', -11, 4, 'end'),
             (31.9720, 35.1900, 'Bīr Zayt', 'vill', -11, 4, 'end'),
             (31.9500, 35.3100, 'Ṭayyibat al-Ism', 'vill', 11, 4, 'start')]
    STY = {'town': (GREEN, 6.4), 'dig': (GREEN, 5.2), 'frank': (PLUM, 5.2), 'insc': (PLUM, 4.8),
           'throne': (RUST, 4.8), 'set': (FOLIO, 4.4), 'vill': (FOLIO, 4.2)}
    dx0, dy0 = M.P(31.9038, 35.2034)
    s.append(f'<circle cx="{dx0:.1f}" cy="{dy0:.1f}" r="{2/ M.km_per_px():.1f}" fill="none" '
             f'stroke="{GREEN}" stroke-width="1" stroke-dasharray="4 3" opacity=".7"/>')
    for la, lo, nm, k, dx, dy, an in SITES:
        col, r = STY[k]
        x, y = dot(s, M, la, lo, col, r)
        label(s, x, y, nm, dx, dy, an, 10.4 if k == 'town' else 9.8)
    M.scalebar(s); M.north(s)
    _legend(s, H - 62, [('dot', GREEN, 'excavated, or the town itself'),
                        ('dia', PLUM, 'named in a medieval document'),
                        ('dot', RUST, 'throne village — a shaykhly seat')])
    s.append(f'<line x1="40" y1="{H-44}" x2="{W-40}" y2="{H-44}" stroke="{RULE}"/>')
    s.append(txt(40, H - 24, 'Ramallah is the one dot with nothing under it before 1562 — which is exactly what a hill of endowment land should look like. The dashed ring is two kilometres.', 10.2, BODY, 'start', '700'))
    s.append(txt(40, H - 10, 'Coastlines and drainage after Natural Earth; Lambert conformal conic.', 9.6, GREY, 'start', '400', 'italic'))
    s.append('</svg>')
    return ''.join(s)


# ═══════════════════════ 4 · the oldest ground ════════════════════════
def fig_oldest():
    W, H = 860, 560
    s = _plate(W, H, 'THE OLDEST GROUND WITHIN A MORNING’S WALK OF RAMALLAH',
               'Every dot is a site with a published excavation and a calibrated date. Distances are measured from the centre of Ramallah.',
               'Atlas map of the earliest excavated sites around Ramallah')
    M = Sheet(*fit_box(34.94, 35.52, 31.70, 32.08, 772, 384), 44, 78, 772, 384)
    M.base(s, '10m'); M.graticule(s, 0.2, 0.2); M.close(s)
    M.sea(s, 31.80, 35.48, 'DEAD SEA', 7.6, -80)
    KIND = {'pal': (PLUM, 'Palaeolithic & Natufian'), 'neo': (GREEN, 'Neolithic'),
            'chal': (RUST, 'Chalcolithic'), 'eb': (GOLD, 'Bronze Age')}
    SITES = [(31.9819, 35.0436, 'SHUQBA CAVE', 'pal', 19.3, 10, -6, 'start'),
             (31.8711, 35.4442, 'TELL es-SULTAN — Jericho', 'neo', 23.0, -11, -6, 'end'),
             (31.8869, 35.2164, 'TELL en-NAṢBA', 'chal', 2.5, -11, 17, 'end'),
             (31.9169, 35.2569, 'et-TELL (Ai)', 'eb', 5.3, 11, -6, 'start'),
             (31.9700, 35.3200, 'ʿAIN SAMIYA', 'eb', 13.8, 11, 4, 'start'),
             (31.7933, 35.1533, 'MOTZA', 'neo', 12.5, 11, 4, 'start'),
             (31.8058, 35.1044, 'ABU GHOSH', 'neo', 13.9, -11, 4, 'end')]
    rx, ry = M.P(31.9038, 35.2034)
    for la, lo, nm, k, km, dx, dy, an in SITES:
        col = KIND[k][0]
        x, y = M.P(la, lo)
        s.append(f'<line x1="{rx:.1f}" y1="{ry:.1f}" x2="{x:.1f}" y2="{y:.1f}" stroke="{col}" '
                 f'stroke-width=".9" stroke-dasharray="3 3" opacity=".5"/>')
        dot(s, M, la, lo, col, 5.8)
        label(s, x, y, nm, dx, dy, an, 9.8)
        label(s, x, y, f'{km} km', dx, dy + 11, an, 8.4, GREY, '400')
    s.append(f'<circle cx="{rx:.1f}" cy="{ry:.1f}" r="8" fill="none" stroke="{INK}" stroke-width="2.2"/>')
    s.append(f'<circle cx="{rx:.1f}" cy="{ry:.1f}" r="2.6" fill="{INK}"/>')
    label(s, rx, ry, 'RAMALLAH', -12, 4, 'end', 11, INK)
    M.scalebar(s); M.north(s)
    _legend(s, H - 68, [('dot', c, l) for c, l in KIND.values()])
    s.append(f'<line x1="40" y1="{H-50}" x2="{W-40}" y2="{H-50}" stroke="{RULE}"/>')
    s.append(txt(40, H - 30, 'The Natufian — the first culture anywhere to build regularly in stone and hold a base camp through the year — is named after a wadi in this governorate.', 10.2, BODY, 'start', '700'))
    s.append(txt(40, H - 14, 'These highlands are thinly excavated compared with the coast and the Jordan valley: the blank spaces are gaps in the survey record, not gaps in the past.', 9.8, GREY, 'start', '400', 'italic'))
    s.append('</svg>')
    return ''.join(s)


# ═══════════════════════ 5 · the Ḥaddādīn of Jordan ═══════════════════
def fig_haddadin():
    W, H = 860, 600
    s = _plate(W, H, 'THE ḤADDĀDĪN IN JORDAN, AS PEAKE’S CLAN REGISTER HAS THEM',
               'Not one family in one town — an old lineage scattered the length of the country, with relatives across the river at Nazareth.',
               'Atlas map of Haddadin communities recorded in Jordan')
    M = Sheet(*fit_box(34.90, 36.75, 30.20, 32.90, 300, 430), 44, 78, 300, 430)
    M.base(s, '10m'); M.graticule(s, 0.5, 0.5); M.close(s)
    M.sea(s, 31.45, 35.47, 'DEAD SEA', 7.8, -78)
    M.sea(s, 32.55, 35.05, 'MEDITERRANEAN', 8, -52)
    PL = [(32.49, 35.87, 'al-Ḥuṣn', 10, -4, 'start'), (32.53, 35.86, 'Aydūn', 10, 10, 'start'),
          (32.40, 35.72, 'Kufr ʿAwān', -10, 4, 'end'), (32.04, 35.73, 'al-Salṭ', 10, 4, 'start'),
          (31.72, 35.79, 'Madaba', 10, -4, 'start'), (31.68, 35.73, 'Maʿīn', 10, 10, 'start'),
          (30.53, 35.56, 'al-Shawbak', 10, 4, 'start'), (30.33, 35.60, 'Udhruḥ', 10, 4, 'start')]
    BIG = [(31.18, 35.70, 'al-KARAK', 10, -4, 'start'), (31.13, 35.73, 'Ḥamūd', 10, 12, 'start')]
    for la, lo, nm, dx, dy, an in PL:
        x, y = dot(s, M, la, lo, RUST, 4.8)
        label(s, x, y, nm, dx, dy, an, 9.8, INK, '400')
    for la, lo, nm, dx, dy, an in BIG:
        x, y = dot(s, M, la, lo, GREEN, 6.4)
        label(s, x, y, nm, dx, dy, an, 10.4)
    for la, lo, nm in [(31.9038, 35.2034, 'Ramallah'), (32.70, 35.30, 'Nazareth')]:
        x, y = M.P(la, lo)
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.6" fill="none" stroke="{GREY}" stroke-width="1.7"/>')
        label(s, x, y, nm, -9, 4, 'end', 9.6, GREY, '400')
    M.scalebar(s); M.north(s)
    bx = M.x + M.w + 34
    s.append(txt(bx, 96, 'WHERE THE REGISTERS PUT THEM', 9, GOLD, 'start', '700', 'normal', '1.2'))
    yy = 120
    for head, lines, col in [
        ('AL-KARAK AND ḤAMŪD', ['The Karak clan register is explicit:',
                                '“they dwell in al-Karak and the village',
                                'of Ḥamūd.” This is the concentration',
                                'the family’s tradition comes out of.'], GREEN),
        ('NORTH — ʿAJLŪN', ['A Ḥaddādīn ḥamūla at al-Ḥuṣn, Aydūn',
                            'and Kufr ʿAwān, a hundred kilometres',
                            'north of Karak.'], RUST),
        ('CENTRE — AL-BALQĀʾ', ['At al-Salṭ, and at Maʿīn and Madaba',
                                'on the plateau beside Nitl.'], RUST),
        ('SOUTH — THE PLATEAU', ['al-Shawbak and Udhruḥ, the southern',
                                 'end of the Christian plateau, where',
                                 'al-Yaʿqūbī located Ghassān in 890.'], RUST),
        ('AND ACROSS THE RIVER', ['Relatives at Nazareth, called',
                                  'al-Hanādisa — and the emigrant',
                                  'fragment at Ramallah that this',
                                  'book is about.'], GREY)]:
        s.append(f'<rect x="{bx}" y="{yy-11}" width="4" height="{13+len(lines)*13}" fill="{col}" rx="2"/>')
        s.append(txt(bx + 13, yy, head, 9, col, 'start', '700', 'normal', '1.1'))
        for i, ln in enumerate(lines):
            s.append(txt(bx + 13, yy + 15 + i * 13, ln, 9.4, BODY))
        yy += 34 + len(lines) * 13
    _legend(s, H - 68, [('dot', GREEN, 'named in the Karak clan register'),
                        ('dot', RUST, 'a Ḥaddādīn ḥamūla also recorded here')])
    s.append(f'<line x1="40" y1="{H-50}" x2="{W-40}" y2="{H-50}" stroke="{RULE}"/>')
    s.append(txt(40, H - 30, 'The clan the family descends from is documented on the other side of the Jordan, in a register kept by another state.', 10.2, BODY, 'start', '700'))
    s.append(txt(40, H - 14, 'After F. G. Peake, History and Tribes of Trans-Jordan, vol. II. Coastlines and drainage after Natural Earth.', 9.8, GREY, 'start', '400', 'italic'))
    s.append('</svg>')
    return ''.join(s)


# ═══════════════════════ 6 · the diaspora ═════════════════════════════
def fig_diaspora():
    W, H = 860, 500
    s = _plate(W, H, 'WHERE RAMALLAH WENT, 1901 ONWARD',
               'The cities the town’s people went to, weighted by the family’s own record. Nobody has ever properly enumerated this diaspora, which is itself a finding.',
               'Atlas map of the Ramallah diaspora in North America')
    M = Flat(-126.0, 38.0, 22.0, 54.0, 44, 74, 772, 306)
    M.base(s, '50m', rivers=False, clipid='cd'); M.graticule(s, 20, 10, labels=False); M.close(s)
    M.sea(s, 40.0, -45.0, 'ATLANTIC OCEAN', 9.4)
    M.sea(s, 34.0, -125.0, 'PACIFIC', 8.6, -90, 'middle')
    CITIES = [(42.33, -83.05, 'DETROIT', 34, 10, -5, 'start'),
              (30.33, -81.66, 'Jacksonville', 18, 10, 4, 'start'),
              (40.71, -74.01, 'New York', 16, 10, -6, 'start'),
              (37.77, -122.42, 'San Francisco', 12, 10, 4, 'start'),
              (41.88, -87.63, 'Chicago', 10, -10, 10, 'end'),
              (34.05, -118.24, 'Los Angeles', 9, 10, 8, 'start'),
              (35.15, -90.05, 'Memphis', 8, 10, 8, 'start'),
              (29.76, -95.37, 'Houston', 8, 10, 4, 'start'),
              (44.98, -93.27, 'Minneapolis', 7, -10, -4, 'end')]
    hx, hy = M.P(31.9038, 35.2034)
    for la, lo, nm, wgt, dx, dy, an in CITIES:
        x, y = M.P(la, lo)
        cx, cy = (hx + x) / 2, min(hy, y) - 70
        s.append(f'<path d="M{hx:.1f} {hy:.1f} Q {cx:.1f} {cy:.1f} {x:.1f} {y:.1f}" fill="none" '
                 f'stroke="{RUST}" stroke-width="{0.7 + wgt/18:.1f}" opacity=".55"/>')
    for la, lo, nm, wgt, dx, dy, an in CITIES:
        x, y = dot(s, M, la, lo, GREEN, 3.4 + wgt / 12)
        label(s, x, y, nm, dx, dy, an, 10 if nm.isupper() else 9.4)
    s.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="7" fill="{GOLD}" stroke="#FFFFFF" stroke-width="2"/>')
    label(s, hx, hy, 'RAMALLAH', -11, 4, 'end', 10.6, '#8A6A3A')
    M.scalebar(s); M.north(s)
    s.append(f'<line x1="40" y1="{H-72}" x2="{W-40}" y2="{H-72}" stroke="{RULE}"/>')
    s.append(txt(40, H - 52, 'Circle size and line weight follow the family’s own record of where people went, not a census — no census of this diaspora has ever been taken.', 10.2, BODY, 'start', '700'))
    s.append(txt(40, H - 36, 'The first four men sail in 1901. By 1946 Shāhīn counts 1,500 in the United States; by 1960 more than 4,000; by 1975 more than 10,000.', 10.2, BODY, 'start', '400'))
    s.append(txt(40, H - 18, 'Equirectangular projection with a mid-latitude correction; coastlines after Natural Earth. Great-circle arcs are drawn schematically.', 9.6, GREY, 'start', '400', 'italic'))
    s.append('</svg>')
    return ''.join(s)


# ═══════════════════════ 7 · the road the family walked ═══════════════
def fig_karak():
    W, H = 860, 600
    s = _plate(W, H, 'THE ROAD THE FAMILY ACTUALLY WALKED — KARAK TO THE RIDGE',
               'Three moves, and the evidence for each. The southern anchors are the plateau’s Christian record; the northern legs are carried by the Ottoman registers.',
               'Atlas map of the route from Karak to Ramallah in three documented legs')
    # Three panels. The geography is portrait — two degrees of latitude against
    # one and a half of longitude — so sheet A is drawn portrait and the width
    # saved goes to sheet B, where the last two legs have room to be read.
    M = Sheet(*fit_box(34.85, 36.30, 30.20, 32.20, 268, 430), 44, 78, 268, 430)
    M.base(s, '10m', clipid='ck1'); M.graticule(s, 0.5, 0.5); M.close(s)
    M.sea(s, 31.24, 35.49, 'DEAD SEA', 7.4, -78)
    s.append(txt(M.x + 10, M.y - 8, 'A · THE WHOLE ROUTE', 8.4, GOLD, 'start', '700', 'normal', '1.1'))

    legs = [([(31.18, 35.70), (31.55, 35.35), (31.60, 35.10)], RUST, '1'),
            ([(31.60, 35.10), (31.72, 35.19)], GREEN, '2'),
            ([(31.72, 35.19), (31.9038, 35.2034)], GREEN, '3')]

    def _badge(sheet, pts, col, n, r=9.6, fs=10.6, off=16):
        # Numeral at the arc midpoint, pushed east of the line. A leg with only
        # two points has no middle vertex, and a badge left sitting on the line
        # lands on a station's own dot — which is exactly how these numerals
        # became unreadable in the first place.
        pp = [sheet.P(a, b) for a, b in pts]
        seg = [((pp[i+1][0]-pp[i][0])**2 + (pp[i+1][1]-pp[i][1])**2) ** .5 for i in range(len(pp)-1)]
        half = sum(seg) / 2
        for i, L in enumerate(seg):
            if half <= L or i == len(seg) - 1:
                f = half / L if L else 0
                ax, ay = pp[i]; bx2, by2 = pp[i+1]
                mx, my = ax + (bx2-ax)*f, ay + (by2-ay)*f
                nx, ny = -(by2-ay)/(L or 1), (bx2-ax)/(L or 1)
                if nx < 0: nx, ny = -nx, -ny
                return (mx + nx*off, my + ny*off, n, col, r, fs)
            half -= L

    badges = [_badge(M, pts, col, n) for pts, col, n in legs]
    for pts, col, n in legs:
        route(s, M, pts, col=col, w=2.6)
    for la, lo, nm, k, dx, dy, an in [
            (30.53, 35.56, 'al-Shawbak', 't', 9, 4, 'start'),
            (31.18, 35.70, 'al-KARAK', 'a', 9, 4, 'start'),
            (31.60, 35.10, 'Kusbār', 'a', -9, -5, 'end'),
            (31.72, 35.19, 'Bayt Jālā', 'a', -9, -5, 'end'),
            (31.9038, 35.2034, 'RAMALLAH', 'a', -9, -5, 'end'),
            (30.33, 35.60, 'Gharandal', 't', 9, 4, 'start')]:
        x, y = dot(s, M, la, lo, GREEN if k == 'a' else RUST, 5.6 if nm.isupper() else 4.6)
        label(s, x, y, nm, dx, dy, an, 9.8 if nm.isupper() else 9.2)
    M.scalebar(s); M.north(s)

    # ── B · the enlargement
    N = Sheet(*fit_box(34.98, 35.40, 31.52, 31.99, 250, 430), 326, 78, 250, 430)
    N.base(s, '10m', clipid='ck2'); N.graticule(s, 0.2, 0.2); N.close(s)
    s.append(txt(N.x + 10, N.y - 8, 'B · THE LAST TWO LEGS, ENLARGED', 8.4, GOLD, 'start', '700', 'normal', '1.1'))
    for pts, col, n in legs[1:]:
        route(s, N, pts, col=col, w=3.2)
    for la, lo, nm, dx, dy, an in [(31.9038, 35.2034, 'RAMALLAH', 10, -5, 'start'),
                                   (31.72, 35.19, 'Bayt Jālā', 10, 4, 'start'),
                                   (31.60, 35.10, 'Kusbār, by Ḥalḥūl', 10, 4, 'start')]:
        x, y = dot(s, N, la, lo, GREEN, 6.2 if nm.isupper() else 5.2)
        label(s, x, y, nm, dx, dy, an, 10.4 if nm.isupper() else 9.8)
    badges += [_badge(N, pts, col, n, 11, 12, 19) for pts, col, n in legs[1:]]
    N.scalebar(s)

    # the key box on sheet A, and the leaders to sheet B
    kl, kt = M.P(N.bbox[3], N.bbox[0]); kr, kb = M.P(N.bbox[2], N.bbox[1])
    s.append(f'<rect x="{kl:.1f}" y="{kt:.1f}" width="{kr-kl:.1f}" height="{kb-kt:.1f}" '
             f'fill="none" stroke="{GOLD}" stroke-width="1.4"/>')
    s.append(f'<rect x="{kr-13:.1f}" y="{kt:.1f}" width="13" height="12" fill="{GOLD}"/>')
    s.append(txt(kr - 6.5, kt + 9, 'B', 8.6, '#FFFAF0', 'middle', '700'))

    # badges last, so nothing on either sheet can paint over a numeral
    for mx, my, n, col, r, fs in badges:
        s.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="{r+2.6:.1f}" fill="#FFFAF0" opacity=".95"/>')
        s.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="{r:.1f}" fill="#FFFAF0" stroke="{col}" stroke-width="2.1"/>')
        s.append(txt(mx, my + fs * .35, n, fs, col, 'middle', '700'))

    # ── C · the evidence for each leg
    bx = 596
    s.append(f'<rect x="{bx}" y="78" width="220" height="430" fill="#FFFFFF" stroke="{RULE}" rx="4"/>')
    yy = 104
    for n, ttl, lines, col in [
        ('1', 'KARAK → KUSBĀR', ['Tradition, plus the plateau’s',
                                 'documented Christian',
                                 'demography: Ghassān located at',
                                 'Gharandal in 890; the pilgrim',
                                 'Thietmar in Shawbak’s suburb,',
                                 '1217–18; a Christian majority at',
                                 'Shawbak in 1321; 103 Christian',
                                 'households and 8 bachelors at',
                                 'Karak in the register of 1596.'], RUST),
        ('2', 'KUSBĀR → BAYT JĀLĀ', ['The Ottoman register of',
                                     '1553–54 finds the group at',
                                     'Bayt Jālā — the 36 Christian',
                                     'households the register calls',
                                     'the Kasābra. They are not yet',
                                     'at Ramallah.'], GREEN),
        ('3', 'BAYT JĀLĀ → RAMALLAH', ['1562: the 36 Kasābra families',
                                       'come up the ridge road, with',
                                       '27 further Christian families',
                                       'and 8 unmarried men — some',
                                       '63 Christian households,',
                                       'joining the 10 Muslim families',
                                       'already on the hill.'], GREEN)]:
        s.append(f'<circle cx="{bx+22}" cy="{yy-4}" r="9" fill="#FFFAF0" stroke="{col}" stroke-width="2"/>')
        s.append(txt(bx + 22, yy - 0.5, n, 10, col, 'middle', '700'))
        s.append(txt(bx + 40, yy, ttl, 8.8, col, 'start', '700', 'normal', '1'))
        for i, ln in enumerate(lines):
            s.append(txt(bx + 40, yy + 15 + i * 12.5, ln, 9.2, BODY))
        yy += 34 + len(lines) * 12.5
    s.append(f'<line x1="40" y1="{H-56}" x2="{W-40}" y2="{H-56}" stroke="{RULE}"/>')
    s.append(txt(40, H - 36, 'Two memories and a tax ledger, telling one story in three voices — and every stage from Karak onward can be checked against a register kept by somebody else.', 10.2, BODY, 'start', '700'))
    s.append(txt(40, H - 18, 'Ḥammūdeh, Jerusalem Quarterly 59 (2014); Hütteroth and Abdulfattah (1977); Piccirillo (2001); al-Yaʿqūbī. Coastlines after Natural Earth.', 9.6, GREY, 'start', '400', 'italic'))
    s.append('</svg>')
    return ''.join(s)
