# -*- coding: utf-8 -*-
"""v61: give every figure the family tree book's look.

The tree book is white paper, Times, Palestinian green (#007A3D), ochre
(#9A6324) and ink. This pass runs on the finished HTML, after the build and
after the atlas maps are restored, and maps every colour used inside the
book's SVG figures onto that palette:

  paper creams      -> white
  band and land tints -> pale ochre / warm stone
  golds and rusts   -> ochre
  plums and violets -> ink greys (the tree book has no third hue)
  water blues       -> cool stone grey
  greens            -> the tree book's greens

It also renames the few colours the captions mention ("the gold ring" is now
"the ochre ring", and so on). It only touches what is inside <svg>...</svg>
plus those exact caption phrases, and it is idempotent: no target colour is
also a source.

    python src/restyle.py out/AFRP_The_One_Line_v5.html
"""
import re
import sys

GREEN, DEEP, OCHRE, INK = '#007A3D', '#004A26', '#9A6324', '#1A1915'

MAP = {
    # paper
    '#FCFBF8': '#FFFFFF', '#FFFAF0': '#FFFFFF', '#FDF9F0': '#FFFFFF',
    # band fills and soft panels
    '#FDF6EC': '#FAF5EC', '#F3ECDD': '#F6EFE3', '#F6EEDF': '#F6EFE3',
    '#F3EFE4': '#F7F4EE', '#F4F1E8': '#F7F4EE', '#F6F3EC': '#F7F4EE',
    '#F1EDE4': '#F7F4EE', '#EFEBE2': '#F2EEE6', '#EFEDE8': '#F2EEE6',
    '#F7E7DC': '#F6EFE3',
    # land and relief on the maps
    '#F0E7D3': '#F7F5F0', '#E7DBC0': '#EDE8DE', '#DED4BE': '#E3DDD0',
    '#EDE7DA': '#F1EEE7', '#CFC6B2': '#D9D3C6',
    # golds, tans and rusts -> ochre family
    '#B98A4E': OCHRE, '#C08A4A': OCHRE, '#C98B3F': OCHRE, '#9A7A45': OCHRE,
    '#8A6A3A': '#7A4E1C', '#8A5A1E': '#7A4E1C', '#7A5A28': '#7A4E1C',
    '#8A6A2E': '#7A4E1C', '#A85210': '#7A4E1C', '#B0A184': '#BFA27A',
    '#A08E6A': '#A9855A',
    '#D4B483': '#D9BE96', '#E0CFAE': '#E9D7BD', '#E8D9BE': '#E9D7BD',
    '#C9BFA8': '#D3C6B0', '#C4B8A0': '#D3C6B0', '#B9B0A0': '#C2B8A8',
    # plums and violets -> ink greys
    '#6D4E9E': '#55514A', '#4A3A7A': '#3A3731', '#9A8CC0': '#9C968B',
    '#C7B8DE': '#CFCAC0', '#EDE7F4': '#F0EEEA',
    # water and blue labels -> cool stone
    '#E7EFF2': '#EEF1F0', '#CFE0E8': '#DDE3E1', '#B9D2DD': '#CBD4D1',
    '#8FB2C2': '#A3B0AC', '#B9CBD4': '#C6CFCC', '#B6C4CB': '#C6CFCC',
    '#BBCBD2': '#C6CFCC', '#D8E4E9': '#E3E8E6', '#7C99A6': '#7D8986',
    '#5E8296': '#6E7A77', '#3F7C90': '#55514A', '#4A7C8C': '#55514A',
    # greens -> the tree book's greens
    '#D5E9DF': '#DFEEE6', '#CFE3D6': '#DFEEE6', '#E4F0E8': '#E8F3ED',
    '#EFF6F1': '#F0F7F3', '#F0F5F0': '#F0F7F3', '#E9F2EC': '#F0F7F3',
    '#79B491': '#5DAA83', '#8FBFA6': '#7DBB9B', '#5E9B76': '#4E9A72',
    '#12703E': GREEN, '#0E5C33': DEEP, '#2E8B57': '#2A8A5C',
    # ink and greys
    '#1A1A1A': INK, '#46423B': '#3D3A35', '#77726A': '#6B6760',
    '#9A958C': '#8F8A80', '#C9A96A': '#C49A62', '#9BB0BA': '#A3B0AC', '#DCD6C9': '#D9D4C8', '#DDD6C6': '#D9D4C8',
}
_SHORT = {'#fff': '#FFFFFF'}

_HEX = re.compile(r'#[0-9A-Fa-f]{6}\b|#[0-9A-Fa-f]{3}\b')


def _swap(m):
    h = m.group(0)
    h = _SHORT.get(h.lower(), h).upper()
    return MAP.get(h, h)


# Gold and rust were two separate hues; on the tree book's single ochre they
# would merge. Shapes keep them apart as strong ochre (rust) against light
# ochre (gold); text keeps them apart as deep ochre (rust) against ochre (gold),
# so labels stay readable on white.
SHAPE = {'#B98A4E': '#C49A5E', '#C08A4A': '#C49A5E', '#C98B3F': '#C49A5E',
         '#9A7A45': '#C49A5E', '#A85210': OCHRE}
_TAG = re.compile(r'<(\w+)\b[^>]*>')


def _tag(m):
    t = m.group(0)
    if m.group(1) in ('text', 'tspan'):
        return _HEX.sub(_swap, t)
    return _HEX.sub(lambda h: SHAPE.get(_SHORT.get(h.group(0).lower(), h.group(0)).upper()) or _swap(h), t)


def recolour_svg(svg):
    return _TAG.sub(_tag, svg)


CAPTION_WORDS = [
    ('only the Franks, in the thin purple band,', 'only the Franks, in the thin dark band,'),
    ('The gold line is 1562', 'The ochre line is 1562'),
    ('The gold ring is the site of Ramallah', 'The ochre ring is the site of Ramallah'),
    ('The gold circle is the site of Ramallah', 'The ochre circle is the site of Ramallah'),
    ('the dashed violet rings are medieval pilgrim tradition', 'the dashed dark rings are medieval pilgrim tradition'),
    ('The book grades the two of them violet and dashed', 'The book grades the two of them dark and dashed'),
    # v60 moved the first naming to 1186; the restored atlas plate still said 1279.
    ('named in none of them, and in nothing at all until 1279.', 'named in none of them, and in nothing at all until 1186.'),
    ('The long gold bar is the important one', 'The long ochre bar is the important one'),
]


def restyle(html):
    html = re.sub(r'<svg\b.*?</svg>', lambda m: recolour_svg(m.group(0)), html, flags=re.S)
    for a, b in CAPTION_WORDS:
        html = html.replace(a, b)
    return html


if __name__ == '__main__':
    p = sys.argv[1]
    h = open(p, encoding='utf-8').read()
    h = restyle(h)
    # v79: the phone reader runs last, on the finished page.
    sys.path.insert(0, __import__('os').path.dirname(__file__))
    from reader import reader
    open(p, 'w', encoding='utf-8', newline='\n').write(reader(h))
