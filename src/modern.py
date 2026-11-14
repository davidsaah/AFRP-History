# -*- coding: utf-8 -*-
"""v83: Ramallah from 1914 to today, set out as a Palestinian history museum would.

David, 14 Nov 2026: "Let's make the more recent history more enriched and include what
happened in Ramallah during all the wars ... the intifadas, the occupation. All the up
today ... in a way that you would see recorded in a Palestinian history museum with facts
and records and a Palestinian narrative." Option C of the plan of 14 November.

This module holds all of the new text, so the book source changes in two lines only:

    build_v5.py, before render():          import modern; modern.apply(globals())
    build_v5.py, before the page is saved:  html = modern.finish(html)

What it does:
  * Chapter 12 becomes "Under occupation, 1967–1987"; a new Chapter 13 runs from the first
    intifada to today; a new section, "The record", sets the dates from 1914 to 2025 on
    one wall; the closing moves to the end.
  * New story entries for 1920–1927, the Second World War, 1947–48, the Jordanian years,
    June 1967, the 1970s, the first intifada, Oslo, the second intifada, the Wall and the
    settlements, the capital years and 2022–2025.
  * Each new entry is built like a museum room: the story; "The record", a panel of the
    documents and numbers; a testimony from a published Palestinian source; and the
    photographs. Only images AFRP holds are printed (Naseeb Shaheen's collection).
    Library of Congress and permission-needed items are listed in docs/MODERN_IMAGES.md.

Sources: Palestinian and Arab first. United Nations and press reports are cited for dates
and counts. No Israeli author is relied on; where an Israeli state record is cited it says so.
Inferences are marked as such.
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
    """The record: a quiet panel of documents and numbers."""
    return ('<div class="record"><div class="rk">The record</div><ul>'
            + ''.join('<li>%s</li>' % x for x in items) + '</ul></div>')


def _testimony(words, who):
    return ('<blockquote class="testimony"><p>%s</p><span class="tw">%s</span></blockquote>' % (words, who))


def _p(t):
    return '<p>' + t + '</p>'


# ---------------------------------------------------------------------------
# chapters
CH12 = (12, 'CHAPTER TWELVE', 'Under occupation &middot; 1967–1987',
        'The army takes the town in June 1967. The town is counted under curfew, its mayors are deported or bombed, '
        'and its people answer from both sides of an ocean.')
CH13 = (13, 'CHAPTER THIRTEEN', 'Two uprisings and a capital &middot; 1987 to today',
        'The first intifada, the Authority, the second intifada and the siege, the Wall and the settlements, '
        'and a town that became a capital without a state.')
REC = (14, 'THE RECORD', 'Ramallah on one wall &middot; 1914 to today',
       'The dates of this town’s modern history, from the Ottoman call-up to the end of 2025, '
       'each with the source that carries it.')


def apply(g):
    """Add the modern history to the book. g is build_v5's globals()."""
    E, c, _plate = g['E'], g['c'], g['_plate']
    RIGHTS = g['RIGHTS']

    def plate(fn, pg, cap, kind='Photograph', made=None):
        if made:
            g['PIC_DATES'][fn] = (0, made)
        return _plate(fn, '../img/shaheen/' + fn, cap, '%s, p. %s. %s' % (SH, pg, RIGHTS['afrp']), kind)

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

    # -- the closing moves to the end; the new chapter and the record come before it
    E[:] = [x[:1] + (15,) + x[2:] if x[1] == 13 else x for x in E]
    chs = [t for t in g['CHAPTERS'] if t[0] not in (12, 13)]
    closing = [t for t in g['CHAPTERS'] if t[0] == 13][0]
    g['CHAPTERS'][:] = chs + [CH12, CH13, REC, (15,) + closing[1:]]
    g['ERA_YEARS'][12] = (1967, 1987)
    g['ERA_YEARS'][13] = (1987, 2100)
    L = g['LINKAT']
    L[15] = L.pop(13)
    L[13] = ('Link nine of nine &middot; to this morning',
             'Documented to the present, in censuses, in the town’s own papers and in living memory.', 'documents', 7)
    g['SCHOLARS']['13'] = [
        {'who': 'Lisa Taraki — “Enclave Micropolis: The Paradoxical Case of Ramallah/al-Bireh”',
         'pub': '<em>Journal of Palestine Studies</em> 37:4 (2008), 6–20',
         'line': 'A Birzeit sociologist on the town that became a capital: its merchants, its camps, its new middle class and its walls.'},
        {'who': 'Institute for Palestine Studies — <em>Palestine Chronology</em>',
         'pub': 'chronology.palestine-studies.org · day by day from 1987',
         'line': 'The dated record of the intifadas, the Authority’s arrival and the sieges of the town.'},
        {'who': 'Birzeit University — “History of Birzeit University”',
         'pub': 'pas.birzeit.edu',
         'line': 'Fifteen closures by military order, the underground classes, and the president deported.'},
    ]

    # =======================================================================
    # CHAPTER 10: the Mandate
    add_body('The war, the locusts', plate('p372_1.jpg', 371,
        'A letter from Ibrāhīm Dāʾūd Ḥarb to his son Wadīʿ, written on 16 December 1916, in the middle of the war, '
        'from Burqīn near Jenin.', 'Document'))

    snow = ent(10, '1920 · 1927', 'Snow, then the earth shakes',
        'On <b>9 February 1920</b> snow began to fall on Ramallah and did not stop for seventy-two hours. It lay up to a metre and a quarter deep. '
        'It broke olive trees and pines, and the road to Jerusalem was closed for a week. The water it left in the ground, Cadora says, gave an excellent harvest in 1921{}. '
        'On <b>11 July 1927</b> the great earthquake struck Palestine. In Ramallah, Shāhīn records, <b>two people were killed</b>, and the damage to property was heavy. '
        'Many houses were broken, above all in the old town, and most people slept that night in the open{}.'.format(
            c(CAD + ', p. 55 (the snow, “for 72 hours non-stop,” up to 1¼ metres) and p. 56 (the harvest of 1921).'),
            c(SHAHIN + ', English section, chronology, p. 75: “Only two inhabitants of Ramallah killed, but property damage heavy”; ' + SH + ', p. 34. '
              + CAD + ', p. 56, for the old town and the night in the open.')),
        _p('<b>After the earthquake.</b> Help came from the Latin Patriarchate of Jerusalem. The Catholic church paid for those who had lost their houses, '
           'and the Patriarch built a row of shops around the church, which widened the town’s market. Cadora adds that they were rebuilt in the modern style in 1953{}.'.format(
               c(CAD + ', p. 56.')))
        + _rec(['9–11 February 1920: seventy-two hours of snow, up to 1¼ m deep; the Jerusalem road closed for a week (Cadora).',
                '11 July 1927: two dead in Ramallah; heavy damage to property (Shāhīn).',
                '1935: electric street lighting for Ramallah and al-Bīra, inaugurated at al-Manāra (Cadora, p. 56).'])
        + _p('<b>What we still don’t know.</b> We have found nothing written about Ramallah in the troubles of August 1929. '
             'The Jerusalem newspapers of that month, which are digitised, are the place to look.'))
    insert_after('The war, the locusts', [snow])

    add_body('The revolt reaches the town', plate('p060_1.jpg', 59,
        'Dr Daoud Mikhail of the ʿAwwād clan in the dress of the countryside, during the uprising of 1936.', 'Portrait'))

    ww2 = ent(10, '1939–1945', 'The Second World War',
        'The war of 1939 reached Ramallah through its young men and its wireless. Some served with the British. '
        '<b>Elias Nasrallah Oudeh</b> enlisted in the Trans-Jordan Frontier Force, the British-commanded frontier cavalry, on 4 October 1938, '
        'and served as a wireless operator until 27 December 1943. His discharge certificate survives, and so does his photograph on horseback{}. '
        '<b>Shukri Elias ʿAjlouny</b> was a telegraph operator for the British at the airport of Lydda in 1940{}. '
        'Others served from the far side of the ocean: <b>Edward Salamy</b> of Ramallah wore the uniform of the United States army{}. '
        'At home the district was run by Palestinian officers of the Mandate government: Mitri Farraj until 1941, then, from 1943, the historian ʿĀrif al-ʿĀrif{}.'.format(
            c(SH + ', p. 282: the Frontier Force photographs and Elias Nasrallah’s certificate of discharge (serial no. 3904; “W/T operator”; enlisted 4 October 1938, discharged 27 December 1943, “termination of contract”).'),
            c(SH + ', p. 275.'),
            c(SH + ', p. 92.'),
            c(CAD + ', p. 55.')),
        plate('p283_1.jpg', 282, 'Men of the Trans-Jordan Frontier Force in the 1930s. The force served across the Jordan under British command, and men of Ramallah served in it.')
        + plate('p283_3.jpg', 282, 'The certificate of discharge of Corporal Elias Nasrallah Oudeh, wireless operator of the Trans-Jordan Frontier Force, '
                'enlisted 4 October 1938 and discharged 27 December 1943, beside his photograph on horseback.', 'Document')
        + _rec(['Certificate of discharge, Trans-Jordan Frontier Force, serial no. 3904, Corporal Elias Nasrallah Oudeh: '
                'enlisted 4 October 1938, discharged 27 December 1943 (Shaheen 2005, p. 282).',
                '24 August 1939: the radio station, the police and the army post at Ramallah attacked again (Totah’s diary, in the entry on 1938 above).'])
        + _p('<b>What we still don’t know.</b> How many men of Ramallah served in the war, and on which side of the ocean, has never been counted. '
             'Khalil Totah’s diary runs on into the war years and has not yet been read for them.'))
    insert_after('The revolt reaches the town', [ww2])

    # =======================================================================
    # CHAPTER 11: 1948 and the Jordanian years
    guard = ent(11, 'November 1947 – May 1948', 'The town guards itself',
        'When the United Nations voted in November 1947 to divide Palestine, the people of Ramallah, al-Bīra and Baytūniyā marched in '
        '“popular and peaceful demonstrations” against the British Mandate, the United Nations and the United States, as people did all over Palestine{}. '
        'Then the young men of the town organised. A committee of the municipality, <b>one member for each clan</b>, raised a tax and bought rifles and grenades. '
        'They built roadblocks and watchtowers outside the town and kept them day and night. Many had served in the Allied armies. '
        'Dr <b>Jalīl Badrān</b> was elected their head, with Salīm Elias ʿAudeh as his deputy. '
        'On <b>14 March 1948</b> they beat off an attack on the Ramallah–Ramle bus, and they fought beside the Palestinian fighters on the Jerusalem and Jaffa roads, at al-Qasṭal among other places{}.'.format(
            c(CAD + ', p. 57.'), c(CAD + ', p. 58.')),
        _p('<b>The spring of 1948, as the acting mayor wrote it down.</b> Yūsuf Qaddūra was acting mayor from 1 April 1948, and he kept a chronicle. '
           'On 18 April armed men at Nabī Yaʿqūb, on the Jerusalem road, shot and killed several young men of the district who worked in Jerusalem. '
           'On 22 April five hundred Syrian volunteers of the Arab Liberation Army arrived. '
           'The people of Bīr Nabālā and Bayt Maḥsīr came to Ramallah after their villages were attacked, and from 26 April the people of Jaffa came too. '
           '“Churches and schools opened their doors to give them refuge and shelter.” '
           'On 2 May, the Orthodox Easter, the Holy Light was carried up from the Sepulchre by the Arab army, “a quiet and somber celebration.” '
           'On 15 May, at almost noon, the Arab Legion drove into the town from Nablus, and the crowds lined both sides of the street{}.'.format(
               c(CAD + ', pp. 58–59. Cadora was acting mayor while Khalīl Ṣalāḥ was away.')))
        + _testimony('What a wonderful hour that was when the Ramallah citizens called on God as the Arab army entered the town! '
                     'Fear dissipated, hope increased and souls felt at ease.',
                     'Yūsuf Qaddūra, acting mayor, on 15 May 1948 (Cadora, p. 59)')
        + plate('p298_2.jpg', 297, 'A Ramallah family in 1947, before the war.')
        + plate('p380_1.jpg', 379, 'The permanent permit of Harb Harb of Ramallah, clerk in the Port Manager’s office, to enter the port of Haifa, '
                'issued on 19 April 1948, three days before Haifa fell. Below it, the notice of his rise in salary of October 1947.', 'Document')
        + _rec(['14 March 1948: an attack on the Ramallah–Ramle bus beaten off by the town guard (Cadora, p. 58).',
                '18 April 1948: young men of the district who worked in Jerusalem shot dead at Nabī Yaʿqūb (Cadora, p. 58).',
                '19 April 1948: Harb Harb’s permit to enter the port of Haifa (Shaheen 2005, p. 379).',
                '26 April 1948: the people of Jaffa begin to arrive (Cadora, p. 58).',
                '15 May 1948: the Arab Legion enters Ramallah (Cadora, p. 59).']))
    insert_before('The catastrophe of 1948', [guard])

    add_body('Where the refugees lived',
        plate('p186_1.jpg', 185, 'Refugee children being fed, probably near Ramallah. The back of the print is stamped 9 April 1949.')
        + plate('p185_2.jpg', 184, '“Refugee School at Ramallah Friends Meetinghouse,” August 1949, as written on the back of the print.')
        + plate('p184_1.jpg', 183, '“Refugee home in camp near Ramallah. This family has a very neat tent and have made stair-steps from the ‘street’ from flat stones.”')
        + plate('p183_3.jpg', 182, '“A refugee store in a camp near Ramallah. The wares are displayed in wooden boxes: soap, matches, thread, kerosene.” '
                'The living quarters were a United Nations tent next door. Received by the Friends in August 1950.'))

    jordan = ent(11, '1949–1966', 'Under the Jordanian crown',
        'From 1950 Ramallah was a town of the Hashemite Kingdom of Jordan, and from 1954 its people were Jordanian citizens and Palestinians at once. '
        'The kingdom gave them a vote and a parliament, and it watched them. On 21 May 1950 the Minister of Education ordered the Christian schools to open on Sundays. '
        'Delegations from Jerusalem, Bethlehem, Ramallah and Bayt Jālā reminded the government of the covenant of the Caliph ʿUmar, and the order was withdrawn. '
        'On 11 May 1951 the leaders of the Labour Party in Ramallah and its district were arrested, accused of communism and jailed in Amman, and the party was dissolved{}. '
        'Dr <b>Daoud Mikhail</b> of the ʿAwwād clan was jailed in 1957 for the National Socialist Party; its sign had hung on his house on the main street. '
        'Many years later his daughter, Dr Hanan Mikhail ʿAshrawi, reminded King Hussein that he had once put her father in prison{}.'.format(
            c(CAD + ', p. 62.'), c(SH + ', p. 54.')),
        _p('<b>1952.</b> “The economic situation in Palestine worsened and life became unbearable,” Cadora writes, and the educated left for the Arab countries and the town’s families for America. '
           'In March 1952 the old Orthodox church of 1807 was pulled down to make a square{}. '
           'Ḥannā Khalaf of Ramallah sat in the Jordanian parliament, and in 1961 he is photographed on his feet in the chamber{}.'.format(
               c(CAD + ', p. 63.'), c(SH + ', p. 44.')))
        + plate('p228_2.jpg', 227, 'Crowds round al-Manāra in the 1950s, with Jordanian policemen among them. The occasion is not known.')
        + plate('p045_3.jpg', 44, 'Ḥannā Khalaf addressing the Parliament of Jordan, 1961.')
        + plate('p333_3.jpg', 332, 'Arbor Day in Ramallah, about 1963. Mayor Boulos Saba, right, and the Governor of the West Bank from Amman plant a tree in the Municipal Park.')
        + plate('p337_2.jpg', 336, 'The Jordanian army band marches round al-Manāra and its five lion heads, probably in the 1960s.')
        + _rec(['21 May 1950: the order to open Christian schools on Sundays, withdrawn (Cadora, p. 62).',
                '11 May 1951: the Labour Party leaders of Ramallah arrested and the party dissolved (Cadora, p. 62).',
                '16 October 1951: Dr Jalīl Badrān appointed mayor (Cadora, p. 63).',
                '1957: Dr Daoud Mikhail imprisoned for the National Socialist Party (Shaheen 2005, p. 54).',
                '18 November 1961: Jordan’s census counts 14,759 people in Ramallah (in the chapter that follows).'])
        + _p('<b>What we still don’t know.</b> We have not yet found what Ramallah did in the Suez war of 1956, or in the protests that followed the Israeli raid on al-Samūʿ in November 1966. '
             'The Jerusalem newspaper <i>Filasṭīn</i> of those weeks is the place to look.'))
    insert_after('Where the refugees lived', [jordan])

    # =======================================================================
    # CHAPTER 12: under occupation, 1967–1987
    june = ent(12, 'June 1967', 'The June war, and the first days of occupation',
        'On <b>6 June 1967</b>, the second day of the war, the Israeli army took Ramallah{}. '
        'The first orders came at once. Every weapon in the town was to be handed in at al-Manāra, on pain of a search of every house. '
        'People who had worked with the Palestinian organisations were arrested, and some were expelled. '
        'The army redrew the West Bank into districts and made <b>Bayt Īl</b>, Beit El, on the Nablus road, the seat of its command. '
        'It took Arab-owned houses at ʿAyn Miṣbāḥ for its offices{}. '
        'Families driven out of ʿImwās, Yālū and Bayt Nūbā, the Latrun villages that the army emptied and destroyed, found shelter in a school at Baytūniyā and in Ramallah{}.'.format(
            c('Applied Research Institute–Jerusalem (ARIJ), <i>Atlas 40</i>, ch. 1.3: “Israel captured Qalqilia, Jenin, and Ramallah in the West Bank” on 6 June 1967.'),
            c(FARHAN + ', pp. 79 and 100–101 (page numbers of the OCR text).'),
            c('al-Haq, field report on the Latrun villages, 13 June 2013, alhaq.org/monitoring-documentation/6744.html. al-Haq is a Palestinian human-rights organisation founded in Ramallah in 1979.')),
        _p('Farḥān writes that the town and its district, being the most exposed to the occupation, were the first to stand against what it brought: '
           'settlement, the taking of land, taxes, killings, demolitions, prison, fines and deportation{}. '
           'The feasts went quiet. “Since the Israeli occupation in 1967,” Shāhīn wrote of the town’s great festival, “it is celebrated in a subdued manner … '
           'all large festivities, both Muslim and Christian, have ceased{}.” The Women’s Union fed the children of needy refugees through these years.'.format(
               c(FARHAN + ', p. 101.'), c(SHAHIN + ', English section, pp. 63–64.')))
        + plate('p162_1.jpg', 161, 'Feeding the children of needy refugees after the 1967 war, late 1960s. Standing on the left are Ellen ʿAkel and Ziadeh Shamieh.')
        + _rec(['6 June 1967: Ramallah taken (ARIJ).',
                '21 September 1967: the town counted under curfew; everyone abroad that day lost the right to return (in the entry above).',
                '1 October 1969: Mayor Nadīm Zarū arrested, and expelled six days later (in the entry above).']))
    insert_after('The city, counted', [june])

    mayor = ent(12, '1973–1982', 'Deported at night, welcomed in Houston',
        'Through the 1970s the occupation emptied the town of the people it feared. Dr <b>Alfred Toubassi</b>, a dentist of Jaffa who had settled in Ramallah, '
        'was deported in 1974: he was taken to the border with Lebanon in the middle of the night and sent across. '
        'The president of Birzeit University, Dr <b>Ḥannā Nāṣir</b>, was deported too, and spent nineteen years in exile{}. '
        'Shaheen, who lived through it, calls the midnight deportations what they were under the Fourth Geneva Convention: a breach of it, used “as a method of intimidation”{}. '
        'From 1978 the occupation set up the <b>Village Leagues</b>, councils of its own choosing to stand against the elected mayors, and their centre was at Ramallah{}.'.format(
            c(SH + ', p. 55; ' + BZU + '.'), c(SH + ', p. 55.'), c(FARHAN + ', p. 102.')),
        _p('The mayor the town had elected, <b>Karīm Khalaf</b>, belonged to both of its halves. In 1973 he handed the diplomas to the graduates of the Boys’ Secondary School '
           'in the Khalil Totah hall of the Friends school. In July 1974 he flew to the Federation’s convention in Houston, and stood for a photograph with every president the Federation had had{}. '
           'Six years later a settler bomb took his leg, and in 1982 the occupation removed him from office.'.format(c(SH + ', pp. 339, 341 and 357.')))
        + plate('p340_1.jpg', 339, 'Mayor Karīm Khalaf gives the high-school diploma to ʿIsa Marshoud Zayed, Boys’ Secondary School, 1973. On the far right is ʿAdel Madi, the principal.')
        + plate('p340_2.jpg', 339, 'The audience at that 1973 graduation, in the Khalil Totah Auditorium. Mayor Khalaf sits sixth from the left in the front row.')
        + plate('p342_1.jpg', 341, 'At a Ramallah convention in America, probably Houston, July 1974: Mayor Karīm Khalaf and his wife on the right.')
        + plate('p358_2.jpg', 357, 'Houston, 1974: Mayor Karīm Khalaf with the Federation’s president, George Mogannam, its deputy, Salim ʿIqal, and all its past presidents.')
        + _rec(['1974: Dr Alfred Toubassi deported to Lebanon at night (Shaheen 2005, p. 55).',
                '1974: Dr Ḥannā Nāṣir, president of Birzeit University, deported; nineteen years in exile (Birzeit University).',
                'July 1974: Mayor Karīm Khalaf at the Federation’s convention in Houston (Shaheen 2005, p. 357).',
                '2 June 1980: Khalaf maimed by a car bomb (in the entry above).']))
    insert_after('The June war', [mayor])

    # =======================================================================
    # CHAPTER 13: two uprisings and a capital
    sec13 = ('s', 13, 'The story', '')
    int1 = ent(13, '1987–1993', 'The first intifada',
        'In December 1987 the uprising began, and Ramallah was one of its centres{}. '
        'Its weapons were the strike, the boycott and the stone. The shops kept the hours the leaflets set, and the town’s merchants carried food to the camps. '
        'Lisa Taraki of Birzeit writes that in the long sieges “the towns’ prosperous merchants … paid their political dues by supplying the camp [al-Amʿarī] with food and provisions,” '
        'and that the villages around did the same for al-Jalazūn{}. '
        'The university paid with its doors. Birzeit was closed by military order for the fifteenth and last time on <b>8 January 1988</b>, and it stayed shut until <b>29 April 1992</b>. '
        'Its teachers held classes underground, in small groups, in houses and offices in Ramallah{}.'.format(
            c(CENT + ': “1987 the first intifada against the Israeli occupation.”'),
            c(TARAKI + ', p. 16.'),
            c(BZU + '; ' + IPS + ', 20 April 1992, for the order to reopen.')),
        _rec(['8 January 1988 – 29 April 1992: Birzeit University closed by military order, its fifteenth closure (Birzeit University).',
              '1988: a one-day strike at al-Mazraʿa al-Sharqiyya, photographed for the Palestinian Museum’s archive (item 0006.02.0093).'])
        + _p('<b>What we still don’t know.</b> The town’s own record of the first intifada has not been gathered: its dead, its prisoners, the tax raids and the popular committees. '
             'The reports al-Haq published from Ramallah in those years, and the oral histories already recorded in the district, are the place to begin.'))

    oslo = ent(13, '1993–2000', 'The Authority comes to Ramallah',
        'After the Oslo agreements the Israeli army withdrew from the town, and on <b>27 December 1995</b> the Palestinian Authority took control of Ramallah and al-Bīra{}. '
        'In 1996 the first council appointed by the Authority took office under Dr ʿĪsā Ziyāda{}. '
        'Jerusalem, a few kilometres south, was being closed off, and Ramallah took over its work. The ministries, the parties, the banks and the foundations moved in. '
        'Taraki calls the result a new middle-class city, and quotes the name its people gave it: “a ‘five-star prison’”{}. '
        'The town built for itself. The Khalil Sakakini Cultural Centre opened in 1996 in a house of 1927 that had been the home of Mayor Khalīl Ṣalāḥ. '
        'In May 1999 the first heart catheterisation under the Authority was carried out at the Ramallah government hospital, by a Palestinian team led by Dr Niḍāl Ḥarb, who had come home after twenty-five years in America{}.'.format(
            c(IPS + ', 27 December 1995: “PA assumes control of Ramallah, al-Bireh.”'),
            c(CENT + '.'),
            c(TARAKI + ', pp. 6–8.'),
            c(SH + ', p. 342 (the Sakakini Centre) and p. 120, with the report from <i>al-Ayyām</i>, 24 May 1999: '
              '<span class="ar" dir="rtl">اجراء أول عملية قسطرة للقلب في مستشفى رام الله الحكومي</span>, “the first heart catheterisation at the Ramallah government hospital,” '
              'on a patient of seventy-two, with equipment paid for by Belgium. <i>al-Ayyām</i> is a Ramallah daily.')),
        plate('p343_3.jpg', 342, 'The Khalil Sakakini Cultural Centre, founded in 1996 in a restored house of 1927 once owned by Khalīl Ṣalāḥ, mayor of Ramallah from 1947 to 1951.')
        + plate('p121_1.jpg', 120, '<i>al-Ayyām</i>, 24 May 1999: “The first heart catheterisation in the Ramallah government hospital.” The team was led by Dr Niḍāl Ḥarb.', 'Newspaper')
        + _rec(['27 December 1995: the Palestinian Authority takes control of Ramallah and al-Bīra (IPS).',
                '1996: the first council appointed by the Authority, under Dr ʿĪsā Ziyāda (the municipality).',
                'May 1999: the first heart catheterisation at the Ramallah government hospital (<i>al-Ayyām</i>).']))

    int2 = ent(13, '2000–2004', 'The second intifada and the siege',
        'On <b>12 October 2000</b>, two weeks into the second intifada, after two Israeli reservists were killed in the town, Israel bombed Ramallah from the air. '
        'The targets were Arafat’s headquarters, the Palestinian broadcasting centre and the police stations{}. '
        'From December 2001 Arafat was held inside the Muqāṭaʿa{}. On <b>29 March 2002</b> the army invaded the town in the operation it called “Defensive Shield”{}. '
        'Some forty thousand people were put under curfew, with water and power cut. By 3 April at least fifty-four Palestinians had been killed, by the count of the Palestinian Centre for Human Rights, '
        'and twenty-three of them were buried together in the car park of the Ramallah hospital because the dead could not be carried to the cemeteries. About a thousand men were arrested{}.'.format(
            c(IPS + ', 12 October 2000.'),
            c('Charmaine Seitz, “In Ramallah, Grueling Reoccupation Grinds On,” <i>Middle East Report Online</i>, 5 April 2002.'),
            c('United Nations, Report of the Secretary-General prepared pursuant to General Assembly resolution ES-10/10, A/ES-10/186, 30 July 2002: the operation “began on 29 March with an incursion into Ramallah.”'),
            c('Seitz (2002), for the curfew, the count of the Palestinian Centre for Human Rights to 3 April, the burial in the hospital car park and the arrests.')),
        _testimony('We have two kilos of rice and we have to make it last for the four of us.',
                   'A Ramallah household under curfew, April 2002 (Seitz, <i>Middle East Report Online</i>)')
        + _p('The United Nations found “extensive physical damage” to the civilian offices of the Authority in Ramallah and the “destruction of office equipment, such as computers and photocopying machines,” '
             'and recorded that the army “admitted that its personnel engaged in some acts of vandalism{}.” '
             'In September 2002 the army returned and pulled down the buildings of the Muqāṭaʿa around Arafat; the men inside did not leave{}. '
             'Yasser Arafat died in Paris on <b>11 November 2004</b>, and the next day he was buried in the Muqāṭaʿa, in Ramallah.'.format(
                 c('A/ES-10/186 (2002), on Ramallah.'), c(IPS + ', 21 September 2002.')))
        + _rec(['12 October 2000: air strikes on Ramallah (IPS).',
                '29 March 2002: the invasion of Ramallah begins (United Nations, A/ES-10/186).',
                'To 3 April 2002: at least 54 Palestinians killed; 23 buried in the hospital car park (PCHR, in Seitz).',
                'September 2002: the Muqāṭaʿa demolished around Arafat (IPS).',
                '12 November 2004: Arafat buried in the Muqāṭaʿa.']))

    wall = ent(13, '2002 to today', 'The Wall, the checkpoint and the settlements',
        'The Wall that Israel began to build in 2002 cut Ramallah off from Jerusalem. '
        'On 9 July 2004 the International Court of Justice gave its opinion that the Wall, where it runs inside the occupied territory, is contrary to international law. '
        'The road south now ends at <b>Qalandiya</b>, the checkpoint that is the southern gate of the town. '
        'The town itself is Area A, under the Authority. Most of the land of its villages is Area B or Area C, and Area C is under the army. '
        'Around the town stand <b>26 settlements</b> with nearly <b>150,000 settlers</b>. Beit El is built mainly on land owned by people of al-Bīra, and Psagot on al-Bīra’s land, '
        'including land owned by Palestinian-Americans{}. '
        'In the village of Bilʿīn, west of the town, the people stood against the Wall, and the village became, in Taraki’s words, an “arena of confrontation and resistance”{}.'.format(
            c('PLO Negotiations Affairs Department, “Israeli Settlements in the Ramallah &amp; Al-Bireh Governorate,” 26 March 2023, nad.ps/en/node/74742; '
              'International Court of Justice, <i>Legal Consequences of the Construction of a Wall in the Occupied Palestinian Territory</i>, advisory opinion of 9 July 2004; '
              'ARIJ, <i>Ramallah Governorate Profile</i> (2015), for the areas.'),
            c(TARAKI + ', p. 8.')),
        _rec(['9 July 2004: the advisory opinion of the International Court of Justice on the Wall.',
              '2023: 26 settlements and nearly 150,000 settlers in and around Ramallah and al-Bīra governorate (PLO Negotiations Affairs Department).']))

    capital = ent(13, '2004–2018', 'A capital without a state',
        'After 2007 the Palestinian government sat in Ramallah, and the town was a capital in all but name{}. '
        'It chose its own council again in December 2005, and elected <b>Janet Mikhail</b>, the first woman to be its mayor, who served until 2012{}. '
        'It buried its poet. <b>Maḥmūd Darwīsh</b> died on 9 August 2008, and on 13 August he was buried in Ramallah, in a grave that “faces the outskirts of Jerusalem”{}. '
        'The Palestinian Museum opened at Birzeit on 18 May 2016, and the Yasser Arafat Museum beside his tomb on 9 November 2016{}.'.format(
            c(TARAKI + '.'), c(CENT + '.'),
            c('Al Jazeera, 13 August 2008.'),
            c('Al Jazeera, 18 May 2016 and 11 November 2016.')),
        _rec(['December 2005: municipal elections; Janet Mikhail, mayor 2005–2012 (the municipality).',
              '13 August 2008: Maḥmūd Darwīsh buried in Ramallah (Al Jazeera).',
              '18 May 2016: the Palestinian Museum opens at Birzeit (Al Jazeera).']))

    now = ent(13, '2022–2025', 'Our own people, and the years since October 2023',
        'The occupation reached the families of the diaspora too. <b>ʿUmar Asʿad</b>, seventy-eight, of Jiljilyā, who had lived for years in Milwaukee, '
        'was detained by soldiers at a checkpoint in his village in January 2022 and left bound and blindfolded. He died there. '
        'The Palestinian autopsy found a heart attack brought on by “the external violence he was exposed to”{}. '
        'On <b>11 July 2025</b> <b>Sayfollah Musallet</b>, twenty, of Tampa, Florida, visiting his family in al-Mazraʿa al-Sharqiyya, was beaten to death by settlers at Sinjil; '
        'Muḥammad al-Shalabī, twenty-three, was killed with him{}.'.format(
            c('Al Jazeera, 16 August 2024.'), c('ABC News, 12 July 2025; <i>The New Arab</i>.')),
        _p('After October 2023 the raids on the town and the attacks on its villages grew. On 22 September 2024 soldiers raided the Al Jazeera office in Ramallah and ordered it closed for forty-five days{}. '
           'In 2025 the United Nations counted 227 Palestinians killed in the West Bank and 1,680 settler attacks, “an average of five incidents per day.” '
           'In the governorate, the spring of ʿAyn Sāmiya, which serves “some 100,000 Palestinians in 20 villages,” had its pipes damaged on 30 November 2025, '
           'after the Bedouin families beside it had been driven out in May 2024; Rantis had seventeen settler attacks after an outpost was set up in September 2024; '
           'and on 1 December 2025 the offices of the Union of Agricultural Work Committees in al-Bīra were sealed{}.'.format(
               c('Anadolu Agency, 22 September 2024.'),
               c('United Nations OCHA, <i>Humanitarian Situation Update #346, West Bank</i>, 4 December 2025.')))
        + _rec(['January 2022: ʿUmar Asʿad, 78, of Jiljilyā and Milwaukee, dies after his detention by soldiers (Al Jazeera).',
                '22 September 2024: the Al Jazeera office in Ramallah raided and closed (Anadolu).',
                '11 July 2025: Sayfollah Musallet, 20, of Tampa, killed by settlers at Sinjil (ABC News).',
                '2025: 227 Palestinians killed and 1,680 settler attacks in the West Bank (OCHA, 4 December 2025).'])
        + _p('<b>What we still don’t know.</b> This chapter stops at the end of 2025. '
             'If your family has a name, a document or a photograph from these years that belongs here, please send it.'))

    # the entry "The city, counted to the present" keeps its 1987 square in chapter 12;
    # its 1997 view of the town goes with the Authority's years
    i = idx('The city, counted')
    m = re.search(r'<figure class="photo[^"]*"[^>]*><img src="[^"]*p343_2\.jpg".*?</figure>', E[i][7], flags=re.S)
    assert m, 'p343_2 plate not found'
    E[i] = E[i][:7] + (E[i][7][:m.start()] + E[i][7][m.end():],) + E[i][8:]
    oslo = oslo[:7] + (oslo[7] + m.group(0),)

    # chapter 13 sits after chapter 12's evidence, before the closing
    k = next(j for j, x in enumerate(E) if x[1] == 15)
    E[k:k] = [sec13, int1, oslo, int2, wall, capital, now, ent(14, '1914–2025', 'The dates, from the war to today', WALL_LEAD, wall_html())]

    g['_check_eras']()


# ---------------------------------------------------------------------------
# the record: one wall of dates, each with the source that carries it
WALL = [
 ('October 1914', 'Ottoman general mobilisation, the <i>seferberlik</i>; men of 18 to 45 called up or fined fifty gold pounds.', 'Cadora'),
 ('1916', 'Typhus. A grain depot and a garrison in the town.', 'Shāhīn; Cadora'),
 ('29 December 1917', 'The British army takes Ramallah.', 'British records'),
 ('9 February 1920', 'Seventy-two hours of snow.', 'Cadora'),
 ('11 July 1927', 'Earthquake: two dead in Ramallah.', 'Shāhīn'),
 ('1935', 'Electric light at al-Manāra.', 'Cadora'),
 ('30 March 1936', 'The Palestine Broadcasting Service opens its station near the town.', 'Library of Congress, Matson photographs; Cadora'),
 ('May 1936', 'The general strike; a joint committee of Ramallah and al-Bīra.', 'Totah; see Chapter 10'),
 ('25 September, 1 October 1938', 'Two battles in the town.', 'Totah; the Quaker letters; the British report'),
 ('1938–1943', 'Elias Nasrallah Oudeh in the Trans-Jordan Frontier Force.', 'Shaheen 2005'),
 ('15 April 1946', 'The town votes by clan.', 'Israel State Archives, P-213/40'),
 ('November 1947', 'Demonstrations against partition.', 'Cadora'),
 ('14 March 1948', 'The town guard beats off an attack on the Ramle bus.', 'Cadora'),
 ('15 May 1948', 'The Arab Legion enters Ramallah.', 'Cadora'),
 ('26–29 May 1948', 'Air raids on the town; a refugee from Ramle killed.', 'Cadora'),
 ('13 July 1948', 'The people of Lydda and Ramle driven out on foot towards Ramallah.', 'see Chapter 11'),
 ('March 1949', 'The Arab Refugee Congress of Ramallah counts 72,660 refugees.', 'the Congress'),
 ('April 1950', 'The West Bank annexed to Jordan.', 'see Chapter 11'),
 ('11 May 1951', 'The Labour Party leaders of Ramallah arrested.', 'Cadora'),
 ('1957', 'Dr Daoud Mikhail jailed for the National Socialist Party.', 'Shaheen 2005'),
 ('20 May 1963', 'The Ramallah New Hospital opens.', 'Shāhīn'),
 ('6 June 1967', 'The Israeli army takes Ramallah.', 'ARIJ'),
 ('21 September 1967', 'The town counted under curfew.', 'see Chapter 12'),
 ('October 1969', 'Mayor Nadīm Zarū expelled.', 'United Nations'),
 ('1974', 'Dr Alfred Toubassi and Dr Ḥannā Nāṣir deported.', 'Shaheen 2005; Birzeit'),
 ('2 June 1980', 'Mayor Karīm Khalaf maimed by a settler bomb.', 'United Nations, A/35/278'),
 ('1982', 'Khalaf removed; the Civil Administration rules the town.', 'see Chapter 12'),
 ('December 1987', 'The first intifada.', 'the municipality'),
 ('8 January 1988', 'Birzeit University closed for four years.', 'Birzeit University'),
 ('27 December 1995', 'The Palestinian Authority takes control of the town.', 'IPS'),
 ('1996', 'The Khalil Sakakini Cultural Centre opens.', 'Shaheen 2005'),
 ('12 October 2000', 'Air strikes on Ramallah.', 'IPS'),
 ('29 March 2002', 'The invasion of Ramallah; the siege of the Muqāṭaʿa.', 'United Nations'),
 ('9 July 2004', 'The International Court of Justice on the Wall.', 'ICJ'),
 ('12 November 2004', 'Yasser Arafat buried in Ramallah.', ''),
 ('December 2005', 'Municipal elections; Janet Mikhail mayor.', 'the municipality'),
 ('13 August 2008', 'Maḥmūd Darwīsh buried in Ramallah.', 'Al Jazeera'),
 ('18 May 2016', 'The Palestinian Museum opens at Birzeit.', 'Al Jazeera'),
 ('3 April 2017', 'The memorial to the founding family unveiled.', 'see Chapter 8'),
 ('January 2022', 'ʿUmar Asʿad of Jiljilyā and Milwaukee dies after his detention.', 'Al Jazeera'),
 ('22 September 2024', 'The Al Jazeera office in Ramallah closed by the army.', 'Anadolu'),
 ('11 July 2025', 'Sayfollah Musallet of Tampa killed by settlers at Sinjil.', 'ABC News'),
 ('4 December 2025', 'The United Nations counts 1,680 settler attacks in the West Bank this year.', 'OCHA'),
]
WALL_LEAD = ('A museum puts the dates on one wall so that a visitor can stand back and see the whole of it. '
             'This is that wall for Ramallah from 1914 to the end of 2025. Every line is told, with its notes, in the chapters before.')


def wall_html():
    rows = ''.join('<li><span class="wd">%s</span><span class="wt">%s%s</span></li>'
                   % (d, t, ' <span class="ws">%s</span>' % s if s else '') for d, t, s in WALL)
    return '<div class="wall"><ol>%s</ol></div>' % rows


CSS = """
/* v83: the museum panels (src/modern.py) */
.record{margin:16px 0 18px;padding:12px 16px 10px;background:#F7F2E8;border-top:2px solid #007A3D;font-size:.9rem;line-height:1.45;break-inside:avoid}
.record .rk{font-variant:small-caps;text-transform:lowercase;letter-spacing:.16em;color:#007A3D;font-size:.82rem;margin:0 0 6px}
.record ul{margin:0;padding:0;list-style:none}
.record li{margin:0 0 5px;padding-left:14px;text-indent:-14px}
.record li::before{content:"·";color:#9A6324;font-weight:700;display:inline-block;width:14px;text-indent:0}
.testimony{margin:16px 0 16px 18px;padding:2px 0 2px 16px;border-left:2px solid #9A6324;background:none;font-style:italic;break-inside:avoid}
.testimony p{margin:0 0 4px;text-indent:0!important}
.testimony .tw{display:block;font-style:normal;font-size:.86rem;color:#77726A}
.wall ol{list-style:none;margin:8px 0 0;padding:0}
.wall li{display:flex;align-items:baseline;margin:0 0 6px;break-inside:avoid}
.wall .wd{flex:0 0 8.2em;text-align:right;color:#9A6324;font-variant-numeric:lining-nums;padding-right:10px;margin-right:12px;border-right:2px solid #007A3D;font-size:.92rem;line-height:1.4}
.wall .wt{flex:1;min-width:0;font-size:.95rem;line-height:1.4;text-align:left!important;hyphens:none}
.wall .ws{display:block;font-size:.8rem;color:#77726A;font-style:italic}
@media print{.record{font-size:9.4pt;padding:.08in .14in .06in}.testimony{margin-left:.12in}.wall li{margin-bottom:3pt}.wall .wd{font-size:9pt;flex-basis:1.15in}.wall .wt{font-size:9.6pt}}
"""


def finish(html):
    """Text that counts the chapters, and the panels' style."""
    for a, b in (('Our history is one timeline in twelve chapters.', 'Our history is one timeline in thirteen chapters.'),
                 ('Twelve chapters run from the first people on these hills to', 'Thirteen chapters run from the first people on these hills to')):
        assert a in html, a
        html = html.replace(a, b)
    return html.replace('</style>', CSS + '</style>', 1)
