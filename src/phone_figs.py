#!/usr/bin/env python3
"""v82: put the phone-first redraws (src/build_figs7.py) in place of the older
860-unit drawings. Run by src/restyle.py after figure_tidy, on the finished
page, so the restore step and its text fixes still run underneath unchanged and
the redraws simply take the finished drawing's place, matched by title.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_figs7 as F7

REDRAW = {
    'The chain, link by link — built from the sources': F7.fig_chain,
    'A line to Adam implies a date for Adam': F7.fig_adam,
    'The branch at ʿĀbir — where this line leaves Abraham’s': F7.fig_branch,
    'The land, drawn as a tell — fifteen thousand years of layering': F7.fig_tell,
    'How a people is made': F7.fig_people,
    'The terraces, and one of the towers standing in them': F7.fig_terraces,
    'The highlands fill up, and nowhere else empties out': F7.fig_highlands,
    'The machine that watered a kingdom': F7.fig_dam,
    'Every biblical place within a day’s walk, and the village it survived as': F7.fig_bible,
    'Six sovereigns, one people': F7.fig_sovereigns,
    'The dam, and a date that has to move': F7.fig_damdate,
    '“They scattered like the people of Sabaʾ”': None,  # a map: see phone_maps
    'Twelve lands, in the order he crossed them': F7.fig_lands,
    'Who ruled, and who stayed, 636–1517': F7.fig_ruled,
    'Forty-five is the wrong number': F7.fig_fortyfive,
    'The void, measured — and shortened': F7.fig_void,
    'Five datings for one town — and they are not rivals': F7.fig_datings,
    'The same people, nine years apart': F7.fig_samepeople,
    'The Karak wheel, redrawn — what it says about Rāshid': F7.fig_wheel,
    'The ladder of a day’s work, about 1900–1903': F7.fig_wages,
    'The dark half-decade, 1914–1918': F7.fig_darkyears,
    'Every number anyone has ever recorded, 1596–2024': F7.fig_lognumbers,
    'John Mogannam’s chart of thirty-six named generations': F7.fig_mogannam,
    'The family’s account of itself, tested': F7.fig_tested,
}
REDRAW = {k: v for k, v in REDRAW.items() if v}

FIG = re.compile(r'(<div class="figtitle">(.*?)</div><div class="figwrap"[^>]*>)(<svg\b.*?</svg>)', re.S)


def apply(html, report=True):
    done = set()
    cache = {}

    def sub(m):
        t = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        if t not in REDRAW:
            return m.group(0)
        if t not in cache:
            cache[t] = REDRAW[t]()
        done.add(t)
        return m.group(1) + cache[t]
    html = FIG.sub(sub, html)
    missing = set(REDRAW) - done
    assert not missing, 'phone_figs: figures not found: %r' % sorted(missing)
    if report:
        print('phone_figs: %d figures redrawn for the phone' % len(done))
    return html


if __name__ == '__main__':
    p = sys.argv[1]
    h = open(p, encoding='utf-8').read()
    open(p, 'w', encoding='utf-8', newline='\n').write(apply(h))
