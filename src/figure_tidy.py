#!/usr/bin/env python3
"""v81: the older drawn figures, brought closer to the book's type.

The charts, diagrams, timelines and tables that the restore step brings back
from v60 were drawn 860 units wide with headings in full capitals and text as
small as 7 units. This pass, run by src/restyle.py after the recolouring, does two things to
each of them (maps are left alone: they follow docs/MAP_STYLE.md):

  * a heading inside the drawing that repeats the figure's title word for word
    is dropped (the title is printed once, above the figure);
  * where the drawing already prints its sources in full (SRC_IN_PLATE), the
    caption does not print them a second time;
  * every other line set in full capitals becomes small capitals, the book's quiet
    label style (the words are the same; only the letter forms change);
  * all the figure's text is enlarged by the largest factor at which nothing
    collides: no two labels touch that did not touch before, no label leaves a
    box it sat in, and nothing runs off the drawing. The factors are measured
    in a browser by tools/fit_figure_text.py and kept in
    data/figure_text_scale.json, so the build itself stays deterministic.

    python3 src/figure_tidy.py out/AFRP_The_One_Line_v5.html   # on its own, if needed
"""
import html as html_mod
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCALES = os.path.join(ROOT, 'data', 'figure_text_scale.json')
# small capitals are drawn about 0.75 of a capital's height: set them larger, so a
# label keeps the size it had in full capitals
SC_COMP = 1.3
# Figures whose drawing already prints its sources in full: the caption's source
# line would only repeat them, so it is left out.
SRC_IN_PLATE = {'Six sovereigns, one people',
                '“They scattered like the people of Sabaʾ”',
                'The road the family actually walked',
                'The Karak wheel, redrawn — what it says about Rāshid',
                'The town, as Shāhīn drew it'}
KINDS = {'Chart', 'Diagram', 'Timeline', 'Table'}

FIG = re.compile(r'(<figure[^>]*>(?:<div class="fignum">([^<]*)</div>)?<div class="figtitle">(.*?)</div><div class="figwrap">)(<svg\b.*?</svg>)', re.S)
TEXT = re.compile(r'(<text\b)([^>]*)>(.*?)</text>', re.S)


def plain(s):
    return re.sub(r'<[^>]+>', '', s)


def eligible(num, svg):
    kind = (num or '').split('·')[-1].strip()
    if kind not in KINDS or 'phonefig' in svg[:400]:
        return False
    vb = re.search(r'viewBox="([\d.\s-]+)"', svg)
    return bool(vb) and float(vb.group(1).split()[2]) >= 600


def is_caps(t):
    t = html_mod.unescape(t)
    letters = re.sub(r'[^A-Za-zÀ-ÖØ-öø-ÿĀ-ſḀ-ỿ]', '', t)
    return len(letters) >= 4 and t == t.upper() and t != t.lower()


def norm(t):
    return re.sub(r'[^a-z0-9]', '', html_mod.unescape(t).lower())


def tidy(svg, f=1.0, title=''):
    def text(m):
        attrs, body = m.group(2), m.group(3)
        if title and is_caps(plain(body)) and norm(plain(body)) == norm(title):
            return ''  # the figure's own title, printed again inside the drawing
        if is_caps(plain(body)):
            body = re.sub(r'>([^<]+)<', lambda x: '>' + x.group(1).lower() + '<', '>' + body + '<')[1:-1]
            attrs = re.sub(r'letter-spacing="([\d.]+)"', lambda x: 'letter-spacing="%.2f"' % (float(x.group(1)) * .6), attrs)
            attrs += ' style="font-variant:small-caps"'
            g = f * SC_COMP
        else:
            g = f
        if g != 1.0:
            sc = lambda x: '%s="%.1f"' % (x.group(1), float(x.group(2)) * g)
            attrs = re.sub(r'(font-size)="([\d.]+)"', sc, attrs)
            body = re.sub(r'(font-size)="([\d.]+)"', sc, body)
        return m.group(1) + attrs + '>' + body + '</text>'
    return TEXT.sub(text, svg)


def apply(html, report=True):
    scales = json.load(open(SCALES, encoding='utf-8')) if os.path.exists(SCALES) else {}
    n = 0

    def sub(m):
        nonlocal n
        if not eligible(m.group(2), m.group(4)):
            return m.group(0)
        n += 1
        return m.group(1) + tidy(m.group(4), scales.get(plain(m.group(3)), 1.0), plain(m.group(3)))
    html = FIG.sub(sub, html)

    def nosrc(m):
        fig = m.group(0)
        t = re.search(r'<div class="figtitle">(.*?)</div>', fig, flags=re.S)
        if t and plain(t.group(1)) in SRC_IN_PLATE:
            fig = re.sub(r'<span class="src">.*?</span>(?=</figcaption>)', '', fig, count=1, flags=re.S)
        return fig
    html = re.sub(r'<figure\b[^>]*>.*?</figure>', nosrc, html, flags=re.S)
    if report:
        print('figure_tidy: %d figures set in small capitals, %d with larger text' % (n, sum(1 for v in scales.values() if v > 1)))
    return html


def main(path):
    html = open(path, encoding='utf-8').read()
    open(path, 'w', encoding='utf-8', newline='\n').write(apply(html))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'out', 'AFRP_The_One_Line_v5.html'))
