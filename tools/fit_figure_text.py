#!/usr/bin/env python3
"""Measure how far each older figure's text can grow (v81).

Run on a freshly built book (figure_tidy is idempotent on the small capitals,
but the scales must be measured on unscaled text, so move data/figure_text_scale.json
aside first):

    python3 tools/fit_figure_text.py out/AFRP_The_One_Line_v5.html

For each figure that src/figure_tidy.py treats, it tries text scales from 1.6
down to 1.0 and keeps the largest at which, in Chromium:
  * no two labels overlap that did not overlap at scale 1,
  * no label that sat inside a box at scale 1 sticks out of it,
  * no label runs outside the drawing.
It writes data/figure_text_scale.json. Set PRINT_CHROMIUM to a browser binary
if Playwright's own is not installed.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
import figure_tidy as ft  # noqa: E402

STEPS = [1.6, 1.5, 1.45, 1.4, 1.35, 1.3, 1.25, 1.2, 1.15, 1.1, 1.05]
MEASURE = r"""
(svg) => {
  const T = [...svg.querySelectorAll('text')].map(t => t.getBBox());
  const vb = svg.viewBox.baseVal;
  const S = [...svg.querySelectorAll('rect,circle,ellipse,polygon')].map(s => s.getBBox())
     .filter(b => b.width < vb.width * .9 || b.height < vb.height * .9);
  return {T: T.map(b => [b.x, b.y, b.width, b.height]), S: S.map(b => [b.x, b.y, b.width, b.height]),
          vb: [vb.x, vb.y, vb.width, vb.height]};
}
"""


def inter(a, b, pad=0.6):
    return not (a[0] + a[2] - pad <= b[0] or b[0] + b[2] - pad <= a[0] or a[1] + a[3] - pad <= b[1] or b[1] + b[3] - pad <= a[1])


def inside(a, b, pad=0.4):
    return a[0] >= b[0] - pad and a[1] >= b[1] - pad and a[0] + a[2] <= b[0] + b[2] + pad and a[1] + a[3] <= b[1] + b[3] + pad


def ok(base, cur):
    T0, T1, S, vb = base['T'], cur['T'], base['S'], cur['vb']
    n = len(T0)
    for i in range(n):
        b = T1[i]
        if b[2] == 0:
            continue
        if b[0] < vb[0] - .5 or b[1] < vb[1] - .5 or b[0] + b[2] > vb[0] + vb[2] + .5 or b[1] + b[3] > vb[1] + vb[3] + .5:
            return False
        for j in range(i + 1, n):
            if T1[j][2] and inter(b, T1[j]) and not inter(T0[i], T0[j]):
                return False
        for s in S:
            if inside(T0[i], s) and not inside(b, s):
                return False
            if not inter(T0[i], s) and inter(b, s, pad=1.0):
                return False
    return True


def main(path):
    from playwright.sync_api import sync_playwright
    html = open(path, encoding='utf-8').read()
    out = {}
    with sync_playwright() as p:
        exe = os.environ.get('PRINT_CHROMIUM')
        b = p.chromium.launch(**({'executable_path': exe} if exe else {}))
        pg = b.new_page(viewport={'width': 900, 'height': 900})
        for m in ft.FIG.finditer(html):
            num, title, svg = m.group(2), ft.plain(m.group(3)), m.group(4)
            if not ft.eligible(num, svg):
                continue

            def measure(s):
                pg.set_content('<html><body style="margin:0">%s</body></html>' % s)
                return pg.eval_on_selector('svg', MEASURE)
            base = measure(ft.tidy(svg, 1.0))
            best = 1.0
            for f in STEPS:
                if ok(base, measure(ft.tidy(svg, f))):
                    best = f
                    break
            out[title] = best
            print('%-22s %-60s %.2f' % (num, title[:60], best))
        b.close()
    os.makedirs(os.path.dirname(ft.SCALES), exist_ok=True)
    json.dump(out, open(ft.SCALES, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True)
    print('wrote', ft.SCALES)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'out', 'AFRP_The_One_Line_v5.html'))
