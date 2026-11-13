# -*- coding: utf-8 -*-
"""v76: the book's one map style (docs/MAP_STYLE.md), as code.

Every drawn map in the book takes its colours, symbol sizes, type sizes and
furniture from here, so a green dot means the same thing on every page.

Terrain
-------
`terrain(...)` lays a soft hillshade over hypsometric tints, with contours and
a wadi network derived from the elevation model. The elevation comes from the
public AWS Terrarium tiles (SRTM / ETOPO / Copernicus composite). Fetching is
done once; what the book needs — a small JPEG and simplified vector paths — is
stored in data/terrain/<key>.json, so the build stays deterministic and needs
no network once those files exist. Delete a file to regenerate it.

The raster sits under every mark: tints are muted so that symbols and labels
always read first.
"""
import base64
import hashlib
import io
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TERRAIN_DIR = os.path.join(os.path.dirname(HERE), 'data', 'terrain')
TILE_CACHE = os.environ.get('AFRP_DEM_CACHE', os.path.expanduser('~/.cache/afrp-dem'))
VERSION = 'v76.3'

# ─────────────────────────────── palette
# Colours here are chosen to be outside src/restyle.py's map, so the restyle
# pass leaves the map style alone.
INK, BODY, NOTE = '#1A1915', '#3D3A35', '#6B6760'
FRAME, TICK = '#8A7E6A', '#8F8A80'
DOC = '#007A3D'          # documented
DOC_DEEP = '#004A26'
MEM = '#9A6324'          # remembered: tradition only
MEM_LIGHT = '#C49A5E'
CONTEXT = '#8F8A80'      # context, named for orientation only
MONUMENT = '#3D3A35'     # monument or standing evidence (open diamond)
RAMALLAH = '#B3261E'     # the one place on every map
# thematic ramp for maps whose subject is a category, not evidence (periods)
ERA = ['#2E2A4A', '#5A4E8C', '#8676B8', '#B0A3D6']
# water: one blue family
SEA = '#D5E5EC'
LAKE = '#C6DCE6'
WATER_LINE = '#6E9BB3'
RIVER = '#4F86A6'
WADI = '#7DA7BE'
WATER_TEXT = '#3B6A86'
SPRING = '#2F78A3'
# land, under the hillshade
HYPSO = [  # elevation m -> RGB, muted
    (-450, (226, 232, 220)),
    (-200, (233, 236, 224)),
    (0, (243, 241, 233)),
    (300, (242, 236, 222)),
    (600, (237, 227, 205)),
    (900, (229, 214, 184)),
    (1200, (221, 203, 168)),
    (2000, (210, 190, 152)),
    (3000, (200, 182, 150)),
]
CONTOUR = '#B09A74'
CONTOUR_INDEX = '#8C7550'

# ─────────────────────────────── type
FONT = 'Times New Roman, Times, serif'
# The plate is 860 units wide and is shown at 720 px on a phone, so 13 units is
# 11 px on the smallest screen the book is read on.
T_TOWN = 13.5        # bold roman, towns and the map's subject places
T_VILLAGE = 13.0     # regular roman
T_REGION = 13.0      # spaced small caps
T_WATER = 13.0       # italic blue
T_NOTE = 11.5        # grey italic notes beside a label (distances, dates)
T_FURN = 11.0        # scale bar, graticule, legend
T_PANEL = 13.0       # panel and sheet headings


def esc(t):
    return (str(t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def text(x, y, t, size, col, anchor='start', weight='400', style='normal', ls='0', halo=False, raw=False):
    body = t if raw else esc(t)
    common = (f'x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" '
              f'font-weight="{weight}" font-style="{style}" letter-spacing="{ls}" font-family="{FONT}"')
    out = ''
    if halo:
        out += (f'<text {common} fill="none" stroke="#FFFFFF" stroke-width="3.4" '
                f'stroke-linejoin="round" opacity=".9">{body}</text>')
    return out + f'<text {common} fill="{col}">{body}</text>'


# ─────────────────────────────── symbols
def sym_documented(s, x, y, r=5.6, uncertain=False):
    if uncertain:
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="#FFFFFF" stroke="{DOC}" '
                 f'stroke-width="2.2" stroke-dasharray="2.6 1.8"/>')
    else:
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{DOC}" stroke="#FFFFFF" stroke-width="1.8"/>')


def sym_remembered(s, x, y, r=5.2, uncertain=False):
    if uncertain:
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="#FFFFFF" stroke="{MEM}" '
                 f'stroke-width="2.2" stroke-dasharray="2.6 1.8"/>')
    else:
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{MEM}" stroke="#FFFFFF" stroke-width="1.8"/>')


def sym_context(s, x, y, r=4.4):
    s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{CONTEXT}" stroke="#FFFFFF" stroke-width="1.5"/>')


def sym_monument(s, x, y, col=MONUMENT, r=5.0):
    s.append(f'<rect x="{x-r:.1f}" y="{y-r:.1f}" width="{2*r:.1f}" height="{2*r:.1f}" fill="#FFFFFF" '
             f'stroke="{col}" stroke-width="2" transform="rotate(45 {x:.1f} {y:.1f})"/>')


def sym_ramallah(s, x, y, empty=False):
    """The ringed dot. Drawn on every map so the reader can always find home.
    `empty` draws the ring with no centre: the site, before the town."""
    s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8.6" fill="#FFFFFF" fill-opacity=".85" '
             f'stroke="{RAMALLAH}" stroke-width="2.4"/>')
    if not empty:
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.4" fill="{RAMALLAH}"/>')


def sym_spring(s, x, y):
    s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" fill="{SPRING}" stroke="#FFFFFF" stroke-width="1.2"/>')


def legend(s, y, items, x0=40, x1=820, rows=None):
    """items: (kind, label[, col]). kind: doc, doc?, mem, mem?, ctx, mon,
    ram, ram0, spring, road, route-doc, route-mem, route-approx, ramp:<col>."""
    n = len(items)
    per = n if not rows else math.ceil(n / rows)
    col_w = (x1 - x0) / per
    for i, it in enumerate(items):
        kind, lab = it[0], it[1]
        c = it[2] if len(it) > 2 else None
        r, k = divmod(i, per)
        lx, ly = x0 + 8 + k * col_w, y + r * 20
        if kind == 'doc':
            sym_documented(s, lx, ly, 5)
        elif kind == 'doc?':
            sym_documented(s, lx, ly, 5, True)
        elif kind == 'mem':
            sym_remembered(s, lx, ly, 5)
        elif kind == 'mem?':
            sym_remembered(s, lx, ly, 5, True)
        elif kind == 'ctx':
            sym_context(s, lx, ly)
        elif kind == 'mon':
            sym_monument(s, lx, ly, c or MONUMENT, 4.4)
        elif kind == 'ram':
            sym_ramallah(s, lx, ly)
        elif kind == 'ram0':
            sym_ramallah(s, lx, ly, True)
        elif kind == 'spring':
            sym_spring(s, lx, ly)
        elif kind == 'dot':
            s.append(f'<circle cx="{lx}" cy="{ly}" r="5" fill="{c}" stroke="#FFFFFF" stroke-width="1.5"/>')
        elif kind == 'ring':
            s.append(f'<circle cx="{lx}" cy="{ly}" r="5" fill="#FFFFFF" stroke="{c}" stroke-width="2" stroke-dasharray="2.4 1.8"/>')
        elif kind == 'road':
            s.append(f'<line x1="{lx-9}" y1="{ly}" x2="{lx+9}" y2="{ly}" stroke="{c or "#C2A275"}" stroke-width="4.5" stroke-linecap="round"/>')
        elif kind in ('route-doc', 'route-mem', 'route-approx'):
            col = {'route-doc': DOC, 'route-mem': MEM, 'route-approx': c or MEM}[kind]
            dash = '7 4' if kind != 'route-approx' else '3 3'
            s.append(f'<line x1="{lx-10}" y1="{ly}" x2="{lx+10}" y2="{ly}" stroke="{col}" stroke-width="2.6" stroke-dasharray="{dash}"/>')
        elif kind == 'line':
            s.append(f'<line x1="{lx-10}" y1="{ly}" x2="{lx+10}" y2="{ly}" stroke="{c}" stroke-width="1.6"/>')
        elif kind == 'water':
            s.append(f'<path d="M{lx-10} {ly+2} q5 -6 10 0 t10 0" fill="none" stroke="{WADI}" stroke-width="1.6"/>')
        elif kind == 'contour':
            s.append(f'<path d="M{lx-10} {ly+3} q10 -9 20 0" fill="none" stroke="{CONTOUR_INDEX}" stroke-width="1.1"/>')
        s.append(text(lx + 14, ly + 4, lab, T_FURN, BODY))


# ─────────────────────────────── furniture
def neatline(s, x, y, w, h):
    s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="none" '
             f'stroke="{FRAME}" stroke-width="1"/>')


def scalebar(s, x, y, km, px):
    """Two-segment bar, bottom-left inside the frame, on a white tab."""
    s.append(f'<rect x="{x-6:.1f}" y="{y-16:.1f}" width="{px+40:.1f}" height="26" fill="#FFFFFF" opacity=".82" rx="2"/>')
    s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{px/2:.1f}" height="4.5" fill="{INK}"/>')
    s.append(f'<rect x="{x+px/2:.1f}" y="{y:.1f}" width="{px/2:.1f}" height="4.5" fill="#FFFFFF" stroke="{INK}" stroke-width=".8"/>')
    s.append(text(x, y - 4, '0', T_FURN, INK, 'middle'))
    s.append(text(x + px, y - 4, f'{km:g} km', T_FURN, INK, 'start'))


def north(s, x, y):
    s.append(f'<path d="M{x} {y-12} L{x+5} {y+5} L{x} {y+1} L{x-5} {y+5} Z" fill="{INK}"/>')
    s.append(text(x, y + 17, 'N', T_FURN, INK, 'middle', '700'))


# ─────────────────────────────── elevation
def _tile(z, x, y):
    os.makedirs(TILE_CACHE, exist_ok=True)
    p = os.path.join(TILE_CACHE, f'{z}_{x}_{y}.png')
    if not os.path.exists(p):
        import urllib.request
        url = f'https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png'
        for attempt in range(4):
            try:
                with urllib.request.urlopen(url, timeout=60) as r:
                    data = r.read()
                break
            except Exception:
                if attempt == 3:
                    raise
        open(p, 'wb').write(data)
    from PIL import Image
    import numpy as np
    a = np.asarray(Image.open(p).convert('RGB')).astype('float64')
    return a[..., 0] * 256 + a[..., 1] + a[..., 2] / 256 - 32768


def _merc(lat, lon, z):
    import numpy as np
    n = 2 ** z
    x = (lon + 180.0) / 360.0 * n * 256
    lr = np.radians(lat)
    y = (1 - np.log(np.tan(lr) + 1 / np.cos(lr)) / math.pi) / 2 * n * 256
    return x, y


def sample_dem(lat, lon, ground_m):
    """Bilinear elevation at arrays lat/lon, from tiles at the zoom whose pixel
    is just finer than ground_m metres."""
    import numpy as np
    latc = float(np.nanmean(lat))
    z = 12
    while z > 3 and 156543.0 * math.cos(math.radians(latc)) / 2 ** z < ground_m * 0.6:
        z -= 1
    fx, fy = _merc(lat, lon, z)
    tx0, tx1 = int(np.floor(fx.min() / 256)), int(np.floor(fx.max() / 256))
    ty0, ty1 = int(np.floor(fy.min() / 256)), int(np.floor(fy.max() / 256))
    mos = np.zeros(((ty1 - ty0 + 1) * 256, (tx1 - tx0 + 1) * 256))
    for ty in range(ty0, ty1 + 1):
        for tx in range(tx0, tx1 + 1):
            mos[(ty - ty0) * 256:(ty - ty0 + 1) * 256, (tx - tx0) * 256:(tx - tx0 + 1) * 256] = _tile(z, tx % 2 ** z, ty)
    gx = fx - tx0 * 256 - 0.5
    gy = fy - ty0 * 256 - 0.5
    x0 = np.clip(np.floor(gx).astype(int), 0, mos.shape[1] - 2)
    y0 = np.clip(np.floor(gy).astype(int), 0, mos.shape[0] - 2)
    ax = np.clip(gx - x0, 0, 1); ay = np.clip(gy - y0, 0, 1)
    return (mos[y0, x0] * (1 - ax) * (1 - ay) + mos[y0, x0 + 1] * ax * (1 - ay) +
            mos[y0 + 1, x0] * (1 - ax) * ay + mos[y0 + 1, x0 + 1] * ax * ay)


def _ramp(e):
    import numpy as np
    out = np.zeros(e.shape + (3,))
    es = [h[0] for h in HYPSO]
    for c in range(3):
        out[..., c] = np.interp(e, es, [h[1][c] for h in HYPSO])
    return out


def _hillshade(e, dx_m, dy_m, exag):
    """Lambertian shade, light from the north-west at 45 degrees."""
    import numpy as np
    g_row, g_col = np.gradient(e * exag, dy_m, dx_m)
    dzdx, dzdy = g_col, -g_row            # image rows run south
    norm = np.sqrt(dzdx ** 2 + dzdy ** 2 + 1)
    az, alt = math.radians(315), math.radians(45)
    lx, ly, lz = math.sin(az) * math.cos(alt), math.cos(az) * math.cos(alt), math.sin(alt)
    hs = (-dzdx * lx - dzdy * ly + lz) / norm
    return np.clip(hs, 0, 1)


def _paths_from_contours(cs_segs, tol=1.8):
    out = []
    for seg in cs_segs:
        if len(seg) < 12:
            continue
        d, last = [], None
        for i, (x, y) in enumerate(seg):
            if last is not None and i < len(seg) - 1 and abs(x - last[0]) < tol and abs(y - last[1]) < tol:
                continue
            d.append(('M' if not d else 'L') + '%.0f %.0f' % (x, y))
            last = (x, y)
        if len(d) > 2:
            out.append(''.join(d))
    return out


def _fill(e, land):
    """Priority-flood with a small epsilon (Barnes et al. 2014), so every land
    cell drains to the sea, a lake or the edge of the sheet."""
    import heapq
    import numpy as np
    H, W = e.shape
    out = e.copy()
    done = np.zeros((H, W), bool)
    pq = []
    for yy in range(H):
        for xx in range(W):
            if not land[yy, xx] or yy in (0, H - 1) or xx in (0, W - 1):
                heapq.heappush(pq, (out[yy, xx], yy, xx)); done[yy, xx] = True
    eps = 1e-3
    while pq:
        z, yy, xx = heapq.heappop(pq)
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                ny, nx = yy + dy, xx + dx
                if (dy or dx) and 0 <= ny < H and 0 <= nx < W and not done[ny, nx]:
                    done[ny, nx] = True
                    if out[ny, nx] <= z:
                        out[ny, nx] = z + eps
                    heapq.heappush(pq, (out[ny, nx], ny, nx))
    return out


def _wadis(e, land, ox, oy, cell, cell_km2, thr_km2):
    """D8 flow accumulation on the plate grid; returns [(path, rank)]."""
    import numpy as np
    H, W = e.shape
    e = _fill(e, land)
    big = np.full((H + 2, W + 2), np.inf)
    big[1:-1, 1:-1] = np.where(land, e, -1e6)   # the sea is the outlet
    best = np.zeros((H, W)); rec = np.full((H, W), -1, dtype=np.int64)
    rows = np.arange(H)[:, None]; cols = np.arange(W)[None, :]
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if not dy and not dx:
                continue
            nb = big[1 + dy:H + 1 + dy, 1 + dx:W + 1 + dx]
            slope = (e - nb) / math.hypot(dx, dy)
            sel = slope > best
            best = np.where(sel, slope, best)
            tgt = np.clip(rows + dy, 0, H - 1) * W + np.clip(cols + dx, 0, W - 1)
            rec = np.where(sel, tgt, rec)
    acc = np.where(land, 1.0, 0.0).ravel()
    recf = rec.ravel()
    order = np.argsort(-e.ravel(), kind='stable')
    for i in order:
        r = recf[i]
        if r >= 0 and acc[i]:
            acc[r] += acc[i]
    area = acc * cell_km2
    chan = (area >= thr_km2) & land.ravel()
    # channel heads: channel cells with no channel upstream
    up = np.zeros(H * W, dtype=bool)
    ok = chan & (recf >= 0)
    up[recf[ok]] = True
    seen = np.zeros(H * W, dtype=bool)
    out = []
    for h in np.nonzero(chan & ~up)[0]:
        pts, i = [], h
        while True:
            yy, xx = divmod(int(i), W)
            pts.append((ox + (xx + .5) * cell, oy + (yy + .5) * cell, area[i]))
            if seen[i]:
                break
            seen[i] = True
            r = recf[i]
            if r < 0 or not chan[r]:
                break
            i = r
        if len(pts) < 4:
            continue
        # split by rank so the line thickens downstream
        cur, rank = [], None
        for x, y, a in pts:
            k = 2 if a >= thr_km2 * 30 else (1 if a >= thr_km2 * 6 else 0)
            if rank is None:
                rank = k
            cur.append((x, y))
            if k != rank:
                out.append((cur, rank)); cur = [(x, y)]; rank = k
        if len(cur) > 1:
            out.append((cur, rank))
    paths = []
    for pts, rank in out:
        # light smoothing and decimation
        sm = []
        for j, (x, y) in enumerate(pts):
            if 0 < j < len(pts) - 1:
                x = (pts[j - 1][0] + 2 * x + pts[j + 1][0]) / 4
                y = (pts[j - 1][1] + 2 * y + pts[j + 1][1]) / 4
            sm.append((x, y))
        d = ''.join(('M' if j == 0 else 'L') + '%.0f %.0f' % p for j, p in enumerate(sm[::2] + [sm[-1]]))
        paths.append((d, rank))
    return paths


def terrain(key, inv, x, y, w, h, km_per_unit, land_polys=(), lake_polys=(), opts=None):
    """Build (or load) the terrain layer for a plate rectangle.

    inv(px, py) -> (lat, lon) on numpy arrays, the inverse of the map's
    projection in plate units. land_polys / lake_polys are lists of point
    lists already in plate units (for the land mask).
    Returns a dict: jpeg (base64), contours [(d, index?)], wadis [(d, rank)].
    """
    opts = dict(opts or {})
    cint = opts.get('contour', 0)
    thr = opts.get('wadi_km2', 0)
    res = opts.get('res', 1.6)          # raster pixels per plate unit
    sig = json.dumps([VERSION, key, round(x, 2), round(y, 2), round(w, 2), round(h, 2),
                      round(km_per_unit, 6), cint, thr, res], sort_keys=True)
    hkey = hashlib.sha1(sig.encode()).hexdigest()[:12]
    os.makedirs(TERRAIN_DIR, exist_ok=True)
    path = os.path.join(TERRAIN_DIR, f'{key}.json')
    if os.path.exists(path):
        d = json.load(open(path, encoding='utf-8'))
        if d.get('sig') == hkey:
            return d
    import numpy as np
    from PIL import Image, ImageDraw, ImageFilter
    W, H = int(round(w * res)), int(round(h * res))
    px = x + (np.arange(W) + .5) / res
    py = y + (np.arange(H) + .5) / res
    PX, PY = np.meshgrid(px, py)
    lat, lon = inv(PX, PY)
    ground_m = km_per_unit * 1000 / res
    e = sample_dem(lat, lon, ground_m)

    def mask(polys, W, H, scale, ox, oy):
        im = Image.new('L', (W, H), 0)
        dr = ImageDraw.Draw(im)
        for p in polys:
            if len(p) > 2:
                dr.polygon([((a - ox) * scale, (b - oy) * scale) for a, b in p], fill=255)
        return np.asarray(im) > 127

    land = mask(land_polys, W, H, res, x, y) if land_polys else np.ones((H, W), bool)
    lake = mask(lake_polys, W, H, res, x, y) if lake_polys else np.zeros((H, W), bool)
    rgb = _ramp(e)
    exag = opts.get('exag', 1.0 if km_per_unit < 0.3 else 2.0)
    hs = _hillshade(e, ground_m, ground_m, exag)
    shade = 0.70 + 0.36 * hs          # muted: never darker than 70 %
    rgb = np.clip(rgb * shade[..., None], 0, 255)
    sea_rgb = np.array([int(SEA[i:i + 2], 16) for i in (1, 3, 5)], float)
    lake_rgb = np.array([int(LAKE[i:i + 2], 16) for i in (1, 3, 5)], float)
    rgb[~land] = sea_rgb
    rgb[lake & land] = lake_rgb
    im = Image.fromarray(rgb.astype('uint8'), 'RGB')
    buf = io.BytesIO()
    q = opts.get('quality', 66)
    im.save(buf, 'JPEG', quality=q, optimize=True, progressive=True)
    while buf.tell() > opts.get('max_bytes', 110_000) and q > 34:
        q -= 8; buf = io.BytesIO(); im.save(buf, 'JPEG', quality=q, optimize=True, progressive=True)
    jpeg = base64.b64encode(buf.getvalue()).decode()

    # vectors on a grid of one cell per plate unit (contours) or coarser (wadis)
    contours = []
    if cint:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from matplotlib import contour as _c
        em = np.where(land & ~lake, e, np.nan)
        step = max(1, int(round(res)))
        es = em[::step, ::step]
        xs = x + (np.arange(es.shape[1]) * step + .5) / res
        ys = y + (np.arange(es.shape[0]) * step + .5) / res
        lo = math.ceil(np.nanmin(es) / cint) * cint if np.isfinite(np.nanmin(es)) else 0
        hi = np.nanmax(es) if np.isfinite(np.nanmax(es)) else 0
        levels = [v for v in np.arange(max(lo, cint), hi, cint)]
        if levels:
            fig = plt.figure()
            cs = plt.contour(xs, ys, es, levels=levels)
            for lev, segs in zip(cs.levels, cs.allsegs):
                idx = abs((lev / 800) - round(lev / 800)) < 1e-6 and lev > 0
                for d in _paths_from_contours([[(a, b) for a, b in sg] for sg in segs]):
                    contours.append((d, bool(idx)))
            plt.close(fig)
    wadis = []
    if thr:
        cell = opts.get('wadi_cell', 2.0)     # plate units per hydrology cell
        stepw = max(1, int(round(res * cell)))
        ew = e[::stepw, ::stepw]
        lw = (land & ~lake)[::stepw, ::stepw]
        cell_u = stepw / res
        cell_km2 = (cell_u * km_per_unit) ** 2
        wadis = _wadis(ew, lw, x, y, cell_u, cell_km2, thr)
    d = {'sig': hkey, 'jpeg': jpeg, 'contours': contours, 'wadis': wadis}
    json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    return d


def draw_terrain(s, t, x, y, w, h, clipid=None):
    clip = f' clip-path="url(#{clipid})"' if clipid else ''
    s.append(f'<image href="data:image/jpeg;base64,{t["jpeg"]}" x="{x:.1f}" y="{y:.1f}" '
             f'width="{w:.1f}" height="{h:.1f}" preserveAspectRatio="none"{clip}/>')
    if t['contours']:
        minor = ''.join(dd for dd, ix in t['contours'] if not ix)
        major = ''.join(dd for dd, ix in t['contours'] if ix)
        if minor:
            s.append(f'<path d="{minor}" fill="none" stroke="{CONTOUR}" stroke-width=".6" opacity=".9"/>')
        if major:
            s.append(f'<path d="{major}" fill="none" stroke="{CONTOUR_INDEX}" stroke-width="1.05" opacity=".8"/>')
    for rank, wd in ((0, .6), (1, 1.0), (2, 1.5)):
        ds = ''.join(dd for dd, r in t['wadis'] if r == rank)
        if ds:
            s.append(f'<path d="{ds}" fill="none" stroke="{WADI}" stroke-width="{wd}" '
                     f'stroke-linecap="round" stroke-linejoin="round" opacity=".8"/>')
