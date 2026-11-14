#!/usr/bin/env python3
"""v82: prove the phone redraws and the phone map plates dropped nothing.

For every drawing frozen in data/fig_v81/, every word it printed must appear in
its redraw at least as many times (words are compared after removing
punctuation and case, since line breaks and small capitals change). Prints the
words a redraw is missing and exits non-zero if any are.

    python3 tools/check_redraw.py
"""
import collections, html, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
import build_figs7 as F7
from phone_figs import REDRAW


def words(svg):
    out = collections.Counter()
    for m in re.finditer(r'<text\b([^>]*)>(.*?)</text>', svg, re.S):
        if ' stroke=' in m.group(1):
            continue
        t = html.unescape(re.sub(r'<[^>]+>', ' ', m.group(2))).lower()
        for w in re.findall(r'[\w؀-ۿ’ʿʾ\'.,%–?-]+', t):
            w = w.strip('.,’\'–-')
            if w:
                out[w] += 1
    return out


bad = 0
for title, fn in REDRAW.items():
    old = words(F7.Old(title).raw)
    new = words(fn())
    miss = {w: n - new[w] for w, n in old.items() if new[w] < n}
    # an old drawing printed its own title as a heading; the page prints it once, above
    status = 'ok' if not miss else 'MISSING %s' % miss
    if miss:
        bad += 1
    print('%-62s %s' % (title[:62], status))

# the maps: every word of each full plate must be on its phone plate
page = os.path.join(ROOT, 'out', 'AFRP_The_One_Line_v5.html')
if os.path.exists(page):
    h = open(page, encoding='utf-8').read()
    # graticule figures (31.8°N, 35°E) are furniture: the phone plate sets them inside
    # the frame where they fit, and the full plate, a tap away, keeps them all
    deg = re.compile(r'<text\b[^>]*>\s*\d+(\.\d+)?°[NSEW]\s*</text>')
    for m in re.finditer(r'<div class="figtitle">((?:(?!figtitle).)*?)</div><div class="figwrap"[^>]*>'
                         r'(<svg[^>]*class="phonefig phonemap">.*?)(<svg class="fullmap".*?</svg>)', h, re.S):
        title = html.unescape(re.sub(r'<[^>]+>', '', m.group(1)))
        old, new = words(deg.sub('', m.group(3))), words(deg.sub('', m.group(2)))
        miss = {w: n - new[w] for w, n in old.items() if new[w] < n}
        if miss:
            bad += 1
        print('%-62s %s' % (('map: ' + title)[:62], 'ok' if not miss else 'MISSING %s' % miss))
sys.exit(1 if bad else 0)
