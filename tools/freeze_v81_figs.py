#!/usr/bin/env python3
"""v82: freeze the older 860-wide drawings, as the v81 book printed them.

The v82 redraws (src/build_figs7.py) are laid out from these frozen copies, so
every word, number and colour they carry is the one the book already printed:
nothing is retyped. Run once, from the repo root, on a v81 build:

    python3 tools/freeze_v81_figs.py out/AFRP_The_One_Line_v5.html

It writes data/fig_v81/<slug>.svg and data/fig_v81/INDEX.json (title -> slug,
figure number and kind at v81).
"""
import json, os, re, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'data', 'fig_v81')
FIG = re.compile(r'<figure[^>]*>(?:<div class="fignum">([^<]*)</div>)?<div class="figtitle">(.*?)</div>'
                 r'<div class="figwrap">(<svg\b.*?</svg>)', re.S)


def slug(title):
    s = unicodedata.normalize('NFKD', re.sub(r'<[^>]+>', '', title)).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '_', s).strip('_')[:60]


def main(path):
    html = open(path, encoding='utf-8').read()
    os.makedirs(OUT, exist_ok=True)
    index = {}
    for num, title, svg in FIG.findall(html):
        vb = re.search(r'viewBox="([\d.\s-]+)"', svg)
        if not vb or float(vb.group(1).split()[2]) < 600:
            continue
        if num.split('·')[-1].strip() == 'Map':
            continue  # maps are drawn fresh by the build; see src/phone_maps.py
        t = re.sub(r'<[^>]+>', '', title)
        sl = slug(t)
        open(os.path.join(OUT, sl + '.svg'), 'w', encoding='utf-8', newline='\n').write(svg)
        index[t] = {'slug': sl, 'num': num.split('·')[0].replace('Figure', '').strip(),
                    'kind': num.split('·')[-1].strip()}
    json.dump(index, open(os.path.join(OUT, 'INDEX.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('froze', len(index), 'figures')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'out', 'AFRP_The_One_Line_v5.html'))
