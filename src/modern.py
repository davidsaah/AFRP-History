# -*- coding: utf-8 -*-
"""v83: Ramallah from 1914 to today, set out as a Palestinian history museum would.

David, 14 Nov 2026: "Let's make the more recent history more enriched and include what
happened in Ramallah during all the wars ... the intifadas, the occupation. All the up
today ... in a way that you would see recorded in a Palestinian history museum with facts
and records and a Palestinian narrative." David chose option A, "Enrich chapters": the
missing events go into the chapters the book already has, and the book grows a little.

All of the new text is here, so the book source changes in two lines only:

    build_v5.py, before CONTENTS:           import modern; modern.apply(globals())
    build_v5.py, before the page is saved:  html = modern.finish(html)

Each new entry is built like a room in a museum: a short story; "The record", a compact
panel of the documents and dates; at most one testimony for each era, quoted from a
published Palestinian source; and one or two photographs. Only images AFRP holds are
printed (Naseeb Shaheen's collection). Library of Congress and permission-needed items
are listed in docs/MODERN_IMAGES.md.

Sources: Palestinian and Arab first. United Nations and press reports are cited for dates
and counts. No Israeli author is relied on.
"""
import re

SH = 'Naseeb Shaheen, <i>A Pictorial History of Ramallah, Part II</i> (Birzeit University Press, 2005)'
CAD = ('Joseph Jiryes Cadora (Yūsuf Jiryis Qaddūra), <i>Remembering Ramallah</i>, trans. Samira Rafidi Meghdessian (2023), '
       'from his <i>History of the City of Ramallah</i> (New York, 1954)')
SHAHIN = 'ʿAzīz Shāhīn, <i>Kashf al-niqāb</i> (Birzeit University, 1982)'
FARHAN = 'Yaḥyá ʿĪsá al-Farḥān, <span class="ar">قصة رام الله والبيرة</span> (<i>Qiṣṣat Rām Allāh wa-l-Bīra</i>)'
CENT = 'Ramallah Municipality, <i>Ramallah: One Hundred Years</i>, the municipality’s centennial book (2008)'
TARAKI = 'Lisa Taraki, “Enclave Micropolis: The Paradoxical Case of Ramallah/al-Bireh,” <i>Journal of Palestine Studies</i> 37:4 (2008), 6–20'
IPS = 'Institute for Palestine Studies, <i>Palestine Chronology</i>, chronology.palestine-studies.org'
BZU = 'Birzeit University, “History of Birzeit University,” pas.birzeit.edu/node/151'


def _rec(items):
    """The record: a compact panel of documents and dates."""
    return ('<div class="record"><div class="rk">The record</div><ul>'
            + ''.join('<li>%s</li>' % x for x in items) + '</ul></div>')


def _testimony(words, who):
    return '<blockquote class="testimony"><p>%s</p><span class="tw">%s</span></blockquote>' % (words, who)


def _p(t):
    return '<p>' + t + '</p>'


def apply(g):
    """Add the modern history to chapters 10 to 12. g is build_v5's globals()."""
    E, c, _plate, RIGHTS = g['E'], g['c'], g['_plate'], g['RIGHTS']

    def plate(fn, pg, cap, kind='Photograph'):
        return _plate(fn, '../img/shaheen/' + fn, cap, '%s, p. %s. %s' % (SH, pg, RIGHTS['afrp']), kind)

    def locplate(fn, item, cap, who):
        return _plate(fn, '../img/loc/' + fn, cap,
                      f'{who} Library of Congress, Prints &amp; Photographs Division, '
                      f'<a href="https://www.loc.gov/item/{item}/">loc.gov/item/{item}</a>. {RIGHTS["loc"]}', 'Photograph')

    def title(e):
        return re.sub(r'<[^>]+>', '', e[5])

    def idx(prefix):
        hits = [i for i, e in enumerate(E) if e[0] == 'e' and title(e).startswith(prefix)]
        assert len(hits) == 1, (prefix, hits)
        return hits[0]

    def add_body(prefix, html):
        i = idx(prefix)
        E[i] = E[i][:7] + (E[i][7] + html,) + E[i][8:]

    def insert_after(prefix, entries):
        i = idx(prefix)
        E[i + 1:i + 1] = entries

    def insert_before(prefix, entries):
        i = idx(prefix)
        E[i:i] = entries

    def ent(ch, date, title_, note, body):
        return ('e', ch, date, 'documents', False, title_, note, body)

    # =======================================================================
    # CHAPTER 10: the Mandate
    add_body('The war, the locusts', plate('p372_1.jpg', 371,
        'A letter from Ibrāhīm Dāʾūd Ḥarb to his son Wadīʿ, written on 16 December 1916, in the middle of the war, '
        'from Burqīn near Jenin.', 'Document'))

    snow = ent(10, '1920 · 1927', 'Snow, then the earth shakes',
        'On <b>9 February 1920</b> snow fell on Ramallah for seventy-two hours, up to a metre and a quarter deep. '
        'It broke the olive trees and closed the Jerusalem road for a week{}. '
        'On <b>11 July 1927</b> the great earthquake struck Palestine. In Ramallah <b>two people were killed</b> and many houses were broken, above all in the old town. '
        'The Latin Patriarchate paid for those who had lost their houses{}.'.format(
            c(CAD + ', p. 55.'),
            c(SHAHIN + ', English section, chronology, p. 75: “Only two inhabitants of Ramallah killed, but property damage heavy”; '
              + SH + ', p. 34; ' + CAD + ', p. 56, for the old town and the Patriarchate.')),
        locplate('03041v.jpg', '2019696336',
            'A house in Nablus left a shell by the earthquake of 11 July 1927. We have found no photograph of the damage in Ramallah.',
            'American Colony Photo Department, 1927.')
        + _p('<b>What we still don’t know.</b> We have found nothing written about Ramallah in the troubles of August 1929.'))
    add_body('The counting years', locplate('16769v.jpg', '2019707547',
        'The opening of the Palestine Broadcasting Service at its transmitter in Ramallah, 30 March 1936. '
        'The High Commissioner gives the inaugural address; the mast stands behind the crowd.',
        'Matson Photo Service, 1936.'))
    insert_after('The war, the locusts', [snow])

    ww2 = ent(10, '1939–1945', 'The Second World War',
        'The war reached Ramallah through its young men. <b>Elias Nasrallah Oudeh</b> served as a wireless operator in the Trans-Jordan Frontier Force, '
        'the British-commanded frontier cavalry, from 1938 to 1943, and his discharge certificate survives{}. '
        '<b>Shukri Elias ʿAjlouny</b> was a telegraph operator at the airport of Lydda in 1940{}, and <b>Edward Salamy</b> of Ramallah served in the United States army{}. '
        'At home the district was run by Palestinian officers of the Mandate: Mitri Farraj until 1941, then, from 1943, the historian ʿĀrif al-ʿĀrif{}.'.format(
            c(SH + ', p. 282: the certificate of discharge, serial no. 3904, “W/T operator,” enlisted 4 October 1938, discharged 27 December 1943.'),
            c(SH + ', p. 275.'), c(SH + ', p. 92.'), c(CAD + ', p. 55.')),
        plate('p283_3.jpg', 282, 'The certificate of discharge of Corporal Elias Nasrallah Oudeh, wireless operator of the Trans-Jordan Frontier Force, '
              'enlisted 4 October 1938 and discharged 27 December 1943, beside his photograph on horseback.', 'Document')
        + locplate('14899v.jpg', '2019705094',
            'A Ramallah woman in the embroidered dress and headdress of the town, photographed in colour between 1935 and 1946.',
            'Matson Photo Service, 1935–46.'))
    insert_after('The revolt reaches the town', [ww2])

    # =======================================================================
    # CHAPTER 11: 1948 and the Jordanian years
    guard = ent(11, 'November 1947 – May 1948', 'The town guards itself',
        'When the United Nations voted in November 1947 to divide Palestine, Ramallah, al-Bīra and Baytūniyā marched against the Mandate, the United Nations and the United States{}. '
        'Then the town organised its own guard. A committee with <b>one member for each clan</b> raised a tax and bought arms, '
        'and built roadblocks and watchtowers under Dr <b>Jalīl Badrān</b>. On 14 March 1948 the guard beat off an attack on the Ramallah–Ramle bus, '
        'and it fought on the Jerusalem road at al-Qasṭal{}. '
        'From April the people of Bīr Nabālā, Bayt Maḥsīr and Jaffa came up the hill: “Churches and schools opened their doors to give them refuge and shelter.” '
        'On 15 May, at almost noon, the Arab Legion drove into the town{}.'.format(
            c(CAD + ', p. 57.'), c(CAD + ', p. 58.'), c(CAD + ', pp. 58–59. Cadora was acting mayor from 1 April 1948.')),
        _testimony('What a wonderful hour that was when the Ramallah citizens called on God as the Arab army entered the town! '
                   'Fear dissipated, hope increased and souls felt at ease.',
                   'Yūsuf Qaddūra, acting mayor, on 15 May 1948 (Cadora, p. 59)')
        + _rec(['14 March 1948: the town guard beats off an attack on the Ramle bus.',
                '18 April 1948: young men of the district shot dead at Nabī Yaʿqūb on their way to work in Jerusalem.',
                '15 May 1948: the Arab Legion enters Ramallah (all from Cadora, pp. 58–59).'])
        + plate('p380_1.jpg', 379, 'The permit of Harb Harb of Ramallah, clerk in the Port Manager’s office, to enter the port of Haifa, '
                'issued on 19 April 1948, three days before Haifa fell.', 'Document'))
    insert_before('The catastrophe of 1948', [guard])

    add_body('Where the refugees lived',
        plate('p185_2.jpg', 184, '“Refugee School at Ramallah Friends Meetinghouse,” August 1949, as written on the back of the print.')
        + plate('p184_1.jpg', 183, '“Refugee home in camp near Ramallah. This family has a very neat tent and have made stair-steps from the ‘street’ from flat stones.” 1950.'))

    jordan = ent(11, '1949–1966', 'Under the Jordanian crown',
        'From 1950 Ramallah was a town of the Hashemite Kingdom, and from 1954 its people were Jordanian citizens and Palestinians at once. '
        'The kingdom gave them a parliament and watched them. On 11 May 1951 the leaders of the Labour Party in Ramallah were arrested, accused of communism, and jailed in Amman{}. '
        'Dr <b>Daoud Mikhail</b> was jailed in 1957 for the National Socialist Party; years later his daughter, Dr Hanan Mikhail ʿAshrawi, reminded King Hussein of it{}. '
        'In 1952, Cadora writes, “life became unbearable,” and the town’s families left for America{}.'.format(
            c(CAD + ', p. 62.'), c(SH + ', p. 54.'), c(CAD + ', p. 63.')),
        plate('p045_3.jpg', 44, 'Ḥannā Khalaf of Ramallah addressing the Parliament of Jordan, 1961.')
        + plate('p337_2.jpg', 336, 'The Jordanian army band marches round al-Manāra and its five lion heads, probably in the 1960s.')
        + _p('<b>What we still don’t know.</b> What Ramallah did in the Suez war of 1956, and in the protests after the raid on al-Samūʿ in November 1966.'))
    insert_after('Where the refugees lived', [jordan])

    # =======================================================================
    # CHAPTER 12: 1967 to today
    june = ent(12, 'June 1967 – 1982', 'Occupation, and the mayor in Houston',
        'On <b>6 June 1967</b> the Israeli army took Ramallah{}. Every weapon in the town was to be handed in at al-Manāra; '
        'people who had worked with the Palestinian organisations were arrested and some expelled. The army made Bayt Īl, Beit El, the seat of its command{}. '
        'Families driven out of ʿImwās, Yālū and Bayt Nūbā found shelter at Baytūniyā and in Ramallah{}. '
        'The feasts went quiet: “all large festivities, both Muslim and Christian, have ceased{}.” '
        'In 1974 the dentist <b>Alfred Toubassi</b> was taken to the Lebanese border at night and sent across, and Birzeit’s president, Dr <b>Ḥannā Nāṣir</b>, was deported for nineteen years{}. '
        'From 1978 the occupation set up the <b>Village Leagues</b> against the elected mayors, with their centre at Ramallah{}. '
        'The mayor the town had elected, <b>Karīm Khalaf</b>, flew in July 1974 to the Federation’s convention in Houston{}.'.format(
            c('Applied Research Institute–Jerusalem (ARIJ), <i>Atlas 40</i>, ch. 1.3.'),
            c(FARHAN + ', pp. 79 and 100–101 (page numbers of the OCR text).'),
            c('al-Haq, field report on the Latrun villages, 13 June 2013. al-Haq is a Palestinian human-rights organisation founded in Ramallah in 1979.'),
            c(SHAHIN + ', English section, pp. 63–64.'),
            c(SH + ', p. 55; ' + BZU + '.'),
            c(FARHAN + ', p. 102.'),
            c(SH + ', pp. 341 and 357.')),
        plate('p162_1.jpg', 161, 'Feeding the children of needy refugees after the 1967 war, late 1960s.')
        + plate('p358_2.jpg', 357, 'Houston, July 1974: Mayor Karīm Khalaf with the Federation’s president, George Mogannam, and all its past presidents.')
        + _rec(['6 June 1967: Ramallah taken (ARIJ).',
                '1974: Dr Alfred Toubassi and Dr Ḥannā Nāṣir deported (Shaheen 2005; Birzeit University).',
                '2 June 1980: Mayor Khalaf maimed by a settler bomb; removed by the occupation in 1982 (in the entry above).']))

    int1 = ent(12, '1987–2000', 'The first intifada, and the Authority',
        'In December 1987 the uprising began, and Ramallah was one of its centres{}. In the long sieges, Lisa Taraki writes, '
        '“the towns’ prosperous merchants … paid their political dues by supplying the camp [al-Amʿarī] with food and provisions{}.” '
        'Birzeit University was closed by military order from <b>8 January 1988</b> to <b>29 April 1992</b>, and its teachers held classes underground in Ramallah{}. '
        'After Oslo the army withdrew, and on <b>27 December 1995</b> the Palestinian Authority took control of Ramallah and al-Bīra{}. '
        'Ramallah took over the work of a Jerusalem that was being closed off. Its own people called the new city “a ‘five-star prison’”{}. '
        'The Khalil Sakakini Cultural Centre opened in 1996, and in May 1999 a Palestinian team performed the first heart catheterisation at the Ramallah government hospital{}.'.format(
            c(CENT + '.'), c(TARAKI + ', p. 16.'),
            c(BZU + '; ' + IPS + ', 20 April 1992.'),
            c(IPS + ', 27 December 1995: “PA assumes control of Ramallah, al-Bireh.”'),
            c(TARAKI + ', pp. 6–8.'),
            c(SH + ', p. 342, and p. 120, with <i>al-Ayyām</i> (Ramallah), 24 May 1999: '
              '<span class="ar" dir="rtl">اجراء أول عملية قسطرة للقلب في مستشفى رام الله الحكومي</span>, led by Dr Niḍāl Ḥarb.')),
        plate('p121_1.jpg', 120, '<i>al-Ayyām</i>, 24 May 1999: “The first heart catheterisation in the Ramallah government hospital.”', 'Newspaper')
        + _rec(['8 January 1988 – 29 April 1992: Birzeit University closed by military order (Birzeit University).',
                '27 December 1995: the Palestinian Authority takes control of the town (IPS).']))

    int2 = ent(12, '2000–2005', 'The second intifada and the siege',
        'On <b>12 October 2000</b> Israel bombed Ramallah from the air: Arafat’s headquarters, the broadcasting centre and the police stations{}. '
        'On <b>29 March 2002</b> the army invaded the town{}. Forty thousand people were under curfew, with water and power cut. '
        'By 3 April at least fifty-four Palestinians had been killed, and twenty-three were buried together in the car park of the Ramallah hospital{}. '
        'The United Nations recorded “extensive physical damage” to the Authority’s civilian offices{}. '
        'Arafat, besieged in the Muqāṭaʿa as its buildings were pulled down around him, died in Paris on 11 November 2004 and was buried there the next day{}.'.format(
            c(IPS + ', 12 October 2000.'),
            c('United Nations, A/ES-10/186, 30 July 2002: the operation “began on 29 March with an incursion into Ramallah.”'),
            c('Charmaine Seitz, “In Ramallah, Grueling Reoccupation Grinds On,” <i>Middle East Report Online</i>, 5 April 2002, citing the Palestinian Centre for Human Rights.'),
            c('A/ES-10/186 (2002).'),
            c(IPS + ', 21 September 2002, for the demolitions.')),
        _testimony('We have two kilos of rice and we have to make it last for the four of us.',
                   'A Ramallah household under curfew, April 2002 (Seitz, <i>Middle East Report Online</i>)'))

    wall = ent(12, '2002–2025', 'The Wall, a capital, and our own people',
        'The Wall cut Ramallah off from Jerusalem, and the road south now ends at the checkpoint of <b>Qalandiya</b>. '
        'The International Court of Justice found the Wall contrary to international law on 9 July 2004. '
        'Around the town stand <b>26 settlements</b> with nearly <b>150,000 settlers</b>; Beit El and Psagot are built on the land of al-Bīra, some of it owned by Palestinian-Americans{}. '
        'The town became a capital without a state. In 2005 it elected <b>Janet Mikhail</b>, its first woman mayor{}. '
        'It buried <b>Maḥmūd Darwīsh</b> on 13 August 2008, in a grave that “faces the outskirts of Jerusalem”{}. '
        'The occupation reached the diaspora too. <b>ʿUmar Asʿad</b>, seventy-eight, of Jiljilyā and Milwaukee, died in January 2022 after soldiers left him bound and blindfolded{}. '
        '<b>Sayfollah Musallet</b>, twenty, of Tampa, was beaten to death by settlers at Sinjil on 11 July 2025{}. '
        'In 2025 the United Nations counted 1,680 settler attacks in the West Bank, “an average of five incidents per day”{}.'.format(
            c('PLO Negotiations Affairs Department, “Israeli Settlements in the Ramallah &amp; Al-Bireh Governorate,” 26 March 2023; '
              'International Court of Justice, advisory opinion of 9 July 2004.'),
            c(CENT + '.'), c('Al Jazeera, 13 August 2008.'), c('Al Jazeera, 16 August 2024.'),
            c('ABC News, 12 July 2025.'),
            c('United Nations OCHA, <i>Humanitarian Situation Update #346, West Bank</i>, 4 December 2025.')),
        plate('p343_3.jpg', 342, 'The Khalil Sakakini Cultural Centre, founded in 1996 in a house of 1927 once owned by Khalīl Ṣalāḥ, mayor from 1947 to 1951.')
        + _rec(['9 July 2004: the International Court of Justice on the Wall.',
                '22 September 2024: the Al Jazeera office in Ramallah raided and closed for 45 days (Anadolu Agency).',
                '2023: 26 settlements and about 150,000 settlers in Ramallah and al-Bīra governorate (PLO Negotiations Affairs Department).'])
        + _p('<b>What we still don’t know.</b> The town’s own record of the first intifada, its dead, its prisoners and its popular committees, has not been gathered.'))

    insert_after('The city, counted', [june, int1, int2, wall])
    g['_check_eras']()


CSS = """
/* v83: the museum panels (src/modern.py) */
.record{margin:14px 0 16px;padding:10px 14px 8px;background:#F7F2E8;border-top:2px solid #007A3D;font-size:.88rem;line-height:1.4;break-inside:avoid}
.record .rk{font-variant:small-caps;text-transform:lowercase;letter-spacing:.16em;color:#007A3D;font-size:.8rem;margin:0 0 5px}
.record ul{margin:0;padding:0;list-style:none}
.record li{margin:0 0 4px;padding-left:14px;text-indent:-14px}
.record li::before{content:"·";color:#9A6324;font-weight:700;display:inline-block;width:14px;text-indent:0}
.testimony{margin:14px 0 14px 18px;padding:2px 0 2px 16px;border-left:2px solid #9A6324;background:none;font-style:italic;break-inside:avoid}
.testimony p{margin:0 0 4px;text-indent:0!important}
.testimony .tw{display:block;font-style:normal;font-size:.86rem;color:#77726A}
"""


def finish(html):
    """The panels' style."""
    return html.replace('</style>', CSS + '</style>', 1)
