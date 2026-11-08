#!/usr/bin/env python3
"""v64.1: text fixes inside figures that the SVG restore step brings back
from the v60 copies. Run after the restore and before restyle.py:

    python3 src/post_restore_fixes.py out/AFRP_The_One_Line_v5.html

Each fix is an exact string swap, and the script stops if a string is
missing. The same fixes are already made in the figure code, so once the
restore step is retired this file can go too.
"""
import sys

FIXES = [
    ('A Palestinian city and the seat of an authority. 43,880 people.',
     'A Palestinian city and the seat of an authority. 42,122 people in 2021.'),
    ('holding Jerusalem’s surrendered priests at Jifnā, six kilometres away.',
     'holding Jerusalem’s surrendered priests at Jifnā, about seven kilometres away.'),
]

p = sys.argv[1]
s = open(p, encoding='utf-8').read()
for old, new in FIXES:
    if old in s:
        s = s.replace(old, new)
    elif new not in s:
        sys.exit(f'post_restore_fixes: not found: {old[:60]}')
open(p, 'w', encoding='utf-8').write(s)
print('post_restore_fixes: done')
