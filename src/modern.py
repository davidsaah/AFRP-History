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
NIR = ('Ibrāhīm Nayrūz (Nirouz Ibrahim), <span class="ar">رام الله: جغرافيا، تاريخ، حضارة</span> '
       '(<i>Ram Allah: Geography, History, Civilization</i>; Ramallah: Dār al-Shurūq, 2004)')
BZU = 'Birzeit University, “History of Birzeit University,” pas.birzeit.edu/node/151'


def _rec(items):
    """The record: a compact panel of documents and dates."""
    return ('<div class="record"><div class="rk">The record</div><ul>'
            + ''.join('<li>%s</li>' % x for x in items) + '</ul></div>')


def _testimony(words, who):
    return '<blockquote class="testimony"><p>%s</p><span class="tw">%s</span></blockquote>' % (words, who)


def _p(t):
    return '<p>' + t + '</p>'


def _ctx(era, big, ground, why):
    """v98: a short 'what was happening' box for younger readers at the head of each conflict."""
    return ('<div class="ctxbox"><div class="ck">What was happening · %s</div>'
            '<p><b>The big picture.</b> %s</p><p><b>On the ground.</b> %s</p>'
            '<p><b>Why it still matters.</b> %s</p></div>') % (era, big, ground, why)


# (entry title prefix, paragraph start or None for the entry's opening, era, big picture, on the ground, why it matters)
CONTEXT_BOXES = [
    ('Magna Mahumeria', None, 'Crusaders and Mamluks, 1099–1516',
     'European armies, the Crusaders, took Jerusalem in 1099 and ruled much of the country for less than a century. Saladin won it back in 1187. From 1260 the Mamluks, soldier-sultans based in Cairo, ruled Palestine for over 250 years.',
     'The Crusaders built a town for European settlers at al-Bīra. Our hill was farmland given to a religious endowment; the Mamluk sultan Qalāwūn’s deed of 1279–80 already names Rām Allāh.',
     'Rulers came and went; the people of these hills stayed and farmed. The Crusaders were the one group that came and truly left.'),
    ('The registers begin', None, 'The Ottomans, 1516–1917',
     'The Ottoman Turks took Palestine from the Mamluks in 1516–17 and ruled it for four centuries from Istanbul. It was a distant empire that mostly wanted taxes and, later, soldiers.',
     'The Ottomans reached Ramallah through their tax registers, not their armies. Our families came up by way of Bayt Jālā and appear by name in 1562–63. The worst violence was local: the Qays–Yaman feuds, and the Egyptian occupation of 1831–40, which crushed the peasants’ revolt of 1834.',
     'The registers are why we can trace our families back 460 years.'),
    ('The war, the locusts', None, 'The First World War, 1914–1918',
     'The Ottomans joined Germany’s side. Britain invaded Palestine from Egypt. In 1917 Britain promised a “national home for the Jewish people” in Palestine, the Balfour Declaration, without asking the people who lived there.',
     'Men were drafted or hid in the wadis. Locusts and requisitions brought famine, and typhus followed: by Shaheen’s count about 30 per cent of the town died. For nine months the front line ran just north of Ramallah.',
     'Emigration to the Americas, already under way, became the town’s lifeline, and Balfour’s promise shaped the next century.'),
    ('Snow, then the earth shakes', None, 'British rule, 1917–1948',
     'Britain governed Palestine under a League of Nations mandate that wrote the Balfour promise into law. Jewish immigration from Europe grew fast, and land bought from absentee owners often meant Palestinian farmers were evicted. Palestinians protested in 1920, 1921 and 1929.',
     'Ramallah grew: schools, a municipality, the radio station of 1936. Emigrants abroad, some shut out by the citizenship rules of 1925, organised to defend Palestine from New York.',
     'The conflict over land and who decides Palestine’s future began here.'),
    ('The revolt reaches the town', None, 'The Great Revolt, 1936–1939',
     'Palestinians held a six-month general strike, then rose in armed revolt against British rule and mass immigration. Britain put it down with troops, curfews, collective fines, house demolitions, detention and executions. About 5,000 Palestinians were killed, and many leaders were exiled.',
     'Ramallah men joined the rebels; George Saah was hanged. In 1938 rebels took the police station, British planes bombed, and the town lived under curfew and checkpoints.',
     'Many of the methods used against Palestinians today were first used by the British in these years, and the revolt’s defeat left Palestinians disarmed for 1948.'),
    ('The Second World War', None, 'The Second World War, 1939–1945',
     'Britain fought Germany and Italy; Palestine was a British base. Rationing and shortages followed.',
     'Ration cards came through the municipality; Ramallah men served in British, American and Transjordanian uniforms; emigrants were stranded abroad.',
     'The war ended with Britain exhausted and the world sympathetic to the Jewish survivors of the Holocaust, which shaped what happened to Palestine next.'),
    ('The town guards itself', None, 'Partition and the Nakba, 1947–1949',
     'In November 1947 the UN voted to divide Palestine, giving more than half the land to a Jewish state when Jews were about a third of the population. War followed. About 750,000 Palestinians, more than half the Arab population, were driven out or fled and were never allowed back. More than 400 villages were emptied and most were destroyed. Palestinians call it the <b>Nakba</b>, the catastrophe.',
     'In July 1948 the people of Lydda and Ramle were forced out and walked to Ramallah in the summer heat. The town’s population tripled, and in 1949 the camps of al-Amʿarī, al-Jalazūn and Qalandiyā were set up.',
     'The refugees and their descendants, now millions, still hold the right of return. The Nakba is the event every later one refers back to.'),
    ('Under the Jordanian crown', None, 'Jordanian rule, 1948–1967',
     'Jordan took the West Bank in 1948 and annexed it in 1950. Palestinians became Jordanian citizens but political parties were suppressed. Israeli raids across the armistice line punished whole villages, at Qibya in 1953 and al-Samūʿ in 1966.',
     'Ramallah became a summer resort and a refugee town at once. Students marched against the Baghdad Pact; the army fired on protesters at al-Jalazūn in 1966.',
     'These were years of rebuilding, and of emigration: many families left for the Americas and the Gulf in this period.'),
    ('Occupation, and the mayor in Houston', None, 'The June War and the occupation, 1967',
     'In six days in June 1967 Israel took the West Bank, East Jerusalem, Gaza, the Golan and Sinai. About 300,000 more Palestinians were displaced. Palestinians call it the <b>Naksa</b>, the setback. Israel annexed East Jerusalem and put the West Bank under military rule. UN Security Council Resolution 242 called for Israel to withdraw.',
     'Ramallah fell on 6 June, after Israeli planes struck the town. Anyone abroad that September, many of our relatives among them, lost the right to live here and was treated as an “absentee.”',
     'The military occupation that began that week has now lasted almost sixty years, longer than most of our readers have been alive.'),
    ('Occupation, and the mayor in Houston', '1972–1973.', 'The resistance movements, 1967–1982',
     'After 1967 the Palestine Liberation Organisation, led by Fatah, became the voice of Palestinians. Its fighters, the <i>fidāʾiyyīn</i>, fought at Karameh in 1968, were expelled from Jordan in 1970–71 (Black September), and moved to Lebanon. In 1974 the Arab states and the UN recognised the PLO.',
     'Ramallah people were arrested, deported and sometimes killed; schools were closed in protest; in 1976 the town elected a nationalist council under Karīm Khalaf.',
     'Palestinians outside the country, our own diaspora included, became part of a national movement for the first time.'),
    ('Occupation, and the mayor in Houston', 'March 1982.', 'The 1980s: bombs, dismissals and appointed rulers',
     'Israel tried to replace the elected nationalist mayors with leaders it chose (the Village Leagues) and created a Civil Administration in 1981. In 1982 Israel invaded Lebanon to destroy the PLO; the PLO left for Tunis, and in September hundreds of refugees were massacred at Sabra and Shatila.',
     'In 1980 a settler car bomb cost Ramallah’s mayor Karīm Khalaf his leg. In 1982 he was dismissed and an Israeli officer ran the town hall; the Manāra column was taken down.',
     'The town’s own memory of these years, and its pride in rebuilding the Manāra, come from here.'),
    ('The first intifada, and the Authority', None, 'The first intifada, 1987–1993',
     'In December 1987 Palestinians in the West Bank and Gaza rose up together. It was mostly an unarmed uprising: strikes, boycotts of Israeli goods, refusing to pay taxes, stone-throwing, and neighbourhood committees that ran daily life. Israel answered with curfews, mass arrests, school closures and a “break their bones” policy. More than 1,000 Palestinians were killed.',
     'Ramallah was one of the uprising’s centres. On 10 January 1988 the army closed Birzeit with a phone call, without even a written order, '
     'and on 2 February it shut all 800 schools in the West Bank “until further notice.” Teaching at home was not allowed either. '
     'In October 1988 six families on one Ramallah street agreed to teach their children together. That same afternoon an army officer '
     'and soldiers came to the street, and the classes never began. The same week, soldiers told the Friends Boys School to stop sending '
     'homework home (Johnson, <i>Journal of Palestine Studies</i>, 1988 and 1989). In 1989–90 the Friends School met about 60 days instead of 165. '
     'Ramallah people in America raised more than $300,000 for families at home.',
     'The uprising put Palestinians back on the world’s map and led to the Oslo talks. Many of our readers’ parents lived through it as teenagers.'),
    ('The first intifada, and the Authority', 'The curfews.', 'The Gulf War, 1990–1991',
     'Iraq invaded Kuwait; a US-led coalition drove it out. The PLO’s stance cost Palestinians dearly: of the 350,000 to 400,000 Palestinians in Kuwait before the war, only 50,000 to 80,000 were left by the end of 1991 (Middle East Watch, <i>Nowhere to Go</i>, 1991).',
     'The West Bank was under round-the-clock curfew for weeks. Families who had worked in Kuwait for decades came back to Ramallah with nothing.',
     'It ended the Gulf as the safe second home many Ramallah families had relied on.'),
    ('The first intifada, and the Authority', '27 December 1995.', 'Oslo and the Palestinian Authority, 1993–2000',
     'In 1993 Israel and the PLO signed the Oslo Accords. A Palestinian Authority was set up to run the towns for five years while a final deal was negotiated. The West Bank was split into Areas A, B and C; Israel kept full control of Area C, about 60 per cent of the land. The final deal never came, and settlements kept growing throughout the Oslo years.',
     'The Israeli army left Ramallah on 27 December 1995. The town became the Authority’s seat and boomed with ministries, offices and returnees.',
     'The Ramallah of today, a capital in all but name surrounded by checkpoints, was made by Oslo.'),
    ('The second intifada and the siege', None, 'The second intifada, 2000–2005',
     'After the Camp David talks failed, Ariel Sharon’s visit to al-Aqṣā in September 2000 set off a second uprising, this time armed on both sides. Israel reoccupied the Palestinian cities in 2002 and began building the separation Wall; the International Court of Justice ruled in 2004 that the Wall breaks international law. More than 3,000 Palestinians were killed.',
     'In 2002 tanks occupied Ramallah for weeks; 21 offices of the Authority were wrecked and their records carried off, and Arafat was besieged in the Muqāṭaʿa. He died in 2004. Many families emigrated.',
     'The Wall, Qalandiyā checkpoint and the permit system our readers meet on every visit all date from these years.'),
    ('The Wall, a capital', None, 'The Wall, 2002 to today',
     'From 2002 Israel built a barrier of fences and 8-metre concrete walls. Israel called it security; but 85 per cent of its route runs inside the West Bank, not on the 1967 line, taking land, wells and villages. In 2004 the International Court of Justice ruled it illegal and said it must come down. It is still being built.',
     'Around Ramallah it runs about 89 km and cuts through 19 villages. Bilʿīn lost about 2,300 dunums and began weekly marches in 2005; two of its people were killed. Qalandiyā’s roadblock became a terminal. A short drive to Jerusalem can take hours, and farmers need permits to reach their own olive trees.',
     'The Wall decides who can pray in Jerusalem, marry across an ID line, or harvest a field. It is the grey line visitors photograph at Qalandiyā.'),
    ('The Wall, a capital', 'The land.', 'Settlements, 1967 to today',
     'Israel began building Jewish settlements in the occupied territories soon after 1967. International law, the Fourth Geneva Convention, forbids an occupying power to move its own people into occupied land; the UN and the International Court of Justice have said the settlements are illegal. Today more than 700,000 settlers live in the West Bank and East Jerusalem.',
     'A ring of settlements went up around Ramallah from the 1970s: Beit El, Psagot, Ofra, Dolev and others, on land taken from our villages. Since 2023 small farm outposts have spread fastest; in 2025 Ramallah governorate had more settler attacks than any other (ARIJ).',
     'Settlements decide which roads we drive, which land we can farm, and where the checkpoints are.'),
    ('The Wall, a capital', 'The roads.', 'What occupation means day to day',
     'Occupation is not one event but a system. Since 1967 the West Bank has been run by military orders: thousands of them, covering who may build, travel, teach, farm, dig a well or come home. Residency, permits and ID cards decide where a person may go. In 2024 the International Court of Justice found the occupation itself unlawful.',
     'For Ramallah families this means permits to cross the bridge, residency cards that can be cancelled, checkpoints like Qalandiyā, and land in Area C that cannot be built on.',
     'Most of the conflicts in this chapter are moments when this daily system broke into open violence.'),
    ('The Wall, a capital', 'A capital without a state.', 'Division and the Gaza wars, 2006 to 2023',
     'Hamas won the 2006 elections; in 2007 Palestinians split, with Hamas ruling Gaza and the Authority ruling West Bank towns from Ramallah. Israel blockaded Gaza and fought wars there in 2008–09, 2012, 2014 and 2021. In the West Bank, villages such as Bilʿīn and Nabī Ṣāliḥ held weekly unarmed marches against the Wall and settlements.',
     'Ramallah was spared the bombing but not the raids, arrests and closures; it mourned Gaza’s dead in its squares.',
     'The split still divides Palestinian politics, and the village marches are the model of popular resistance many young people know.'),
    ('The Wall, a capital', '2025.', 'Since October 2023',
     'After the Hamas attack of 7 October 2023, Israel’s war on Gaza killed tens of thousands of Palestinians and destroyed most of the Strip. In 2025 the UN’s independent Commission of Inquiry concluded that Israel had committed genocide there. In the West Bank, raids, arrests, closures and settler attacks rose sharply.',
     'Ramallah’s district villages, Turmus ʿAyyā, Sinjil, al-Mughayyir, Kafr Mālik and Ṭaybeh among them, faced settler attacks; Palestinian-Americans were among the dead. Fourteen new outposts went up in the governorate in 2025.',
     'This is the present. It is why the next generation is asking these questions.'),
]


# The wars around the town, 1911–2025: the table at the end of chapter 12, and the chart drawn from it (src/build_figs10.py).
WARS_AROUND_US = [['1911–1913', 'Italy’s war on Libya; the Balkan wars', 'Felt from a distance'],
    ['1914–1918', 'The First World War', 'Garrison, conscription, hunger, typhus; the front north of the town'],
    ['1920–1921, 1929', 'The riots', 'Felt from a distance'],
    ['1936–1939', 'The great revolt', 'Village searches; the attack on the town, October 1938; George Saah'],
    ['1939–1945', 'The Second World War', 'Rations; men in British, American and Transjordan uniform'],
    ['1947–1949', 'The Nakba', 'The town guard; the refugees and the camps'],
    ['1953', 'Qibya', 'A village of the district destroyed'],
    ['1956', 'Suez', 'The National Security Force drilled in the town'],
    ['1966', 'al-Samūʿ', 'Protests put down at al-Jalazūn'],
    ['1967', 'The June war', 'Ramallah taken on 6 June; the occupation begins'],
    ['1968', 'Karameh', 'Ibrāhīm al-Ṭawāsheh shot; emigration'],
    ['1970', 'Black September', 'Felt from a distance'],
    ['1973', 'October', 'The National Front; the mayors deported'],
    ['1978, 1982', 'Lebanon', 'The mayors removed, 1982; emigration'],
    ['1987–1993', 'The first intifada', 'Curfews; Birzeit closed four years'],
    ['1990–1991', 'The Gulf War', 'Round-the-clock curfew; families home from Kuwait'],
    ['1996', 'The tunnel', 'Seven killed in Ramallah'],
    ['2000–2005', 'The second intifada', 'The town invaded; the Muqāṭaʿa besieged'],
    ['2003', 'Iraq', 'Felt from a distance'],
    ['2006–2007', 'Lebanon; the split', 'Ramallah left as the seat of government'],
    ['2008–2022', 'The Gaza wars', 'Protests; the Qalandiyā march of 2014'],
    ['2023–2025', 'Gaza, Lebanon, Iran', 'Raids, settler attacks, closures; Iron Wall in the north']]


def apply(g):
    """Add the modern history to chapters 10 to 12. g is build_v5's globals()."""
    E, c, _plate, RIGHTS, D = g['E'], g['c'], g['_plate'], g['RIGHTS'], g['D']
    NUMTABLE = g['NUMTABLE']

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
        'from Burqīn near Jenin.', 'Document')
        + _p('In December 1917, with the front a few miles south, the Ottoman and German command at the Friends School ordered everyone in Ramallah to leave the town. '
             'A delegation went to the town’s governor, the mudīr <b>Jamīl al-ʿUmarī</b> of Aleppo, the last to hold the post, and won a month’s grace. '
             'The British came a few days into the month’s grace, and the order was never carried out{}.'.format(c(NIR + ', pp. 55–56.'))))

    snow = ent(10, '1920 · 1927', 'Snow, then the earth shakes',
        'On <b>9 February 1920</b> snow fell on Ramallah for seventy-two hours, up to a metre and a quarter deep. '
        'It broke the olive trees and closed the Jerusalem road for a week{}. '
        'On <b>11 July 1927</b> the great earthquake struck Palestine. In Ramallah <b>two people were killed</b> and many houses were broken, above all in the old town. '
        'The Latin Patriarchate paid for those who had lost their houses{}. '
        'One of the broken houses has a name. ʿAbdallah ʿĪsā Bateh’s home in Dār Ibrāhīm, near today’s Scout headquarters, was left unfit to live in. '
        'His family rented elsewhere for five years while he built again on Radio Street, near the Manāra{}.'.format(
            c(CAD + ', p. 55.'),
            c(SHAHIN + ', English section, chronology, p. 75: “Only two inhabitants of Ramallah killed, but property damage heavy”; '
              + SH + ', p. 34; ' + CAD + ', p. 56, for the old town and the Patriarchate.'),
            c(SH + ', p. 100.')),
        locplate('03041v.jpg', '2019696336',
            'A house in Nablus left a shell by the earthquake of 11 July 1927. We have found no photograph of the damage in Ramallah.',
            'American Colony Photo Department, 1927.')
        + _p('<b>What we still don’t know.</b> Beyond one shoemaker’s story, we have found nothing written about what Ramallah saw in the troubles of August 1929.'))
    add_body('The counting years', locplate('16769v.jpg', '2019707547',
        'The opening of the Palestine Broadcasting Service at its transmitter in Ramallah, 30 March 1936. '
        'The High Commissioner gives the inaugural address; the mast stands behind the crowd.',
        'Matson Photo Service, 1936.'))
    insert_after('The war, the locusts', [snow])

    ww2 = ent(10, '1939–1945', 'The Second World War',
        'The war reached Ramallah through its young men. <b>Elias Nasrallah Oudeh</b> served as a wireless operator in the Trans-Jordan Frontier Force, '
        'the British-commanded frontier cavalry, from 1938 to 1943, and his discharge certificate survives{}. '
        '<b>Shukri Elias ʿAjlouny</b> was a telegraph operator at the airport of Lydda in 1940{}, and <b>Edward Salamy</b> of Ramallah served in the United States army{}. '
        'At home the district was run by Palestinian officers of the Mandate: Mitri Farraj until 1941 (Nayrūz has 1940), then, from 1943, the historian ʿĀrif al-ʿĀrif{}. '
        'Nayrūz’s list of the subdistrict’s qāʾimmaqāms, its district governors, also names Jamīl al-Tājī, Naʿīm ʿAbd al-Hādī and Naẓīf al-Khayrī{}.'.format(
            c(SH + ', p. 282: the certificate of discharge, serial no. 3904, “W/T operator,” enlisted 4 October 1938, discharged 27 December 1943.'),
            c(SH + ', p. 275.'), c(SH + ', p. 92.'), c(CAD + ', p. 55.'), c(NIR + ', p. 60.')),
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
        'and built roadblocks and watchtowers under Dr <b>Jalīl Badrān</b>. Its fighters, drawn first from the town’s rover scouts, called themselves the <b>Armed Youth Organisation</b>. Years later Badrān laid out a square beside the women’s teachers’ college, with a stone column at its centre inscribed “Ramallah Youth Organisation”{}. On 14 March 1948 the guard beat off an attack on the Ramallah–Ramle bus, '
        'and it fought on the Jerusalem road at al-Qasṭal{}. '
        'In April units of the Arab Liberation Army came to the town, first the Yarmūk battalion under the Iraqi officer ʿAbd al-Ḥamīd al-Rāwī, then the Qādisiyya. Once they came close to blows with the town’s own fighters by the gate of the Latin convent, until Jordanian officers made peace between them{}. '
        'From April the people of Bīr Nabālā, Bayt Maḥsīr and Jaffa came up the hill: “Churches and schools opened their doors to give them refuge and shelter.” '
        'On 15 May, at almost noon, the Arab Legion drove into the town{}.'.format(
            c(CAD + ', p. 57.'), c(NIR + ', p. 64.'), c(CAD + ', p. 58.'), c(NIR + ', pp. 66–67.'), c(CAD + ', pp. 58–59. Cadora was acting mayor from 1 April 1948.')),
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
        'From 1950 Ramallah was a town of the Hashemite Kingdom, and from the end of 1949 its people were Jordanian citizens and Palestinians at once, as the Nationality Law of 1954 confirmed. '
        'On 30 September 1948 ʿUmar Maṭar al-Maʿānī was named the town’s military governor. At the Jericho Conference of 1 December 1948 the lawyer <b>ʿAzīz Shiḥāda</b> spoke for Ramallah, on 26 December a second conference, in Ramallah, approved its decisions, and on 2 January 1949 King ʿAbdallāh came back to Ramallah and stayed several days{}. '
        'The kingdom gave them a parliament and watched them. On 11 May 1951 the leaders of the Labour Party in Ramallah were arrested, accused of communism, and jailed in Amman{}. '
        'Dr <b>Daoud Mikhail</b> was jailed in 1957 for the National Socialist Party; years later his daughter, Dr Hanan Mikhail ʿAshrawi, reminded King Hussein of it{}. '
        'In 1952, Cadora writes, “life became unbearable,” and the town’s families left for America{}. '
        'Ramallah’s sons also sat in the king’s cabinets. The longest serving was <b>Simʿān Dāwūd</b>, of the al-Ballāṭ family: minister in twelve governments between May 1955 and August 1969, of commerce, reconstruction, the national economy, finance, communications and, from 1966, justice. '
        '<b>Jalīl Badrān</b> was minister of commerce and of reconstruction in the government of 15 December 1955, which fell five days later in the protests against the Baghdad Pact. Which Jalīl Badrān it was is disputed: the dentist born in Ramallah in 1913, later the town’s mayor, or the engineer Jalīl Ijḥā Badrān of the Amman municipality. '
        '<b>Jalīl Ḥarb</b> was minister of the national economy from 28 June 1961, and <b>Ḥannā Khalaf</b> was three times minister of justice, in 1962 and 1963. <b>Nadīm al-Zarw</b>, a pharmacist who was mayor when the occupation came, was named minister for municipal affairs in April 1970 and stood down the same day, unwilling to take office while comrades of his were still in prison; he was minister of transport from 1972 to 1974{}.'.format(
            c(NIR + ', pp. 69–70; ' + CAD + ', p. 61, for 26 December 1948.'), c(CAD + ', p. 62.'), c(SH + ', p. 54.'), c(CAD + ', p. 63.'),
            c('<i>al-Madīna News</i> (Amman), 6 October 2009: <span class="ar" dir="rtl">التمثيل العشائري: آل خلف، آل بدران، آل حرب (حدّادين فلسطين) / رام الله</span>, a series on the clans represented in Jordan’s governments, which gives the dates and traces each family through Shāhīn (1982) to the sons of Rāshid, and reports the dispute over which Jalīl Badrān was minister. ' + D('2009_AlMadina_Haddadin_of_Palestine_Ramallah.html') + '; the same series on Āl al-Zarw, 10 October 2009, for al-Zarw’s refusal in 1970; and its print edition, <i>al-Madīna</i> no. 175, 16 March 2009, p. 28, ' + D('2009_AbuGhneimeh_al-Haddadin_Ghassanids_of_Karak_al-Madina_175.pdf') + '. Every post and date here was checked against the Prime Ministry of Jordan’s database of ministers, pm.gov.jo (records 93, 97, 119, 127 and 192, read 26 November 2026), which lists al-Zarw as appointed and resigned on 19 April 1970. That Simʿān Dāwūd was of the al-Ballāṭ family of Ramallah is al-Madīna’s statement; the database gives only his name.')),
        plate('p045_3.jpg', 44, 'Ḥannā Khalaf of Ramallah addressing the Parliament of Jordan, 1961.')
        + plate('p337_2.jpg', 336, 'The Jordanian army band marches round al-Manāra and its five lion heads, probably in the 1960s.')
        + _p('<b>The border raids.</b> The armistice line ran a few kilometres west of the town, and across it the Israeli army raided the villages of the district. '
             'On the night of <b>14–15 October 1953</b> it attacked <b>Qibya</b>, a village of what is now the Ramallah governorate, and killed sixty-nine people, most of them in their houses as they were blown up. '
             'Jordan laid the attack before the Security Council two days later{}. '
             'Three years on, on <b>10 October 1956</b>, a raid on Qalqīliya came days before Israel invaded Sinai on 29 October, in concert with Britain and France, the war the Arabs call the Tripartite Aggression{}. '
             'Ramallah itself was not attacked. For the town the lasting blow came after, in the crackdown of 1957 that sent Dr Daoud Mikhail to prison.'.format(
            c('United Nations Security Council, S/3113, letter from Jordan, 16 October 1953.'),
            c('United Nations Security Council, S/3670 (1956), on the Qalqīliya raid; Institute for Palestine Studies, Palquest, “The 1956 War.”')))
        + _p('<b>What we still don’t know.</b> What Ramallah did in the days of the Suez war of 1956, and in the protests after the raid on al-Samūʿ in November 1966.'))
    insert_after('Where the refugees lived', [jordan])

    # =======================================================================
    # CHAPTER 12: 1967 to today
    june = ent(12, 'June 1967 – 1982', 'Occupation, and the mayor in Houston',
        'On <b>6 June 1967</b> the Israeli army took Ramallah{}. It made the <b>Odeh Hotel</b> its first headquarters in the town{}. Every weapon in the town was to be handed in at al-Manāra; '
        'people who had worked with the Palestinian organisations were arrested and some expelled. The army made Bayt Īl, Beit El, the seat of its command{}. '
        'Families driven out of ʿImwās, Yālū and Bayt Nūbā found shelter at Baytūniyā and in Ramallah{}. '
        'The feasts went quiet: “all large festivities, both Muslim and Christian, have ceased{}.” '
        'In 1974 the dentist <b>Alfred Toubassi</b> was taken to the Lebanese border at night and sent across, and Birzeit’s president, Dr <b>Ḥannā Nāṣir</b>, was deported for nineteen years{}. '
        'From 1978 the occupation set up the <b>Village Leagues</b> against the elected mayors, with their centre at Ramallah{}. '
        'The mayor the town had elected, <b>Karīm Khalaf</b>, flew in July 1974 to the Federation’s convention in Houston{}. '
        'Many of the town’s students were abroad that June and could not come home. The poet <b>Murīd al-Barghūthī</b>, of Dayr Ghassāna, was sitting his Latin examination at Cairo University on the morning of 5 June 1967; he crossed the Jordan bridge back to Ramallah only in the summer of 1996, thirty years later. '
        'He found the Society for the Support of the Family, which Umm Khalīl had founded “two years before Ramallah fell to the Israeli Occupation in 1967,” teaching the daughters and sons of martyrs and prisoners to sew, embroider and carve{}.'.format(
            c('Applied Research Institute–Jerusalem (ARIJ), <i>Atlas 40</i>, ch. 1.3.'),
            c(NIR + ', p. 70.'),
            c(FARHAN + ', pp. 79 and 100–101 (page numbers of the OCR text).'),
            c('al-Haq, field report on the Latrun villages, 13 June 2013. al-Haq is a Palestinian human-rights organisation founded in Ramallah in 1979.'),
            c(SHAHIN + ', English section, pp. 63–64.'),
            c(SH + ', p. 55; ' + BZU + '.'),
            c(FARHAN + ', p. 102.'),
            c(SH + ', pp. 341 and 357.'),
            c('Mourid Barghouti, <i>I Saw Ramallah</i>, trans. Ahdaf Soueif (Cairo: American University in Cairo Press, 2000; Arabic original <span class="ar" dir="rtl">رأيت رام الله</span>, 1997), pp. 1–2 and 115–16.')),
        plate('p162_1.jpg', 161, 'Feeding the children of needy refugees after the 1967 war, late 1960s.')
        + plate('p358_2.jpg', 357, 'Houston, July 1974: Mayor Karīm Khalaf with the Federation’s president, George Mogannam, and all its past presidents.')
        + _rec(['6 June 1967: Ramallah taken (ARIJ).',
                '1974: Dr Alfred Toubassi and Dr Ḥannā Nāṣir deported (Shaheen 2005; Birzeit University).',
                '2 June 1980: Mayor Khalaf loses a leg to a settler bomb; removed by the occupation in 1982 (in the entry above).']))

    int1 = ent(12, '1987–2000', 'The first intifada, and the Authority',
        'In December 1987 the uprising began, and Ramallah was one of its centres{}. In the long sieges, Lisa Taraki writes, '
        '“the towns’ prosperous merchants … paid their political dues by supplying the camp [al-Amʿarī] with food and provisions{}.” '
        'Birzeit University was closed by military order from <b>10 January 1988</b> to <b>29 April 1992</b>, and its teachers held classes underground in Ramallah{}. '
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
        + _rec(['10 January 1988 – 29 April 1992: Birzeit University closed by military order (Birzeit University).',
                '27 December 1995: the Palestinian Authority takes control of the town (IPS).']))

    int2 = ent(12, '2000–2005', 'The second intifada and the siege',
        'On <b>12 October 2000</b> Israel bombed Ramallah from the air: Arafat’s headquarters, the broadcasting centre and the police stations{}. '
        'On the evening of <b>Thursday 28 March 2002</b> the army invaded the town with about sixty tanks and 2,500 soldiers{}. Forty thousand people were under curfew, with water and power cut. '
        'By 3 April at least fifty-four Palestinians had been killed, and twenty-three were buried together in the car park of the Ramallah hospital{}. '
        'The United Nations recorded “extensive physical damage” to the Authority’s civilian offices{}. '
        'Arafat, besieged in the Muqāṭaʿa as its buildings were pulled down around him, died in Paris on 11 November 2004 and was buried in the Muqāṭaʿa the next day{}.'.format(
            c(IPS + ', 12 October 2000.'),
            c(NIR + ', p. 73, which puts the tanks in the town at six in the evening of Thursday, 28 March, though it prints the date as 29 March; United Nations, A/ES-10/186, 30 July 2002, gives the official date: the operation “began on 29 March with an incursion into Ramallah.”'),
            c('Charmaine Seitz, “In Ramallah, Grueling Reoccupation Grinds On,” <i>Middle East Report Online</i>, 5 April 2002, citing the Palestinian Centre for Human Rights.'),
            c('A/ES-10/186 (2002).'),
            c(IPS + ', 21 September 2002, for the demolitions.')),
        _testimony('We have two kilos of rice and we have to make it last for the four of us.',
                   'A Ramallah household under curfew, April 2002 (Seitz, <i>Middle East Report Online</i>)'))

    wall = ent(12, '2002–2025', 'The Wall, a capital, and our own people',
        'The Wall cut Ramallah off from Jerusalem, and the road south now ends at the checkpoint of <b>Qalandiyā</b>. '
        'The International Court of Justice found the Wall contrary to international law on 9 July 2004. '
        'Around the town stand <b>26 settlements</b> with nearly <b>150,000 settlers</b>; Psagot is built wholly on the land of al-Bīra, and Beit El on land of Dūrā al-Qarʿ, al-Bīra and Baytīn, some of it owned by Palestinian-Americans{}. '
        'The town became a capital without a state. In 2005 it elected <b>Janet Mikhail</b>, its first woman mayor{}. '
        'Its women went to law for what was theirs: in a study of 2010–13, women who claimed their inheritance in court outnumbered the men who did, in the courts of Ramallah, Hebron and Nablus{}. '
        'It buried <b>Maḥmūd Darwīsh</b> on 13 August 2008, in a grave that “faces the outskirts of Jerusalem”{}. '
        'The occupation reached the diaspora too. <b>ʿUmar Asʿad</b>, seventy-eight, of Jiljilyā and Milwaukee, died in January 2022 after soldiers left him bound and blindfolded{}. '
        '<b>Sayfollah Musallet</b>, twenty, of Tampa, was beaten to death by settlers at Sinjil on 11 July 2025{}. '
        'In 2025 the United Nations counted 1,680 settler attacks in the West Bank, “an average of five incidents per day”{}.'.format(
            c('PLO Negotiations Affairs Department, “Israeli Settlements in the Ramallah &amp; Al-Bireh Governorate,” 26 March 2023; '
              'International Court of Justice, advisory opinion of 9 July 2004; ARIJ, <i>Al Bireh City Profile</i> (2012): “Pesagot settlement was built wholly on Al Bireh city territories,” and Beit El “semi built on the city’s northern territories”; ARIJ, <i>Dura al-Qar’ Village Profile</i> (2012): “The major part of the settlement was established on the village lands”; POICA (2012) for Baytīn.'),
            c(CENT + '.'),
            c('Women’s Centre for Legal Aid and Counselling (WCLAC), <i>Palestinian Women and Inheritance</i> (Ramallah, 2014), ISBN 978-9950-354-00-5, p. 10 of the held copy; the survey ran from early 2010 to late 2013. ' + D('2014_WCLAC_Palestinian_Women_and_Inheritance_Study.pdf') + '.'),
            c('Al Jazeera, 13 August 2008.'), c('Al Jazeera, 16 August 2024.'),
            c('ABC News, 12 July 2025.'),
            c('United Nations OCHA, <i>Humanitarian Situation Update #346, West Bank</i>, 4 December 2025.')),
        plate('p343_3.jpg', 342, 'The Khalil Sakakini Cultural Centre, founded in 1996 in a house of 1927 once owned by Khalīl Ṣalāḥ, mayor from 1947 to 1951.')
        + _rec(['9 July 2004: the International Court of Justice on the Wall.',
                '22 September 2024: the Al Jazeera office in Ramallah raided and closed for 45 days (Anadolu Agency).',
                '2023: 26 settlements and about 150,000 settlers in Ramallah and al-Bīra governorate (PLO Negotiations Affairs Department).']))

    add_body('Ramallah becomes a city, clan by clan', _p(
        '<b>The Ottoman governors of the town.</b> Nayrūz, after Yūsuf Qaddūra, lists them: Aḥmad Murād of Jerusalem, the first, 1902–1905; '
        'Jamīl al-ʿUmarī of Aleppo, 1905–1911; a Turkish officer whose name we cannot read clearly in our copy, 1911–1912; ʿAlī Riḍā, also a Turk, 1912–1916; '
        'and al-ʿUmarī again, 1916–1917, the last. Elias ʿAudeh, he adds, was chosen as first mayor because he was not born into any of Ramallah’s clans (his family, newcomers from Dibbīn, had attached themselves to the ʿAwwād): '
        'every clan had its own candidate, and a man raised in the town but born outside it settled the quarrel{}.'.format(
            c(NIR + ', p. 388, notes 4 and 8, after Qaddūra, <i>Tārīkh madīnat Rām Allāh</i>, p. 43, and Khalīl Abū Rayya, <i>Rām Allāh qadīman wa-ḥadīthan</i>, p. 135. '
              'Nayrūz gives 1 April 1908 for the founding of the municipality and notes Abū Rayya’s 1 April 1910.')))
        + NUMTABLE('THE HEADS OF THE MUNICIPALITY, 1908–1999 — as Nayrūz lists them',
            ['Years', 'Head of the town'],
            [['1908–1921', 'Elias ʿAudeh al-Dubaynī'],
             ['1921–1922', 'Yūsuf Jiryis Darbās'],
             ['1922–1927', 'a council whose members took the chair in turn'],
             ['1927–1932', 'Mūsā Khalīl Mūsā'],
             ['1932–1937', 'Dr Saʿdallāh al-Qassīs'],
             ['1937–1940', 'Dimitri Farrāj, qāʾimmaqām'],
             ['1940', 'Jamīl al-Tājī, qāʾimmaqām'],
             ['1940–1943', 'Sālim Zaʿrūr'],
             ['1943–1947', 'Yūsuf Jiryis Qaddūra'],
             ['1947–1951', 'Khalīl Ṣalāḥ'],
             ['1951–1956', 'Dr Jalīl Badrān'],
             ['1956–1957', 'Shāhir al-Liḥaysin, qāʾimmaqām'],
             ['1957–1958', 'Falāḥ Ḥannūn'],
             ['1958–1961', 'Jalīl Ḥarb'],
             ['1961–1964', 'Būlus Sābā'],
             ['1964–1969', 'Nadīm al-Zarū'],
             ['1969–1972', 'Khalīl Mūsā Khalīl'],
             ['1972–1982', 'Karīm Khalaf'],
             ['1982–1986', 'officers of the Israeli army, appointed by the occupation'],
             ['1986–1996', 'Khalīl Mūsā Khalīl, again'],
             ['1996–1999', 'ʿĪsā Ziyāda'],
             ['from 1999', 'Ayyūb Yaʿqūb Rabāḥ']],
            NIR + ', p. 387. The dates are Nayrūz’s. A qāʾimmaqām is a district governor, here acting as head of the town.'))

    # ---- v87, second batch from Nayrūz (David, 16 Nov 2026: "3 its George Saah our relative")
    add_body('The revolt reaches the town', _p(
        '<b>The fight at al-Maskūbiyya, and George Saah.</b> The revolt had already come into the town once. In a winter of the revolt (Nayrūz writes 1936; the capture “some days later” and the hanging in November 1939 point rather to the winter of 1938–39) rebels came over the hills and held '
        'al-Maskūbiyya, the Russian ground by the Orthodox church in the old town, and fought the British troops there through the day. The British sent to Jerusalem for more men, '
        'then marched the people of Ramallah to the Odeh Hotel, their headquarters, in heavy rain and cold, and kept them there until dark, with every house left open for the search{}. '
        'Ṭalʿat Ḥarb remembered a bullet coming through his family’s front door while they hid inside{}. At sunset the rebels were gone and no one had been caught. '
        'The Orthodox priest, Fr <b>Yūsuf Ḥarb</b>, had agreed with them beforehand to leave the church door open, and they hid in the church until they could get away. '
        'The soldiers then went from house to house, mixing the oil with kerosene, the lentils with the olives, the flour with sugar and mud, so that the town’s winter stores were spoiled{}.'.format(c(NIR + ', p. 95.'), c(NIR + ', p. 95, from Ṭalʿat Ḥarb, <i>Tadhkārāt Ṭalʿat Ḥarb: ṣafaḥāt min al-dhākira al-filasṭīniyya</i>, p. 21.'), c(NIR + ', pp. 95–96, and p. 277, under Fr Yūsuf Ḥarb.')))
        + _p('One of the rebels was our own: <b>George Saah</b> (Jūrj al-Saah), son of Jaber Yaʿcoub Saah, known by his fighting name, <b>George al-Aqraʿ</b>. He fought, the town remembers, mostly alone and on his own decision. '
             'Farīd al-Ṭawāsha, born in 1921, remembered him on the hills above ʿAin Miṣbāḥ firing an old Turkish rifle at the Odeh Hotel. '
             'That night at al-Maskūbiyya he and his comrades escaped thanks to Fr Yūsuf Ḥarb. Some days later he was taken at Jifnā with a group of fighters, tried, and sentenced to death. '
             'Before the hanging he asked for a priest, to make his confession and take communion, and a priest of the Latin Patriarchate, Fr <b>Ibrāhīm ʿAyyād</b>, came to him at the Maskūbiyya prison in Jerusalem. '
             'When his body was brought home, Khalīl Mūsā Khalīl remembered, every town and village in Palestine sent people to console Ramallah for its martyr, its <i>shahīd</i>, and for days the al-Kharja square was full of women singing the old laments for him{}. The Palestinian register of martyrs executed by the Mandate names him <b>George Jaber al-Ṣāʿ</b> and records that he was hanged in the Jerusalem prison on <b>16 November 1939</b>{}.'.format(
            c(NIR + ', pp. 260–261, from his interviews with Farīd al-Ṭawāsha (7 October 2003) and Khalīl Mūsā Khalīl (1 November 2003), and Yaʿqūb al-Aṭrash, <i>Min aʿlām al-niḍāl al-waṭanī al-filasṭīnī: al-Ab Ibrāhīm ʿAyyād</i>, p. 193; '
              'p. 277, under Fr Yūsuf Ḥarb; p. 95 and its note naming Fr ʿAyyād, from the lawyer ʿĪsā Qandaḥ (interview, 2 August 2003). '
              'Qandaḥ also names George with Yaʿqūb Ḥishma, ʿAṭallah Khashshān, Ilyās Samʿān and others among the Ramallah men who went with the rebels from 1936 (p. 95, note). '
              '<b>Inference, labelled.</b> Nayrūz writes the execution beside the year 1936. British military courts began hanging rebels only in November 1937, with Shaykh Farḥān al-Saʿdī, '
              'and McDowell’s diary of November–December 1938 and the West Yorkshire Regiment’s reports (Hughes 2015) record a search of the town and rebel fire on the Ramallah billets that winter; George Jaber al-Ṣāʿ was hanged in the Jerusalem prison on 16 November 1939. The AFRP family tree records his father as Jaber Yaʿcoub Saah and his death in 1938; he left two sons, Fareed and Fuad (AFRP family tree, record AWD1019; identification confirmed by David Saah, 17 November 2026). The Maskūbiyya in town and the prison in Jerusalem share a name: both were Russian ground (Cadora, <i>Remembering Ramallah</i>, 2023, editors’ note).'), c('WAFA, Palestinian News and Information Agency, <i>Shuhadāʾ aʿdamathum sulṭāt al-intidāb al-barīṭānī fī Filasṭīn</i> (2021): “George Jaber al-Ṣāʿ, Jifnā, 1908, 16/11/1939, Jerusalem prison, execution by hanging.” The register gives Jifnā, where he was taken, as his place, and 1908 as his birth year. Other dates differ: Shaheen (2005), p. 261, beside his photograph, says he was hanged “ca. 1937” at about forty, and the family tree has 1938. We print the register’s date, the only one given to the day.')))
        + _p('<b>The town in the national movement.</b> A survey of 1935 counted a hundred leading figures of Palestinian politics. Twenty-three were Christians, and two of them were from Ramallah, one Orthodox and one Protestant, from a town of at most five thousand people. '
             'Among the women, <b>Nelly Ziyāda</b> of Ramallah was a prominent member of the Syrian Social Nationalist Party{}.'.format(c(NIR + ', p. 62.'))))
    add_body('New families arrive', _p('The Saah family also gave the revolt a <i>shahīd</i>: George Saah, “George al-Aqraʿ”, son of Jaber Yaʿcoub Saah and father of Fareed and Fuad, whose story is told in “The revolt reaches the town”.'))

    add_body('Snow, then the earth shakes', _p(
        'It was not the first great snow. In <b>1895</b>, Nayrūz writes, snow more than a metre deep caught a party of Russian pilgrims on the road near Ramallah, and thirty of them died. '
        'The young men of the town went out into the storm and brought the living in on the backs of animals, many of them the horses of the Friends School, in the care of ʿĪsā Abū Shahla. '
        'The pilgrims were shared out among the guest houses and the homes of the town until the storm passed{}.'.format(
            c(NIR + ', p. 86. Cadora’s editors place the Russian pilgrims’ graves at al-Maskūbiyya, by the Orthodox church in the old town (Cadora, <i>Remembering Ramallah</i>, 2023, note to the Russian Compound); that these are the dead of 1895 is our inference.'))))

    add_body('The war, the locusts', _p(
        'Hunger came before the guns. In the dry year of <b>1913</b> the municipality rebuilt the spring of ʿAin Miṣbāḥ, brought the water of ʿAin al-Karzam to it, and rebuilt ʿAin al-Mizrāb{}. '
        'In the war years, Fr Yūsuf Ḥarb remembered, the hungry of Ramallah followed the Turkish army’s horses to pick up their dung, dry it, and take out the barley grains the horses had not digested, '
        'to grind them again for bread; people searched the roads for orange peel to eat{}.'.format(c(NIR + ', p. 87.'), c(NIR + ', p. 87, from Fr Yūsuf Ḥarb.'))))

    add_body('The town guards itself', _p(
        '<b>The battle of al-Maṣyūn.</b> Nayrūz tells the road war of early 1948 from the town’s side. A week after three Ramallah travellers were killed on the Jerusalem road, about twenty men from the settlement of ʿAṭarot, by Qalandiyā, lay in wait at dawn on the road to Rāfāt. '
        'A bus going from Ramallah to Jaffa drove into the ambush, and its ticket seller, a Ramallah man, was killed. As the attackers made their way back over the heights of al-Maṣyūn, close above the town, men of Ramallah and al-Bīra caught them, '
        'and young men came running from al-Bīra, al-Jīb, Baytūniyā, Rāfāt and al-Judayra. Qāsim al-Rīmāwī read the news on the radio from Ramallah. '
        'Nayrūz counts it the fight that took Ramallah off the list of towns to be taken{}.'.format(
            c(NIR + ', pp. 97–98, from the lawyer ʿĪsā Qandaḥ. Nayrūz dates the ambush 1 March 1948; whether it is the attack on the Ramallah–Ramle bus that Cadora dates 14 March, we cannot tell.')))
        + _p('The refugees began to arrive on <b>22 April 1948</b>; Jaffa’s people came after 26 April, and those of Ramle and Lydda after 12 July. Soon there were more refugees in the town than people of Ramallah, and they gathered in the west of the town, at Baṭn al-Hawā. '
             'On 26, 27 and 29 May aircraft bombed the town, and above all the refugees at Baṭn al-Hawā. Jiryis Rayyān remembered a pedlar at al-Manāra killed by a shard, and the town sleeping more than a week under the olive trees{}.'.format(
            c(NIR + ', p. 99, from Jiryis Rayyān, born 1920 (interview, 23 July 2003).'))))

    add_body('The peasants’ revolt of 1834', _p(
        'Nayrūz keeps a place name from that year. <i>Maḥaṭṭ al-madāfiʿ</i>, “where the guns stood,” is the ground where the Friends Boys School stands today. '
        'There, he writes, Ibrāhīm Pasha’s army set its cannon in 1834 and fired on the men of al-Bīra, who held Rās al-Ṭāḥūna in defence of their town{}.'.format(c(NIR + ', p. 93.'))))

    add_body('Elihu Grant writes the town down', _p(
        'Grant saw older Ramallah too. Nayrūz reports his account of rock-cut tombs in the garden of Dr Saʿdallāh al-Qassīs, near the Friends Girls School, reached by a horizontal passage and finely carved: '
        'not wayside graves, Grant judged, but the burial ground of notables. Nayrūz adds that many more were found while digging the foundations of the Mustaqbal school, on the Birzeit road and at ʿAin Miṣbāḥ, and that most are being lost to building{}.'.format(
            c(NIR + ', p. 307, citing Grant. We have not found the passage in Grant’s <i>The Peasantry of Palestine</i> (1907).'))))

    add_body('The city, counted', _p('By 2004 Ramallah had six congregational mosques, among them al-ʿUmarī in the old town and the mosques of ʿAin Miṣbāḥ and ʿAin Munjid{}.'.format(c(NIR + ', p. 301.'))))
    insert_after('The city, counted', [june, int1, int2, wall])
    add_body('Occupation, and the mayor in Houston', _p(
        '<b>Relief from the emigrants.</b> After the war the Federation sent relief to the town through ʿAzīz Shāhīn, back in Ramallah since 1958. About $24,000 passed through his hands in 1967–68 alone. In October 1967 he wrote to America: “There will be starvation unless you help us”{}.'.format(
            c('<i>Hāthihi Rām Allāh</i>, the Federation’s magazine, 1967–68 issues.'))))

    # ---- v95, wars and the occupation spread through the chapters (David, 17 Nov 2026: "Spread through").
    # Sources and the full list: /mnt/project-files/history/conflicts_1936_present/LIST.md
    HRW12 = 'Human Rights Watch, <i>“Forget About Him, He’s Not Here”: Israel’s Control of Palestinian Residency in the West Bank and Gaza</i> (5 February 2012)'
    ARIJ15 = 'Applied Research Institute–Jerusalem (ARIJ), <i>Ramallah Governorate Profile</i> (2015)'
    OCHA = 'United Nations OCHA'
    FTB = 'Mogannam and Saah, <i>Ramallah Family Tree Book</i>, v117 (AFRP, 2026)'

    add_body('The war, the locusts', _p(
        '<b>Shot for refusing.</b> “In 1914, three persons from Ramallah were executed in Jerusalem by the Turks. They were accused of treason for refusing to join the war.” '
        'One of them, the family record says, was <b>Ḥannā Jiryis al-Nāṭūr</b>, eighteen years old. The other two are not named{}.'.format(
            c(FTB + ', p. 651, record JIR3010. We have found no Ottoman or newspaper record of the executions.'))))

    add_body('The revolt reaches the town', _p(
        '<b>In the courts.</b> The town also defended its rebels at law. <b>Mogannam E. Mogannam</b>, head of the Arab lawyers of Palestine and husband of Matiel Mogannam, '
        '“was credited for arguing multiple cases of Palestinian rebel fighters and getting them saved from the death sentence by the British after 1936 uprising”{}.'.format(
            c(FTB + ', p. 144, record SHAR782.'))))

    add_body('The town guards itself', _p(
        'One of the dead of Nabī Yaʿqūb may be ours by name. The family tree records that <b>Ayyūb Rizq Yaʿqūb Mīkhāʾīl</b> of Ramallah “was killed in Naby Ya’coub … in the war … between Arabs and Jews in 1947.” '
        'Cadora dates the shooting of the district’s young men there to 18 April 1948. We print both dates{}.'.format(
            c(FTB + ', p. 91, record AWD469; ' + CAD + ', pp. 58–59.'))))

    add_body('Occupation, and the mayor in Houston', _p(
        '<b>1972–1973.</b> On <b>28 March 1972</b> the towns of the West Bank voted for their councils for the first time under occupation, and Ramallah chose Karīm Khalaf. '
        'In October 1973 Egypt and Syria went to war, and with the war’s end the West Bank stopped waiting for the Arab armies. Its leaders, the mayors of Ramallah and al-Bīra among them, formed the <b>Palestinian National Front</b> that year. '
        'In <b>December 1973</b> the army arrested eight of them and drove them across the river to Jordan, al-Bīra’s mayor <b>ʿAbd al-Jawwād Ṣāliḥ</b> among them{}. '
        'Birzeit College was closed by military order for the first time that autumn, after a student march, and less than a year later its president was deported{}.'.format(
            c('<i>New York Times</i>, 10 December 1973, on the deportations.'),
            c(BZU + '.')))
        + _p('<b>March 1982.</b> The occupation then removed the mayors. On <b>18 March 1982</b> it dissolved al-Bīra’s council and dismissed its mayor, <b>Ibrāhīm al-Ṭawīl</b>. '
             'Two days later, on 20 March, <b>Ibrāhīm ʿAlī Darwīsh</b>, seventeen, was shot dead in al-Bīra’s square. On <b>25 March</b> Karīm Khalaf was dismissed. '
             'The two towns answered with a general strike, the army closed them, and Birzeit had already been shut in February. For four years Israeli officers ran Ramallah’s town hall{}.'.format(
            c('United Nations Security Council, S/14923 (1982); ' + FARHAN + ', p. 102; ' + NIR + ', p. 387, for the officers, 1982–1986.'))))

    add_body('The first intifada, and the Authority', _p(
        '<b>The curfews.</b> When the Gulf War began on <b>17 January 1991</b> the whole West Bank was put under curfew day and night, the longest since 1967. Work in Israel stopped, and so did the money sent home from the Gulf{}. '
        'From <b>1 December 1991</b> Ramallah and al-Bīra were under full curfew of their own; it was eased to a night curfew on 15 December and lifted by court order by 11 February 1992{}.'.format(
            c('Human Rights Watch, 27 January 1991, and <i>World Report 1992</i>.'),
            c(IPS + ', December 1991; Human Rights Watch, <i>World Report 1993</i>.')))
        + _p('<b>September 1996.</b> When the tunnel under the Old City of Jerusalem was opened, the protests began in Ramallah. Between 25 and 27 September seven Palestinians were killed in Ramallah and hundreds wounded, '
             'Palestinian police and the army fired on each other, and the town was made a closed military zone: “the worst fighting since the peace process began”{}.'.format(
            c(IPS + ', 25–27 September 1996; Palestinian Centre for Human Rights, <i>The Clashes of September 1996</i>.'))))

    add_body('The Wall, a capital, and our own people', _p(
        '<b>A capital without a state.</b> After June 2007, when the Authority lost Gaza to Hamas, it governed from Ramallah alone, and the town’s place as the seat of government was fixed{}. '
        'Its streets became the place where the West Bank’s protests gathered. On <b>24 July 2014</b>, during the war on Gaza, about ten thousand people marched from al-Amʿarī camp to Qalandiyā; two were killed and dozens hurt{}. '
        'In October 2015 the weekly clashes were at the <b>DCO checkpoint</b> by Beit El, at al-Bīra’s northern edge, and in one week, 20–26 October, 188 people of the governorate were injured{}.'.format(
            c(TARAKI + '.'),
            c('PBS NewsHour, 24 July 2014.'),
            c(OCHA + ', <i>Protection of Civilians</i> weekly report, 20–26 October 2015.')))
        + _p('<b>The land.</b> Under the Oslo map of 1995, about <b>64 per cent</b> of the governorate, 549,906 of its 855,587 dunums, is Area C, under full Israeli control; Area A, under the Authority, had grown to only about 18 per cent of the West Bank by 1999. '
             'Most of the settlements around the town were set down in a few years: Ofra in 1975, Beit El in 1977, Psagot in 1981, Kokhav Yaʿacov in 1984{}.'.format(
            c(ARIJ15 + ', p. 48, and its table of settlements.')))
        + _p('<b>The roads.</b> The town’s gates are the checkpoints: Qalandiyā to the south, the DCO by Beit El to the north, and the gates at ʿAyn Yabrūd and ʿAṭāra that cut it off from the villages beyond. '
             'In December 2025 the United Nations counted <b>925</b> checkpoints, gates and roadblocks in the West Bank, more than 120 of the gates put up that year{}.'.format(
            c(OCHA + ', <i>Movement and Access in the West Bank</i>, April 2026.')))
        + _p('<b>Water.</b> In 2010 the people of the governorate had on average 108 litres of water a day each, and some of its villages less than 28; the settlers around them used over 400{}.'.format(
            c(ARIJ15 + ', pp. 44–46.')))
        + _p('<b>The right to come home.</b> This is where the occupation reaches our families abroad. It began with the census of September 1967: everyone away that day lost the right to live in the town. '
             'Between 1967 and 1994 about <b>130,000</b> West Bank Palestinians were struck off the register after long stays abroad, and in 2000 Israel stopped deciding requests to reunite families altogether{}. '
             'For decades a Palestinian-American with a West Bank identity card could come home only over the Allenby bridge. '
             'Only in 2023, as the price of joining the United States visa-waiver programme, did Israel agree to let all American citizens in through its airport, “regardless of national origin”{}.'.format(
            c(HRW12 + '.'),
            c('United States Department of Homeland Security, 27 September 2023, designating Israel for the Visa Waiver Program after Israel’s commitment of 19 July 2023.')))
        + _p('The settlers’ violence reached our own. <b>Tawfīq ʿAbd al-Jabbār</b>, seventeen, of Gretna, Louisiana, was shot on 19 January 2024 on the road by al-Mazraʿa al-Sharqiyya, his family’s village, and died in the Ramallah hospital{}.'.format(
            c('Al Jazeera, 21 January 2024.')))
        + _p('<b>What we still don’t know.</b> The town’s own record of the first intifada has not been gathered: the names of its dead, the count for the town itself apart from the district, and its prisoners. If you know of a list of the town’s martyrs or prisoners from those years, we would like to hear from you.'))

    # ---- v96, the wars plan (David, 17 Nov 2026: "Go, as recommended").
    # Plan: /mnt/project-files/history/conflicts_1936_present/v2_2026-11-17/PLAN_and_RED_TEAM.md, steps 3, 4 and 6.
    # Grade A/B items only. The step 2 holds (1929, the WWI toll, the conscription year, the 1944 radio raid,
    # George Saah's date, the 12 October 2000 wording, landowners' names, family stories) stay out.
    KHURI = ('Niqūlā Khūrī, memoir, in <i>The House of the Priest</i>, ed. Sarah Irving, Charbel Nassif and Karène Sanchez Summerer '
             '(Leiden: Brill, 2022, open access)')
    HRW02 = 'Human Rights Watch, <i>In a Dark Hour: The Use of Civilians during IDF Arrest Operations</i> (April 2002)'
    UN186 = 'United Nations, Report of the Secretary-General, A/ES-10/186 (30 July 2002)'
    JPS67 = '<i>Journal of Palestine Studies</i>, Special Document File, “Jerusalem 1967” (2007), the memoir of Anwar al-Khaṭīb, Jordan’s governor of Jerusalem'
    DSP04 = ('Sarah Jessup and Nader Saʿīd, <i>Community Organizing in the West Bank: Opportunities and Obstacles in Civil Society, 2000–2003</i> '
             '(Birzeit University Development Studies Programme, 2004)')
    POICA = 'Applied Research Institute–Jerusalem (ARIJ), POICA, the 2025 reports on settler attacks and on uprooted trees (February 2026)'
    UNKNOWN = '<p><b>What we still don’t know.</b>'

    def add_before_unknown(prefix, html):
        """Put new paragraphs before the entry's closing 'What we still don't know'."""
        i = idx(prefix)
        b = E[i][7]
        k = b.rfind(UNKNOWN)
        b = b[:k] + html + b[k:] if k >= 0 else b + html
        E[i] = E[i][:7] + (b,) + E[i][8:]

    def replace_in(prefix, old, new):
        i = idx(prefix)
        k = 6 if old in E[i][6] else 7
        assert E[i][k].count(old) == 1, (prefix, old)
        E[i] = E[i][:k] + (E[i][k].replace(old, new),) + E[i][k + 1:]

    BARGH = 'Mourid Barghouti, <i>I Saw Ramallah</i>, trans. Ahdaf Soueif (Cairo: American University in Cairo Press, 2000)'
    # v115: movie facts checked against the Literature folder (David, 20 Nov 2026)
    add_body('Occupation, and the mayor in Houston', _p(
        'Some 5,500 people were driven out of the three villages, and Nayrūz writes that they were sent toward Ramallah{}.'.format(
            c('UN-Habitat, <i>Spatial Planning in Area C of the Israeli-Occupied West Bank</i> (2015), p. 37: “Beit Nuba was one of three villages from which some 5,500 Palestinians were expelled”; ' + NIR + ', p. 201: '
              '<span class="ar" dir="rtl">قامت عصابات الاحتلال بتهجير هذه القرى الثلاث نحو مدينة رام الله</span>.'))))
    add_body('The first intifada, and the Authority', _p(
        '<b>ʿAdlī and the leaderships.</b> Three teams of the uprising’s Unified National Leadership were arrested one after another in Ramallah{}. '
        'At Dayr Ghassāna a schoolboy, ʿAdlī, ran to close the school gates when soldiers attacked a demonstration there, and was shot in the chest and the head. He was his mother’s only son{}.'.format(
            c(NIR + ', p. 27, n. 30: <span class="ar" dir="rtl">تم اعتقال ثلاث طواقم للقيادة الوطنية الموحدة للانتفاضة في رام الله</span>.'),
            c(BARGH + ', p. 74: “’Adli rushed to close the school gates, his arms wide open. One shot in the chest. One in the head.”'))))
    add_body('The second intifada and the siege', _p(
        'Nayrūz writes that more than nine houses in ten in the town were broken into, and that the hospital morgue filled until it held twenty-five bodies, who were buried in the hospital yard{}.'.format(
            c(NIR + ', p. 74: <span class="ar" dir="rtl">فاكثر من 90% من بيوت المدينة تم اقتحامها</span>; the morgue <span class="ar" dir="rtl">وصلت إلى خمسة وعشرين جثة</span>. '
              'The figure of twenty-three in the car park is MERIP’s (2002); the two counts may be of different days.'))))
    add_body('The Wall, a capital, and our own people', _p(
        '<b>The olive harvest of 2025.</b> In the first twenty-seven days of October the United Nations counted <b>126</b> settler attacks on the harvest, four in ten of them in Ramallah governorate. '
        'Al-Mughayyir alone had suffered 43 attacks that year, and is ringed by seven outposts. Between April and June at least four new outposts went up among Sinjil, Silwād, Kafr Mālik and al-Mazraʿa al-Sharqiyya, and their farmers were kept from their own olive groves{}.'.format(
            c('United Nations OCHA, <i>Humanitarian Situation Update #335, West Bank</i> (October 2025).'))))

    # v116: facts sourced 22 Nov 2026 (David: "for the missing facts look up reliable sources")
    add_body('Occupation, and the mayor in Houston', _p(
        '<b>Ṣumūd.</b> Palestinians have a word for staying: <i>ṣumūd</i>, steadfastness. In 1982 Raja Shehadeh, a Ramallah lawyer, described it as a third way between violent resistance and passive acceptance{}. Its common sign is the olive tree{}.'.format(
            c('Institute for Palestine Studies, <i>Palestinian Journeys</i>, “Sumud”: “Shehadeh described sumud as a state of mind, a ‘third way’ between violent resistance and passive acceptance.” Raja Shehadeh, <i>The Third Way: A Journal of Life in the West Bank</i> (London: Quartet, 1982).'),
            c('Rijke and van Teeffelen, “To Exist Is to Resist,” <i>Jerusalem Quarterly</i> 59 (2014): the olive tree is “a widely used metaphorical expression of sumud.”'))))
    add_body('The second intifada and the siege', _p(
        'The voice of the town went first. On 13 December 2001 Israeli missiles hit the main transmitter of the Palestinian Broadcasting Corporation in Ramallah and soldiers toppled its 90-foot tower, and on 19 January 2002 they blew up its five-storey building{}. The Palestine Broadcasting Service had begun broadcasting from a transmitter at Ramallah on 30 March 1936{}.'.format(
            c('Committee to Protect Journalists, 13 December 2001 and January 2002; Palestinian Centre for Human Rights, <i>Israeli Attacks Against Journalists</i>, January–March 2002: “They destroyed the five-story building of the Palestinian Broadcasting Corporation (PBC).”'),
            c('Andrea L. Stanton, <i>This Is Jerusalem Calling</i> (University of Texas Press, 2013), introduction: “On the penultimate day of March 1936, the Palestine Broadcasting Service (PBS) began radio broadcasts from a new transmitter in Ramallah.”'))))
    add_body('The Wall, a capital, and our own people', _p(
        'On <b>18 May 2021</b> Palestinians in Gaza, the West Bank and inside Israel went on a general strike together{}. '
        'In January 2025 the army began its operation in the northern camps, which UNRWA called the longest in the West Bank since the second intifada; Jenin camp was left empty, and by December nearly 32,000 people from the camps of Jenin, Ṭūlkarm and Nūr Shams were still displaced{}. '
        'When Israel attacked Iran on 13 June 2025 it put the whole West Bank under closure, shut the main checkpoints and closed the Allenby Bridge{}. '
        'Modiʿin Illit, begun in 1991, was built on land of Bilʿīn, Niʿlīn, Dayr Qiddīs, al-Midya and Kharbathā al-Miṣbāḥ, and by 2011 held some 52,000 settlers{}.'.format(
            c('Al Jazeera, 18 May 2021: “Shops were shuttered across cities in Gaza, the occupied West Bank and in villages and towns inside Israel.”'),
            c('UNRWA, press release, 10 February 2025; United Nations OCHA, <i>Humanitarian Situation Update #346, West Bank</i>, 4 December 2025.'),
            c('WAFA, 13 June 2025: “Israel imposed a full closure on the West Bank”; United Nations OCHA, <i>Humanitarian Situation Update #298</i>, 18 June 2025: “Main checkpoints on major road arteries were completely shut.”'),
            c('ARIJ/POICA, 5 May 2008: “established on lands originally owned by Palestinians from Ni’lin, Deir Qiddies, Al Midya, Bil’in”; ' + ARIJ15 + ', table 34.'))))

    # CHAPTER 10 ---------------------------------------------------------
    add_body('The war, the locusts', _p(
        '<b>The front line.</b> Before the British came, the town was a Turkish base, with a garrison and grain depots{}. '
        'The war shut it off from the world. The schools of the area closed in 1914, Bishop Gobat’s school among them, and emigration stopped because the sea was too dangerous{}. '
        'Men who fled the army hid in the wilderness and the wadis and came home at night for food; if they were caught they were usually executed{}. '
        'After December 1917 the front ran just north of the town for nine months. In Birzeit, the priest Niqūlā Khūrī remembered, his family was “traumatized because the British cannons were incessantly bombarding the town from Ramallah, since the Turks were still occupying” it{}. '
        'In March 1918 the battle of Tell ʿĀṣūr fixed the line from Kafr Mālik to Nabī Ṣāliḥ, and there it stayed until September{}.'.format(
            c(CAD + ', p. 53.'),
            c(NIR + ', pp. 358 and 213.'),
            c(NIR + ', p. 55.'),
            c(KHURI + ', PDF p. 107.'),
            c('Cyril Falls, <i>Military Operations: Egypt and Palestine</i>, vol. 2 (London, 1930), the British official history, used for the dates.')))
        + _p('<b>In three armies.</b> Ramallah’s sons fought on both sides. <b>Ibrāhīm Rashīd Ḥishmeh</b> was photographed in Turkish uniform about 1916{}. '
             '<b>Khalīl ʿŪdeh ʿAwwād</b> served in the British army and came home with two medals{}. '
             'From America <b>Mūsā Rabāḥ</b> and <b>Yaʿqūb Ḥanania</b> served in the United States army, and <b>Ibrāhīm Shiḥāda Qandaḥ</b> came home from it in 1919{}. '
             'That same year emigrants from Ramallah helped found the Palestine Anti-Zionism Society in New York{}.'.format(
            c(SH + ', p. 249.'), c(SH + ', p. 154.'), c(SH + ', pp. 249 and 251.'), c(NIR + ', p. 210.'))))

    add_body('The revolt reaches the town', _p(
        '<b>The villages, 1936.</b> The revolt was fought in the district’s villages before it reached the town. In early July 1936 troops sweeping the Ramallah subdistrict '
        '“repeatedly fired on villagers, killing six and injuring four.” The searches spoiled their food stores, and the collective fines were taken at once, often in kind, in grain and animals{}. '
        'The rebels hid in the same villages. Ḥannā ʿĪsā Khalaf of Ramallah hid from the British night raids in a dry well at Ṭaybeh, and at Kafr Mālik and Kafr Niʿma{}.'.format(
            c('Charles Anderson, “The Suppression of the Great Revolt and the Destruction of Everyday Life in Palestine,” <i>Jerusalem Quarterly</i> 79 (2019), pp. 12–13, drawing on al-Sifrī and the British files.'),
            c(SH + ', p. 41.'))))

    add_body('The Second World War', _p(
        '<b>The home front.</b> When the war began in 1939 people rushed to buy food. Then the municipality issued ration cards and handed out supplies and cloth “in an orderly and equitable manner”{}. '
        'The Italian priests left Palestine in 1940{}. <b>Farḥāt Ziadeh</b> finished his law degree in London that year and could not get home; he went to the United States and made his career there{}. '
        'The war also brought one man out of hiding. Ḥannā ʿĪsā Khalaf, wanted since the revolt, was allowed out once it began, through <b>Miriam Zaʿrūr</b>, a Ramallah woman in British service{}. '
        'In 1945 the church bells rang for the peace, and the town’s sects gave thanks together in the Greek Orthodox church{}.'.format(
            c(CAD + ', p. 57.'), c(NIR + ', p. 288.'), c(SH + ', p. 77.'), c(SH + ', p. 41.'), c(CAD + ', p. 57.'))))

    # CHAPTER 11 ---------------------------------------------------------
    replace_in('Under the Jordanian crown',
        _p('<b>What we still don’t know.</b> What Ramallah did in the days of the Suez war of 1956, and in the protests after the raid on al-Samūʿ in November 1966.'),
        _p('<b>Suez, 1956.</b> When Britain, France and Israel attacked Egypt, Ramallah drilled. Two photographs show the <b>National Security Force</b> in the town “at the time of the triple attack on Egypt.” '
           'In them are the attorney <b>Ḥannā Saʿah</b>, George Shunnāra, Boulos Mogannam, the attorney ʿĪsā Qandaḥ and Elias Naṣrallah. Many of the men were refugees of 1948 living in Ramallah{}. '
           'The missionaries of the Evangelical Home left the town that year{}.'.format(c(SH + ', p. 99.'), c(NIR + ', p. 369.')))
        + _p('<b>al-Samūʿ, 1966.</b> After the Israeli raid on al-Samūʿ, near Hebron, in November 1966, the camps rose. At <b>al-Jalazūn</b>, north of the town, the Jordanian commander of the Ramallah brigade, Brigadier Kamāl al-Ṭāhir, put the protest down with what Jerusalem’s governor called “brutalities”{}.'.format(
            c(JPS67 + ', p. 91.')))
        + _p('<b>What we still don’t know.</b> What the town’s own papers wrote in the weeks of November 1956 and November 1966.'))

    # CHAPTER 12 ---------------------------------------------------------
    add_body('Occupation, and the mayor in Houston', _p(
        '<b>June 1967.</b> Israeli planes struck Ramallah on 6 June{}. Jordan’s Ramallah brigade, under the same Brigadier al-Ṭāhir, held the heights of Nabī Ṣamwīl above Jerusalem. '
        'On the second day it pulled back without a fight. Anwar al-Khaṭīb, Jordan’s governor of Jerusalem, called it “a lion unto the refugees and a rabbit in the face of the enemy”{}. '
        'Flights that had used the Jerusalem airport at Qalandiyā were sent to Lod{}.'.format(
            c(NIR + ', p. 358.'), c(JPS67 + ', pp. 90–91.'), c(JPS67 + ', with Rūḥī al-Khaṭīb’s memorandum of 26 August 1967; ' + CAD + ', p. 57, note.')))
        + _p('<b>Karameh, 1968–1969.</b> On <b>21 March 1968</b>, the day of the battle of Karameh across the river, <b>Ibrāhīm al-Ṭawāsheh</b> of Ramallah was stopped by a patrol near Bayt ʿŪr al-Taḥtā and shot dead{}. '
             'In 1969 soldiers stormed the Girls’ Secondary School, beat its teachers and pupils, and closed it for forty days{}. '
             'Nayrūz counts Karameh, October 1973 and the invasion of Lebanon in 1982 among the wars that kept the town emigrating{}.'.format(
            c(NIR + ', p. 100, from Farīd al-Ṭawāsheh.'), c(NIR + ', p. 366.'), c(NIR + ', p. 209.'))))

    add_body('The first intifada, and the Authority', _p(
        '<b>The town hall and the Manāra.</b> After Karīm Khalaf was removed in 1982, an Israeli officer ran the town hall with an armed bodyguard and soldiers at the door. '
        'Under him the <b>Manāra</b>, the column with its five lions’ heads, was taken down, officially for the traffic. The town saw it as an attack on its identity, since the square was where its demonstrations began. The Federation’s magazine <i>Hathihe Ramallah</i> answered in 1983: “Al-Manara Will Be Rebuilt.” It was: the work began in 1999, and the new monument, with four marble lions, was finished in July 2000{}. '
        'From 28 September 1986 an appointed Palestinian council under Khalīl Mūsā Khalīl ran the town until 1996{}.'.format(
            c(SH + ', pp. 224–225.'), c(NIR + ', p. 381.')))
        + _p('<b>Closed.</b> Military orders closed Birzeit University fifteen times. In the long closures every school was shut, and a pupil carrying a textbook could be taken for questioning{}. '
             'The first camp youth centre in the West Bank to be closed was Qalandiyā’s, on 13 December 1981{}. '
             'In the Gulf War of 1991 the army took over the Girls’ Secondary School and made it a barracks{}, and from 1990 families who had worked in Kuwait came home{}.'.format(
            c('Birzeit University, Right to Education campaign, “History of the Campaign.”'),
            c('Rania Alazzeh, <i>Jerusalem Quarterly</i> 94 (2023), p. 37.'),
            c(NIR + ', p. 367.'), c(NIR + ', p. 181.')))
        + _p('<b>27 December 1995.</b> When the army left, crowds came out to welcome the National Security forces and the police. Ramallah, Nayrūz writes, had spat out the occupation after nearly thirty years{}.'.format(
            c(NIR + ', p. 381, which prints the year as 1994; the Institute for Palestine Studies gives 27 December 1995.'))))

    add_body('The second intifada and the siege', _p(
        '<b>Bayt Rīmā, October 2001.</b> The first great raid into land the Authority ran came to a village of our district. At half past one in the morning of <b>24 October 2001</b> undercover units, tanks, bulldozers and helicopters entered Bayt Rīmā. '
        'Three men of the National Security Force and two policemen were killed and at least seven people hurt. Ambulances were kept from the wounded until seven, and three family homes were blown up{}.'.format(
            c(HRW02 + ', pp. 9–12.')))
        + _p('<b>The ministries.</b> Ramallah was the first city taken in 2002. The United Nations counted <b>21</b> offices of the Authority damaged, about <b>$8 million</b> of loss, and found that the town’s place as the seat of government “appeared to be a factor.” '
             'The records of the ministries of Education, Health and Finance and of the Central Bureau of Statistics were carried off{}.'.format(
            c(UN186 + ', paras 71–73.')))
        + _p('<b>A village held together from abroad.</b> Al-Mazraʿa al-Sharqiyya, fifteen kilometres north-east of the town, had 3,660 people at home in 1997 and 8,685 abroad. '
             'Its elected council had resigned in 1988 after the army killed two of its young men, and it had none until 1996. In the closures after 2000 the money sent from abroad kept it going. '
             'Soldiers raided the youth club and it closed. A stone-cutter could no longer reach Jerusalem, and in two years more than forty families, about two hundred people, emigrated{}.'.format(
            c(DSP04 + ', pp. 20–26.'))))

    add_before_unknown('The Wall, a capital, and our own people',
        _p('<b>The villages that marched.</b> West of the town the Wall and the settlement plans beside it took land from Bilʿīn, Niʿlīn and Dayr Qaddīs{}. '
           'From February 2005 <b>Bilʿīn</b> marched every Friday. <b>Bāsim Abū Raḥma</b> was killed by a tear-gas canister on 17 April 2009, and his sister <b>Jawāhir</b> died after breathing tear gas at the march on 31 December 2010{}. '
           'At <b>Nabī Ṣāliḥ</b> the marches began in 2009, over land and springs taken by the settlement of Ḥallamish, and <b>Muṣṭafā al-Tamīmī</b>, twenty-eight, was hit in the face by a canister on 9 December 2011 and died the next day{}.'.format(
            c(ARIJ15 + ', PDF p. 60.'), c('Al Jazeera, 7 January 2011.'), c('Al Jazeera, 11 December 2011.')))
        + _p('<b>Turmus ʿAyyā, 2023.</b> Turmus ʿAyyā, known for its many American citizens, was burned on <b>21 June 2023</b>. About four hundred settlers came; thirty homes and more than sixty cars were set alight, twelve people were wounded by live fire, and <b>ʿUmar Qaṭīn</b>, twenty-seven, an electrician, was shot dead. '
             'A Chicago man’s brother lost his house, and a family from Ohio lost four cars{}.'.format(
            c('Al Jazeera, 21 June 2023, citing the mayor, Lāfī Adīb, through WAFA.')))
        + _p('<b>2025.</b> At <b>Kafr Mālik</b> on 25 June settlers burned cars and homes, and when the villagers faced them three were shot dead: <b>Luṭfī Ṣabrī Buʿayrāt</b>, twenty, <b>Murshid Nawwāf Ḥamāyil</b>, thirty-six, and <b>Muḥammad Qāhir al-Nājī</b>, twenty{}. '
             'At <b>Ṭaybeh</b>, the Christian village where Ḥannā Khalaf once hid, a fire set on 7 July reached the ruins of the fifth-century church of St George, and on 14 July the patriarchs came to stand with the village{}. '
             'On 20 August Israel gave final approval to about 3,500 homes at <b>E1</b>, on one of the last links of open land between Ramallah and Bethlehem{}. '
             'By the count of the Applied Research Institute, 2025 was the worst year yet. Of 65 new outposts in the West Bank, <b>14</b> were in the Ramallah governorate, and the governorate had more settler attacks than any other (as of February 2026){}.'.format(
            c('Palestinian Centre for Human Rights, 27 June 2025.'),
            c('Vatican News, 15 July 2025.'),
            c('Al Jazeera, 20 August 2025.'),
            c(POICA + '.')))
        + NUMTABLE('THE WARS AROUND US, 1911–2025 — what reached Ramallah',
            ['When', 'War', 'What reached the town'],
            WARS_AROUND_US,
            'The wars felt only from a distance are listed too, so that none is left out. The sources are in the entries of chapters 10 to 12.'))

    # ---- v105, the war list folded in (David, 18 Nov 2026: "Fold it in").
    # Sources: /mnt/project-files/history/conflicts_1936_present/v2_2026-11-17/ (YOUTH_EXTRAS.md, CASUALTY_LISTS.md,
    # INTIFADAS_in_Ramallah.md, NAMES_VS_FAMILY_TREE.md) and the B'Tselem exports of 17 Nov 2026 (support only).
    FT26 = 'AFRP family tree, export of 17 November 2026, the notes on each record'
    WAFA = 'WAFA, Palestinian News and Information Agency, the register of martyrs'
    PCBS = ('Palestinian Central Bureau of Statistics, <i>Killed in the al-Aqsa Intifada by district, 29 September 2000 – 31 December 2009</i>: '
            'Ramallah and al-Bīra, 182 killed (163 men, 19 women), 49 of them under eighteen')
    BARG = 'Mourid Barghouti, <i>I Saw Ramallah</i>, trans. Ahdaf Soueif (Cairo: American University in Cairo Press, 2000)'

    add_before_unknown('The war, the locusts', _p(
        '<b>The men who did not come home.</b> The family tree’s own notes name the dead of these years one by one. '
        '<b>Butrous Ibrahim Elias Saah</b> was drafted and never returned. <b>Ibrahim Daoud El-Karawat</b> died in the Turkish army, and <b>Anton Hanna Omran</b> was killed. '
        'The notes also mark as dying in the war years Mikhail Saleh Ayoub El-Safadi, Nicola and Elias Ayoub Danfoura, Yousef Hanna Mousa Ahwal, '
        'the brothers Bajis, Aziz and Mousa Khalil, and the infant Nicola Badran. Two sons of Ramallah who had emigrated, <b>Jameel Abdallah Mikhail</b> and <b>Najeeb Farhat</b>, died in the uniform of the United States army{}.'.format(
            c(FT26 + '. The tree records a death in these years for each; the cause is given only where we print it.')))
        + plate('p092_2.jpg', 91, 'Dr Jameel Izhaq, photographed in 1938. His whole family died in the typhus of 1916, the year in which, by Shaheen’s count, about three in ten of the people of Ramallah died.')
        + plate('p341_2.jpg', 340, 'ʿAzeez and Selma Shaheen at their fig grove, 5 August 1984. In the hunger of the First World War, they said, the figs kept them alive.')
        + plate('p247_1.jpg', 246, 'Four elders of Ramallah about 1916, photographed by Khalīl Raʿad: Farhat el-Muhawi, Yousef el-Katsha, Hanna el-Muhawi and Shaheen ʿAudi Muhawieh.'))

    add_before_unknown('The revolt reaches the town', _p(
        '<b>The barricades.</b> On 1 October 1938, the lawyer ʿĪsā Qandaḥ remembered, the young men of the town built barricades of stone across the streets to stop the British armoured cars, '
        'while British aircraft fought the rebels in the hills around{}.'.format(c(NIR + ', p. 96, from ʿĪsā Qandaḥ (interview, 2 August 2003).')))
        + _plate('matpc_18762.jpg', '../img/loc/matpc_18762.jpg', '“Airplane engagement over Ramallah with Arab rebels,” 1 October 1938. The dots in the sky are British aircraft.',
                 'Matson Photo Service, 1938. Library of Congress, Prints &amp; Photographs Division, Matson collection, matpc-18762. ' + RIGHTS['loc'], 'Photograph')
        + plate('p262_3.jpg', 261, 'George Saah, “George al-Aqraʿ”, hanged by the British in the Jerusalem prison on 16 November 1939.')
        + plate('p060_1.jpg', 59, 'Dr Daoud Mikhail in the dress of the countryside, which townsmen put on in the revolt of 1936 so that the rebels could not be told apart.'))

    add_body('The Second World War',
        plate('p283_1.jpg', 282, 'The Trans-Jordan Frontier Force in the 1930s. Ramallah men served in it, Elias Nasrallah Oudeh among them.')
        + plate('p093_2.jpg', 92, 'Edward Salamy of Ramallah in the uniform of the United States army in the Second World War, in Panama.'))

    add_body('Where the refugees lived',
        plate('p186_1.jpg', 185, 'Refugee children being fed. The photograph, from the Friends’ archives, is stamped 9 April 1949 and was probably taken near Ramallah.'))

    add_before_unknown('Under the Jordanian crown',
        plate('p100_1.jpg', 99, 'The National Security Force drilling in Ramallah at the time of the Suez war, 1956.')
        + plate('p192_1.jpg', 191, 'Ramallah Scouts serving in the National Guard, 1956.')
        + plate('p125_1.jpg', 124, 'Prisoners in al-Qashla prison, Jerusalem, 1957. Second from the right is Ṭalʿat Ḥarb of Ramallah, who was jailed for thirteen years in all for calling for democracy and for Glubb’s dismissal.'))

    add_body('The counting years',
        plate('p275_1.jpg', 274, 'The High Commissioner and his staff about 1931, with the Ramallah attorney ʿIsa ʿAkel and Naseef Harb.'))

    # 22 Nov 2026: the date stays open (tree 1947; Cadora 18 April 1948; Christina Jones about 13-14 April 1948), so both dates are printed

    add_before_unknown('The first intifada, and the Authority', _p(
        '<b>Help from America.</b> Ramallah people in the United States raised more than $300,000 in the first intifada. It went home in instalments, through known men of the town, to families in need, '
        'and from it grew the <b>Sons of Ramallah</b> society{}. '
        'At the entrance to Dayr Ghassāna a monument stands for <b>Luʾay</b> of Dār Dāwūd, shot there{}.'.format(
            c(NIR + ', p. 315.'),
            c(BARG + ', p. 75. Barghouti gives no date. <b>Inference, labelled:</b> we place him in the first intifada.')))
        + _p('<b>Seventeen from the district.</b> The seven killed in the town in September 1996 were part of a larger loss. WAFA names <b>17</b> people of Ramallah governorate killed between 25 and 27 September, '
             'and a United Nations report agrees. The youngest was <b>Rāʾid Ibrāhīm Sharāka</b>, fourteen, of al-Jalazūn camp{}.'.format(
            c(WAFA + ', Ramallah governorate, September 1996; United Nations, A/52/131.'))))

    add_before_unknown('The second intifada and the siege', _p(
        '<b>The count.</b> In the intifada’s first nine years, from 29 September 2000 to the end of 2009, <b>182</b> people of Ramallah and al-Bīra district were killed. <b>Forty-nine</b> of them were children{}. '
        'In April 2002 the hospital morgue filled. When the curfew was lifted for two hours, hundreds of people came out and buried the dead together in the hospital yard{}. '
        'Since 1971, <b>21</b> people of the district have died in Israeli prisons and detention{}.'.format(
            c(PCBS + '.'), c(NIR + ', p. 74.'), c(WAFA + ', deaths in custody, 1971–2025.'))))

    add_before_unknown('The Wall, a capital, and our own people', _p(
        '<b>The homes.</b> Building in Area C needs an Israeli permit, and permits are almost never given. Since 2006 the army has demolished <b>482</b> buildings in the governorate “for lack of a permit,” '
        '<b>191</b> of them homes, leaving <b>1,064</b> people homeless, <b>573</b> of them children. The worst year was 2025, with 88. '
        'The Bedouin of al-Muʿarrajāt lost 34 buildings, and 190 of their people their homes{}.'.format(
            c('B’Tselem, demolitions database, exported 17 November 2026. B’Tselem is an Israeli rights group, so these figures are support only; we have found no Palestinian count by village and year.'))))

    # ---- v98, the context boxes (David, 17 Nov 2026: "This is great").
    # Text: /mnt/project-files/history/conflicts_1936_present/v2_2026-11-17/CONTEXT_BOXES.md, numbers rechecked against the book.
    # Each box sits at the head of its conflict: the entry's opening, or the paragraph that begins with `at`.
    for (prefix, at, era, big, ground, why) in CONTEXT_BOXES:
        box = _ctx(era, big, ground, why)
        i = idx(prefix)
        if at is None:
            E[i] = E[i][:6] + (box + E[i][6],) + E[i][7:]
        else:
            mark = '<p><b>' + at
            k = 6 if mark in E[i][6] else 7
            assert E[i][k].count(mark) == 1, (prefix, at)
            E[i] = E[i][:k] + (E[i][k].replace(mark, box + mark),) + E[i][k + 1:]

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
/* v98: the context boxes for younger readers (src/modern.py) */
.ctxbox{margin:12px 0 16px;padding:9px 14px 6px;background:#F4EFE6;border-left:3px solid #9A6324;font-size:.86rem;line-height:1.45;color:#3A3730;break-inside:avoid}
.ctxbox .ck{font-variant:small-caps;text-transform:lowercase;letter-spacing:.14em;color:#9A6324;font-size:.8rem;margin:0 0 5px}
.ctxbox p{margin:0 0 6px;text-indent:0!important}
.ctxbox b{color:#1A1915}
@media (max-width:520px){.ctxbox{margin:10px 0 14px;padding:8px 11px 4px;font-size:.84rem}}
"""


def finish(html):
    """The panels' style; v105: Steadfast and the memorial close chapter 12."""
    import steadfast
    mark = '<div class="erahead" id="ch13">'
    assert html.count(mark) == 1, 'chapter 12 end'
    html = html.replace(mark, steadfast.html() + mark)
    return html.replace('</style>', CSS + steadfast.CSS + '</style>', 1)
