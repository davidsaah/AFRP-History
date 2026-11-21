# -*- coding: utf-8 -*-
"""v107: "What we have found" — the book's open questions answered from the literature.

Each chapter's box stands immediately before its "What we still don't know" box.
Only answers the researchers graded RESOLVED or RANGE, at medium confidence or
higher, are printed here. The full list, with the questions still open and what
was searched, is docs/ANSWERS_v107.md.

ANSWERS = {chapter: [(question, status, html text, source line), ...]}
status is 'resolved' or 'range'.
"""

ANSWERS = {
 1: [
  ('When were the terraces first built?', 'range',
   'No terrace wall around our town has been dated directly, because a wall that is repaired every year '
   'keeps no layers. The oldest terraces we can tie to a dated village are at Khirbet Raddana, on our own '
   'ridge, where farmers levelled the slopes around their houses about 1200 to 1000 BC. An earlier start, '
   'about 3000 BC, has been proposed but not shown. Most of the walls standing today were rebuilt, stone by '
   'stone, in the last five or six centuries.',
   'Nayrūz (2004), p. 143; Ghadban (2015), pp. 39 and 42; OSL dates of standing terraces from Israeli '
   'studies (web), context only.'),
  ('How old is the Shuqba layer?', 'range',
   'The layer that held the Neanderthal tooth has never been dated directly. The team that studied the '
   'tooth places it, from the animal bones found with it, in the time when Neanderthals lived in this land, '
   'roughly seventy to fifty thousand years ago. That is an estimate, not a date, and a published reply '
   'disputes what the tooth was found with.',
   'Blinkhorn et al., <i>Scientific Reports</i> 11 (2021), discussion. Web only; nothing on our shelf.'),
  ('How settled were the Natufians?', 'range',
   'Scholars now describe them as settled in some places and seasons and on the move in others. At their '
   'main sites in the hills, families stayed in stone houses for much or all of the year; in drier country '
   'and harder times they moved again. They were not the first people to stay put, but they were the first '
   'here to make a habit of it.',
   'Ghadban (2015), p. 39; Edwards (1989) and Maher et al. (2012), web; Israeli site studies context only.'),
 ],
 2: [
  ('Where did the Philistines’ southern-European ancestry come from?', 'range',
   'The genes cannot yet name the homeland. The newcomers’ ancestry matches Bronze Age people of the Greek '
   'islands, Sardinia and Spain about equally well, because those peoples were themselves alike; the Aegean '
   'is the most often favoured. What the genes do show is the ending: within two hundred years the newcomers '
   'had married into the people already here.',
   'Feldman et al., <i>Science Advances</i> 5 (2019). Web only; no ancient-DNA paper on our shelf.'),
  ('Is there an Iron Age village under the old town?', 'resolved',
   'None has ever been reported. What has been found in the old town, a watchtower, a church and an oil '
   'press, is Crusader, and no one has dug beneath it. The Iron Age village of our ridge is Khirbet Raddana: '
   'an open village without walls, where farmers stored wheat, cast bronze in their own workshop and '
   'gathered the rain from their terraces into cisterns cut in the rock. It now lies under apartment blocks.',
   'Nayrūz (2004), pp. 53 and 137–144; the Greenberg and Keinan gazetteer (Israeli), context only.'),
 ],
 3: [
  ('When was Gerizim’s first sanctuary, and when did the Samaritans part from Judaism?', 'range',
   'The first sanctuary on Gerizim goes back to the Persian period, sometime between about 450 and 330 BC. '
   'The parting of Samaritans and Jews was not one quarrel on one day. It grew over three or four centuries, '
   'hardened when the Hasmoneans burned the sanctuary about 110 BC, and was complete by the time of the '
   'Gospels.',
   'Web summaries of the excavation (Magen, Israeli, context only) and of Pummer (2016) and Knoppers (2013), '
   'which were not read for this answer.'),
 ],
 4: [
  ('What became of al-Ḥārith’s family after 594?', 'range',
   'The family does not vanish with the Greek writers. Al-Ḥārith’s grandson Jafna was back in Roman service '
   'by 587. Al-Mundhir was still alive in exile in Sicily in July 600, when the Pope himself pleaded for him, '
   'and he came home in 602. Their people fought the Persians on their own ground in 613 and lost, and after '
   'that the house is a name in Arabic poetry until the conquest.',
   'Shahîd, <i>BASIC</i> I.1 (1995), pp. 554–564, 602–605, 618–619, 636–645; Nöldeke (1887).'),
  ('When did the dam at Maʾrib finally fail?', 'range',
   'The last repair carved in stone is from 557/558, and the Qurʾān, revealed at Mecca before 622, already '
   'speaks of the flood as past (Sūrat Sabaʾ 34:15–16). So the dam gave way for the last time somewhere in '
   'those sixty years, most likely late in the sixth century. The familiar 570 or 575 is a later reckoning '
   'that sits inside that window.',
   'Robin (2002), p. 54; Shahîd, <i>BASIC</i> II.1 (2002), pp. 18–19.'),
 ],
 6: [
  ('Is Qalāwūn’s deed known?', 'resolved',
   'The deed itself is lost, but its terms outlived it. Later writers say it gave a tenth of the hill’s '
   'harvest to the sanctuary of Abraham at Hebron; Ottoman clerks went on collecting that share, and in 1838 '
   'the Jerusalem mosque still drew rents from Ramallah and Ṭaybeh. Two Jerusalem court records cite the '
   'deed and disagree on its year: the record of 1565 gives 678 AH (1279–80), and a record of 1644 gives '
   '640 AH (1242–43).',
   'Ḥammūdeh (2014), p. 40 and nn. 17–18, citing Rabāyiʿa (2008), p. 102; Nīrūz (2004), pp. 44–45; '
   'Robinson (1841), II, p. 513.'),
  ('When did our people make the journey from the plateau?', 'range',
   'No paper describes the road, but the papers mark where it ran. Christians from Karak were on the land at '
   'Kusbār, by Ḥalḥūl, after 1539. Their families were registered at Bayt Jālā by 1553–54 and stood in a '
   'Jerusalem court as people of Ramallah on 1 April 1561. So our people left the plateau between about 1539 '
   'and 1553, most likely in the 1540s. Between about 1538 and 1596 Karak lost about forty Christian households, close '
   'to the thirty-six counted at Bayt Jālā; that the two are the same families is our inference.',
   'Ḥammūdeh (2014), pp. 44–48 and nn. 57–62; Abū al-Shaʿr, <i>Tārīkh Sharq al-Urdun</i>, p. 80, via Ḥammūdeh.'),
  ('Which village is on Niʿma ibn Bishāra’s contract?', 'range',
   'The editors read the place as “Jifnā al-Jawz” and put a question mark after it. The first word is most '
   'likely our neighbour Jifnā, a Christian village then as now: a man of Jifnā signed a Frankish charter in '
   '1182, and another, Mūsā al-Jufnāwī, carved his name over the door of a desert monastery. What the second '
   'word means, nobody yet knows.',
   'Aljoumani, Bhalloo and Hirschler (2024), pp. 48 and 175; <i>Survey of Western Palestine</i> III (1883), '
   'pp. 197–98.'),
  ('Were there Christian Ghassanids at Karak or Shawbak?', 'resolved',
   'Irfan Shahîd places the Ghassanid king in Moab around the year 600, in a land running from Rabba, beside '
   'Karak, to the southern end of the Dead Sea, and al-Yaʿqūbī in the ninth century still found Ghassān at '
   'Gharandal, south of Karak. But no writer we have read names a single Christian Ghassanid living at '
   'Karak or Shawbak in the centuries after.',
   'Shahîd, <i>BASIC</i> II.1 (2002), pp. 61–62, 247–48, 346–47; Zahran (2006), pp. 149–50.'),
 ],
 7: [
  ('Who are the eighty heads of household of 1596?', 'resolved',
   'Naseeb Shaheen, who read the register, found that its seventy-one Christian names are the same names as '
   'in 1562, copied over unchanged after thirty-four years. To them it adds nine Muslim households. So the '
   '1596 count is the 1562 list carried forward, not a fresh count; only the nine Muslim names are still to '
   'be read, in the published register.',
   'Shaheen (2005), II, pp. 22 and 32; Ḥammūdeh (2014), p. 47.'),
  ('Where does “143 Christian households at Karak” come from?', 'resolved',
   'From Hind Abū al-Shaʿr’s reading of a detailed register of the ʿAjlūn district, with 11 more at Shawbak. '
   'The “970” cited with it is the register’s number, TD 970, not the year 970 AH; the register belongs to '
   'the middle of the century, about 1538. By 1596 the same town had 103 Christian households.',
   'Ḥammūdeh (2014), n. 57, citing Abū al-Shaʿr, p. 80; Bani Issa (2023) for the date of TD 970.'),
  ('Was Rāshid’s father ʿĪsā or Ṣaqr?', 'range',
   'Our Arabic sources on both sides of the Jordan, from Khalīl Abū Rayya in 1980 to the Ḥaddādīn of Karak '
   'today, name him Ṣaqr; only one Ramallah chart names him ʿĪsā. So we follow Ṣaqr and keep ʿĪsā beside '
   'him. ʿĪsā may have been Ṣaqr’s own given name, or Ṣaqr’s father, and neither is proven.',
   'Ḥammūdeh (2014), p. 43; Nīrūz (2004), pp. 186–87; al-Farḥān; the Karak diwan (2022).'),
  ('What does “1561” at the hub of the Karak wheel mean?', 'range',
   'Most likely the year our people first appear on paper as people of Ramallah, in the Jerusalem court '
   'record of 1 April 1561. Family writers have long quoted that year as the documented arrival, and the '
   'chart sets it beside the founder’s father as a marker for his generation. It is not his birth year.',
   'Cadora, restored edition, p. 110 (foreword); Ḥammūdeh (2014), pp. 47–48.'),
  ('Is the name in the registers Ḥadīd or Ḥaddād?', 'range',
   'Everyone who has read the registers reads Ḥadīd, “iron”, and so does a Jerusalem court in 1604, which '
   'records a Ramallah clan called “the sons of Ḥadīd”. Sāmiḥ Ḥammūdeh takes that clan to be the Ḥadāda, the '
   'line of Rāshid’s eldest son Ḥaddād. The reading is firm; that identification is reasonable but unproven.',
   'Ḥammūdeh (2014), pp. 45–49; Shaheen (2005), II, p. 27.'),
 ],
 8: [
  ('Can we name the first families before 1700?', 'range',
   'No parish book names them, but the Ottoman clerks and the Jerusalem court did. In 1562 they wrote down '
   'Jarīr son of Ḥadīd, Sālim and Dīb sons of Jiryis, and ʿUmrān and ʿUmayra sons of Ḥassān, and in 1604 the '
   'court heard a quarrel between ʿUbayd son of Ghānim “of the sons of Ḥadīd” and Musliḥ son of Ibrāhīm “of '
   'the sons of al-Naqqāsh”. Ḥammūdeh reads these men as Rāshid’s grandsons, which would put the founders '
   'themselves about 1520–60. The first Ramallah-born priest, Yaʿqūb Ilyās, was ordained in 1700.',
   'Ḥammūdeh (2014), pp. 45–49 and n. 74; Shāhīn (1982), English, chronology; Nīrūz (2004), p. 353.'),
  ('What do we know of the town from 1565 to 1800?', 'range',
   'The record is thin but not empty. The court heard Ramallah’s quarrels and debts in 1604 and 1605, '
   'Ramallah men helped roof the Church of the Nativity in 1671, the town had its own priest by 1700 and a '
   'paid parish school by 1706, and in the 1770s al-Jazzār took our masons to rebuild Acre. Most of the '
   'eighteenth century reaches us as family memory, and its dates differ from book to book by up to a '
   'generation.',
   'Ḥammūdeh (2014), p. 49 and n. 74; <i>Analekta</i> II (1894); Nīrūz (2004), pp. 254–55, 353.'),
  ('Whose feud was it in 1820?', 'resolved',
   'The Shakara’s. Cadora in 1954 and Shāhīn in 1982 both tell it as a fight inside the Shakara clan, and '
   'the Abū Hānī family at its heart is a Shakara family. Shaheen’s one-line “Sharaka” is best read as a '
   'slip: the Sharaka had their own quarrel about 1850, when the whole clan left for Bayt Ijzā for a year.',
   'Cadora (1954), p. 30 (restored ed., p. 41); Shāhīn (1982), English, p. 33 and chronology; '
   'Shaheen (1992), p. 23.'),
 ],
 9: [
  ('Where does the story of the Rafeedie’s arrival come from?', 'resolved',
   'It is in print long before Ḥammūdeh. Elihu Grant, teaching in Ramallah about 1904, wrote that al-Bīra’s '
   'one Christian family, about eighty strong and kin to a Ramallah household, took its name from “a town '
   'near Nablus” and had come from there. Ibrāhīm Nīrūz heard the fuller story from the lawyer ʿĪsā Qandaḥ: '
   'a killing at Rafīdiyā about 1750, a refusal at Jifnā, a welcome in Ramallah and an invitation from '
   'al-Bīra. The year 1750 rests on that one account.',
   'Grant (1907), p. 209; Nīrūz (2004), pp. 196–97.'),
  ('Where were Judge Edward Rafeedie’s parents from?', 'resolved',
   'His father, Fūteh (Fred) Salāmeh Rafeedie, was of al-Bīra, and his mother, Nabīha Hishmeh, was born in '
   'Ramallah on 5 May 1905. So the judge was of the al-Bīra family, and his mother of a Ramallah one.',
   'Shāhīn (1982), Arabic, the Hishmeh family; Ramallah Family Tree Book v117, trees 24 and 162; Prabook (web).'),
  ('When was St Andrew’s built?', 'range',
   'It was begun in 1887 and opened in 1888, as the inscription over the door of its old hall records, and '
   'as Ibrāhīm Nīrūz gives it from the diocese’s own history; Shāhīn has 1887. Cadora’s 1855 is earlier than '
   'any mission worker living in Ramallah, and it most likely marks the start of the mission’s work here, '
   'not the building.',
   'Nīrūz (2004), pp. 286–87, citing Faraḥ (1991), I, p. 339; Shāhīn (1982), English, p. 62.'),
 ],
 10: [
  ('What happened in Ramallah in 1929?', 'resolved',
   'In 1929 our town had one Jewish household: a shoemaker the town called Abū Ibrāhīm, who worked in a shop '
   'belonging to the Orthodox priest Khūrī Yūsuf Ḥarb. That year a young man of the town beat him, and only '
   'the priest’s intervention saved his life. He moved his family to Jerusalem. In 1967 his grandsons came '
   'back to Ramallah to ask after the priest’s family and offer them help, as Ṭalʿat Ḥarb, the priest’s '
   'grandson, remembered. The month of the beating is not recorded.',
   'Nayrūz (2004), pp. 303–304, from ʿĪsā Qandaḥ and the memoir of Ṭalʿat Ḥarb.'),
  ('How many of our men served and died in the First World War?', 'range',
   'The sources agree on “about thirty” but not on what the thirty were. Shāhīn and Shaheen count about '
   'thirty who died in the Turkish army; Nayrūz counts about thirty men of the town who went to the war at '
   'all. Every man of eighteen to forty-five was called; some paid the fine of fifty gold pounds and some '
   'hid in the vineyards. The family tree names five who died in Ottoman service, among them Khalīl Manṣūr '
   'and Buṭrus Ibrāhīm al-Saah, and about seven more who died in the war, place unstated. So the dead in arms '
   'were between five and twelve named men and about thirty remembered.',
   'Shāhīn (1982), English, chronology; Shaheen (1992), p. 160; Nayrūz (2004), p. 56; Cadora (1954), p. 53; '
   'Ramallah Family Tree Book v117.'),
  ('When were our Christians first conscripted?', 'range',
   'The law came first and the call-up later. Christians were made liable by the law of 1909, though Shāhīn '
   'remembered it as 1905. By the Balkan wars of 1912 and 1913 Ramallah men such as Mūsā Ḥraiz were already '
   'in uniform. The great call-up came with the war in 1914, and for a while a family could still buy its '
   'son out a year at a time: Khalīl Manṣūr was bought out twice, and in the third year he was taken and did '
   'not come back.',
   'Shāhīn (1982), Arabic, p. 60; Nayrūz (2004), p. 55; Shaheen (1992), pp. 160–61; Khoury (2022), p. 88.'),
  ('What was the radio raid of May 1944?', 'resolved',
   'On the night of 17 May 1944 armed men of the Irgun, the Zionist underground then fighting the British, '
   'broke into the transmitting station at Ramallah, disarmed the guard and tried to force the operator to '
   'put them on the air. When he refused they shot up the equipment and fled. On the road outside town the '
   'same night two Arab travellers were wounded. The British and the newspapers of the day disagree on how '
   'many attackers there were and whether any policemen were hurt.',
   'Hansard, HC Deb 6 December 1944, vol. 406, cc. 557–61W; JTA, 21 May 1944. Web only; no Palestinian '
   'source found yet.'),
  ('Whom did the revolt of 1938 cost us?', 'range',
   'We can name one son of the town who died for the revolt: George al-Saah, “George al-Aqraʿ”, of the '
   'ʿAwwād, taken at Jifnā with a group of fighters and hanged by the British, and mourned for days in the '
   'Kharja square. Of those killed in the fighting of 1 October 1938 we have counts, not names: two women '
   'and three men in the vineyards, and from more than twenty to about eighty fighters, as the witnesses tell it. After the '
   'searches the British left food stores ruined and some houses burned.',
   'Nayrūz (2004), pp. 95–96, 113, 260–61; McDowell (1939), pp. 28, 45–47; Cadora (1954), p. 57.'),
  ('Who brought the election case of 1946?', 'resolved',
   'It was a petition against the election of Jalīl Ḥarb, the fourth winner, brought by men of the Jābir '
   'side. Saʿīd Buluṣ Jābir, a voter in the district, gave evidence as petitioner, the lawyer Mughannam '
   'argued for them, and the Atalla brothers argued to keep the result. It was heard before a judge between '
   '29 October and 7 December 1946. The judgment has not been found, but the two families of Dār Yūsuf, the '
   'Jābirs and the Ḥarbs, held their feasts of reconciliation about 1949.',
   'Israel State Archives, P-213/40, PDF pp. 42, 50, 53–55, 61, 69; Shaheen (1992), p. 220.'),
  ('Is the councillor of 1946 our historian?', 'resolved',
   'Yes. Yūsuf Jiryis Qaddūra was mayor from 1943 to 1947, as he tells it himself and as Nayrūz and Shaheen '
   'record. He stood in the Ḥaddāda district in April 1946, was elected second, served again as acting mayor '
   'in 1948, and in New York in 1954 published the town’s first history.',
   'Cadora (1954), pp. 69–72; Nayrūz (2004), p. 387 and n. 65; Shaheen (2005), p. 17.'),
  ('Are the Ḥasāsna of the 1946 lists the Hasasneh?', 'resolved',
   'Yes. The column is headed <span class="ar">الحساسنه</span>, al-Ḥasāsna: the Hasasneh, the house of '
   'Ḥassān son of Rāshid. In court the chairman counted the same five men “from Haasassneh”.',
   'Israel State Archives, P-213/40, PDF pp. 63 and 122; Cadora (1954), p. 31; Nayrūz (2004), p. 191.'),
 ],
 11: [
  ('Who leased the land of al-Jalazūn?', 'range',
   'The camp was set up in 1949 on about 253 dunums of rocky hillside, first by the Red Cross, and UNRWA '
   'took it over in 1950. UNRWA’s lease was with the Jordanian government; most of the land was state '
   'land, and the rest belonged to families of Jifnā and nearby. One account gives the lease a term of '
   'ninety-nine years. No source produces the deed.',
   'UNRWA camp profile; OCHA (2008); palquest; B’Tselem (2018, Israeli NGO, context only). Web only.'),
  ('When did Jordan’s radio leave Ramallah?', 'range',
   'Jordan took over the Mandate station at Ramallah on 15 May 1948. The kingdom’s radio opened its own '
   'broadcasting house in Amman on 1 March 1959, after a second studio there from about 1956, but the '
   'Ramallah transmitter kept working until 1967.',
   'Cadora (1954), “The Broadcasting Station”; Nīrūz (2004), p. 344 and n. 30; Jordanian sources for 1959 (web).'),
  ('Did 1,500 of 6,000 leave by 1946 or by 1956?', 'resolved',
   'By 1946. Shāhīn’s table of emigrants opens with 1,500 in 1946, and his English text says the same.',
   'Shāhīn (1982), Arabic, p. 22; English, p. 28.'),
 ],
 12: [
  ('How many of the district died in the first intifada?', 'range',
   'The town has not yet gathered the names. In the uprising’s first two years, from December 1987 to '
   'November 1989, Israeli forces killed forty-nine people of Ramallah district. By the end of the uprising '
   'the district’s dead were probably between seventy and a hundred; that projection is ours. The popular '
   'committees were outlawed in the summer of 1988, on 1 July or 18 August by different accounts.',
   'B’Tselem, <i>Annual Report 1989</i>, pp. 19–23 (Israeli NGO, used for its count); Johnson, <i>JPS</i> 18 '
   '(1989), p. 94; Tamari, <i>JPS</i> 20 (1991), n. 39.'),
  ('When was the Federation incorporated?', 'range',
   'In Michigan in 1959, the year the clubs met in Detroit and resolved to unite; Shāhīn has 1958. The '
   'government recognised it as a non-profit in August 1963.',
   'Shaheen (2005), pp. 354–55; Shāhīn (1982), English, chronology; ProPublica, EIN 38-6096448 (web).'),
  ('When did Ramallah’s Muslims become the majority?', 'range',
   'In the count of 1967 Ramallah was still 59.4 Christians in every hundred of known religion, and by 1997 it was 32. No '
   'count in between asked anyone’s religion, but after 1967 the Christian number could only fall while the '
   'town grew around it. Muslims most likely became the majority in the 1970s, and certainly before the '
   'mid-1980s.',
   'Nīrūz (2004), pp. 179–83; Israeli CBS, <i>Census of Population 1967</i>, vol. 1, p. XII (Israeli state source); Taraki, <i>JPS</i> 37:4 (2008), n. 21.'),
 ],
 13: [
  ('What is Shāhīn’s figure of 13,500?', 'resolved',
   'It is a local count of the town in 1953 (Jordan held no census that year): 4,500 natives and 9,000 refugees and others, 13,500 in all. It '
   'is not from the Ottoman census book, which Shāhīn cites only for names and births.',
   'Shāhīn (1982), English, p. 27; Arabic, p. 22.'),
 ],
}

LABEL = {'resolved': 'resolved', 'range': 'a range'}


def render(ch):
    """The 'What we have found' box for chapter ch, or '' if it has none."""
    items = ANSWERS.get(ch)
    if not items:
        return ''
    out = ['<div class="found"><h4>What we have found</h4>']
    for q, status, text, src in items:
        out.append(f'<p><b>{q}</b> <span class="st">{LABEL[status]}</span> {text} '
                   f'<span class="src">{src}</span></p>')
    out.append('</div>')
    return ''.join(out)
