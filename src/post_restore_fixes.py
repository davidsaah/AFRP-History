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
    # v65.1: David's choices on the 31 conflicts (Figures 21, 22, the tell, the Karak wheel, the population chart)
    ('<text x="300.0" y="253.0" font-size="9.6" fill="#46423B" text-anchor="start" font-weight="400" font-style="normal" letter-spacing="0" font-family="Times New Roman, Times, serif">The name Rām Allāh is written down in a sultan’s endowment deed, 1279.',
     '<text x="300.0" y="247.0" font-size="9.6" fill="#46423B" text-anchor="start" font-weight="400" font-style="normal" letter-spacing="0" font-family="Times New Roman, Times, serif">A sultan’s endowment of 1279 includes Rām Allāh (the deed is lost; a court</text><text x="300.0" y="259.0" font-size="9.6" fill="#46423B" text-anchor="start" font-weight="400" font-style="normal" letter-spacing="0" font-family="Times New Roman, Times, serif">record of 1565 cites it).'),
    ('The gap from Jafna (fl. c. 520) to Rāshid (fl. c. 1500) is about 1,000 years. Dividing it 45 ways gives a',
     'The gap from al-Ḥārith (d. 569) to Rāshid (fl. c. 1500) is 931 years. Dividing it 45 ways gives a'),
    ('<rect x="250" y="106" width="266.7" height="22" fill="#A85210" rx="3"/>',
     '<rect x="250" y="106" width="248.3" height="22" fill="#A85210" rx="3"/>'),
    ('<text x="526.7" y="122.0" font-size="10.5" fill="#46423B" text-anchor="start" font-weight="700" font-style="normal" letter-spacing="0" font-family="Times New Roman, Times, serif">22.2 years per generation',
     '<text x="508.3" y="122.0" font-size="10.5" fill="#46423B" text-anchor="start" font-weight="700" font-style="normal" letter-spacing="0" font-family="Times New Roman, Times, serif">20.7 years per generation'),
    ('<text x="526.7" y="136.0" font-size="9.5" fill="#77726A" text-anchor="start" font-weight="400" font-style="italic" letter-spacing="0" font-family="Times New Roman, Times, serif">',
     '<text x="508.3" y="136.0" font-size="9.5" fill="#77726A" text-anchor="start" font-weight="400" font-style="italic" letter-spacing="0" font-family="Times New Roman, Times, serif">'),
    ('<rect x="250" y="140" width="387.1" height="22" fill="#007A3D" rx="3"/>',
     '<rect x="250" y="140" width="360.4" height="22" fill="#007A3D" rx="3"/>'),
    ('<text x="647.1" y="156.0" font-size="10.5" fill="#46423B" text-anchor="start" font-weight="700" font-style="normal" letter-spacing="0" font-family="Times New Roman, Times, serif">32.3 years per generation',
     '<text x="620.4" y="156.0" font-size="10.5" fill="#46423B" text-anchor="start" font-weight="700" font-style="normal" letter-spacing="0" font-family="Times New Roman, Times, serif">30.0 years per generation'),
    ('<text x="647.1" y="170.0" font-size="9.5" fill="#77726A" text-anchor="start" font-weight="400" font-style="italic" letter-spacing="0" font-family="Times New Roman, Times, serif">what 32 years a generation gives',
     '<text x="620.4" y="170.0" font-size="9.5" fill="#77726A" text-anchor="start" font-weight="400" font-style="italic" letter-spacing="0" font-family="Times New Roman, Times, serif">what 30 years a generation gives'),
    ('THE GENEALOGICAL VOID — 931 years, about thirty-one generations, and only three of them named',
     'THE GAP IN OUR LINE — 931 years, about thirty-one generations, and only three of them named'),
    ('<rect x="382.1" y="280" width="256.7" height="24" fill="#007A3D" opacity=".13" stroke="#007A3D"/><text x="510.4" y="296.0" font-size="9.8" fill="#004A26" text-anchor="middle" font-weight="700" font-style="normal" letter-spacing="0" font-family="Times New Roman, Times, serif">THE DOCUMENTARY VOID — 610 years',
     '<rect x="554.6" y="280" width="84.2" height="24" fill="#007A3D" opacity=".13" stroke="#007A3D"/><text x="638.8" y="318.0" font-size="9.8" fill="#004A26" text-anchor="end" font-weight="700" font-style="normal" letter-spacing="0" font-family="Times New Roman, Times, serif">THE GAP IN THE RECORD OF OUR PEOPLE — about two centuries, after c. 1300'),
    ('<path d="M247.0 292 L380.4 292" stroke="#007A3D" stroke-width="2.4"/><text x="314.6" y="286.0" font-size="8.6" fill="#004A26" text-anchor="middle" font-weight="700" font-style="normal" letter-spacing="0" font-family="Times New Roman, Times, serif">',
     '<path d="M247.0 292 L552.9 292" stroke="#007A3D" stroke-width="2.4"/><text x="400.8" y="286.0" font-size="8.6" fill="#004A26" text-anchor="middle" font-weight="700" font-style="normal" letter-spacing="0" font-family="Times New Roman, Times, serif">'),
    ('Greek sources stop naming the Ghassanids. <tspan font-style="italic">The void has a start date.</tspan>',
     'Our line stops in 569. In 593/4 the Greek writers stop naming the family.'),
    (' I.17; Serikoff (2017) for the silence after 594; Kennedy (2010) and al-Yaʿqūbī (d. 890); the ʿAbūd, Jifnā, Karak and Shawbak records as cited in Part II.',
     ' I.17; Shahîd, <tspan font-style="italic">BASIC</tspan> I.1 (1995) for the silence after 593/4; Kennedy (2010) and al-Yaʿqūbī (d. 890); the ʿAbūd, Jifnā, Karak and Shawbak records as cited in Part II.'),
    ('<text x="692.0" y="321.0" font-size="10.6" fill="#8A5A1E" text-anchor="middle" font-weight="700" font-style="normal" letter-spacing="0" font-family="Times New Roman, Times, serif">Ḥasan</text>',
     '<text x="692.0" y="321.0" font-size="10.6" fill="#8A5A1E" text-anchor="middle" font-weight="700" font-style="normal" letter-spacing="0" font-family="Times New Roman, Times, serif">Ḥassān</text>'),
    ('Two counts disagree: Guérin estimated about 1,100 in 1870, but the census Shāhīn cites for the same year counted 2,000. The chart follows the census.',
     'Two counts disagree: an estimate of about 1,100 is given for 1870, but the census Shāhīn cites for the same year counted 2,000. The chart follows the census.'),
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
