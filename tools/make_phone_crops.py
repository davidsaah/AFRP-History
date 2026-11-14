"""Make the phone close-ups for the document scans and old maps (v86).

Each entry: figure number -> (source image, list of boxes as fractions
x0,y0,x1,y1, optional rotation). Several boxes are stacked top to bottom.
Writes img/crops/fig<N>.jpg, about 1200 px wide, readable on a phone.
Run from the repo root: python3 tools/make_phone_crops.py
"""
import os, sys
from PIL import Image


SPECS = {
    '6.3':  ('img/sources/strehlke_1869_p18_no20.jpg', [(0.08, 0.26, 0.94, 0.38)]),
    '7.4':  ('img/sources/shahin_1982_p10.jpg', [(0.5, 0.033, 1.0, 0.077), (0.0, 0.033, 0.5, 0.077)]),
    '7.8':  ('img/sources/defter_1562_p73.jpg', [(0.60, 0.775, 0.97, 0.895), (0.0, 0.885, 0.32, 1.0)]),
    '7.11': ('img/shaheen/p024_1.jpg', [(0.0, 0.0, 1.0, 0.33), (0.0, 0.9, 1.0, 1.0)]),
    '8.5':  ('img/sources/seetzen_1854_p197.jpg', [(0.0, 0.07, 1.0, 0.22)]),
    '9.1':  ('img/sources/robinson_1841_p263.jpg', [(0.0, 0.898, 1.0, 0.945)]),
    '9.2':  ('img/sources/guerin_1875_p40.jpg', [(0.0, 0.622, 1.0, 0.716)]),
    '9.13': ('img/shaheen/p371_1.jpg', [(0.0, 0.27, 1.0, 0.62)]),
    '10.14': ('img/shaheen/p372_1.jpg', [(0.0, 0.0, 1.0, 0.40)], 'rot'),
    '10.16': ('img/sources/mirat_al_sharq_1919.jpg', [(0.0, 0.07, 1.0, 0.29)]),
    '10.19': ('img/shaheen/p283_3.jpg', [(0.0, 0.06, 0.53, 0.555)]),
    '10.21': ('img/sources/ramallah_1946_notice.jpg', [(0.03, 0.503, 1.0, 0.72)]),
    '10.22': ('img/sources/ramallah_1946_results_ar.jpg', [(0.0, 0.60, 1.0, 0.86)]),
    '10.23': ('img/sources/ballot_1946_p142.jpg', [(0.0, 0.08, 1.0, 0.38), (0.0, 0.77, 1.0, 1.0)]),
    '11.1': ('img/shaheen/p380_1.jpg', [(0.0, 0.0, 1.0, 0.418)]),
    '12.8': ('img/shaheen/p121_1.jpg', [(0.0, 0.0, 1.0, 0.21)]),
    # old maps: the part around Ramallah
    '6.4':  ('img/period/vesconte_c1320.jpg', [(0.59, 0.37, 0.82, 0.69)]),
    '7.5':  ('img/shaheen/p012_1.jpg', [(0.04, 0.22, 0.60, 0.56)]),
    '8.4':  ('img/shaheen/p038_1.jpg', [(0.44, 0.57, 0.74, 0.77)]),
    '9.14': ('img/period/pef_1880_sheet17.jpg', [(0.08, 0.0, 0.75, 0.55)]),
}

W = 1200


def make(num, src, boxes, rot=None):
    im = Image.open(src).convert('RGB')
    if rot == 'rot':
        im = im.rotate(-90, expand=True)
    parts = []
    for (x0, y0, x1, y1) in boxes:
        p = im.crop((int(im.width * x0), int(im.height * y0), int(im.width * x1), int(im.height * y1)))
        s = W / p.width
        if s > 2.6:
            s = 2.6
        parts.append(p.resize((int(p.width * s), int(p.height * s)), Image.LANCZOS))
    w = max(p.width for p in parts)
    gap = 24 if len(parts) > 1 else 0
    h = sum(p.height for p in parts) + gap * (len(parts) - 1)
    out = Image.new('RGB', (w, h), (255, 255, 255))
    y = 0
    for p in parts:
        out.paste(p, ((w - p.width) // 2, y)); y += p.height + gap
    os.makedirs('img/crops', exist_ok=True)
    path = 'img/crops/fig%s.jpg' % num.replace('.', '_')
    out.save(path, quality=80, optimize=True, progressive=True)
    return path, out.size


if __name__ == '__main__':
    only = sys.argv[1].split(',') if len(sys.argv) > 1 else list(SPECS)
    for n in only:
        spec = SPECS[n]
        p, sz = make(n, spec[0], spec[1], spec[2] if len(spec) > 2 else None)
        print(n, p, sz, os.path.getsize(p) // 1024, 'KB')
