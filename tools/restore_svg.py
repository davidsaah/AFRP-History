#!/usr/bin/env python3
"""Put the v60 figure drawings back into the built book, matched by figure title.

Run from the repo root after build.py:

    python3 tools/restore_svg.py out/AFRP_The_One_Line_v5.html

The v60 drawings come from git (commit 9bcad59). Figures whose title is not in
v60 keep the drawing the build made. Text changes inside restored figures go in
src/post_restore_fixes.py. (This replaces the scratch-folder restore_svg.py used
up to v66.)
"""
import re, subprocess, sys

V60 = '9bcad59'
# Figures drawn fresh by the build, never restored (the old restore did not
# match them either; restoring Figure 27 would bring back 64 + 7 for 1562).
# v76: the maps are redrawn to docs/MAP_STYLE.md and must not be restored.
# Their text was checked against v60 before this list was added: no drift.
KEEP_NEW = {'The households, counted',
            'The oldest ground within a morning’s walk of Ramallah',
            'The ridge in the Iron Age, and the gap in the middle',
            'The roads he used, and the ridge they run along',
            'The district when Rome wrote it down',
            '“They scattered like the people of Sabaʾ”',
            'The road, and the ground it passes',
            'The hills around Ramallah — what has been dug, what was written, who ruled',
            'The road the family actually walked',
            'Where Ramallah went, 1901 onward',
            'The town, as Shāhīn drew it',
            'Where the road stopped'}
PAT = re.compile(r'(<div class="figtitle">(.*?)</div><div class="figwrap">)(<svg\b.*?</svg>)', re.S)

def figs(html):
    return {m.group(2): m.group(3) for m in PAT.finditer(html)}

path = sys.argv[1] if len(sys.argv) > 1 else 'out/AFRP_The_One_Line_v5.html'
old = figs(subprocess.run(['git', 'show', f'{V60}:out/AFRP_The_One_Line_v5.html'],
                          capture_output=True, text=True, check=True).stdout)
html = open(path, encoding='utf-8').read()
n = tot = 0
def sub(m):
    global n, tot
    tot += 1
    if m.group(2) in old and m.group(2) not in KEEP_NEW:
        n += 1
        return m.group(1) + old[m.group(2)]
    return m.group(0)
html = PAT.sub(sub, html)
open(path, 'w', encoding='utf-8').write(html)
print(f'restore_svg: {n} of {tot} figures restored from v60')
