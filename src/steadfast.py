# -*- coding: utf-8 -*-
"""v105: "Steadfast", the closing pages of chapter 12 for younger readers, with the memorial and the youth-group page.

Text: the Steadfast doc (claude.ai/artifact/1ixp4qPE4BLaBs9fUERtcY, 18 Nov 2026), checked against the book.
Two lines of the doc are left out because no source was found: Budrus's "eight months" and the claim
that Qaddūra camp stood on Cadora land. Names of the dead are printed up to 1967 only; after that, counts.
"""

def _era(head, *paras):
    return '<div class="sfera"><h4>%s</h4>%s</div>' % (head, ''.join('<p><b>%s.</b> %s</p>' % p for p in paras))


ERAS = [
    _era('1914–1918: hunger, typhus and the front line',
         ('Losing', 'The Ottoman army drafted our young men. Locusts and requisitions brought famine, and the typhus of 1916 killed, by Shaheen’s count, about three in ten people in the town. For nine months the front ran just north of Ramallah. The family tree names more than a dozen of the men who died, among them Butrous Ibrahim Saah, who was drafted and never came home.'),
         ('Caring', 'Dr Philip Maʿlūf died of typhus on 13 February 1916, caught while treating the sick. ʿAzeez and Selma Shaheen said a fig grove kept them alive. In 1918 the Catholic school became a hospital.'),
         ('Resisting', 'In 1914 Ḥannā Jiryis al-Nāṭūr, eighteen, and two other Ramallah men were executed by the Ottoman authorities for refusing to join the war. Others hid in the wadis rather than serve.')),
    _era('1936–1939: the great revolt',
         ('Resisting', 'Ramallah joined the six-month general strike and then the revolt. George Jaber Saah was hanged by the British in the Jerusalem prison on 16 November 1939. Mogannam Mogannam, head of the Arab lawyers, argued the cases of rebel fighters and saved several from the gallows. In 1938 the young men built stone barricades across the streets against the British armoured cars.'),
         ('Losing', 'British planes bombed the hills in 1938. Two women and three men were killed by bombs on their way home from the vineyards.')),
    _era('1948: the Nakba comes to Ramallah',
         ('Caring', 'In July 1948 the people of Lydda and Ramle were driven out and walked here in the summer heat. About 25,000 refugees reached Ramallah, and the town’s bakers worked day and night; the four Abū Shahla sisters baked bread for them every day. The Friends Boys School became a hospital staffed by volunteer doctors, and the Girls School housed about 200 people. Nameh Cadora’s Infant Welfare Society cared for families from Lydda, Ramle and Jaffa. The Friends Meeting House became a school, and tent schools went up in the new camps of al-Amʿarī, al-Jalazūn and Qalandiyā. By 1953 two in three people in Ramallah were refugees.'),
         ('Resisting', 'The town’s own Armed Youth Organisation defended Ramallah, paid for by a tax the people laid on themselves.'),
         ('Losing', 'Ḥannā Jiryis ʿUmrān was killed at Muṣrāra in Jerusalem. Ayyūb Rizq Mīkhāʾīl was killed at Nabī Yaʿqūb on 18 April 1948.')),
    _era('1967: the Naksa and the occupation',
         ('Losing', 'Ramallah fell on 6 June 1967. Dina Kharūfeh, fifteen, and her sister Lucy, twelve, were killed when an air raid hit the Evangelical Home school. They are buried in Ramallah. Anyone who was abroad that September lost the right to live here, and many of our own relatives were among them.'),
         ('Caring', 'Ramallah took in the people of ʿImwās, Yālū and Bayt Nūbā, three villages Israel destroyed, and many of them still live here. The Arab Women’s Union fed up to 200 refugee children.'),
         ('Resisting', 'In 1976 the town elected a nationalist council under Karīm Khalaf. In 1980 a settler car bomb cost him his leg, and town staff, volunteers and the Ramallah First Scouts guarded his hospital room in shifts for more than three months. When Israel dismissed the elected mayors in March 1982, the town boycotted the officer-run town hall. In 1983 Israel made the town take down the Manāra, because demonstrations gathered there. The town rebuilt it in 1999 and 2000.')),
    _era('1987–1993: the first intifada',
         ('Learning', 'On 10 January 1988 the army closed Birzeit University with a phone call. On 2 February it shut all 800 schools in the West Bank “until further notice.” So teachers taught in secret: Birzeit held classes in the al-Ḥamrā Hotel, the old Bateh house. The Friends School met only about 60 days in 1989–90 instead of 165, sold land to keep paying its teachers, and helped found a network to make home-teaching materials. When six families on one Ramallah street tried to teach their children together, soldiers came that same afternoon and the classes never began. Carrying a textbook could get you arrested.'),
         ('Caring', 'Merchants fed al-Amʿarī camp under curfew. The Abū Rayyā centre treated the injured. Ramallah people in America raised more than $300,000 for families at home, and from it grew the Sons of Ramallah society.'),
         ('Resisting', 'Neighbourhood committees ran daily life. People went on strike, boycotted Israeli goods and refused to pay taxes. Most of it was unarmed.'),
         ('Remembering', 'At the entrance to Dayr Ghassāna a monument stands for Luʾay of Dār Dāwūd, shot there.')),
    _era('2000–2005: the second intifada and the siege',
         ('Losing', 'In its first nine years, 182 people from Ramallah and al-Bīra district were killed, 49 of them children. In April 2002 tanks occupied the town. The hospital morgue filled, and when the curfew lifted for two hours, hundreds of people came out to bury the dead in the hospital yard.'),
         ('Caring', 'Doctors and ambulance crews kept working under fire, and not every patient could be reached. ʿUmar Ḥamāyil of Kafr Mālik bled to death because ambulances could not get to him. Widād Ṣafwān was shot while walking to the hospital.')),
    _era('2002 to today: the Wall',
         ('Resisting', 'Around Ramallah the Wall runs about 89 km and cuts through 19 villages. In 2004 the International Court of Justice ruled it illegal. From 2005 the people of Bilʿīn marched every Friday to their land, joined by visitors from abroad. In 2007 Israel’s own Supreme Court ordered the route moved, and in 2011 two kilometres came down, returning about 1,200 dunums. Bāsim Abū Raḥma was killed in 2009 and his sister Jawāhir in 2010. Birzeit’s Right to Education campaign protested the checkpoint on the student road.'),
         ('Losing', 'Since 2006, Israel has demolished 482 homes and other buildings in the district for lack of a permit it almost never grants (B’Tselem’s count, used here as support). More than a thousand people lost their homes, over half of them children.')),
    '<div class="sfera"><h4>Since 2023</h4><p>Settler attacks on Turmus ʿAyyā, al-Mughayyir, Kafr Mālik and Ṭaybeh rose sharply. In 2025 Ramallah governorate had more attacks than any other, and 88 buildings were demolished, the most of any year (B’Tselem). Villagers stayed on their land and replanted their olive trees.</p></div>',
    '<div class="sfera"><h4>What it adds up to</h4><p>The rulers changed every few decades: Ottoman, British, Jordanian, Israeli. What did not change was the answer. A school kept going somewhere, someone fed the stranger, someone refused, and someone wrote down the names. That is the inheritance this book hands on.</p></div>',
]

NAMES = [
    ('1914', 'Ḥannā Jiryis al-Nāṭūr, eighteen, executed for refusing to fight, and two men of the town whose names are lost'),
    ('1914–1918', 'Butrous Ibrahim Elias Saah · Ibrahim Daoud El-Karawat · Anton Hanna Omran · Mikhail Saleh Ayoub El-Safadi · Nicola and Elias Ayoub Danfoura · Yousef Hanna Mousa Ahwal · Bajis, Aziz and Mousa Khalil · Khalīl and Niqūlā Ḥishmeh · Khalīl Manṣūr · the infant Nicola Badran · in American uniform, Jameel Abdallah Mikhail and Najeeb Farhat'),
    ('1916', 'Dr Philip Maʿlūf, 13 February, of the typhus he caught treating the sick'),
    ('1939', 'George Jaber Saah, “George al-Aqraʿ”, hanged in Jerusalem on 16 November'),
    ('1939–1946', 'ʿĪsā Mūsā Khalīl Mūsā and Henry Abū Ḥadīd, in the Second World War · Khalīl Bishāra Mogannam, at the King David Hotel, 1946'),
    ('1948', 'Ayyūb Rizq Mīkhāʾīl, at Nabī Yaʿqūb, 18 April · Ḥannā Jiryis ʿUmrān, at Muṣrāra · Jamīl Jamīl Zanāyid Jr.'),
    ('1955', 'Rajā Abū ʿAmāsha'),
    ('1967', 'Dina Kharūfeh, fifteen, and her sister Lucy, twelve · Abū al-Ḥabāyib'),
]

COUNTS = [
    ('1987–1990', 'about 14 named', 'Al-Haq'),
    ('25–27 September 1996', '17', 'WAFA; UN A/52/131'),
    ('29 September 2000 – 2009', '182, 49 of them children', 'PCBS'),
    ('Died in Israeli custody, 1971–2025', '21', 'WAFA'),
    ('2000–2026, all years', '360, 104 of them children', 'B’Tselem (support only)'),
    ('Buildings demolished, 2006–2026', '482, 191 of them homes', 'B’Tselem (support only)'),
    ('Left homeless by them', '1,064, 573 of them children', 'B’Tselem (support only)'),
]

QUESTIONS = [
    'In 1988 teaching children at home could get a family in trouble. Why would an army be afraid of a classroom?',
    'In 1948 thousands of refugees reached Ramallah in a few days. What would your town need if that happened tomorrow?',
    'Which of the four answers (learning, caring, resisting, remembering) do you see in your own family’s story?',
    'Bilʿīn marched every week for years. What makes a protest last?',
    'Why does it matter to count the homes as well as the people?',
]

TODO = [
    ('Interview an elder.', 'Ask where they were in 1967, in 1988 or in 2002, and what they did. Record it, with their permission, and send it to the Federation, the AFRP.'),
    ('Find your name on the tree.', 'Look for a relative who was born abroad, and work out which war made the family leave.'),
    ('Make a memorial card.', 'Choose one name from the memorial and find out one thing about that person’s life, not only their death.'),
    ('Plant or pick olives.', 'Join a harvest trip in the district, or send support for one.'),
]


def html():
    mem = ''.join('<li><span class="my">%s</span> %s</li>' % n for n in NAMES)
    tab = ''.join('<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % r for r in COUNTS)
    return (
        '<section class="steadfast" id="steadfast">'
        '<div class="sfk">For younger readers · the close of chapter 12</div>'
        '<h3>Steadfast</h3>'
        '<p class="sflead">Every generation of Ramallah has lived through a war, an uprising or an occupation. None of them chose it. '
        'What each one did choose was how to answer it. They kept the schools going when schools were shut. They fed the people who arrived with nothing. '
        'They refused, in the street, in court and in the fields. And they wrote down the names. Palestinians call this <i>ṣumūd</i>, steadfastness. '
        'These pages follow the four answers through the century: <b>learning, caring, resisting and remembering.</b></p>'
        + ''.join(ERAS) +
        '<div class="memorial"><div class="mk">In memory</div><h4>The people we have lost</h4>'
        '<p class="mnote">Named here up to 1967. After that the dead are too many, and too recent, to name in a family book; they are counted below, each count as its source gives it.</p>'
        '<ul class="mlist">' + mem + '</ul>'
        '<table class="mcount"><thead><tr><th>Since 1967</th><th>Killed or lost</th><th>Source</th></tr></thead><tbody>' + tab + '</tbody></table>'
        '<p class="mfoot">From 2000 to 2009, the Palestinian statistics bureau counts 49 children of Ramallah and al-Bīra district killed; B’Tselem, an Israeli rights group, counts 104 from 2000 to 2026. Since 2006, 482 homes and buildings have been demolished, leaving more than a thousand people without a home.</p>'
        '</div>'
        '<div class="sfyouth"><h4>For youth groups</h4>'
        '<p><b>Questions to talk about</b></p><ol>' + ''.join('<li>%s</li>' % q for q in QUESTIONS) + '</ol>'
        '<p><b>Things to do</b></p><ul>' + ''.join('<li><b>%s</b> %s</li>' % d for d in TODO) + '</ul>'
        '<p><b>Help fill the gaps.</b> The tree has three men marked only “killed,” with no cause or year: Shawki Mikhail Akel (1977), Suleiman Khaleel Awwad and El-Abid Salah, who was killed on Holy Saturday. If your family knows their story, tell us.</p>'
        '</div>'
        '<p class="sfsrc">Every fact in these pages is told, with its source, in the entries of chapters 10 to 12. The names come from the family tree’s notes, Cadora, Nayrūz and Shaheen; the counts from Al-Haq, WAFA, the Palestinian Central Bureau of Statistics and the United Nations. B’Tselem, an Israeli rights group, is used only to fill and check them, and is marked where it is used.</p>'
        '</section>')


CSS = """
/* v105: Steadfast, the memorial and the youth-group page (src/steadfast.py) */
.steadfast{margin:28px 0 20px;padding:14px 16px 8px;border-top:3px solid #9A6324;background:#FBF8F2}
.steadfast .sfk{font-variant:small-caps;text-transform:lowercase;letter-spacing:.14em;color:#9A6324;font-size:.82rem;margin:0 0 2px}
.steadfast h3{margin:0 0 8px}
.steadfast p{text-indent:0!important}
.steadfast .sflead{font-size:1.02rem}
.steadfast .sfera{margin:12px 0 4px;break-inside:avoid-page}
.steadfast .sfera h4{margin:0 0 4px;color:#007A3D}
.steadfast .sfera p{margin:0 0 6px}
.memorial{margin:18px 0 14px;padding:12px 14px 6px;background:#fff;border:1px solid #D8D0C0;break-inside:avoid-page}
.memorial .mk{font-variant:small-caps;text-transform:lowercase;letter-spacing:.2em;color:#77726A;font-size:.8rem;text-align:center}
.memorial h4{text-align:center;margin:2px 0 6px}
.memorial .mnote{font-size:.84rem;color:#5A564E;text-align:center}
.memorial .mlist{list-style:none;margin:8px 0 12px;padding:0;font-size:.88rem;line-height:1.45}
.memorial .mlist li{margin:0 0 6px;padding-left:76px;text-indent:-76px;border:0;background:none}
.memorial .mlist li::before,.memorial .mlist li::after{content:none!important;display:none}
.memorial .my{display:inline-block;width:72px;text-indent:0;color:#9A6324;font-weight:700}
.memorial .mcount{width:100%;border-collapse:collapse;font-size:.82rem;margin:4px 0 8px}
.memorial .mcount th,.memorial .mcount td{text-align:left;padding:4px 6px 4px 0;border-bottom:1px solid #E6DFD2;vertical-align:top}
.memorial .mcount th{font-weight:700;color:#3A3730}
.memorial .mfoot{font-style:italic;font-size:.88rem;text-align:center;margin:8px 0}
.sfyouth{margin:14px 0 8px;padding:10px 14px 4px;background:#F4EFE6;border-left:3px solid #007A3D;font-size:.9rem;break-inside:avoid-page}
.sfyouth h4{margin:0 0 6px;color:#007A3D}
.sfyouth ol,.sfyouth ul{margin:0 0 8px;padding-left:20px}
.sfyouth li{margin:0 0 4px}
.steadfast .sfsrc{font-size:.8rem;color:#77726A;margin-top:10px}
@media (max-width:520px){.steadfast{padding:12px 11px 6px}.memorial{padding:10px 10px 4px}.memorial .mlist li{padding-left:0;text-indent:0}.memorial .my{display:block;width:auto}}
"""
