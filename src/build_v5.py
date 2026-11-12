# -*- coding: utf-8 -*-
"""THE ROOTS OF RAMALLAH: A HISTORY OF ITS PEOPLE (formerly "The One Line"), fifth edition — the whole book as a single unbroken chronicle.
Every narrative folded into one chronological line, Adam to today, each entry
carrying its own evidence, figures and tables at its own date. Ends with the
Verdict: origins, the merging into the Palestinian people, and the founding.
Key texts: Shāhīn (1982) and John Mogannam's chart — entries supported by both
carry the TWO WITNESSES badge."""
import sys, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_recon as R
import build_figs2 as F
import build_figs3 as F3
import build_figs4 as F4
import build_atlas as ATLAS
import build_timeline_test as T
import build_figs5 as F5

from paths import out as _out, asset as _asset
OUT = _out('AFRP_The_One_Line_v5.html')
GREEN, RUST, PLUM = '#007A3D', '#A85210', '#6D4E9E'
GOLD, GREY, RULE, FOLIO = '#B98A4E', '#77726A', '#DCD6C9', '#9A958C'
INK, BODY, DARK = '#1A1A1A', '#46423B', '#004A26'

# ─────────────────────────── machinery
CITES = []
def c(t):
    CITES.append(t); n = len(CITES)
    return f'<sup class="cn"><a href="#n{n}" id="r{n}">{n}</a></sup>'

FIGN = [0]
def fig(svg, title, caption, source):
    FIGN[0] += 1
    return (f'<figure><div class="fignum">Figure {FIGN[0]}</div>'
            f'<div class="figtitle">{title}</div><div class="figwrap">{svg}</div>'
            f'<figcaption>{caption}<span class="src">{source}</span></figcaption></figure>')

GRADE = {'scripture':('#D5E9DF','#1A1A1A','SCRIPTURE'),
 'classical':('#A9CDB8','#1A1A1A','CLASSICAL'),'attested':('#79B491','#1A1A1A','ATTESTED'),
 'none':('#FDF6EC','#8A5A1E','NO EVIDENCE'),'documents':(GREEN,'#FFFFFF','DOCUMENTS'),
 'oral':('#F6EEDF','#7A5A28','ORAL TRADITION')}

def FIX(element, correction, justification):
    return ('<div class="fix"><div class="fixhead">A correction</div>'
            '<div class="fixgrid">'
            '<div><span class="fl">As it stood</span>' + element + '</div>'
            '<div><span class="fl">Corrected to</span>' + correction + '</div>'
            '<div><span class="fl">How it is justified</span>' + justification + '</div>'
            '</div></div>')

def NUMTABLE(title, heads, rows, foot=''):
    h = ''.join(f'<th>{x}</th>' for x in heads)
    body = ''.join('<tr>' + ''.join(
        f'<td class="{"lbl" if i==0 else "num"}">{v}</td>' for i, v in enumerate(r)) + '</tr>'
        for r in rows)
    ft = f'<div class="tfoot">{foot}</div>' if foot else ''
    return (f'<div class="ntwrap"><div class="nthead">{title}</div>'
            f'<table class="ntable"><thead><tr>{h}</tr></thead><tbody>{body}</tbody></table>{ft}</div>')

def testtable():
    rows = []
    for yr, claim, verdict, note in T.ROWS:
        bg, fg, lab = T.V[verdict]
        rows.append('<tr><td class="when">' + str(yr) + '</td><td class="what"><b>' + claim + '</b>'
                    '<br><span class="tn">' + note + '</span></td>'
                    '<td class="gr"><span class="g" style="background:' + bg + ';color:' + fg + '">'
                    + lab + '</span></td></tr>')
    return ('<div class="ntwrap"><div class="nthead">THE TEST IN FULL — thirty-six claims, one by one'
            '</div><table class="ttable"><thead><tr><th>Year</th>'
            '<th>What the family’s account says, and what happens when it is checked</th>'
            '<th>Verdict</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>')

D = lambda f: f'<code class="fn">{f}</code>' 

# entry: (date_display, grade, w2:boolean, title, note_html, body_html_or_empty)
E = []
CHAP = [1]

# The twelve chapters of the line, plus the closing verdict. The chapter scheme
# follows the twelve-chapter outline agreed for the book; every entry is filed
# under one of them and the line is assembled chapter by chapter, in order.
CHAPTERS = [
 (1,'ERA ONE','In the Beginning — Two Accounts',
  'Scripture opens with Adam and Eve; the ground opens with a cave in this governorate. <i>Both accounts are printed here, each graded for what carries it, and neither is asked to do the other’s work.</i>'),
 (2,'ERA TWO','The Canaanite Foundation &middot; 3500–1200 BC',
  'The layer everything else is built on. Villages within walking distance of Ramallah, city-states writing to Egypt in Akkadian — and the population from which present-day Lebanese draw more than ninety per cent of their ancestry, and southern Levantine populations a large part of theirs.'),
 (3,'ERA THREE','Coastal and Highland Worlds &middot; 1200–800 BC',
  'Philistines on the coast, Phoenicians to the north, Moab, Ammon and Edom across the Jordan, Aramaeans inland. <i>Every one of them was absorbed. Not one of them replaced the people already here.</i>'),
 (4,'ERA FOUR','Iron Age Kingdoms in Context &middot; 8th–7th c. BC',
  'Assyria pulls these hills into the record of a world empire — and at the far end of a tolled caravan road that ends at Gaza, the kingdom of Sabaʾ builds the dam this family still remembers.'),
 (5,'ERA FIVE','Persian and Hellenistic Palestine &middot; 539–63 BC',
  'The ridge changes empires five times in five centuries and the villages do not move. One community separates on Mount Gerizim, and is still there.'),
 (6,'ERA SIX','Roman and Late Antique Palestine &middot; 63 BC – AD 324',
  'Rome paves the ridge road, ranks this district second after Jerusalem, and writes its villages down — and the Gospels put the Lord on that road eleven kilometres from the future town.'),
 (7,'ERA SEVEN','Byzantine Christian Palestine &middot; AD 324–638',
  'The country becomes overwhelmingly Christian by conversion rather than replacement — Samaritan Samaria and Jewish Galilee remaining. <i>And on the Roman frontier the family’s claimed dynasty walks out of literature into contemporary Greek — just as, a thousand miles south, the dam finally breaks.</i>'),
 (8,'ERA EIGHT','Early Islamic Palestine &middot; 638–1099',
  'The conquest changes the rulers, not the people. The Christian villages of this ridge go on being Christian villages, and go on leaving dated traces.'),
 (9,'ERA NINE','Crusader, Ayyubid and Mamluk Worlds &middot; 1099–1517',
  'The land changes hands around an unmoved population — and in 1186 the name <i>Rām Allāh</i> is written down for the first time, as the place a Crusader king’s road leads to, nearly four centuries before the family arrives to live on the hill.'),
 (10,'INTERLUDE','The Missing Centuries',
  'Four eras have just passed. In every one of them the land is documented and our own line is not. <i>This interlude stops and measures the hole rather than filling it.</i>'),
 (11,'ERA TEN','Ottoman Palestine and the First Traceable Families &middot; 1517–1562',
  'The state starts writing everyone down, village by village and household by household — and for the first time an ancestor of ours is inside a document.'),
 (12,'ERA ELEVEN','Ramallah and Its Founding Families &middot; 1562–1900',
  'The Christian families come up the ridge road from Bayt Jālā — seventy-one Christian taxpayers in the count of 1562, sixty-three households and eight single men — divide the land in fifths, and spend three centuries becoming a town.'),
 (13,'ERA TWELVE','Mandate to Present &middot; 1901–today',
  'The town starts leaving and never stops, is tripled by catastrophe, and becomes a capital almost by accident — and everything it builds afterwards is paid for from both sides of an ocean.'),
 (14,'THE VERDICT','What Is Proven',
  'Three claims, weighed on everything above — and the key dates on one page.'),
]

# where the family's own chain stands in each era: (link text, status, grade)
LINKAT = {
 1:  ('Links one and two of nine &middot; Adam to ʿĀbir, and the branch at ʿĀbir’s two sons',
      'Scripture, and nothing else. No document of any kind reaches this stretch.', 'scripture', 14),
 2:  ('Link four of nine &middot; Qaḥṭān to al-Azd',
      'The genealogists put our line in South Arabia in this era. Nothing datable supports it — and nothing contradicts it.', 'none', 17),
 3:  ('Link four of nine &middot; Qaḥṭān to al-Azd',
      'Still South Arabia; still tradition. Our line leaves no trace in this era anywhere.', 'none', 20),
 4:  ('Link four of nine &middot; Qaḥṭān to al-Azd',
      'The dam is built in the country the tradition names. <b>The place is proven by inscription; the persons are not.</b>', 'classical', 23),
 5:  ('Link four of nine &middot; Qaḥṭān to al-Azd',
      'Nothing datable in our own line for the whole of this era.', 'none', 26),
 6:  ('Link five of nine &middot; al-Azd to Ghassān, named at a water',
      'Classical Arabic scholarship, written down three to six centuries after the fact.', 'classical', 29),
 7:  ('Link six of nine &middot; the Jafnid phylarchs',
      '<b>A Greek historian writing in al-Ḥārith’s own lifetime.</b> This is the hardest evidence in the whole chain, and it is in this era.', 'attested', 34),
 8:  ('Link seven of nine &middot; the void',
      'No names. A Ghassān population is still <i>located</i> in 890 — on the plateau the tradition names — but not one father is named.', 'none', 35),
 9:  ('Link seven of nine &middot; the void',
      'No names. Four dated Christian traces on the ridge and the plateau, and none of them ours.', 'none', 35),
 10: ('Link seven of nine &middot; the void, measured',
      'Nine hundred and thirty-one years, about thirty-one generations — and a name for only the last of them.', 'none', 35),
 11: ('Link eight of nine &middot; Rāshid al-Ḥaddādīn',
      '<b>The registers reach him.</b> From this era on, the line is carried by documents and not by tradition.', 'documents', 66),
 12: ('Link nine of nine &middot; Rāshid to today',
      'Documented the whole way: defters, parish books, censuses, ration cards.', 'documents', 68),
 13: ('Link nine of nine &middot; Rāshid to today',
      'Documented the whole way, and now within living memory.', 'documents', 84),
}


def linkat(n):
    """Where the family's own chain stands as this era opens."""
    if n not in LINKAT:
        return ''
    lab, note, g, upto = LINKAT[n]
    gf, gc, gl = GRADE[g]
    return (f'<div class="linkat"><div class="lkhead">Where our own line stands here</div>'
            f'<div class="lkrow"><span class="lkname">{lab}</span>'
            f'<span class="g" style="background:{gf};color:{gc}">{gl}</span></div>'
            f'<div class="lknote">{note}</div>'
            f'<div class="lkladder">{F4.fig_ladder(upto)}</div></div>')


def sect(label, sub=''):
    """A waymark inside a link. These are the twelve chapters of the country,
    kept as signposts inside the nine links of the family's own chain."""
    E.append(('s', CHAP[0], label, sub))


def CH(n):
    """File everything that follows under chapter n."""
    CHAP[0] = n

# v69 story-check corrections. A body carries a marker such as [[C32]]; ent() swaps it for the box.
V69 = {
 'C11': FIX('The Maʾrib dam as “some five hundred and eighty metres of packed earth faced with stone,” working “something close to thirteen hundred years,” with dam-building at the Wadi Dhana from “around 1750–1700 BC.”',
  'The Great Dam was <b>620 to 680 metres</b> long as its surveyors measured it. One continuous dam dates from the <b>sixth century BC</b>, and the design held for <b>about a thousand years</b>. Flood irrigation in the wadi goes back to the third millennium BC.',
  'Ueli Brunner’s survey (2014) and Kohler (1994) for the dam and its date; Christian Robin (2002) gives 650 metres for the last stage. No specialist source we could find gives 1750–1700 BC, so we have withdrawn it.'),
 'C27': FIX('“For two and a half centuries the men of ʿEin Qīniya, Jifnā and al-Bireh came up this ridge, worked it, and went home at dusk. <b>The Ḥaddādīn were the first to stay the night.</b>”',
  'People lived on this hill before our families did. There was a Mamluk village here, deserted by the end of that period, and four Muslim households in 1538–39. <b>Our families were the first Christians to stay, and they made the village a town.</b>',
  'Sāmiḥ Ḥammūdeh, <i>Jerusalem Quarterly</i> 59 (2014), from the Mamluk papers and the Ottoman registers of 1525–28, 1531–32 and 1538–39. This book’s own table of the registers already showed the Muslim households; the sentence had run ahead of it.'),
 'C29': FIX('“We are in it from the start,” and “the registers that name Rāshid’s children.”',
  'The registers begin in 1525. <b>Our people are in them from 1553–54</b>, at Bayt Jālā, in the fourth survey. No register names Rāshid or a son of Rāshid; they name the Kasābra households, whom Ḥammūdeh takes to be his grandchildren.',
  'This is the book’s own evidence, set out in the chapters that follow. The old wording claimed a generation more than the registers give.'),
 'C32': FIX('“On <b>29 June 1565</b>,” with a note that the entry printed on p. 54 was a different one and that the deed was lost by then.',
  '<b>22 June 1565</b> in the printed edition of the register; Ḥammūdeh gives 29 June. Page 88 of the register and p. 54 of the printed edition are <b>one entry</b>. The deed of 678 AH was <b>shown in court</b> that day. It does not survive now.',
  'The IRCICA edition of sijill 48 prints the entry (register p. 88, <i>ḥujja</i> 1) on its p. 54, dated 23 Dhū al-Qaʿda 972. Its summary says the overseer produced the endowment deed dated 678 AH. Ḥammūdeh (2014), n. 17, gives “the end of Dhu al-Qiʿda,” and he may have read the folio itself, so we print both days.'),
 'C39': FIX('“<b>Two shaykhs</b> of the Ramallah highlands were <b>beheaded</b> for it,” and 1834 “destroyed” the rule of the district shaykhs.',
  '<b>Three shaykhs were put to death</b>: ʿAlī Rabbāḥ and ʿAbd al-Jābir of the Barghūthīs of Banī Zayd, and Ismāʿīl of the Simḥān, who died at Damascus. 1834 <b>broke</b> the system. It did not end it at once.',
  'The local chronicle printed by Macalister and Masterman (<i>PEF Quarterly Statement</i>, 1905, pp. 353–355, and 1906) names all three, says “killed” and “put to death,” and shows the Simḥān still acting as chiefs in the 1840s and 1850s. It does not say how the three men died.'),
 'C45': FIX('One battle, “at the end of September, or on Saturday 1 October,” in which “about eighty Palestinians were killed.”',
  '<b>Two fights, a week apart: 25 September and Saturday 1 October 1938.</b> The count of the dead depends on the witness: “more than twenty” (Fāʾiq Warrād, who saw it as a boy); at least thirty (the ALECSO volume); forty (a press cable of 3 October); “some 50 casualties” (the British report, for 1 October); seventy-five (Ḥammūda’s sources, for the fight at Wādī Shaybān); about eighty (the Quaker teacher).',
  'Totah’s diary dates the battle with six aircraft to 25 September. The British government’s report to the League of Nations for 1938 puts the fight in Ramallah on 1 October, which was a Saturday, as the Quaker letters say. We name each witness and do not choose one number.'),
 'C58': FIX('Kaddoura was “mayor of Ramallah from 1943 to 1952.”',
  '<b>Mayor from 1943 to 1947.</b>',
  'Naseeb Shaheen, <i>A Pictorial History of Ramallah, Part II</i> (2005), p. 85: “Yousef Cadoura, a pharmacist, who became mayor of Ramallah from 1943-1947.” The municipality’s own list of its heads agrees: Yūsuf Qaddūra 1943–1947, then Khalīl Ṣalāḥ 1947–1951. We have found no source for 1952. If he held office until 1947, the Yūsuf Qaddūra who came second in the poll of April 1946 was the sitting mayor.'),
}

# v70 additions from the deep research of 10 November (A1 to A40). Each paragraph is appended to the
# body of the entry named by its title; the note is made when the entry is built, so numbering stays in order.
def _P(text, note=None):
    return '<p>' + (text.replace('{n}', c(note)) if note else text) + '</p>'

ADD70 = {
 'The highlands fill up': [lambda: _P(
  "<b>Khirbet Raddana, a closer look.</b> The village on the edge of our town was lived in only in these two centuries. It had clusters of pillared houses, cisterns and terraces, and a jar handle from it carries one of the early alphabetic inscriptions of the hill country. It was dug in a hurry from 1969 to 1974, in its excavator’s words “before the encroachments of modern civilization destroyed or covered the ancient remains.” Today it is almost wholly built over{n}.",
  "Joseph Callaway, the excavator, in his 1983 account of the dig, for the quotation; he dated the village to about 1200–1050 BC. The summary of the finds follows Klaus Koenen, “Khirbet Raddana,” <i>Das wissenschaftliche Bibellexikon</i> (2014). Both were read online and want a check against the printed reports.")],
 '“A city called Ephraim”': [lambda: _P(
  "One caution about the old witnesses. Eusebius, about AD 300, lists a village Aphra “five miles to the east” of Bethel, which fits eṭ-Ṭaybeh. He is also reported to place an Ephraim twenty Roman miles north of Jerusalem, which is too far for it. The Madaba map takes its caption from Eusebius, so the map and the book are one tradition, not two witnesses{n}.",
  "Eusebius, <i>Onomasticon</i>, in C. Umhau Wolf’s translation, for Aphra; the twenty miles as W. Ewing reports it in the <i>International Standard Bible Encyclopaedia</i> (1915). Read online.")],
 'The dam breaks': [lambda: _P(
  "The last great repair can be followed month by month. Abraha learned of the breach in July 547. Plague stopped the work. It began again in January 548, and his two inscriptions are dated February and March 548{n}.",
  "George Hatke, “Abraha,” in the online <i>Thematic Dictionary of Ancient Arabia</i>, read in extract.")],
 'The silence starts later than the chart': [lambda: _P(
  "What followed al-Mundhir’s arrest is told by Theodor Nöldeke from the Greek and Syriac writers. His sons rose in revolt. Al-Nuʿmān was taken in his turn, and the Arabs of the frontier split into fifteen groups. Greg Fisher adds that Arab forces “remained in imperial service” after 582. Any later return of the family to power is inference, and we do not claim one{n}.",
  "Th. Nöldeke, <i>Die Ghassânischen Fürsten aus dem Hause Gafna’s</i> (Berlin, 1887), pp. 29–33, read in the project library. Greg Fisher, “Arabia and the Late Antique East,” p. 12, read in extract.")],
 'al-Yaʿqūbī finds Ghassān in Transjordan': [lambda: _P(
  "We should say plainly what this is and what it is not. After the conquest Ghassān lives on in the Arab writers as the name of a tribe: here about 890, and “in the Balqāʾ,” “at the Yarmūk” and “at Ḥimṣ” in a notice of the Mamluk period. None of these writers states their faith, and no medieval source we have found ties Karak itself to Ghassān. Mark Whittow notes that they “supported the Umayyads during the first century of Islam.” Our family’s memory of a Christian Ghassān at Karak stays what it is: a tradition, honestly held{n}.",
  "ʿUmar Riḍā Kaḥḥāla, <span class='ar'>معجم قبائل العرب</span>, vol. 3, s.v. Ghassān, citing al-Ḥamdānī through al-Qalqashandī. Mark Whittow (2013), p. 2. Both read online.")],
 'The name appears in 1186': [lambda: _P(
  "The register that runs to 1531–32 gives Ramallah a revenue of 500 akçe; Ḥammūdeh reports no count of households from it. So the hill was settled again between 1528 and 1532. In all these registers no lord of Ramallah is ever named. Its revenue stayed with the two sanctuaries and was managed by their officers: Ḥammūdeh names Muḥammad ibn Mūsā al-Kurdī, “the endowment collector for the two sites,” and Muḥammad Jalabī, “overseer of the two holy sanctuaries.” Al-Bīra next door was different. In the court case of 1565 it is the <i>tīmār</i>, the military fief, of one Muṣṭafā Bey. <b>Ramallah had no lord, and its neighbour did</b>{n}.",
  "Ḥammūdeh (2014), pp. 41–43, for register T.D. 131 and the two officers; the IRCICA edition of sijill 48, printed p. 54, for al-Bīra as Muṣṭafā Bey’s <i>tīmār</i>.")],
 'Karak was a Christian town': [lambda: _P(
  "<b>One endowment at both ends of the road.</b> The Ottoman registers of 1548 and 1596 list, in the district of Karak, a share for the sanctuary of Abraham at Hebron: 2,000 akçe, then 2,500. This is the endowment that owned the hill of Ramallah. It is not evidence that anyone moved. By inference it shows only that, in the decades when our tradition has the family on the road, one endowment’s collectors worked at both ends of it{n}.",
  "The entry “Hisse-i Vakf-ı Hz. Halîl” in the Karak registers, as published in <i>GTTAD</i> (2023), p. 187, read online. Jordanian scholarship reads the register of 1596 as this book does, 78 Muslim and 103 Christian households at Karak: Al Btoush (2024), in a University of Jordan journal, citing Hind Abū al-Shaʿr.")],
 'When the Ḥaddādīn name enters the record': [lambda: _P(
  "<b>They went back and forth.</b> Frederick Peake, writing of the Christian clans of Transjordan, says: “Most of the Christian clans hail from Palestine … In el-Karak, many of them have come from Hebron, Bethlehem and Jerusalem.” Heikki Palva, who quotes him, adds that the clans’ claims of Ghassanid origin are as impossible to prove as the Muslim clans’ claims of Bedouin descent. Set beside Burckhardt, this does not refute our tradition. It shows that Christian families moved in both directions between Karak and the Jerusalem hills, over centuries, and ours may have done both{n}.",
  "Heikki Palva, in the <i>Journal of Arabic and Islamic Studies</i> 8 (2008), pp. 54–55, quoting Peake. Read online; Peake’s own page is still to be checked.")],
 'The registers begin': [lambda: _P(
  "Two small facts from the same papers. A second group called Kasābra is recorded at Dayr Abān, also “from Khirbat Kusbar.” So the name marks people who came from Kusbār, not one family. And a man of al-Bīra called Ḥijāz ibn Ḥusayn appears in a court record of 947 AH, 1540–41. It is a father’s name and no more. It neither supports nor contradicts al-Bīra’s own tradition of its Ḥusayn founders{n}.",
  "Ḥammūdeh (2014), pp. 41–42 and his discussion of the Kasābra.")],
 'The registers do give names': [lambda: _P(
  "<b>Two court records put the names on the hill.</b> Ḥammūdeh found them in the Jerusalem registers. On 27 November 1604 the court recorded a reconciliation between ʿUbayd ibn Ghānim “of the clan of the sons of Hadid” and Muṣliḥ ibn Ibrāhīm “of the sons of al-Naqqāsh,” both Christians of Ramallah. On 3 July 1605 it names “Muṣliḥ son of the Christian Shuqayr, from the families of Ramallah.” These are the only firm mentions of the town we have between 1596 and 1800. They put a Ḥadīd clan and a Shuqayr here within forty-three years of the register of 1562, where Shuqayr is missing. They bear on whether the old name was Ḥadīd or Ḥaddād. They do not settle it{n}.",
  "Sijill 84, p. 541, and sijill 85, p. 188, as Ḥammūdeh (2014) reports them at p. 49 and in his notes 74 and 76. The registers themselves are unpublished.")],
 'The Christian settlement of 1561–62': [lambda: _P(
  "The case of 1565 also drew the town’s edges. The judge went out to the ground in person. Ramallah’s limits were set at Dayr Fazṭām to the south, the “Roman” chain wall along the road to the east, and Burj Salmiya to the north. Ḥammūdeh’s English prints the southern limit as “Dayr Qurtam,” and the reading of that word is not settled. The same volume names a Ramallah man, Ḥammād ibn Aḥmad, in 1566{n}.",
  "The IRCICA edition of sijill 48, printed p. 54, read from the page images on 9 November 2026.")],
 'Feuds, a pasha and a faction': [lambda: _P(
  "<b>The ʿAzzouz incident, as the town tells it.</b> A marriage was refused in a Hānī family, and the killing followed. The whole town left. The Shakara went to Beitunia, the Sharaka to Beit Ijza, the Jaghab to Silwad, the Yousef to Abu Qash, the Hasasneh to ʿAin Yabroud, the ʿAwwaad to Mazraʿa al-Gharbiyya, the Ibrahim to Mazraʿa al-Sharqiyya and the Jirius to al-Fandaqumiyya. They were home within the year, and the ʿAzzouz who survived joined the Jaghab. This is oral tradition, written down by Kaddoura in 1954. No outside source confirms it{n}.",
  "Shāhīn (1982), pp. 33–34, after Kaddoura (1954), p. 59, which we have not yet read; Shaheen (2005), p. 18, for the ʿAzzouz joining the Jaghab."),
  lambda: _P(
  "<b>The faction wars, from a local chronicle.</b> Macalister and Masterman printed it in 1905–06 “from native sources.” After the Egyptians left in 1840, Ramallah’s people sought the protection of Muṣṭafā Abū Ghōsh of the Yaman, who set guardians over them. The Qaysī leaders of the town, Yūsif Ḥarb and ʿAīsa Abū Jughub, appealed to the Simḥān. A Qaysī force “proceeded against Ram Allah, which they reached a little before sunset.” Abū Ghōsh attacked at midnight with about three thousand men. His brother Ṭāhā was killed, and more than a hundred died. Later he “set out for Ram Allah, which he attacked. All the inhabitants fled except one dumb old man”; “the village, however, was not looted.” So a Ḥarb and a Jaghab led the town in the 1840s, and they are named in an account written outside it{n}.",
  "R. A. S. Macalister and E. W. G. Masterman, <i>PEF Quarterly Statement</i> 38 (1906), pp. 41–44. Read online.")],
 'The peasants’ revolt of 1834': [lambda: _P(
  "Ramallah had no shaykhly house of its own. The chronicle and the British survey of the 1870s both place it in Jabal al-Quds, a district of four shaykhs, two of them next door at al-Bīra and Beitunia. Our town sat between two small seats{n}.",
  "Macalister and Masterman (1905), pp. 353–354: “Among the other villages of this district are Ram Allah, Kefr ʿAkab, Jebaʿ.” <i>The Survey of Western Palestine</i>, Memoirs III, p. 13, lists the town under “Jebel el Kuds.”")],
 'The five sons and the eight clans': [lambda: _P(
  "Each of the eight clans, Naseeb Shaheen writes, “had its own neighborhood where members of that clan built their homes around a central courtyard,” the <i>ḥōsh</i>. The town’s guest house, the <i>madāfa</i>, stood beside the shrine of al-Khalīl and was pulled down about 1960. Karm ʿAlī comes back into the story too. Salem Butros Jaber of the Yousef clan bought land there, on the northern edge, “and in about 1850 moved there with his many relatives.” It became the first quarter outside the old village, the Kedaireh{n}.",
  "N. Shaheen, <i>A Pictorial History of Ramallah, Part II</i> (2005), pp. 63–64 and 234, read in the project library. On the guest house in general, Suad Amiry and Vera Tamari, <i>The Palestinian Village Home</i>, p. 15: “The guest-house (madafah), usually situated in the sahah, was also the centre of male gatherings and entertainment.”")],
 'The parish proves itself in writing': [lambda: _P(
  "<b>Why the next two centuries are nearly blank.</b> Naseeb Shaheen puts it down to the lack of registers: “the Orthodox Church kept no records of the births, baptisms, marriages, and deaths of Ramallah people.” Careful records begin in 1857, and they are the Roman Catholic parish’s, kept for its own flock. So the town’s own registers cannot name the first families before then, and the names must come from the Jerusalem court and from the Patriarchate. The Patriarchate’s archive lists a “Collective petition of the inhabitants of Ramallah” of 1889, which we have not yet read{n}.",
  "Shaheen (2005), p. 31. Ḥammūdeh (2014), n. 2, reports him as dating Greek Orthodox registration from 1857; Shaheen’s own page says the Roman Catholic Church. The petition is in the Open Jerusalem inventory of the Patriarchate’s archive, reference JM-AEPI/VI/Γ/15/1889/9; title only.")],
 'The town gains its churches and schools': [lambda: _P(
  "The Friends’ first school was called the Hope School, and it opened in August 1869. Hishmeh, who had been the Joneses’ guide, ran the day schools for seventeen years, and by 1893 there were eight of them. In 1888 the English and American Friends divided their work, and the Americans took Ramallah. After Katie Gabriel the girls’ school was led by Alice Jones from 1906, and then by Mildred White, Victoria Hannush, Sylvia Clark, Anna Langston, Annice Carter and Margaret Paull. It had 150 girls in 1930. In 1966 the two schools had 233 girls and 320 boys{n}.",
  "Enaya Othman, <i>Jerusalem Quarterly</i> 50, pp. 50 and 62 n. 11; the Philadelphia Yearly Meeting’s history page for 1888; the Ramallah Friends School’s own history page for the heads and the numbers. The last two were read online."),
  lambda: _P(
  "The British surveyors who mapped the country about 1875 described the town in a few lines: “A large Christian village, of well-built stone houses … In the village is a Greek church, and on the east a Latin convent and a Protestant schoolhouse, all modern buildings.” They gave al-Bīra about 800 people{n}.",
  "<i>The Survey of Western Palestine</i>, Memoirs III (London, 1883), pp. 9 and 13. Read online.")],
 'The terraces and their': [lambda: _P(
  "One word needs care. <i>Qaṣr</i> means two things in this book. In the fields it is the watchtower, built, the survey says, “to watch over the cultivated land” and as “an alternate living space” at harvest: of the 167 towers, 125 have two storeys, 41 have one and a single tower has three. In the story of 1834 it is the fortified house of a district shaykh. The two share a name and little else{n}.",
  "Al-Houdalieh and Ghadban (2013), pp. 510 and 521.")],
 'The twin town and the Rafeedie family': [lambda: _P(
  "One dated trace of the family at al-Bīra survives. Shāhīn lists, from the Ramallah population register, Ilyās Yaʿqūb Nazzāl and his wife Salmā, daughter of Sālim al-Rafīdī of al-Bīra (<span class='ar' dir='rtl'>الياس يعقوب نزال وزوجته سلمى بنت سالم الرفيدي من البيرة</span>), and his English edition dates that household to “about 1890 or 1895.” So a Sālim al-Rafīdī was at al-Bīra by about 1890. Where his family came from we still do not know{n}.",
  "Shāhīn (1982), Arabic and English editions. The Arabic was read by machine from the scan and wants an eye.")],
 'Elihu Grant writes the town down': [lambda: _P(
  "<b>What the town lived on.</b> Lisa Taraki shows Ramallah merchants selling olive oil to the soap makers of Jaffa, and buying raisins from the villages for a German firm that shipped them through Jaffa; women workers prepared them. The Bellevue <i>locanda</i>, a hotel, opened in 1902. Grant himself wrote that “the finest grapes within reach of Jerusalem are those from Hebron and Râm Allâh.” The dollars came from peddling. Saleh Abdel Jawad, writing of al-Bīra men on the same road, found that “successful peddlers made about three to five dollars a day in 1910.” He names Ramallah peddlers who rose to be wholesalers: Abdullah and Issa al-Batih, Hanna Hishmeh and Aziz Shahin. And when the men left, “their wives saw to the affairs of the family and the lands”{n}.",
  "Lisa Taraki, <i>Jerusalem Quarterly</i> 83, pp. 87–88 and 96–99. Elihu Grant, <i>The Peasantry of Palestine</i> (1907), ch. I. Saleh Abdel Jawad, <i>Jerusalem Quarterly</i> 36, pp. 20–24.")],
 'The Patriarchate counts its flock': [lambda: _P(
  "<b>Ramallah, 30 August 1932.</b> The struggle came to our own town. More than sixty Arab Orthodox priests from Palestine and Transjordan met here. They passed reforms for the schools, the churches, the endowments and the church courts, and elected a committee with Father Niqūlā Khoury as its secretary. Khoury tells it himself in his memoirs. His editors note that his account is disputed, and Papastathis confirms that the meeting took place. In the 1940s Ramallah had its own club in the Union of Orthodox Clubs. Grant, thirty years before the meeting, had watched a village wedding read “partly in Arabic and partly in Greek” by a head priest “who was a Greek by blood”{n}.",
  "Niqūlā Khoury, <i>Memoirs</i>, printed pp. 101–102 and the editors’ n. 66; Papastathis, p. 39; Neveu, p. 57; all read in the project library on 9 November 2026. Grant (1907).")],
 'The counting years': [lambda: _P(
  "<b>The missing men were Christian men.</b> The census of 1931 counts 1,662 Christian men against 2,104 Christian women in the town, a gap of 442. The town’s Muslims had more men than women, 280 against 240. In 1922 the Christian gap had been 204, so it doubled in nine years. Over the same years the town’s Muslims grew from 125 to 520. The men who sailed were ours, and the town was already changing behind them{n}.",
  "E. Mills, <i>Census of Palestine 1931</i>, vol. II, Tables V and VI, pp. 16–17; Barron (1923) for 1922. The 1931 tables were read through a machine-read scan and want an eye."),
  lambda: _P(
  "After 1948 Jordan took over the Ramallah transmitter. When Jordan opened a national station at Amman in 1956, it shared a frequency with what one study calls “its then primary radio station, which broadcast its programs from Ramallah”{n}.",
  "Andrea Stanton (2013), chronology, for 1948; Tweissi (2021) for 1956. Both read online. How long Ramallah went on broadcasting after that we have not established.")],
 'The revolt reaches the town': [lambda: _P(
  "<b>1936 in the town.</b> The revolt began with the general strike of 1936. Totah wrote on 11 May: “In Ram-Allah we kept open during the first week of the strike.” On 8 July he protested to the High Commissioner about troops shooting villagers. The national committees of Ramallah and al-Bīra formed a joint committee, with Ḥannā Khalaf for Ramallah, and on 7 May the municipality voted twenty-five Palestine pounds for the poor whom the strike had hurt{n}.",
  "Ricks, ed., <i>Turbulent Times in Palestine</i>, for Totah; Ḥammūda (2019) for the committees and the vote, read in a web copy without its footnotes."),
  lambda: _P(
  "<b>The months around the battle.</b> A rebel communiqué of 7 September 1938 claimed about four hundred men under Muḥammad ʿUmar al-Nūbānī, with units from Ramallah, Baytūniyā and al-Bīra. After the fighting Totah’s diary records long curfews, and an order to the townspeople to pull down the stone walls and trees around their houses. The post office and the telephone came back on 10 and 11 February 1939. On 24 August 1939 the radio station, the police and the army post were attacked again{n}.",
  "Totah’s diary as set out by the Institute for Palestine Studies (2023), cited above."),
  lambda: _P(
  "<b>The names of the dead.</b> No townsman of Ramallah killed in the fighting is named in anything we have read. Ḥammūda names villagers who fell at Wādī Shaybān: Rāḍī Muṣṭafā Shaḥāda, Saʿīd Jumʿa Ṣāfī, Zaʿīd Yāsīn Muḥammad and Nasīm ʿAbdallāh Ẓāhir of Baytīn, and Aḥmad ʿAbd al-Muṭṭalib Aḥmad Jabr of Rāfāt, with eight men of Dayr Dibwān and three of Burqa whose names he does not give. He also records that a man of the al-Kaʿbīnī family of Ramallah died in a disused well the British used to hold prisoners. Of our own clans, Ḥannā ʿĪsā Khalaf of the Shaqara “took an active part in the 1936 Arab uprising,” was jailed at Sarafand, deported to Iraq, and came home about 1939 “in disguise”{n}.",
  "Ḥammūda (2019), web copy; Shaheen (2005), pp. 41–42, for Khalaf."),
  lambda: _P(
  "<b>The army’s word.</b> The intelligence summaries of the West Yorkshire battalion, written at Ramallah that winter, say “the town of Ramallah had refused to pay the rebels a subsidy.” The historian Matthew Hughes files this under “collaboration.” That is the British army’s word, and we print it as theirs. Totah’s diary shows the other side of the same months: the rebels held a court and punished men who had robbed townspeople. The summaries are kept at the regimental museum in York, and they are our best lead for the names{n}.",
  "Matthew Hughes, <i>Journal of Contemporary History</i> (2016), p. 300.")],
 'The town votes by clan': [lambda: _P(
  "<b>The quarrel behind the fifth candidate.</b> Naseeb Shaheen keeps the family memory. “The dispute was over a nomination to the city council, ca. 1943 … the clan nominated Hanna Jaber as the new member. But the Harb family … selected one of their own family, Jaleel Harb.” Two feasts of reconciliation followed about 1949. The result sheet has exactly these two men in the Ḥaddāda district: Jalīl Ḥarb, elected with 215 votes, and Ḥannā Jābir with 154. Shaheen’s “ca. 1943” is memory; the poll was on 15 April 1946{n}.",
  "N. Shaheen, <i>A Pictorial History of Ramallah</i> (1992), p. 220, and <i>Part II</i> (2005), p. 75.")],
 'Where the refugees lived': [lambda: _P(
  "Al-Jalazūn began with “around 4,000–5,000 people.” About 1951–52 some families built in rubble stone and earth, and concrete shelters came in 1953. Early residents also lived in “olive and apricot orchards belonging to the village Jifna”{n}.",
  "“Jalazone,” in the <i>Interactive Encyclopedia of the Palestine Question</i> (Institute for Palestine Studies and the Palestinian Museum), read online."),
  lambda: _P(
  "The refugees changed the town for good. After 1948, Salim Tamari writes, in towns like Ramallah “the majority of local merchants did not originate from the town itself, but were war refugees from the coastal cities.” In the census of 2017 refugees were 41 per cent of the town’s residents, against 67 per cent in the local count of 1953{n}.",
  "Salim Tamari, <i>Mountain against the Sea</i> (2009), p. 48; PCBS 2017, Table 4, p. 59.")],
 'The Federation': [lambda: _P(
  "The Federation says of itself that it “represents more than 50,000 people.” That is its own figure, not a count.")],
 'The city, counted to the present': [lambda: _P(
  "<b>The twin towns in 1967.</b> The same count has a row for Ramallah and al-Bīra together: 21,808 people, 34.2 per cent Christian and 65.6 per cent Muslim, with 45 in every hundred from land that had become Israel. So the two towns together were already two-thirds Muslim while Ramallah alone was still mostly Christian. This too is the occupying power’s count{n}.",
  "The census of 1967, vol. 1, Table 1, in the copy published by the Levy Economics Institute."),
  lambda: _P(
  "<b>The mayors under occupation.</b> A United Nations committee recorded in 1970 that Mayor Nadīm Zarū “was arrested on 1 October 1969, detained in prison for six days, and then expelled from the area.” Karīm Khalaf won the elections of 1972 and 1976. He lost a leg to a car bomb on 2 June 1980, and the occupation authorities removed him from office in 1982. From 1982 to 1987 the Israeli Civil Administration ran the town. The municipality’s own list of its heads dates his term 1976–1985, so its two pages do not agree{n}.",
  "UN Special Committee report (1970), para. 84; Ramallah Municipality, <span class='ar'>تاريخ البلدية</span>: <span class='ar' dir='rtl'>أقالته السلطات عام 1982م من رئاسة البلدية</span>; the Khalaf entry in the <i>Interactive Encyclopedia of the Palestine Question</i>."),
  lambda: _P(
  "<b>The lions of al-Manāra.</b> The municipality commissioned a monument from a Ramallah artist in 1946. It was finished in 1951: five lion heads on a pillar. “The five lions represented the five Ramallah families who viewed themselves as the city’s ‘original’ inhabitants.” A decree of 1982 ordered the square demolished. The old monument was later set up again, with a clock, in Mīdān al-Mughtaribīn, the Emigrants’ Square, and a new one with four lions was finished in July 2000. The square’s own beginning is dated two ways: 1923 by the municipality, and 1935, when the electricity pole went up, by Shibli. When the square was renamed for Yasser Arafat, residents objected: “It is no longer the original landmark of Ramallah city.” We do not yet know the name of the sculptor of 1946{n}.",
  "Adania Shibli, <i>Jerusalem Quarterly</i> 26, for the monument; Brocket, <i>Geopolitics</i> (2021), p. 557, for the renaming."),
  lambda: _P(
  "And the founder has a monument of his own. On 3 April 2017 the municipality unveiled a memorial to Rāshid al-Ḥaddādīn at the municipality building. It is the work of the artists Sliman Mansour and Nabil Anani, and it was given by Ḥannā Ghānim and his sister Najma Ghānim{n}.",
  "Wattan news agency, 3 April 2017: <span class='ar' dir='rtl'>ازاحت دار بلدية رام الله، مساء اليوم الاثنين، الستار عن النصب التذكاري لمؤسس مدينة رام الله راشد الحدادين</span>. The municipality’s own page lists only <span class='ar' dir='rtl'>افتتاح نصب راشد الحدادين</span> among the works of Mayor Mūsā Ḥadīd’s terms.")],
 'The people our town produced': [lambda: _P(
  "The Palestinian Museum’s archive confirms the Nahda from outside Shāhīn: it was “founded in 1925 to serve women and children in the Ramallah district,” with a kindergarten, a clinic and literacy classes. Women here also earned wages by the needle. At the Hishmeh shawl factory “specially trained women” embroidered flowers on shawls. The dress itself was the town’s signature: white handwoven linen worked in wine-red cross-stitch, a tall palm on the back, and a headdress “surrounded by a stuffed halo of material with coins attached to it.” The star of Bethlehem’s embroidery, Widad Kawar wrote, “becomes a moon in Ramallah.” And in April 1933 Matiel Mogannam spoke at the Mosque of ʿUmar in Jerusalem, a Christian woman speaking in a mosque{n}.",
  "Palestinian Museum Digital Archive, the Nahda collection. Widad Kawar, in the <i>Journal of Palestine Studies</i> (1980), pp. 123–127. Saca, <i>Embroidering Identities</i>, pp. 16–26. Ellen Fleischmann, <i>Journal of Palestine Studies</i> (2000), pp. 19 and 24.")],
}

# v72 round 2 additions (12 Nov 2026). Same mechanism as ADD70: appended to the entry whose title starts with the key.
ADD72 = {
 'The present Greek Orthodox church is built': [lambda: _P(
  "Cadora names the builders. At the inauguration of 1852, under the supervision of Sheikh Muḥammad al-ʿĀmir of al-Bīra, the prefect of the district, who was paid a quarter of a mejīdī a day, “the builders of the church were from the Al-Saah family”{n}.",
  "Cadora, <i>Remembering Ramallah</i>, p. 46.")],
 'How the town lived': [lambda: _P(
  "<b>Each clan had its craft.</b> Cadora gives the town’s trades by family. Weaving was the speciality of the Sharaqa, who wove woollen and striped cloaks. Shoemaking belonged to the Hishmeh and the ʿAudeh. “Construction was the domain of the Saah clan.” The women made the clay jars, stoves and hearths, the straw trays, and the cross-stitch embroidery{n}.",
  "Cadora, <i>Remembering Ramallah</i>, p. 101.")],
 'The first four sail for America': [lambda: _P(
  "Cadora, writing in 1954, tells the first departures more fully than Shāhīn. Ḥannā Ibrāhīm al-Saah sold Holy Land goods, and in 1858 he left with the Greek pilgrims for Istanbul, where he opened a shop. He went back and forth for years, grew rich, and died there without heirs, leaving his fortune to the Patriarchate of the Phanar. Cadora’s Saah chart marks a Ḥannā who “Died in Constantinople.” The idea of America, Cadora writes, came in 1889, when the Friends brought masons from Bethlehem to build the girls’ school, and the Ramallah labourers heard them talk of the money to be made there. Joseph ʿAudeh then left for America in 1895. Shāhīn has the first to go west leaving in 1895 for England; we print both{n}.",
  "Cadora, <i>Remembering Ramallah</i>, p. 104, and the clan chart, p. 146. Shāhīn (1982), English text, p. 23, calls Ḥannā “the first person who is known to have left Ramallah for another country” and adds that others may have gone earlier, “but if so, nothing is known about them”; Shaheen (1992 and 2005) repeats it in his timeline. These are one town tradition written down three times, and no Ottoman or church record of the journey has been found.")],
 'The counting years': [lambda: _P(
  "The light has a family history too. In 1885 Ibrāhīm al-Saah brought petrol lanterns from Jerusalem to light his house, and the village came to look; Cadora had the story from Sheikh Ḥannā al-Zaʿrūr. Cadora adds that in 1935 ʿAzīz Cadora, the grandson of Khalīl Ibrāhīm al-Saah, was the first to install the electric grid and carry it to the houses and streets. ʿAzīz had come home from studying electrical engineering in America. The same book says that in 1935 the Jerusalem power company laid the cables to Ramallah and al-Bīra, so the supply was the company’s, and ʿAzīz is remembered as the man who wired the town to it{n}.",
  "Cadora, <i>Remembering Ramallah</i>, pp. 12, 56 and 89 (PDF pages). Only Cadora names ʿAzīz, and Cadora was his family; Shaheen (2005), p. 225, dates the first electricity to 1934.")],
 'Our first history, written in New York': [lambda: _P(
  "The name has its own story, told by the family in the 2023 edition. Khalīl Saah’s wife was warned as a girl that the district’s Ottoman policeman, a man named Qaddūra, would be called to punish her. She became “the Qaddoura mother,” her children “the children of Qaddoura,” and the family was known as the Qaddūras instead of Saah. At Ellis Island the name was written Cadora{n}.",
  "Cadora, <i>Remembering Ramallah</i>, English edition (2023), front matter, p. 10, family tradition.")],
 'The people our town produced': [lambda: _P(
  "In 1940 Yūsuf Jiryis al-Saah opened a large furniture factory in Washington, D.C., making tables, chairs and cupboards{n}.",
  "Cadora, <i>Remembering Ramallah</i>, pp. 108–109.")],
 'New families arrive': [lambda: _P(
  "<b>The Saah builders and Acre.</b> Cadora tells this story as the families told it to him. After Ẓāhir al-ʿUmar was killed in 1775, Aḥmad al-Jazzār made Acre his seat and set about rebuilding its walls. His men roamed the villages of Palestine and south Lebanon and forced men into labour, and Ramallah was not spared. “The Al-Saah family were builders and among the first forced into labor.” When the work was done, the Saah builders escaped. Al-Jazzār knew where they came from, so they went to Safad instead of home and worked there as builders. In Safad their daughter Hishmeh married Khaled, a roaming shoemaker, and her grandchildren are the Hishmehs of Ramallah. The family stayed away for fifteen years, until Yaʿqūb of the Ḥaddādīn went to Safad and brought them home. They came back with a new name, al-Ṣafadī, the people from Safad. The outside record fits the story. Al-Jazzār governed from Acre from 1776 until 1804. James Silk Buckingham, who saw Acre in 1816, wrote that its outer walls were “the work of Djezzar Pasha,” who improved the fortifications after the French withdrew in 1799. The family tree puts Elias Salāmeh Saah’s birth at about 1769, and his daughter Sabḥa (born about 1799) married Ayoub Ibrahim Safadi. That fits Cadora’s own clan chart, which is headed “The Saah or Al Safadi Clan”{n}.",
  "Cadora, <i>Remembering Ramallah</i> (1954; English 2023), pp. 35–36 and the clan chart, p. 146, family tradition. J. S. Buckingham, <i>Travels in Palestine</i> (1821), p. 76. The Saah family tree."),
  lambda: _P(
  "Two more family stories belong with this one. The same labour gangs explain a priestly line. Ḥannā Saʿad of the ʿAwwād clan was an only son, so his cousins took him to the Greek Orthodox monastery in Jerusalem rather than let him be taken to Acre. He became a priest, and he is the ancestor of the al-Qassīs family, who are kin to the ʿAwwād. And the trade went on. Ayoub Ḥannā al-Ṣafadī was a mason who built houses in the villages and a revered sheikh at home. One house-owner paid him with four silk robes, the only ones in Ramallah, and for years couples borrowed them to be married in{n}.",
  "Cadora, <i>Remembering Ramallah</i>, pp. 35 and 40, family tradition.")],
 'Feuds, a pasha and a faction': [lambda: _P(
  "<b>The feud of 1820 in Cadora’s telling.</b> Cadora, who was Shāhīn’s source, writes that “in 1820, a fight broke out among members of Al-Shaqara clan.” A marriage into the Abū Hānī family was refused, and the would-be groom’s brother was killed. The killer fled to the Barāghtha of Banī Zayd, and Muḥammad Abū Salāmeh of the Ghazāwneh of al-Bīra turned the revenge onto the Qaysī side. The families scattered to the villages around, among them Silwād and Yabrūd, and they “returned to Ramallah through a Sulha after an absence of one year.” His spelling is Shaqara, as in Shāhīn (1982){n}.",
  "Cadora, <i>Remembering Ramallah</i>, pp. 40–41 (scan page markers). The scan is machine-read and garbles some village names and the number of the dead, so those are not printed here.")],
 'Ramallah becomes a city, clan by clan': [lambda: _P(
  "Cadora, who later sat in the mayor’s chair himself, gives the day: the municipality was “established on April 1, 1908,” and Elias ʿAudeh was its first mayor, from 1908 to 1921{n}.",
  "Cadora, <i>Remembering Ramallah</i>, p. 65 (scan page marker).")],
 'Musil asked them himself': [lambda: _P(
  "<b>What Peake’s Arabic edition adds.</b> Peake’s Arabic volume of 1935 gives two Karak entries that touch this table. Of al-Ḥalasa he writes that “they are said to be the sons of an Egyptian who came to Karak and married a girl of the Ḥaddādīn clan; their rite is Greek Orthodox; they live in Karak and the village of Ḥammūd, and they have kin in Nazareth called al-Ḥanādisa.” So one Karak Christian clan kept kin west of the Jordan. Of al-Ṭanāshāt he says the opposite of Musil. Musil counts them among the old lineages “who built the town”; Peake lists them under a Muslim clan, “descendants of one of the old Ottoman officials.” We print both views by name. Kaddoura’s Sheikh Ṭanāsh, who flees with Rāshid, belongs to this same name{n}.",
  "F. G. Peake, <span class='ar'>تاريخ شرقي الأردن وقبائلها</span> (Jerusalem, 1935), p. 351, page image read: <span class='ar' dir='rtl'>يقال انهم ابناء رجل مصري قدم الى الكرك وتزوج فتاة من عشيرة الحدادين، ومذهبهم روم ارثودكس. يقطنون في الكرك وقرية حمود ولهم اقارب في الناصرة يدعون بالحنادسه</span>; for al-Ṭanāshāt, <span class='ar' dir='rtl'>من اعقاب أحد الموظفين العثمانيين القدماء</span>. Page 351 is the al-Ḥalasa page; Peake’s Ḥaddādīn entry, which Kaḥḥāla cites, is p. 348.")],
 'The revolt reaches the town': [lambda: _P(
  "<b>The officer who was killed.</b> The British police officer killed on 1 October has a name. The Palestine Police report for 1938 lists, among the British police killed that year, “Assistant Inspector W. E. Birch. Killed by unknown persons during an engagement at Ramallah on 1st October.” The Quaker teacher knew him. On 8 October she wrote: “Of the British, only one, our friend, Sargent Birch, was killed. He had taken refuge in the house of our laundress, where the Arabs shot him down and burned the house. The poor widow who owned it had worked years and just finished building her home.” So one house that burned that day can be named by its owner’s work, though not by her name, and it burned in the fight, not by a British demolition order. The next day “burned houses were still smoldering.” She adds that the roads “had been blocked off with rocks so that British armored cars couldn’t get by,” and the telephone wires were cut. Cadora, writing in Ramallah, tells the same day from the town’s side: the rebels under ʿUmar al-Nūbānī took the police station, and “a British police inspector and an Arab policeman were killed.” Troops came from Jerusalem and planes from Sarafand, thirty Arabs died, and the rebels brought down a British plane near Bayt ʿŪr{n}.",
  "Palestine Police, <i>Annual Administrative Report 1938</i>, s. 17(a), British entry 7, page image read. McDowell, <i>Notes from Ramallah, 1939</i>, printed pp. 14–17. " + D('1939_McDowell_Notes_from_Ramallah.pdf') + ". Cadora, <i>Remembering Ramallah</i>, p. 57 (scan page marker)."),
  lambda: _P(
  "<b>The fighters’ side of the same weeks.</b> The Palestinian historian Bilāl Fāris names the units: the Ramallah unit under Ḥannā ʿĪsā Khalaf, and the al-Bīra unit under ʿAbd al-Dāʾim ʿAbd al-Ṣamad. A Ḥannā Khalaf also sat on the national committee of 1936 and the election committee of 1946; we do not assume they are one man without a source that says so. Abū ʿUmar al-Nūbānī “took the British police station in the town,” and Darwaza’s memoirs record that “the Ramallah police office was closed and its equipment taken to Jerusalem.” <i>Al-Akhbār</i> of 8 September reports two fighters martyred on 5 September, where Totah speaks only of wounded{n}.",
  "Bilāl Fāris, <span class='ar'>تحرير المدن 1938</span>, Institute for Palestine Studies (2023), pt 1, read in extract, with his sources: Ḥammūda for al-Nūbānī; Muḥammad ʿIzzat Darwaza, memoirs, p. 502; <i>al-Difāʿ</i>, 20 September 1938, for the move of the post office and court; <i>al-Akhbār</i>, 8 September 1938. His notes put Ricks’s edition of Totah at p. 232 for the police post and the entry of 500 to 800 men on 9 September, and p. 234 for the evening of 7 September. The Arabic wants an eye check.")],
 'The catastrophe of 1948': [lambda: _P(
  "<b>Before Lydda.</b> Jordan took charge of the Ramallah region weeks before the expulsions. Bahjat Tabbāra was appointed for the Ramallah region on 18 May 1948, with ʿAzmī al-Nashāshībī as his assistant, and a second company of the Arab Legion was sent to the town on 27 May. Cadora, who was acting mayor from 1 April 1948 while Khalīl Ṣalāḥ was away, gives the same date for Tabbāra. He records that Ramallah was bombed from the air on 26, 27 and 29 May, and a refugee from Ramle was killed. On 5 June the mayors of Lydda, Ramle, Ramallah and al-Bīra went together to King Abdullah about the refugees. In December 1948 the king came to a conference in Ramallah, and the notables, the mukhtārs and the National Committee of the Ramallah area signed a petition against Jordanian rule{n}.",
  "Bilāl Shalash, <i>Almuntaqa</i> 8 (2021), from the writings of Qāsim al-Rīmāwī, read in extract. Cadora, <i>Remembering Ramallah</i>, pp. 58–60, 64 and 72 (scan page markers)."),
  lambda: _P(
  "<b>The march.</b> About seventy thousand people of Lydda, Ramle and the villages near them were given half an hour to leave on 13 July. They were sent on “a rugged, treacherous path to reach Ramallah.” More than four hundred people were killed in Lydda, eighty to 176 of them at the Dahmash mosque, and close to a thousand died in the city and on the march together. Hundreds died of thirst and exhaustion on the road, and newborns did not survive. The painter Ismāʿīl Shammūṭ lost his brother to thirst on the march. Reja-e Busailah, George Ḥabash and Spiro Munayyer, who walked it or saw it, have left their own accounts{n}.",
  "“Lydda, 9–13 July 1948,” <i>Palestinian Journeys</i> (Institute for Palestine Studies and the Palestinian Museum), read in extract; it names the witnesses: Reja-e Busailah, <i>In the Land of My Birth</i> (2017); George Ḥabash in <i>Majallat al-Dirāsāt al-Filasṭīniyya</i> (1998); Spiro Munayyer, “The Fall of Lydda” (1998), with notes by Walid Khalidi."),
  lambda: _P(
  "<b>The town receives them.</b> Christina Jones of the Friends schools wrote on 13 July of “thousands of people on foot struggling up the twenty-five-mile road.” About two hundred were sheltered in the Girls School, and the Boys School became an emergency hospital, with a maternity ward in the principal’s house and “as many as seven refugee babies born in a single day.” Cadora writes of “25,000 refugees who came overnight,” fed by the Jordanian government until the Red Cross took over. By March 1949 the refugees’ own body, the Arab Refugee Congress of Ramallah, counted <b>72,660</b> refugees, almost certainly for the Ramallah area rather than the town. That is a Palestinian count, made by the refugees themselves{n}.",
  "Christina Jones’s diary, Philadelphia Yearly Meeting, “1948 July,” read in extract; Ramallah Friends School, history page, for the maternity ward. Cadora, <i>Remembering Ramallah</i>, pp. 58–60. UN Conciliation Commission for Palestine, Technical Committee, working paper CDM.TECH/W.2 (14 June 1949), section “Ramallah, March 1949”; the scan is poor and the total wants an eye check."),
  lambda: _P(
  "<b>The count of 1953, in two hands.</b> Shāhīn gives 13,500 people: four and a half thousand natives and nine thousand refugees. Shāhīn took his figures from Cadora, and the two splits are both inside Cadora’s own book. His chapter on the town says “The original inhabitants numbered 5,000. The additional 8,500 were refugees.” His appendix of 1953 statistics, and his chapter on the churches, give 4,500 citizens and 9,000 refugees, the figures Shāhīn prints. We print both{n}.",
  "Shāhīn (1982), p. 22; Cadora, <i>Remembering Ramallah</i>, p. 37, and Appendix B, p. 124 (scan page markers).")],
 'The Federation': [lambda: _P(
  "<b>The founding year, in each source’s own words.</b> The Federation’s own annual report for 2024–25 says: “Founded in 1952, the American Federation of Ramallah Palestine is a nationwide organization headquartered in Westland, Michigan.” Shāhīn (1982) and the municipality’s centennial book give 1958, the book as “the founding of the Union of Ramallah’s Sons in America in Detroit, Michigan.” Shaheen (2005) has incorporation in Michigan in 1959, and the Federation’s roster names Farid Shatara as its first president, 1959 to 1962. In 1978 <i>Aramco World</i> wrote that the Federation had sponsored annual conventions “for 19 years,” which points to a first convention in 1959; that is our inference. The 1952 founding is the five students’ magazine; the Friends School’s own history calls them “five Friends School graduates, who were attending Wayne State University in Detroit”{n}.",
  "American Federation of Ramallah Palestine, <i>Annual Report 2024–25</i>, PDF p. 2, “Who we are.” Ramallah Municipality, centennial book (2008), timeline: <span class='ar' dir='rtl'>إنشاء اتحاد أبناء رام الله في أمريكا في ديترويت ميتشيغان</span>. Shaheen (2005), pp. 353–355. AFRP, past presidents. P. Bates, “Reunion on the Potomac,” <i>Aramco World</i> (1978). Ramallah Friends School, history page.")],
 'The city, counted to the present': [lambda: _P(
  "<b>The day of the 1967 count.</b> The census volume itself gives the day for the Ramallah–Jericho region: it was enumerated on <b>21 September 1967</b>, under curfew. This is the occupying power’s count, and we use it only for its date and its figures{n}.",
  "Israeli Central Bureau of Statistics, <i>Census of Population 1967</i>, vol. 1, p. V, dates of enumeration, page image read (Israeli state source). The dataset documentation (Perlmann, Levy Institute, 2012) adds that a curfew was declared for the day of the enumeration."),
  lambda: _P(
  "<b>The Christian mayor is written into law.</b> Ramallah’s Christian mayor is not only a custom. Presidential Decree no. 19 of 2021 puts Ramallah first in its table, with 8 of the council’s 15 seats reserved for Christians, and its second article says that “the head of each of the councils named above shall be a Christian.” Earlier decrees on the same subject were issued in 2010, 2016 and 2017, under the 2005 amendment to the local elections law. Eight of fifteen is a political allocation, not a share of the population{n}.",
  "Decree no. 19 of 2021, dated 27 September 2021, <i>al-Waqāʾiʿ al-Filasṭīniyya</i> no. 184 (27 October 2021), pp. 30–31: <span class='ar' dir='rtl'>يكون رئيس كل من الهيئات المحلية المذكورة أعلاه مسيحيا</span> (Burqīn excepted). Central Elections Commission, decrees of 2010 (no. 4), 2016 and 2017, and the 2017 local elections report, annex 7. The Arabic wants an eye check.")],
}


def ent(date, grade, w2, title, note, body=''):
    for _tab in (ADD70, ADD72):
        for _k in [k for k in _tab if title.startswith(k)]:
            for _f in _tab.pop(_k):
                body += _f()
    for _k, _v in V69.items():
        body = body.replace('[[' + _k + ']]', _v)
        note = note.replace('[[' + _k + ']]', _v)
    assert '[[C' not in body and '[[C' not in note, title
    E.append(('e', CHAP[0], date, grade, w2, title, note, body))

txt = R.txt
SURF, TAN = '#FCFBF8', '#D4B483'
import math

def fig_pop_corrected():
    import math
    W, H = 860, 430
    pts = [(1596,400,'e'),(1838,850,'e'),(1839,1000,'e'),(1870,2000,'c'),(1896,2061,'e'),
           (1905,3214,'c'),(1922,3104,'c'),(1931,4286,'c'),(1944,6300,'c'),(1945,5080,'c'),
           (1953,13500,'c'),(1961,14759,'c'),
           (1967,12134,'c'),(1997,17851,'c'),(2007,27460,'c'),(2017,38998,'c'),(2021,42122,'c')]
    x0,x1,yb,yt = 92,800,320,88
    t0,t1,v0,v1 = 1580,2035,300,60000
    px = lambda y: x0+(x1-x0)*(y-t0)/(t1-t0)
    py = lambda v: yb-(yb-yt)*(math.log10(v)-math.log10(v0))/(math.log10(v1)-math.log10(v0))
    s=[f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Recorded population of Ramallah 1596 to 2024, log scale, with the 1916 typhus epidemic marked">']
    s.append(f'<rect width="{W}" height="{H}" fill="{SURF}"/>')
    s.append(txt(40,32,'EVERY NUMBER ANYONE HAS EVER RECORDED, 1596–2024',11,GOLD,'start','700','normal','1.4'))
    s.append(txt(40,50,'A logarithmic scale, because the town multiplied by more than a hundred.',10.5,GREY,'start','400','italic'))
    for i,(a,b,lab) in enumerate([(1917,1948,'British Mandate'),(1967,1994,'occupation before the Authority')]):
        s.append(f'<rect x="{px(a):.1f}" y="{yt}" width="{px(b)-px(a):.1f}" height="{yb-yt}" fill="{GOLD}" opacity=".10"/>')
        # stagger the two band labels so they cannot run into each other
        s.append(txt(px(a) if i==0 else px(b), yt-(18 if i==0 else 6), lab, 9, GOLD,
                     'end' if i==0 else 'start', '700'))
    for v in (500,1000,5000,10000,50000):
        s.append(f'<line x1="{x0}" y1="{py(v):.1f}" x2="{x1}" y2="{py(v):.1f}" stroke="{RULE}" stroke-width=".8"/>')
        s.append(txt(x0-10,py(v)+4,f'{v:,}',9.5,FOLIO,'end'))
    for yr in range(1600,2001,100):
        s.append(txt(px(yr),yb+20,str(yr),9.5,FOLIO,'middle'))
        s.append(f'<line x1="{px(yr):.1f}" y1="{yb}" x2="{px(yr):.1f}" y2="{yb+6}" stroke="{FOLIO}"/>')
    # the 1916 epidemic — annotated, NOT interpolated
    s.append(f'<line x1="{px(1916):.1f}" y1="{yt}" x2="{px(1916):.1f}" y2="{yb}" stroke="{RUST}" stroke-width="1.5" stroke-dasharray="5 4"/>')
    s.append(f'<path d="M{px(1916):.1f} {py(2600):.1f} q -6 26 2 46" fill="none" stroke="{RUST}" stroke-width="1.6"/>')
    s.append(txt(px(1916)-8,py(2600)-12,'1916 — typhus',10,RUST,'end','700'))
    s.append(txt(px(1916)-8,py(2600)+2,'“about 30 per cent',9.4,RUST,'end'))
    s.append(txt(px(1916)-8,py(2600)+14,'of Ramallah perish”',9.4,RUST,'end'))
    line=' '.join(f'{px(y):.1f},{py(v):.1f}' for y,v,_ in pts)
    s.append(f'<polyline points="{line}" fill="none" stroke="{GREEN}" stroke-width="2" stroke-linejoin="round"/>')
    # the true shape between 1896 and 1922, drawn as inference
    inf=[(1896,2061),(1914,2650),(1917,1850),(1922,3104)]
    li=' '.join(f'{px(y):.1f},{py(v):.1f}' for y,v in inf)
    s.append(f'<polyline points="{li}" fill="none" stroke="{RUST}" stroke-width="1.6" stroke-dasharray="4 4" opacity=".9"/>')
    for y,v,k in pts:
        x,yy=px(y),py(v)
        if k=='c': s.append(f'<circle cx="{x:.1f}" cy="{yy:.1f}" r="4.5" fill="{GREEN}" stroke="#fff" stroke-width="1.6"/>')
        elif k=='e': s.append(f'<circle cx="{x:.1f}" cy="{yy:.1f}" r="4.5" fill="{SURF}" stroke="{GREEN}" stroke-width="2"/>')
        else: s.append(f'<circle cx="{x:.1f}" cy="{yy:.1f}" r="4.5" fill="{FOLIO}" stroke="#fff" stroke-width="1.6"/>')
    for y,v,lab,dy in [(1596,400,'400',-12),(1905,3214,'3,214',-13),(1944,6300,'6,300',-12),
                       (1953,13500,'13,500 — the refugees',-12),
                       (1967,12134,'12,134 — counted under curfew',26),(2017,38998,'38,998',-12)]:
        anc = 'start' if lab.startswith('12,134') else 'middle'
        s.append(txt(px(y)+(9 if anc=='start' else 0),py(v)+dy,lab,10,INK,anc,'700'))
    ly=H-52
    for cx,lab,style in [(52,'an enumeration','solid'),(200,'an estimate, or a count of houses or taxable men','hollow'),(560,'projection','grey')]:
        if style=='solid': s.append(f'<circle cx="{cx}" cy="{ly}" r="4.5" fill="{GREEN}" stroke="#fff" stroke-width="1.6"/>')
        elif style=='hollow': s.append(f'<circle cx="{cx}" cy="{ly}" r="4.5" fill="{SURF}" stroke="{GREEN}" stroke-width="2"/>')
        else: s.append(f'<circle cx="{cx}" cy="{ly}" r="4.5" fill="{FOLIO}"/>')
        s.append(txt(cx+12,ly+4,lab,10,BODY))
    s.append(f'<line x1="640" y1="{ly}" x2="672" y2="{ly}" stroke="{RUST}" stroke-width="1.6" stroke-dasharray="4 4"/>')
    s.append(txt(680,ly+4,'inferred shape, not data',10,BODY))
    s.append(txt(40,H-34,'Two counts disagree: an estimate of about 1,100 is given for 1870, but the census Shāhīn cites for the same year counted 2,000. The chart follows the census.',10,BODY))
    s.append(txt(40,H-18,'The recorded points hide an event. Shāhīn records a typhus epidemic in 1916 killing about a third of the town; the dashed line shows what that means for the curve.',10.5,BODY,'start','700'))
    s.append('</svg>')
    return ''.join(s)

def fig_verdicts():
    W,H=860,372
    data=[('Confirmed',13,GREEN,'the deck and Shāhīn agree'),
          ('New',15,GOLD,'Shāhīn supplies what the deck did not have'),
          ('Refined',3,'#79B491','the date or detail sharpens'),
          ('Corrected',3,RUST,'the deck was wrong'),
          ('In conflict',1,'#8A5A1E','irreconcilable as they stand'),
          ('Untested',1,FOLIO,'no external check available')]
    tot=sum(d[1] for d in data)
    lx,x0,span=182,196,300.0
    s=[f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Result of testing the family presentation against Shahin 1982">']
    s.append(f'<rect width="{W}" height="{H}" fill="{SURF}"/>')
    s.append(txt(40,32,'THE FAMILY’S PRESENTATION, TESTED AGAINST ITS OWN 1982 HISTORY',11,GOLD,'start','700','normal','1.4'))
    s.append(txt(40,50,f'{tot} checkable claims, each read in Shāhīn’s Arabic text and against the external record.',10.5,GREY,'start','400','italic'))
    y=96
    for lab,n,col,note in data:
        w=span*n/15.0
        s.append(f'<rect x="{x0}" y="{y-13}" width="{w:.1f}" height="23" fill="{col}" rx="2"/>')
        s.append(txt(lx,y+4,lab,11.5,INK,'end','700'))
        s.append(txt(x0+w-8 if n>=3 else x0+w+8, y+4, str(n), 12,
                     '#FFFFFF' if n>=3 else INK, 'end' if n>=3 else 'start','700'))
        s.append(txt(x0+span+16,y+4,note,10.5,BODY))
        y+=36
    s.append(f'<line x1="40" y1="{y-6}" x2="820" y2="{y-6}" stroke="{RULE}"/>')
    s.append(txt(40,y+16,'Three corrections and one open conflict out of thirty-six.',11,INK,'start','700'))
    s.append(txt(40,y+32,'The family’s account of itself survives the test in better shape than most published histories would.',10.5,BODY))
    s.append('</svg>')
    return ''.join(s)

POP_CHART = fig_pop_corrected()
VERDICT_CHART = fig_verdicts()

# ═════════════════════════════════ THE LINE ═════════════════════════════════

CH(1)

sect('And in our own line', 'Where the family says it begins — and the only kind of evidence there is for it')
ent('—', 'scripture', 'shared', 'Adam and Eve',
 f"""Long before there was a town on our hill, there was the land, and there were people living on it. Our story begins twice: once in scripture, and once in the ground of these hills. Our family’s line begins where Genesis begins. <b>Adam to ʿĀbir (Eber) comes from Genesis 5 and 11</b>{c('Genesis 5:3–32 and 11:10–14. Fourteen names from Adam to Eber in the Masoretic text; fifteen in the Septuagint, which inserts Kainan. The family chart counts thirteen. See the branch figure below, and the appendix.')}, and from nothing else. No document, inscription or excavation reaches back that far, and we claim none.""",
 f"""
<p>First, it helps to know what kind of claim a line like this is. In the Middle Ages, peoples on
three continents traced their descent back to a universal ancestor. The House of Wessex traced theirs
to Woden and then to Noah, the Irish kings to Míl, and the Georgian kings to a grandson of Noah{c('<i>The Anglo-Saxon Chronicle</i>, s.a. 855, the genealogy of Æthelwulf; the Irish Milesian genealogies; the Georgian royal genealogies from Kartlos.')}.</p>
<p>A line like this says that a family <b>belongs to the human story</b>. It is not a chain of
checked fathers, and it would be a mistake to read it as one and then find it wanting.</p>
<p>Our way of building the line has changed. Our family has its own guide to it:
<b>John Aziz Mogannam’s chart of thirty-six named generations</b>, from Adam to Rāshid, in Arabic
and English. John is one of the two of us writing this history, and the chart is his own earlier
work. We no longer treat it as a source. Instead we build the line from the texts and documents
themselves: Genesis, the Arabic genealogists, Procopius and the Ottoman registers.</p>
<p>The chart is printed in the appendix for what it is: our family’s own working guide, and a very
good one, which the sources are allowed to correct{c('John Aziz Mogannam, chart of thirty-six named generations, Adam and Eve to Rāshid, in Arabic and English; the deep lineage compiled after al-Suwaydī, <i>Sabāʾik al-dhahab</i>, and Wüstenfeld’s tables, both in the family library. Printed in full in the appendix to this book, with the points at which it diverges from the sources. <b>Its compiler is a co-author of this book. Every correction to it printed here is therefore a self-correction, made in the open and in our own voice — which is the only kind this book is entitled to make.</b>')}. Where the two differ, we show the
difference and do not smooth it over.</p>
<p>One text is still a key to everything: <b>ʿAzīz Shāhīn’s history of 1982</b>{c('ʿAzīz Shāhīn, <span class="ar">كشف النقاب عن تاريخ رام الله والأنساب</span> (1982), 894 pp., OCR’d in full for this project; the English edition read complete. '+D('1982_Shahin_Kashf_al-Niqab_OCR_TEXT.txt')+'.')}. It is a
documentary history of the town, written from local memory and local records, and it can be checked
line by line. Where Shāhīn and the chart each carry an entry on their own, it carries the label
<span class="w2">TWO WITNESSES</span>. Where both are drinking from the same well, it carries the label
<span class="w2 sh">ONE TRADITION</span> instead.</p>"""),

ent('—', 'scripture', False, 'The three Bibles and the date of creation',
 'They differ by as much as <b>1,366 years</b>. From creation to Abraham is 1,948 years in the Masoretic text (the standard Hebrew Bible), 3,314 in the Septuagint (the ancient Greek translation) and 2,249 in the Samaritan (the Samaritans’ own books of Moses).',
 f"""
{fig(R.fig_chron(),'A line to Adam implies a date for Adam',
 'The three surviving forms of the Old Testament give systematically different ages for the patriarchs. Which text you follow depends on your church, and our family, as a Rūm Orthodox house, follows the Septuagint.',
 'Genesis 5 and 11 in the Masoretic, Septuagint and Samaritan recensions.')}
<p>These numbers are scripture, not chronology, and were never meant to be read as
chronology{c('The Byzantine <i>anno mundi</i> era, built on the Septuagint chronology, was the reckoning of the Orthodox churches; the Masoretic figures underlie the Western <i>anno mundi</i>.')}. The first thirteen generations of the chart make no claim a laboratory could
test. What they say is something no laboratory could touch: that our family belongs to the whole
human story.</p>"""),

CH(1)
ent('—', 'scripture', False, 'Joktan’s thirteen sons and their homeland',
 f"""Genesis 10:26–29 names thirteen sons of Joktan. <b>Several can be put on a map, and all of those are in South Arabia.</b> Hazarmaveth is Ḥaḍramawt and Sheba is Sabaʾ beyond serious doubt, and Ophir, Havilah and Uzal are also generally placed there{c('Genesis 10:26–29, and the closing formula at 10:29b, “all these were the descendants of Joktan.” <b>Ḥaṣarmāweṯ = Ḥaḍramawt</b> is the securest identification in the list: the consonantal skeleton ḥ-ḍ-r-m-w-t matches the South Arabian kingdom <i>ḥḍrmt</i> attested in Sabaic inscriptions and in Pliny (<i>NH</i> VI.32, <i>Atramitae</i>) and Ptolemy (<i>Chatramotitai</i>). The Hebrew form invites a folk-etymology “court of death”, which is secondary. <b>Šəḇā = Sabaʾ</b> is secure as a place; note that Genesis gives a Sheba three times over (10:7 via Cush, 10:28 via Joktan, 25:3 via Abraham and Jokshan), and which line the Sabaeans belong to is an old crux. <b>Ophir and Havilah are disputed</b> — Ophir has been placed in south-west Arabia, on the African Red Sea coast and in India, and no location commands agreement. The remaining nine are names that fit South Arabian onomastics and nothing more.')}. So scripture itself puts this branch in the very country that every later chapter of our family’s tradition walks out of.""",
 f"""
{fig(F4.fig_branch(),'The branch at ʿĀbir — where this line leaves Abraham’s',
 'Genesis 10:25 gives ʿĀbir (Eber) two sons and says so in a pun: <i>Peleg</i>, “because in his days the earth was divided” — <i>niplegāh</i>, from the same root as the name. Peleg’s line runs on through Reu, Serug, Nahor and Terah to <b>Abraham</b>, and from Abraham through Isaac, Jacob, Levi, Kohath and Amram to <b>Moses</b>. Joktan’s line is ours. <b>The two branches part three generations after the Flood — four in the Septuagint, which inserts Kainan — and six generations before Abraham</b>. So if we ask “where do we split from Abraham?”, the answer is that we never joined him. We share Noah, Shem and ʿĀbir with that line, and part company at ʿĀbir’s two sons.',
 'Genesis 5; 10:21–29; 11:10–26; Exodus 6:16–20. The Septuagint reading of Genesis 11:12–13 and Luke 3:36 for Kainan.')}
<p><b>Where Moses sits.</b> Counting inclusively, Moses is the seventh name from Abraham: Abraham,
Isaac, Jacob, Levi, Kohath, Amram, Moses. He stands on the far branch, not on ours{c('Genesis 11:26 for Abraham; Exodus 6:16–20 for Levi, Kohath, Amram and Moses; the same line at Numbers 26:57–59 and 1 Chronicles 6:1–3.')}.</p>
<p>That short chain is a known puzzle inside the text. The three generations from Levi to Moses,
Kohath and Amram between them, cannot span the four hundred and thirty years the same book gives to the stay in Egypt. The usual explanation is that the
list is a clan genealogy, telescoped (squeezed down) into personal names{c('Exodus 12:40–41 gives the sojourn in Egypt as 430 years, which three generations cannot span; Numbers 3:27–28 already counts 8,600 Kohathite males in the wilderness, impossible if Amram were Moses’s biological father. The standard reading is that “Amram” names the Amramite clan (Numbers 3:27) rather than a father — the list is telescoped. Genesis 15:16, “the fourth generation,” reflects the same short schema.')}. We meet the same
kind of puzzle at generation 35 of our own line, from the end of Chapter 4 onward, and the Bible does not solve it
either.</p>
<p>There is also a difference worth showing. The family chart counts <b>thirteen</b> names from Adam
to ʿĀbir. Genesis in the Masoretic text gives fourteen. The Septuagint gives fifteen, adding Kainan
between Arpachshad and Shelah, and Luke follows the Septuagint{c('Masoretic Genesis 5:3–32 and 11:10–14 give fourteen names from Adam to Eber. The Septuagint inserts Kainan at Genesis 11:12–13, and again at LXX Genesis 10:24 and LXX 1 Chronicles 1:18; Jubilees 8:1–5 has him too. Luke 3:36 follows the Septuagint, though the name is absent from Codex Bezae. Fourteen names in the Masoretic text against fifteen in the Septuagint.')}.</p>
<p>The difference is one or two names in a list nobody can check, and it changes nothing that matters
here. We show it because a chart our family uses as a guide should be measured against the text it
comes from, not the other way round.</p>"""),


sect('What the ground says', 'The other account of how this started — and it begins in this governorate')

ent('about 13,000 – 9,600 BC', 'attested', False, 'The Natufians and the cave at Shuqba',
 f"""Scripture tells the beginning one way, and the ground tells it another. The first people in this land to build regularly in stone and to hold a camp through the year are called Natufians. They take that name because their way of life was first identified, in 1928, in a cave called Shuqba, on the north bank of <b>Wadi an-Naṭūf, in the Ramallah and al-Bireh governorate</b>, some eighteen kilometres west-north-west of Ramallah{c('Shuqba Cave, north bank of Wādī an-Naṭūf, Ramallah and al-Bīra Governorate; 31.9819° N, 35.0436° E — some 17.7 km west-north-west of Ramallah. The figure of 28 km often attached to the cave is its distance from Jerusalem, not from Ramallah.')}. (A wadi is a valley that runs with water only after rain.) The oldest named thing in our whole story is local.""",
 f"""
{fig(ATLAS.fig_oldest(),'The oldest ground within a morning’s walk of Ramallah',
 'Every dot is a site with a published excavation, and every distance is measured from the centre of Ramallah. The nearest of them, Tell en-Naṣba, is about two and a half kilometres away. <b>What the map cannot show is how little of these highlands has been dug</b>: the blank spaces are gaps in the survey record, not gaps in the past, and we say so rather than suggest the district was empty.',
 'Garrod (1928, 1932); Boyd &amp; Crossland, Antiquity 74 (2000); Badè at Tell en-Naṣba (1926–35); Marquet-Krause and Callaway at et-Tell; Yeivin at ʿAin Samiya; Khalaily and Vardi at Motza; Perrot and Khalaily at Abu Ghosh; Kenyon at Tell es-Sultan.')}
<p><b>Dorothy Garrod dug the cave at Shuqba in 1928</b>, for the British School of Archaeology in
Jerusalem. She named the industry she found there, meaning its style of stone tools, after the
wadi{c('D. A. E. Garrod, “Excavation of a Palaeolithic cave in western Judaea,” <i>Quarterly Statement of the Palestine Exploration Fund</i> 60 (1928), 182–85; and “A new Mesolithic industry: the Natufian of Palestine,” <i>Journal of the Royal Anthropological Institute</i> 62 (1932), 257–69 — the formal naming paper. The full excavation report is Garrod &amp; D. M. A. Bate, “Excavations at the cave of Shukbah, Palestine, 1928,” <i>Proceedings of the Prehistoric Society</i> 8 (1942), 1–20.')}.</p>
<p>She was not the first to find the cave. Fr Alexis Mallon had noted it in 1924 and urged the
School to take it on. But hers is the excavation that gave the culture its name, and that name is a
Palestinian place-name{c('Alexis Mallon, “Quelques stations préhistoriques de Palestine,” <i>Mélanges de l’Université Saint-Joseph</i> 19 (1925), 191–92. Fieldwork was resumed at the cave and in the wadi by Brian Boyd and Zoë Crossland, “New fieldwork at Shuqba Cave and in Wadi en-Natuf, Western Judea,” <i>Antiquity</i> 74:286 (2000), 755–56.')}.</p>
<p>The Natufians are often called the first settled people in the world. That is more than the
evidence carries. Brush huts with prepared floors and bedding at Ohalo II, on the Sea of Galilee, are
some eight thousand years older, and scholars still argue over how settled the Natufians really
were{c('Chronology after L. Grosman, “The Natufian Chronological Scheme — New Insights and their Implications,” in Bar-Yosef &amp; Valla (eds), <i>Natufian Foragers in the Levant</i> (2013), 622–37: roughly 13,050–9,550 cal BC, conventionally split into an Early and a Late phase — though T. Richter et al., <i>Scientific Reports</i> 7 (2017), 17025, show the two overlap. For the earlier huts: D. Nadel et al., “Stone Age hut in Israel yields world’s oldest evidence of bedding,” <i>PNAS</i> 101:17 (2004), 6821–26. For the sceptical case on sedentism: Brian Boyd, “On ‘sedentism’ in the Later Epipalaeolithic (Natufian) Levant,” <i>World Archaeology</i> 38:2 (2006), 164–78.')}.</p>
<p>What we can say is narrower, and still remarkable. <b>They were the first here to build in stone
as a matter of course</b>, and the first to keep base camps lived in through much or all of the year,
before farming began.</p>
<p>The best single clue is not a building at all. The house mouse pushes out its wild cousin only
where people stay put long enough to feed it, and <b>the house mouse appears at Natufian
sites</b>{c('L. Weissbrod, F. B. Marshall, F. R. Valla, H. Khalaily, G. Bar-Oz, J.-C. Auffray, J.-D. Vigne &amp; T. Cucchi, “Origins of house mice in ecological niches created by settled hunter-gatherers in the Levant 15,000 y ago,” <i>PNAS</i> 114:16 (2017), 4099–4104. Cited here as strong but not unchallenged; it drew a published comment and reply in the same journal.')}.</p>
<p>Below the Natufian floor of the same cave lay something older still. Garrod found a single tooth
in the Mousterian layer beneath, the layer of the Neanderthal-age stone tools. It is a child’s
<b>permanent</b> lower first molar, from someone about seven to twelve years old.</p>
<p>In 2021 a fresh study by micro-CT scan identified the tooth as <b>Neanderthal, the southernmost
Neanderthal yet securely identified</b>. On the excavators’ reading, which is disputed, it was found
with Nubian Levallois stone-working, a technique once treated as a mark of
<i>Homo sapiens</i>{c('J. Blinkhorn, C. Zanolli, T. Compton, H. S. Groucutt, E. M. L. Scerri, L. Crété, C. Stringer, M. D. Petraglia &amp; S. Blockley, “Nubian Levallois technology associated with southernmost Neanderthals,” <i>Scientific Reports</i> 11 (2021), 2869, DOI 10.1038/s41598-021-82257-6. The specimen is NHMUK PA EM 3869, a lower right first molar of a child from Layer D; it should not be confused with the Natufian burials Garrod found in Layer B above it, and there is still no direct chronometric date on Layer D. <b>The Nubian association was rebutted the following year in the same journal</b> — Hallinan, Barzilai, Bicho, Cascalheira, Demidenko, Goder-Goldberger, Hovers, Marks, Oron &amp; Rose, “No direct evidence for the presence of Nubian Levallois technology and its association with Neanderthals at Shukbah Cave,” <i>Scientific Reports</i> 12 (2022), DOI 10.1038/s41598-022-05072-7 — on the grounds that Layer D is a brecciated palimpsest that cannot be treated as one undisturbed deposit. <b>The tooth is Neanderthal. What it was found with is still argued.</b>')}. The cave is eighteen kilometres from Ramallah, in our own governorate,
and there is still no direct date on the layer.</p>"""),

ent('about 9600 BC', 'attested', False, 'Jericho, twenty-three kilometres away',
 f"""Twenty-three kilometres from Ramallah as the crow flies, down the eastern slope from our ridge, at Tell es-Sultan, people stopped moving and stayed. They settled there for good from about <b>9600 BC</b>. About 9000 BC they built a round stone tower 8.5 metres high, with twenty-two steps inside it, and a wall 3.6 metres high and 1.8 metres thick at the base{c('Kathleen M. Kenyon &amp; T. A. Holland (eds), <i>Excavations at Jericho, Vol. 3: The Architecture and Stratigraphy of the Tell</i> (London: British School of Archaeology in Jerusalem, 1981). The tower is c. 8.5 m high and c. 9 m across at the base, tapering to c. 7 m, with an internal staircase of twenty-two stone steps; the wall over 3.6 m high and 1.8 m thick at the base. Earlier work: Sellin and Watzinger 1907–11; Garstang 1930–36, whose Bronze Age dating Kenyon overturned.')}. It is one of the earliest permanent settlements known anywhere on earth. It is also the same mound as the Jericho of Joshua 6. But that town, if it is in this tell at all, lies near the <i>top</i>, some eight thousand years higher in the layers than the tower{c('The Jericho of Joshua 6 would belong to the Late Bronze Age, at the top of a mound whose base is Pre-Pottery Neolithic A. Whether there was a walled Late Bronze town there at all is one of the longest-running arguments in the archaeology of this country — Garstang read the destruction as Joshua’s, Kenyon re-dated it, and the debate has not closed. <b>This book takes no position on it</b>, because its subject here is the bottom of the mound and not the top. See Sparks, Finlayson, Wagemakers &amp; Briffa (eds), <i>Digging Up Jericho</i> (2020).')}. One hill holds forty layers, and here we are standing on the bottom one.""",
 f"""
<p>Two things often said about Jericho should not be said. It is <i>not</i> “the oldest
continuously inhabited town in the world”. The tell has known
gaps. There are several centuries between the Pre-Pottery Neolithic A and B
(the early farming ages before pottery), more in the Pottery Neolithic, abandonment around 1950 BC,
and near-abandonment after the Iron Age. The modern town also sits <i>beside</i> the mound, not on
it.</p>
<p>Nor is it safely the oldest walled town. <b>The round towers at Tell Qaramel in northern Syria are
some two thousand years older</b>, and Jericho’s wall has never been traced around the whole
settlement{c('On the occupation gaps and the making of the “oldest city” claim, see Rachael Sparks, Bill Finlayson, Bart Wagemakers &amp; Josef Briffa (eds), <i>Digging Up Jericho: Past, Present and Future</i> (Oxford: Archaeopress, 2020) — the best single volume on the evidence and its historiography. For the older towers: R. F. Mazurowski &amp; Y. Kanjou (eds), <i>Tell Qaramel 1999–2007</i> (Warsaw: PCMA, 2012), with radiocarbon in Mazurowski et al., <i>Radiocarbon</i> 51:2 (2009), 771–81: the earliest tower c. 10,900–9,670 cal BC.')}.</p>
<p>UNESCO inscribed the site in 2023 under the State of Palestine. It calls Jericho a sizeable
permanent settlement and ties it to the shift to a settled way of life. <b>We follow UNESCO’s
wording</b>, not the tourist one{c('UNESCO World Heritage List no. 1687, “Ancient Jericho/Tell es-Sultan,” inscribed 2023 at the extended 45th session of the World Heritage Committee, Riyadh, under the State of Palestine, on criteria (iii) and (iv). The statement of Outstanding Universal Value describes deposits “dating back to about 10,500 BC” and a “sizeable permanent settlement.” <a href="https://whc.unesco.org/en/list/1687/">whc.unesco.org/en/list/1687</a>.')}.</p>
<p>What the tower was for is still unresolved. Kathleen Kenyon, who found it in 1952, read the tower
and wall as fortification. Ofer Bar-Yosef argued they were defences against floods and mudflows.</p>
<p>Bar-Yosef made the strongest single point in the debate. <b>There is no evidence of burnt
settlements, mass casualties or comparable fortifications anywhere in the Levant before the sixth
millennium BC</b>, some three thousand years later. Anyone who reads the tower as a defence has to
explain that absence. Others have read the tower as a monument of political power over a prime
spring, or as a solstice marker{c('Kenyon &amp; Holland (1981) for the defensive reading; Ofer Bar-Yosef, “The Walls of Jericho: An Alternative Interpretation,” <i>Current Anthropology</i> 27:2 (1986), 157–62, for flood defence and the absence-of-warfare argument; Danny Naveh, “PPNA Jericho: A Socio-Political Perspective,” <i>Cambridge Archaeological Journal</i> 13:1 (2003), 83–96; Ran Barkai &amp; Roy Liran, “Midsummer Sunset at Neolithic Jericho,” <i>Time and Mind</i> 1:3 (2008), 273–83.')}. No explanation is agreed, and we set out the disagreement
rather than pick a side.</p>
<p>One caution on dates. The figure “8000 BC”, still common in books, is an <b>uncalibrated</b>
radiocarbon date from Kenyon’s samples, that is, one not yet corrected against the known record of
the past. Calibrated, the Pre-Pottery Neolithic A at Tell es-Sultan runs roughly 9700/9600 to
8600/8500 BC, and the tower is about eleven thousand years old, around 9000 BC. We use the calibrated
figures throughout.</p>
<p>Who did the digging matters too. Every excavator named so far is European or Israeli, and our
earlier versions told Jericho only through them. That is not how the mound has actually been dug for
the last thirty years.</p>
<p>Since <b>1997</b> Tell es-Sultan has been dug by a joint expedition of the Palestinian Department
of Antiquities and Cultural Heritage, under the Ministry of Tourism and Antiquities, and Rome «La
Sapienza». It is directed by Hamdan Taha and Lorenzo Nigro, with Nicolò Marchetti in the early
seasons. The work is still running, and Lorenzo Nigro and Jehad Yasine have published an interim
report on the Bronze and Iron Age towns, covering the seasons of 2019–2023{c('The Italian–Palestinian Expedition to Tell es-Sultan, from 1997: Rome «La Sapienza» with the Palestinian Ministry of Tourism and Antiquities, Department of Antiquities and Cultural Heritage (MOTA-DACH). Season reports are published jointly under Lorenzo Nigro and Hamdan Taha, with Nicolò Marchetti in the first seasons — e.g. Marchetti, Nigro &amp; Taha, “Preliminary Report on the Third and Fourth Seasons… 1999–2000,” in I. Thuesen (ed.), <i>Proceedings of the Second ICAANE</i> (Bologna, 2016), 581–97; Nigro &amp; Taha, “The Early Bronze Age Palace and Fortifications at Tell es-Sultan/Jericho: the 6th–7th seasons (2010–2011)”; and the interim report on the Bronze and Iron Age cities covering 2019–2023. See also Nigro, <i>Aside the Spring: Tell es-Sultan / Ancient Jericho — the Tale of an Early City and Water Control in Ancient Palestine</i>.')}.</p>
<p>It is their work, not Kenyon’s, that now describes the <i>town</i> around the tower. By
<b>Early Bronze II, about 3000–2700 BC</b>, it had an urban plan and a massive system of
fortification. A double city wall has been traced at the southern and south-western edges of the
mound. Early Bronze III saw a society centred on a palace, and later settlement spread outside the
Middle Bronze wall.</p>
<p>The file on which UNESCO inscribed the site in 2023 <b>was prepared by a Palestinian team</b>
under that same ministry{c('Hamdan Taha, “Tell es-Sultan, Ancient Jericho,” <i>This Week in Palestine</i>: “Following the transfer of authority to the Palestinian Authority in 1994, the Palestinian Department of Antiquities, working jointly with La Sapienza University of Rome, resumed the work at Tell es-Sultan,” and the nomination file was “being prepared by a team of experts under the auspices of the Ministry of Tourism and Antiquities.” Inscribed 2023 as World Heritage no. 1687, under the State of Palestine.')}.</p>
<p>The tower is still Kenyon’s find, and what it was for is still unresolved. But the town around it
has been dug again, dated again and published by the people whose town it is, and we now cite them
for it.</p>
{FIX('Jericho told entirely through Sellin and Watzinger, Garstang, Kenyon and Bar-Yosef — every excavator named in the entry European or Israeli.',
        'The current excavation is <b>Palestinian–Italian and has run since 1997</b>: MOTA-DACH with Rome «La Sapienza», <b>Hamdan Taha</b> and <b>Lorenzo Nigro</b> directing. Their sequence for the Bronze Age town is the one this book now follows, and the 2023 UNESCO nomination is a Palestinian document.',
        'Not a factual correction but a correction of attribution, and the book’s own standard requires it: <i>Palestinian and Arab scholarship is cited as the source, and the foreign partner as the route.</i> The Neolithic tower remains Kenyon’s discovery and is still credited to her; what changes is that the Bronze Age town, the fortifications and the site’s present interpretation are credited to the expedition that produced them.')}"""),

ent('the whole of it', 'attested', False, 'What this land is made of',
 'Before the story starts moving, here is one picture of the whole of it. It shows <b>fifteen thousand years of people living on this ridge and around it</b>, drawn as a cut through a tell, a mound built up from layer upon layer of settlement. Our own family walks in at the fourth layer from the top.',
 fig(F4.fig_layers(),'The land, drawn as a tell — fifteen thousand years of layering',
  'Read it from the bottom up, the way a section is dug. <b>Nothing in this column replaces the layer beneath it.</b> Arrivals are absorbed; only the Franks, in the thin purple band, come and go again. Our family arrives in the Ottoman layer, four from the top, into a land that had already been lived in continuously for more than eleven thousand years. <i>The layers are drawn thick enough to read, not to scale in time; every date in the column is calibrated and sourced in the entries around this figure.</i>',
  'Our own entries throughout: the deep layers from the entries that follow in this chapter, the later ones from the chapters after it.')),

CH(4)
sect('And in our own line', 'A dam in Joktan’s country, and a road that ends at Gaza')
ent('8th–7th c. BCE', 'attested', 'shared', 'The great dam of Maʾrib is built',
 f"""The great sluice works of the Sabaean dam, the stone gates that let its water out into the fields, are dated by inscription and excavation to about the eighth and seventh centuries BC{c('The Maʾrib sluice structures, Sabaean period, c. 8th–7th c. BCE, with earlier earthworks beneath; ʿAdnān al-Ḥaddādīn, <i>A Brief History of the Haddadeen</i> (MS, Ramallah City Hall, 8 August 1953), as printed in Shāhīn (1982), ch. 1.')}. Our family’s own account, ʿAdnān al-Ḥaddādīn’s manuscript of 1953 as Shāhīn prints it, remembers the dam “built as early as the 7th century B.C.” That memory lands on the right phase, with a caution we come to in a moment.""",
 f"""
<p>It is worth pausing on what the dam actually was, because <b>the whole first half of our family’s
story is a story about water</b>. The dam was not a reservoir. It was a diversion wall of packed earth, some
620 to 680 metres long as the surveys variously give it{c('The length differs by survey and by building phase: Ueli Brunner, “Die sabäische Dammanlage Mabnā al-Ḥašraǧ” (2014), gives a 620-metre earth dam up to 20 metres high; Kohler (1994) gives 680 metres; Christian Robin (2002) gives 650 metres long and 15 high for the final stage. Brunner also confirms that the dam stored no water. Earlier printings of this book gave 580 metres, which none of them supports.')}. It was thrown across the Wadi Dhana where
the valley breaks through a gap between two mountains.</p>
<p>Its purpose was to catch the flash floods that come off the Yemeni highlands twice a year. Through
two great masonry sluice towers, it pushed that water into a network of canals{c('On the structure and its phases: the Sabaean earthworks of the 8th–7th centuries BCE, the monumental sluice towers of the 6th, and the successive raisings of the wall recorded in the Sabaic inscriptions of the mukarribs. The irrigated area is generally estimated at some 9,600 hectares.')}. It watered
something on the order of ninety-six square kilometres of desert.</p>
<p>With repairs, <b>it worked for more than a thousand years</b>. Almost nothing else
in the ancient world matched that working life, though the Dujiangyan irrigation works in Sichuan,
begun about 256 BC, are still running today{c('UNESCO World Heritage List no. 1001, “Mount Qingcheng and the Dujiangyan Irrigation System,” inscribed 2000: built c. 256 BC and still in operation. Earlier editions of this book said nothing else in the ancient world ran as long as the Maʾrib dam; that is not true, and the claim is now stated as a comparison rather than a record.')}.</p>
{fig(F3.fig_dam_eng(),'The machine that watered a kingdom',
 'The dam of Maʾrib in schematic: the wadi, the gap between the two Balaq mountains, the wall, the two sluices, and the two irrigated gardens on either bank. The Qurʾān’s phrase for Sabaʾ — “two gardens, on the right hand and on the left” — is a literal description of this diagram.',
 'The Sabaic inscriptions and the excavation record; Qurʾān 34:15.')}
<p>Here the Qurʾān joins Genesis and our family’s manuscript. The Qurʾān describes this very place, in these very
terms: <i>“There was for Sabaʾ, in their dwelling-place, a sign: two gardens, on the right hand and
on the left”</i>{c('Qurʾān 34 (Sūrat Sabaʾ):15. The chapter takes its name from the kingdom.')}.</p>
<p>So the pieces fit together. Genesis puts Joktan’s sons in this country. Arab tradition knows
Joktan as Qaḥṭān, father of the southern Arabs, and counts the Azd among his descendants. The Qurʾān describes its
gardens. <b>Our family’s 1953 manuscript dates the dam’s monumental phase to the seventh century
BC</b>, and the inscriptions bear that phase out.</p>
<p>Three cautions belong here. Genesis says nothing at all about a dam: it is a witness to the
<i>country</i>, not to the structure. And a 1953 Arabic manuscript that gives a date as “the 7th
century B.C.” is far more likely to be repeating published European scholarship on Maʾrib than
remembering anything. <b>It is the one-tradition problem in small, and it applies to our family’s own
text.</b></p>
<p>The men who surveyed the oasis do not all give the same date. Ueli Brunner puts the first
continuous Great Dam in the sixth century BC, and flood irrigation at the Wadi Dhana as far back as the
third millennium BC{c('Brunner (2014): the Sabaeans closed the wadi with one continuous barrier in the sixth century BC, “the hour of birth of the Great Dam,” where irrigation had begun in the third millennium BC, and the design held for about a thousand years. Kohler (1994) gives about 600 BC. Earlier printings of this book put the first dam-building at 1750–1700 BC; no specialist source we have read gives that date.')}. So “as early as the 7th century B.C.” is close for the
dam, and late by two thousand years about the site.</p>[[C11]]"""),

CH(2)

sect('What the ground says', 'The first people of this land, and the layers they left')
ent('about 3500 – 2400 BC', 'attested', False, 'The first villages of this district',
 f"""These are not general claims about “the region”. They are <b>named, excavated and dated sites within a few kilometres of our town</b>. Tell en-Naṣba, on the edge of al-Bireh and about two and a half kilometres from the centre of Ramallah, was a village of about 3500–3300 BC, in the Late Chalcolithic (the Copper Age) and Early Bronze I{c('Tell en-Naṣba, identified with biblical Mizpah, on the edge of al-Bīra. Excavated in five seasons, 1926–1935, by William Frederic Badè for the Pacific School of Religion. The Late Chalcolithic / Early Bronze I village is Stratum 5, c. 3500–3300 BC, after which the site was long abandoned.')}. et-Tell, five kilometres east, was an Early Bronze town lived in from 3200 to 2400 BC{c('et-Tell, generally identified with biblical Ai, 5.3 km east of Ramallah. Excavated by John Garstang (1928), Judith Marquet-Krause (1933–35), Joseph Callaway (1964–70) and Hani Nur el-Din (2005–07). Occupation runs from Early Bronze I through Early Bronze III, c. 3200–2400 BC.')}. ʿAin Samiya, fifteen and a half kilometres north-east, holds a cemetery of shaft tombs from the Intermediate Bronze Age, the time between the Early and Middle Bronze Ages, 2300–2000 BC. The famous ʿAin Samiya goblet came from it{c('ʿAin Samiya and the neighbouring Dhahr Mirzbaneh, east of Kafr Malik. <b>The distance is now checked:</b> the spring and valley of ʿAin Samiya lie at about 31.988° N, 35.333° E (Palestine grid 181/155), some 15.5 km in a straight line north-east of al-Manāra square in Ramallah (31.904° N, 35.203° E). Earlier editions gave about 13 km, measured from the marker on our maps at 31.97° N, 35.32° E, which sits a little short of the site: Intermediate Bronze Age (Early Bronze IV) shaft-tomb cemeteries, c. 2300–2000 BC. Paul Lapp excavated Dhahr Mirzbaneh in 1963; Zvi Yeivin excavated ʿAin Samiya in 1970–71. The ʿAin Samiya goblet is an Intermediate Bronze piece, not a Chalcolithic one.')}.""",
 """
<p>Two mistakes are common in local writing, and we put them right here. ʿAin Samiya is often
called Chalcolithic. <b>It is Intermediate Bronze Age</b>, some fifteen hundred years later. And
et-Tell has no Chalcolithic phase at all: its earliest settlement is Early Bronze I, about
3200 BC.</p>
<p>We name these places for a simple reason. When we say the people of these hills were never
replaced, we are not arguing from a general theory about the Levant. <b>We are speaking of ground you
can walk to from Ramallah in an afternoon</b>, ground that has been dug, dated and published.</p>"""),

ent('about 1500 BCE', 'attested', False, 'The Canaanite population of these highlands',
 f"""Everything that comes later is added to this people. <b>Lebanese today draw more than ninety per cent of their ancestry from the Bronze Age Canaanite population.</b> People of the southern Levant today, our town among them by inference, carry a large Bronze Age share of the same kind, alongside later mixing{c('Haber et al., “Continuity and Admixture in the Last Five Millennia of Levantine History,” <i>AJHG</i> 101:2 (2017), 274–82 — the >90% figure is measured for <b>present-day Lebanese</b> against Bronze Age Sidon, and earlier editions of this book wrongly generalised it to “Levantine ancestry.” For the southern Levant: Agranat-Tamir et al., <i>Cell</i> 181:5 (2020), 1146–57.')}.""",
 f"""
{fig(F.fig_confluence(),'How a people is made',
 'Ten arrivals and one people. Each bar begins when that group enters the record and fades into the common green as it is absorbed. Only the Samaritans keep their own colour to the present; only the Franks stop. Our family’s own stream — Arabs, and Ghassān — is the ninth bar. It was absorbed like the rest, and that is our whole story in one picture.',
 'Haber et al. (2017); Feldman et al. (2019); Agranat-Tamir et al. (2020) (Israeli authors; cited for context); Haber et al. (2019) on the Crusader pulse; Killebrew (2005); Ehrlich (2022) on conversion (Israeli authors; cited for context).')}
<p><b>At no point in the last four thousand years were the people of this country wholly replaced.</b>
The Philistines, as Chapter 2 shows, are the case that can be measured.{c('Feldman et al., “Ancient DNA sheds light on the genetic origins of early Iron Age Philistines,” <i>Science Advances</i> 5:7 (2019), eaax0061.')}</p>
<p>They were not driven out. They married their neighbours. The Idumaeans were absorbed by AD 70.
The Nabataeans’ kingdom became a Roman province in 106 while its people stayed put. <b>The country
turned Christian, then largely Muslim, by conversion and not by replacement</b>{c('Michael Ehrlich, <i>The Islamization of the Holy Land, 634–1800</i> (Arc Humanities, 2022); Milka Levy-Rubin on Arabization versus Islamization.')}.</p>
<p>The Samaritans, who never merged, are still on Mount Gerizim, a living point of comparison. The
Franks, who really did leave, prove the rule by breaking it. <b>They left a trace in the DNA, and
even that trace faded</b>{c('Haber et al., “A Transient Pulse of Genetic Admixture from the Crusaders in the Near East,” <i>AJHG</i> 104:5 (2019): “present-day populations derive most of their ancestry from local people who preceded the Crusades.”')}.</p>
<p>So a Christian family claiming descent through Ghassān from Yemen, a Muslim family in the next
village claiming the Ḥijāz, and the Samaritans of Nablus claiming to have gone nowhere are not making
rival claims. <b>They are describing different arrivals into the same people.</b> Our own family’s
arrival is the ninth bar in the chart.</p>"""),

ent('nobody can date it, and it is still in use', 'attested', False,
    'The terraces and their stone towers',
 f'''The hills around Ramallah are not really hills. They are staircases. Every workable slope within
sight of the town has been cut into level steps, held up by dry-stone walls called sanāsil (<span class="ar">سناسل</span>),
the local word. Nothing holds such a wall up but the weight of its own stones: no mortar, no
foundation, no bonding material of any kind{c('Shadi Ghadban, “Palestinian Dry Stone Structures — An Endogenous Expression of Cultural Landscape,” <i>Journal “Sustainable Development, Culture, Traditions”</i> 1b (2015), 34–46, at 44: the structures are “generally constructed from rubble natural stones with irregular and polygonal forms without using any bonding material,” the stones “simply fitted in harmony with their natural form and not in regular layers.” ' + D('2015_Ghadban_Palestinian_Dry_Stone_Structures_SDCT_1b.pdf') + '.')}. In the fields stand small round huts with stone
roofs, built by the farmers so that somebody could sleep beside the crop while it ripened. In 2013 two
Palestinian scholars went out and counted them. In al-Tireh quarter and the village of ʿAin Qinia
alone, on Ramallah’s own western and northern edge, they recorded <b>one hundred and sixty-seven
watchtowers over some three thousand dunums</b>{c('Salah Hussein Al-Houdalieh &amp; Shadi Sami Ghadban, “Agricultural Watchtowers in Al-Tireh Quarter and ʿAin Qinia Village, Ramallah, Palestine,” <i>International Journal of Architectural Heritage</i> 7:5 (2013), 509–535, DOI 10.1080/15583058.2011.654049. The survey documented <b>167 watchtowers distributed over an area of approximately 3,000 dunums</b>, by site documentation, fieldwork and interviews with residents. Al-Houdalieh is the same al-Quds University archaeologist who excavated Khirbet et-Tireh; Ghadban is professor of architectural engineering at Birzeit.')}. (A dunum is the local measure of land.)''',
 f"""
{fig(F4.fig_terraces(), 'The terraces, and one of the towers standing in them',
 'A hillside above Ramallah drawn in section. Every riser is a dry-stone wall; every tread is a field; the small domed hut on the third terrace is one of the hundred and sixty-seven. The cutaway shows how the roof closes — each course of stone oversailing the one below until the last two meet, with nothing binding them. <b>The strip along the bottom is the year:</b> the tower is occupied for grain in May and June, for figs and grapes from July to September, and for the olives in October and November.',
 'Al-Houdalieh &amp; Ghadban, <i>International Journal of Architectural Heritage</i> 7:5 (2013), 509–35, for the count and the survey; Ghadban (2012, 2015) for the construction and the seasons.')}
<p>The roofs of the huts are corbelled. Each course of stone juts out a little over the one below,
until the last two meet at the top, with nothing binding them.</p>
<p><b>Nobody can date the terraces.</b> Corbelled dry-stone building is old in this region, probably
Early Bronze Age in origin. But a terrace wall is not a monument. It is a machine, and a machine in
use gets repaired.</p>
<p>The stone that fell out last winter went back in this spring, and the stone beside it may have
been set by a Canaanite. A wall that has never been allowed to fall down has no layers to date. The
survey says so plainly: there is no concrete evidence for when the dry-stone structures of Palestine
first appeared{c('Ghadban (2015), 37 and 39: corbelled structures “originated mainly in the Near East of the Mediterranean Basin probably at the beginning of the Early Bronze Age,” but there is “no concrete evidence regarding when exactly the dry-stone structures first appeared” in Palestine. <b>This book therefore gives the terraces no date at all rather than an invented one.</b>')}.</p>
<p>What we can date is the work, because the work follows the seasons and has not changed. The tower
is used when there is something in the field worth losing: the grain and early fruit in May and June,
the figs and grapes from July through September, and the olives in October and November. <b>For seven
months of the year, somebody from the household is sleeping out on the land.</b></p>
<p>The huts were built together, several men to a tower, and the owner of the ground fed them while
they built it{c('Ghadban (2015), 40 and 43, on the three harvest seasons — “early fruit and grain harvest… May and June,” “figs and grape-vines… July through September,” “olive harvesting… October and November” — and on cooperative building: “peasants would mostly collaborate in building the structures,” with the owner providing food. Also Ghadban, “The Architecture of the Palestinian Dry-Stone Hut — Al-mantarah,” <i>Journal of Comparative Cultural Studies in Architecture</i> 6 (2012), 16–25.')}.</p>
<p>This is our district’s own technology. <b>Of everything in these early pages, it is the one thing
our own ancestors certainly made with their hands.</b> Later, churches were built by patrons,
registers were written by clerks, and the armies belonged to somebody else. The terraces were built by
whoever was going to eat from them. They are still there, and people are still eating from them.</p>
<p>They are also disappearing. Ghadban’s parallel survey of the walls themselves found roughly
<b>eighty-seven per cent of them partly collapsed</b>. The causes are land confiscation and settlement
expansion, the separation wall cutting farmers off from their own plots, the town spreading up its own
hillsides, and the plain fact that fewer people now farm{c('Ghadban (2015), 36 and 42: “approximately 87% of the individual walls are partially destroyed,” under pressure from land confiscation, settlement expansion, the separation wall, the declining economic weight of agriculture and “rapid and largely sprawl urban expansion.” <b>The 87 per cent is measured on the walls, not on the towers; the 167 towers are those still standing.</b>')}. A wall that is repaired every year
survives four thousand years. A wall that nobody walks to falls down in twenty.</p>"""),

ent('about 1350 BCE', 'documents', False, 'The Amarna letters and who worked the fields',
 f'''About 1350 BC the rulers of Canaan’s towns wrote letters to the pharaoh in Egypt. The clay tablets were found at Amarna, in Egypt, and are called the Amarna letters. Jerusalem, Shechem, Gezer and Lachish wrote in Akkadian, the written language of the courts of the time{c('The Tell el-Amarna correspondence, fourteenth century BCE: some 350 letters and administrative texts from the Egyptian capital at Akhetaten, found in 1887. The standard edition is William L. Moran, <i>The Amarna Letters</i> (Baltimore: Johns Hopkins, 1992); see also Anson F. Rainey, <i>The El-Amarna Correspondence</i>, 2 vols (Leiden: Brill, 2015).')}. These were the city-states of our landscape, and they were Canaanite. Even our town’s name keeps the sound of that age: rām (<span class="ar">رام</span>) is a Semitic root meaning <i>height</i>, Canaanite-era vocabulary still doing its job{c('al-Dabbāgh, <span class="ar">بلادنا فلسطين</span>, viii/2, on <span class="ar">رام</span>; the same root as Hebrew <i>rām</i> and Aramaic <i>rāmā</i>.')}. The letters are usually read as diplomacy: kings, tribute, the <i>ʿapiru</i> (people on the margins), who is loyal and who is not. <b>Read them the way an employer reads a file, and they are about labour</b>: who goes up the hill, and who ploughs.''',
 f"""
<p>The clearest sentence in the whole archive on that question is on a small tablet in the Louvre,
six and a half centimetres by six, numbered <b>EA 365</b>. Moran gives it the heading
<i>Furnishing corvée workers</i>. A corvée is unpaid labour owed to a ruler. The letter is from
Biridiya, the mayor of Megiddo, and after the usual words of bowing down it says this{c('EA 365, Louvre, Antiquités orientales AO 7098; 6.5 × 6.0 cm. Translations: Moran (1992); Anson F. Rainey (1970); earlier Mercer (1939) and Albright in <i>ANET</i> (1969). The rendering quoted here follows the standard English of the passage.')}:</p>
<blockquote>Let the king, my lord, be aware regarding his servant and his city.
<b>Behold, I alone am cultivating in the city of Shunama; and, as for me, I provide forced
labourers.</b> Now, behold, the mayors who are near me do not do as I do. They do not cultivate
in the city of Shunama, and they do not provide forced labourers. <b>I alone provide forced
labourers.</b>
<span class="cite">Amarna letter EA 365, Biridiya of Megiddo to the king of Egypt · Louvre AO 7098</span></blockquote>
<p>The word he uses is <i>massu</i>. <b>It is the same Semitic word as the Hebrew Bible’s
<i>mas</i></b>, the levy of forced labour a king raises out of his own people{c('Akkadian <i>massu</i> / <i>mas</i>, corvée labour imposed on subject populations for building, quarrying and agricultural work; the same term appears in Biblical Hebrew as <span class="ar">מס</span> <i>mas</i>, e.g. 1 Kings 5:13–14 and 9:15. See Moran (1992), glossary s.v.; Rainey, <i>El-Amarna Correspondence</i>, ii, on the labour vocabulary of the Megiddo letters.')}. Biridiya is
not complaining about an invasion. He is complaining that his neighbours are not sending men, and that
the whole gang on that field is his. He is filing a labour return.</p>
<p>This letter is not about our ridge, and we should not make it so. Shunama is Shunem, in the
Jezreel valley, some sixty kilometres north. The ridge above Ramallah lay in the land the king of
Jerusalem wrote about.</p>
<p>We quote it for a different reason. Every document in our story from here to the Ottoman registers
is written by somebody counting other people: a mayor, a scribe, a bishop, a tax clerk. In every one
of them, the people being counted are the same people, the ones in the field. <b>The archive names the
mayors. The corvée is everybody else, and everybody else is our ancestors.</b></p>
<p>Three thousand years later a qāḍī, a judge of the Islamic court, in Jerusalem will write down six
men from the village of Ramallah who have promised to plough a hill, and he will name all six. That is
the whole difference between the two ends of our story. It is not who was working, but whether anyone
wrote down their names.</p>
<p><b>What we still don’t know.</b> We don’t know when the terraces around our town were first built,
and no one has yet dated them. We don’t know what the great tower at Jericho was for.
The layer in the Shuqba cave that held the Neanderthal tooth still has no direct date, and what the
tooth was found with is still argued. Scholars also still argue over how settled the Natufians really
were. If you know of work that answers any of these, we would like to hear from you.</p>"""),

CH(3)

sect('What the ground says', 'Who else was on this coast and this plateau — and what became of every one of them')
ent('about 1200 → 1000 BCE', 'attested', False,
    'The highlands fill up',
 f'''Around 1200 BC the Late Bronze order of city-states came apart, and the whole region reorganised itself. In the two centuries that followed, the central hill country went from roughly <b>twenty-five settlements to roughly two hundred and fifty</b>, and from a scatter of people to something near forty-five thousand. The new villages were small, unwalled and farming, founded on hilltops nobody had bothered with before{c('The figures are from the archaeological surveys of the central hill country, summarised in Israel Finkelstein, <i>The Archaeology of the Israelite Settlement</i> (Jerusalem: Israel Exploration Society, 1988), and revisited in Finkelstein &amp; Neil Asher Silberman, <i>The Bible Unearthed</i> (New York: Free Press, 2001). For the population estimate and the ethnogenesis models, Ann E. Killebrew, <i>Biblical Peoples and Ethnicity</i> (Atlanta: SBL, 2005). <b>These are survey counts, not excavation counts</b> — the great majority of the 250 sites have been walked and sherded, not dug.')}. Nothing like it happened on the coast, in the Jordan valley, or anywhere a migration would have had to come from.''',
 f"""
{fig(F4.fig_highland_fill(), 'The highlands fill up, and nowhere else empties out',
 'One dot for every settlement the surveys found. <b>The jump is real and it is local.</b> A tenfold increase in two centuries is a great deal of people — but they appear in the hills without appearing to leave anywhere else, and they arrive carrying the same cooking pots as the country they are already in.',
 'Finkelstein (1988); Finkelstein &amp; Silberman (2001) (Israeli authors; cited for context); Killebrew (2005).')}
<p>The surveys fail to find three things, and each one tells us something. They find <b>no layer of
destruction</b>: the highland villages are new foundations on empty ground, not burnt towns taken
over. They find no new pottery tradition: the cooking pots carry on the local Late Bronze styles, and
people arriving from outside bring their own kitchen. And they find no matching emptying-out
elsewhere. If these tens of thousands had walked in from the coast or the valley, the coast and the
valley would show it, and they do not{c('On the absence of a destruction horizon and the continuity of the ceramic repertoire, William G. Dever, <i>Who Were the Early Israelites and Where Did They Come From?</i> (Grand Rapids: Eerdmans, 2003); Avraham Faust, <i>Israel’s Ethnogenesis</i> (London: Equinox, 2006), which argues for a distinct highland identity forming <i>in situ</i> rather than arriving; and Killebrew (2005) for the multi-origin model — local Canaanites, sedentarising pastoralists, and marginal groups the Egyptian records call <i>ʿapiru</i> and <i>Shasu</i>.')}.</p>
<p>So where did they come from? <b>From the country itself.</b> The evidence points to a people
forming in place: highland farmers already there, herders settling down, and people moving up off the
failing lowland city-states as the Late Bronze order came apart. There was no single origin. It was
the ordinary churn of a region reorganising itself after a collapse, and every strand of it was
already local.</p>
{fig(F4.fig_iron_ridge(), 'The ridge in the Iron Age, and the gap in the middle',
 'Every excavated Iron Age site within a morning’s walk. <b>Khirbet Raddana lies on the edge of Ramallah and al-Bīra</b>, about 800 metres north of al-Manāra (its excavators placed it “in Bireh”) — a village of the twelfth and eleventh centuries BC, on Ramallah’s doorstep, excavated over four salvage seasons between 1969 and 1974 and since built over by the town’s own growth. The dashed ring is Ramallah, which is not there yet and will not be for two and a half thousand years.',
 'Callaway and Cooley at Khirbet Raddana and et-Tell; Badè at Tell en-Naṣbeh; al-Houdalieh &amp; Sauders (2009) on what urban growth has since done to these sites.')}
<p>Then comes the name. The word <i>Israel</i> first appears in 1208 BC, on a victory stele, a carved
stone slab, of the pharaoh Merneptah. <b>It is written with the Egyptian sign for a people, not for a
city or a land</b>{c('The Merneptah stele, Cairo Museum JE 31408, from Thebes, year 5 of Merneptah, c. 1208 BC. In the closing lines Israel is the only entity of the group written with the determinative for a people rather than a foreign land — <i>a group of people, located somewhere in Canaan, without a territory of its own attached to the name.</i> Every other place in the passage — Ashkelon, Gezer, Yanoam — takes the city or land determinative.')}. Egyptian writing adds such a sign, called a determinative, to show what
kind of thing a word names. So the earliest outside witness describes Israel as a people in Canaan,
with no territory attached to its name: a group of people living in this country, among the people of
this country.</p>
<p>That is our whole story in one paragraph. The population on this ridge is continuous: Canaanite,
then Israelite and Judaean, then Hellenised (Greek in language and ways), then Christian by
conversion, then in large part Muslim by conversion, then Palestinian. <b>These are names taken by a
people, not peoples replacing one another.</b> Our family is inside that continuity, and so is everyone
else who ever farmed these terraces. Nobody on this ridge is a newcomer, and nobody on it is the only
one who was here.</p>"""),

ent('the names on the ground', 'documents', False,
    'The Bible as a map of our district',
 f'''<b>Nobody found the biblical places by reading the Bible.</b> They were found by walking into Palestinian villages and asking the people who lived there what they called home. The answers turned out to be the ancient names, carried in Arabic by farming families for three thousand years{c('Edward Robinson and Eli Smith travelled Palestine in 1838 and published <i>Biblical Researches in Palestine, Mount Sinai and Arabia Petraea</i> in 1841. Robinson’s method was to record the Arabic name in local speech and test it against the Hebrew or Greek form. Rana Issa describes it as “phonology as a kind of anthropological archaeology,” drawing its information “from the lips of the natives.” '+D('1841_Robinson_Biblical_Researches_v2.pdf')+'.')}. ʿAin Shams is Beth Shemesh. ʿĀqir is Ekron. Beitin is Bethel. Seilūn is Shiloh. Mukhmās is Michmash.''',
 f"""
{fig(F4.fig_bible_ridge(), 'Every biblical place within a day’s walk, and the village it survived as',
 'The right-hand grade is for <b>the identification</b>, not for the scripture — whether the ground has confirmed the name, merely agrees with it, or is still argued. <b>Nine places, and the furthest is nineteen kilometres from Ramallah.</b> Ramallah is not among them, because Ramallah is not there yet; but al-Bīra next door may be Beeroth, and the ground the town would be built on lay in the middle of all of it.',
 'Robinson &amp; Smith (1841); Pritchard at al-Jib (1956–59); Badè at Tell en-Naṣbeh; Albright and Kelso at Beitin; Marquet-Krause, Callaway and Hani Nur el-Din at et-Tell.')}
<p>At one of these places the ground answered in writing. At al-Jib, six kilometres from Ramallah,
James Pritchard dug between 1956 and 1959. He found <b>more than sixty jar handles inscribed
<span class="he">גבען</span>, Gibeon</b>, in Hebrew script of the eighth and seventh
centuries BC{c('James B. Pritchard, <i>Hebrew Inscriptions and Stamps from Gibeon</i> (Philadelphia: University Museum, 1959), and <i>Gibeon: Where the Sun Stood Still</i> (Princeton, 1962). The handles carry the formula <i>gbʿn gdr</i> followed by a personal name. It has been called as strong a site identification as anyone is ever likely to find in biblical archaeology — at the time, only the fourth ancient Palestinian place-name confirmed at its own site by excavated inscriptions.')}. The village had been called al-Jib for as long as anyone could remember, and the
jars in the ground agreed with the villagers.</p>
<p>One of the nine places works the other way round, and we include it just as gladly. et-Tell, five
kilometres east, is biblical Ai, and the Hebrew <i>ha-ʿAi</i> means <b>“the ruin”</b>. The
excavation found exactly that: an Early Bronze town destroyed about 2400 BC, then empty for more than
a thousand years, then a village of Iron I, the first part of the Iron Age, built quietly on the abandoned mound{c('Judith Marquet-Krause (1933–35); Joseph A. Callaway for the American Schools of Oriental Research (1964–70); Hani Nur el-Din, al-Quds University (2005–07). John Garstang trenched the site in 1928. The absence of a Late Bronze town at et-Tell is long-established and much discussed; what is not in doubt is the sequence — Early Bronze town, long abandonment, Iron I village.')}. The name and
the ground say the same thing. Whoever named that hill knew what was on it.</p>
<p>What does this mean for a family from Ramallah? The landscape of scripture is not somewhere else.
It is the ground between al-Bireh and Ṭaybeh. <b>Its names were kept by the people who farmed those
hills and went on saying the words</b>, not in a library, not by a church, not by a state. When we say
the people of this ridge were never replaced, the map of the Bible is one of the proofs. A replaced
people forgets the names.</p>"""),

ent('about 1175–840 BCE', 'attested', False, 'The neighbours, near and across the Jordan',
 'While the highland villages went on terracing the same slopes, the coast and the plateau filled up with peoples whose names are still in the language. The Philistines lived at Gaza, Ashkelon and Ashdod, the Phoenicians at Tyre and Sidon, and the Arameans inland at Damascus. Across the river were Moab, Ammon and Edom. <b>Every one of them was in time absorbed into the people of this region, and not one of them replaced it.</b>',
 f"""
<p>One of these neighbours matters directly to our family. The plateau our tradition names as its
road out, Karak and Shawbak, is ancient Moab and ancient Edom. <b>Karak itself is generally identified
with the Kir of Moab of the Hebrew Bible.</b></p>
<p>And Moab left a document. The Mesha Stele, a stone cut about 840 BC and found at Dhībān in 1868,
is the longest Iron Age inscription anyone has recovered from this landscape. It is written in
Moabite, a language so close to Hebrew that it can be read straight off the stone.</p>
<p>It can also be checked against scripture, because both sides wrote the war down. The stele is King
Mesha’s account of throwing off Israelite overlordship. <b>2 Kings 3 is the same war from the other
side</b>, and names the same king: <i>“Mesha king of Moab was a sheep-master”</i>{c('2 Kings 3:4–27, and the Mesha Stele (the Moabite Stone), Louvre AO 5066, found at Dhībān in 1868. The stele names <span class="he">מלך ישראל</span> — the king of Israel — and the god <span class="he">יהוה</span>, the earliest occurrence of the divine name in an inscription outside the Bible. The two accounts agree on the participants and the shape of the conflict and disagree, as one would expect, about who won.')}. So we have
two accounts of one campaign, one on stone and one in scripture, each of them the enemy’s version of
the other. The plateau our family remembers as a place of exile has been literate, settled and writing
about itself for nearly three thousand years.</p>
<p>One neighbour is the clearest example of all. The Philistines arrived about 1175 BC carrying a
southern-European-related ancestry whose source population is not yet pinned down, and the arrival is
visible in the ancient DNA at Ashkelon. Then, within no more than two centuries, the signal is gone.
They did not leave. They married their neighbours. <b>That is what happens in this country to
everybody who comes</b>, and it is what happened to our family too, three thousand years later.</p>""" + fig(R.fig_peoples(),
 'The peoples of this land do not replace one another — they overlap',
 'Each band is a language and an identity, not a population. They run into and over one another for four thousand years, and the genetics now say the population underneath them is largely continuous. <b>Only the Samaritans kept a separate identity to the present; only the Franks genuinely left.</b> The gold line is 1562, the year the family arrives on the ridge — into a landscape that has been continuously inhabited since long before the first band on this chart.',
 'Haber et al. (2017, 2019); Feldman et al. (2019); Agranat-Tamir et al. (2020) (Israeli authors; cited for context); Killebrew (2005); the Amarna correspondence; Samaritan census figures.')),

CH(4)

sect('What the ground says', 'Assyria, and the road that already joined the two ends of this story')
ent('745–681 BCE', 'documents', False, 'Assyria writes the land down',
 f"""From <b>Tiglath-pileser III (745–727)</b> onward, the Assyrian empire recorded this country in cuneiform, the wedge-shaped writing of Mesopotamia. It left tribute lists, provincial reorganisations and deportations, and Sennacherib’s siege of Lachish carved in relief for the walls of Nineveh{c('The Assyrian royal inscriptions of Tiglath-pileser III, Sargon II and Sennacherib; the Lachish reliefs from Sennacherib’s palace at Nineveh, now in the British Museum. Standard editions in the <i>Royal Inscriptions of the Neo-Assyrian Period</i> series.')}. What matters here is not who paid whom. From the eighth century BC onward, outside powers documented this landscape continuously, and in none of their documents is it ever empty.""",
 f"""
<p>At the other end of our family’s story, <b>the incense road was already running</b> in these
centuries. Pliny, writing much later, in the first century AD, describes it in detail. The frankincense of South Arabia was gathered at Sabota,
which is Shabwa, in Ḥaḍramawt. Ḥaḍramawt is the land of Hazarmaveth, one of Joktan’s thirteen sons in
the Genesis list we met in Chapter 1. At Sabota a tenth of the incense was tithed to the god at a single gate.</p>
<p>From Sabota the incense was carried on to Thomna, capital of the Gebbanites, a neighbouring
people, and from there it went <b>1,487½ miles by camel to Gaza
on the Palestinian coast, in sixty-five stages</b>. Pliny even totals the bill. Water, fodder, lodging
and tolls came to 688 denarii (Roman silver coins) a camel, before a single Roman customs officer was
paid{c('Pliny, <i>Naturalis Historia</i> XII.63–65: the incense tithed at Sabota (Shabwa) in Ḥaḍramawt, then carried from Thomna, capital of the Gebbanitae, 1,487½ Roman miles to Gaza in sixty-five camel stages, with charges at every halt totalling 688 denarii a camel.')}.</p>
<p>This is worth stopping on. More than a thousand years before the dam of Maʾrib broke, and more than
two thousand years before Rāshid crossed the Jordan, <b>a permanent, tolled, mapped trade road already
joined the country scripture gives our family to the country our family now lives in</b>. It ended at
Gaza, some eighty kilometres south-west of the ridge. The migration our tradition remembers did not
need to invent a route. It only needed to use one that had been open, in both directions, for the
better part of a thousand years.</p>"""),

CH(5)

sect('What the ground says', 'Five empires in five centuries, and a village that does not move')
ent('539–63 BCE', 'documents', False, 'Six sovereigns over one ridge',
 'Cyrus took Babylon in 539, and the edict of return is usually dated 538. Alexander came in 332. Then came the Ptolemies, the Seleucids and the Hasmoneans, a Judaean royal house, and Pompey in 63 BC. <b>Five changes of sovereign in five centuries, and no change of population.</b> The district around Jifnā, the Roman Gophna, that Rome would inherit, and Pliny would write down, began in the Hellenistic age of the Greek kings. Rome did not invent this landscape; it took delivery of it.',
 f"""
<p>The period left ordinary paperwork, which is the best kind of evidence there is. The Zenon papyri
are the working letters of an agent of Ptolemy II’s finance minister. <b>He was travelling through
this country in 259 BC</b>, on a tour begun late in 260. His letters record estates, grain, slaves,
wine and olive oil moving through Palestinian towns, in Greek, as routine commercial
business{c('The Zenon archive (P. Cair. Zen.), 261–229 BCE; Zenon’s Palestinian journey of 259 BCE on behalf of Apollonios, dioiketes of Ptolemy II Philadelphus.')}. Nobody writes letters like that about an empty country.</p>"""),

E[-1] = E[-1][:7] + (E[-1][7] + fig(F5.fig_sovereigns(), 'Six sovereigns, one people',
 'Five changes of sovereign in five centuries, and every one of them happened above the villages rather than to them. The bands are the rulers; the green line underneath is everyone else.',
 'Reign dates as conventionally given; the Zenon archive (P. Cair. Zen.) for 259 BC.'),)
ent('5th–2nd c. BCE', 'attested', False, 'The Samaritans and Mount Gerizim',
 f"""Magen dates the sanctuary on Gerizim, from its remains, to the <b>mid-fifth century BC</b>, and that date is disputed. When the Samaritans finally parted from Judaism is disputed too. The decisive break is usually placed at the Hasmonean destruction of their temple there, about 110 BC{c('Y. Magen (Israeli author; cited for context), <i>Mount Gerizim Excavations</i> I–II (Israel Antiquities Authority, 2004, 2008), for the mid-fifth-century sanctuary — excavated and published by the Staff Officer of Archaeology under the Civil Administration, on a mountain in occupied territory, and cited here for its stratigraphy and not for its frame (see the bibliography, §XXX). The Persian-period date is disputed; Gary Knoppers, <i>Jews and Samaritans: The Origins and History of Their Early Relations</i> (Oxford, 2013), ch. 1, for the range of dates proposed — from Ezra to 70 CE; Josephus, <i>Antiquitates</i> XIII.255–56, for John Hyrcanus and the destruction of the Gerizim temple. <b>Earlier editions of this book printed a flat “c. 400 BCE,” which no source supports.</b>')}. What follows is not disputed. The Samaritans are still on that mountain. From a population in the hundreds of thousands in the Byzantine era, they fell to about 150 people by 1900, and they have grown again to some 900 today{c('On Samaritan demographic history: the Byzantine-era revolts of 484, 529 and 555 and the collapse that followed; census counts of 163 (1922) and 182 (1931); c. 900 today at Holon and Kiryat Luza.')}. Here continuity is something you can see, not just argue. And the Gospel sets a conversation in sight of that same mountain: <i>“our fathers worshipped in this mountain, and ye say that in Jerusalem is the place where men ought to worship”</i>{c('John 4:20, the Samaritan woman at the well near Sychar; the well itself is at Bālāṭa outside Nablus, at the foot of Gerizim, and the mountain in the verse is the one this entry is about. <b>The dispute the verse records is the one the archaeology dates.</b>')}.""",
 ),

CH(6)
sect('What the ground says', 'Rome paves the ridge, ranks the district, and writes its villages down')
ent('63 BCE → 77 CE', 'documents', False, 'Rome writes the district down',
 f"""Pompey took Judaea from the Hasmoneans in 63 BC, and a century and a half later the empire had the place on paper. Pliny lists Gophna, which is Jifnā, about seven kilometres due north of our ridge, among the ten toparchies, or districts, of Judaea. Josephus calls it <b>“the second of those cities”</b> after Jerusalem itself{c('Pliny, <i>Naturalis Historia</i> V.70; Josephus, <i>Bellum Judaicum</i> III.54–55; also IV.551 (Vespasian takes the toparchy, 68 CE), V.50 and VI.115.')}.""",
 f"""
{fig(ATLAS.fig_roman(),'The district when Rome wrote it down',
 'Ramallah’s neighbours in the Roman and Byzantine record, with the imperial road that runs the length of this ridge. Every green dot is named in a surviving text. The gold circle is the site of Ramallah — named in none of them, and in none at all until 1186.',
 'Pliny, NH V.70; Josephus, BJ III.54–55; Eusebius, Onomasticon; the Madaba mosaic; Tappy, NEA 75 (2012); al-Houdalieh on Khirbet et-Tireh.')}
<p>The hills our family would one day reach were not a wilderness. They were an imperial district with
a paved highway down the middle. This was the road from Aelia Capitolina, as Rome called Jerusalem, to
Neapolis, today’s Nablus, milestoned and measured.</p>
<p>Eusebius later used this road as his surveyor’s baseline. Bethel, he writes, is <i>“twelve miles
from Jerusalem, to the right of the road going to Neapolis.”</i>{c('Eusebius, <i>Onomasticon</i>, s.vv. Baithel, Silo; ed. Klostermann (1904); Notley &amp; Safrai (Brill, 2005). The road’s milestones catalogued by Thomsen, <i>ZDPV</i> 40 (1917).')} <b>When our family walks up
this ridge in 1562, and when the first emigrants ride down it in 1901, they are using a road Rome
paved.</b></p>
<p>Two kilometres from the future town centre lies Khirbet et-Tireh (a khirbet is a ruined site). It
has two churches, a monastery and an oil press, excavated by Salah al-Houdalieh, and it shows the
ground itself was worked and prayed on for some seven hundred years, from the Roman period
onward{c('Salah al-Houdalieh (al-Quds University), excavations at Khirbet et-Tireh from 2013 — two contemporaneous churches, a monastery and an oil press, two kilometres west of the present town centre; the settlement covers some thirty thousand square metres. Hamdan Taha at ʿAbūd. See the bibliography, §XVIII and §XXIX. <b>Two corrections here. Earlier editions said “a thousand years before the founding,” which implied an unbroken occupation the excavation does not show. And earlier editions said the site was abandoned after the earthquake of 749 and reoccupied only in the Ottoman period — al-Houdalieh’s own publication of the press says the opposite: “we believe that the press facility itself was maintained in continuous use from the Byzantine through the late Ottoman periods.” The 749 abandonment is withdrawn.</b> Salah Hussein al-Houdalieh, “The Oil Press Complex of Khirbat al-Tira,” <i>Jerusalem Quarterly</i> 62 (2015), 84–96.')}. Only the name Ramallah is missing from every text. The neighbours are Roman, the
ground is Byzantine, and the name will come with the Crusader records, in 1186.</p>"""),

ent('about 30 CE', 'documents', False, '“A city called Ephraim”',
 f"""John 11:54: “A city called Ephraim, and there continued with his disciples.” The city is generally identified with <b>Ṭaybeh, eleven kilometres from Ramallah</b>{c('John 11:54: <span class="gk">εἰς Ἐφραὶμ λεγομένην πόλιν</span>. The identification with eṭ-Ṭaybeh is standard from Robinson (1841) and the <i>Survey of Western Palestine</i>, resting on Eusebius and the villagers’ retained memory of the older name; Albright preferred ʿAyn Sāmiya.')}.""",
 f"""
<blockquote><span class="gk">Εφρων ἡ Εφραια ἔνθα ἦλθεν ὁ Κ(ύριο)ς</span><br>
“Ephron, also Ephraia, <b>where the Lord went.</b>”
<span class="cite">The Madaba mosaic map, sixth century — the caption still in the church floor at
Madaba{c('Avi-Yonah, <i>The Madaba Mosaic Map</i> (1954), no. 41; Donner no. 43; Piccirillo no. 44.')}</span></blockquote>
<p>And the road Jesus used is this road. In the Josephus passage quoted above, <b>the Galileans
going up to the festivals take their journeys through the country of the Samaritans</b>{c('Josephus, <i>Antiquitates</i> XX.118; cf. <i>BJ</i> II.232. The Gospels assume both routes: Luke 9:51–53 and John 4:3–5 the ridge, Mark 10:1 the Jordan valley.')}. That is the ridge route, past the site of Ramallah.</p>
<p>In 451, at the Council of Chalcedon, Jerusalem became a Patriarchate, the seat of one of the
church’s senior bishops. The church our family belongs to took the form it still
has{c('The see of Jerusalem elevated to patriarchal rank at the Council of Chalcedon, 451; on the continuity of its structures through the early Islamic period, Milka Levy-Rubin, <i>ARAM</i> 15 (2003).')}.</p>
<p><b>Our family’s faith did not arrive with us in 1562.</b> It was already here, and it is one of the
things that never left.</p>"""),

ent('about 27–30 CE', 'scripture', False, 'The roads Jesus used',
 f'''The Gospels are not set <i>near</i> our district. <b>They are set in it.</b> Put every place they name at its real position, and the whole of it fits inside a day’s walk of the hill Ramallah would be founded on fifteen centuries later. Jerusalem is fourteen kilometres away, Bethany fifteen, Jericho twenty-three, and Ephraim eleven{c('Distances are great-circle measurements from the centre of present-day Ramallah (31.8996° N, 35.2042° E) to the accepted site of each place. Every distance printed on a plate in this book is now computed from that point and the site’s own plotted coordinates, so a label cannot drift away from the dot it belongs to. <b>Earlier editions printed eṭ-Ṭaybeh at twelve kilometres throughout; the measurement is 10.7, and the book now prints eleven.</b>')}.''',
 f"""
{fig(F4.fig_jesus_road(), 'The roads he used, and the ridge they run along',
 'Left, the country: the two roads between Galilee and Jerusalem, and where this ridge sits on one of them. Centre, the district within a day’s walk. Right, what the Gospels say is at each place. <b>Every marker is graded on the identification of the site, never on the verse.</b> Green is named in the Gospels at a securely identified place; grey is named in the Roman record but not in the Gospels; the dashed violet rings are medieval pilgrim tradition, printed and labelled as tradition.',
 'John 11:54; Luke 2:41–46, 10:30, 19:1, 24:13; Josephus, Ant. XX.118 and BJ IV.550–51, VI.113–15; Robinson &amp; Smith (1841); Pringle, Churches of the Crusader Kingdom.')}
<p><b>Start with the road, because the road is the part that is certain.</b> There were two ways from
Galilee to Jerusalem: down the Jordan valley and up through Jericho, or straight down the watershed,
the high spine of the hills, through Samaria.</p>
<p>Josephus says plainly which one Galilean pilgrims used: <i>“It was the custom of the Galileans,
when they came to the holy city at the festivals, to take their journeys through the country of the
Samaritans”</i>{c('Josephus, <i>Antiquitates</i> XX.118; the same episode at <i>BJ</i> II.232. The Gospels assume both routes are available: Luke 9:51–53 and John 4:3–5 take the ridge, Mark 10:1 the valley.')}. The watershed road runs along the top of our ridge, within sight of the
future town, and Rome later paved it and set milestones along it{c('Eusebius uses the Jerusalem–Neapolis road as his surveyor’s baseline in the <i>Onomasticon</i>, locating Bethel “twelve miles from Jerusalem, to the right of the road going to Neapolis”; the milestones were catalogued by Thomsen, <i>ZDPV</i> 40 (1917).')}.</p>
<p><b>Three times a year, at Passover, Pentecost and Tabernacles, the pilgrims of Galilee came down
past this hill.</b> That is not a claim of faith. It rests on a road, a custom recorded by a
witness of the time, and a count of milestones.</p>
<p>Now to the one town on this ridge the Gospels actually name. John says that when it became unsafe
for Jesus near Jerusalem he <i>“went thence unto a country near to the wilderness, into a city called Ephraim,
and there continued with his disciples”</i>{c('John 11:54 (King James Version): <span class="gk">εἰς Ἐφραὶμ λεγομένην πόλιν</span>. The identification with eṭ-Ṭaybeh is standard from Robinson (1841) and the <i>Survey of Western Palestine</i>, and is supported by the sixth-century Madaba mosaic, which captions the place <span class="gk">Εφρων ἡ Εφραια ἔνθα ἦλθεν ὁ Κ(ύριο)ς</span> — “Ephron, also Ephraia, where the Lord went.”')}.</p>
<p>Ephraim is generally taken to be today’s Ṭaybeh. Look at where it sits on the map. It is on the last inhabited edge of the ridge, and east of
it the land falls away into the wilderness of the Jordan rift. <b>The verse describes this place
accurately</b>: a town at the end of the settled country, with the desert starting at its feet, which
is exactly what a man withdrawing from Jerusalem would want. And it is still, today, the last entirely
Christian town in Palestine.</p>
<p>Two more places on this map belong to the beliefs of the neighbours rather than to the evidence,
and we mark them that way. At <b>al-Bireh</b>, one and a half kilometres from the centre of Ramallah,
there is a Crusader church. It is in the record by 1128, and the German pilgrim Theodoric described it
in 1172. By the fourteenth century the Latins held that this was the day’s-journey halt of Luke 2:44,
where Mary and Joseph discovered the boy was not with the company{c('On the church of St Mary at al-Bīra: in the record from September 1128 under the jurisdiction of the Holy Sepulchre, and described by Theodoric in 1172; a Romanesque basilica of roughly 22 × 35 metres. The Holy Family association is attested from the fourteenth century. See Denys Pringle, <i>The Churches of the Crusader Kingdom of Jerusalem</i>, s.v. al-Bīra; and the Palestinian Ministry of Tourism and Antiquities site record. <b>The identification of al-Bīra with the Beeroth of Joshua 9:17 is Robinson’s and remains disputed; the Holy Family association is later still, and rests on nothing earlier than the Crusader period.</b>')}.</p>
<p>At <b>al-Qubeiba</b>, nine kilometres to the south-west, there is a Crusader village and a fort
called <i>Castellum Emmaus</i>. Pilgrims began calling it the Emmaus of Luke 24:13 in the thirteenth
century, and the Franciscans adopted it in 1335{c('Al-Qubeiba is one of four candidates for Emmaus, with ʿImwās/Nicopolis, Abū Ghōsh and Moẓa/Qālūniya. The choice turns partly on a manuscript split at Luke 24:13 — sixty stadia in most witnesses, a hundred and sixty in Sinaiticus and others — which suits Nicopolis at roughly 160 stadia and al-Qubeiba at about 65. Franciscan pilgrimage from 1335; excavated by Bellarmino Bagatti, 1940–44.')}.</p>
<p>Neither place is evidence about the first century. What they show is worth saying: <b>for eight
hundred years the people living beside this ridge have believed the Gospel happened at their own
door.</b> That belief is itself a dated, documented, physical fact, with a church and foundations. We
mark the two places violet and dashed on the map, and leave the reader to weigh them.</p>"""),

ent('about 30 CE', 'documents', False, 'Life on the ridge in AD 30',
 f'''A tax district, a highway and a harvest. <b>The people on these hills in the year of the Gospels were villagers of the Gophna toparchy</b>, one of the ten districts of Judaea, with its capital at Jifnā, about seven kilometres from the future town{c('Pliny, <i>Naturalis Historia</i> V.70, listing Gophna among the ten toparchies of Judaea; Josephus, <i>BJ</i> III.54–55, where Gophna heads the list after Jerusalem. The toparchy is Hellenistic in origin and was inherited, not invented, by Rome.')}. They grew olives and vines on terraces their grandparents had built, pressed oil, and paid it to Rome.''',
 f"""
<p><b>We cannot name one person who stood on Ramallah’s own hill in AD 30.</b> There is no Ramallah
yet. The excavations at Khirbet et-Tireh, two kilometres away, show the ground was worked and prayed on
from the Roman period onward, but no text names a soul on it{c('Salah al-Houdalieh’s excavations at Khirbet et-Tireh, from 2013: two contemporaneous churches, a monastery and an oil press, in use from the Roman period onward; al-Houdalieh’s publication of the press finds it in continuous use into the late Ottoman period, so the earlier claim of abandonment after the earthquake of 749 is withdrawn (see the note on the excavation above). The Roman-period phase is the relevant one here; the churches are later.')}.</p>
<p>What we can name is everything around a person: the district, the road, the crop, the press and the
tax. That is more than most families can say about their ground in any century, let alone the
first.</p>
<p>The terraces are the strongest single piece of it. They are the same system we described in Chapter
1: dry-stone walls with no mortar of any kind, built to hold soil and water on a slope, and worked
for so long that no one can date their beginning{c('On the dry-stone technique and its continuity: Shadi Ghadban, “Palestinian Dry Stone Structures — An Endogenous Expression of Cultural Landscape,” <i>Journal “Sustainable Development, Culture, Traditions”</i> 1b (2015), 34–46.')}.</p>
<p>The terraces on the hills Jesus walked through are the terraces our family would one day farm.
Nobody rebuilt this landscape between the two dates. <b>It was kept up, wall by wall, by whoever was
living on it.</b></p>
<p>The road was busy, and dangerous. Josephus records Galilean pilgrims attacked at the Samaritan
village of Ginae on their way up to a festival (one man killed in his first telling, many in his second), and the reprisals and Roman hearings that
followed{c('Josephus, <i>Antiquitates</i> XX.118–136; <i>BJ</i> II.232–246. Under the procurator Cumanus, c. 51 CE. The affair reached the emperor Claudius.')}. The episode only makes sense if the ridge route carried heavy, regular, mixed
traffic. <b>Whoever was farming this ridge in the first century was living on the main road</b>,
watching the whole country walk past their terraces three times a year.</p>"""),

ent('69 → 70 CE', 'documents', False, 'Rome returns, AD 69–70',
 f'''When Rome came back to settle the revolt, it came up this road, and Josephus names the stops. Vespasian <i>“went up to the mountainous country, and took those two toparchies that were called the Gophnitick and Acrabattene”</i>. Then Josephus goes on: <b><i>“after which he took Bethel and Ephraim, two small cities; and when he had put garrisons into them, he rode as far as Jerusalem.”</i></b>{c('Josephus, <i>BJ</i> IV.550–551 (Whiston IV.9.9), the campaign of AD 69. Bethel is Beitin, 4.4 km from Ramallah; Ephraim is eṭ-Ṭaybeh, 11 km in a straight line from al-Manāra square. The same march has Cerealis sent against upper Idumaea, where he stormed and burned Hebron.')} Acrabattene was the district around ʿAqraba, south-east of Nablus.''',
 f"""
<p>Read those two names together. Bethel is the town of Jacob’s ladder, and Ephraim is the town John
says Jesus withdrew to. <b>They lie four kilometres and eleven kilometres from the centre of today’s
Ramallah</b>, and they are the two places the Roman army thought worth garrisoning on its way to
besiege Jerusalem. The Gospel map of this ridge and the Roman army’s map are the same map: the same
small towns, on the same road, forty years apart.</p>
<p>Then the district is used one more time, in the most human detail in this chapter. During the
siege, Titus took the surrender of a group of Jerusalem’s notables, among them the high priests
<b>Joseph and Jesus</b>, and the sons of leading families. He <i>“sent them to Gophna, and desired
them to remain there for the present,”</i> promising that when the war was over he would restore every
man his property.</p>
<p>The rebels inside the city then put about that the Romans had butchered them, to stop anyone else
deserting. So Titus <b>brought the same men back from Gophna</b> and walked them round the walls with
Josephus, alive, where the defenders could see them{c('Josephus, <i>BJ</i> VI.113–115 (Whiston VI.2.2). Gophna is Jifnā, about 7 km in a straight line from al-Manāra square, the centre of Ramallah.')}.</p>
<p>So in the summer of AD 70, the surrendered priesthood of Jerusalem was being housed in a village about seven
kilometres from a hilltop that had no name yet. <b>After the life of Jesus, this ridge was
the last stage of the road to Jerusalem, and then the place Jerusalem’s survivors were put.</b></p>
<p>And then, as we read the evidence, nothing happened to the population. The villages of the Gophna toparchy were not destroyed
and not emptied. The terraces were not abandoned, and the same names went on being used. Within three
centuries these hills were Christian, and in the next chapter we show it happened <b>by conversion, not by
replacement</b>. The people who watched the pilgrims pass in AD 30, and the legions pass in AD 69, are
the people who were still on this ridge when sixty-three Christian households and eight single men walked up it in 1562.</p>
<p><b>What we still don’t know.</b> We cannot yet name anyone who lived on Ramallah’s own hill in
these centuries, because no text names a soul there. The date of the first sanctuary on Mount
Gerizim is still disputed, and so is when the Samaritans finally parted from Judaism. If you know of a
record that speaks to any of these, we would like to hear from you.</p>"""),

CH(6)

sect('And in our own line', 'The name enters at a spring in Yemen — four thousand miles from this ridge')
ent('about 250 → about 350', 'documents', False, 'Ghassān named in stone',
 'In the third and fourth centuries AD, the kingdoms of Yemen were sending envoys and armies north across Arabia. Our family’s story hangs on one word from that world: Ghassān. For a long time we knew that word only from the Arabic genealogists, the scholars of family descent, who wrote five hundred years after the fact. But <b>Ghassān is named twice in South Arabian inscriptions</b>, cut into stone while the Jafnids, the ruling house later tied to Ghassān, were still unheard of{}.'.format(c('<b>ʿInān 75</b>, mid-third century AD, recording an embassy to “the kings of the peoples (<span class="ar">أشعب</span>) of Ghassān, al-Asd, Nizār and Madhḥij”; <b>ʿAbadān 1</b>, roughly a century later, on a Ḥimyarite campaign “between the land of Nizār and the land of Ghassān.” Both in the Sabaic corpus; see the DASI database (Università di Pisa / CNR) and the discussion in Christian Julien Robin’s work on the Arab peoples of the pre-Islamic peninsula.')),
 f"""
<p>Both inscriptions are in Sabaic, the old written language of Yemen. The first, <b>ʿInān 75</b>,
comes from the middle of the third century AD. It records a Sabaean embassy sent to
<i>“the kings of the peoples of Ghassān, al-Asd, Nizār and Madhḥij.”</i></p>
<p>The second, ʿAbadān 1, is about a century later. It has a Ḥimyarite army campaigning
<i>“between the land of Nizār and the land of Ghassān.”</i></p>
<p>In both, Ghassān is a <i>shaʿb</i>: a large territorial grouping with kings of its own. In both
it is placed in <b>western Arabia</b>, out of Yemen and on the road north.</p>
<p>This is one of the most useful things we have found about the name. It does not prove any
family’s descent, and it never could. What it shows is that <b>“Ghassān” was a real, sizeable,
politically organised people</b>, named by outsiders, on stone, before any Arabic genealogist wrote
a word about it. The tradition our family inherited is not describing a literary invention. It is
describing something that existed.</p>
<p>The old scholars did not agree about the name itself. The classical authorities all say Ghassān
is a water rather than a man. Then they give <b>four locations for it that cannot all be true</b>:
between Rimaʿ and Zabīd in the Yemeni Tihāma, the coastal plain (Ibn al-Kalbī, the oldest and
best-supported); at the Maʾrib dam itself (Ibn Hishām); at al-Mushallal near al-Juḥfa, on the
Mecca–Medina road; and one report that it is not a place at all but an animal that fell into a
water{c('Yāqūt al-Ḥamawī, <i>Muʿjam al-buldān</i>, s.v. <span class="ar">غسان</span>, who assembles the variants: Ibn al-Kalbī via Ibn Ḥabīb and Naṣr al-Iskandarī for Rimaʿ/Zabīd; Ibn Hishām (d. 218/833) for the dam at Maʾrib; an anonymous <i>wa-yuqāl</i> for al-Mushallal near al-Juḥfa; and a <i>wa-qīla</i> that the water was named after an animal that fell into it. The three geographical variants are hundreds of kilometres apart and mutually exclusive; none of the authorities had independent evidence.')}.</p>
<p>They also disagreed about who had the right to the name. Yāqūt includes the Anṣār of Medina.
Ibn Ḥazm expressly excludes them and admits only four sons of ʿAmr Muzayqiyāʾ. Al-Samʿānī rules out
Khuzāʿa, Aslam, Bāriq and the Azd of Oman on the ground that they did not drink from the water called Ghassān{c('Yāqūt, s.v. <span class="ar">غسان</span>, for the Banū Māzin b. al-Azd “who are the Anṣār,” with Banū Jafna and Khuzāʿa; Ibn Ḥazm, <i>Jamharat ansāb al-ʿArab</i>, admitting only al-Ḥārith, Jafna, Mālik and Kaʿb, the four sons of ʿAmr Muzayqiyāʾ, and excluding the Anṣār; al-Samʿānī, <i>al-Ansāb</i>, s.v. al-Ghassānī, following Ibn al-Kalbī in excluding Khuzāʿa, Aslam, Bāriq and Azd ʿUmān.')}.
Even the medieval genealogists could not agree on who could be called Ghassānī.</p>
<div class="fix"><div class="fixhead">A trap we will not fall into</div>
<div style="font-size:.95rem;line-height:1.65;color:#46423B">
<p style="max-width:none"><b>The written form <span class="ar">الغساني</span> is not, by itself,
evidence of Ghassanid descent — and it was not in the classical period either.</b> Al-Samʿānī’s own
entry on the nisba, the part of a name that says where or whom you come from, contains three separate traps on the same pages: <b><span class="ar">الغُساني</span></b>
with a <i>ḍamma</i>, the short “u” vowel, is a different nisba altogether, to a clan of Ḥaḍramawt; <b>al-Ghassāniyya</b> is
a theological sect of Kufa, of the Murjiʾa, who left judgement of sinners to God, named after some man called Ghassān; and at least one famous
bearer, Ibrāhīm ibn Ṭalḥa, is simply <i>named after a great-grandfather who happened to be called
Ghassān</i>. Unvocalised manuscripts do not distinguish any of these{c('Al-Samʿānī, <i>al-Ansāb</i>, s.v. <span class="ar">الغساني</span>: <span class="ar">الغُساني</span> with <i>ḍamma</i>, to Ghassān b. Judhām b. al-Ṣadif, a <i>baṭn</i> of Ḥaḍramawt, on the authority of al-Dāraquṭnī; al-Ghassāniyya, the Murjiʾī sect of Kufa; and Ibrāhīm b. Ṭalḥa, <span class="ar">نُسب إلى جدّه الأعلى</span>, “named after his great-grandfather.” Ibn Ḥibbān moreover calls Yaḥyā b. Yaḥyā al-Ghassānī a <i>Kindī</i>.')}.</p>
<p style="max-width:none"><i>So when our family’s oldest named ancestor is written </i>Rāshid
al-Ḥaddādīn al-Ghassānī<i>, the last word is a claim, not a proof. We have said from the
beginning that the claim is a claim.</i> <b>What the inscriptions add is that the thing being claimed
was real.</b></p></div></div>"""),

ent('about 260–280', 'documents', False,
    'A traveller lists twelve lands',
 f'''A third inscription was published in 2016. It is a dedication to Taʾlab Riyām, the god of the
tribes of Ḥashid and Ḥumlān. Its authors thank him for bringing their steward home
<i>“from the land of the North.”</i> Then they list, in order, every land the man crossed, from the
Azd to Ghassān and beyond: <b>Asd, Nizār, Tanūkh, Liḥyān, Tadmur, Nabaṭ, Rūmān, Lakhm,
Ghassān, Maʿadd, Ṭayyiʾ, Khaṣaṣat</b>{c('Riyam 2006-17, from the village of Riyām in the Yemeni highlands, published by Jérémie Schiettecatte &amp; Mounir Arbach, “The political map of Arabia and the Middle East in the third century AD revealed by a Sabaean inscription,” <i>Arabian Archaeology and Epigraphy</i> 27:2 (2016), 176–196, DOI 10.1111/aae.12071. The text is one of a group of ten dated to the first–third century AD on palaeographic grounds; the authors place this one in the third century, probably c. 260–280. Lines 15–20 carry the list of lands. '+D('2016_Schiettecatte_Arbach_Political_Map_of_Arabia_3rd_c_AAE_27.pdf')+'.')}. It is an itinerary, a record of a journey, cut into stone by
somebody who had just walked it.''',
 f"""
{fig(F4.fig_riyam_road(), 'Twelve lands, in the order he crossed them',
 'The stops are the inscription’s own, in the inscription’s own order. <b>The land of the Azd is the first; the land of Ghassān is the ninth</b>, and between them lie Palmyra, the Nabataeans, Rome and Lakhm — the whole northern client system, seen from Yemen and named in Sabaic. The two green stops are the two names the family’s tradition depends on, and in the third century AD they are not in the same place.',
 'Riyam 2006-17, lines 15–20; Schiettecatte &amp; Arbach, <i>Arabian Archaeology and Epigraphy</i> 27 (2016), 176–196.')}
<p>This stone gives our family history three things, and one caution.</p>
<p><b>First, Ghassān has a position.</b> It is not a genealogy, not an eponym (a founder a people is
named after), and not a water somewhere in the Tihāma. It is a place in a sequence of places, between
Lakhm and Maʿadd, listed by a man who had been there. The name our own chart hangs on turns out to be
a piece of third-century political geography.</p>
<p><b>Second, the Azd and Ghassān are two different stops.</b> They are stop one and stop nine, with
seven lands between them. The genealogists later drew a relation between al-Azd and Ghassān. But in
the third century a Sabaean envoy crossed one, then crossed seven other territories, and then crossed
the other.</p>
<p><b>Third, the road in this inscription is our road.</b> It runs by Palmyra, the Nabataeans, Rome
and al-Ḥīra, and the Nabataean land he names is this country. The route from Yemen to the Roman
frontier was open, known, walkable and worth carving in the third century AD. That is exactly the
period in which our family’s tradition has its ancestors taking it.</p>
<p>Now the caution. The list may not be a step-by-step route. It may be a register of lands reached
rather than an ordered march, and the editors say so. Rome, Palmyra and the Nabataeans in sequence
make geographical sense; Tanūkh in lower Mesopotamia at position three does not.</p>
<p>The date, too, comes from the shape of the letters (palaeography), not from a fixed year. What the
stone does fix is the list itself: <b>these twelve lands existed, under these names, and a Sabaean
government knew all of them.</b></p>"""),
ent('about 250–500', 'classical', 'shared', 'The name in the water',
 'As Ghassān moves north, the main tradition remembers its name as coming not from a man but from <b>a water</b>. Ibn al-Kalbī writes: <span class="ar">وإنّما غسّان ماء شربوا منه فسُمّوا به</span>, “Ghassān is simply a water they drank from, and so were named after it.” He places it between Zabīd and Rimaʿ, in the Tihāma of Yemen{}. The sources do not agree about where the water was, or whose sons drank there.'.format(c('Ibn Durayd (d. 933), <i>al-Ishtiqāq</i>, s.v. Ghassān; Ibn al-Kalbī (d. 819), <i>Jamharat al-nasab</i>, ed. Nājī Ḥasan, p. 615, read from the page on 11 November 2026: <span class="ar">وإنما غسانُ ماءٌ شربوا منه فسُمّوا به، وهو ماءٌ بين زبيد ورِمَع، وهذان واديان للأشعريين</span>. Yāqūt, quoting him at second hand, has him put the water near the Maʾrib dam and gives the Zabīd placing to Naṣr; the <i>Jamhara</i> itself settles what Ibn al-Kalbī wrote. '+D('0819_Ibn_al-Kalbi_Jamharat_al-nasab.pdf')+'.')),
 f"""
{fig(ATLAS.fig_road(),'The road, and the ground it passes',
 'Yemen to the Levant: the migration the tradition remembers, over the country the classical geographers describe. The chart’s generations 15–29 travel this map; at generation 29, with ʿAmr Muzayqiyāʾ, the name Al-Ghassānī enters — exactly where the classical sources put the naming at the spring.',
 'al-Hamdānī, Ṣifat Jazīrat al-ʿArab; Ibn al-Kalbī; al-Masʿūdī; the chart, generations 15–29.')}
<p>Both of our family’s key texts carry this stretch of the story. The chart names the
generations, and Shāhīn tells the migration. The classical scholars supply the larger system it
fits into{c('The Azdī pedigree (al-Azd → Māzin → … → ʿAmr Muzayqiyāʾ → Jafna) in al-Suwaydī, <i>Sabāʾik al-dhahab</i>, tabulated by Wüstenfeld (1852–53); the identification Joktan = Qaḥṭān stated by al-Ṭabarī c. 915 — a harmonisation with Genesis 10, made a thousand years before this family repeated it. <b>It is not the load-bearing joint of Qaḥṭānī genealogy</b> — the Arabic tradition runs Qaḥṭān through Yaʿrub and Hūd without needing Joktan at all — so removing it costs the chart nothing.')}.</p>
<p>Those scholars did not agree on where Ghassān’s edges lay. Three of the tradition’s greatest
authorities draw the boundary in three different places: Ibn al-Kalbī wide, Ibn Ḥazm narrow, Ibn
Durayd narrower still. Ibn Khaldūn, the sharpest critic the tradition ever produced, warns that the
memory of a common ancestor beyond a few generations is an assertion, not a knowledge{c('Ibn Ḥazm, <i>Jamharat ansāb al-ʿArab</i>, at only the four sons of ʿAmr Muzayqiyāʾ who drank; Ibn Khaldūn, <i>Muqaddimah</i>, Book One, ch. 2 — naming this branch. '+D('1064_Ibn_Hazm_Jamharat_ansab_al-Arab.pdf')+'.')}.</p>
<p>This changes the kind of claim more than it weakens it. <b>Ghassanid identity was never a
bloodline out of one man.</b> It was a people who arrived somewhere and were named for it. A family
that walked from Karak to a ridge should recognise that kind of story.</p>"""),

CH(7)

sect('What the ground says', 'The hills turn Christian, and stay that way')
ent('324 → 638', 'attested', False, 'The hills become Christian',
 'Within three or four centuries of the road through Ephraim, the country is overwhelmingly Christian, and it simply stays that way. It happened <b>mostly by conversion rather than by replacement</b>: the people already living here took up the new faith. Samaritan Samaria and Jewish Galilee remain, and the Samaritan revolts of 484, 529 and 555 are fought within sight of this ridge. In the Byzantine centuries Palestine reaches a density of population it will not regain until the twentieth century. The ridge north of Jerusalem fills with village churches, monasteries and oil presses{}.'.format(c('On the Byzantine demographic peak and the density of rural churches on this ridge: Piccirillo, <i>The Mosaics of Jordan</i> and the Madaba map corpus; al-Houdalieh’s excavations at Khirbet et-Tireh (from 2013); Hamdan Taha at ʿAbūd. See the bibliography, §XVIII and §XXIX.')),
 """
<p>The evidence is in the ground within walking distance of the future town.</p>
<p><b>Khirbet et-Tireh</b>, two kilometres from the present town centre, has two churches, a
monastery and an oil press.</p>
<p><b>ʿAbūd</b>, about eighteen kilometres north-west, has a church so old that its rebuilding in
1058 is itself a dated medieval event. We come back to it in the next chapter, when it is rebuilt in 1058.</p>
<p><b>Ṭaybeh</b>, the Ephraim of John 11:54, has its Byzantine church still standing in ruin.</p>
<p>And at <b>Madaba</b>, a great mosaic map was laid in a church floor in the sixth century. It labels
this district with the confidence of an administrator working from an official list.</p>
<p>This is the most important fact about the ground our family will settle on. When sixty-three
Christian households and eight single men come up the ridge road in 1562, they are not bringing Christianity to these
hills. <b>They are joining a Christian population that has been in this district, continuously,
since before Arabic was its language.</b></p>
<p>Our family’s faith is the oldest part of our story that can be checked without any genealogy at
all.</p>"""),

CH(7)
sect('And in our own line', 'The water fails, the dynasty is already north, and a Greek historian writes one of them down')
ent('455 → about 575', 'documents', 'shared', 'The dam breaks',
 'Our family’s tradition says we left Yemen when the great dam at Maʾrib burst, “about 300 AD.” <b>The dam’s failures are dated, and they are later.</b> A breach was repaired under Sharaḥbiʾīl Yaʿfur in 455. There was a further breach in 542/543. The great breach of 547 was repaired in 548, and the last recorded restoration came in 557/558{}.'.format(c('Norbert Nebes, “A New ʾAbraha Inscription from the Great Dam of Mārib,” <i>Proceedings of the Seminar for Arabian Studies</i> 34 (2004), 221–30, esp. 223–24. CIH 540, Sharaḥbiʾīl Yaʿfur’s rupture-and-repair text, is dated Himyarite year 565 = <b>AD 455</b> on the 110 BC epoch Nebes uses; the figure of 449–450 printed in earlier editions of this book reflects the older 115 BC epoch and <b>contradicts the very study cited beside it</b>. CIH 541 records the breach of 657 HE (547) repaired in 658 HE (548). '+D('2004_Nebes_New_Abraha_Inscription_Marib_Dam.pdf')+'.')),
 f"""
<p>We know this in remarkable detail, because the great repair of 548 left <b>an inscription</b>.
That year the Ethiopian-born king Abraha had a record of the work cut into the stone. It lists the
breach, the levies raised, the tribes summoned to labour, and a plague that struck the workforce.</p>
<p>In a separate passage of the same stone he records the delegations he received at Maʾrib: from
Aksum, Byzantium, Persia, and three Arab rulers: al-Mundhir of al-Ḥīra, and al-Ḥārith ibn Jabala with his brother Abūkarib{c('CIH 541, the Abraha inscription of 548 — 136 lines, one of the longest pre-Islamic Sabaic inscriptions known. The dam repair occupies lines 55–61 and 92–117; the diplomatic reception is a distinct episode at lines 87–92, after Abraha’s campaigns and his return to Maʾrib. <b>Earlier editions of this book said the embassies came to witness the repair, and omitted Aksum — the first delegation named, and the one Abraha himself came from.</b> Christian Julien Robin, “Abraha and Ethiopia,” in S. F. Johnson (ed.), <i>The Oxford Handbook of Late Antiquity</i> (2015), 247–332, at 292.')}. It is a maintenance
report, carved in stone, from the collapse of the world our family says it came from.</p>
<p>The Qurʾān records the same disaster from the other side, as the end of a people’s prosperity:
<b>“they turned away, and We sent against them the flood of al-ʿArim.”</b> That is the flood of the
dam, and the two gardens became gardens of bitter fruit{c('Qurʾān 34:16: <span class="ar">فَأَعْرَضُوا فَأَرْسَلْنَا عَلَيْهِمْ سَيْلَ الْعَرِمِ</span> — “the flood of al-ʿArim,” generally understood as the dam or its embankment.')}.</p>
<p>It also draws the lesson that became a proverb, and then a genealogy: “We made them tales, and
scattered them utterly.”{c('Qurʾān 34:19: <span class="ar">فَجَعَلْنَاهُمْ أَحَادِيثَ وَمَزَّقْنَاهُمْ كُلَّ مُمَزَّقٍ</span>. The Arabic proverb <i>tafarraqū aydī Sabaʾ</i> — “they scattered like the people of Sabaʾ” — is still current.')}</p>
{FIX('The family left Yemen “about 300 AD,” when the dam broke.',
 'The dam’s dated failures are <b>455, 542/543 and 547–548</b>, with a last recorded restoration in 557/558 and abandonment conventionally placed at <b>570 or 575</b>. The migration tradition stands; the century attached to it moves forward by some 250 years.',
 'Abraha’s repair inscription of 548 (CIH 541) fixes the mid-sixth-century breach absolutely. <b>The final failure is fixed by nothing:</b> every South Arabian text about the dam is a repair text, the last dated 557/558, and the conventional 570 or 575 rests on later Arabic tradition, not on epigraphy or excavation. This book prints that rather than the confident “c. 575–580” of earlier editions. <b>This correction costs the story nothing and gains it everything:</b> moved forward, the departure lands in exactly the century when the family’s claimed dynasty was at its height on the Roman frontier — which is where the next entries find them.')}
{fig(R.fig_dam(),'The dam, and a date that has to move',
 'The tradition’s “about 300 AD” against the dated breaches. A correction, not a demolition.',
 'Nebes, PSAS 34 (2004); CIH 541; the family tradition in both key texts.')}"""),

ent('c. 250 against 455', 'documents', False,
    'The dam cannot have sent them north',
 f'''Our family’s tradition tells the move north as a chain of three links: the dam failed, the Azd
scattered, and Ghassān went north. Earlier in this chapter we dated the first link, the dam, and
the entries just before this one dated the last, Ghassān in the north. Here we set those dates side by side, and <b>they do not fit</b>. Ghassān is
named as a people with kings of its own in ʿInān 75, in the middle of the third century AD, and again
about a century later in ʿAbadān 1. It is a people of western Arabia, out of Yemen and on the road
north, and in ʿAbadān 1, cut in AD 360, its border with Nizār lies at wells in central Arabia{c('Christian Robin, “The Peoples beyond the Arabian Frontier in Late Antiquity,” pp. 39 and 44: a fight “between the country of Nizārum and the country of Ghassān,” and Ghassān as “an Arab tribe from western Arabia whose main centre was apparently at Yathrib”; Schiettecatte and Arbach (2016), p. 181, place the wells of Sijā in central Arabia. ʿInān 75 itself is a list of kings and names no place. Earlier printings said “both times it is in western Arabia.”')}. In Riyam 2006-17, cut around 260–280, a Sabaean envoy crosses the land of the Azd as his first
stop and the land of Ghassān as his ninth. The dam’s first dated breach is 455. <i>On the evidence set out
in this chapter, Ghassān was in the north at least two hundred years before the water failed.</i>''',
 f"""
<p>There are three ways to explain the mismatch, and only one of them agrees with the stones.</p>
<p><b>One: the inscriptions name a different Ghassān.</b> They do not. They give the same name, the
same region and the same road. No other Ghassān appears anywhere in the South Arabian inscriptions.
We mention this idea only to set it aside.</p>
<p><b>Two: 455 is only the first breach anyone wrote down.</b> This is fair, and partly true. The dam
had been kept up for a thousand years, and every South Arabian text about it is a repair text. But a
record of repairs is not a record of disaster. A slow silting of the Jawf, the lowland of the old Sabaean kingdom,
does not make the single dramatic morning the tradition describes. This idea softens the problem. It
does not remove it.</p>
<p><b>Three, and this is what we believe: the dam is not the cause. It is the memory.</b> The
scattering of the Azd was not one event. It was a slow drift north along the caravan roads over
several centuries. That is how the decline of a trading system feels from the inside: nobody leaves
on a given day, yet in the end everybody has gone.</p>
<p>What the dam gave the tradition was not a reason. It gave it a date and a picture. People do not
remember two hundred years of falling caravan trade. They remember the day the water came through the
wall{c('On the long decline of the South Arabian caravan economy rather than a single catastrophe: Christian Julien Robin on the political fragmentation of the second and third centuries, and Alessandra Avanzini, <i>By Land and By Sea: A History of South Arabia before Islam Recounted from Inscriptions</i> (Rome: L’Erma di Bretschneider, Arabia Antica 10, 2016), which reconstructs the whole period from the epigraphy rather than from later Arabic tradition. '+D('2016_Avanzini_By_Land_and_By_Sea_South_Arabia_before_Islam.pdf')+'.')}.</p>
<p>This does not knock down our family’s story. Every part of the tradition survives: the South
Arabian origin, the Azd, the road north and the name Ghassān. What changes is only the cause. The
neat sentence in which a dam bursts and a people picks up and walks is not the real history.</p>
<p>The genealogists, the scholars who recorded the family trees of the Arab tribes, were not making
up a migration. Writing several centuries later, they gave the one dramatic cause they had to a move
whose real cause was slow and had no story in it{c('Brian Ulrich, <i>Arabs in the Early Islamic Empire: Exploring Al-Azd Tribal Identity</i> (Edinburgh, 2019), 13, 29–31, on the “Scattering of Azd” as an eighth-to-tenth-century literary construction; and Mounir Arbach, Jérémie Schiettecatte &amp; Muḥammad al-Ḥājj, “The Kingdom of Sabaʾ in the Second Century CE — A Reassessment,” in Darles, Khalidi &amp; Arbach (eds), <i>Contacts between South Arabia and the Horn of Africa</i> (Toulouse: Presses Universitaires du Midi, 2021), 69–84, for the political fragmentation already under way three centuries before the dam’s recorded failures. '+D('2021_Arbach_Schiettecatte_Kingdom_of_Saba_2nd_c_CE.pdf')+'.')}.</p>
{FIX('Moved forward, the departure “lands in exactly the century when the family’s claimed dynasty was at its height on the Roman frontier.”',
 'It cannot. <b>The dynasty is on the Roman frontier because Ghassān had left the south long before the water failed.</b> ʿInān 75 puts the name in western Arabia in the mid-third century — some two hundred years before the dam’s first recorded breach — and its editor places the tribe’s centre in that period at Yathrib, not on the frontier. <i>The inscriptions do not put Ghassān in Syria by 250; they put it out of Yemen by 250, which is enough.</i> Correcting the dam’s date forward does not rescue the causal chain — it breaks it from the other end.',
 'The correction in “The dam breaks” (chapter three) is right about the dam and wrong about what the dam explains, and this book does not get to keep both. <b>The Sabaic inscriptions are the strongest thing this project has found about the name</b>, and a find that strong has to be allowed to constrain the story it sits inside rather than decorate it. <i>What survives is the migration. What goes is its trigger.</i> The tradition is not thereby weakened; it is relocated — from history of events to history of memory, which is where most family traditions of this age actually live.')}
<p>One thing follows from this. In the story half of this chapter, the entry on
the scattering quotes Brian Ulrich’s caution that the “Scattering of Azd” is itself a literary
creation of the eighth to tenth centuries. In earlier editions that caution sat in a footnote, as a
scholar’s hedge. On the dates set out here, <b>it becomes the main finding</b>.</p>"""),

ent('473', 'attested', False, 'Amorkesos signs a treaty with Byzantium',
 'In 473 or 474 Amorkesos, an Arab chief on the southern frontier, makes a well-dated federate arrangement with Byzantium: a pact under which an Arab group served the empire as its allies. It covers the Byzantine province called Palaestina Tertia. It is <b>not the earliest, because Queen Mavia’s treaty with Valens is a century older</b>{}. The system our family’s ancestors are said to have led is already running.'.format(c('The Amorkesos episode is known from a fragment of Malchus preserved by Photius (fr. 1, ed. Blockley); Shahîd, <i>Byzantium and the Arabs in the Fifth Century</i> (Dumbarton Oaks, 1989), 61–113, reconstructs it as a formal <i>foedus</i>, which others dispute. <b>Mavia’s treaty with Valens, c. 377–378, is nearly a century earlier and is attested by four independent church historians — Rufinus, Socrates, Sozomen and Theodoret. Earlier editions of this book called Amorkesos “the earliest,” which is wrong.</b>'))),

ent('528–569', 'attested', 'shared', 'Al-Ḥārith ibn Jabala, named in Greek',
 'Al-Ḥārith ibn Jabala stands at generation 34 of our family’s chart, and he is named in Greek by a writer of his own time. Justinian sets him over “as many clans as possible” of the Saracens of Arabia, as the Romans called the Arabs. He gives him <b>“the dignity of king, a thing which among the Romans had never before been done.”</b> Procopius, a contemporary who disliked him, writes it down{}.'.format(c('Procopius, <i>Wars</i> I.17.45–48, Loeb ed. Dewing (1914), i.158–59: <span class="gk">βασιλέως ἀξίωμα</span>, “the dignity of king.” <b>Earlier editions of this book printed the honorific <i>patrikios</i> here; Procopius does not use it in this passage, and what he does say is stronger.</b> '+D('0550_Procopius_History_of_the_Wars_I-II_Loeb.pdf')+', 610 pp. The modern treatment: Shahîd, <i>Byzantium and the Arabs in the Sixth Century</i> I.1 (1995); the field now prefers “Jafnid dynasty” to “Ghassanid kingdom” — Fisher (2011, 2018), Genequand &amp; Robin (2015).')),
 f"""
<p>This is where our family’s line walks out of literature and into history. <b>No sixth-century Greek, Syriac
or Latin source ever uses the word “Ghassanid.”</b> They name individuals, and the
individuals are real{c('Hoyland’s observation. Two centuries earlier, in 363, Ammianus names a “phylarchus Saracenorum Assanitarum,” which Robin reads as Ghassān; the statement here is about the writers of al-Ḥārith’s own century. The scholarly shift from “kingdom” to “dynasty of Byzantine-appointed supreme phylarchs” in Fisher, <i>Between Empires</i> (2011) and Genequand &amp; Robin, <i>Les Jafnides</i> (2015).')}.</p>
<p>In 542 al-Ḥārith petitions the empress Theodora and brings about the consecration of Jacob
Baradaeus, the bishop who rebuilt the Syriac Orthodox church. It is the best-attested fact tying the dynasty to the eastern church{c('John of Ephesus, <i>Ecclesiastical History</i> and <i>Lives of the Eastern Saints</i>, on the 542 petition and the ordinations of Jacob Baradaeus and Theodore.')}. In 554 he defeats the king of the Lakhmids, the Arab allies of Persia, at Chalcis.</p>
<p>On the plateau beside Madaba, the very plateau our family remembers as its road, a sixth-century
church at <b>Nitl</b> carries mosaic inscriptions. They name “Thaʿlaba, the most illustrious
phylarch” and “Arethas son of Arethas.” A phylarch was the chief of an allied Arab tribe, appointed
by the empire. Nitl is the most important monument in Jordan tied to the Jafnids, al-Ḥārith’s own ruling house,
named after their ancestor Jafna, though the
identification rests on the names alone, and both readings are partly restored.</p>
<p>The royal inscriptions that leave no doubt are in Syria. One is the Arabic text at Jabal Usays,
dated 423 of the era of Bostra, the local calendar, which is AD 528. It was first read and published
by the Syrian scholar <b>Muḥammad Abū al-Faraj al-ʿUsh</b>, and it names al-Ḥārith the king
outright. The other is the inscription of al-Mundhir in the apse of his hall at Ruṣāfa{c('Piccirillo, “The Church of Saint Sergius at Nitl,” <i>Liber Annuus</i> 51 (2001); the al-Mundhir audience hall at Ruṣāfa (562–583) and the Ḥarrān inscription of 568 complete the epigraphic core.')}.</p>
<p>Then the empire turns. Al-Mundhir is arrested in 581, shipped to Constantinople, and exiled to
Sicily when Maurice comes to the throne in 582. Al-Nuʿmān is condemned and held after him, as Evagrius tells it, or banished, as Bar Hebraeus does. The
phylarchate, the office of chief phylarch, is broken up among many smaller phylarchs and, so far as
the record shows, never rebuilt under one house{c('Shahîd I.1, 530–563, on the exiles, the dissolution of 582–585 and the restoration of 585–587.')}.</p>
<p>Our chart falls silent after al-Ḥārith, who dies in 569. <b>The last Greek writer to mention a living prince of
his family is Evagrius, writing in 593–594</b>{c('Evagrius, <i>Ecclesiastical History</i> 6.2; Theodor Nöldeke, <i>Die Ghassânischen Fürsten</i> (1887), p. 30: al-Nuʿmān “was still alive when Evagrius wrote (593/4).” Syriac tradition, in Michael the Syrian, still names a “Jafna” as a go-between in the 590s, so the silence is in Greek narrative only. Irfan Shahîd, <i>Byzantium and the Arabs in the Sixth Century</i> I.1 (Dumbarton Oaks, 1995), 554–60, for the disappearance of the Jafnid names from Greek after 593/594. <b>Earlier editions of this book credited this to Serikoff (2017), which is a philological note on Greek loanwords and not about the Ghassanids at all.</b>')}.</p>"""),

ent('after 543', 'classical', 'shared', 'The scattering of the Azd',
 'The classical genealogists trace the whole dispersal of the Azd to the failing of the dam. Arabic keeps the memory in a proverb still spoken today: <b><i>tafarraqū aydī Sabaʾ</i></b>, “they scattered like the people of Sabaʾ.”{}'.format(c('Ibn al-Kalbī and the Azdī pedigree tradition; al-Masʿūdī, <i>Murūj al-dhahab</i>, on the dispersal. Brian Ulrich, <i>Arabs in the Early Islamic Empire</i> (Edinburgh, 2019), 13, 29–31, cautions that the “Scattering of Azd” is itself a literary construction of the eighth to tenth centuries — the tradition’s shape, not necessarily its detail, is what survives scrutiny.')),
 f"""
{fig(F3.fig_scattering(),'“They scattered like the people of Sabaʾ”',
 'Where the Azd tribes went when the water failed. Each arrow became a famous people: the Khuzāʿa who kept Mecca, the Aws and Khazraj who received the Prophet at Medina and are remembered as the Anṣār, the seafaring Azd of Oman — and, north along the caravan roads to the Roman frontier, Ghassān. The family’s tradition is not an eccentric private claim; it is a branch of the best-known migration story in the Arabic language.',
 'Ibn al-Kalbī; al-Masʿūdī; Qurʾān 34:15–19; Ulrich (2019) for the modern caution.')}
<p>One catastrophe, five destinies. <b>This is what makes our family’s story ordinary, in the best
sense.</b> A house claiming descent from Ghassān is claiming a place in the same dispersal that
produced the guardians of Mecca and the helpers of Medina.</p>
<p>The tradition is shared, ancient and enormous. What belongs to our family alone is our own thread
through it.</p>
<p>One scholar, Brian Ulrich, warns that the story of the scattering may itself have been shaped by
writers of the eighth to tenth centuries. The dates do not sit easily with the story, and the
evidence half of this chapter shows why.</p>"""),

ent('563/4 · 569 → 581/2', 'attested', False, 'The silence starts later than the chart',
 'Our family’s line stops at al-Ḥārith, who dies in 569. <b>The dynasty’s record does not.</b> Two inscriptions, one of them published only in 2026, carry the Jafnids further than any text does, and both are in Jordan{}.'.format(c('Both were found and published in Jordan, on the plateau and the desert edge the family’s tradition names as its road — not in Syria, where the dynasty’s capitals were.')),
 f"""
<p>At Tall al-ʿUmayrī East, on the Balqāʾ plateau near Amman, there is a Greek mosaic inscription
three and a half metres long, laid in red tesserae, the small stone cubes of a mosaic. It names
<b>Alamoundaros</b>, that is al-Mundhir, al-Ḥārith’s son, with the Greek titles <i>megaloprepestatos</i>,
“most magnificent”, and <i>komes</i>, “count”. It calls on the God of Saint Sergius over and over. It is dated to about 563/4,
while his father was still alive{c('George Bevan, Greg Fisher and Denis Genequand, “The Late Antique Church at Tall al-ʿUmayrī East: New Evidence for the Jafnid Family and the Cult of St Sergius in Northern Jordan,” <i>Bulletin of the American Schools of Oriental Research</i> 373 (2015), 49–68. The terminal date of the inscription is lost; the authors place it in al-Ḥārith’s tenure, with al-Mundhir holding an intermediate rank before succeeding about 568/9.')}.</p>
<p>In 2024 a stone was found in the north-eastern Jordanian ḥarrah, the basalt desert, at Wadi
al-Shuwayṭī. It carries a <b>Paleo-Arabic inscription dated by the regnal year of al-Mundhir the
king</b>: “year six of the reign of al-Mundhir.” Paleo-Arabic is the Arabic script as it was written
before Islam.</p>
<p>The stone also carries a three-generation genealogy of ordinary men, and that is what makes it
remarkable. It is not a king’s monument. It is somebody counting the years by a Jafnid king’s reign,
in Arabic, on the desert edge{c('Ahmad Al-Jallad, Ali al-Manaser and Greg Fisher, “A Dated Paleo-Arabic Inscription Mentioning al-Mundhir (ʾmndr) the King,” <i>Arabian Archaeology and Epigraphy</i> 70:1 (2026), doi:10.1111/aae.70013. The text is dated to year six of al-Mundhir’s reign, placing it between 569 and his exile in 581/2, and carries the genealogy Zubaydah/Ziyaydah b. ʾhd b. Kuwayṯ; a second text names ʿAlqamah b. ʿAntarat. <b>This is the newest Jafnid epigraphy known and it was published while this book was being written.</b>')}.</p>
<p>What does this do to the gap? The chart’s last named ancestor still dies in 569. But the
silence in the documents about the dynasty now begins around <b>581/2</b> rather than 569, and the
Greek narrative sources run to 593/4.</p>
<p>So the hole in our family’s line and the hole in the record are two different holes. It helps to
keep them apart.</p>"""),

ent('the frontier, in stone', 'attested', False,
    'What they left: one fort, three rulers',
 f'''So far nearly everything we have for the Ghassanids is <i>writing</i>, apart from the church at Nitl: Procopius, two Sabaic
inscriptions, a Greek dedication, an itinerary. <b>There is also a building.</b> At Qaṣr al-Ḥallābāt,
on the Jordanian steppe, stands a Roman fort of the <i>limes Arabicus</i>, Rome’s Arabian frontier.
It was rebuilt, as its excavator Ignacio Arce reads the remains, as a monastic and Ghassanid complex,
and then refurbished again as an Umayyad palace. No inscription there names a Jafnid; the buildings that do carry
their names are at Nitl, Ruṣāfa, Qaṣr al-Ḥayr al-Gharbī, Ḥayyāt and Tall al-ʿUmayrī.
A Roman fort, a Ghassanid hall and an Umayyad palace stand inside the same walls: three regimes, one
set of walls, and no destruction layer between them{c('Ignacio Arce, “Romans, Ghassanids and Umayyads and the Transformation of the <i>Limes Arabicus</i>: from Coercive and Deterrent Diplomacy towards Religious Proselytism and Political Clientelarism,” in Guido Vannini &amp; Michele Nucciotti (eds), <i>La Transgiordania nei secoli XII–XIII e le “frontiere” del Mediterraneo medievale</i>, Limina/Limites 1, BAR International Series 2386 (Oxford: Archaeopress, 2012), ISBN 978-1-4073-0978-1. The article is dedicated to Michele Piccirillo, Svend Helms and Irfan Shahid. '+D('2012_Arce_Romans_Ghassanids_Umayyads_and_the_Limes_Arabicus_BAR_S2386.pdf')+'.')}.''',
 f"""
<p>The archaeologist Arce explains how a frontier stops being a wall. Rome held this line with
forts and garrisons: force, and the threat of it. What replaced that was not collapse but a
different tool: <i>client kings, and a shared religion</i>.</p>
<p>The Ghassanid phylarchs were paid, given titles and made Christian, and the forts they inherited
became audience halls and churches. The Umayyads then inherited the same buildings and the same
method, and changed the religion. <b>The same walls serve three states because each state is doing
the same job by gentler means.</b></p>
<p>There is a lesson in this for our own story. Arce notes that the Ghassanid century has been
almost invisible in archaeology. Classical archaeologists passed over it as a barbarian takeover of
Roman ground, even though the takers were Christian Arabs. Islamic archaeologists passed over it as
the tired last decades before the conquest. It fell between two fields of study, and nobody dug
it.</p>
<p>A gap in a record is not always an absence in the world. <b>Sometimes it is an absence of people
looking</b>{c('Arce, in Vannini &amp; Nucciotti (2012), on the “academic frontier” between classical and Islamic archaeology in Transjordan, and on the excavation and restoration of Qaṣr al-Ḥallābāt directed by the author from 2002. On the same ground: Michele Piccirillo, <i>The Mosaics of Jordan</i> (Amman: ACOR, 1993), for the Nitl church and its Ghassanid dedications.')}. We make the same point about our own
nine hundred missing years in the evidence for the next two chapters.</p>"""),
ent('the question behind the question', 'attested', False, 'Were the Ghassanids sovereign?',
 f"""Procopius says the emperor Justinian gave al-Ḥārith “the dignity of king”. A modern argument
starts from that phrase. If the Ghassanids were sovereigns, the argument goes, then somebody today
might inherit something. <b>Our family should understand how that question works</b> before anyone
answers it for us.""",
 f"""
<p>In the story half of this chapter, al-Ḥārith ibn Jabala leads the Arab allies
of Rome in the sixth century. Here we look at one word used about him, and at what it can and cannot
tell us.</p>
<p><b>Start with what the word is doing.</b> Procopius writes <span class="gk">βασιλέως
ἀξίωμα</span>, the <i>dignity</i>, or rank, of a king. He adds that it had never been done before.
He is describing a promotion inside an empire. He writes as a man of Constantinople, the capital, and
he disliked al-Ḥārith.</p>
<p>So this is an imperial writer telling us what Rome gave. It is not a statement about what
al-Ḥārith already was.</p>
<p><b>Now hear it in Arabic.</b> At Jabal Usays in 528 an ordinary frontier guard, Ruqaym son of
Maʿarrif the Awsite, records that <b>al-Ḥārith the king</b>, <span class="ar">الحارث الملك</span>,
sent him. He does not ask Constantinople’s permission for the word, and he is not writing for
Constantinople.</p>
<p>One man calls him king because an emperor said so. The other calls him king because that is what
people called him on the ground. These are two different kinds of evidence, and the second is
ours.</p>
<div class="fix"><div class="fixhead">The category is younger than the men in it</div>
<div style="font-size:.95rem;line-height:1.65;color:#46423B">
<p style="max-width:none">The modern argument needs “sovereign” to mean a state, a territory,
and a crown that descends and can be inherited or lost. That is a <b>European vocabulary of the
seventeenth century onward</b>. It fits the sixth-century Levant badly. Other cases are worth
comparing, and none of them settles cleanly:</p>
<p style="max-width:none"><b>Persian Yehud.</b> Sheshbazzar and Zerubbabel were Davidic
descendants appointed governors of a Persian province. The empire used the prestige of the dynasty
precisely <i>because</i> it was a dynasty — and that is not the same thing as the dynasty ruling{c('Nadav Naʾaman, “Royal Vassals or Governors? On the Status of Sheshbazzar and Zerubbabel in the Persian Empire,” <i>Henoch</i> XXII (2000). <b>The pattern matters more than the case:</b> an imperial power appointing members of local dynasties as its officers, and both sides finding the arrangement useful.')}.</p>
<p style="max-width:none"><b>The Keneges of Shahrisabz.</b> Their own royal chronicle has them
inheriting their domain from Timur and never being defeated. The surrounding record has them as
one more emirate inside somebody else’s order. <i>A dynasty writing its own sovereignty into its own
chronicle is a normal thing for a dynasty to do</i>{c('James Pickett, “Written into Submission: Reassessing Sovereignty through a Forgotten Eurasian Dynasty,” <i>American Historical Review</i> Forum. The essay is about exactly this: how the paperwork of sovereignty is produced, and by whom.')}.</p>
<p style="max-width:none"><b>And Byzantium itself is a contested category.</b> The people we call
Byzantines called themselves Romans; “Byzantine” is a later coinage, and the field now argues about
how much of the identity was constructed by the people who later wrote about it{c('Anthony Kaldellis, “Provincial Identities in Byzantium” (Routledge, 2022); Yannis Stouraitis, “Is Byzantinism an Orientalism? Reflections on Byzantium’s Constructed Identities and Debated Ideologies”; Koray Durak and Ivana Jevtić (eds.), <i>Identity and the Other in Byzantium</i>, Fourth Sevgi Gönül Byzantine Studies Symposium, Istanbul 2016. <b>These are cited here as what they are — a frame for the question, not evidence about this family.</b>')}. <b>If the empire’s own name for itself is
an argument, the status of its Arab allies will not be settled by a phrase in Procopius.</b></p>
</div></div>
<p>So the answer comes in three sentences. Al-Ḥārith held real authority over real people and was
called a king in two languages. Rome treated him as its instrument and said so. Whether that adds up
to “sovereignty” depends on a definition brought in from outside the sixth century.</p>
<p>For that very reason, scholars have stopped saying “the Ghassanid kingdom”. They now say <b>“the
Jafnid dynasty”</b>, named after Jafna, from whom the line descends{c('Greg Fisher, <i>Between Empires: Arabs, Romans and Sasanians in Late Antiquity</i> (2011) and <i>Arabs and Empires before Islam</i> (2015); Denis Genequand and Christian Robin (eds.), <i>Les Jafnides: des rois arabes au service de Byzance</i> (Paris: De Boccard, 2015) — <i>“Arab kings in the service of Byzantium,”</i> and the tension in that subtitle is the whole argument.')}.</p>
{FIX('The interesting question is whether the Ghassanids were sovereign.',
 'The interesting question is <b>why anyone needs them to have been</b>.',
 'Nothing in this family’s history turns on the answer. Rāshid al-Ḥaddādīn was a farmer with five sons who moved up a ridge and paid a tithe to Hebron; <b>he is not more or less real depending on whether a man in Ruṣāfa nine hundred years earlier met a seventeenth-century European definition of a crown.</b> The question is being asked hard, in our own century, by people for whom the answer has consequences. <b>That is a fact about our century, not about Ghassān</b> — and it is the reason this entry exists at all.')}
<p>Our evidence label for this link does not change. It was <b>Attested</b>, because a Greek historian
of the time and a dated Arabic inscription both name the man. It stays Attested. Sovereignty was
never what held it up.</p>"""),

CH(8)

sect('And in our own line', 'The dynasty’s last century in the record — and then the gap in the record of our people')
ent('636', 'oral', False, 'Yarmūk, a story with no witness',
 'The story goes that at the Yarmūk in 636, Jabala ibn al-Ayham led the Ghassanid contingent. Then he converted, quarrelled with the caliph over a broken nose, and fled to Byzantium. <b>No source from his own time names him at all.</b> The whole story comes from writers of the Abbasid era, 150 to 550 years later, and scholars read Jabala as semi-legendary{}. It is the most famous Ghassanid story and the weakest-attested claim in our whole history. We should know that before we repeat it.'.format(c('Fisher, <i>Rome, Persia, and Arabia</i> (2020): “there are no contemporary sources about Jabala.” The narrative sources are al-Balādhurī (d. 892), al-Ṭabarī (d. 923), and Ibn ʿAsākir (d. 1176).'))),

ent('684', 'documents', False, 'Marj Rāhiṭ: still a people',
 'In 684, the year of the battle of Marj Rāhiṭ near Damascus, the Ghassān are still a people, forty-eight years on. At Jābiya, the old Ghassanid capital, a <i>shūrā</i>, a council of leaders, is called by the Banū Kalb and makes Marwān I caliph. Damascus is secured for him by a Ghassanid nobleman, <b>Yazīd ibn Abī l-Nims</b>{}. Named Ghassanid men, among them a governor of Mosul, a “leader of the people of Damascus” and a family of scholars, hold office in Damascus into the 830s{}.'.format(
  c('Crone, <i>Slaves on Horses</i> (1980), 34–36; Kennedy, “Syrian Elites from Byzantium to Islam,” in Haldon (2010), 196–198.'),
  c('Khalek, <i>Damascus after the Muslim Conquest</i> (2011), 43–46, 66–67; Madelung, <i>JSAI</i> 24 (2000), 333.'))),

ent('about 890', 'documents', False, 'al-Yaʿqūbī finds Ghassān in Transjordan',
 'The geographer al-Yaʿqūbī, describing his own present, records the Ghassān living in the Ghūṭa, the green farmland of Damascus, <b>and at Gharandal, in Transjordan</b>{}. It is the last time a geographer describing his own present places a settled Ghassān population on the ground. It is in the hill country of Jibāl, south of Karak, on the plateau our family remembers as its road. He names other tribes there too, and he says nothing of anyone’s faith.'.format(c('al-Yaʿqūbī (d. 897), <i>Kitāb al-Buldān</i>: Jibāl, “its town is ʿArandal, and its people are of Ghassān, of Balqayn and others”; for the Balqāʾ he names Qays, and for Maʾāb, the Karak district, no tribe. Cited in Kennedy (2010), 198. Gharandal (Arindela) lies on the plateau south of Karak.')),
 """
<p>By then al-Ḥārith had been dead for three hundred and twenty-one years. The Greek sources had
stopped naming the family two hundred and ninety-six years before. Yet a Muslim geographer
writing in Arabic still knows where the Ghassān live, and one of the two places he gives is the
southern Transjordanian plateau.</p>
<p>That single sentence <b>carries the record of our people three centuries further</b>. The gap in
our line is still 931 years, with no fathers named. The gap in the record of our people is much
shorter: about two centuries, after c. 1300. It puts the people our family claims on the exact
ground where our own migration story starts.</p>
<p>It is not a chain of fathers. It is something more modest and more useful: evidence that the
population the tradition names was still there, still named, and still in the right place, long
after the kingdom that made it famous had gone.</p>"""),

sect('What the ground says', 'Meanwhile on this ridge, the Christian villages go on being Christian villages')
ent('about 550 → 750', 'attested', False,
    'The towns do not die',
 f'''In the 630s the armies of Islam take this land from Byzantium. For the people of these hills,
<i>the rulers change and life goes on</i>. We can now show that from the ground itself. Across the river, at Pella,
Jarash and ʿAmmān, the two centuries either side of the conquest of 636 show occupation, markets,
building and church repair running straight through it, with no destruction layer and no
abandonment{c('Alan Walmsley, “Pella, Jarash and ʿAmman: Old and New in the Crossing to Arabia, ca. 550–750 C.E.” The paper opens from the Nessana papyri — the administrator of Nessana, in the <i>kūra</i> of Ghazza within <i>jund Filasṭīn</i>, receiving a requisition for two camels and two drovers about 685 — and works east into the highland towns of Jordan. '+D('19xx_Walmsley_Pella_Jarash_and_Amman_550-750_CE.pdf')+' <b>The offprint carries no year of publication; this book therefore prints none.</b>')}. The names of the governors change on the documents. The
pottery does not change at all.''',
 f"""
<p>This matters to us for one reason. Our family’s tradition puts its ancestors on the
Transjordanian plateau, the country of Karak and Shawbak. That is the same side of the river as
these three towns. It puts them
there in exactly the centuries when the usual story says the region emptied out. <b>It did not empty
out.</b></p>
<p>The excavated towns show that the population stayed, kept trading, kept worshipping, and simply
got new rulers. We believe the same thing happened on our own ridge, for the same reasons.</p>
<p>What it does not do is find anybody of ours. Continuity of settlement is not continuity of a
family, and no name from any of these three towns is ours. It removes an objection rather than
giving a proof: <b>nobody can now say the plateau was empty when the tradition says our people were
on it.</b></p>"""),
ent('1058', 'documents', False, 'A village church is rebuilt at ʿAbūd',
 'About eighteen kilometres north-west of the future Ramallah, the church at <b>ʿAbūd</b> is rebuilt, and the work is dated{}. It is a dated record from inside the silence. Nothing in our family’s record covers this year. The hills do.'.format(c('The rebuilding of the church at ʿAbūd, dated 1058, among the dated Christian records of these hills between the seventh and sixteenth centuries; Hamdan Taha\u2019s work at \u02bfAb\u016bd. See the bibliography, \u00a7XXIX.')),
 """
<p><b>What we still don’t know.</b> We have no chain of fathers between al-Ḥārith, who died in 569,
and the Ghassān that al-Yaʿqūbī found at Gharandal, and no name from Pella, Jarash or ʿAmmān is ours.
The story of Jabala ibn al-Ayham at the Yarmūk has no witness from its own time. If you know of an
inscription, a manuscript or a site from these centuries, you may hold part of the answer.</p>"""),

E[-1] = E[-1][:7] + (E[-1][7] + fig(F5.fig_rulers_traces(), 'Who ruled, and who stayed, 636–1517',
 'Seven dynasties pass over these hills in nine centuries. Underneath them runs one line that never breaks: the Christian villages of the ridge, leaving a dated trace in every one of those dynasties. In 1186, under the Franks, the name Ramallah is written down for the first time.',
 'The traces as cited in this chapter and the next: Taha at ʿAbūd; the cartulary of the Holy Sepulchre; Strehlke no. 20; Thietmar; sijill 48 p. 88; the Ḥaram documents.'),)
CH(9)

sect('What the ground says', 'Four centuries in which the land is thoroughly documented and our own line is not')
ent('1099 → 1187', 'documents', False, 'Magna Mahumeria and the Franks',
 'In these centuries rulers change again and again around villages that stay put. The first new rulers are the Franks, the Crusaders from Western Europe, who arrive in 1099. Crusader al-Bireh, the next hill over from ours, becomes <b>Magna Mahumeria</b>, one of the largest Frankish rural settlements in the kingdom of Jerusalem. Its charter of 1156 lists ninety-two Frankish burgesses, or townsmen, by name, and some fifty more are added over the next thirty years{}. Not one local Christian is listed, though the local Christians were plainly there, because the Franks had to farm around them. Saladin takes the place back in 1187. Yāqūt, writing a generation later, reports having seen the ruin himself{}.'.format(
  c('The 1156 charter in the cartulary of the Holy Sepulchre, often cited as of 11 February, a day this project has not verified against the cartulary itself; Ellenblum, <i>Frankish Rural Settlement in the Latin Kingdom of Jerusalem</i> (1998); Pringle, <i>The Churches of the Crusader Kingdom of Jerusalem</i>, I. '+D('1993_Pringle_Churches_of_the_Crusader_Kingdom_v1.pdf')+'.'),
  c('Yāqūt al-Ḥamawī, <i>Muʿjam al-buldān</i>, s.v. <span class="ar">البيرة</span>. <b>Earlier editions of this book quoted a first-person <span class="ar">رأيتها</span> here; this project has not been able to verify that word in the text and no longer prints it.</b> The secondary literature says only that Yāqūt mentions having seen the ruins.')),
 f"""
{fig(ATLAS.fig_district(),'The hills around Ramallah — what has been dug, what was written, who ruled',
 'Everything within a few kilometres of the future town: the excavated Byzantine sites, the Frankish settlement at al-Bīra, the inscription at Jifnā, the throne villages that ran this district for the Ottomans, and the watershed ridge road that all of it hangs off. Ramallah itself is the one dot with nothing under it before 1562 — which is exactly what a hill of endowment land should look like.',
 'al-Houdalieh on Khirbet et-Tireh; Taha at ʿAbūd; Pringle on the Frankish churches; the Ottoman defters; Conder and Kitchener, <i>Survey of Western Palestine</i>.')}
<p>The Franks are the exception to a pattern we will meet again. <b>They are the one arrival
in four thousand years that truly left.</b> They left a short-lived pulse of European ancestry. Of
nine Crusader-era men buried in a pit at Sidon, only two had mixed European and local ancestry, and
the pulse was gone within a few generations{c('Haber et al., “A Transient Pulse of Genetic Admixture from the Crusaders in the Near East,” <i>AJHG</i> 104:5 (2019), DOI 10.1016/j.ajhg.2019.03.015. The study sequenced thirteen individuals from Lebanon across a thousand years, of whom <b>nine</b> are from the Sidon pit. <b>The negative result is Lebanese</b> — the same test has not been run on this ridge.')}.</p>
<p>Everybody else whose ancestry has been studied stayed and married into the people here. In
Lebanon, where the test has been run, the Frankish ancestry is simply gone. Our family’s own arrival,
four centuries later, is of the second kind: we came, and we stayed.</p>"""),

ent('1182 · 1217/18 · 1321 · 14th c.', 'documents', False, 'The ridge and the plateau stay Christian',
 'Four dated traces show Christians still at both ends of our family’s road. They are in other people’s documents: none was written by anyone in our family, and all fall inside the blank our chart prints. There is <b>a Frankish charter of 1182 signed by one <i>Raymundus de Jafenia</i></b>. There is the pilgrim Thietmar at Shawbak on his journey of 1217–18, hosted and fed by a Frankish widow living in the suburb, where Christians and Muslims lived side by side. There is a Christian majority still at Shawbak in 1321, when Abū al-Fidāʾ wrote in his geography that “most of its inhabitants are Christians” (<span class="ar">وغالب ساكنيه النصارى</span>). And there is one Christian man, in a single contract of 1374 among the Jerusalem Ḥaram al-Sharīf documents, whose village the editors read, with a question mark, as a compound name beginning “Jifnā”{}.'.format(c('The Jifnā charter of 1182, signed by Raymundus de Jafenia, and the Jerusalem Ḥaram documents: the contract of 7 Ṣafar 776 AH (1374), in a collection mostly from 1391–92 (793–794 AH); see “One Christian, one debt” for the queried village name. <b>Earlier editions of this book also printed “the Jifnā inscription of 1179”; the project has not been able to verify that a separate inscription of that year exists, and has retired the date rather than print an object it cannot find.</b> (Little, <i>A Catalogue of the Islamic Documents from al-Ḥaram aš-Šarīf</i>); Thietmar, <i>Peregrinatio</i>, the journey of 1217–18; the stop at Shawbak (Mons Regalis) is dated 1217 in the Transjordanian survey literature and 1218 elsewhere, so this book gives the journey rather than the year; the Christian majority at Shawbak in 1321 from the Mamluk-period record.')),
 f"""
<div class="fix"><div class="fixhead">What the archaeologist sees on the plateau</div>
<div style="font-size:.95rem;line-height:1.65;color:#46423B">
<p style="max-width:none"><b>The family’s tradition asserts continuous Christian residence on the
Shawbak–Karak–Maʿīn plateau from late antiquity to about 1500. The leading archaeologist of Christian
southern Jordan says that is not what the ground shows.</b> Robert Schick finds that the plateau
was solidly Christian in the sixth century, with some fifty churches and hundreds of Christian
tombstones. Its churches, he says, <i>cease Christian use by the ninth or tenth century and often
earlier</i>, and Christians are “scarcely attested in historical sources” from the eighth. In the
tenth to twelfth centuries, in his view, <b>the absence of evidence genuinely reflects population
decline rather than poor survival</b>. Christians reappear briefly with the Crusader presence and then
largely vanish again{c('Robert Schick, <i>The Christian Communities of Palestine from Byzantine to Islamic Rule</i> (Princeton: Darwin Press, 1995), whose survey stops at 813; and his later and harder position in “The Decline of Christianity in Southern Jordan after the Muslim Conquest,” given at the Khalili Research Centre, Oxford. <b>Cited here against the family’s tradition, not for it.</b>')}.</p>
<p style="max-width:none"><i>We print that, because it belongs in our story.</i> <b>What
stands against it is not nothing:</b> a bishop of Karak about 800, a Latin cathedral there in 1167,
a bishop at Shawbak in 1217 (not the pilgrim’s host), a church of St George at Karak in 1329, and a Christian community
paying <i>jizya</i>, the poll tax on non-Muslims, at Shawbak in the register of 1596. <b>The fairest reading is a much-reduced and
possibly interrupted Christian presence, not an unbroken one — and a family tradition of continuous
residence there is asserting more than the archaeology will carry.</b></p></div></div>
<p>These are not our family’s records, and they do not name our family. But they show <b>what our
family’s tradition actually needs</b>. Between the last Ghassanid named in Greek and the first
Ḥaddādīn named in any register at all, there were Christian populations, with the possible break Schick notes, at both ends of
the road the tradition describes: the Karak–Shawbak plateau in the south, and this ridge in the
north.</p>
<p>A migration story needs a population at each end. Both ends are documented. The journey between
them is not.</p>""" + FIX(
 'A grey-haired Greek bishop brings the pilgrim Thietmar bread and cheese at Karak in 1217.',
 'The pilgrim <b>Thietmar</b> was hosted at <b>Shawbak</b>, on his journey of <b>1217–18</b>, by <b>a Frankish widow</b> living in the suburb — <b>not by a bishop, and not at Karak</b>.',
 'Thietmar’s own <i>Peregrinatio</i> is explicit about the place and the person; earlier editions of this book conflated two separate episodes. <b>The year is the one part still loose</b> — the Transjordanian survey literature dates the Shawbak stop to 1217, other accounts to 1218 — so this book prints the journey, 1217–18, rather than choosing. <b>The corrected reading is weaker as an anecdote and stronger as evidence</b>: a resident Frankish widow, in a suburb where Christians and Muslims lived side by side, shows an ordinary settled population, where a visiting bishop would have shown only a visit.')),

ent('26 July 1374', 'documents', False,
    'One Christian, one debt',
 f'''Inside the gap in our record there is a single sheet of paper. In late July 1374, a man called <b>Niʿma ibn Bishāra al-Naṣrānī</b>, “the Christian,” bought a
weight of cotton on credit. The seller was the provisioner Ḥājj ʿUmar ibn Muḥammad ibn ʿUmar
al-ʿAllāf. The price was 218 dirhams, the silver coins of the day, to be repaid at six dirhams at the
close of every week. Two witnesses signed it. Later somebody struck the whole thing through, which is
how a debt is marked paid. The paper survived in the Ḥaram al-Sharīf deposit at Jerusalem{c('Text #922/4 (recto), contract 4, in Said Aljoumani, Zahir Bhalloo &amp; Konrad Hirschler, <i>The Ḥaram al-Sharīf Documents: A Catalogue</i> (Berlin: De Gruyter, 2024), 48 and 175, open access, DOI 10.1515/9783111330242. Six lines, two witness clauses, in very good condition with no lacunae. The witnesses are ʿAlī b. Ismāʿīl b. Shākir and ʿAbd al-Raḥmān b. Muḥammad. The Gregorian date is the tabular conversion of 7 Ṣafar 776 and may be a day or two out. '+D('2024_Aljoumani_Bhalloo_Hirschler_Haram_Documents.pdf')+'.')}. It also says where he came from, but nobody can read
the place-name for certain: it carries a question mark.''',
 f"""
<p>The editors read the scribe’s word as <span class="ar">جفنا الجوز</span>, and print it with a
question mark, <span class="ar">جفنا الجوز؟</span>. They index it under that queried form. <b>It is not simply “Jifnā.”</b> It is a
compound name, uncertainly read, and the catalogue’s own index of places keeps it separate from
anything else.</p>
{FIX('“Men of Jifnā in the Ḥaram registers in 1374,” listed among the dated records that fall inside the blank.',
 '<b>One man, not men</b> — a single named individual in a single contract. And <b>the village is a queried reading</b> of a compound place-name that the editors do not identify with Jifnā north of Ramallah.',
 'Autopsy of the published catalogue, which this project did not do when it first made the claim. The document is real, the man is real, the date is firm and the fact that he is a Christian is written on the page. <i>What is not firm is the one thing the claim rested on.</i> The entry is kept, and demoted from evidence about this district to evidence about the century.')}
<p>We still keep this paper, and here is why. A Christian of the Jerusalem countryside, in 1374, is
named with his father’s name. He buys goods on credit from a Muslim dealer, and the terms are written
into a document good enough to survive six hundred and fifty years.</p>
<p>Whatever village he walked in from, that is what an ordinary Christian life looked like in the
gap in the record of our people, the two centuries after c. 1300 that we cannot yet cross. <b>It is exactly the kind of paper our own
ancestors would have left, if anybody had kept theirs.</b></p>
<p>We also searched the rest of the archive. McGill University has put the 1978 microfilm of the
entire collection online: four rolls, some nine hundred documents, free to anyone{c('McGill University Library, <i>Islamic documents from al-Ḥaram al-Sharīf in Jerusalem</i>, four microfilm rolls digitised and open on archive.org, items <code>McGillLibrary-isl_al-haram-as-sarif_CD2019J47L571984_roll1-20453</code> through <code>roll4-20456</code>. The catalogue that makes them usable is Donald P. Little, <i>A Catalogue of the Islamic Documents from al-Ḥaram aš-Šarīf in Jerusalem</i>, Beiruter Texte und Studien 29 (Beirut, 1984), ISBN 3-515-03699-7 — print only.')}. <b>The machine-read text of it is worthless.</b></p>
<p>In three hundred and ten thousand characters of Arabic read by computer, drawn from a religious
archive in Jerusalem, the words
<span class="ar">القدس</span>, <span class="ar">الحرم</span>, <span class="ar">الشريف</span> and
<span class="ar">قرية</span> occur <b>not once</b>, and <span class="ar">محمد</span> occurs
<b>once</b>. The commonest strings the software produced are <span class="ar">ااا</span> and
<span class="ar">الا</span>. The software is reading the strokes and not the words. The handwriting
of fourteenth-century government offices and courts, photographed on microfilm in 1978, defeats it
completely.</p>
<p>So we searched <b>the published catalogue</b> instead, which any reader can check. Across the whole
of it, the villages of our country, north and south of Jerusalem (Jifnā, ʿAbūd, Ṭaybeh, al-Bireh,
Silwād, Beit Jala, and Ramallah itself), appear exactly twice. One is the queried <span class="ar">جفنا الجوز؟</span> above. The other is a
letter of 1914 about appointing an imam at Silwād in the nāḥiya, or district, of ʿAbawīn, five and a
half centuries too late to help{c('#887, a letter of Jumādā I 1332 / 1914 from Muḥammad Kāmil al-Ḥusaynī, deputy judge of the sharīʿa court at Jerusalem, requesting a <i>berat</i> for Shaykh Muḥammad b. Shaykh ʿAbd al-Fattāḥ as imam of the mosque at Silwād. Aljoumani, Bhalloo &amp; Hirschler (2024), 103.')}.</p>
<p>That is a real result. It does not say the collection holds nothing of ours. It says the
<i>published</i> part of it holds nothing of ours. The unpublished part cannot at present be read by
anybody who is not sitting in a reading room with the originals, or working page by page through
the catalogue Donald Little published of these papers. The gap remains, and the search is written down here so that nobody has to
run it twice.</p>
<p><b>What we still don’t know.</b> The deed of Sultan Qalāwūn’s endowment of 1279–80 is lost. No
document traces the journey between the Karak–Shawbak plateau and this ridge. The village written on
Niʿma ibn Bishāra’s contract has not been read for certain. The unpublished part of the Ḥaram
al-Sharīf documents is still unread. If you can read these old hands, or know of papers from these
centuries, our family would be glad to hear from you.</p>"""),
ent('1186 → 1330', 'documents', False, 'The name appears in 1186',
 f"""A Crusader charter names our town a century before the Mamluk sultans do. On <b>7 March 1186</b>
Guy de Lusignan owed the German hospital in Jerusalem a hundred and eleven marks of silver. He
pledged it a small farm, a hamlet, of his “near the royal road by which one goes to Ramallah,” <i>prope viam
regalem, qua vaditur Ramelie</i>. The village would become the hospital’s if he could not pay within
a year and a day{c('Ernst Strehlke, ed., <i>Tabulae Ordinis Theutonici</i> (Berlin, 1869), p. 18, no. 20; the Latin and an English translation are printed in Azeez Shaheen, <i>A Pictorial History of Ramallah</i> (1992), pp. 17–19. Sāmiḥ Ḥammūdeh, “New Light on Ramallah’s Origins in the Ottoman Period,” <i>Jerusalem Quarterly</i> 59 (2014), p. 39, gives the same date. <b>Earlier editions of this book said the name first appears in 1279. It appears in 1186 — in an article this project already held.</b> ' + D('2014_Hammoudeh_New_Light_Ramallah_Ottoman_JQ59.pdf') + ' · ' + D('1992_Shaheen_A_Pictorial_History_of_Ramallah.pdf') + '.')}.
Its editor had a doubt about it, and the reader should know{c('Strehlke’s own note on no. 20 says <i>totum hoc diploma spurium videtur</i>, “this whole charter seems spurious.” His reasons: it was copied into the register in a separate hand after a charter of December 1243; Guy was crowned only in August 1186; and its opening and closing formulas are unusual. His apparatus shows that <i>qua vaditur</i>, “by which one goes,” is his own correction: the manuscript reads <i>qui vacatur</i>. Ḥammūdeh (2014), p. 39, and Shaheen (1992) accept the charter, and this book follows them. Read from the page itself, printed p. 18, on 11 November 2026.')}.
So the road already went to Ramallah while the Crusader kingdom still stood. The place was well
enough known to give a king’s road its direction.""",
 f"""
{FIX('Guy de Lusignan pledges that if he cannot pay, <b>“the village of Ramallah becomes the hospital’s property”</b>; and “Rey found <i>Ramalei</i> in a manuscript of <b>1198</b>” — as printed in earlier editions.',
 '<b>The village pledged in 1186 is not named.</b> Ramallah is named as the place the royal road beside it leads to — which is still the first time the name is written down. <b>The 1198 document is a forgery</b>, and is withdrawn as evidence.',
 'The charter’s own words are <i>unum casellum nostrum … prope viam regalem, qua vaditur Ramelie</i> — “one hamlet of ours … near the royal road by which one goes to Ramelie.” The “1198” grant to Marseilles, Rey’s source and the one that names an <i>Andreas de Ramella</i>, is one of a set of documents forged at Acre about 1220, identified by Hans Eberhard Mayer from their wrong formulas.' + c('H. E. Mayer, <i>Marseilles Levantehandel und ein akkonensisches Fälscheratelier des 13. Jahrhunderts</i> (Tübingen: Niemeyer, 1972), pp. 1–3; E. G. Rey, <i>Les colonies franques de Syrie</i> (Paris, 1883), p. 389; Mas Latrie, <i>Histoire de l’île de Chypre</i> II (Paris, 1852), pp. 24–25. Summarised in Shaheen (1992), pp. 19–20. <b>Shaheen’s own conclusion is worth keeping: the forger could only use a name everybody already knew.</b>'))}
<p>Next comes an endowment. A Jerusalem court record of 1565 cites a waqf, a religious endowment,
of Sultan Qalāwūn. It is dated 1279–80. In it <i>Rām Allāh</i> is
already a named place, <b>about 283 years before the traditional founding</b>. The deed was shown to
the court in 1565. It does not survive today.{c('Ḥammūdeh (2014), p. 40 and n. 17: “We do not have the text of Sultan Qalawun’s waqf, but court records (sijill 48, page 88) from the end of Dhu al-Qiʿda 972 AH (29 June 1565 CE) mention the waqf and date it back to 678 AH.” 678 AH runs 14 May 1279 – 3 May 1280. <b>The entry is one entry, not two: page 88 of the register, <i>ḥujja</i> 1, is printed on p. 54 of the IRCICA edition.</b> The edition’s summary dates it 23 Dhū al-Qaʿda 972, which is 22 June 1565; Ḥammūdeh, who may have read the folio itself, gives the end of the month, 29 June. We print the edition’s day and name his. The summary records a boundary dispute between Ramallah and al-Bīra over <span class="ar">قرية رام الله</span>, in which the overseer of the endowment produced the deed of 678 AH in court (<span class="ar">احضر … كتاب الوقف المؤرخ سنة ٦٧٨هـ</span>). Ḥammūdeh also reports that Rabāyiʿa dates the endowment earlier, to 640 AH (1242–43). <b>Earlier editions of this book first printed “p. 54, 22 June 1565,” then called that wrong and treated p. 54 as a different entry. What we print here is the summary in the printed edition; the folio itself still wants an eye.</b>')}</p>
<p>Two things follow. First, <b>our family did not name the hill.</b> The name is older than the
settlement, and it is a place-name of the ordinary Semitic kind: <span class="ar">رام</span>, a
height, joined to the divine name.</p>
<p>Second, the legal status explains the archaeology. Land held in <i>waqf</i> could not be sold or
given away. That is exactly the sort of ground that turns up in a sixteenth-century Ottoman register
as cultivated but uninhabited. It is what the register of 1525–28 records for this hill.</p>
<p>A waqf was not just a legal label. It was a working arrangement. A sultan does not endow Hebron’s
kitchen with bare rock. He endows it with a tithe, a share of the harvest, and a tithe means a crop,
and a crop means hands.</p>
<p>Sāmiḥ Ḥammūdeh reads the Mamluk papers as showing a village on this hill, deserted by the end of
that period. The register of 1525–28 finds the land worked and nobody living on it. A register that runs
to 1531–32 lists Ramallah as a village again, and four Muslim households are named here in 1538–39.
<b>Our families, in 1561–62, were the first Christians to stay, and they made the village a town.</b></p>[[C27]]
<p>The better Mamluk evidence is not the lost deed at all. Ramallah is named in documents that
<i>do</i> survive. One group is the Ḥaram al-Sharīf corpus of the 1390s, papers kept at the great
mosque compound in Jerusalem, where Ramallah cultivators guarantee a yearly sum to the Hebron
endowment. The other is <b>Tankiz’s endowment of 1330</b>, where the village is named as the eastern
boundary of ʿEin Qīniya{c('The Ḥaram al-Sharīf documents of 793–796 AH / 1390–95, catalogued by Donald P. Little, <i>A Catalogue of the Islamic Documents from al-Ḥaram aš-Šarīf in Jerusalem</i> (Beirut, 1984); Tankiz’s endowment of 12 Jumādā I 730 / 3 March 1330. These documents exist; Qalāwūn’s deed does not. <b>The figure of “twelve fellāḥīn and 950 dirhams a year” printed in earlier editions of this book cannot be traced to Ḥammūdeh or to Little and is withdrawn until a folio is produced.</b> <b>A lead, not yet a folio:</b> Yossef Rapoport’s study of the same archive describes “a subset of twenty-seven documents, all dating from the 1300s, concerned with villages endowed for the benefit of the Haram al-Sharif in Jerusalem or the Tomb of the Patriarchs in Hebron,” and indexes Ramallah at pp. 93, 97, 99, 103–6 and 109 — Yossef Rapoport, <i>Becoming Arab: The Formation of Arab Identity in the Medieval Middle East</i> (Princeton University Press, 2025), Introduction p. 16 and index, seen in the publisher’s preview; the chapter pages themselves have not been seen. Christian Müller, “A Legal Instrument in the Service of People and Institutions,” <i>Mamlūk Studies Review</i> 12.1 (2008), p. 188 n. 96, lists the village headmen’s guarantees of crops to the Ḥaram endowment as Ḥaram documents nos. 19, 48, 110, 194, 202, 280, 348 and 459, all of 706–708 AH / 1306–08, without naming the villages. The English Wikipedia article on Ramallah (October 2026) puts the twelve men and the 950 dirhams, from “apples, olives and cotton,” on Rapoport’s p. 105; the same sum is given for ʿAyn ʿArīk on p. 104, so the Ramallah figure is held back until p. 105 and the Arabic deed it rests on are read. The surveyed boundaries once attached here to the 1279 deed come from Bakhīt and Sawāriyya and cannot at present be assigned to either instrument with confidence.')}.</p>
<p>We also looked where the name might be missing. Mujīr al-Dīn wrote a topography of Jerusalem
and Hebron, completed in 1495 (900 AH). We searched it in full, and <b>it has no Ramallah in
it</b>{c('Mujīr al-Dīn al-ʿUlaymī, <i>al-Uns al-jalīl bi-taʾrīkh al-Quds wa-l-Khalīl</i> (1495), searched complete for this project in the copy held in the family library. <b>The silence is weak evidence and is printed as such:</b> <i>al-Uns al-jalīl</i> is a history of Jerusalem and Hebron with an incidental and selective village list, not a gazetteer, and a hamlet of a few households would not be expected in it. ' + D('1495_Mujir_al-Din_al-Uns_al-jalil.pdf') + '.')}.
</p>
<p>Between 1186 and 1562 the name is on paper, but the hill is barely a hamlet. It is endowment land
with no residents in 1525–28. By 1538–39 there are four Muslim households: <b>Ḥasan bin Labūd,
Khaṭṭāb bin Ḥasan, Rajab bin Yaʿqūb and Ibrāhīm bin Labūd</b>, the first people of this place whose
names we have. By 1553–54 there are six. The deed and the registers say the same thing from opposite
ends.</p>"""),

CH(10)

sect('And in our own line', 'The missing centuries, measured rather than filled')
ent('569 → about 1500', 'none', False, 'Thirty-one generations, and one name',
 'Al-Ḥārith dies in 569 and is named in Greek writing of his own time. Rāshid lived about 1500, by our family’s own texts, and the Ottoman registers reach his grandchildren in 1562. Between the two men, <b>the family chart draws two links across 931 years</b>. That cannot be done. <i>The chart says so itself: it prints the gap, in the same type as everything else.</i>',
 f"""
<p>The chapter before this one, this chapter and the two that follow tell the story of the land
across many centuries. Through that long stretch the land is well recorded,
but our own line of fathers is not. Here we look at that gap.</p>
<p>This is the weakest link in our family’s chain. It also shows how carefully the chart was made,
and the right response is arithmetic, not embarrassment. Nine hundred and thirty-one years,
divided by <b>an assumed</b> father-to-son generation of twenty-five to thirty-five years, gives
twenty-seven to thirty-seven generations. The most likely figure is about thirty-one.</p>
<p>The chart draws two. So the right thing to print at generation 35 is not a blank and not an
invention. It is <b>a number: “about 31 generations.”</b></p>
<p>That number changes how we count the line. The co-authors’ own chart runs to thirty-six rows,
because it draws the gap as one row. Opened out to the thirty-one generations the arithmetic needs,
the line from Adam to Rāshid is <b>sixty-six generations, not thirty-six</b>. That is thirty-four down
to al-Ḥārith, thirty-one across the gap, and Rāshid at sixty-six. <i>The family ladder drawn through
our chapters now uses that count.</i></p>
<p>Of those thirty-one, thirty have no name of any kind. <b>One does</b>: the last of them, generation
sixty-five, <b>Ṣaqr</b>, the name the Karak side of the family gives for Rāshid’s father (we
meet him in chapter 7). <i>He is named by the Karak side of the family, in print since Abū Rayya
(1980) and on the Karak wheel (2024). That is one tradition, with no document, so the ladder prints
him in a broken outline.</i></p>
<p>The other reading comes from our own chart: Rāshid bin ʿĪsā bin ʿIyād bin Ḍahdūḥa. It would fill
generations sixty-three to sixty-five instead, and we set it out in the evidence for chapter 7,
From Karak to Ramallah. Either way the count is sixty-six. What changes is only how many of the
last three places carry a name.</p>
<div class="ntwrap"><div class="nthead">The line, recounted</div>
<table class="ntable"><tr><th>generations</th><th>who</th><th>what carries them</th></tr>
<tr><td><b>1–34</b></td><td>Adam and Eve down to al-Ḥārith b. Jabala, d. 569</td><td>scripture, then the Arabic genealogists, then Procopius in Greek</td></tr>
<tr><td><b>35–64</b></td><td><i>thirty men, and not one name for any of them</i></td><td>Nothing. This is the gap, measured rather than filled</td></tr>
<tr><td><b>65</b></td><td><b>Ṣaqr</b> <span class="ar">صقر</span></td><td>the Karak side, in print since Abū Rayya (1980) and on the Karak wheel (2024) — one tradition, no document</td></tr>
<tr><td><b>66</b></td><td><b>Rāshid al-Ḥaddādīn</b>, lived about 1500</td><td>both family texts; the registers reach his grandchildren in 1562</td></tr>
</table></div>
<p><b>Thirty-six of the sixty-six have names. Thirty do not.</b> <i>Those two numbers sum up all that
our family knows of its own line, and neither of them is anything to be ashamed of.</i></p>
{fig(R.fig_arith(),'Forty-five is the wrong number',
 'Before looking for the missing generations it is worth checking the count that is usually quoted. Forty-five generations across 931 years implies a male-line generation of about twenty-one years, shorter than any population on record sustains. Thirty-one generations at thirty years each fits. <b>Correcting the arithmetic does not close the void — it measures it.</b> <i>The thirty-year figure is an assumption and not a measurement; the entry on the clock says so at length.</i>',
 'Generational-interval range after the standard genealogical-demography literature; the span from al-Ḥārith (d. 569) to Rāshid (fl. c. 1500), 931 years.')}
{FIX('A fixed count of generations between al-Ḥārith and Rāshid.',
 '<b>A range: about 27 to 37 generations</b>, most probably around 31 — and the line recounted at sixty-six, not thirty-six.',
 'Arithmetic, not a source: al-Ḥārith (d. 569) to Rāshid (fl. c. 1500) is 931 years; at <b>an assumed</b> 25–35 years a generation, that is 27–37, of which the chart draws two. No source is needed for a division, and none is claimed — <b>but the interval is not a fact, and the entry that follows says where it comes from and why no better one exists.</b>')}
{fig(F.fig_void_solved(),'The void, measured — and shortened',
 'The gap in our line runs 931 years, from al-Ḥārith (d. 569) to Rāshid (fl. c. 1500), with no fathers named, and needs about thirty-one generations to cross. The gap in the record of our people is far shorter, about two centuries after c. 1300 — Ghassān is entered as a living people, at al-Balqāʾ, the Yarmūk and Ḥimṣ, on the authority of a Mamluk officer who died about 1300 — and dated records fall inside the blank: ʿAbūd’s rebuilt church in 1058, a man of Jifnā signing a Frankish charter in 1182 and a Christian buying cotton on credit at Jerusalem in 1374, the pilgrim Thietmar hosted in Shawbak’s suburb on the journey of 1217–18, a Christian majority at Shawbak in 1321. What no source supplies is a chain of fathers. So the chart should print the number, not a blank.',
 'Procopius; Shahîd, BASIC I.1 (1995), 554–60; Kennedy (2010), p. 198, citing al-Yaʿqūbī; the ʿAbūd, Jifnā, Thietmar and Shawbak records.')}
<p>The silence in our family’s line is not a silence in our family’s world. The next two chapters
walk through these centuries one dated record at a time. A people is still named in 684 and still located in 890.
It is <b>still entered as existing about 1300</b>.</p>
<p>A church is rebuilt in 1058. A man of Jifnā signs a Frankish charter in 1182. A pilgrim is fed at
Shawbak in 1217–18, and there is a Christian majority there in 1321. A named Christian buys cotton on
credit at Jerusalem in 1374, and our town’s own name stands on a sultan’s deed of 1279–80.</p>
<p><i>Everything survives across those nine hundred years except the one thing a family tree needs, a
chain of fathers. The chart is the document that admits it.</i></p>"""),


ent('about 1300 → about 1418', 'documents', False,
    'Ghassān is still there in 1400',
 f'''In chapter 5 we saw al-Yaʿqūbī place the Ghassān at Gharandal in 890. They can be followed much
later than that. <b>The gap in the record of our people is not six hundred years long. It is about two centuries, after c. 1300.</b> Al-Qalqashandī
finished <i>Qalāʾid al-jumān</i>, <i>Necklaces of Pearls, on the Tribes of the Arabs of the Present Age</i>,
in the first years of the fifteenth century. Ghassān is in it, not as a memory but as a people with
addresses: al-Balqāʾ, the Yarmūk, and Ḥimṣ{c('Al-Qalqashandī, <span class="ar">قلائد الجمان في التعريف بقبائل عرب الزمان</span>, ed. Ibrāhīm al-Ibyārī, 2nd ed. (Cairo/Beirut, 1402/1982), <b>p. 97</b>, closing the entry <span class="ar">البطن الثاني من الأزد: غسان</span> at pp. 94–97: <span class="ar">قال في مسالك الأبصار: وبالبلقاء طائفة من غسان. وباليرموك منهم الجمّ الغفير، وبحمص منهم جماعة</span>. The same notice stands in his <span class="ar">نهاية الأرب في معرفة أنساب العرب</span>, ed. Ibyārī, no. 1421, p. 388, where it is credited not to al-ʿUmarī but to <span class="ar">الحمداني</span> — <b>the two attributions together are the transmission chain, visible in one author’s two books.</b>')}.
<i>Somebody in Mamluk service knew where to find them.</i>''',
 f"""
<p><b>And we can name that somebody.</b> The chain runs back from al-Qalqashandī to a man whose job was
to know exactly this. Al-ʿUmarī wrote his <i>Masālik al-abṣār</i> in the 1340s. He opens his chapter
“On the Arabs of our own time and their places” by saying where he got it: “I have relied
for most of this on what the trustworthy amīr Badr al-Dīn Abū al-Maḥāsin Yūsuf ibn Zammākh, known as
Ibn Sayf al-Dawla al-Ḥamdānī, <span class="ar">المهمندار</span>, has recorded”{c('Ibn Faḍl Allāh al-ʿUmarī, <span class="ar">مسالك الأبصار في ممالك الأمصار</span>, ed. al-Majmaʿ al-Thaqāfī (Abu Dhabi), <b>iv.243</b>, opening <span class="ar">في ذكر العرب الموجودين في زماننا وأماكنهم</span>: <span class="ar">واعتمدت في أكثر من ذلك على ما ذكره الأمير الثقة بدر الدين أبو المحاسن يوسف بن أبي المعالي بن زمّاخ المعروف بابن سيف الدولة الحمدانيّ المهمندار</span>. The editor’s note adds that he was <i>the</i> genealogist of his age and that most who came after him on the Arab tribes were in his debt — <span class="ar">عالة عليه</span> — <b>al-ʿUmarī included</b>. Al-Qalqashandī in turn writes <span class="ar">قال الحمداني</span> fifty-eight times in <i>Qalāʾid al-jumān</i> alone.')}.</p>
<p>A <span class="ar">مهمندار</span>, <i>mihmandār</i>, is not a collector of old stories. He is the
officer who receives, lodges and feeds the tribal delegations that arrive at the sultan’s court. He
has to know which tribes exist, how many they are and where they camp, because he answers for feeding
them.</p>
<p>Al-ʿUmarī gives Ibn Zammākh’s own account of hosting one such delegation for the sultan Aybak. Gifts
worth thirty-six thousand dinars passed, he says, “all of it through my own hands”{c('<i>Masālik</i> iv.340. On the man: Ibn Ḥajar, <span class="ar">الدرر الكامنة</span> vi.227 no. 2605; Ibn Shākir al-Kutubī, <span class="ar">فوات الوفيات</span> iv.349 no. 589, calling him <span class="ar">مهمندار العرب</span>; Bakr Abū Zayd, <span class="ar">طبقات النسابين</span> no. 321, which names his <span class="ar">كتاب الأنساب</span>. <b>Born 602/1205–6; the death date is disputed and this book prints the dispute</b> — Ibn Ḥajar and Abū Zayd give 700/1300, al-Ziriklī (<span class="ar">الأعلام</span> viii.233) and Kaḥḥāla give about 670/1272, balking at an age of ninety-eight.')}.
<i>This is an official’s record that happens to have survived inside a work of literature.</i></p>
{NUMTABLE('THE CHAIN, END TO END',
 ['when', 'who', 'what it gives'],
 [['c. 945', 'al-Hamdānī of Yemen, <span class="ar">صفة جزيرة العرب</span>', '<span class="ar">ديار غسان</span> — Ghassān as a named territory'],
  ['538 / 1144', 'Ibn ʿAsākir, at Damascus', 'a family still nicknamed <b>Half the Road</b> for an ancestor who set out after Jabala b. al-Ayham and turned back'],
  ['<b>d. c. 1272–1300</b>', '<b>Ibn Zammākh al-Ḥamdānī, <i>mihmandār al-ʿarab</i></b>', '<b>Ghassān among the tribes of the present day — from the officer paid to know</b>'],
  ['c. 1340s', 'al-ʿUmarī, <i>Masālik al-abṣār</i>', 'transmits him, and places the Ghassān of the Yarmūk, al-Balqāʾ and Ḥimṣ'],
  ['c. 1400', 'al-Qalqashandī, <i>Qalāʾid al-jumān</i>', 'copies it into a handbook whose stated subject is tribes now existing'],
  ['<b>c. 1500</b>', '<b>Rāshid al-Ḥaddādīn</b>', '<b>generation 66</b>']],
 'Read down the column of dates. <b>Between the last administrative notice of Ghassān as a living people and the first man in our own line there are about two centuries</b>: this is the gap in the record of our people, after c. 1300. The book that carries the notice is a century nearer, about 1400. <i>Six hundred years of silence was never the right number.</i>')}
{FIX('“The documentary void is three hundred years shorter — a named Ghassān population is attested to about 890.”',
 '<b>To about 1300, and quite possibly to about 1400.</b> Ghassān is entered as a currently existing people, with three locations, in a Mamluk chancery handbook, on the authority of the officer whose duty was receiving Arab delegations.',
 'Al-Qalqashandī, <i>Qalāʾid al-jumān</i> (ed. Ibyārī), p. 97, and <i>Nihāyat al-arab</i>, no. 1421, p. 388; al-ʿUmarī, <i>Masālik al-abṣār</i>, iv.243 and iv.358–59. <b>The 890 date stands as the last notice in Transjordan specifically; what changes is the last notice anywhere.</b>')}
<p>This is the best news the tradition has had, and that is exactly when we should slow down. Three
cautions follow.</p>
<p><b>One: the places are east and north, not here.</b> Al-Balqāʾ, the Yarmūk and Ḥimṣ are all across
the Jordan or beyond. <i>This record shortens the gap. It does not move Ghassān to our ridge.</i> And,
as we show in chapter 7, From Karak to Ramallah, every Arab authority who names a
place puts them east.</p>
<p><b>Two: al-Qalqashandī is copying, not observing.</b> The fact is Ibn Zammākh al-Ḥamdānī’s, from about 1300.
Al-ʿUmarī passes it on about 1340, and al-Qalqashandī writes it out about 1400. To say that
al-Qalqashandī saw Ghassān at the Yarmūk in his own lifetime would claim four generations more than
the page supports.</p>
<p><b>Three: he also changed a word, and it is the word that matters.</b> Al-ʿUmarī wrote that at the
Yarmūk there were <span class="ar">صليبة من غسان</span>. Al-Qalqashandī replaced that with
<span class="ar">الجمّ الغفير</span>, “a great multitude.” <i>The multitude is al-Qalqashandī’s. The
word underneath it is al-ʿUmarī’s, and it explains the whole silence, as the next part shows.</i></p>"""),

ent('about 1340', 'documents', False,
    'The word underneath',
 f'''Al-ʿUmarī does not file these Ghassānids under tribes. He files them under
<span class="ar">صليبة العرب</span>, <i>Arabs of pure and direct descent</i>. Then he says what has
become of them: <b>“in Syria there are, of the pure-stock Arabs, various peoples in the
settled country <span class="ar">قد خرجوا بها عن حكم العرب</span> — they have passed out of the
reckoning of Arabs — and have become townspeople, settled, dwellers who populate
houses”</b>{c('<i>Masālik al-abṣār</i>, ed. al-Majmaʿ al-Thaqāfī, <b>iv.358</b>: <span class="ar">وبالشام من صليبة العرب أقوام شتى في البلاد قد خرجوا بها عن حكم العرب وصاروا بها أهل حاضرة ساكنة، وعمّار ديار قاطنة</span>. <b>An earlier draft of this book read <i>ṣalība</i> as meaning “those who passed out of Arab status.” It does not.</b> It is the standard genealogical term for unmixed, direct descent — the opposite of <i>mawlā</i> — glossed in the ḥadīth manuals as <span class="ar">خالصة النسَب</span>. The passing-out is not the definition; it is what al-ʿUmarī says has happened <i>to</i> them. <i>Correcting the gloss makes the sentence stronger, not weaker.</i> A caution for anyone checking the page: the Abu Dhabi editor’s own footnote confuses <i>ṣalība</i> with the Ṣulubba of the Syrian desert, an unrelated and genealogically déclassé group, and contradicts al-ʿUmarī’s usage two pages later.')}.
<i>They are still of the purest descent. They have simply stopped being the kind of people a tribal
register records, because they stopped moving.</i>''',
 f"""
<p>This explains how a people can be present and yet go unrecorded. <b>The man compiling the list
says it himself, in the fourteenth century.</b></p>
<p>A register of tribes records tribes. A village of farmers is not a tribe. When a family line
settles, it does not vanish. It moves into a new category, and nobody was keeping a list of that
category.</p>
<p><i>So the silence in the record is not the silence of a people dying out. It is the silence of a
people who were no longer written down, because the officials who wrote people down were counting
those who moved.</i></p>
<p>Then there is the list itself, which surprised us. Al-ʿUmarī names where these settled Arabs of
pure descent live, and the places are not in Transjordan. They are <b>here</b>{c('<i>Masālik al-abṣār</i>, iv.358–59: <span class="ar">فبمدينة غزة وبلد الخليل … معمور بني تميم الداريّ. وبوادي بني زيد فرقة من بني جعفر بن أبي طالب، وفرقة من بني عمر بن الخطاب، وبالقدس منهما، وبنابلس كثير من قحطان وطائفة من مضر بن نزار، وبجينين وبلادها أقوام من حارثة ومن بكر بن وائل</span>; then, further on, <span class="ar">وبالبلقاء منهم ومن بني أمية ومن غسّان … وباليرموك صليبة من غسان … وبحمص قوم من غسّان</span>. The Ghassān notice that al-Qalqashandī later abridged sits <b>inside this same section</b>.')}:</p>
{NUMTABLE('AL-ʿUMARĪ’S SETTLED ARABS OF SYRIA, c. 1340 — the Palestinian entries',
 ['where', 'who he says is there'],
 [['<b>Gaza and the country of Hebron</b>', 'the settlement of Banū Tamīm al-Dārī'],
  ['<b><span class="ar">وادي بني زيد</span> — the Banū Zayd valley</b>', '<b>a section of Banū Jaʿfar b. Abī Ṭālib, and a section of the line of ʿUmar b. al-Khaṭṭāb</b>'],
  ['<b>Jerusalem</b>', 'members of both of those'],
  ['<b>Nablus</b>', 'many of Qaḥṭān, and a group of Muḍar b. Nizār'],
  ['<b>Jenin and its country</b>', 'peoples of Ḥāritha and of Bakr b. Wāʾil'],
  ['al-Balqāʾ · the Yarmūk · Ḥimṣ', '<b>Ghassān</b> — al-Balqāʾ with Banū Umayya, the Yarmūk group named <i>ṣalība of Ghassān</i>']],
 '<b>Wādī Banī Zayd is this district.</b> It is the nāḥiya that contains Dayr Ghassāna, and it begins a few hours’ walk north of our hill. <i>Al-ʿUmarī is not naming our family — he names two lineages, and neither is ours.</i> But he is doing something this book had assumed no fourteenth-century source did: <b>naming settled Arab lineages of claimed pure descent, by name, in the Ramallah hills, a hundred and sixty years before Rāshid.</b> The category the family belongs to is in the record. Only the family is not.')}
<p><i>We can put it plainly.</i> <b>The gap is not a gap in the world. It is a gap in one column of one
kind of document.</b> And al-ʿUmarī, who kept that column, wrote down in so many words why the people
he describes had begun to drop out of it.</p>"""),

ent('900 / 1495', 'documents', False,
    'The man who should have known',
 f'''<b>Now the evidence on the other side, at full strength.</b> Mujīr al-Dīn al-ʿUlaymī finished
<i>al-Uns al-jalīl</i> at Jerusalem in 900 AH, which is 1495. That is within a few years of the time
Rāshid lived, in the city our ridge belongs to, in a book about the country of Jerusalem and Hebron
and its people. He mentions the Ghassānids exactly once, in the usual list of the Prophet’s letters to
foreign kings: al-Ḥārith the Ghassānid at Damascus. He mentions them nowhere else{c('Mujīr al-Dīn al-ʿUlaymī, <span class="ar">الأنس الجليل بتاريخ القدس والخليل</span>, searched complete in <b>two independent printed editions</b> (the Dandīs and the Najaf texts). <span class="ar">غسان</span> and every inflected form return nothing; <span class="ar">الغساني</span> returns one hit in each, the same sentence: <span class="ar">وأرسل إلى الحارث الغساني بدمشق</span>. <span class="ar">الغساسنة</span>, <span class="ar">الأيهم</span>, <span class="ar">تنوخ</span> and <span class="ar">لخم</span> return nothing at all. <b>Controls prove the search reaches the text</b>: <span class="ar">القدس</span> 363 and 307, <span class="ar">غزة</span> 62 and 55. <i>An earlier draft of this entry said “zero times.” It is once, formulaically, and the difference is printed because anybody can check it in five seconds.</i>')}.''',
 f"""
<p>Mujīr al-Dīn wrote in our forefather Rāshid’s own generation, so his silence deserves a careful
look, from both sides.</p>
<p><b>First side.</b> Mujīr al-Dīn is a qāḍī, a judge, of Jerusalem, writing local history and the
lie of the land for local readers. Suppose a people in his hills called itself Ghassān, or was called
so by its neighbours. He was better placed than anyone in the world to say so, and he had every
reason to. <i>He does not.</i> Nor does he name Jafna, or al-Ayham, or Tanūkh, or Lakhm.</p>
<p><b>Other side.</b> <i>Al-Uns al-jalīl</i> is a history of two holy places with a village list on the
side. It is not a census and not a register of tribes. The same book has no Ramallah in it either, at
a time when the registers prove there were households on the hill. <b>An argument from its silence
proves less than it seems to.</b></p>
<p>So we set both pages side by side. The Mamluk government’s records say Ghassān is a living people,
at al-Balqāʾ and the Yarmūk and Ḥimṣ, in about 1300. The qāḍī of Jerusalem, two centuries later and
thirteen kilometres away, says nothing of them as a living people.</p>
<p>Both are true. Neither cancels the other. A family history that gave only the first would be
poorer than one that gives the second beside it.</p>"""),

ent('828 / 1424', 'attested', False,
    'The tradition’s own word: <span class="ar">نسب القطع</span>',
 f'''<b>Arab genealogists did not pretend a chain was unbroken when it was not.</b> They had a term for
it, and Ibn ʿInaba defines it in his chapter on the words of the trade: “when there is a group in some
region of whom no report has come, and of whom the genealogists know no trace, they say —
<span class="ar">هم في نسب القطع</span> — their lineage is cut off from connection, <i>even if they
were formerly well known</i>”{c('Ibn ʿInaba (Jamāl al-Dīn Aḥmad b. ʿAlī al-Ḥusaynī, d. 828/1424), <span class="ar">عمدة الطالب في أنساب آل أبي طالب</span>, ed. Muḥammad Ḥasan Āl al-Ṭāliqānī, 2nd ed. (Najaf, 1380/1961), <b>p. 372</b>, in the section <span class="ar">فصل في كلمات تداولتها النسابون في كتبهم</span>: <span class="ar">ومن ذلك إذا كان جماعة في صقع من الأصقاع لم يرد لهم خبر ولا عرف لهم عند النسابين أثر قالوا: (هم في نسب القطع) أي مقطوع نسبهم عن الاتصال وإن كانوا من قبل مشهورين</span>. He ascribes the phrase to <span class="ar">النسابون</span> generally — it is the guild’s word, not his coinage. <b>Not to be confused with</b> <span class="ar">منقطع</span>, the ḥadīth critics’ term for a broken chain of transmission. Pagination from the digital text of the Najaf edition; it should be checked against a printed copy.')}.
<i>That is our family’s situation, described four centuries before any of us went looking.</i>''',
 f"""
<p>The term is <i>nasab al-qaṭʿ</i>, “cut-off lineage”. <b>The tradition joins a rule to it.</b>
Ibn ʿInaba writes of the Idrīsids of the Maghrib, North Africa, whose line had dropped out of the
record in just this way: “they are in <i>nasab al-qaṭʿ</i>; <span class="ar">يحتاج من يعتزى إليهم إلى زيادة وضوح في حجته</span>
— whoever traces his descent to them needs additional clarity in his proof — because of their
remoteness from us and our not being informed of their circumstances”{c('<span class="ar">عمدة الطالب</span>, p. 161: <span class="ar">وبنو إدريس كثيرون وهم في نسب القطع يحتاج من يعتزى إليهم إلى زيادة وضوح في حجته لبعدهم عنا وعدم وقوفنا على أحوالهم</span>. <b>Said of the Idrīsids specifically, not as a general maxim</b> — but the reasoning is general, and it is the reasoning this book has been applying without knowing there was a name for it.')}.</p>
<p>Notice what this sentence is not. It is not a modern doubter holding an old claim to a foreign
standard. It is the old standard itself, in the old words, set out by a working genealogist of
the generations just before Rāshid. <b>Where the record is cut, the person making the claim has more to prove.</b></p>
<p>Throughout our story we have raised that burden and met what can be met. It turns out we were
following a rule that already existed.</p>
<p>And the greatest of the Arab historians names our people in the very next paragraph. Ibn Khaldūn
argues that pure lineage survives only among Arabs who stayed in the desert. He lists those who did
not: “the Lakhm, the Judhām, <span class="ar">وغسّان</span>, the Ṭayy, the Quḍāʿa and the
Iyād — <span class="ar">فاختلطت أنسابهم وتداخلت شعوبهم</span>, their lineages became mixed and their
groups intermingled, and it is known that the genealogists differ about every one of these
houses”{c('Ibn Khaldūn, <span class="ar">المقدمة</span>, Book Two, chapter 9 — <span class="ar">الفصل التاسع في أن الصريح من النسب إنما يوجد للمتوحشين في القفر من العرب</span>; Rosenthal (Bollingen) translates the chapter heading “Purity of lineage is found only among the savage Arabs of the desert and other such people.” <b>The cause he gives is the same one al-ʿUmarī gives:</b> settlement, and contact with non-Arabs. <i>Cited by book and chapter rather than by page, because this project has not verified a page in the Bollingen printing.</i>')}.</p>
<p>So the two greatest authorities of the generations just before Rāshid both say, in their own words, that a
claim like ours is hard to prove. They also say that <b>Ghassān is one of the lines where it is
hardest</b>. <i>Our family’s tradition does not fall short of a modern standard. It falls short of a
fourteenth-century one, and it is open about that.</i></p>"""),

ent('the neighbours’ word for us', 'attested', False,
    'What the other archive calls them',
 f'''<b>A second body of writing ought to have our people in it, and it is in Syriac</b>, the language of
the eastern churches. Six Syriac chronicles were searched for our family’s history, and <b>Ghassān
appears in none of them</b>. But the chronicles are not silent about Arab Christians. After the Islamic
conquest they name living Arab Christian peoples, in the same country. There are the
<b>Tanūkhāyē</b>, five thousand of whom were forced to give up their faith at Aleppo in 778–9; the
chronicle names the martyr Layth among them. There are the Tuʿāyē, and the ʿĀqōlāyē. They appear at
Aleppo and Boṣrā, the very ground the Jafnids held.''',
 f"""
<p>This part asks why the name “Ghassanid” may be nobody’s word but ours.</p>
<p><b>The Syriac writers had words for these people, and the words were not ours.</b> They say
<span class="ar">ܛܝܝܐ</span> <i>Ṭayyāyē</i>, “Arabs”. When they mean a ruling family, they build its
name on the ruler’s name: <i>Bēth Ḥārith</i>, the house of al-Ḥārith, and <i>Bēth Mundhir</i>, the
house of al-Mundhir{c('Robert G. Hoyland, “Insider and Outsider Sources: Historiographical Reflections on Late Antique Arabia,” in J. H. F. Dijkstra &amp; G. Fisher (eds), <i>Inside and Out: Interactions between Rome and the Peoples on the Arabian and Egyptian Frontiers in Late Antiquity</i> (Leuven: Peeters, 2014), p. 269; and Greg Fisher &amp; Philip Wood, “Writing the History of the ‘Persian Arabs’,” <i>Iranian Studies</i> 49:2 (2016), 247–90, at 250. <b>Neither states that a form</b> Bēth Ghassān <b>never occurs</b>, and this book will not claim a universal negative it has not proved; what is established is that the form is unattested in the corpus these scholars survey.')}.
<i>A house named for a man, not for a tribe.</i></p>
<p>The Greek and Latin writing helps us no more. Fergus Millar went through the whole record written
at the time inside the Roman empire, and he says it plainly: <b>“the entire contemporary
evidence discussed here, literary and documentary, in Latin, Greek, Syriac, and Arabic, from within
the empire does not contain a single expression which equates to, or could properly be translated as,
either ‘Ghassanid’ or ‘Jafnid’”</b>{c('Fergus Millar, “Rome’s ‘Arab’ Allies in Late Antiquity: Conceptions and Representations from within the Frontiers of the Empire,” in H. Börm &amp; J. Wiesehöfer (eds), <i>Commutatio et Contentio: Studies in the Late Roman, Sasanian, and Early Islamic Near East</i> (Düsseldorf: Wellem, 2010), p. 200; quoted by Hoyland (2014), p. 268 n. 3. <b>Note the clause “discussed here”</b> — Millar is scoping to the corpus he has surveyed, and this book quotes him with the clause intact. <i>Seen through Hoyland’s quotation; the Börm and Wiesehöfer volume has not been obtained.</i> What the Roman sources do use is personal: <i>Arethas son of Gabalas</i>, <i>phylarch</i>, <i>patricius</i>, <span class="ar">Σαρακηνοί</span>.')}.</p>
<p>Think about what that means. The state these people served, in all four of its written languages,
never once called them by the name their descendants now carry. “Ghassanid” comes from the Arabic
family-tree tradition. Later writers, and then modern ones, laid it back over a frontier power of
Roman times.</p>
<p>That does not make the Jafnids imaginary. They are in Procopius, in the inscriptions and in the
ruins at Ruṣāfa. <b>It makes the <i>name</i> a reconstruction.</b></p>
{FIX('“Chabot supplies ‘Ghassanide’ in a nineteenth-century footnote to a text that says <i>Ṭayyāyē</i>” — offered as a worked example of an editor becoming a source.',
 '<b>Withdrawn. The footnote is not there.</b> Chabot’s French translation of Michael the Syrian was searched in full: <b>“Ghassan” and its derivatives occur zero times across all three translated volumes, against 593 occurrences of <i>Taiyayé</i>.</b>',
 'Text and footnotes sit in the same searchable stream, and the vocabulary is plainly being read, so a repeated editorial gloss would have surfaced. <b>The general point survives on Millar, Hoyland and Fisher–Wood; the specific anecdote does not, and is removed rather than softened.</b> <i>The Chronicle of 1234, also edited by Chabot, has not been checked and is where anyone wanting the instance should look.</i>')}
<p>One more limit, and it is an uncomfortable one. The best-known modern case for Ghassanid survival
after the conquest is Irfan Shahîd’s. <i>We have not been able to obtain his volumes, so we cannot
tell the reader what evidence they rest on.</i></p>
<p>We cannot say whether his case rests entirely on Arabic literature of the eleventh to fourteenth
centuries. <b>We could not check it, so we leave the question open</b> until somebody reads
the books{c('Irfan Shahîd, <i>Byzantium and the Arabs in the Sixth Century</i> (Dumbarton Oaks, 1995–2009), 2 vols in 4 parts — not open access, and not obtained by this project. <b>Named here as an outstanding item so that the gap is visible rather than papered over.</b> The critical reviews by Lawrence Conrad and Mark Whittow are the place to begin an audit of his source base.')}.</p>"""),

ent('the name, tested', 'none', False,
    'Five searches and what they prove',
 'We searched for our family’s name, our town’s name and our neighbours’ names in al-Maktaba al-Shāmila, a large digital library of early Arabic writing. <b>We give the results with their controls</b>, test searches for words that must appear. Without a control, a search shows nothing.',
 f"""
{NUMTABLE('AGAINST AL-MAKTABA AL-SHĀMILA',
 ['term', 'hits', 'what it means'],
 [['<span class="ar">الحدادين</span>', '<b>553</b>', 'and <b>effectively every one is the trade</b> — “the blacksmiths.” Only three entries use it as a family name, and all three are twentieth-century compilations. <i>In the pre-modern corpus this word is an occupation.</i>'],
  ['<span class="ar">الكسابرة</span> · <span class="ar">كسبر</span>', '<b>0</b>', 'the name the register of 1553–54 actually gives the group'],
  ['<span class="ar">حلحول</span> <i>(control)</i>', '31', 'a Hebron-hills village — the search reaches Palestinian village names'],
  ['<span class="ar">نوبا</span> <i>(control)</i>', '452', 'another — it reaches them easily'],
  ['<span class="ar">دير غسانة</span>', '<b>0</b>', 'confirmed twice, independently'],
  ['<span class="ar">رام الله</span>', '<b>none pre-modern</b>', 'no attestation of the town in the corpus at all']],
 '<b>Read the controls first.</b> Ḥalḥūl and Nūbā return freely, so the corpus does contain Palestinian villages and the search finds them. <i>Then read Dayr Ghassāna: zero — for a large, real, continuously inhabited throne-village.</i> <b>That single line is the proof that these zeroes are a property of the library, not of the country.</b> Shāmila is a corpus of law, ḥadīth, literature and chronicle. It is not a gazetteer and not a tax register, and a Christian hamlet in the Jerusalem hills is exactly what it would never contain.')}
<p><b>So the three zeroes tell us about the library, not about our family.</b>
Missing from it means missing from one kind of writing, the kind that was never going to record
families like ours. <i>To read these blanks as evidence against our family would be to mistake the
shape of a library for the shape of the past.</i></p>
<p><b>The first line is different, and it does matter.</b> The word <span class="ar">الحدادين</span>,
Ḥaddādīn, appears five hundred and fifty-three times. In almost all of them it does the same job: it
means the men who work iron, the smiths.</p>
<p>So any argument that finds “Ḥaddādīn” in an early Arabic text and reads it as our family is
reading the name of a trade. The register of 1553–54 calls the group the Kasābra. Together these
support what the next entry shows: <b>the family name is late</b>, and we
will not claim it any earlier than we can show it.</p>"""),

ent('the clock', 'none', False,
    'The generation length nobody measured',
 f'''<b>Every number we give that turns years into generations rests on one assumption, and we should
name it.</b> We count the line at sixty-six because nine hundred and thirty-one years divided by
thirty is thirty-one. <b>Thirty is not a measurement.</b> No one has published a father-to-son
generation length for any Middle Eastern population. The standard collection of such studies covers
French Canadians, Icelanders, north Greenland Inuit, the English, and the family tree of
Confucius{c('The ISOGG wiki’s “Generation length” survey, which is the field’s working list: Tremblay &amp; Vézina (2000) on French Canadians, 34.5 years in the male line; Helgason et al. (2003), Iceland, 31.9; Matsumura &amp; Forster (2008), north Greenland Inuit, 32; King &amp; Jobling (2009), England, 35; the Confucius pedigree, China, 32; and a set of British surname projects. <b>No Arab, Levantine or Middle Eastern population appears anywhere on it.</b> <i>The honest claim is that the standard compendium contains no Middle Eastern population — not that no such study exists anywhere on earth.</i>')}.''',
 f"""
<p>The studies of this region’s genes do something else: they assume a figure, and say so. The
figures they assume are at or below the bottom of the range we have been using.</p>
{NUMTABLE('WHAT THE LITERATURE ASSUMES, AND WHAT IT IS ASSUMING IT FOR',
 ['study', 'interval', 'but note'],
 [['Haber et al., <i>PLoS Genetics</i> 9:2 (2013) — the Levant, Palestinians included', '<b>25 years</b>', '<b>autosomal.</b> The 25 calibrates admixture-decay dating, not a male line'],
  ['Fernandes et al., <i>PLoS ONE</i> 10:3 (2015) — Arabia', '<b>25 years</b>', '<b>mitochondrial — the maternal line.</b> It has no bearing on a father-to-son count and this book will not cite it as if it had'],
  ['Haber et al., <i>AJHG</i> 101:2 (2017), with Zalloua — Canaanite and present-day Lebanese', '<b>28 years</b>', 'the closest thing to a regional working figure'],
  ['Zhivotovsky et al., <i>AJHG</i> 74 (2004) — the Y-STR clock itself', '<b>—</b>', '<b>the rate is defined per twenty-five <i>years</i>, not per generation</b>, and the paper offers a per-year conversion. <i>Any date taken from this clock and reported as a number of generations has had an interval smuggled into it.</i>']],
 'Calibrated, in Zhivotovsky’s case, on Maori, Cook Islanders and Bulgarian Roma. <b>Not one of these four studies measured a Middle Eastern father-to-son interval, because none of them set out to.</b>')}
<p><b>So the result is a range.</b> Nine hundred and thirty-one years across the gap gives
twenty-seven generations at thirty-five years each, thirty-one at thirty, thirty-three at
twenty-eight, and thirty-seven at twenty-five.</p>
<p>The whole line from Adam to Rāshid is therefore between sixty-two and seventy-two generations. We
use sixty-six because that is what thirty years gives. <i>Sixty-six is a choice inside a range, not a
fact, and every family ladder in our history should be read that way.</i></p>
<div class="fix"><div class="fixhead">And the evidence this family has been told to go and buy</div>
<div style="font-size:.95rem;line-height:1.65;color:#46423B">
<p style="max-width:none"><b>A Y-chromosome subclade called <span style="white-space:nowrap">J-Z640</span> circulates as
“the Ghassanid marker.” It does not hold up.</b> The one paper on it appeared in 2019, in a
little-known journal. It rests on <b>one hundred and forty-five samples, of which eight are
academic</b>. The rest are customers of two commercial testing firms, whose tribal affiliation is
<b>self-reported</b>{c('M. Waas, D. Yacobi, L. Kull, V. Urasin, G. Magoon, W. Penninx, A. Brown &amp; I. Nogueiro, “Haplogroup J-Z640 — Genetic Insight into the Levantine Bronze Age,” <i>Journal of Phylogenetics &amp; Evolutionary Biology</i> 7:1 (2019), 1000209. First author at the Department of Jewish History, University of Haifa; a co-author is of YFull.com, <b>whose tree then supplies the date the paper is checked against</b> — not misconduct, but not independence either. <b>On the publisher, a precise statement rather than a loose one:</b> OMICS International is on Beall’s list of predatory publishers and was fined by the US Federal Trade Commission; this title is a former OMICS journal now under Hilaris Publishing SRL. <i>This book does not assert that the present publisher is itself listed.</i>')}.</p>
<p style="max-width:none"><b>And the dating rules it out.</b> YFull’s own tree puts the
formation of J-Z640 and its most recent common ancestor at <b>4,600 years before the present</b>, with
a confidence interval of 5,000 to 4,100{c('YFull YTree v14.05.00, J-Z640: formed 4600 ybp, TMRCA 4600 ybp, 95% CI 5000–4100. The paper’s own independent estimate is a TMRCA of 4,100 ybp with a range of 4,900–3,300. <b>An earlier draft of this book gave ~3,600 ybp. That figure was wrong and is corrected here.</b>')}. <b>That is the Bronze Age.</b> It is
two thousand years before any Arab tribal genealogy existed to belong to, and two and a half
thousand before the Jafnids. The paper’s own title says as much: it is a paper about <i>Levantine
Bronze Age</i> ancestry. <i>A marker whose carriers go back to one ancestor twenty centuries before a
people exists cannot be that people’s marker.</i></p>
<p style="max-width:none"><b>And one point of simple fairness to the authors: the paper never says
“Ghassān.”</b> The word does not appear in it, and its own tribal claim — about al-Azd — is expressly
hedged as neither confirmable nor disprovable. <b>The Ghassanid framing comes from the project pages
of a commercial testing service, not from the study.</b> <i>The claim and the paper it is attributed
to are two different objects, and we keep them apart.</i></p></div></div>
<p>Under all of this lies a deeper problem, and it is not about our family. <i>No published study of
ancestry has ever sampled Palestinian Christians as a group of their own.</i>{c('The landmark Y-chromosome study of the population, Nebel et al., “High-resolution Y chromosome haplotypes of Israeli and Palestinian Arabs…,” <i>Human Genetics</i> 107:6 (2000), 630–41 — Hebrew University and Hadassah — is explicit in its own abstract that its 143 subjects are <b>Muslim</b> Arabs. Haber et al. (2013) resolves Lebanese Christians, Muslims and Druze into separate clusters and runs its admixture analysis on each — and then treats Palestinians as a single undifferentiated bloc, lumped with “other Muslim populations as distant as Morocco and Yemen.” <b>Christian Arabs do appear in the Israeli medical-genetics literature as a founder population for disease-allele studies</b> — a recurrent BRCA2 duplication, consanguinity surveys — but that is disease genetics, not ancestry. <i>The only Christian-Palestinian Y-DNA datasets in existence are unpublished citizen-science projects.</i>')} <b>The question
our family would be asking is one the field has never been set up to answer.</b></p>
<p>The field also has a history that explains some of the caution. In 2001 the journal <i>Human
Immunology</i> deleted a paper it had already published on the origins of the Palestinians. It
removed it from its own archive and asked libraries to tear the pages out{c('A. Arnaiz-Villena et al., “The origin of Palestinians and their genetic relatedness with other Mediterranean populations,” <i>Human Immunology</i> 62:9 (2001), 889–900 — withdrawn after publication. Reported in <i>Nature</i> 414 (22 November 2001), “Genetics paper erased from journal over political content”; the editor cited political comment in the text. <b>A rebuttal in <i>Nature</i> 415 (2002), 115, argued the paper was also scientifically weak, and this book prints that alongside rather than presenting the episode as purely political.</b>')}.</p>
<p>Whatever one makes of that, it is why a Palestinian family should come to this field with open
eyes. It is also why <b>we have built our case on registers, deeds and parish books instead</b>.</p>
<p>Our advice is narrower than it once was. Testing the Y-chromosome, which passes from father to
son, would still be the only truly new evidence our history could gain. <i>But it would be worth doing
to build a body of data that does not yet exist, not to confirm a marker that does not mean what it
is said to mean.</i></p>"""),

ent('the shape of the hole', 'documents', False, 'The gap is not our family’s failure',
 'One more thing must be said about the nine hundred years, and it changes what they mean. <b>Our family is recorded right down to the floor of the archive.</b> The registers and court papers that name our people, the Kasābra households whom Ḥammūdeh takes to be Rāshid’s grandchildren, in 1553–54, 1561, 1562, 1565 and 1596, are the <i>first generation of records in which a family of this kind could appear at all</i>, anywhere in Palestine.',
 f"""
<p><b>Think about what would have to exist to fill the gap.</b> Ordinary village families in Bilād
al-Shām, the lands of greater Syria, have no recorded descent before the sixteenth century. The
families that do are not ordinary. They are noble houses with waqf deeds, the papers of religious
endowments. They are church families with the patriarchs’ archives, or monks with notes written into
their manuscripts, or the Jewish merchants of the Cairo Genizah, a store of old papers in a Cairo
synagogue.</p>
<p>There is now a fifth kind, and it is the closest comparison we have. It is the Jerusalem household
of <b>Burhān al-Dīn</b>, a scholar of middling rank in the 1390s. His books and papers survived in the
store of documents at the Ḥaram al-Sharīf, and they can be pieced back together almost item by item:
a library, a list of his estate, a family.</p>
<p><i>He lived a morning’s walk from our ridge, in the very century our own line is silent.</i> What
separates his family from ours is not distance, class or reading and writing. It is that somebody
put his papers in a mosque, and somebody else never threw them away{c('Said Aljoumani &amp; Konrad Hirschler, <i>Owning Books and Preserving Documents in Medieval Jerusalem: The Library of Burhān al-Dīn</i>, Edinburgh Studies in Classical Islamic History and Culture (Edinburgh University Press, 2023) — open access. Same corpus, and largely the same team, as the 2024 study of the Ḥaram documents already cited in this book. '+D('2023_Aljoumani_Hirschler_Owning_Books_Medieval_Jerusalem_EUP.pdf')+'.')}.</p>
<p>For a Christian farming family on a hill ridge, the earliest records we can hope for are the
Ottoman tax surveys. <b>Our family is in them within a generation of the first.</b></p>
<p><i>So the true sentence is not “our line goes dark for nine hundred years.” It is this: the
writing that could have carried our line does not begin until 1525, and we are in it by
1553.</i> <b>The gap is not a gap in our family’s history. It is the depth of the archive.</b></p>[[C29]]
<div class="fix"><div class="fixhead">And the hardest thing the record says about the name</div>
<div style="font-size:.95rem;line-height:1.65;color:#46423B">
<p style="max-width:none"><b>The earliest document that records this community does not call it
al-Ḥaddādīn.</b> The register of 1553–54 that finds the group at Beit Jala calls them the
<b>Kasābra</b>, and lists thirty-six heads of household by first name and father’s name only. <b>No
occurrence of <span class="ar">الحدادين</span> as a family or clan name anywhere in Bilād al-Shām
has been found before the nineteenth century</b>{c('The 1553–54 register of Bayt Jālā names the group <span class="ar">الكسابرة</span> and lists 36 Christian heads of household by given name and patronymic — Ḥammūdeh (2014), 44–45. On the wider search: no pre-1800 occurrence of <span class="ar">الحدادين</span> as a Levantine Christian family name has been established. The earliest documented naming of a Ḥaddādīn clan at Karak reachable in this project is Latin Patriarchate material of the 1870s–80s; the earliest scholarly record is Peake (1934). <b>Corpora still unsearched, and named here so the negative can be tested:</b> the Jerusalem sharīʿa <i>sijillāt</i> from 1529 onward beyond register 48; the Jerusalem sharīʿa <i>sijillāt</i> from 1529 onward beyond register 48; <b>the unpublished folios of the ʿAjlūn <i>mufaṣṣal</i> behind Hütteroth and Abdulfattah’s summary lines</b>; the Ḥaram al-Sharīf corpus; Franciscan and Greek Orthodox parish registers; and Christian Arabic manuscript colophons at Sinai, Jerusalem, Balamand and Dayr al-Mukhalliṣ. <i>A caution: <span class="ar">الحدادين</span> is not a unique name — there is an unrelated group among the Banū Asad in Iraq — so any hit must be shown to be Levantine and Christian before it counts.</i>')}.</p>
<p style="max-width:none"><i>That is not fatal, and it should not be read as such.</i> Occupational
family names of this kind — <span class="ar">الحدّاد</span>, the smith — generally stabilise as
inherited surnames late, and a register that lists men by father’s name is not a register that would
record a clan name even if one existed. <b>But we will not print “the family name, in a tax
register, in the sixteenth century” again, because the sixteenth-century register uses a different
name.</b></p></div></div>
<p>One more caution comes from our family’s own Arabic books. Two clan histories exist in Arabic that
we do not yet hold: <span class="ar">عشائر الحدادين حتى عام ١٩٩١م</span>, and a later
<span class="ar">عشائر الحدادين</span> launched in Amman. The first <b>rejects the blacksmith
meaning of the name</b>. It offers two other origins: <span class="ar">تحديد</span>, the marking
out of the clan’s land in the Shawbak–Karak country, and the Yemeni port of al-Ḥudayda{c('<span class="ar">خلف خليل حدادين ومنير جريس حدادين وعواد جريس حدادين، عشائر الحدادين حتى عام ١٩٩١م</span>, as reported in <span class="ar">الرأي</span>, 27 November 2007. The book is said to reject the blacksmith derivation and to offer <span class="ar">تحديد</span> — the demarcation of the clan’s land at Shawbak and Karak — and descent from the Yemeni port of al-Ḥudayda. The same article records a Karak tradition of <b>two brothers, Ṣabra and Rāshid</b>, which does not appear in the Ramallah tradition and is worth chasing. <i>This project has not obtained either book; both should be acquired.</i>')}.</p>
<p><i>The first is a strained reading of the word, but at least it puts the name on the plateau. The
second cannot carry a sixth-century origin, for the reasons set out in the box below.</i></p>
<p><div class="fix"><div class="fixhead">A correction, and a narrow one</div>
<div class="fixgrid"><div><span class="fl">As it stood</span>“al-Ḥudayda is not a place of any consequence before the Ottoman centuries.”</div>
<div><span class="fl">Corrected to</span><b>al-Ḥudayda existed, and was a constituted place, eighty years before the Ottomans reached Yemen.</b> The Yemeni chronicler <b>Ibn al-Dayba’</b> (d. 944/1537) has a <i>ṣāḥib</i> — a lord — of al-Ḥudayda in <b>Shawwāl 859 / September 1455</b>, and in <b>868/1464</b> has <b>its lord, its qāḍī and its resident ascetic</b> ride out together to meet the Ṭāhirid sultan. Three offices, one town.</div>
<div><span class="fl">How it is justified</span>Ibn al-Dayba’, <span class="ar">قرة العيون بأخبار اليمن الميمون</span>, ed. Muḥammad b. ʿAlī al-Akwaʿ, pp. <b>407</b> and <b>413</b>; the second notice reads <span class="ar">فتوجه إليه صاحب الحديدة وقاضيها وزاهدها الشيخ إدريس الجبرتي</span>, with a plural verb for three separate men. <i>EI</i>² III, 539 gives the same 859/1454–5 notice as the town’s first appearance as an inhabited place, citing al-Dayba’ <b>and</b> Abū Makhrama. <b>But the sentence is only half wrong, and this book will not overcorrect.</b> <i>EI</i>² also says al-Ḥudayda “had not yet any strategic importance” when the Mamluks raided it in 1516, stayed secondary to Mocha through the seventeenth and eighteenth centuries, and rose only in the nineteenth; and al-Akwaʿ’s own note on the 1455 passage calls the place a cluster of huts of reed, straw and brushwood. <b>So: wrong about whether al-Ḥudayda existed, right about whether it mattered.</b> <i>And the etymology fails on other grounds anyway — a man from al-Ḥudayda is a</i> Ḥudaydī, <i>not a</i> Ḥaddād.</div></div></div> Our family’s own historians disagree with each other about where its name comes from,
and that disagreement belongs in our history.</p>
<p><b>What we still don’t know.</b> We have not been able to read Irfan Shahîd’s volumes on Ghassanid
survival, so we cannot say what evidence they rest on. The Syriac Chronicle of 1234 has not yet been checked for the name Ghassān. We do not yet hold the two Arabic histories of
the Ḥaddādīn clans. No published ancestry study has ever sampled Palestinian Christians as a group,
so a Y-chromosome study of our family would be building a body of data that does not yet exist.
Readers who hold any of these, or can help with them, can help us close part of the gap.</p>"""),

CH(11)

sect('And in our own line', 'One name, carried by tradition alone, at the far edge of the void')
ent('about 1500', 'oral', True, 'Rāshid al-Ḥaddādīn',
 f"""Around 1500, the family remembers, our people still lived across the Jordan, at Karak. Within a generation the Ottomans would rule this land and begin counting every household in it. <b>Rāshid al-Ḥaddādīn, generation 66, is the last ancestor our family’s own texts name, and the first whose children a document reaches.</b> He himself is in no register. The earliest Ottoman survey of this district, made in 1525–28, comes a generation after his time. The family chart ends at his name. ʿAzīz Shāhīn, in his Arabic history of the town (1982), prints the family’s two accounts of his road, and then weighs them{c('Shāhīn (1982), ch. 1, printing ʿAdnān al-Ḥaddādīn’s 1953 manuscript account and Joseph Kaddoura’s 1954 account, with his own adjudication.')}.""",
 f"""
<p><b>The Ḥaddādīn account.</b> The family live at Shawbak and Karak among the Kaysoom, the ruling tribes of the plateau. The
tyrant demands a Christian daughter for his Muslim son. Sabra Haddad answers with the unsalted feast,
a meal without salt, which binds no one to keep faith:
<i>“Treachery, O Haddad!”</i> The clan flees by night across al-Lisān, the ford of the Dead Sea, to
Ḥalḥūl, and then to the Beit Jala country.</p>
<p><b>The Kaddoura account.</b> Rāshid is a blacksmith, a <i>ḥaddād</i> in Arabic. He plants forged
blades in the ford, so that the pursuers’ horses turn the water red. He settles first at al-Bireh beside
Sheikh Ṭanāsh. Then he buys the wooded hill next door from the Ghazāwneh, for the sake of kindling for
his forge.</p>
<p>Shāhīn weighs both and decides. The eldest son was named Haddad, and that is where the name
<i>Hadadeh</i> comes from. <b>Sabra was Rāshid’s brother.</b> He returned to Karak, where the Karak
Ḥaddādīn still count themselves his line.</p>
{fig(ATLAS.fig_karak(),'The road the family actually walked',
 'Karak to the ridge in three moves: one documented, one carried by a name, and one by tradition. Bayt Jālā to Ramallah is in the registers name by name; Kusbār is carried by the name al-Kasābra; Karak to Kusbār is the family’s memory alone. The southern anchors are the plateau’s Christian record: Shawbak, Karak, and Gharandal, where Ghassān is named in 890. The northern legs are carried by the Ottoman registers. The tradition’s Ḥalḥūl matches the registers’ Kusbār-by-Ḥalḥūl. The tradition’s Bayt Jālā stage is where the 1553–54 defter, the Ottoman tax register, finds the group. The tradition’s purchase matches endowment land acquiring an owner. Two memories and a tax ledger tell one story in three voices.',
 'Hammoudeh, Jerusalem Quarterly 59 (2014); Hütteroth and Abdulfattah (1977); Piccirillo (2001); al-Yaʿqūbī.')}"""),

ent('1953 · as remembered', 'oral', False, 'What the family remembers',
 f"""<b>In 1953 the town sent two teachers across the Jordan to ask the Ḥaddādīn where Ramallah came from.</b> Mayor Dr Jalīl Badrān sent Khalīl Abū Rayya and ʿAbdallah Mogannam. They came back with ʿAdnān al-Ḥaddādīn’s written account, which is still on file at Ramallah city hall{c('Naseeb Shaheen, <i>A Pictorial History of Ramallah, Part II</i> (Birzeit University Press, 2005), ch. 1, p. 10. Shaheen says the ʿAdnān and Kaddoura accounts in his chapters 2–3 are taken from ʿAzeez Shāhīn’s book of the family trees (1982).')}. Everything here is our family’s own memory, and we give it as memory.""",
 f"""
<p><b>Ṣabra had three brothers.</b> In ʿAdnān’s account the brothers come down from Karak together.
They stop six months at Ḥalḥūl, then settle in the Beit Jala and Bethlehem country. Rāshid stays in
Ramallah. A second brother stays in Beit Jala. The third goes to al-Salṭ, “where his offspring, the
Haddadeen, remain until this day.”</p>
<p>Their Muslim neighbours from the south, the seven brothers of al-Banawiyya under one Ḥusayn, settle
beside them at al-Bireh. After six years Ṣabra goes home to
Karak{c('N. Shaheen (2005), ch. 2, pp. 13–16, printing ʿAdnān al-Ḥaddādīn’s account dated 8 August 1953. The Bayt Jālā and al-Salṭ brothers are not named.')}.</p>
<p><b>The daughter the whole flight was about stays in the story.</b> “An Egyptian Christian named
Haleesa came as a refugee to Sabra. Sabra gave him his daughter as a bride (the daughter that was the
center of the dispute), along with one-third of his property. From them descended the Halasa
clan, which still lives in Karak”{c('N. Shaheen (2005), ch. 2, p. 16. A separate Karak list gives the same origin for el-Ḥalasa — an Egyptian who married a girl of the Ḥaddādīn — see the Karak clan table in this chapter.')}.</p>
<p>In 1892 the Ḥaddādīn and Ḥalasa moved from Karak to the village of Maʿīn. After four years the
Ḥalasa and some Ḥaddādīn went back. The rest settled at el-ʿAzeeyyeh, where they numbered “over
800 souls by 1953”{c('N. Shaheen (2005), ch. 2, p. 16. The move to Mādabā in 1882 that the same page records was by other Karak Christian families — al-ʿAzāzāt, al-Karādsha and al-Maʿāyʿa — not the Ḥaddādīn.')}.</p>
<p><b>Kaddoura remembers the land.</b> In his version it is Sheikh Ṭanāsh of Karak who flees with
Rāshid and becomes the father of the Ḥusayn clan at al-Bireh. Rāshid buys the hill of Ramallah from
the Ghazāwneh, “the original Bireh natives.” He goes back to Karak and leaves his five sons, who
divide the land in fifths, as the next chapter tells{c('Joseph Kaddoura, <i>History of the City of Ramallah</i> (New York, 1954), as printed in N. Shaheen (2005), ch. 3, pp. 17–18. Shaheen notes where Kaddoura differs from ʿAdnān: the girl is Rāshid’s daughter, Rāshid returns to Karak, and Ṣabra is Rāshid’s son. The two accounts name different founders for the Ḥusayn clan of al-Bīra — al-Banawiyya’s Ḥusayn or Sheikh Ṭanāsh.')}.</p>
<p>Abū Rayya also wrote down what he was told at Maʿīn.</p>
<blockquote><span class="ar">لما ذهبت إلى قرية ماعين في شرقي الأردن عام ١٩٥٣ م للبحث عن أصل سكان رام الله، اجتمعنا
مع وجوه الحدادين ومعمريهم، فأطلعونا على شجرة عائلة الحدادين المنحدرين من شيخ صبرة، فلم أر لأي من أبناء
صبرة اسماً ينطبق على اسم أي من جدود حمائل رام الله الخمس، وقالوا لنا أن حدادي شرقي الأردن هم أبناء صبرة،
ونحن في رام الله أولاد راشد أخ صبرة</span><br>
“When I went to the village of Maʿīn in Transjordan in 1953 to look for the origin of Ramallah’s
people, we met the notables and elders of the Ḥaddādīn. They showed us the family tree of the
Ḥaddādīn descended from Shaykh Ṣabra, and I saw no name among Ṣabra’s sons that matched any ancestor
of Ramallah’s five clans. They told us that the Ḥaddādīn of Transjordan are <b>the sons of Ṣabra</b>,
and we in Ramallah are <b>the sons of Rāshid, brother of Ṣabra</b>.”
<span class="cite">Khalīl Abū Rayya, <i>Rām Allāh qadīman wa-ḥadīthan</i>, pp. 14–15, quoted in <i>Qiṣṣat madīnat Rām Allāh wa-l-Bīra</i> (ALECSO and the PLO, “Palestinian Cities” series), p. 24{c('<i>Qiṣṣat madīnat Rām Allāh wa-l-Bīra</i>, p. 24, citing Abū Rayya pp. 14–15; the same page cites Dissard, <i>Revue Biblique</i> 1905. The author and year of the ALECSO volume are not on the copy this project holds.')}</span></blockquote>
<p><b>The oldest printed telling is French, and it comes from Karak.</b> In January 1905 J. Dissard,
a priest of the Latin Patriarchate, read a lecture at the École biblique in Jerusalem on the Bedouin
of Moab. Into it he put the story the Christians of Karak told him.</p>
<p>“The little tribe of Ḥaddādīn is made up of a number of families, exclusively Christian.” A man of
the tribe named Rcheid, that is Rāshid, promised his newborn daughter in jest to the Muslim chief
Diāb. Years later Diāb came to claim her for his son. Rāshid asked for “a few days to make my
daughter a complete trousseau.” He was “a blacksmith by trade,” and he forged a great quantity of
blades.</p>
<p>The Ḥaddādīn fled west down the valley to the Ghōr al-Ṣāfī and crossed at the little ford at the
tip of al-Lisān. Rāshid planted the blades in the ford, where Diāb’s horsemen were cut to pieces.
“Rcheid and his people lived near Hebron for some years. He afterwards had <b>five sons who founded
lines, and who are the ancestors of part of the present Christians of Ramallah</b>. As for the
father, he went back to Karak with part of his tribe after Diāb’s
death”{c('J. Dissard, “Les migrations et les vicissitudes de la tribu des ʿAmer,” <i>Revue Biblique</i> n.s. 2 (14) (1905), pp. 410–425, at pp. 419–421; lecture read at the École biblique de Saint-Étienne, 18 January 1905; the author is styled “du Clergé de Jérusalem.” Read in the archive.org scan of vol. 14 (item revuebiblique1419unse); the printed page numbers are inferred from the scan leaves.')}.</p>
<p>Dissard puts the episode “about 1815.” That cannot be right for Ramallah, because the Ottoman
registers count the Christian families on this hill in 1562. What Dissard keeps is the shape of the
story, told at Karak seventy years before Kaddoura wrote it down in New York: the forge, the blades
in the ford, the five sons, and the father going home.</p>
<p>So the family’s tellings, written down on both sides of the river, keep the same shape: brothers
left Karak together, and one went back. <b>The registers do not name them, and they correct the
dates.</b></p>"""),

ent('1005 / 1596', 'documents', False,
    'Karak was a Christian town',
 f'''The Ottoman survey of 1596 counts al-Karak, and the numbers run the other way from what our family
had long assumed about the town we came from. It was not a small remnant under pressure. The survey
lists <b>one hundred and three Christian households against seventy-eight Muslim</b>, with eight
Christian bachelors and two Muslim. That makes a hundred and eighty-one households, of which
fifty-seven in every hundred are Christian{c('Hütteroth &amp; Abdulfattah, <i>Historical Geography of Palestine, Transjordan and Southern Syria in the Late 16th Century</i> (Erlangen, 1977), <b>p. 171</b>, from the <i>mufaṣṣal</i> of liwāʾ ʿAjlūn, 1005/1596. <b>Karak in this survey is not its own liwāʾ</b> — it is the <i>nāḥiya</i> of al-Karak inside liwāʾ ʿAjlūn, alongside the nāḥiyas of Jibāl al-Karak and al-Shawbak; <i>the register was published by Muḥammad ʿAdnān al-Bakhīt and Nūfān Rajā al-Ḥamūd at Amman.</i> <b>This project has not yet seen p. 171 with its own eyes, and says so.</b> The figures are confirmed to the unit by an independent route: Khalīf Muṣṭafā Gharāybeh, working from the same volume, totals al-Karak at <b>191</b> — which is 78 + 2 + 103 + 8 — and his method checks out against three other entries (al-Shawbak 70, al-Ṭafīla 33, al-Salṭ 70). ' + D('1977_Hutteroth_Abdulfattah_Historical_Geography_Palestine_Transjordan.pdf') + '.')}.''',
 f"""
{FIX('“The Karak and Shawbak <i>tahrir defterleri</i> are not in Hütteroth and Abdulfattah” — printed in this book as a list of corpora still unsearched.',
 '<b>They are, and this book should have known it.</b> Karak and Shawbak are <i>nāḥiyas</i> of liwāʾ ʿAjlūn in the survey of 1596, and their settlements are in the gazetteer at pp. 169–173 like everybody else’s.',
 'The error came of assuming a liwāʾ of Karak-Shawbak because a <i>sanjaqbey</i> of Karak-Shawbak existed as a military office. <b>The political command and the fiscal survey unit were not the same thing.</b> <i>The correction costs this book a line of alibi and gains it a page of evidence.</i>')}
<p><b>First, a caution.</b> A <i>tahrir</i>, an Ottoman tax survey, counts taxable households, not
people. The castle garrison, the officials and soldiers, and everyone exempt are left out. And
“Christian” here is a tax category: the <span class="ar">نصارى</span> who paid the poll tax. It is
not a census of belief. So the careful phrase is “a Christian majority of the taxable households in
the register of 1596,” and we do not shorten it to “a Christian town” anywhere it matters.</p>
<p><b>The Mamluk chroniclers said the same three centuries earlier.</b> In 1301 (700 AH) Cairo ordered
the Christians of the realm into blue turbans and the Jews into yellow. At Karak the order was not
carried out. Al-Nuwayrī served the same state and wrote within a generation. He records the excuse
that was made for them: <span class="ar">أهل الكرك نصارى وأن
المسلمين بها قليل</span>, <i>“the people of Karak are Christians, and the Muslims there are
few.”</i> Marking them, it was said, would show strangers how many they were. “And so it remained at
Karak and Shawbak to this day.”{c('Al-Nuwayrī, <i>Nihāyat al-arab fī funūn al-adab</i> XXXI, pp. 418–419: <span class="ar">أهل الكرك نصارى وأن المسلمين بها قليل</span> … <span class="ar">فاستقر ذلك بالكرك والشوبك إلى الآن</span>. Al-Maqrīzī, <i>al-Sulūk</i>, ed. Ziyāda, I/3, p. 912 (= ed. ʿAṭā, II, p. 339): <span class="ar">اعتذر بأن أكثر أهل الكرك نصارى … فلم يغيّر أهل الكرك والشوبك من النصارى العمائم البيض</span>. <b>Cite Ziyāda, not ʿAṭā:</b> Ziyāda marks the part of the sentence he restores from al-Nuwayrī, and the name of the official who made the excuse is not secure. Read in the printed editions for this book, 6 October 2026.')}
A Mamluk official, three hundred years before the Ottoman clerk, saw the same picture.</p>
<p>The 1596 figure stands apart from every later count. The table sets them side by side.</p>
{NUMTABLE('THE CHRISTIAN SHARE AT KARAK, 1596 TO 1961',
 ['when', 'who counted', 'what they found', 'share'],
 [['<b>1596</b>', 'the Ottoman <i>mufaṣṣal</i>', '<b>103 Christian households · 78 Muslim</b>', '<b>~57%</b>'],
  ['1806', 'Seetzen, on the spot', '70–80 Christian houses · 120 Muslim; four mills held jointly', '~37–40%'],
  ['1812', 'Burckhardt, on the spot', '150 Christian families · 400 “Turkish”', '~27%'],
  ['1818', 'Irby &amp; Mangles, on the spot', '“about as many Christian inhabitants as Turks”; 400 armed men', '~50%'],
  ['1872', 'Tristram, reporting hearsay', '8,000 of whom 1,600 Christian — and he says the town was empty when he came', '20%'],
  ['1895–96', 'Hill, for the Palestine Exploration Fund', '8,000 Muslim · 2,000 Greek Orthodox, town and district', '20%'],
  ['1896–1902', 'Musil, clan by clan', 'about 1,140 families; <i>en-Naṣāra</i> 200 within one faction', '~18%, <i>and probably an undercount</i>'],
  ['1961', 'the Jordanian census', '7,422 persons · 1,622 Orthodox', '22%']],
 '<b>Nothing after 1596 corroborates a Christian majority.</b> The nearest is Irby and Mangles at parity. <i>What the series does show is a large, stable and strikingly secure Christian community</i> — a fifth to two-fifths of the town for two hundred years, armed on the same terms as its Muslim neighbours, which both Burckhardt and Irby stress independently and with some surprise. <b>So print the 1596 majority, and do not let it imply continuity with the community the travellers met.</b>')}
<p><b>One sentence of Burckhardt’s runs the family’s road backwards.</b> Of the Karak Christians he
writes that they are “for the greater part, descendants of refugees from Jerusalem, Bethlehem, and
Beit Djade,” that is, Bayt
Jālā{c('J. L. Burckhardt, <i>Travels in Syria and the Holy Land</i> (London: John Murray, 1822), <b>p. 381</b>, from his stay at Karak in July–August 1812. The same sentence continues on the Muslims: “settlers from all parts of southern Syria, but principally from the mountains about Hebron and Nablous.” <b>Bayt Jālā is the stage the family’s own tradition puts between Karak and this ridge.</b>')}.</p>
<p>Our tradition has the family leaving Karak for Beit Jala. Burckhardt has the Christians of Karak
arriving from Beit Jala. The roads have the same two ends and run in opposite directions, and
<b>nothing in either record says they cannot both have been travelled</b>. Christian families on this
plateau moved in both directions for centuries. A tradition of flight out and a report of refuge in
do not contradict each other. Until now our story has told only one of them.</p>"""),

ent('1908', 'oral', False,
    'Musil asked them himself',
 f'''<b>Alois Musil did one thing nobody else did: he went round the family lines of Karak and asked
each one where it came from.</b> He opens the section simply: <i>“most of the lineages,
</i><span class="ar">حمايل</span><i>, of the fellāḥīn of el-Kerak are, according to their own family
tradition, immigrants from elsewhere”</i>. The <i>ḥamāyil</i> are the family lines, and the
<i>fellāḥīn</i> are the farmers. Then he prints the answers in a table{c('Alois Musil, <i>Arabia Petraea, III. Band: Ethnologischer Reisebericht</i> (Vienna: Kaiserliche Akademie der Wissenschaften, 1908), section <b>El-Kerak</b>, <b>pp. 84–85</b>; the Christian clan list at <b>p. 99</b>. Fieldwork of 1896–1902. Opening sentence: „Die meisten Geschlechter, ḥamâjel, der Fellâḥîn von el-Kerak sind ihrer Familientradition nach von andersher eingewandert.“')}.
The Ḥaddādīn line reads: <i>El-Ḥaddâdîn, stammen aus <span style="white-space:nowrap">ḫ.
el-Ḥaddâd</span></i>, “they come from Khirbet al-Ḥaddād.” <i>A ruin. Not a country, and not
Palestine.</i>''',
 f"""
{FIX('This project’s own first reading of the page: “the Karak Ḥaddādīn said they came from <i>b. el-Ḥaddād</i> — a lineage name, Banū al-Ḥaddād.”',
 '<b><span class="ar">ḫ.</span> not <span class="ar">b.</span></b> — Musil’s abbreviation for <i>ḫirbe</i>, a ruin-site. <b>The answer is a place-name: Khirbet al-Ḥaddād.</b>',
 'The page was rendered at 500 dots per inch to settle it; two separate machine transcriptions of the volume had both misread the character. The same glyph stands in <i>el-Ḫalîl</i> — الخليل, Hebron — two lines below, against the visibly different <i>Ḥ</i> in <i>el-Ḥaddâd</i> itself. <b>The correction strengthens the finding rather than weakening it:</b> a lineage name is a claim about ancestry, and a ruin is a claim about ground.')}
<p><b>And the ruin can be found.</b> Musil’s own first volume walks past it. One stage of his journey
runs <i>“from Ǧaʿfar to ḫ. el-Ḥaddâde”</i> and the next <i>“from ḫ. el-Ḥaddâde to Mâdaba.”</i> In this
volume Musil spells the name el-Ḥaddâde, with a final vowel. The site
lies south of Khirbet Abū Ḥammūr, on the wadi that drains the el-Feǧǧ hollow. <b>From there, he notes,
the fortress of Karak is in sight</b>{c('Musil, <i>Arabia Petraea</i> I (<i>Moab</i>), itinerary stages at pp. 366 and 369, with the topography in the body of the volume. <b>One caution, and it is real:</b> volume III writes <i>el-Ḥaddâd</i> and volume I writes <i>el-Ḥaddâde</i>. The identification is highly probable and one vowel short of certain, and this project could not corroborate it in any modern gazetteer.')}.</p>
<p><i>So the Ḥaddādīn of Karak told Musil they came from a ruin on their own plateau, within sight of
their own castle.</i></p>
<p>Now look at the whole table, because the pattern is what matters.</p>
{NUMTABLE('WHAT EACH KARAK LINEAGE TOLD MUSIL, 1896–1902',
 ['lineage', 'where they said they came from'],
 [['<b>el-Ḥaddâdîn</b>', '<b>ḫ. el-Ḥaddâd — a ruin on the Karak plateau</b>'],
  ['el-Maʿâjṭa', '<b>ǧ. el-Ḫalîl — the Hebron highlands</b>'],
  ['eḍ-Ḍmûr', '<b>el-Ḫalîl and Beni Nâjem — Hebron and Bani Naʿim</b>'],
  ['el-Ḥalasa', 'Egypt; the ancestor settled at Kerak, <i>married a girl of the Ḥaddādīn</i>, and founded a new lineage'],
  ['el-Heǧâzîn', 'the Ḥijāz'],
  ['ez-Zrêḳat · el-ʿAkaše · eṭ-Ṭarâwne', 'ḫ. el-Mḫêlle, east of Wādī Mūsā'],
  ['el-ʿAzêzât', 'Mōte — Muʾta, on the plateau'],
  ['el-Mdânât', 'Middīn'],
  ['el-Bḳâʿîn', 'el-Beqʿe'],
  ['eṣ-Ṣunnâʿ', 'merchants of Damascus — “originally Greek Catholic, later gone over to the schism”'],
  ['as-Serâjre · el-Ḥabâšne', 'ḫ. ez-Zuṭṭ · ḫ. Ḥbêš'],
  ['el-Aṛawât · aṭ-Ṭanâšât · el-Mḫâmîd', 'old lineages, come centuries ago, <i>“who built the town”</i>'],
  ['el-Ḳdaʾ · el-Bašâbše', '<b>the original inhabitants of el-Kerak</b>']],
 '<b>Read the third column of Musil’s Christians.</b> He names eight Christian clans at p. 99 — Ḥalasāʾ, Ḥegāzīn, ʿAkāse, <b>Ḥaddādīn</b>, Mdānāt, Zrejkāt, Ṣunnāʿ, Beqāʿīn — and gives every one of them a non-Palestinian origin: Egypt, the Ḥijāz, Muʾta, Khirbet Mkhēlle, Middīn, el-Beqʿe, Damascus, Khirbet al-Ḥaddād. <i>Jerusalem, Bethlehem and Bayt Jālā appear nowhere in the list.</i>')}
<p>This puts Musil and Burckhardt on opposite sides of the same question, and here we must be
careful. Musil’s traditions <i>agree</i> with Burckhardt on the Muslim clans. The Maʿāyṭa come from the
Hebron highlands, and the Ḍmūr from Hebron and Bani Naʿim, exactly the “mountains about Hebron and
Nablous” Burckhardt names.</p>
<p><b>They disagree with him on the Christians at every single entry.</b> <i>But Musil never cites
Burckhardt, never mentions him, and is not arguing with him</i>{c('The whole of <i>Arabia Petraea</i> III was searched for <i>Burckhardt</i>, <i>Seetzen</i>, <i>Doughty</i> and <i>Travels in Syria</i>: not one occurrence. Volume III is a report of oral tradition collected in the field, with no engagement with earlier travellers at all. <b>So this is divergence between two independently gathered bodies of evidence, not a correction of one man by another</b>, and it must be written that way.')}.
Two men asked, ninety-six years apart, and got different answers. That tells us about the evidence.
It is not a judgement on either man.</p>
{NUMTABLE('FOUR ACCOUNTS OF WHERE THE ḤADDĀDĪN CAME FROM',
 ['account', 'the road it describes', 'when and how it was collected'],
 [['<b>Ramallah’s own tradition</b>', 'Ghassanid Christians, flight from Karak north to this ridge', 'written down 1953 and 1954 from family memory; printed by Shāhīn 1982'],
  ['<b>Burckhardt, 1812</b>', '<b>the opposite direction</b> — the Karak Christians are refugees <i>from</i> Jerusalem, Bethlehem and Bayt Jālā', 'a traveller’s report of local information, on the spot'],
  ['<b>Musil, 1896–1902</b>', '<b>no road at all</b> — the Ḥaddādīn come from a ruin on the Karak plateau itself', 'asked of each lineage in the field and tabulated, published 1908'],
  ['<b>The Karak diwan, 2022</b>', 'Rāshid and his brother Ṣabra go <i>from</i> Karak; Ṣabra returns', 'the Karak family’s own printed statement, at a reception for the Ramallah delegation']],
 '<b>These do not reconcile, and this book will not make them.</b> Two say the family left Karak; one says the Karak Christians arrived from the Bayt Jālā country; one says the Ḥaddādīn never came from anywhere but the next valley. <i>Printed as four, with the date and the method of collection attached to each, they are more use to a reader than any one of them smoothed into a story.</i>')}
<p><i>Notice what all four accounts share.</i> <b>Every account agrees that the Ḥaddādīn were at Karak,
were Christian, and were many enough to need an explanation.</b> What none of them can settle is
which way they travelled.</p>
<p>Our family’s memory of a road is older and more detailed than anything that contradicts it. It
remains the reading we follow, with three other readings now standing beside it, as they should.</p>"""),

ent('three names above Rāshid', 'oral', False, 'Who was Rāshid’s father?',
 'For years we worked from the Mogannam chart, which ends at row 36 (generation 66 in our recount). All along it has carried <b>three more names, inside that row’s own title</b>, and until now we never spelled them out. John Mogannam writes it in full: <b>Rāshid bin Essaye bin Eyad bin Dhahdouheh al-Ghassani</b>, <span class="ar">راشد بن عيسى بن عياد بن ضهدوحة الغساني</span>{}.'.format(c('John Aziz Mogannam, chart of thirty-six named generations, generation 36, given in full as “Rashed bin Essaye bin Eyad bin Dhahdouheh al-Ghassani.” <b>Earlier editions of this book reproduced the chart as a data table and shortened this to “Rāshid,” silently discarding three named ancestors.</b>')),
 f"""
<p>So on the Ramallah side the answer is this. Rāshid’s father was <b>ʿĪsā</b>, his grandfather
ʿIyād, and his great-grandfather Ḍahdūḥa. <i>These three generations were printed on every copy of
the chart, and never once read out.</i></p>
<p><b>On the Karak side the answer is different.</b> The diwan, the family council, of the Ḥaddādīn
of Karak says it in print, and says it about itself:</p>
<blockquote><span class="ar">راشد بن صقر الحدادين وأبناؤه ونسله، وكان قدم إليها مع شقيقه صبرة بن صقر
الحدادين من الكرك… وما لبث صبرة أن عاد إلى قواعده في الكرك</span><br>
“Rāshid <b>son of Ṣaqr</b> al-Ḥaddādīn and his sons and his line — he came to it with <b>his brother
Ṣabra son of Ṣaqr</b> al-Ḥaddādīn from al-Karak… and before long Ṣabra returned to his bases in
al-Karak.”
<span class="cite">The Karak Ḥaddādīn diwan, at a reception given for the Ramallah municipal
delegation, August 2022{c('<i>ʿAmmūn News</i> (Amman), 30 August 2022, reporting a reception given by Dr Munther Haddadin at his home in Dābūq for the Ramallah municipal delegation led by Mayor ʿĪsā Rajāʾ Qassīs. <b>The name Ṣaqr is in print in the Karak tradition from Abū Rayya (1980) onward; this report is its fullest statement, not its earliest.</b> The same report says Ramallah was built “over five centuries,” which would place the founding about 1520 — and which contradicts a 1561 floruit for Rāshid’s father.')}</span></blockquote>
<p>Two things in that sentence are a real gain, and we should say so first. The Karak side, speaking
about itself and without prompting from Ramallah, confirms that <b>Ṣabra was Rāshid’s brother and not
his son</b>. That settles an old disagreement in Shāhīn’s favour against
Kaddoura. It also confirms that Ṣabra went back.</p>
<p><i>The two ends of the tradition were written down separately, on opposite sides of the Jordan, and
they tell the same story about the same two men.</i></p>
<div class="fix"><div class="fixhead">And then they name different fathers</div>
<div class="fixgrid">
<div><span class="fl">Ramallah says</span>Rāshid <b>bin ʿĪsā</b> bin ʿIyād bin Ḍahdūḥa — the
Mogannam chart, row 36 (generation 66 in our recount).</div>
<div><span class="fl">Karak says</span>Rāshid <b>bin Ṣaqr</b>, brother of Ṣabra bin Ṣaqr. <b>This is
not a 2022 novelty.</b> Ḥammūdeh prints <i>Rāshid bin Ṣaqir al-Ḥaddādīn</i> in 2014, on the authority
of <b>Khalīl Abū Rayya (1980)</b>; the Karak diwan is the fullest statement of it, not the
first.</div>
<div><span class="fl">What we do</span><b>We enter Ṣaqr at generation sixty-five</b> and
print ʿĪsā beside him, because the wheel that carries Ṣaqr agrees with Ramallah on four other points
and our own chart’s three names agree with nobody. <i>It is our best judgement, and we will change it
if a document says otherwise.</i> <b>ʿIyād and Ḍahdūḥa have no independent attestation anywhere</b> — <span class="ar">ضهدوحة</span> returns nothing
at all as a personal name, and its shape is that of a Levantine nickname rather than a given name;
it may be a copying slide from the well-known Christian name <span class="ar">الدحداح</span>. <b>And
Ṣaqr is not attested in any <i>document</i> at all</b> — not in Peake, not in Kaḥḥāla, not in any
Ottoman register. He is well attested in the Arabic family literature from Abū Rayya (1980) onward,
<i>which is why he is drawn in a broken outline on every ladder in our history: named by the tradition,
named by nobody’s clerk.</i>{c('Checked and negative for both names: F. G. Peake, <i>History and Tribes of Trans-Jordan</i> ii, the Karak clan tables; Kaḥḥāla, <span class="ar">معجم قبائل العرب</span>, s.v. <span class="ar">الحدادين</span>; the Jordanian clan registers, which all carry one recycled sentence from Peake and no genealogy; and <span class="ar">الرأي</span>, 27 November 2007, digesting <span class="ar">عشائر الحدادين حتى عام ١٩٩١م</span> — which uses no date between the seventh century and 1937. On <span class="ar">عياد</span>: an ordinary and well-attested Levantine Christian name, from <span class="ar">عيد</span> — its very ordinariness argues mildly for authenticity, since nobody inserts it for prestige.')}</div>
</div></div>
<div class="fix"><div class="fixhead">One reading that would make both traditions right</div>
<div style="font-size:.95rem;line-height:1.65;color:#46423B">
<p style="max-width:none"><b><span class="ar">صقر</span> — “falcon” — is a byname, not a baptismal
name.</b> No Christian of sixteenth-century Karak was christened Ṣaqr. Levantine men of this period
routinely carry a given name and a byname. A family diwan on the east bank is exactly the kind of
memory that keeps the byname and loses the given name. A genealogy written in Ramallah is exactly
the kind that does the opposite. <b>If Ṣaqr and ʿĪsā are one man, both traditions are
right</b> — and generation sixty-five is <i>ʿĪsā, called Ṣaqr</i>.</p>
<p style="max-width:none"><i>We cannot prove that and do not assert it.</i> It is set down
because it could be checked: a single Karak or Ramallah document giving both names together would settle
it, and because it is the only reading yet proposed under which nobody in this argument is wrong.
<b>This is only a guess, and we do not add it to the ladder.</b></p></div></div>
<div class="fix"><div class="fixhead">The date at the centre of the Karak chart cannot mean what it looks like</div>
<div style="font-size:.95rem;line-height:1.65;color:#46423B">
<p style="max-width:none">The radial chart reproduced in the family’s own presentation carries
<b><span class="ar">صقر — عام ١٥٦١</span></b> at its hub. <i>Read as Ṣaqr’s lifetime, that is
impossible on the family’s own evidence.</i> <b>Ṣaqr is Rāshid’s father. Rāshid’s grandchildren
brought the Kasābra up the ridge road in 1562, with forty-four further Christian households behind
them.</b> A father cannot flourish in
1561 and have great-grandchildren settling the hill the following year.</p>
<p style="max-width:none"><b>It lands on a document.</b> On <b>1 April 1561</b> three men of this
community — Ghunaym bin Sālim <i>al-Kasbūrī</i>, Mūsā bin Baraka and Isḥāq bin Yaʿqūb — stand in a
Jerusalem court and swear to plough this hill, and the qāḍī divides Ramallah in thirds between them
and the Muslim householders. <i>A hub date sitting exactly on the earliest document in which these
families can be found is a document date, or a compiler’s back-count from one — not a birth
year.</i> There is no apparatus in Ottoman Karak that could produce a birth year for a
Christian villager of the 1500s. <b>We print 1561 as a date we cannot yet explain, and we will
not enter it as a lifetime.</b></p>
<p style="max-width:none"><b>What the rest of that chart does say is the subject of the next
entry</b> — and it is a good deal better than a caution. Read outward from the hub, as a radial
genealogy is meant to be read, the Karak wheel is coherent, it is generous to Ramallah, and on four
separate points it says what Ramallah says.</p></div></div>"""),

ent('the Karak wheel, read outward', 'oral', True, 'The Karak chart, read outward',
 f"""The family chart kept on the Karak side is drawn as a wheel. <b>Ṣaqr sits at the hub, and each
ring outward is one generation further down.</b> Read that way, the way it was drawn, it is not a
rival to Ramallah’s account. <b>It is a second copy of it, kept for four hundred years on the other
side of the Jordan.</b>{c('<b>Munther Haddadin, <span class="ar">دولة الغساسنة؛ أصيلها ورحيلها</span> [<i>The Ghassanid State: Its Origin and Its Departure</i>] (Amman: <span class="ar">دار ورد الأردنية للنشر والتوزيع</span> / Dār Ward al-Urduniyya, 2024), ISBN 978-9923-76-975-1</b> — the radial chart of the El-Ḥaddādīn clan of al-Karak, plate 84: about one hundred and sixty names in six hand-drawn rings, with the compiler’s own line picked out in green. Reproduced in the family presentation of 2026, which is where this project first met it. <i>The presentation’s English caption — “El-Haddadeen Tribe, Origins and Branches, Warda Books, 2025” — is a loose rendering of that book, not a second book: “Warda Books” is <span class="ar">دار ورد</span>, and the year is one out.</i>')}""",
 f"""
{fig(F4.fig_karak_wheel(),'The Karak wheel, redrawn — what it says about Rāshid',
 'The hub of the Karak chart, set straight so that it can be read. <b>Ṣaqr has two sons. One keeps Karak and the diwan traces his line to the present day; one goes to Ramallah, and the chart writes the destination under his name, records his five sons, and stops.</b> That is not the shape of a chart trying to annex somebody else’s ancestor. It is the shape of a family recording where its brother went.',
 'Redrawn from the radial chart, plate 84; the outer rings, which carry the modern Karak clan, are summarised rather than transcribed.')}
<div class="fix"><div class="fixhead">A correction to this book, printed before the gain</div>
<div style="font-size:.95rem;line-height:1.65;color:#46423B">
<p style="max-width:none">An earlier state of this chapter said of the Karak chart that <i>&ldquo;its
inner ring carries ʿĪsā, Jiryis, Mūsā and Sālim as Rāshid’s peers,&rdquo;</i> and concluded that it
was <i>&ldquo;either read in the wrong direction, or two stocks joined at a convenient
name.&rdquo;</i> <b>That was this book misreading a chart, not the chart being wrong.</b> ʿĪsā,
Jiryis, Mūsā and Sālim are not Rāshid’s peers. They are <b>Ṣabra’s descendants in Karak</b> — the
fourth, fifth, sixth and seventh names outward along the branch that stayed. The wheel reads outward
from the hub, correctly, all the way round. <i>The reading is withdrawn in full.</i></p></div></div>
<p>So what does the wheel tell us about Rāshid? It says four things that Ramallah says too, and there
is one point on which the two sides part.</p>
<div class="fix"><div class="fixhead">Where Karak and Ramallah agree</div>
<div class="fixgrid">
<div><span class="fl">His brother</span>Ṣabra is Rāshid’s <b>brother</b>, and Ṣabra <b>went back</b>.
John Mogannam argued his way to exactly this against Kaddoura — <i>&ldquo;Sabra must have been
Rashed’s brother&rdquo;</i> — from Ramallah, without the Karak chart in front of him.{c('John Aziz Mogannam, <i>The Ramallah Family Tree Book</i>, ch. 2, p. 18: “Second, it appears that Sabra Haddad was the one who returned to Karak… all the Haddadeen in Karak claim that they are descended from Sabra… Sabra must have been Rashed’s brother.” Kaddoura, <i>Taʾrīkh Rām Allāh</i>, makes Ṣabra Rāshid’s <i>son</i> and puts him at the head of the five. <b>The Karak wheel settles it three to one.</b>')}</div>
<div><span class="fl">His five sons</span><b>Ḥaddād, Ibrāhīm, Jiryis, Shuqayr, Ḥassān</b> — the same
five sons, in the same order, as the Ramallah tradition’s own division of the land into
fifths. The Karak wheel writes the fifth as Ḥasan (<span class="ar">حسن</span>).{c('The Karak wheel, inner arc below Rāshid: <span class="ar">حداد · ابراهيم · جريس · شقير · حسن</span>. Mogannam, p. 18: “the children of Rashed Haddad were five: Haddad, Ibrahim, Jirius, Shukair, and Hassaan,” and ch. 8 for the clan chart built on them. Karak writes <span class="ar">حسن</span>, Ḥasan; Ramallah, Shāhīn and the registers of 1553 and 1562 write <span class="ar">حسان</span>, Ḥassān. These are two different names, not two spellings of one.')}</div>
<div><span class="fl">Where he went</span>The chart writes <span class="ar">رام الله</span> under his
name. <i>The Karak side records the destination.</i></div>
<div><span class="fl">That the line ends there</span>Rāshid’s branch stops at the five sons. A chart
written to claim Ramallah would have carried it on; this one lets it go and keeps counting its
own.</div>
</div></div>
<p>Set this beside the two fathers in “Who was Rāshid’s father?” just before. On his brother, his
sons, where he went and the way the family parted, <b>the two traditions agree</b>. They agree
separately, in two languages, on two sides of the Jordan.</p>
<p>They disagree on exactly one thing: his father. On his grandfather the Karak side says nothing at
all. <i>The wheel has nothing above Ṣaqr</i>, so ʿIyād and Ḍahdūḥa rest on the Mogannam chart
alone.</p>
{FIX('Kaddoura: Ṣabra was Rāshid’s son, and the eldest of the five.',
 '<b>Ṣabra was Rāshid’s brother</b>, and the eldest of the five was <b>Ḥaddād</b>.',
 'Four independent witnesses now say so: <b>Khalīl Abū Rayya (1980)</b>; Shāhīn (1982); <b>Ḥammūdeh (2014)</b>, who prints it from the Arabic literature; and the Karak wheel, which puts Ṣabra beside Rāshid at the hub and Ḥaddād first among the sons — with John Mogannam reaching the same conclusion by argument from the clan names, p. 18, without any of them in front of him. <b>Kaddoura’s reading is retired, with thanks — it is the reason the question was ever asked.</b>' + c('Kaddoura, <i>Taʾrīkh Rām Allāh</i>; Shāhīn (1982), ch. 1; Mogannam, ch. 2, p. 18; the Karak wheel, plate 84.'))}
<p><i>One caution remains.</i> The wheel has no dates except at its hub. It was first published in this
form in the twenty-first century, and the man who compiled it is alive and speaks to a Ramallah
audience. That does not make it wrong. A family diwan is exactly the kind of source that keeps such
memories.</p>
<p>But it means the agreement above is the agreement of two traditions, not of two documents.
<b>No Ottoman register names Rāshid, Ṣabra or Ṣaqr.</b> That has not changed.</p>"""),

sect('What the ground says', 'The state begins writing down every household in every village on this ridge')
ent('1517–1554', 'documents', False, 'The registers begin',
 'The Ottomans conquered this land in 1517, and the registers we met in chapter 6 now reach our own families. In 1553–54 a group called the Kasābra, 36 Christian households, is registered at Beit Jala, twenty kilometres south. They are not yet at Ramallah.{}'.format(c('The pre-1596 registers come from Ḥammūdeh (2014), pp. 40–47, working from the Istanbul <i>tapu tahrir</i> series; <b>Hütteroth and Abdulfattah (1977) published only the 1005 AH / 1596–97 <i>mufaṣṣal</i> registers</b> (TK 72, 100, 112, 181, 185, 192, Tapu ve Kadastro archive, Ankara), and earlier editions of this book wrongly credited the whole series to them. '+D('1977_Hutteroth_Abdulfattah_Historical_Geography_of_Palestine.pdf')+'.'))),

CH(12)
sect('The ground and the line, together', 'From this page on there is only one story: the family is in the land, and the land is in the documents')
ent('1 April 1561', 'documents', False, 'The people of Ramallah speak',
 f"""<b>A year before the census, the people of this place speak for themselves in a document for the
first time.</b> On 1 April 1561 the judge Abū Wafā al-Ḥanafī was sitting in Jerusalem
with Ḥusām al-Dīn bin Yaʿqūb, deputy overseer of the Ḥaram al-Sharīf. Six men came before him,
“all of them from the village of Ramallah”{c('Sāmiḥ Ḥammūdeh, “New Light on Ramallah’s Origins in the Ottoman Period,” <i>Jerusalem Quarterly</i> 59 (2014), pp. 47–48, translating the Jerusalem sharīʿa court record of 16 Rajab 968 AH. ' + D('2014_Hammoudeh_New_Light_Ramallah_Ottoman_JQ59.pdf') + '. <b>This entry did not exist in earlier editions of this book, which had the article on the shelf and read it for its register tables only.</b>')}.""",
 f"""
<div class="ntwrap"><div class="nthead">Named in court, Jerusalem, 1 April 1561</div>
<table class="ntable"><tr><th>who</th><th>which community</th><th>and elsewhere</th></tr>
<tr><td><b>ʿAlī bin Ḥasan</b> and his brother <b>ʿUmar</b></td><td>Muslim, of the Labūd house</td><td>the Labūd are among the four Muslim households of 1538–39</td></tr>
<tr><td><b>Aḥmad bin Muḥammad Qarʿala</b></td><td>Muslim, of Abū al-Thanā</td><td>—</td></tr>
<tr><td><b>Ghunaym bin Sālim</b>, <i>al-Kasbūrī</i></td><td>Christian</td><td><b>in the Bayt Jālā list of 1553 and the Ramallah list of 1562</b></td></tr>
<tr><td><b>Mūsā bin Baraka</b></td><td>Christian</td><td><b>in the Bayt Jālā list of 1553</b></td></tr>
<tr><td><b>Isḥāq bin Yaʿqūb</b></td><td>Christian</td><td><b>in both registers — one of the nineteen</b></td></tr>
</table></div>
<p>All three Christians appear in the Ottoman registers too. One of them carries the road in his own
name: <b><i>al-Kasbūrī</i></b>, “of Kusbār,” the stage by Ḥalḥūl that the family’s tradition names.
The family’s memory and the court record use the same word for the same people.</p>
<blockquote>They swore an oath that from that day on they will develop the lands of the same village,
and that none of them will farm any other land until all of its lands were cultivated [sic]. Should any of
them violate this, he pledges to pay one hundred gold <i>sulṭānī</i> to the charitable kitchen of our
prophet Khalīl al-Raḥmān.
<span class="cite">Jerusalem sharīʿa court, 16 Rajab 968 / 1 April 1561, in Ḥammūdeh (2014), p. 48</span></blockquote>
<p><b>Then the court divides the hill in three.</b> One third goes to ʿAlī bin Ḥasan, his brother
ʿUmar, Aḥmad bin Muḥammad and their people: the Muslims who were already there. One third goes to
Ghunaym and his people. One third goes to Mūsā and Isḥāq and their people.</p>
<p>So two thirds of Ramallah went to the newcomers, and one third to the men who had held it. It was
agreed in front of a judge and backed by the promised fine.</p>
<p>No sultan or king appears here, and no family tree. Six farmers stand in a Jerusalem court. They
promise to plough one hill and no other until it is all under crop, and they share it between two
religions by agreement.</p>
<p>The Ramallah tradition remembers the land divided into fifths among Rāshid’s five sons. The court
record shows <b>a division into thirds in 1561, the year before the census of 1562, between Muslims and Christians</b>.
Both can be true. One is the arrangement with the neighbours, the other the arrangement inside the
family, and only one of them is on paper.</p>
{FIX('The founding of Ramallah begins in 1562, with the census.',
 'It begins in <b>1561</b>, with an oath — and the people who swore it are named.',
 'The census of 970/1562 records a population; the court record of 968/1561 records a decision. <b>Fourteen months before the clerk counted them, these families had already agreed with the Muslim householders how the hill would be worked and had bound themselves to it in a Jerusalem court.</b> That is what founding a town actually looks like, and it is the reason this book now dates the settlement from 1561 and the count from 1562.' + c('Ḥammūdeh (2014), pp. 47–48. The register of 970/1562 is the count; sijill 48, p. 88 (1565) recites the endowment; the court record of 968/1561 is the agreement. Three instruments, three different things, and earlier editions of this book used only the first.'))}"""),

ent('1561 · 1562', 'documents', True, 'The Christian settlement of 1561–62',
 'The register recorded thirty-six Christian families, called the Kasābra, at Beit Jala in 1553–54. Now they come up the ridge road, and they are not alone when they arrive. <b>The register of 1562 lists seventy-one Christian taxpayers at Ramallah</b>: sixty-three households and eight single men. Ten Muslim households were already living on the hill{}.'.format(c('The detailed Ottoman census (<i>tapu tahrir mufaṣṣal</i>) of 970/1562, in Ḥammūdeh (2014), pp. 45–47. Ramallah’s revenue was assigned to endowment, but the document is a fiscal cadastre, not a waqf register, and earlier editions of this book called it one. The municipality’s and the Federation’s pages print eight Muslim families; Ḥammūdeh, from the register, has ten, and we follow him.')),
 f"""
{FIX('Ramallah was <b>founded in 1562</b> — the year this entry, the key-dates page and the households chart all called “the founding.”',
 'There is no single founding on paper. The record shows a <b>named place by 1186</b>, <b>endowment land by 1279–80</b>, <b>uninhabited farmland in 1525–28</b>, <b>Muslim households living on the hill from 1538–39</b>, and then <b>the Christian families binding themselves to terms in a Jerusalem court in 1561 and counted by the state in 1562</b>. This book now calls 1561–62 <b>the Christian settlement</b>, not the founding.',
 'This is the actual data, set out in order: the charter of 1186 (Strehlke no. 20), sijill 48 p. 88 for 1279, the registers of 1525–28, 1538–39 and 1553–54 and the court record of 968/1561 (Ḥammūdeh 2014, pp. 41–48), and the register of 970/1562. <b>The households chart in earlier editions also showed thirty-seven Christian households for 1562; the register lists seventy-one Christian taxpayers, sixty-three households and eight single men</b>, and the chart is corrected.' + c('Ḥammūdeh (2014), p. 45: the Kasābra families “left Bayt Jala and inhabited Ramallah, accompanied by an additional 27 Christian families also from Bayt Jala and eight unmarried Christian men,” followed by the list of names (pp. 45–46), which marks seven men as single. The endowment register TTd. 406 counts the same Christians as seventy-one taxpayers.'))}
{fig(R.fig_datings(),'Five datings for one town — and they are not rivals',
 'The founding of Ramallah has five different dates attached to it, resting on five different kinds of evidence. Read in order rather than argued over, they describe one coherent sequence: a site that was named endowment land in 1279, uninhabited in 1525, held by a few Muslim households by 1538, bought from the Ghazāwneh by tradition, and settled by the Christian families in 1562. <b>The family did not name the hill. The family settled a hill that already had a name.</b>',
 'Sijill 48, p. 88 (1565, citing a waqf of 1279); Mujīr al-Dīn (1495); the defters of 1525–28 to 1596; al-Dabbāgh; Shāhīn (1982).')}
{fig(R.fig_neighbourhood(),'Ramallah among its neighbours, 1596',
 'The town in its own district in the register of 1596–97. <b>Ramallah at eighty households is one of the larger villages of the nāḥiya</b> — bigger than al-Bīra’s forty-five, nearly four times Jifnā’s twenty-one — and one of only a handful with a Christian majority. <i>This is the company the family kept for the next three hundred years.</i>',
 'Hütteroth and Abdulfattah (1977), pp. 114–21, the nāḥiya of Quds, 1596–97 defter. Note that they record Jifnā as Muslim; Toledano (1984), p. 312, corrects this — the village was wholly Christian in every sixteenth-century defter.')}
{fig(R.fig_households(),'The households, counted',
 'Ramallah in the Ottoman registers of the sixteenth century: from uninhabited endowment land, to a handful of Muslim households, to a village of eighty households — seventy-one Christian and nine Muslim — paying 9,400 akçe, all of it to the endowment. The arrival of 1562 is a visible step. <b>One caution: seventy-one is also the Christian count of 1562, and thirty-four years rarely leave a count unchanged. The clerk of 1596 may have carried the older figure forward, and we have not yet read the 1596 row itself.</b> <b>Hütteroth and Abdulfattah publish the 1596 register as counts; the register itself is a <i>mufaṣṣal</i> and names all eighty heads of household, and we have not yet read them.</b> The family names we do have come earlier and separately, and that is the hardest fact we have: <b>al-Kasābra in the Bayt Jālā register of 1553–54, Rāshid’s descendants in a Jerusalem court deed of 1561 and the census of 1562, al-Naqqāsh in a court record of 1604</b>.',
 'Ḥammūdeh, Jerusalem Quarterly 59 (2014), pp. 45–48, for the registers of 1525–28 to 1562 and the court documents; Hütteroth and Abdulfattah (1977), p. 121, for 1596–97.')}
{FIX('The family settled Ramallah “about 1550” (Shāhīn), under Rāshid and his five sons (Kaddoura).',
 '<b>1562</b>, and the movers were <b>Rāshid’s grandchildren</b>.',
 'The detailed census of 970/1562 records the arrival; the 1553–54 register still shows the group at Bayt Jālā; and Hammoudeh’s archival work shows the last leg made by the grandsons, the popular version compressing three generations into one. <b>A remembered date replaced by a documented one twelve years later costs the tradition nothing — and that the memory was only twelve years out is itself evidence of its quality.</b>' + c('Hammoudeh, “New Light on Ramallah’s Origins in the Ottoman Period,” <i>Jerusalem Quarterly</i> 59 (2014). '+D('2014_Hammoudeh_New_Light_Ramallah_Ottoman_JQ59.pdf')+'.'))}
{FIX('Karak “still holds 143 Christian households” in 1562 (as printed in earlier editions of this book).',
 'The documented figure is <b>103 Christian households and 8 Christian bachelors — beside 78 Muslim households and 2 bachelors — at al-Karak in 1596</b>, in the nāḥiya of Karak, Sanjak of ʿAjlūn: register TK 185, Ankara, published in Hütteroth and Abdulfattah (1977), p. 171.',
 'The 1596 count can be pointed to in a named register; the 1562/143 figure was carried second-hand from “the same survey series” and no folio has been produced for it. <b>It is not discarded — it is demoted to unverified</b>, so that a future researcher chases it rather than assuming it was dropped without cause.' + c('Ottoman Defter 185, the Karak register of 1596: 103 Christian households and 8 Christian bachelors. The 143 figure previously printed here awaits a register reference and should not be repeated until one is produced.'))}
<p>Three years later the hill’s legal position was stated in open court. On <b>22 June 1565</b>
(Ḥammūdeh gives 29 June) the qāḍī, the judge, of Jerusalem entered into sijill 48, p. 88, the court’s register, the fact of an
endowment of 678 AH: this ground belongs to the Ibrāhīmī sanctuary at Hebron. The case was a boundary
dispute with al-Bīra, and the overseer of the endowment brought the deed of 678 AH into court.</p>[[C32]]
<p>That is not a title for the family. <b>It is the reason there was room on the hill at all.</b> This
was endowment land, worked by tenants, with the tithe going to the endowment and not to a landlord.
The early registers split that revenue. In 1538–39 the larger share, 3,000 akçe, went to the Dome
of the Rock in Jerusalem and 2,000 to Hebron. By 1553–54 the whole village supported the shrine of
Abraham{c('Ḥammūdeh (2014), pp. 40–42, for the shares in the registers of 1538–39 and 1553–54: by the latter “the entire village is an endowment supporting the shrine of Abraham.”')}.
This is the hill that, as we saw, already had a name, and the family paid Hebron for the privilege
of settling it.</p>
<p><b>A second register, kept by a different office for a different purpose, counts the same
seventy-one.</b> The endowment survey of the district of Jerusalem was delivered to the treasury in
970, that is 1562–63, the same year as the census. It lists Ramallah on its first folio, under the
endowment of Hebron: the whole village, and “71 persons at 80 akçe, 5,680” from its Christians. The
akçe was the Ottoman silver coin. Beit Jala, on the same folio, has 218 at the same rate, matching
the census there too{c('<i>Defter-i Evkaf-ı Liva-i Kuds-i Şerif</i>, ed. Sevgi Işık (Ankara: Tapu ve Kadastro Genel Müdürlüğü, 2015), an edition of TKG.KK.TTd. 406 (old no. 514/539), folio 1, under <i>Vakf-ı Hazret-i Halīlü’r-Rahman</i>, publication p. 73: <i>Karye-i Ramallah … tamāmen</i>, <i>hāsıl maʿa rüsūm</i> 2,905; <i>Deyr-i Nasārā der-karye-i Ramallah, 71 neferen fī 80 = 5,680</i>. The editor reads the word before <i>Nasārā</i> as <i>deyr</i>; the per-head charge at 80 akçe is the pattern of the Christian poll tax. <b>The edition prints a transcription only, without the Ottoman page, so the word has not been checked against the folio.</b> ' + D('1562_Defter_Evkaf_Kuds_TKGM.pdf') + '.')}.
Two registers, two offices, one number.</p>
<p><b>What we still don’t know.</b> The register of 1596 is a detailed one, and it names all eighty
heads of household at Ramallah, but we have not yet read them. The figure of 143
Christian households once given for Karak in 1562 still has no register reference. Readers who can
help with either would add a page to our story.</p>"""),

ent('1553 and 1562, name by name', 'documents', True, 'The registers do give names',
 f"""In the story half of this chapter, our families come up the ridge from Beit Jala and are
counted at Ramallah in 1562. <b>Every household head in both registers has been in our own family’s
book for thirty years.</b> The co-authors’ <i>Ramallah Family Tree Book</i> prints, in its fourth chapter,
copies of the original pages of Register 289 and Register 516. Beside each it gives a full English
transliteration, the names written in English letters: <b>the 36 Christian households at Beit Jala in
1553–54, and the 10 Muslim households, 63 Christian households and 8 bachelors at Ramallah in
1562–63</b>. <i>One hundred and nine households and eight unmarried men, by name and by father’s
name.</i>{c('John Mogannam, <i>The Ramallah Family Tree Book</i>, ch. 4, charts 1–4: facsimiles of Register 289, cols. 79–80 (Bayt Jālā, 961 AH / 1553–54) and Register 516 (Ramallah, 970 AH / 1562–63), each with his own English transliteration. <b>Earlier editions of this book worked from Ḥammūdeh’s counts and never opened the charts beside them.</b> The transliterations carry his query marks and alternative readings, which are kept here exactly as he set them down.')}""",
 f"""
{fig(F4.fig_registers(),'The same people, nine years apart',
 'Both lists in full. <b>Nineteen of the thirty-six households the clerk recorded at Bayt Jālā in 1553 appear again at Ramallah in 1562 under the same name and the same father</b> — Ishaq bin Yaʿcoub, ʿAmeera bin Hassaan, Jareer bin Hadeed, Farah bin Suweid, Musa bin Braik, Khaleel bin Sadaqa, Kaʿoosh bin Zayed, Suweidan bin Khaleel and eleven more. <i>That is not an argument. It is the same men, on two pieces of paper, nine years apart.</i>',
 'Registers 289 and 516, transliterated by John Mogannam; matching and counts by this edition.')}
{FIX('“The registers give counts, not names.”',
 '<b>Not true of any of them.</b> All three are <i>mufaṣṣal</i> — detailed — registers, and a <i>mufaṣṣal</i> names every household head with his father’s name. <b>The eighty names of Ramallah in 1596 are in the Ankara register, not yet read by us.</b>',
 'The claim confused the register with the book about it. What gives counts and not names is <b>Hütteroth and Abdulfattah’s published tabulation</b> of the 1596 defter, not the defter itself: an <i>icmāl</i> register gives a settlement and a revenue, a <i>mufaṣṣal</i> gives every household head and his patronym, and all three of these are <i>mufaṣṣal</i>. <b>The correction is not a new source. It is a shelf this book had not read to the end — and a folio in Ankara we have not yet asked for.</b>')}
<p><b>What the nineteen prove.</b> The Kasābra, <span class="ar">الكسابرة</span>, were the Christians
of Beit Jala. Until now, the link between them and the Christians who settled Ramallah rested on
Ḥammūdeh’s reading of the two registers together. That was a good argument, but only an argument.
<b>Now it can be shown name by name.</b> Our count also revises his: Ḥammūdeh has all thirty-six
households move, and the names show nineteen.</p>
<p>More than half the households move as a body. The rest show the ordinary losses and gains of nine
years. The Ramallah list is longer because more than fifty further Christian names are on it that
are not on the Beit Jala list at all.</p>
<p>Ḥammūdeh, reading the same register, counts <b>sixty-three households and eight single men</b>,
and the heading of our family’s own transcription says the same. <i>Every reading agrees on the
total: <b>seventy-one Christian taxpayers, sixty-three households and eight single men</b>.</i> One
small detail can still trip a careful reader. Both name lists mark only seven of the eight as single,
so counting the marks gives sixty-four and seven. The difference is one man the lists leave
unmarked{c('Sāmiḥ Ḥammūdeh, <i>Jerusalem Quarterly</i> 59 (2014), on register I.S. 516: the 36 Kasābra households of Bayt Jālā, “accompanied by an additional 27 Christian families also from Bayt Jala and eight unmarried Christian men,” joining “the ten Muslim families residing in Ramallah.” <b>He nowhere prints a total.</b> 36 + 27 = 63 households and 8 bachelors, the same as the heading of the family’s own transcription of the same folio: 71 in all. Both name lists mark only seven of the eight. <b>This retires the “eighth bachelor” from this book’s open questions: he exists, and he is the one man the lists leave unmarked.</b>')}. <i>This is our
strongest piece of written evidence, and it was in our own house all along.</i></p>
<div class="fix"><div class="fixhead">And now the hard part</div>
<div class="fixgrid">
<div><span class="fl">Nobody is called Rāshid</span><b>Not one of the sixty-three Christian household
heads at Ramallah in 1562 bears the name Rāshid</b>, and not one of them is recorded as the son of a
Rāshid.</div>
<div><span class="fl">Which we expected</span>This is what it should look like if the movers
were Rāshid’s <b>grandchildren</b>, as Ḥammūdeh argues and we follow. Their fathers would be
Rāshid’s sons, and it is the sons’ names we should be looking for in the patronymics — <i>not
Rāshid’s.</i></div>
<div><span class="fl">And there they are — carefully</span>As fathers in the 1562 list:
<b>Ḥassān 5, Hadeed 3, Ibrāhīm 3, Jiryis 1, Shuqayr 0</b> — twelve households out of sixty-three.
<b>Ḥassān and Ibrāhīm are two of the commonest names in the Levant and prove nothing.</b> Jiryis is
one household. Shuqayr is absent altogether. <i>The one worth chasing is Hadeed.</i></div>
</div></div>
<p>The name itself has a Palestinian and Jordanian literature that we had not used before.
<span class="ar">الحدادين</span> means <i>the blacksmiths</i>. Hind Abū al-Shaʿr shows that Christian
families of Transjordan specialised in the trade and carry the name to this day.</p>
<p>Travellers in the nineteenth century met Christian blacksmiths in the villages of ʿAjlūn in 1868,
1877 and 1884. Tamīmī and Bahjat recorded that most Nablus Christians were blacksmiths or
leather-dyers. And the Jerusalem court records of the seventeenth century treat blacksmithing as a
trade for Christians only{c('Hind Abū al-Shaʿr, <span class="ar">تاريخ شرق الأردن في العهد العثماني</span> (Amman: Jordanian Ministry of Culture, 2010), p. 364; Rafīq al-Tamīmī and Muḥammad Bahjat, <span class="ar">ولاية بيروت</span> (1917), p. 123; Maḥmūd ʿAṭāllah on seventeenth-century Jerusalem; all cited in Ḥammūdeh (2014), n. 52. <b>The family name is an occupation, and the occupation was a Christian one in this country. That is not a lesser origin than a dynasty; it is a better-documented one.</b>')}.</p>
<p><i>A trade name is not a family tree, and it does not contradict one. But <b>it is the explanation
the record supports</b>, and it should come first.</i></p>
<p>This brings the register question into focus. <span class="ar">حديد</span> and
<span class="ar">حداد</span>, “iron” and “blacksmith”, share the same root and differ by one letter.
In an Ottoman clerk’s hand, in a register written without the dots that tell letters apart, they look
almost the same. <b>John transliterated it Hadeed.</b></p>
<p>And it is not new in 1562. Jareer bin Hadeed is in the Beit Jala register of 1553 as well, one of
the nineteen who make the move. <i>If that reading is right, the family name is in a document nine
years before the Christian settlement</i>{c('Jareer bin Hadeed appears in both registers; Ghneim bin Hadeed and Ghanayem bin Hadeed appear at Ramallah in 1562. <b>The reading cannot be settled from a transliteration.</b> It requires the Arabic of Registers 289 and 516 — the Istanbul <i>tapu tahrir</i> series, I.S. 289 and I.S. 516 — read for the pointing. Until then this is a lead, not a finding, and it is exactly the kind of surname resemblance this book warns against three eras earlier, in the <span class="ar">الحدادة</span> entry.')}.</p>
{FIX('A finding.',
 '<b>A lead, and the trap named beside it.</b>',
 'This book has already refused one attractive surname match — al-Suwaydī’s <span class="ar">الحدادة</span>, an unrelated North African group — on the ground that a resemblance between a clan name and an ancestor’s name is not evidence of anything. <b>The same rule applies here, to our own advantage rather than against it.</b> Ḥadīd is worth the trip to Istanbul, where registers 289 and 516 are; Ankara holds the 1596 mufaṣṣal. It is not worth a sentence in the family’s history until somebody makes it.')}
<p>One more number to keep. The ten Muslim households of 1562 are named too: Khaleel bin Hassaan,
ʿAmeer bin ʿOmar, Hasan bin ʿAta, Ahmad bin Muhammad and six more. <b>They were on the hill first, and
the register puts them at the head of the page.</b> We have long said that
Muslims were never absent from Ramallah. <i>Now we can say who they were.</i></p>"""),

ent('after 1562', 'oral', True, 'The five sons and the eight clans',
 'Ramallah was now a mostly Christian village on endowment land, counted by the Ottoman clerks. The family remembers how its land was shared out. It was divided in fifths among <b>Haddad, Ibrahim, Jirius, Shukair and Hassaan</b>. Jirius was not satisfied, so he was given the extra parcel called Karm ʿAli. Haddad’s fifth was then divided again among his own five sons{}.'.format(c('Shāhīn (1982), ch. 1: the fifths, Karm ʿAli, and the eight clans — four Hadadeh (Sharaka, Jaghab, Yousef, ʿAwwaad-with-ʿAzzouz) and four Hamayel.')),
 f"""
<p>Out of this double division comes the shape every Ramallah family still knows: <b>eight clans,
four Hadadeh and four Hamayel</b>. The Hadadeh are Haddad’s descendants; the Hamayel are the clans
descended from Rāshid’s other sons. The names carry the sixteenth century inside them. The Sharaka are
simply “the easterners.” The Jaghab are named for their ancestor shouting at a stubborn ox at the
trough: <i>“Drink, or I will break your horn!”</i></p>
<p>A community that still organises its conventions in Detroit by these names is organising itself
by a joke shouted at an ox four hundred years ago. That is not a weakness of the record. It is the
record.</p>
{fig(F3.fig_clans_tree(),'One man, five sons, eight clans — and a town',
 'The social structure of Ramallah in a single diagram, with each clan’s population from the ration-card census of 1944. Nearly four centuries after the division of the land, a British administrator issuing ration books could still count the town by Rāshid’s grandsons.',
 'Shāhīn (1982), ch. 1, for the fifths, Karm ʿAli and the clan etymologies; the 1944 ration-card census for the counts.')}"""),

CH(12)

ent('1671 · 1700 · 1706', 'documents', True, 'The parish proves itself in writing',
 'The parish of Ramallah begins to appear in church records in the 1600s. Ramallah workers helped repair the roof of the Church of the Nativity in 1671. In 1700 <b>Yaʿqūb Ilyās of the Yousef clan, one of the four Hadadeh, was ordained, the first priest born in Ramallah</b>. In 1706 a Ramallah priest earned 20 piasters a month teaching the parish boys to read <i>Arabic and Greek</i>{}. The Patriarchate’s own registers, printed by Papadopoulos-Kerameus, name Ramallah in 1706 and 1709{}. So a Greek publication of 1894 and an Arabic family history of 1982 describe the same parish in the same decade, and Shāhīn, writing in 1982, did not know the Greek book: two witnesses who never met.'.format(
  c('Shāhīn (1982), the seventeenth-century chapter and the 1706 salary record, there credited to Kaddoura.'),
  c('Papadopoulos-Kerameus, <i>Analekta Hierosolymitikēs Stachyologias</i>, II–III (St Petersburg, 1894–97).'))),

ent('about 1750', 'oral', False, 'New families arrive',
 '“Ramallah became a prosperous town and attracted other families... The influx began about 1750.”{} First came the ʿAjlounys from ʿAjlūn. The Hishmeh came by way of al-Jazzār’s walls at Acre about 1775, the Nazzal from Rafidia about 1805, and the ʿAraj, Zagroot and Shahla from Deir Aban about 1810. Each family was given land and folded into a clan. The town took in its newcomers just as the land had always taken in its own. Much later, in 1923, Muhammad El Jaʿooni, a plumber, is remembered as <b>the first Muslim to buy land and build inside the town itself</b>. Yet Muslim households are in the tax registers from 1538, nine of the eighty in 1596, and the British census counted 125 Muslims here in 1922{}.'.format(c('Shāhīn (1982), ch. 2, “Outsiders Who Settled in Ramallah,” with the dates and circumstances of each family’s arrival, and the first Muslim resident in 1923. For the Nazzal, N. Shaheen (2005), ch. 27, prints both about 1805 and about 1905; we follow 1805.'),
  c('Against the tradition: Ḥammūdeh (2014), pp. 41–42, names Muslim household heads at Ramallah from 1538 — Ḥasan ibn ʿAlī al-Labūd and his sons, Rajab ibn Yaʿqūb, Muḥammad ibn Abī al-Thanāʾ; Hütteroth and Abdulfattah (1977), p. 121, count nine Muslim households of eighty in 1596; Barron, <i>Census of Palestine 1922</i>, counts 125 Muslims in Ramallah. <b>What 1923 records is a first Muslim purchase inside the town, not a first Muslim.</b>'))),

ent('1834', 'documents', False,
    'The peasants’ revolt of 1834',
 f'''In 1834 came the largest political event in this hill country between the Ottoman conquest and the Ottoman reforms of the mid-1800s. In April <b>Ibrāhīm Pasha ordered conscription, one man in five</b>. He added a new head tax, the <i>farḍa</i>, and ordered the villages disarmed. The men who rose were the shaykhs, the local chiefs, who had been ordered to enforce it{c('Beshara Doumani, <i>Rediscovering Palestine: Merchants and Peasants in Jabal Nablus, 1700–1900</i> (California, 1995), pp. 33–34: the rural leaders “began to greatly resent their exclusion from the Advisory Councils… This resentment turned to rebellion when they were ordered to implement the highly unpopular measures of disarming and conscripting the peasantry, as well as collecting a new head tax, the <i>ferde</i>.” '+D('1995_Doumani_Rediscovering_Palestine_Jabal_Nablus.pdf')+'. On the Egyptian measures from the Arabic side: <span class="ar">الموسوعة الفلسطينية</span>, “<span class="ar">الحكم المصري ١٨٣١–١٨٤٠</span>” — 3,000 conscripts demanded from each of the districts of Jerusalem, Nablus and Hebron, and a <i>farḍa</i> of 15–50 piastres a year.')}: Qāsim al-Aḥmad of Jammāʿīn, and with him the shaykhly houses of this district.''',
 f"""
<p>In May something like twenty thousand men besieged Jerusalem and took it through a sewer near the
Dung Gate. Ibrāhīm marched up from Jaffa with nine thousand troops. By August the rising was broken at
Dayr al-Ghuṣūn and at Hebron. Qāsim al-Aḥmad fled to <b>Karak</b>, the town our family’s own
tradition comes from. There a seventeen-day siege ended with the place destroyed and Qāsim handed
over{c('Judith Mendelsohn Rood, “The Time the Peasants Entered Jerusalem: The Revolt against Ibrahim Pasha in the Islamic Court Sources,” <i>Jerusalem Quarterly</i> 27 (Summer 2006), 28–43, DOI 10.70190/jq.i27.p28 — read directly for this edition, and the source of every quoted detail here. Her own evidence is the Jerusalem Islamic court records and the chronicle of the Greek Orthodox monk <b>Spyridon</b>, resident in the city, at his pp. 88–92. Her fuller narrative is <i>Sacred Law in the Holy City</i> (Brill, 2004), pp. 123–34, which this project has <b>not</b> read; where a detail rests on the book alone it is flagged. Eugene Rogan, <i>Frontiers of the State in the Late Ottoman Empire</i>, pp. 31–32, for the flight to al-Karak and the siege.')}.</p>
<p>The road our family says it came up in the sixteenth century is the road the revolt’s last leader
went down in the nineteenth.</p>
<p><b>Three shaykhs of the Ramallah highlands were put to death for it</b>: ʿAlī Rabbāḥ and ʿAbd al-Jābir, Barghūthīs of
Banī Zayd, whose seat was Dayr Ghassāna, and Ismāʿīl ibn Simḥān of Rās
Karkar{c('R. A. S. Macalister and E. W. G. Masterman, “Occasional Papers on the Modern Inhabitants of Palestine,” <i>PEF Quarterly Statement</i> 37 (1905), 343–356. At p. 355, of Banī Zayd, ʿAlī Rabbāḥ and ʿAbd al-Jābir “were both put to death by Ibrahim Pasha”; the 1906 instalment places Ismāʿīl’s death at Damascus. The chronicle says “killed” and “put to death”; it does not say how. <b>Earlier editions of this book reported that the sources disagreed about which <i>nāḥiya</i> the Samḥān headed. They do not; the confusion was a table.</b> Macalister and Masterman at p. 354 divide Banī Ḥārith in two: of the <b>northern</b> half the ruling family is <b>Simḥān</b>, “chief sheikh, Ismāʿīl (killed by Ibrāhīm Pasha in 1834),” with chief towns el-Jāniyah and <i>er-Rās</i> — and their own footnote adds “also called Rās Karker.” Its villages include <b>Jifnā</b>, Bīr Zayt, Dayr ʿAmmār, Surdah and Abū Kash. Of the <b>southern</b> half the ruling family is Kaʿraja, seated at Bayt Ibzīʿ. <b>Banī Zayd is a separate nāḥiya</b>, the Barghūthīs’ own, seated at Dayr Ghassāna. A widely circulated table collapses the two halves into one row and parks Rās Karkar in Banī Zayd, citing Doumani p. 35 — where no such table exists; Doumani’s only nāḥiya table is for Jabal Nablus in 1850 and contains none of these names. The Institute for Palestine Studies study of the Abū Ghūsh family confirms the reading: Shaykh Samḥān “was the shaykh of the Banī Ḥārith nāḥiya,” controlling the northern part of the Jerusalem mountains. Ramallah itself sat in <b>Jabal al-Quds</b>, in the quarter administered from al-Bīra, and is listed there among “the other villages of this district” — not as a seat.')}.</p>
<p>The village of this district that paid for it was a Christian one. Edward Robinson rode into Jifnā
four years later and wrote down what he found: a village entirely Christian, forty-two taxable men,
perhaps two hundred souls, and this sentence.
<i>“After the rebellion of 1834, twenty-six men were taken to Egypt and put into the public works,
whence they have never returned. Not long since, one of their two priests went to Egypt to look
after them, and died there.”</i>{c('Edward Robinson and Eli Smith, <i>Biblical Researches in Palestine, Mount Sinai and Arabia Petræa: A Journal of Travels in the Year 1838</i>, vol. III (Boston: Crocker &amp; Brewster; London: John Murray, <b>1841</b>), pp. 78–79. Robinson spells the village <i>Jufna</i>. <b>Cite the 1841 edition: the 1856 second edition renumbers the volumes and this material sits elsewhere.</b> Robinson gives no motive, no accusation and no trial, and he does not describe a rising at Jifnā — the deportation follows the general rebellion. Jifnā’s connection to it is administrative: the village belonged to the northern Banī Ḥārith, whose paramount shaykh Ismāʿīl Simḥān was executed by Ibrāhīm Pasha in the same year.')}</p>
<p>The version in general circulation says twenty-six men were <i>exiled for their alleged
participation</i>, and that <i>two priests joined them voluntarily</i>. Neither is in Robinson. The
men were <i>put into the public works</i>: taken for forced labour, not sent into exile, and they
<b>never came back</b>. The village had two priests. One of them went to Egypt afterwards, on a
pastoral errand, to look after them, and died there. The mistake grew out of the phrase “one of their
two priests”: somebody read the two and dropped the one.</p>
<div class="fix"><div class="fixhead">A correction this book makes to itself, within a day of printing it</div>
<div class="fixgrid">
<div><span class="fl">As it stood</span>Twenty-six men of Jifnā were exiled to Egypt for their part in the rising, and two of their priests went with them voluntarily.</div>
<div><span class="fl">Corrected to</span><b>Twenty-six men of Jifnā were taken to Egypt and put into the public works, and never returned. One of the village’s two priests went afterwards to look after them, and died there.</b></div>
<div><span class="fl">How it is justified</span>Robinson and Smith, 1841, III.78–79, read directly. The superseded reading came to this book through a summary of a summary, and it is the reading printed by the general reference works. <i>It is worth saying what the difference is: the received version makes Jifnā a village of rebels who were punished. What Robinson describes is a village stripped of twenty-six men for a rebellion he does not say they joined — and a priest who followed them into Egypt and did not come home either.</i></div>
</div></div>
<p>What happened at Jifnā matters, because it cuts against the easy story. On 31 May, the day after Ibrāhīm
Pasha re-entered Jerusalem, his soldiers attacked Beit Jala, the village our family came up from in
1562. They killed thirty-three Christian men and women, on suspicion of
looting{c('Rood, <i>Jerusalem Quarterly</i> 27 (2006): “The following day the village of Bayt Jala was attacked by soldiers and 33 Christian men and women were killed on suspicion of looting.” Her source for the Bayt Jālā and Bethlehem episodes is the chronicle of the monk Spyridon, pp. 88–92. <b>Note the pretext: not rebellion, looting.</b>')}.</p>
<p>Christian shops in Jerusalem were looted along with Muslim and Jewish ones, in the three days after the city fell.
After the revolt was put down, conscription was extended to Christians as well. The rising of 1834 was a revolt of
tax-farming shaykhs, the chiefs who collected the state’s taxes, and their villages against a
centralising state. <b>Religion was a factor, but it was not the dividing line.</b>{c('On the looting of 23–24 May: Rood (2004), p. 128 — “virtually every Muslim, Jewish and Christian-owned shop was raided and damaged.” On conscription extended to Christians after the revolt: Joel Beinin, <i>Workers and Peasants in the Modern Middle East</i>, p. 33. <b>A claim this book will not print:</b> that Bethlehem’s Muslim quarter was destroyed in reprisal on 1 June. It circulates widely, sourced to Rood’s 2004 book at p. 130; her own article says something else for that date — that the Taʿāmira armed themselves to defend Christians in Bethlehem against looting Khedival troops — and this project could not read the book. <b>Withdrawn pending the page.</b>')}</p>
<p>Apart from a few lines in Shāhīn, Ramallah and al-Bireh appear in no account of that year that we
have found. As we told in “Feuds, a pasha and a faction,” Shāhīn records only that Ibrāhīm Pasha
occupied the town without resistance, and that its hundred and fifty families fed his army’s oxen and
got them back.</p>
<p>Robinson went on to Beit Jala the same year, and found it as it had always been. He writes that it “is inhabited solely by Christians,” and that “the tradition
formerly was current, that no Muhammedan could live in it more than two years.” Pilgrims had already
recorded that tradition in 1496.</p>
<p>The village belonged to the Tekiyeh, “a charitable establishment in Jerusalem, near the Haram.” Its
taxable men numbered five hundred, “indicating a population of about two thousand souls,” and “of
the men, sixty can read.” Under the old government it had paid its land tax to the Greek convents,
which in turn paid each of its five shaykhs a yearly
stipend{c('Edward Robinson and Eli Smith, <i>Biblical Researches in Palestine</i> (Boston, 1841), vol. II, pp. 321–324 (read in the 1856 reprint, vol. II, pp. 3–4, which gives the 1841 pages in the margin). Robinson’s footnote sends the two-year tradition to the pilgrimage of Alexander, Count Palatine of the Rhine, in 1496.')}.
The town the Kasābra, our forebears’ group at Beit Jala, came up from in the 1550s was still, three centuries later, a Christian town
run by its own shaykhs.</p>
<p><b>Here is what 1834 did to the country our family lives in.</b> The <i>shaykh al-nāḥiya</i> was the tax-farming lord of a
group of villages, ruling from a fortified house (<i>qaṣr</i>) in his “throne village.” That is the
system 1834 broke. The chronicle shows the Simḥān still acting as district chiefs in the 1840s and 1850s.</p>[[C39]]
<p>The institution itself took another thirty years to die, and paperwork killed it rather than
cannon: the urban advisory councils; the Land Code of 1858 and the Vilayet Law of 1864, the Ottoman laws
that gave land a deed and villages a headman; and the appointed <i>mukhtār</i>, the village headman, who replaced the
shaykh{c('Doumani, <i>Rediscovering Palestine</i>, pp. 111–12 and 169, for the sequence — merchant credit hollowing out the subdistrict chiefs before 1834, the Egyptian councils after it, and the permanent assertion of central authority around 1860; Suad Amiry, <i>Space, Kinship and Gender</i> (PhD, Edinburgh, 1987), p. 43, for the transfer of authority to urban notables and appointed <i>mukhtārs</i>, after which “the influence of their throne villages all but disappeared by the beginning of the twentieth century.” On the throne villages of these hills: Riwaq — Centre for Architectural Conservation, Ramallah, <i>Qurā al-Karāsī</i>.')}.</p>
<p>The Qays–Yaman war of the mid-1840s, which we told early, in “Feuds, a pasha and a faction,” because it
belongs with the older feuds, therefore falls in a gap:
after the shaykhs were put to death and before the new government arrived. This is our own reading. No
source we consulted draws the connection, and readers are free to refuse it.</p>
<div class="fix"><div class="fixhead">And what it says about Ramallah’s own standing</div>
<div style="font-size:.95rem;line-height:1.65;color:#46423B">
<p style="max-width:none"><b>Ramallah is on no list of throne villages, and it has no shaykhly house
in any of them.</b> The seats of this hill country were Dayr Ghassāna and Abwein for Banī Zayd,
Dayr Ibzīʿ or Rās Karkar for Banī Ḥārith, Qaryat al-ʿInab for Banī Mālik. Ramallah was registered in
1596 not under a tribal <i>nāḥiya</i>, or subdistrict, at all but directly under the <i>nāḥiya</i> of al-Quds, with
its revenue assigned to endowment. <i>It was a waqf village, held by a religious endowment, not a lordship.</i></p>
<p style="max-width:none"><b>But this is an argument from silence, and we say so.</b> Sāmiḥ
Ḥammūdeh, who has read the registers, states plainly that the period between about 1600 and 1800 is
almost entirely undocumented for this town. <i>Ramallah is absent from the lists. That is not the
same as having been proved to be nothing.</i></p></div></div>
<p><b>What we still don’t know.</b> Beyond Shāhīn’s few lines, we have found no account of 1834 that
names Ramallah or al-Bireh. And the two centuries from about 1600 to 1800 are still almost entirely
undocumented for our town. Papers or memories from those years, in any family, could help fill the
gap.</p>"""),

ent('1820 · 1834 · 1844', 'oral', True, 'Feuds, a pasha and a faction',
 'In 1820 the ʿAzzouz incident scattered the whole town to eight villages for months. It began as a feud within the Shakara clan, as Shāhīn (1982) tells it (Shaheen 1992 and 2005 print Sharaka), and ten-odd men were killed. In 1834 Ibrāhīm Pasha, whose Egyptian army then held the country, occupied Ramallah without resistance. The town was about 150 families, and they fed his army’s oxen and got them back. In the mid-1840s the hill country fought between its two great factions, Qays and Yaman, and <b>Ramallah, in Shāhīn’s word, was the Qays headquarters</b>{}. Shāhīn dates the fighting to 1844. A local chronicle printed in 1906 puts it about 1846, with a second attack about 1852–53.'.format(c('Shāhīn (1982), ch. 3, pp. 33–34: the ʿAzzouz incident and the village-by-village dispersal, after Kaddoura (1954), p. 59; the quarrel was among <span class="ar">آل الشقرة انفسهم</span>, the Shakara themselves, and <span class="ar">بضعة عشر رجلا</span>, ten-odd men, were killed. R. A. S. Macalister and E. W. G. Masterman, <i>PEF Quarterly Statement</i> 38 (1906), p. 41, for the chronicle’s dates and for Ramallah and al-Bīra “recognised as belonging to the Kais.” Shāhīn again for Ibrāhīm Pasha’s occupation; the 1844 war — the sixteen-man garrison at Beitunia, Suleiman El Samhan’s killing of Taha Abu Ghosh, Patriarch Keirollus’s intervention, and Abu Ghosh’s year of exile in Constantinople.')),
 FIX('“No source found in this research assigns Ramallah itself to Qays or to Yaman” (the family presentation).',
 '<b>Ramallah was Qaysī, and Shāhīn calls it the Qaysī headquarters in 1844.</b> Beitunia, next door, was the Yemeni one — and the Shakara declared themselves Yemen simply to protect their lands near Beitunia.',
 'Shāhīn (1982) devotes a chapter to the 1844 war and assigns the town explicitly. The chronicle printed by Macalister and Masterman (1906, p. 41) agrees on the side, though not on the year or the word: Ramallah and al-Bīra “were recognised as belonging to the Kais,” while “some part of the former village, at any rate, was always recognised as Yamanite.” The deeper point survives him: the faction language was genealogical, but families chose sides for local reasons — descent language in this country has always described belonging as much as biology.')),

ent('1850', 'documents', True, 'The present Greek Orthodox church is built',
 'In the 1800s Ramallah grew into a town of about two thousand people by 1870, as Guérin counted it, and of some four thousand by 1904, as Othman reports, and it built new churches and new schools. The present Greek Orthodox church went up in 1850, on the site of the first church of 1807, which Fr Mitry Elias Kassees had built near the present bus station{}. <b>It was built out of an older church.</b> The dressed stone was carried up from the Byzantine church at Khirbet et-Tireh, on the western edge of the town. Guérin, here about 1870, was told the church had been built eighteen years before “partly with the remains of an ancient church of Kharbet et-Thireh.” The excavator of et-Tireh confirms that in 1850 the Orthodox community “robbed out a large number of trimmed stones” to build it{}. So the town’s church is built from a church that people here had prayed in a thousand years before our family arrived. In August 2015 the bones from et-Tireh’s crypt were carried to this church in procession and buried there{}.'.format(
   c('Shāhīn (1982): the 1807 first church and its builder; the present church of 1850; the outstanding-dates list confirms both.'),
   c('V. Guérin, <i>Description de la Palestine: Samarie</i> II (Paris, 1875), ch. XXXIV–XXXV: “Ils y ont élevé, il y a dix-huit ans, une église, construite en partie avec les restes d’une ancienne église du Kharbet et-Thireh”; and of et-Tireh, the old church “a été complètement démoli, il y a un petit nombre d’années, pour servir à la construction de l’église grecque de Ram-Allah.” Its apse still stood in 1863. S. H. A. al-Houdalieh, “The Byzantine Eastern Church of Khirbet et-Tireh,” <i>Archaeological Discovery</i> 4 (2016), 48–67, the section on the dismantling of the walls. ' + D('1875_Guerin_Description_de_la_Palestine_Samarie_II.pdf') + ' · ' + D('2016_Houdalieh_Byzantine_Church_Khirbet_et-Tireh.pdf') + '.'),
   c('Al-Houdalieh (2016): the skeletal remains from the graves were carried “on 4 August 2015 in a solemn funeral procession to the Greek Orthodox Church in Ramallah, where a requiem was celebrated,” at the request of the Patriarchate.')),
 FIX('The present church, built <b>1852</b> (as circulated in the family’s materials).',
 '<b>1850 is the date carved on the portal</b> — most naturally the start of building — and Shāhīn gives 1850 too. <b>Published sources generally give 1852 for the inauguration.</b> Both can be true.',
 'A datestone records when a stone was cut, not when a church opened. This book prints 1850 for the building and notes 1852 for the inauguration, rather than claiming to have overturned the published date.')),

ent('1857–1895', 'attested', True, 'The town gains its churches and schools',
 '<b>In 1869 the Friends opened a school for girls in Ramallah, because Miriam Karam asked them for one</b>; we tell her story in “A teacher and a doctor from outside.” The school opened with twenty girls, and by 1873 the Friends had fifty girls in four day schools. A boarding school, the Girls Training Home, followed in 1889 with fifteen pupils, and the school took the name Friends Girls School in 1925{}. That is the shape of the whole century. The missions came to Ramallah because Ramallah’s people asked them for things, and then ran what they were given. Bishop Gobat’s Protestant school came first, about 1848–50, and the Latin school followed in 1857–58. The Sisters of St Joseph opened a girls’ school and a free clinic in 1873. St Andrew’s came in 1887, and Our Lady of the Annunciation in 1895 under Fr Yaʿqūb Mogannam{}. Six denominations came in fifty years, to a town of two thousand.'.format(
  c('Enaya Othman, <i>Jerusalem Quarterly</i> 50, p. 62 n. 11: the Hope School opened in August 1869 and “was attended by twenty girls”; “By 1873, there were fifty girls in the four schools.” Shāhīn (1982): Miriam Karam’s exchange with Eli and Sybil Jones; the boarding school of 1889 (15 pupils, first principal Katie Gabriel — who gave the school forty-one years, eighteen as principal and more than twenty as matron); the boys’ boarding school of 1901 under Elihu Grant. <b>Shāhīn (p. 63) and the school’s own history both date the street encounter to 1869, the year the school opened, and the school makes Miriam fifteen and already schooled in Jerusalem. The renaming to Friends Girls School is dated 1925 by the school’s own history; earlier editions of this book printed 1919.</b>'),
  c('Shāhīn (1982), the education and denominations chapters, with the dates of each school and church; the Catholic mechanism of close-relative marriages and the 150 Catholics of 1870. <b>The Latin Patriarchate dates its Ramallah school to 1858; St Andrew’s at 1887 is carried by Shāhīn alone and no diocesan record for it has been found.</b>'))),

ent('the 1800s', 'oral', True, 'How the town lived',
 'Before the schools, the clinics and the steamships, Ramallah was a farming village of stone cottages, built wall to wall for safety. Its people spent the summers in the fig groves and the winters around a clay oven. <b>Shāhīn wrote all of it down</b>, and it is the world every emigrant from our town carried in his head.',
 f"""
<p><b>The guest house.</b> Each clan kept a <i>madafa</i>, a large upper room in the clan leader’s
house. There the men gathered in the evening over coffee to settle disputes, appoint the village
watchman and shepherd, and argue about the harvest. At first the whole town had one. Then there were
two, one for the Hadadeh and one for the Hamayel. Then, as the clans grew, each of the eight had its
own{c('Shāhīn (1982), ch. 4, “Social Gatherings; the Guest House.” The oldest known photograph of Ramallah’s inhabitants — the ʿAwwaad clan seated outside their madafa, c. 1890 — hangs enlarged in Ramallah’s City Hall.')}.</p>
<p>A distinguished guest was given a <i>mensaf</i>. It came in a wooden bowl big enough for fifteen
loaves: bread soaked in lamb broth, a deep layer of rice, and an entire leg of lamb, the
<i>shadah</i>, laid on top for the guest of honour. That was <b>twenty to thirty pounds of meat</b>,
eaten with the hands in three sittings: the men and the guest first, then the older children, then
the women{c('Shāhīn (1982), ch. 4, on the mensaf and the order of eating. The <i>shadah</i> reappears in the 1844 story of Esa Abu Misleh, who seized the sheikh’s hand rather than surrender it.')}.</p>
<p><b>The oven, and the news.</b> Bread was baked in a <i>taboon</i>, a domed clay oven in its own
stone hut, floored with smooth pebbles. It was heated three times a day with dry manure and hay, and
never allowed to go out, because relighting took two days. Five or six families shared one and baked
in turns. In winter the women gathered there for warmth and talk, and the Arabic of Ramallah gained a
phrase for gossip: <i>tawabeen news</i>, “news of the ovens”, what you heard at the
oven{c('Shāhīn (1982), ch. 4, “The Taboon.” <i>Tawabeen</i> is the plural of <i>taboon</i>.')}.</p>
<p><b>The summer house.</b> From the fig harvest on, the whole family moved out to the <i>qaṣr</i>, a
two-storey drystone tower in the groves. Provisions and the drying figs were kept below and the
sleeping quarters above, with a wide window to watch the trees from. A thick belt of thorn branches
around the upper floor served in place of barbed wire{c('Shāhīn (1982), ch. 4, “Agriculture,” with the photograph of a qasr taken in 1955.')}.</p>
<p>Even as late as 1920, the crop gives the scale of that world: 84,000 kilograms of olive oil, a million and a half
kilograms of dried figs, 1.2 million of grapes. Shāhīn, writing in 1982, adds a line that marks his
own generation: <i>“Eighty percent of the land is now uncultivated. The generations that worked the
land have passed away and, alas, the land too is passing away.”</i></p>
<p><b>A wedding took a week.</b> Three steps came first: the <i>tulbeh</i> (the formal asking), the
engagement, and the buying of the <i>kissweh</i>, the bride’s clothes, in Jerusalem and Bethlehem.
Then came Monday to Sunday of dancing: the men’s <i>mel‘ab</i> in two facing rows around a fire,
the henna on Saturday, and on Sunday the <i>zaffa</i>, the procession to the church. The bride rode
on a horse holding a sword in both hands, to signify that the family would defend its honour with
one{c('Shāhīn (1982), ch. 4, “Marriage Arrangements” and “The Wedding.” The dowry about 1900: fifty French gold pieces, worth $3.80 each; half that for a widow.')}.</p>
<p>The Orthodox church forbade marriage inside fourth or fifth cousins, so families looked a little
further out. Three or four families would arrange a ring: a son of A marrying a daughter of B, a son
of B a daughter of C, a son of C a daughter of A. In that way the clans kept marrying among
themselves, without breaking the church’s rule.</p>"""),

ent('the church year', 'oral', True, 'The festivals of the church year',
 'Ramallah’s calendar ran on the Julian reckoning, the older calendar kept by the Greek Orthodox church. There were three fasts a year: Lent, forty-eight days; the fortnight of Saint Mary in August; and forty days before Christmas.',
 f"""
<p><b>Palm Sunday belonged to the young.</b> The girls of the town, between fifteen and twenty-five,
put on their best embroidered dresses, or borrowed their mothers’ and aunts’. They went to the
threshing floor and formed two rows of fifteen to twenty, twenty metres apart. Then they danced
toward each other and back, singing, for most of the day, with the whole town
watching{c('Shāhīn (1982), ch. 4, “Festivals and Holidays.” He notes that the Palm Sunday dances are among the fondest memories of Ramallah women living in the United States.')}. Shāhīn records that it is the memory Ramallah women in America keep
longest.</p>
<p><b>Holy Light Saturday belonged to the whole town.</b> Three or four men walked to the Church of
the Holy Sepulchre in Jerusalem, lit a candle at the flame, sealed it in a lantern and carried it
back on foot. The head priest, the clergy, the choir and most of the town waited at the edge of
Ramallah with unlit candles. When the light arrived the church bells rang and everyone lit from it,
and the young men led the procession in a chant with rhyme and metre. Easter itself, <i>el-Hajmeh</i>,
“the sudden rising,” began at one in the morning and ran till four or five{c('Shāhīn (1982), ch. 4; he prints the Holy Light chant in Arabic. He also records, of the years after 1967, that “it is celebrated in a subdued manner.”')}.</p>
<p>Every day of Holy Week had its own name, translated literally from the Arabic: <b>Long Monday,
God’s Tuesday, Job’s Wednesday, Washing-of-the-Feet Thursday, Sad Friday, Holy Light Saturday, and
Easter Sunday, the great feast of joy</b>. Before Easter the town also made a deliberate effort to
reconcile anyone who had quarrelled during the year, a custom Shāhīn notes was still kept when he
wrote.</p>"""),

ent('1883', 'attested', False, 'The first doctors',
 'Ramallah’s first doctor was a foreigner at the Friends clinic in 1883: Dr George Hassenauer, whom the town renamed Dr Ḥassan Nawwār because it could not say his name{}. Its second came from Beirut: from 1891 Dr Philip Asʿad Maʿlouf, a Lebanese, whose story we tell in “A teacher and a doctor from outside.” Before them both there were midwives, bloodletting, hot-oil massage and charms, and a three-hour donkey ride to Jerusalem.'.format(c('Shāhīn (1982), “Medical Treatment”: Hassenauer (1883–89), the C.M.S. ladies and Dr Croper (to 1910), Dr Maʿlouf (1891–1916), and the author’s own illness of 1906.'))),

ent('about 1900', 'oral', False, 'What a day was worth',
 'Shāhīn preserves the town’s whole price system. It shows what every choice in our story cost, including the choice to leave.',
 fig(F3.fig_wages_ladder(),'The ladder of a day’s work, about 1900–1903',
  'Daily wages in piasters, when a piaster was worth five US cents. Note where the top of the ladder is: a <b>mason</b> earned 23 piasters, one silver majeedy — nearly four times a labourer. This is why Ramallah men learned to cut and set stone, why they worked the monasteries of Jerusalem, and why they, of all the villages on this ridge, could afford the passage to America.',
  'Shāhīn (1982), “Money, Weights, and Measures.”') + NUMTABLE('THE MONEY, ABOUT 1900 — “the piaster was worth five cents (U.S.)”',
  ['Coin', 'Value'],
  [['sahtoot (½ kabak)', '2½ baras'], ['kabak', '5 baras'], ['matleek / ashara', '10 baras'],
   ['piaster', '40 baras'], ['bishlek', '3 piasters'], ['¼ majeedy', '5¾ piasters'],
   ['½ majeedy', '11½ piasters'], ['majeedy (silver)', '23 piasters'],
   ['French franc (gold)', '109 piasters'], ['Turkish lira (gold)', '125 piasters'],
   ['British guinea (gold)', '137 piasters']],
  'Wages: a labourer 6 piasters a day, a boy 4, a craftsman 15–20, a mason 23 — one silver majeedy. '
  'A doctor’s visit 6–10; plowing hire 20 a day with a mule, 25 with oxen; the carriage to Jerusalem, 6. '
  'The Christian head-tax, one to two majeedy a year, ends about 1905–10 — after which army redemption costs 50 French gold francs, '
  '“beyond the reach of most persons.” One more reason to sail. — Shāhīn (1982), “Money, Weights, and Measures.”')),

CH(13)

sect('The ground and the line, together', 'The town starts leaving, and every road out is one this book has already walked')

ent('19th century', 'documents', False,
    'The twin town and the Rafeedie family',
 f'''One and a half kilometres from the centre of Ramallah there is a second town, al-Bireh. It is older than ours, larger than ours until our families came up the ridge in 1562 (after that, the registers count Ramallah at about twice its size), and Muslim where ours is Christian. From some point in the nineteenth century a Christian family has lived there, <b>the Rafeedie family</b> (al-Rafīdī). They came to al-Bireh, Sāmiḥ Ḥammūdeh tells us, from the village of Rafīdiyā in the Nablus district, and their name is simply that village worn into a surname{c('Sāmiḥ Ḥammūdeh (Birzeit University), <span class="ar">البيرة في فترة الاحتلال والانتداب البريطاني ١٩١٧–١٩٤٨</span>, in <i>Shuʾūn Filasṭīniyya</i>: al-Bīra’s Mandate-era population was the continuation of families settled there in the Mamluk and Ottoman periods — al-Ṭawīl, al-Qarʿān, al-Ḥamāyil, al-Ghazāwna — <span class="ar">وعائلة الرفيدي المسيحية، وقد وفدت إليها من قرية رفيديا، قضاء نابلس في العهد العثماني، في القرن التاسع عشر</span>: “and the Christian Rafeedie family, which came to it from the village of Rafīdiyā, Nablus district, in the Ottoman period, in the nineteenth century.” Ḥammūdeh is the author of <i>Ottoman Ramallah</i> (Institute for Palestine Studies) and of the 2014 article this book’s founding chapter is built on — he is the same historian, reading the same kind of register, for the town next door. <b>An honest qualification, added after the endnotes were obtained: Ḥammūdeh’s note on this sentence (endnote 9) is an explanatory aside about the 1948 refugees, not a citation, and he gives no source for the Rafeedie’s arrival from Rafīdiyā.</b> The nearest reference in the passage is his note 8, to Muṣṭafā Murād al-Dabbāgh, <span class="ar">بلادنا فلسطين</span>, vol. 8 pt. 2, p. 258, which supports the family-names list but which he does not attach to this sentence. <i>The claim is printed here as Ḥammūdeh’s assertion, on his authority as the historian of Ottoman Ramallah, and not as a documented finding.</i> The article appeared in <i>Shuʾūn Filasṭīniyya</i> 275–276 (2019); Ḥammūdeh died on 25 May 2019, aged 59, before the series of city studies he had planned could go further.')}. They belong in our story, and not only as neighbours.''',
 f"""
<p><b>The Rafeedie tell our own story back to us, in another town’s voice.</b> Rafīdiyā’s account
of itself goes like this. A Christian family of Ghassanid descent fled Karak to escape a forced
marriage between one of their women, Rafīd, and a Muslim prince. They settled beside Nablus and
divided the land and the water with the Muslim family already
there{c('The Rafīdiyā foundation account, in the form it circulates locally and in the reference literature: a Ghassanid Christian family in flight from al-Karak over a forced marriage, settling beside Nablus alongside the Ḥassūna family, with land and water divided equally. It is a tradition, and it is printed here as one.')}.</p>
<p>Set that beside our own story of Ghassān and of Karak, told in the chapters “Ghassān and a
Christian countryside” and “From Karak to Ramallah”. Ghassanid
Christians. Karak. A forced marriage refused. A flight north. A new village on a hill.
<b>It is the Ramallah story, with the names changed.</b></p>
<p>The parallel has a limit. The Rafīdiyā tradition dates the flight to the seventeenth century. Yet
the Ottoman defter, the tax register, of 1596 already records <b>eighty-five Christian households at
Rafīdiyā</b>, beside nine Muslim households and six bachelors. The Christian community was large and
long-established before the date the story gives for its founding. So the tradition cannot be a
literal account of a founding{c('Hütteroth and Abdulfattah (1977) for the 1596 <i>mufaṣṣal</i> figures at Rafīdiyā: 85 Christian households, 9 Muslim households, 6 bachelors. The arithmetic is the same objection this book has already made to its own “about 1550,” and to the 143 Christian households once claimed at Karak in 1562.')}.</p>
<p>What is it, then? Our answer is a reading, not a finding: <b>it is a form</b>. It is a way the
Christian communities of these hills, Ramallah, Rafīdiyā and others, have told their own origins for
a very long time. Ghassān for descent, Karak for the road, a refused marriage for the reason, a hill
for the destination.</p>
<p>Two towns forty kilometres apart, that never compared notes, tell the same shape of story. That is
not evidence that the events happened twice. It is evidence about how Palestinian Christians remember
themselves.</p>
<p>And a form is not a lie. It is what a people uses to carry a truth it cannot document. Here the
truth is this: <i>we are old here, we are Christian here, and we came to this hill because staying
where we were had become impossible.</i> Every part of that is true of our family, whether or not
Rāshid ever stood at a ford.</p>
<p><b>The ground under our neighbours is not a tradition at all.</b> Al-Bireh has been lived in
without a break for so long that the shape of the medieval town can still be read in the modern
street plan. Denys Pringle, the Crusader archaeologist who excavated it, writes that the general
layout of medieval al-Bireh <i>remains fairly clear in the twentieth-century street pattern, despite
over eight centuries of continuous habitation</i>{c('Denys Pringle, “Magna Mahumeria (al-Bīra): the Archaeology of a Frankish New Town in Palestine,” in <i>Fortification and Settlement in Crusader Palestine</i> (Routledge, 2023), ch. VI, 147–168, DOI 10.4324/9781003418405-6; and <i>The Churches of the Crusader Kingdom of Jerusalem</i> I (Cambridge, 1993), 161–165. Al-Bīra sits at 860 m on the Nablus road, 16 km north of Jerusalem. Medieval Islamic reoccupation is attested by the thirteenth century, evidenced by a hoard of 116 copper coins, Ayyubid and Mamluk, found in a cistern in 1951.')}.</p>
<p>The Frankish, or Crusader, new town there was Magna Mahumeria, which we met in chapter six. Its
charter of 1156 lists ninety-two burgesses, its townsmen, by name. Its parish church of St Mary is in
the record by <b>1128</b>, and the German pilgrim Theodoric described it in
1172{c('Palestinian Ministry of Tourism and Antiquities, site record for the church at al-Bīra: documented September 1128 under the jurisdiction of the Holy Sepulchre; described by Theodoric, 1172; a Romanesque basilica of roughly 22 × 35 m with three semi-circular apses; known as St Mary’s Parish Church, the Church of the Holy Family and the Church of the Visitation; probably converted to a mosque after Ṣalāḥ al-Dīn retook the town in 1195, and largely demolished by Turkish forces in the First World War for bridge stone.')}.</p>
<p>The old buildings are counted too. Riwaq’s registry of historic buildings, a Palestinian survey
that walked 422 localities between 1994 and 2007 and recorded 50,320 buildings, lists 381
historic buildings at Ramallah, the most in the governorate, and <b>168 at al-Bireh</b>. The al-Bireh list is dominated by the houses of al-Qarʿān, al-Ṭawīl, al-Ḥamāyil and
al-Qarāqira. These are the same families Ḥammūdeh names, arrived at independently, building by
building{c('Riwaq — Centre for Architectural Conservation, Ramallah, <i>Registry of Historic Buildings in Palestine</i>, browsable free at buildings.riwaq.org: 50,320 buildings in 422 localities, surveyed 1994–2007, with 400+ digitised maps and 45,000+ photographs. Ramallah and al-Bīra governorate: 71 localities, 7,618 historic buildings, of which Ramallah city holds 381 and al-Bīra 168. Three Riwaq restoration projects at al-Bīra, five at Ramallah. <b>The Ramallah list is given house by house under its owners’ names</b> — <span class="ar">دار حنا وجريس عيسى حنا حديد</span>, <span class="ar">دار بشارة حنا عقال</span>, <span class="ar">دار سالم غنام</span>, <span class="ar">دار مغنم</span>, the Ottoman court, the Ramallah hotel and dozens more. It is the nearest thing that exists to a house-by-house gazetteer of this town, it is Palestinian, and it is free.')}.</p>
<p>Underneath all of it, inside the modern streets, lies Khirbet Raddana, the farming village of the
early Iron Age (Iron I) that we mapped in chapter two. It was dug in salvage seasons between 1969 and
1974, and al-Bireh’s own growth has since built over it. Iron Age village, Frankish town, Ayyubid
coins in a cistern, Ottoman quarter, modern city: one continuous street plan.</p>
<p><b>The two towns are recorded together twenty-one years before the Christian families were counted
here.</b> A Jerusalem court record of 1541 has Ḥasan bin ʿAlī of the village of Ramallah doing
business with men from the village of al-Bireh{c('Jerusalem sharīʿa court records, 1541, in Sāmiḥ Ḥammūdeh, “New Light on Ramallah’s Origins in the Ottoman Period,” <i>Jerusalem Quarterly</i> 59 (2014). Note the date: 1541 is twenty-one years before the Christian settlement was counted in 1562, and the Ramallah party is one of the Muslim households already on the hill.')}.
So before there was a Christian Ramallah at all, the Muslim households on this hill were already
trading with the town next door. The relationship is older than the Christian settlement.</p>
<div class="fix"><div class="fixhead">And the thing the numbers say, which is the opposite of ours</div>
<div style="font-size:.95rem;line-height:1.65;color:#46423B">
<p style="max-width:none">Al-Bireh’s Christians were always a small minority in a large Muslim town —
<b>none at all in the register of 1596</b> (45 households, all Muslim); <b>72 of 1,479 in 1922</b>;
<b>248 of 2,292 in 1931</b>; <b>280 of 2,920 in 1945</b>. Never more than about a ninth of the
town{c('1596: Hütteroth and Abdulfattah (1977), p. 116 — 45 households, all Muslim, 4,570 akçe. 1922: Barron, <i>Report and General Abstracts of the Census of 1922</i>, p. 16 — 1,479 total, 1,407 Muslim, 72 Christian (61 Orthodox). 1931: Mills, <i>Census of Palestine 1931</i>, p. 48 — 2,292 total, 248 Christian. 1945: <i>Village Statistics, April 1945</i>, p. 26 — 2,920 total, 280 Christian. Of 23,012 dunums in 1945, 22,406 were Arab-owned and none Jewish-owned.')}.
<b>That is the exact inverse of Ramallah</b>, which was 2,972 Christian out of 3,104 in 1922.
<i>Two towns whose streets run into one another, with opposite religious arithmetic, and no record
of that ever having been the point.</i></p>
<p style="max-width:none"><b>We will not claim them as our own.</b> The Rafeedie are an
al-Bireh family, not a Ramallah clan; in America they have their own society, organised around
descent from their own town, as the Federation is organised around descent from ours. <i>They are
not part of this genealogy.</i> <b>They are part of this history</b> — which is a different claim,
and the truer one.</p></div></div>
<p>Jumping ahead a century, one Rafeedie we can name from the record is Wissām Rafeedie, journalist, of al-Bireh. He was
arrested at his home on 11 August 1994 and held under administrative detention orders, renewed for
twenty-one months, until the United Nations Working Group on Arbitrary Detention declared the
detention <b>arbitrary</b> in 1996{c('UN Working Group on Arbitrary Detention, <i>Rafeedie v. Israel</i>, Opinion No. 17/1996, 23 May 1996 — residence given as “El Bireh, West Bank”; arrested 11 August 1994; the Working Group found the detention arbitrary, citing the absence of effective appeal and its duration.')}.</p>
<p>He wrote a novel in prison on Red Cross booklets, and it was confiscated. He got a second copy out
in miniature handwriting hidden in pill capsules, and it was printed in <b>Ramallah</b>, in
1998{c('Wissām Rafeedie, <span class="ar">الثالوث الأصولي</span> (<i>The Trinity of Fundamentals</i>), written from 1993 in al-Naqab (Ktzi‘ot) prison, printed in Ramallah in 1998 after his release; English translation 2024.')}.
An al-Bireh man’s book, printed in our town. That is what the bond between these two places looks
like, and it did not need a shared family tree.</p>
<div class="fix"><div class="fixhead">Two things this book was offered and would not print</div>
<div class="fixgrid">
<div><span class="fl">Not printed</span><b>That Judge Edward Rafeedie of the U.S. District Court was of the al-Bīra family.</b> He was born in Orange, New Jersey, on 6 January 1929 to Palestinian immigrants, and <i>no source names their town</i>. The surname is a nisba from Rafīdiyā and is carried by families in several places. A famous name is not evidence.</div>
<div><span class="fl">Not printed</span><b>That the Rafeedie are “Nestorian.”</b> One Arabic wiki says so; al-Bīra’s Christians in the Mandate censuses are overwhelmingly Greek Orthodox, and there is no Church of the East community in this district. The claim has no source that will bear weight.</div>
<div><span class="fl">How it is justified</span>The same rule this book applies to its own family: <b>a claim is printed at the strength of the document behind it, and a claim with no document is named as one.</b> The Rafeedie deserve the same care as the Ḥaddādīn — which means not decorating them either.</div>
</div></div>
<p><b>What we still don’t know.</b> Ḥammūdeh gives no source for the Rafeedie’s arrival from
Rafīdiyā, so we do not yet know where his account comes from. No source names the town of Judge
Edward Rafeedie’s parents. And no diocesan record has yet been found for St Andrew’s of 1887.
Readers who hold any of these answers can help us complete the story.</p>"""),

ent('1901', 'oral', True, 'The first four sail for America',
 'As the twentieth century opened, our town still lived under Ottoman rule. In 1901, by Shāhīn’s account, the first Ramallah men began to emigrate to the United States{}. Saleh Abdel Jawad names another man, Yūsuf ʿOdeh, brother of the first mayor, as “the first emigrant from Ramallah,” without a year, and notes that some whole families left before the war (<i>Jerusalem Quarterly</i> 36, p. 30). The same year the Turkish carriage road from Jerusalem to Nablus was finished, and the Friends Boys School opened, in rented rooms; it closed in the war and reopened in 1919 in the building it still uses. The old ridge road became a modern road, and the first men left on it.'.format(c('Shāhīn (1982): emigration to the United States begins in 1901 — Esa Izhak ʿEadeh, Hanna ʿAazar Hishmeh, Esa Salah Jaghab and Esa Khashan the first four (1900 or 1901), seven more named in 1903; before 1914 the only entry requirement was eyes free of trachoma.')),
 f"""
<p>Leaving has its own family tree, and ʿAzīz Shāhīn, who wrote our town’s great history in 1982,
sets it down name by name. The first to leave at all was <b>Ibrahim of the Hassaan clan</b>, in the
seventeenth century. He went to ʿIsifyā near Haifa, and four hundred of his descendants live there
today.</p>
<p>The first to go abroad was Hanna Ibrahim Saah, in 1858, to Constantinople. The first to go west
went to England, in 1895. And in 1898 came <b>the first cheque the town had ever seen</b>, sent from
Brazil: 100 French gold francs, “and it created quite a sensation.”</p>
<p>The early emigrants were men over thirty who meant to come home, and almost all of them did.
<b>Their children did not.</b> That one fact tells much of the story of our town’s people ever
since.</p>
{fig(ATLAS.fig_diaspora(),'Where Ramallah went, 1901 onward',
 'The cities our people went to, weighted by the family’s own record: Detroit above all, then Jacksonville, New York and San Francisco. Nobody has ever made a full count of this diaspora, our community abroad.',
 'Shāhīn (1982) for the start date and the named firsts; the Federation’s conventions for the cities.')}"""),

ent('1901–1904', 'documents', False, 'Elihu Grant writes the town down',
 'Most of what we know about how Ramallah lived comes from ʿAzīz Shāhīn, who lived it. <b>Elihu Grant</b> was superintendent of the American Friends Schools at Ramallah and Jerusalem from 1901 to 1904. He happened to be counting the same houses at the time, so his notes let us put dates on what Shāhīn remembered. Shāhīn is our source, and Grant is our clock. In 1907 Grant published <i>The Peasantry of Palestine</i>, two hundred and fifty-five pages on village life, with a chapter on Ramallah and al-Bireh by name{}.'.format(c('Elihu Grant, <i>The Peasantry of Palestine: The Life, Manners and Customs of the Village</i> (Boston: Pilgrim Press, 1907), 255 pp. with 39 leaves of plates — the c. 340-page figure belongs to the enlarged edition of 1921, <i>The People of Palestine</i>; the title page describes him as “Resident (1901–1904).” Chapter IX, from p. 187, is “Village life in the concrete. Description of actual villages, Ram Allah and el-Bireh”; chapter X covers eṭ-Ṭīreh, ʿAyn ʿArīk, Baytīn, Dayr Dīwān, eṭ-Ṭaybeh, Jifnā, ʿAyn Sinya, Bīr Zayt, ʿAbūd and Mukhmās — nearly every village on this book’s district map. ' + D('peasantryofpales00gran.pdf') + '.')),
 f"""
<p>Grant counted things. Down one street south of the market he recorded <b>twenty-two houses, one
store and one silversmith’s shop</b>, and he measured seven hundred and eighty feet to the threshing
floor. He gave the price of meat at Ramallah: eight to twelve cents a pound, depending on the season.
He also dated the carriage road from Jerusalem exactly. It opened in May 1901 and ran fifteen
kilometres to al-Bireh{c('Grant (1907), 191–96 for the street survey, the market and the threshing floor; 189 for the road: “It was in May, 1901, that the road mentioned was opened up for use from Jerusalem to el-Bireh, a distance of fifteen kilometers.” <i>Shāhīn dates the same road to 1901; Grant, who used it, gives the month.</i>')}.</p>
<p>Grant also read the town’s history in its buildings. In 1903 he could see four kinds of house
standing side by side. The oldest were the <i>skīfeh</i> huts: stone bedded in earth, with dirt roofs
laid on boughs. Next came dressed stone and mortar with rolled earth roofs. Then came the heavy arched
stone dome roofs, which by then were <b>the majority in Ramallah</b> and rare in al-Bireh. Newest were
the houses of several rooms, with modern windows, paved floors and cisterns, which the wealthier
villagers were putting up as he watched. <i>“The development of several centuries in highland peasant
homes may thus be traced.”</i> He was reading our town’s whole economic history off its own walls,
standing in the street.</p>
<p>One of his notes matters for everything we say about land. Ramallah’s people had bought fields in
<i>a dozen or more villages</i>, as far out as ʿAyn Qīniya, Mukhmās and Dayr Dīwān. <b>For those
outside lands they held no government deeds</b> (<i>kushān</i>, plural <i>kuwashīn</i>).
The title stayed in the register with the original village{c('Grant (1907), 191–92: “The needs of Ram Allah are so much in excess of the lands which are legally recorded as belonging to it that its people have bought tracts here and there all about the country… For such outside lands the Rām Allah people have no government deeds (<i>kushān</i>, plural <i>kuwashīn</i>), the title resting, so far as the government records are concerned, with the original village.”')}.</p>
<p>So our town’s wealth had outgrown its own land, and much of that land was held without paper.
This was a place about to start sending its sons to America, and Grant, who arrived in 1901, the
year the first four sailed, was there to write it down.</p>
<p>Without meaning to, Grant also confirms a picture we have drawn all through our history. He lists
the Christian villages of the central highlands: <b>Ramallah, Beit Jala, eṭ-Ṭaybeh and Jifnā</b>.
Christians outnumber Muslims at Birzeit, ʿAyn ʿArīk and ʿAbūd. This is the same band along the ridge
that the Ottoman register of 1596 describes three hundred years earlier, and that the Byzantine
churches describe a thousand years before that. Different observer, different language, different
century: the same map.</p>"""),

ent('1902 · 1908', 'documents', True, 'Ramallah becomes a city, clan by clan',
 'In 1902 Ramallah was made a district seat, the centre of government for thirty villages. As Shāhīn puts it, “Till 1902 there had been no government rule in the villages and small towns of Palestine.”{} In 1908, the municipality’s own date, Ramallah was incorporated as a city, with Elias ʿAudi as its first mayor; Saleh Abdel Jawad gives April 1910 for his taking office (<i>Jerusalem Quarterly</i> 36, p. 30). Its council had <b>one representative from each clan</b>. The ḥamūla, or clan, structure of 1562 had become, quite literally, the town’s constitution.'.format(c('Shāhīn (1982): the district of 1902 under mudīr Ahmad Murad, and the incorporation of 1908 — Elias ʿAudi mayor, Assʿad Ibrahim Kassees secretary-treasurer; compare Zeʾevi, <i>An Ottoman Century</i> (1996).')),
 fig(F3.fig_town_plan(),'The town, as Shāhīn drew it',
  'Central Ramallah after the sketch map in Shāhīn’s own book. The dashed ring is the original village: the eight clans’ quarters and their guest houses, all within walking distance. Everything numbered outside it was built later: the church of 1850, the Catholic mission of 1857, the Friends schools, the Meetinghouse of 1910, and the hospital the diaspora paid for in 1963. Note the two roads south. One is the old track from El Sharafa, where the town said goodbye to its emigrants. The other is the carriage road of 1901 through El Bireh, which replaced it.',
  'After Shāhīn (1982), p. 69, simplified; institution dates from his own chapters.')),

ent('1904 · 1908', 'documents', False, 'The Patriarchate counts its flock',
 'In 1904 the Orthodox Patriarchate of Jerusalem estimated its own people, parish by parish, for its schools. Of 49,596 people in the whole Patriarchate, <b>Ramallah had 4,500</b>, second only to Jerusalem’s 6,000; Beit Jala had 4,340 and Bethlehem 3,600. That is an estimate, and a generous one: a year later the town’s own census counted 3,214 people in all. Karak had 1,600. So the two ends of our family’s road appear in one table, written by the church our family never left.{}'.format(c('Sir Anton Bertram &amp; H. C. Luke, <i>Report of the Commission appointed by the Government of Palestine to inquire into the affairs of the Orthodox Patriarchate of Jerusalem</i> (Oxford, 1921), §9, p. 9 n. 1: “In an official estimate prepared by the Patriarchate for the purposes of its schools in 1904 … Jerusalem 6,000, Bethlehem 3,600, Beit Jala 4,340, Ramallah 4,500 … Es Salt 3,000, Kerak 1,600.” ' + D('1921_Bertram_Luke_Report_Orthodox_Patriarchate_Jerusalem.pdf') + '.')),
 f"""
<p>The same report names a quarrel that runs underneath the rest of our church history. The parishes,
the parish priests and the people spoke Arabic. The Patriarch and the Brotherhood of the Holy
Sepulchre, which governed them, were Greek. The laity are the ordinary members of the church, as
against its clergy. <b>When the Ottoman constitution was restored in 1908, the Arab Orthodox laity
began a long and bitter fight for a share in running their own church</b>{c('Bertram &amp; Luke (1921), §§11–14: the laity and parochial clergy “almost exclusively Arabic-speaking”; “the bitter and prolonged struggle with the local Arabic-speaking laity which arose on the declaration of the Turkish Constitution in 1908.” The commissioners were British officials of the Mandate government; their report is used here for its figures and its record of the dispute, not for its judgements.')}.</p>
<p>Ramallah, with the largest Orthodox parish outside Jerusalem, was in that fight from the start.</p>"""),

ent('12 June 1905', 'oral', False, 'The last big fight',
 'On 12 June 1905 a wedding procession went through the narrow streets, and a quarrel broke out over clan songs. It became a <b>three-hour stone-throwing battle</b> between the Hadadeh and the Hamayel, fought from the rooftops, with the women refilling the trays of stones. Nobody was killed{}. The whole town was jailed together in Jerusalem, and released together when the church pleaded for it. The 1905 census counts 3,214 people in the eight clans, and every one of them seems to have been on a roof.'.format(c('Shāhīn (1982), “Ramallah’s Last Big Fight,” 12 June 1905; the 1905 clan census total of 3,214 from the population chapter.'))),

ent('1914–1918', 'oral', True, 'The war, the locusts, the typhus',
 'About thirty Ramallah men died in the Turkish army in the war of 1914–1918. The locusts of 1915 spared no crop. In <b>1916 typhus killed a large part of the town, and Shāhīn puts it near a third</b>{}. No independent record of it survives, so we read the figure as family memory rather than a measurement. The counts on either side, 3,214 in 1905 and 3,104 in 1922, do not require a loss that large, and heavy emigration accounts for much of the gap. <b>The British Army took Ramallah on the morning of 29 December 1917, without a fight.</b> 27 December, which is sometimes given, is the date of the Ottoman counter-attack on Jerusalem.'.format(c('For 29 December: General Allenby’s despatch, <i>London Gazette</i> supplement of 6 November 1918, p. 13101, “On the left the 74th Division occupied Ram Allah”; and W. T. Massey, <i>How Jerusalem Was Won</i> (London, 1919), ch. XVI, “Ramallah had been taken at nine o’clock in the morning without opposition by the 230th and 229th Brigades.” Earlier editions of this book said no published source recorded the day. Shāhīn (1982): the war dead, the locust plague of 1915, and the typhus of 1916 — “about 30% of Ramallah’s population perished”; among the dead, Dr Maʿlouf, and the child in the family photograph on p. 30.')),
 f"""
{fig(F3.fig_war_strip(),'The dark half-decade, 1914–1918',
 'Four blows in five years. The middle one may be the largest demographic event in the town’s recorded history, and no government count sits close to it on either side: the Ottoman count of 1905 and the British census of 1922 are sixteen years apart. We know of it because Shāhīn wrote it down, and because his own doctor died in it.',
 'Shāhīn (1982), the war chapters; Schick (1896) and Barron (1922) for the counts that bracket the epidemic without recording it.')}
{FIX('A population curve drawn smoothly through 1896 (2,061) and 1922 (3,104).',
 'The curve must show <b>1916</b>: about 30 per cent mortality, drawn as a labelled inference.',
 'Shāhīn records the epidemic and its scale; no census sits on either side of it, so the chart shows the event as a dashed line explicitly marked “inferred shape, not data.” No figure in this book invents a data point.')}"""),

ent('1922–1944', 'documents', False, 'The counting years',
 'After the war Britain ruled Palestine under the Mandate, and the Mandate government counted everything. For once our town can be set out in tables.',
 f"""
{NUMTABLE('EVERY COUNT OF RAMALLAH, 1838–1953 — as Shāhīn assembles them',
 ['Year', 'Count', 'Counted by'],
 [['1838', '800–900', 'Robinson and Smith, travellers'],
  ['1839', '200 Greek Orthodox families', 'Anthemos, secretary of the Patriarch'],
  ['1870', '249 houses; 635 males', 'A. Socin’s Ottoman village list, <i>ZDPV</i> 2 (1879), p. 158, marked uncertain in the original. A household multiplier puts the total near 2,000, but that is inference, not Socin. Another estimate the same decade: ~1,100'],
  ['1905', '3,214', 'census, by the eight clans'],
  ['1922', '3,104 — 125 Muslims, 7 Jews', 'British census, 23 October'],
  ['1931', '4,286 in 1,014 homes', 'British census, village list (its towns tables print 4,287)'],
  ['1941', '≈ 5,000', 'British estimate, 1 January'],
  ['1944', '6,300 (4,885 natives)', 'ration-card distribution — the government <i>Village Statistics</i> of April 1945 give 5,080'],
  ['1953', '13,500 (natives + 8,500–9,000 refugees)', 'a local count — <b>Jordan held no census in 1953</b> (its censuses are 1952 and 1961)'],
  ['1953', '+ 2,580 in the United States', '“the total number of Ramallah people in 1953 was 7,080”']],
 'Shāhīn (1982), citing Kaddoura (1954), pp. 136–37, and the British census reports; Barron (1923); Mills (1932).')}
{NUMTABLE('THE 1944 RATION-CARD CENSUS — the eight clans of 1562, still countable',
 ['Clan', 'Persons'],
 [['ʿAwwaad', '625'], ['Sharaka', '650'], ['Yousef', '750'], ['Jaghab', '675'],
  ['Shakara', '660'], ['Jirius', '550'], ['Ibrahim', '775'], ['Hassaan', '200'],
  ['<b>Natives</b>', '<b>4,885</b>'], ['Outsiders', '1,415'], ['<b>Total</b>', '<b>6,300</b>']],
 'By religion: Greek Orthodox 3,570 · Roman Catholic 1,080 · Greek Catholic 700 · Episcopalian 325 · Friends 200 · Muslims 425. — Shāhīn (1982).')}
{fig(R.fig_sex(),'What emigration looks like in a census',
 'Mills, 1931: 1,941 men against 2,345 women in the village list (the towns tables of the same census print 1,942 men). A deficit of four hundred men in a town of four thousand is the men who left after 1901, counted by their absence.',
 'E. Mills, Census of Palestine 1931, the Ramallah tables.')}
<p>The 1922 census shows the missing men another way. In Ramallah it counted <b>170 widowed or
divorced women against 92 men</b>. In Beit Jala, the other town of emigrants, it counted 285 women
against 41 men. Ramallah had 576 married men and 736 married women: <i>a hundred and sixty wives whose
husbands were not in the town on census day</i>{c('J. B. Barron, <i>Palestine: Report and General Abstracts of the Census of 1922</i> (Jerusalem, 1923), Table XX, “Civil Condition Return for Municipal Areas”: Ramallah married 576 M / 736 F, widowed and divorced 92 M / 170 F, single 817 M / 713 F, total 3,104; Bait Jala married 463 / 523, widowed and divorced 41 / 285, single 876 / 913, total 3,101. That the missing husbands were abroad is this book’s reading of the figures, not the census’s statement.')}.</p>
<p>Two new things reached the town in these years: electric light and radio. In <b>1935</b> the Jerusalem Electric Company ran its
lines up from Jerusalem. The current was switched on at what is now al-Manāra square, with the mayor,
Dr Saʿadallah Kassees, present{c('Ramallah Municipality, “تاريخ البلدية” (History of the Municipality), ramallah.ps/ar/Article/3217. Shāhīn (1982), “Outstanding Dates in Ramallah’s History,” gives <b>1936</b>: “Electricity comes to Ramallah from the Jerusalem Electric Company. Most homes soon had electric lights.” N. Shaheen (2005) gives <b>1934</b>. The municipality’s year is printed; the other two are noted.')}.</p>
<p>From the end of March 1936 the voice of the country came out of Ramallah. The Palestine
Broadcasting Service spoke from Jerusalem, but <b>its main transmitter stood in Ramallah</b> until
1948{c('Andrea Stanton, “Situating Radio in the Soundscape of Mandate Palestine,” <i>Jerusalem Quarterly</i> 86, pp. 101 and 109–10, citing <i>Filasṭīn</i>, 1 April 1936, p. 5.')}.</p>"""),

ent('1938', 'documents', False, 'The revolt reaches the town',
 'In the autumn of 1938 the great Palestinian revolt against British rule came to Ramallah. The post office and telephones were removed, and six hundred British soldiers were expected, to occupy two old hotels. There were two fights a week apart, on 25 September and on Saturday 1 October, when fighters from across the country gathered in the town. British forces attacked them with machine-gun trucks and, after some hours, with aircraft, which bombed the thickest of the fighting. No one number for the dead can be printed as fact: the witnesses run from “more than twenty” to about eighty. Among them were <b>two women and three men bombed as they ran home from their vineyards</b>{}.'.format(c('Nancy Parker McDowell, <i>Notes from Ramallah, 1939</i> (Richmond, Ind.: Friends United Press, 2002), pp. 9–17: the letters and journal of a young American teacher at the Friends school, September–December 1938 — the six hundred soldiers expected and the hotels taken (p. 9); the battle of 1 October and its dead, from her journal of 8 October (pp. 13–14) and a letter (pp. 16–17); “Ramallah has become a rebel town” (p. 16). ' + D('1939_McDowell_Notes_from_Ramallah.pdf') + '.')),
 f"""
<p>This is the first time in our story that the town itself is a battlefield. The first witness was an
outsider: a Quaker teacher at the Friends school, watching from the school roof and writing home to
her family.</p>
<p>The second witness was one of our own. <b>Khalil Totah</b>, born in Ramallah in 1886 and head of the
Friends Boys School, kept a diary through the revolt.</p>
<p>On 5 September 1938 the fighters attacked the police station. On 9 September they entered the
magistrate’s court and took its typewriter. The British shut the court and the post office and carried
both to Jerusalem. That night <b>five to eight hundred armed men</b> closed the roads into the town,
marched through it and raised an Arab flag on a house. On 16 September three armed men took the
typewriters and the duplicator from the district offices.</p>
<p>Totah dates the great battle to <b>25 September</b>. He tells of six British aircraft, and of
fighting from the armoured car at al-Manāra to the al-Bireh crossroads. The Quaker letters put their
battle on Saturday 1 October, and the British government’s own report for 1938 agrees with them: on 1 October “a British police inspector was fatally wounded at Ramallah by a band,” which “was later engaged and suffered some 50 casualties.” So these are two fights, a week apart. Totah also records the plan for the soldiers: 260 in the Friends school and 400 in government schools and hotels.</p>[[C45]]
<p>In October three men of the town stole two typewriters, and Totah complained. <b>The rebels then
held a court in Ramallah</b>, returned the machines and punished the thieves{c('Thomas M. Ricks, ed., <i>Turbulent Times in Palestine: The Diaries of Khalil Totah, 1886–1955</i> (Jerusalem and Ramallah: Institute for Palestine Studies and PASSIA, 2009), diary entries of 5, 9, 16 and 25 September and October 1938, as set out in “Ramallah and the Great Palestinian Rebellion in the Diaries of Khalil Totah (1938–1939),” Institute for Palestine Studies, 7 March 2023, palestine-studies.org/en/node/1653696 (pp. 231–32 of Ricks for the police-station attack; the other page numbers are still to be checked in Ricks). The article notes that the 25 September battle may be the one at Wadi Shaiban, in which some sources count seventy-five fighters killed. On the rebel courts across the country, which sat “in business places or school buildings” and heard ordinary disputes as well as political cases: Charles W. Anderson, “State Formation from Below and the Great Revolt in Palestine,” <i>Journal of Palestine Studies</i> 47:1 (2017), pp. 45–47.')}.</p>"""),

ent('1946', 'documents', False, 'The town votes by clan',
 'On <b>Monday 15 April 1946</b>, from nine in the morning, the men of the Ḥaddāda went up to the municipal building. They were choosing four councillors out of five candidates. The other three seats were already filled, because nobody had stood against the one man nominated in each of the other three districts. The districts were the clans. Dār Jiryis was district 1, the Ḥaddāda district 2, Dār Ibrāhīm district 3 and al-Shaqara district 4. Nearly four centuries after the settlement, our town’s first families were still the units in which it voted{}.'.format(c('Israel State Archives, file P-213/40: the election file of the Jerusalem advocates Anton and Hanna Atalla, 1945–46, 208 scanned pages without a text layer. The electoral committee’s own Arabic summary, items 1–13 (PDF pp. 70–72); the English notice of 6 April 1946 signed by Mousa Khalil, chairman of the electoral committee (PDF p. 91); the committee’s minutes from 16 November 1945 (PDF p. 131). ' + D('1946_Ramallah_Municipal_Election_File_Atalla_ISA_P-213-40.pdf') + '. Read for this book from the scans on 7 November 2026; the typed pages are read in full, the lawyers’ handwritten notes only in part.')),
 f"""
<p>An electoral committee was named in the autumn of 1945 to run the vote. It first sat on 16 November
1945 under Khalīl Ṣalāḥ. When he fell ill, <b>Mūsā Khalīl</b> took the chair, by notice in the Official
Gazette no. 1465. The other members were Sālim al-Zaʿrūr, Ḥannā Jiryis, Khalīl Mubārak, Ḥannā Khalaf
and Khalīl al-Qassīs.</p>
<p>Registration ran from 15 November to 15 December 1945. The register, the list of voters, was posted
on <b>1 February 1946</b> for fourteen days. Objections were heard on 21 February, and the chairman
signed the register on 17 March. Its names were taken from the municipal tax registers. In Mūsā
Khalīl’s words, every person paying taxes was put on the register, whether he had applied or not.
Nobody under twenty-one could vote{c('Israel State Archives, P-213/40: the committee’s summary, items 1–7 (PDF p. 70); the evidence of Mūsā Khalīl, 23 November 1946, points 1–5 (PDF p. 55); the lawyers’ notes on qualification (PDF p. 5). Every name read for this entry on the voters’ lists is a man’s.')}.</p>
<p>The register counted the clans. The committee numbered the voters district by district: the
Ḥaddāda from 1 to <b>401</b>, Dār Ibrāhīm to 55, al-Shaqara to 84 and Dār Jiryis to 43 or 13. The figure for
Dār Jiryis is hard to read in the original. Its list of names holds thirteen, but every house’s list holds fewer names than the register, so the list alone cannot settle it. The lists of names break the Ḥaddāda into the same four
houses that the ration-card count of 1944 gives (see “The counting years”): Dār Abū Jaghab, Dār Yūsuf, al-Sharāka and Dār ʿAwwād.</p>
<p>Two further columns stand apart. One is the Ḥasāmna. The other is <i>al-aghrāb</i>, “the
strangers”: men living in the town but outside its families, among them Muslim and Armenian
names{c('Israel State Archives, P-213/40: the committee’s minutes of 26 January 1946 (PDF p. 131); the list of voters by house, “exhibit P.4” in the case (PDF pp. 117–124). The minutes do not say which district the Ḥasāmna and the strangers voted in. These are first readings of poor scans: the full list is still to be transcribed and checked.')}.</p>
<p>The names on the lists are the families of our tree. On the lists by house, <b>407 names</b> can be
read: Jaghab 75, Yūsuf 78, Sharāka 89, ʿAwwād 57, Dār Ibrāhīm 32, Dār Jiryis 13, Shaqara 12, Ḥasāmna 5
and 46 strangers. Each house is a clan of the Ramallah Family Tree.</p>
<p>We matched the 361 clan names against the tree. Of these, 106 are one man in the same clan, and 111
could be one of several. 27 match a man of the same name only in another clan. <b>The other 117 are
not in the tree at all.</b> They are men of Ramallah,
alive and of age in 1946, whom the tree has still to take in{c('The lists by house (PDF pp. 117–124), transcribed for this book in November 2026, and matched to the Ramallah Family Tree export of 3 November 2026: men not born after 1926 and not dead before 1946, with the father’s name checked where the list gives it. The lists hold fewer names than the register numbers above, because some pages are faint and the lists may not be complete. The review list is with John Mogannam, and nothing in the tree has been changed from it.')}.</p>
{NUMTABLE('RAMALLAH MUNICIPAL ELECTION, 1946 — the result',
 ['District', 'Candidate', 'Votes'],
 [['1 · Dār Jiryis', 'Boulos Jiryis Sābā', 'unopposed'],
  ['3 · Dār Ibrāhīm', 'Khalīl Sālim Ḥanāniyā', 'unopposed'],
  ['4 · al-Shaqara', 'Ḥannā Samʿān Khalaf', 'unopposed'],
  ['2 · the Ḥaddāda', 'Jamīl Ṭūṭaḥ', '255'],
  ['2 · the Ḥaddāda', 'Yūsuf Qaddūra', '236'],
  ['2 · the Ḥaddāda', 'Khalīl Ṣalāḥ', '222'],
  ['2 · the Ḥaddāda', 'Jalīl Ḥarb', '215'],
  ['2 · the Ḥaddāda', 'Ḥannā Jābir', '154 — not elected']],
 'Nominations were taken at the municipality on Saturday 6 April 1946, and the poll for district 2 was announced in <i>Filasṭīn</i> on 7 April. The English notice gives the district 4 member as “Sama’an Khalaf”; the committee’s Arabic gives <span class="ar" dir="rtl">حنا سمعان خلف</span>. — Israel State Archives, P-213/40, PDF pp. 72 and 91.')}
<p>One of the four winners in district 2 carries a name we know. <b>Yūsuf Jiryis Kaddoura</b> (Yūsuf Qaddūra in the
table), second in the poll, has the name of the author of our town’s first history, published in New York in 1954, which
we meet again in the next chapter. Shāhīn gives the author’s full name as Yūsuf Jiryis Qaddūra, the
same full name as the councillor’s. That they are the same man is likely, but not yet shown.</p>
<p>The result was taken to law. The Atalla file, the election papers of the Jerusalem lawyers Anton
and Hanna Atalla, holds the lawyers’ notes of hearings on <b>23 November
and 7 December 1946</b>. Mūsā Khalīl gave evidence for the committee. The presiding officer of the poll,
Shafīq Musallam of the Ramallah district office, said polling ran from nine to half past twelve and
again from half past one to about five.</p>
<p>The notes argue over how the register was published. They also argue over men with a right to vote
in more than one district: against each such man, the lists mark whether he owned or rented in the
other district. Mūsā Khalīl said that none of the men from other districts who could have voted in the
Ḥaddāda chose to, and the notes put them at about ten{c('Israel State Archives, P-213/40: evidence of Mūsā Khalīl, 23 November 1946 (PDF p. 55); of the presiding officer and of a police corporal, 7 December 1946 (PDF p. 42); the lawyers’ points on publication and on the districts (PDF pp. 3–9); the lists of men entitled to register in a second district, with “owner” or “tenant” against each (PDF pp. 135–141).')}.</p>
<p><b>What we still don’t know.</b> We do not yet have the names of those killed when the revolt of
1938 reached the town, the houses burned, or what the revolt cost the families that stayed. We do not
know who brought the election case of 1946, or how it was decided. We are still looking for exhibit
P.5, the register itself as shown in court, which Mūsā Khalīl said gave each voter’s age, and for the <i>Filasṭīn</i>
notice of 7 April 1946. The 1946 lists of names are still to be fully transcribed and checked, and we
have not yet shown that the Yūsuf Kaddoura of the poll is the author of the 1954 history. If your
family’s papers hold any of these, we would like to hear from you.</p>"""),

ent('1948', 'documents', False, 'The catastrophe of 1948',
 'In the summer of 1948 the war reached Lydda and Ramle, west of our hills. On <b>11 July 1948</b> Israeli forces took Lydda, and Ramle surrendered the next day. At half past one on 12 July Yitzhak Rabin signed the order to expel the inhabitants. On the morning of the 13th the people of Lydda were marched east on foot in the July heat. Somewhere between fifty and seventy thousand people were driven out of the two towns, and an unknown number died on the road. The Arab Legion, the army of Jordan, picked up the survivors and brought them to Ramallah. Ramallah was not destroyed. <b>Ramallah opened its doors and was tripled.</b> People were taken into every madafa, the clan guest house, every schoolroom, and every qaṣr, the stone field house, in the fig groves. A local count of 1953 gives some 13,500 souls: about nine thousand refugees and four and a half thousand Ramallah natives. With 2,580 in America, that is the figure behind Shāhīn’s total of 7,080 Ramallah people in the world{}. The town’s own money went at the same time. The deposits in Bank al-Umma were frozen, not lost, as part of the wholesale freezing of Palestinian bank accounts that year. The town’s pig-farming venture collapsed with over $400,000 in it, and some 200 Mandate salaries simply stopped{}. Shāhīn saw it himself in 1951–52: <i>“The future looked grim and the morale of the people was at its lowest ebb.”</i>'.format(
  c('Shāhīn (1982), “The Great Influx of 1948,” with the figures of the local count of 1953.'),
  c('Shāhīn (1982): the swine venture, the Bank El Ummeh closure, and the 200 lost government jobs — “all of these misfortunes occurred within three or four years.”'))),

ent('1949 → 1957', 'documents', False,
    'Where the refugees lived',
 f'''The refugees who reached Ramallah in July 1948 went into five camps, and the official lists add a small sixth at Silwād (453 people in the census of 2017). One, Qaddūra, is <b>inside Ramallah itself</b>{c('The camp figures throughout this entry are from the Applied Research Institute–Jerusalem (ARIJ) locality profiles for Qaddura, al-Amʿari, al-Jalazun, Qalandiya and Deir ʿAmmar (2012), which carry PCBS 2007 population counts; and from UNRWA’s camp pages for registered-refugee totals. '+D('2012_ARIJ_Qaddura_Camp_Profile.pdf')+' · '+D('2012_ARIJ_al-Amari_Camp_Profile.pdf')+' · '+D('2012_ARIJ_al-Jalazun_Camp_Profile.pdf')+' · '+D('2012_ARIJ_Qalandiya_Camp_Profile.pdf')+'.')}. Al-Amʿarī, al-Jalazūn and Qalandiyā are within about six kilometres, and Dayr ʿAmmār is twelve kilometres north-west.''',
 f"""
{NUMTABLE('The camps of this district', ['camp','where','set up','on whose land','who is in it','2017'],
 [['<b>Qaddūra</b>','inside Ramallah city, 0.5 km east of the centre','1948','<b>private land</b> — so UNRWA never recognised it as a camp','Dayr Ṭarīf, al-Lidd, Lifta, al-Ramla, Jaffa, Qālūniya, ʿImwās','924'],
  ['<b>al-Amʿarī</b>','al-Bīra, 1.4 km east of Ramallah centre','1949','leased by UNRWA from the Jordanian government','al-Ramla, al-Lidd, Jaffa, Haifa','4,725'],
  ['<b>al-Jalazūn</b>','5.3 km north of Ramallah','1949, named for a spring','rented from a private owner in Jifnā, by most accounts; no lease document is public','thirty-six villages (the encyclopedia of the Institute for Palestine Studies counts forty-six) of Lydda, Ramle, Haifa and west of Hebron; chiefly Bayt Nabāla and al-Lidd','8,201'],
  ['<b>Qalandiyā</b>','the southern entrance to Ramallah; Jerusalem governorate','1949','leased by UNRWA from the Jordanian government','the Jerusalem-corridor villages — ʿAllār, Lifta, ʿArtūf, Khirbat al-Lawz, ʿIshwaʿ, Ṣarʿa','8,336'],
  ['<b>Dayr ʿAmmār</b>','12 km north-west','1949 (UNRWA)','land of non-refugee villagers of Dayr ʿAmmār and Jammāla','Bayt Nabāla, Dayr Ṭarīf, Ṭīrat Dandan, al-Sāqiya','—']],
 'Populations are PCBS 2017 for the camp localities; UNRWA’s registered-refugee rolls are far larger, because they count the descendants wherever they now live — al-Amʿarī, 97 dunums, carries 15,315 registered refugees.')}
<p>Look at where each camp’s people came from, and the map of 1948 comes together. Qalandiyā holds the
villages of the Jerusalem corridor. Al-Amʿarī and al-Jalazūn hold Lydda, Ramle and Jaffa. <i>The people
who walked east out of Lydda on 13 July settled where they could walk no further.</i>{c('Lisa Taraki, “Enclave Micropolis: The Paradoxical Case of Ramallah/al-Bireh,” <i>Journal of Palestine Studies</i> 37:4 (2008), p. 10: “The vast majority of refugees who made their way to Ramallah/al-Bireh in the hot days of July 1948 were peasants from villages near al-Lidd (Lydda), Ramla, and Jaffa who settled — often after several temporary relocations — in al-Bireh, Qaddura refugee camp, and later in Amʿari and Jalazon camps.” '+D('2008_Taraki_Enclave_Micropolis_Ramallah_al-Bireh_JPS37.pdf')+'.')}</p>
<p>Counting the people of a camp is not simple. UNRWA is the United Nations agency for Palestine
refugees. Its own page for al-Jalazūn, as we read it in September 2026, says “around 9,450 refugees live in Jalazone camp.” Two lines
later it gives the camp as 0.253 km² at “an estimated population density of 51,383 per sq km.”
Multiply the two and you get thirteen thousand: <i>51,383 × 0.253 = 13,000.</i> <b>The density was
worked out from a population of thirteen thousand, and printed beside a headline of nine thousand four
hundred.</b> The difference is inside one page, not between sources. It is the difference between the
people registered and the people counted{c('UNRWA, “Jalazone Camp,” read 7 September 2026. PCBS counts residents — 7,344 in 2007, 8,201 in 2017, 8,858 projected for 2021; UNRWA counts registered refugees and their descendants wherever they live. Khaldun Bshara gives UNRWA c. 13,000 for 2023 against a PCBS estimate of 9,228. UNRWA’s camp profile of 2022 prints a third pair: 16,439 registered and a density of 64,976, which is simply the one divided by the 0.253 km². <b>On the land: ARIJ says leased by UNRWA from the Jordanian government; Bshara says rented from a private owner in Jifnā, and the encyclopedia of the Institute for Palestine Studies and the Palestinian Museum says the same, adding that the Red Cross set the camp up and UNRWA took it over in 1950; OCHA in 2008 said most plots were state-owned with the remainder belonging to landowners from nearby towns. These are probably one arrangement described at three levels of detail, and Jifnā is exactly a “nearby town” — but no source produces the lease, its date or its parties, and this book will not pretend the question is closed.</b>')}.</p>
<p>A camp is one of the few places on earth where those two numbers can drift this far apart without
anybody minding.</p>
<p>The tents came down slowly. UNRWA began building permanent structures in 1951 and adopted a shelter
programme in 1955. <b>Al-Jalazūn had concrete shelters from 1953, and al-Amʿarī’s last tent was gone by
1957</b>{c('Kjersti G. Berg, “The Evolving Infrastructure of Palestinian Refugee Camps,” <i>Interactive Encyclopedia of the Palestine Question</i> (Institute for Palestine Studies): UNRWA began constructing permanent structures in 1951, adopted a shelter programme in 1955, and “by 1959 most tents were replaced with concrete huts.” Khaldun Bshara, “Al-Jalazone Refugee Camp,” same encyclopedia, for concrete at Jalazone from 1953; UNRWA’s own camp page for al-Amʿari for the 1957 date. UNRWA itself was created by UN General Assembly Resolution 302 (IV) of 8 December 1949 and began operations on 1 May 1950.')}. It took nine years to go from a tent to a wall.</p>
<p>In <b>1950</b> Jordan annexed the West Bank and gave the refugees citizenship. That made them, alone
among Palestinians in exile, refugees and citizens at the same time{c('The Jericho Conference of 1 December 1948 preceded the annexation of April 1950; the Jordanian Nationality Law of 1954 conferred citizenship on “any person who, not being Jewish, possessed Palestinian nationality before 15 May 1948 and resides ordinarily in the Hashemite Kingdom.” Jalal Al Husseini, “Palestinian Refugees in the West Bank,” and “Palestinians in Jordan, 1948–1967,” both in the <i>Interactive Encyclopedia of the Palestine Question</i>, drawing on Myriam Ababsa (ed.), <i>Atlas of Jordan</i> (IFPO, 2013). Some 280,000 refugees were in the West Bank in 1949.')}.</p>
<div class="fix"><div class="fixhead">How our town changed</div>
<div style="font-size:.95rem;line-height:1.65;color:#46423B">
<p style="max-width:none"><b>Ramallah was 2,972 Christian out of 3,104 in 1922, and is a
Muslim-majority city today.</b> Here is how that happened, step by step.</p>
<p style="max-width:none"><b>One.</b> The Christian majority was itself made, not primordial:
the register of 1562 has Christians arriving to join ten Muslim households already on the hill.
<b>Two.</b> The town was already emptying before the Nakba — <i>about 1,500 of some 6,000
Ramallawis, people of Ramallah, had gone to America by 1946</i>. <b>Three.</b> 1948 changed the denominator before it
changed the numerator: the town did not lose Christians in 1948, <b>it gained some nine thousand
refugees and others</b>, most of them villagers from around Lydda and Ramle. Many moved on, and in
1967 Christians were still 57 per cent of the town. <b>Four.</b>
Then the emigration curve steepened: over four thousand Ramallah-born in the United States by 1960,
over ten thousand by 1975 with fewer than two thousand left in the town{c('Taraki (2008), p. 10 and nn. 14, 16, 21, drawing on ʿAzīz/Naṣīb Shāhīn: 1,500 of about 6,000 emigrated by 1946; some 200 Ramallawis employed by Mandate institutions jobless at once in 1948; 4,000+ Ramallah-born in the United States by 1960; over 10,000 by 1975 with fewer than 2,000 remaining; the 1953 local count at 13,500 with 67 per cent refugees, which Taraki calls “a Jordanian census” (Jordan held no census in 1953; its censuses are 1952 and 1961). <b>The “about nine thousand refugees” this book has printed is 67 per cent of 13,500 — the 1953 count is the source, and it should have been cited as such from the first edition.</b> Note also that PCBS does not publish religion by locality: the last locality-level figure is 32 per cent Christian in 1997, and the date of the crossover to a Muslim majority is not established.')}.</p>
<p style="max-width:none"><i>So the Christian share of Ramallah fell because Ramallah’s Christians
left for America, and because Ramallah took in the survivors of an expulsion.</i> <b>The second of
those is not a loss. It is the best thing this town ever did</b> — and a family history written from
Detroit and San Francisco should say plainly that the people who filled the houses we left were
driven out of Lydda at gunpoint. <i>Lisa Taraki, who has studied this town harder than anyone, warns
against exactly the way of seeing that we have tried to avoid: the Christian villagers of Birzeit and eṭ-Ṭaybeh, she
writes, have more in common with their Muslim neighbours than with the Christian well-off of
Masyūn, a prosperous neighbourhood of the town.</i></p></div></div>"""),

E[-1] = E[-1][:7] + (fig(F5.fig_camps(), 'Where the road stopped',
 'The people driven east out of Lydda and Ramle on 13 July 1948 stopped where the road stopped. The five camps of this district are joined here to the towns and villages their people came from, as the camp table below records them.',
 'UNRWA camp profiles; ARIJ, Ramallah governorate camp profiles (2012); Shāhīn (1982). The line of the march is drawn only approximately.') + E[-1][7],)
ent('1944–1963', 'documents', True, 'The diaspora builds a hospital',
 'In 1944 the Ramallah Foundation, Inc. of New York was formed. A three-man delegation of Peter George Shihadeh, Yousef Abdallah Bateh and ʿAzīz Shāhīn himself toured every Ramallah community in the United States in 1944–45 and collected over <b>$90,000</b>{}. The Summer Resorts Company was founded in 1945, capitalised at £P50,000, in Palestine pounds, since there was no dinar in Palestine until 1950. Most of its stockholders were in the diaspora, and in 1951 it brought the water from ʿAin Fara. On <b>20 May 1963 the Ramallah New Hospital opened</b>, with fifty beds on 26 dunams, the local measure of land. Its assets were vested in the New York Foundation. The money came back along the road the people had left on.'.format(c('Shāhīn (1982), “Societies”: the Foundation of 1944, the delegation and the $90,000; the Hospital Society of c. 1945 and the 26 dunams; the hospital’s completion in 1961–63, third floor 1966–68, out-patient clinic 1977.')),
 f"""
<p><b>What we still don’t know.</b> No source we have found produces the lease for the land of
al-Jalazūn camp, its date or its parties. If you know of a document, please tell us.</p>"""),

ent('1954 · 2023', 'documents', False, 'Our first history, written in New York',
 'After 1948 more and more of our people lived in America, and the town’s story began to be written there. <b>Joseph Jiryes Kaddoura</b> was a pharmacist and mayor of Ramallah from 1943 to 1947. In 1954 he published <span class="ar">تاريخ مدينة رام الله</span>, the <i>History of the City of Ramallah</i>, at al-Hudá Press, New York. Shāhīn took his census figures from it, “pp. 136–37”{}. Seventy years later the author’s niece by marriage, Samira Rafidi Meghdessian, published it in English as <i>Remembering Ramallah</i> (2023), with notes and a foreword by his son. He signed himself Cadora; the family today writes Kaddoura. For years our project hunted for it under another spelling, and it was in the family’s hands the whole time. Cadora, Kaddoura and Qaddūra are one name in three spellings.'.format(c('Kaddoura/Cadora, <i>The History of Ramallah</i> (New York: Huda Press, 1954), 159 pp.; <i>Remembering Ramallah: A Preservation of History</i>, trans. Meghdessian (2023), ISBN 979-8-3507-0767-0; Shāhīn (1982) cites the census figures to Kaddoura pp. 136–37.')),
 '[[C58]]'),

ent('1958 / 1959', 'oral', True, 'The Federation',
 'The American Federation of Ramallah, Palestine, is the body we are writing for.',
 FIX('Founded 1952, federated in Detroit on 7 September 1959 (the family presentation).',
 '<b>Resolved, and the answer is that there are three foundings.</b> <b>1952:</b> five or six Ramallah students at Wayne State (Shaheen names five and then says six) begin <i>Hāthihi Rām Allāh</i>, the magazine that knits the scattered clubs together. <b>7 September 1959, Detroit:</b> delegates from those clubs resolve to constitute a Federation and adopt interim by-laws and a constitution — and the first convention is held that year. <b>August 1963:</b> the IRS recognises the Federation and its education fund.',
 'The convention count settles it arithmetically. The Federation’s own roster of conventions begins at Detroit 1959; the fiftieth fell in Detroit in 2008 and the sixty-third in Dearborn, by Detroit, in 2022 (the roster prints Detroit). The roster lists no convention for 2020, so the sixty-third falls in 2022 rather than 2021, and both close on 1959 as the first; neither closes on 1958. <b>Shāhīn’s “incorporated in Detroit, 1958” is best read as the clubs’ coalition rather than a filing</b>: 1958 appears in the Federation’s own literature too, but always attached to the conventions, never to a document. The IRS Business Master File gives the American Federation of Ramallah Palestine, EIN 38-6096448, 501(c)(4), and the American Ramallah Federation Education Fund, EIN 38-6096449, 501(c)(3), both ruled <b>August 1963</b>, both at Westland, Michigan. <b>What is still not in hand is the Michigan incorporation record itself</b> — a five-minute lookup in the LARA business-entity search for anyone with a browser, and the last thing that would let this entry name a filing date. <i>Note also that the Ramallah Foundation of New York is older and separate: founded 1943, incorporated in New York 1944 by its own account, IRS ruling February 1947.</i>')),

ent('1961–2024', 'documents', False, 'The city, counted to the present',
 'After 1967 our town lived under occupation, and its people kept leaving and kept sending money home. Jordan’s census of 1961 counted <b>14,759</b> people. Israel’s count after the occupation of 1967 found 12,134, and that drop is not simply emigration. The count was taken under curfew in the summer of 1967, just after the war. It recorded only those standing in the town on the day, and every Ramallah person who happened to be abroad lost the right to come home. The dip is an act of the occupation, recorded as a statistic. Birzeit College began four-year degrees in 1972 and became Birzeit University in 1975. Ramallah did not become a capital by accident. It became one because its people made it ungovernable from outside. Birzeit’s students led the way from 1972 onward, and then the strike committees of the first intifada, the uprising that began in 1987. The Muqāṭaʿa, the government compound, was built to hold the town down, and it could not. That compound passed through every hand in turn: a Tegart fort, one of the British police forts of the 1930s; then Jordanian headquarters; then Israeli headquarters; and, after the Israeli army withdrew from the city in December 1995, the seat of the Palestinian Authority. Arafat made it his home in 1996. In 2002 the Israeli army came back into the city and besieged it, and the town lived under curfew for weeks. The census numbers are what survived that. The Palestinian census bureau, PCBS, gives <b>17,851 (1997) · 27,460 (2007) · 38,998 (2017) · 42,122 projected (2021)</b>{}. Meanwhile the number of Ramallah people in America overtakes the number of Ramallah natives still at home: 1,500 in the United States by 1946, over 4,000 by 1960, over 10,000 by 1975. By his own 1975 figures, more than four in five Ramallah people lived in America; he put it at over 85 per cent, counting the town’s families, not the town’s residents{}.'.format(
  c('The census series: Jordan 1961 (14,759); the census conducted by the Israeli Central Bureau of Statistics in the occupied territories in 1967 (12,134); PCBS 1997, 2007 and 2017; and the PCBS projection series, <i>Projected Mid-Year Population for Ramallah &amp; al-Bireh Governorate by Locality 2017–2021</i>, locality code 301810, which gives Ramallah <b>42,122 for 2021</b> — the 2022–26 table is attested by title but PCBS has taken it offline, so this book prints 2021 and no later projection. <b>On religion: the 1967 census is the only count of Christians and Muslims for Ramallah alone between 1945 and 1997.</b> Jordan’s census of 18 November 1961 counts Christians only for the two towns together: Table 2.11, row “Ramallah &amp; Bira,” has 8,745 Christians among 29,269 people, 29.9 per cent (printed p. 116). It gives Ramallah 14,759 people and al-Bīra 14,510 (Table 1.7, p. 15), with no split by religion for either alone. The 1967 census recorded <b>6,966 Christians of 12,134 — 57 per cent</b> of everyone counted; its own Table D prints 59.4 Christians per hundred inhabitants of known religion — and 5,203 people, 43 per cent of the town, originating from what had become Israel. <i>It is an Israeli state source, produced by the occupying power in the first months of the occupation, and this book says so on the page rather than passing the number through a tertiary work.</i> Its tables are now published in full and independently by the Levy Economics Institute of Bard College, so a reader can check them. By the first Palestinian census in 1997 Christians were <b>32 per cent</b> (PCBS, <i>Final Results: Ramallah City</i>, City Reports Series 005, 2000). <b>Between 1967 and 1997 there was no census of any kind, and no municipal, church or scholarly source publishes a religious breakdown for the town in that interval. The crossing from a Christian to a Muslim majority cannot at present be dated more closely than to those thirty years.</b>'),
  c('Shāhīn (1982), the emigration chapter: 1,500 by 1946, 4,000+ by 1960, 10,000+ by 1975 with fewer than 2,000 remaining, and the 85% figure.')),
 f"""
{fig(F3.fig_two_pop(),'Two populations, one town',
 'Ramallah natives at home against Ramallah natives in the United States, on Shāhīn’s own figures. By 1975 he counts more than ten thousand Ramallah people in America: a diaspora that had grown to rival, and by some readings to overtake, the native population still at home. By his own 1975 figures, more than four in five Ramallah people lived in America; he put it at over 85 per cent, counting the town’s families, not the town’s residents. What is not in doubt is the direction of the money: the hospital, the water supply and the schools at home were paid for from the far side of the ocean.',
 'Shāhīn (1982): the home censuses of 1905–1953 and his diaspora counts — 1,500 by 1946, 2,580 in 1953, 4,000+ by 1960, 10,000+ by 1975.')}
{fig(POP_CHART, 'Every number anyone has ever recorded, 1596–2024',
 'The recorded population on a logarithmic scale, now carrying every count Shāhīn assembled — 1839, 1870, 1905, 1944, 1953 — with the 1916 typhus drawn as a labelled inference and the 1967 dip labelled as what it is: not simply emigration, but a count taken under curfew weeks after the occupation, which left out every Ramallah person then abroad.',
 'The 1596 defter; Robinson and Smith; Anthemos; the censuses of 1870–2017; PCBS projections; the epidemic from Shāhīn (1982).')}"""),

ent('1982', 'documents', False, 'Shāhīn closes the record',
 'ʿAzīz Shāhīn was born in 1894. He survived typhoid in 1906, boarded at the Friends Boys School in 1907–10 and was a fund-raiser in 1944–45. In 1982 he published <span class="ar">كشف النقاب</span>, <i>Kashf al-niqāb</i>, “Lifting the veil”: 894 pages, the book we measure everything else here against{}. His history ends: <i>“The foregoing history of Ramallah brings us down to the end of 1978. Every effort has been made to make it as complete and as accurate as possible.”</i> Where we could check him against other records, he held up.'.format(c('Shāhīn (1982); the autobiographical details from his own chapters. The full test of his chronology against the external record: 36 checkable claims — 13 confirmed, 15 new, 3 refined, 3 corrected, 1 in conflict, 1 untestable.')),
 f"""
<p><b>What we still don’t know.</b> We have not yet found the Michigan record of the Federation’s
incorporation, which would give the date it was filed. We also cannot yet date the town’s change from
a Christian to a Muslim majority more closely than the thirty years between the censuses of 1967 and
1997. If your family’s papers can answer either question, please tell us.</p>"""),

sect('Three things said plainly', 'The Karak evidence, two false leads, and the people this town produced')
ent('1812 → 1934', 'documents', False, 'When the Ḥaddādīn name enters the record',
 'Our family’s road runs through Karak, and we can now date the Karak end of it quite closely. The date turns out to be <b>much later than the tradition suggests</b>, and we should say so plainly.',
 f"""
<p><b>1812.</b> The Swiss traveller Burckhardt counted about <b>150 Christian families at Karak</b>,
and he did not name the Ḥaddādīn among them{c('J. L. Burckhardt, <i>Travels in Syria and the Holy Land</i> (London, 1822), on the Christians of Karak. He names no clans.')}. As we saw earlier in this chapter, he was also told
that Karak’s Christians were, in the main, <i>descendants</i> of refugees from Jerusalem,
Bethlehem and Beit Jala{c('J. L. Burckhardt, <i>Travels in Syria and the Holy Land</i> (London: John Murray, 1822), 381: “Kerek is inhabited by about four hundred Turkish, and one hundred and fifty Christian families… The Christians are, for the greater part, descendants of refugees from Jerusalem, Bethlehem, and Beit Djade.” <b>Earlier editions of this book read this as migration Burckhardt observed. It is not — it is what the Christians of Karak told him about their ancestry.</b>')}.</p>
<p>It does not break our family’s tradition of coming out of Karak. It does mean that <b>the road by
itself proves a connection, never a direction</b>.</p>
{FIX('A one-way migration corridor: Karak → Palestine.',
 'A <b>corridor remembered in both directions</b>. Burckhardt’s Karak Christians said they were descended from refugees out of Jerusalem, Bethlehem and Bayt Jālā.',
 'The map and the narrative may show the family’s claimed route, but must not use the corridor’s existence as evidence of which way anyone travelled. Direction has to come from a document about <i>this</i> family, not from the road.')}
<p><b>About 1879: the first named Ḥaddādīn at Karak.</b> A house in the town is said to have belonged
to Jreis Sulayman Haddadeen{c('Reported attribution of a Karak house to Jreis Sulayman Haddadeen, c. 1879. A deed, building inscription, tax entry, photograph or conservation inventory is still needed to confirm it.')}.</p>
<p><b>From 1867.</b> Karak Christians began resettling Maʿīn from 1867 (Ottoman records). The family
remembers the Ḥaddādīn move as 1892, and the Latin Patriarchate’s own history of Maʿīn names the
Ḥaddādīn among the Christians who came from Karak{c('Ḥammūdeh (2014), p. 44, citing Abū al-Shaʿr: Maʿīn lay in ruins until 1284 AH (1867), when Christian families from Karak settled and rebuilt it; it had 30 households in 1288 AH (1871). N. Shaheen (2005), ch. 2, p. 16, for 1892. The Latin Patriarchate of Jerusalem’s page for Maʿīn says only that the Ḥaddādīn came from Karak at the end of the nineteenth century. <b>Earlier editions gave 1886 here; we can trace that date to no source, and it is dropped.</b>')}. <b>This is the strongest evidence from an institution that ties the clan to
the place.</b></p>
<p><b>The 1920s</b> bring confirmation in print. Al-Ziriklī lists fifteen Greek Orthodox Ḥaddādīn
houses at Karak. Kaḥḥāla repeats the figure in his dictionary of tribes of 1949, which gathers earlier
authorities and is not a separate witness{c('Kaḥḥāla, <i>Muʿjam qabāʾil al-ʿArab</i>, s.v. al-Ḥaddādīn: a Christian Greek Orthodox clan of Karak of fifteen houses. <b>Kaḥḥāla assigns them no Ghassanid ancestry.</b> '+D('1949_Kahhala_Mujam_qabail_al-Arab_v4.pdf')+'.')}. Importantly, <i>both assign them no Ghassanid
ancestry.</i></p>
<p><b>1934: the claim is written down by a doubter.</b> Frederick Peake, listing the tribes of
Transjordan, calls the Karak Ḥaddādīn the oldest Christian tribe of Karak. He records their claim of
descent from Banū Ghassān, <b>and states that the claim lacks supporting proof</b>{c('F. G. Peake, <i>History and Tribes of Trans-Jordan</i>, vol. II, the Ḥaddādīn entry. '+D('1935_Peake_Tarikh_sharqi_al-Urdun_wa-qabailiha.pdf')+'.')}.</p>
<p><b>1979: a Palestinian authority names the family outright.</b> Until now we had followed the
Ḥaddādīn–Ghassān question only through Peake and Kaḥḥāla. We should have gone to the Palestinian
record first.</p>
<p>Muṣṭafā Murād al-Dabbāgh wrote <span class="ar">القبائل العربية وسلائلها في بلادنا فلسطين</span>,
a whole book on the Arab tribes of Palestine and their descendants. It has a chapter on the
Ghassanids. Under <span class="ar">ومن سلائل الغسانيين</span>, “and among the lines of the
Ghassanids,” <b>the first name he lists is <span class="ar">الحدادين</span></b>{c('<span class="ar">مصطفى مراد الدباغ، القبائل العربية وسلائلها في بلادنا فلسطين</span>, chapter <span class="ar">الغساسنة</span>, 151–55, at 153: <span class="ar">ومن سلائل الغسانيين نذكر: ١ ــ الحدادين</span>. He traces them to Biskintā on the flank of Jabal Ṣannīn and thence to ʿAnbah, Sammūʿ, Khanzīra and Dayr Abū Saʿīd in the ʿAjlūn district and al-Salṭ in the Balqāʾ, and adds <span class="ar">ومن الحدادين جماعات نزلت فلسطين وخاصة بيت المقدس</span>. <b>His footnote for the Transjordanian branch is Peake, <i>Tārīkh sharqī al-Urdunn wa-qabāʾiluhā</i>, 246</b> — the same officer who recorded the claim in 1934 and declined to endorse it. ' + D('1979_Dabbagh_al-Qabail_al-Arabiyya_fi_Filastin.pdf') + '.')}.</p>
<p>Two things must be said about that. <b>It is the strongest Palestinian statement of our family’s
claim that exists.</b> He writes from inside the country, in Arabic. He names the Ḥaddādīn among
Ghassanid lines, and traces the branch that crossed into Transjordan through ʿAjlūn and al-Salṭ, and
then <span class="ar">ومن الحدادين جماعات نزلت فلسطين</span>, “and of the Ḥaddādīn, groups came down
into Palestine.”</p>
<p>But his own footnote sends the reader back to Peake. So al-Dabbāgh is not a separate witness to the
descent. He is a Palestinian scholar gathering, in Arabic, the same tradition we have been looking
into. <i>That is worth having, and it is not the same thing as proof.</i></p>
<p>In the same chapter he weakens the other half of the story. <b>Every place where al-Dabbāgh says the
Ghassanids actually lived is east of the Jordan</b>: Tadmur, Ḥawrān, the Yarmūk, Gharandal, al-Qasṭal,
al-Zarqāʾ, Adhruḥ, al-Jarbāʾ and Maʿān{c('Irfan Shahîd, <i>Byzantium and the Arabs in the Sixth Century</i> II.1 (Washington: Dumbarton Oaks, 2002), pp. 61–62: the Arabic sources associate the Ghassanids of southern Transjordan with al-Dajāniyya, Adhruḥ and Ubayr, and Shahîd accepts the association because a Greek papyrus finds a Ghassanid active at Ṣadaqa, close to all three; his list of Ghassanid sites in Palaestina Tertia begins with Adhruḥ (Augustopolis). <b>Adhruḥ is the Udhruḥ that the Ḥaddādīn route begins from.</b> It places the people in the region in the sixth century; it does not place any one family in the people. ' + D('2002_Shahid_Byzantium_and_the_Arabs_6th_Century_v2p1.pdf') + '.')}{c('Al-Dabbāgh, <span class="ar">القبائل العربية</span>, 151–52. His only Palestinian instances are the place-names themselves — Dayr Ghassāna, and a suggestion that Jifnā in the Ramallah district may be named for <span class="ar">آل جفنة</span>, again hedged with <span class="ar">ولا يستبعد</span>, “it is not to be ruled out.” <i>The evidence for the settlement is the place-name; the evidence for the place-name is the settlement.</i> Every Arab authority that specifies where the Ghassanids actually were — al-Qalqashandī, al-Hamdānī, Ibn Faḍl Allāh al-ʿUmarī, Jawād ʿAlī, Kurd ʿAlī, and al-Dabbāgh himself — puts them east and north.')}. West of it he offers only two place-names, Dayr Ghassāna and
perhaps Jifnā, and he hedges both, in the tribes book and again in his village gazetteer, as we will
see.</p>
<p><i>The Palestinian record puts our claimed people on the plateau the tradition names, and nowhere
near these hills until we walked here ourselves.</i> That is exactly what we have found from the
Ottoman side, reached separately from the Arabic.</p>
<p>So the Karak evidence comes to this. <b>The clan is firmly at Karak from the late nineteenth
century, and in print as such by the 1920s.</b> The Ghassanid claim attached to it is first recorded
in 1934, by an outsider who would not support it.</p>
<p>Everything earlier is background to the claim: the plateau’s unbroken Christian life from Nitl to
Shawbak to the register of 1596. It is good background. But it is not a chain of fathers, and we
will not present it as one.</p>"""),

ent('a warning', 'none', False, 'Two false leads',
 'Both are the kind of mistake a family history makes when a name looks familiar. We mark them here so that nobody follows them twice.',
 f"""
<p><b>The first lead: Dayr Ghassāna.</b> About nineteen kilometres north-north-west of Ramallah as the
crow flies, some twenty-five by road, there is a village whose name looks like a gift. People often point to it as proof that Ghassanids settled in
these hills. We went to the Palestinian and Arabic sources first. They do not support that idea, but
they say something better than a flat no.</p>
<p><b>The earliest text is Arabic, and it does not choose.</b> In 1710 the traveller Muṣṭafā
al-Bakrī stood at the village: <span class="ar">ووقفنا على تلك الآثار</span>, “and we stopped at
those remains.” He reached for two reference books, al-Jawharī’s <i>Ṣiḥāḥ</i> and al-Suyūṭī’s
<i>Lubb al-albāb</i>, and set out <b>two different Ghassāns</b>.</p>
<p>One was the Azdī water of the Jafnid kings. The other was <span class="ar">غسّان بن جذام</span>, a
clan of the Ṣadif of Ḥimyar, an entirely different people. <i>He chose neither, and turned at once to
the Barāghitha, the Barghūthī family, who actually lived there</i>{c('<span class="ar">مصطفى بن كمال الدين البكري الصديقي، «الخمرة الحسية في الرحلة القدسية»</span>, the journey of 1122/1710, serialised in <span class="ar">مجلة الرسالة</span>, no. 801, p. 38. He quotes al-Jawharī’s <i>Ṣiḥāḥ</i> for the Azdī water of the Jafnids and al-Suyūṭī’s <i>Lubb al-albāb</i> for <span class="ar">غسّان بن جذام بطن من الصدف</span>, and settles neither. <b>Ghussān b. Judhām of the Ṣadif is independently attested — al-Dāraquṭnī, <i>al-Muʾtalif wa-l-mukhtalif</i> ii.976 and iv.1800; al-Samʿānī, <i>al-Ansāb</i> iii.316; Ibn Ḥajar, <i>Tabṣīr al-muntabih</i> iii.1045; al-Bakrī, <i>Muʿjam mā istaʿjam</i> i.317 — and is a different people from the Jafnids entirely.</b>')}.</p>
<p>That second reading is real, old and supported by other sources, and later writers quietly dropped
it. <b>Bringing it back is the one correction we would press.</b></p>
<p><b>The standard Palestinian entry is cautious, and its own source points east.</b> Muṣṭafā Murād
al-Dabbāgh, in <span class="ar">بلادنا فلسطين</span>, writes
<span class="ar">يبدو أنّ اسمها يعود إلى أنّ طائفة من الغساسنة نزلتها</span>, <i>“it appears that</i>
its name goes back to a group of the Ghassanids having settled it.” He offers no evidence beyond the
name.</p>
<p>The authority he cites, al-Qalqashandī, places Ghassān at al-Balqāʾ, the Yarmūk and Ḥimṣ: <b>not
one place west of the Jordan</b>{c('<span class="ar">مصطفى مراد الدباغ، بلادنا فلسطين، ج ٨ ق ٢، «دير غسّانة»، ص ٢٦٦–٢٧٠</span>. His footnote sends the reader to al-Qalqashandī, <span class="ar">نهاية الأرب في معرفة أنساب العرب</span>, no. 1421, i.388, which locates Ghassān <span class="ar">بالبلقاء… وباليرموك الجمّ الغفير، وبحمص منهم جماعة</span> — al-Balqāʾ, the Yarmūk and Ḥimṣ. <b>Al-Dabbāgh himself also prints al-Bakrī’s Ṣadif alternative on the same pages, without deciding between them.</b> Pagination is that of the Bibliotheca Alexandrina scan; the Dār al-Ṭalīʿa and Dār al-Hudá editions differ.')}. Shurrāb repeats al-Dabbāgh’s sentence word for word, caution
and all, and drops the Ṣadif alternative{c('<span class="ar">محمد محمد حسن شرّاب، معجم بلدان فلسطين</span> (Damascus–Beirut: Dār al-Maʾmūn li-l-Turāth, 1407/1987), 393–94, reproducing al-Dabbāgh’s <span class="ar">يبدو أنّ</span> verbatim. <i>Two of the three standard Palestinian gazetteers are therefore one source counted twice — and the transmission lost the competing etymology on the way.</i> Shukrī ʿArrāf’s <span class="ar">المواقع الجغرافية في فلسطين</span> has no entry: its remit is sites inside the Green Line.')}.</p>
<p><b>The clearest witness is the village’s own son.</b> ʿUmar al-Ṣāliḥ al-Barghūthī of Dayr Ghassāna
wrote <span class="ar">تاريخ فلسطين</span> (Jerusalem, 1923) with Khalīl Totah. It was the first
Palestinian national history. He writes about his own village and its Barghūthī shaykhs, and <b>says
nothing at all about a Ghassanid origin for its name</b>.</p>
<p><i>He is not shy of Ghassān. He places the Palestinian Ghassanid remnant among the Balāwina of Banī
Ṣaʿb and the Baysān valley, and he claims Ghassanid descent for Palestine’s Arab Christians as a
national claim. He simply does not attach it to Dayr Ghassāna.</i>{c('<span class="ar">عمر الصالح البرغوثي وخليل طوطح، تاريخ فلسطين</span> (Jerusalem, 1923): p. 239 for the Barāghitha as amīrs of the Qaysiyya in Banī Zayd, Banī Murra and Banī Sālim <span class="ar">ومركزهم دير غسانة</span> — and no etymology; p. 124 for the Palestinian Ghassanid remnant among <span class="ar">البلاونة</span> of Banī Ṣaʿb, al-Sabʿ and Ghawr Baysān; p. 189 for Palestine’s Arab Christians <span class="ar">وأثبتوا أنهم من أبناء غسان وطيّ وتغلب الذين هم من صميم العرب</span>. <b>The leading man of Dayr Ghassāna, writing the first Palestinian national history, does not claim the Ghassanid etymology for his own village.</b>')}</p>
<p>So here is where the Arab and Palestinian sources leave us. In the Arabic tradition the name has
three possible origins. One is the Jafnid water. One is Ghussān b. Judhām of the Ṣadif. The third is
the ordinary word <span class="ar">غسّانة</span>, “handsome,” which Ibn Durayd already gave and the
<i>Lisān al-ʿArab</i> keeps. <i>The Jafnid origin is the only one of the three with nothing behind
it but the sound of the word</i>{c('<span class="ar">ابن دريد، الاشتقاق</span>, 435: after stating that the children of Jafna were named for a water <span class="ar">ليس بأبٍ ولا أمٍّ</span>, he adds that where others are called Ghassān the derivation is from <span class="ar">الغُسَن</span>, tresses of hair, <span class="ar">أو يكون من قولهم غَيْسان الشباب</span>, “the first freshness of youth.” The same sense in <span class="ar">ابن منظور، لسان العرب</span> xiii.313; <span class="ar">الأزهري، تهذيب اللغة</span> viii.70, 149; <span class="ar">ابن فارس، مقاييس اللغة</span> iv.405; and Yāqūt s.v. <span class="ar">غسان</span>, who brackets the water-story with four morphological derivations. <i>This etymology is sometimes attributed to modern Western scholarship. It is not modern and it is not Western: it is Ibn Durayd’s, and the Western citation of it is a route to the Arabic, not a substitute for it.</i>')}.</p>
<p><b>The village’s name and our family’s nisba, the name that marks descent, are not the same
evidence, and our family’s claim does not need the village.</b></p>
<p><b>The second lead: “al-Ḥaddāda” in al-Suwaydī is not us.</b> This classical genealogist has an
entry under that name. Beside it is a Banū al-Ṣabr among Ghassān, which looks temptingly like
<i>Sabra</i>. It is a coincidence. <b>Al-Ḥaddāda is an unrelated Lubayd/Sulaym group in North
Africa</b>, and a likeness between an Arabic clan name and an ancestor’s name is not evidence of
anything{c('Muḥammad Amīn al-Suwaydī, <i>Sabāʾik al-dhahab fī maʿrifat qabāʾil al-ʿArab</i>, s.vv. In the family library, '+D('1831_Suwaydi_Sabaik_al-Dhahab_qabail_al-Arab.pdf')+'.')}.</p>
<p><i>Similar surnames are the most common way family histories go wrong. We name the trap here so
that no later editor walks into it.</i></p>
<p><b>And a book we long failed to find, because we were looking for the wrong
title.</b> The wheel chart of the Karak clan in the family presentation has the caption <i>“El-Haddadeen
Tribe, Origins and Branches, Warda Books, 2025.”</i> For a long time we could not find such a
book in any catalogue, and went looking for a different one.</p>
<p>The caption is not a ghost. It is a loose English rendering of a real book, listed in catalogues
and possible to obtain: <b>Munther Haddadin, <span class="ar">دولة الغساسنة؛ أصيلها ورحيلها</span></b>
(<i>The Ghassanid State: Its Origin and Its Departure</i>), Amman: <span class="ar">دار ورد
الأردنية للنشر والتوزيع</span>, <b>2024</b>, ISBN 978-9923-76-975-1{c('Munther Haddadin, <span class="ar">دولة الغساسنة؛ أصيلها ورحيلها</span> (Amman: <span class="ar">دار ورد الأردنية للنشر والتوزيع</span>, 2024), ISBN 978-9923-76-975-1; announced in the Jordanian press on publication and listed by Neel wa Furat with the publication date 29 July 2024. <b><span class="ar">دار ورد</span> is “Dār Ward” — the presentation’s “Warda Books.”</b> The English caption also renders <span class="ar">أصيلها ورحيلها</span>, “its origin and its departure,” as “Origins and Branches,” and dates the book a year late.')}.
<i>“Warda Books” is <span class="ar">دار ورد</span>. The year is one out. The title was translated
loosely. Everything else in the caption is right, and the chart under it is that book’s plate 84.</i></p>
{FIX('“<i>El-Haddadeen Tribe, Origins and Branches</i> (Warda Books, 2025) appears in no catalogue anywhere, and the tree attributed to it cannot be assessed until its pages are produced.” Earlier editions went on to propose <span class="ar">عشائر الحدادين</span> by <span class="ar">عباس حدادين</span> (2016) as the book actually meant.',
 '<b>The book is Munther Haddadin, <span class="ar">دولة الغساسنة؛ أصيلها ورحيلها</span>, Dār Ward al-Urduniyya, Amman, 2024</b> — and this book had already found it, printed its ISBN, and then wrongly concluded that it “contains no Karak clan genealogy at all.” <i>It contains the wheel.</i>',
 'A publisher’s name anglicised, a title translated loosely and a year off by one were enough to send two editions of this book down a false trail — and the false trail was published, which is why the retraction is printed here at the same size. <b>The 2016 identification is withdrawn.</b> The earlier titles remain worth having: <span class="ar">عشائر الحدادين</span> (2016) and <span class="ar">عشائر الحدادين حتى عام ١٩٩١م</span> by Khalaf Khalīl, Munīr Jiryis and ʿAwwād Jiryis Ḥaddādīn are real books about this clan, and the question of whether Ṣaqr and 1561 appear in the 1991 volume — before Haddadin 2024 — is still the decisive test of the Karak tradition’s age.' + c('<i>ʿAmmūn News</i>, 9 January 2016, on the launch of <span class="ar">عشائر الحدادين</span> by <span class="ar">عباس حدادين</span> at <span class="ar">جمعية آل حدادين (المعمورة)</span>, Sweifieh, at which Munther Haddadin was a speaker; <span class="ar">الرأي</span>, 27 November 2007, citing <span class="ar">عشائر الحدادين حتى عام ١٩٩١م</span>. <b>Still to be checked, through the Ḥaddādīn diwan in Amman or the Jordanian National Library deposit record: whether Ṣaqr and the date 1561 stand in the 1991 book.</b>'))}
<p><b>What stays true after the correction.</b> The wheel is a family tree published in 2024, <b>not an
Ottoman record</b>. Naming its source correctly lifts
it from a caption nobody could check to a book anyone can cite. <i>It does not lift it to a
document.</i></p>
<p>This matters for how we weigh witnesses. The 2026 family presentation reproduces plate 84 of that
same book. <i>So the presentation and Haddadin 2024 are one stream of evidence, not two separate
witnesses.</i> That is why the evidence badges on the family ladder change at 1500.</p>
<p>Where we do count two witnesses for Rāshid, they are <b>Haddadin 2024 on the Karak side, and Shāhīn
1982 with the co-authors’ chart on the Ramallah side</b>. These two really are independent of each
other.</p>
<p><b>What we still don’t know.</b> No Ottoman register names Rāshid, Ṣabra or Ṣaqr. We do not know
whether Rāshid’s father was ʿĪsā or Ṣaqr, or whether they were one man; a single Karak or Ramallah
document giving both names together would settle it. We do not know what the date 1561 at the hub of
the Karak wheel refers to. And the reading Hadeed in the registers is a lead still to be followed. If
you hold family papers from Karak or Ramallah, they may answer one of these.</p>"""),

ent('1869 → 1916', 'attested', True, 'A teacher and a doctor from outside',
 'Two people from outside our town gave it a school for girls and a doctor: Miriam Karam, who asked for the school and taught in it, and Dr Philip Maʿlouf, for years the only doctor in the district.',
 f"""
<p>In 1869 <b>Miriam Karam</b>, fifteen, whose family had lived in Ramallah for some years but were not
from here, stopped Eli and Sybil Jones in a narrow street and asked for a school for girls. They asked who would
teach it. <i>“I will,”</i> she said. She could, because she had been schooled at the Deaconesses’
school in Jerusalem and came from a family of teachers.</p>
<p>The school <b>opened in 1869 with twenty girls</b>, and by 1873 there were fifty girls in the Friends’
four day schools. A boarding school, the Girls Training Home, was founded beside it in 1889, and the school took the name Friends Girls School in 1925. Miriam herself
taught for four years, then married and left, and the school she started is still open{c('Shāhīn (1982), the education chapter, p. 63: “Miss Karam’s family were not natives of Ramallah, but lived there for several years”; she married Hanna Bayyuk of Jerusalem.')}. Katie
Gabriel, who was Lebanese, ran the boarding school from 1889 and gave the Friends forty years.</p>
<p><b>Dr Philip Asʿad Maʿlouf</b>, a Lebanese, came from Beirut in 1891 and opened his own clinic in 1895.
For years he was <i>the only doctor in the entire Ramallah district</i>, and he <b>covered the whole
district alone for twenty-five years</b>. The town called him <i>Hakeem Abu Iskandar</i>, “Doctor,
father of Iskandar”; <i>hakeem</i> means doctor.</p>
<p>In 1906 Dr Maʿlouf pulled a twelve-year-old boy through forty days of typhoid fever. The boy was
ʿAzīz Shāhīn, who lived to write our town’s history. <b>Maʿlouf himself died in the typhus of
1916, while treating it.</b> He used to say that a doctor got no credit in Ramallah: people waited until a man was nearly
dead to call him, and then blamed him if the man died{c('Shāhīn (1982), “Medical Treatment.” His predecessor, Dr George Hassenauer of the Friends clinic (1883–89), was called <b>Dr Ḥassan Nawwār</b> because the town could not pronounce his name.')}.</p>"""),

ent('1901 → 1963', 'attested', True, 'The people our town produced',
 'Our town was a village of three thousand souls, on one ridge, and in one century it gave all of the people below. This is only a partial list.',
 f"""
<p><b>Boulos Shehadeh</b>, born in Ramallah in 1882, founded the newspaper <i>Mirʾāt al-Sharq</i>,
“Mirror of the East”, in Jerusalem on 17 September 1919. Its 1,132 surviving issues are digitised, and
they mention his home town 1,535 times. Khalil Totah, born here in 1886, ran the Friends Boys School.
His diary of the 1938 revolt is told in “The revolt reaches the town”. From 1944 until his death in 1955 he argued Palestine’s case
across the United States, and his diaries are now a source for the Mandate years. The school’s
auditorium, which he raised the money for, carries his name. Dr Fuad Shatara (1892–1942) was a
physician on the staff of Cumberland Hospital in Brooklyn. He was an early leader of the Ramallah Young
Men’s Society of New York, and helped organise its demonstration against the Balfour Declaration on
8 November 1917. He later became president of the Arab National League, arguing the Arab case for
Palestine on American platforms{c('Shāhīn (1982), “Notable Individuals,” “Societies,” and the education chapter.')}.</p>
<p>In 1925 a group of Ramallah women founded the <b>Nahda Women’s Association</b>, registering it on
1 January. It was the town’s first women’s society, and their own. It outlived the Mandate, the
Nakba, the Jordanian years and the occupation, and was still serving about a hundred hot meals a week
when Shāhīn wrote. Into that town came Matiel Mogannam. She had already been a secretary of the Arab
Women’s Executive of 1929, and had argued the Palestinian case in English in <i>The Arab Woman and the
Palestine Problem</i> (London, 1937). From 1938, Shāhīn says, she lived here, and in 1939 she formed the Women’s Union
Society; the society’s own papers, in the Palestinian Museum Digital Archive, date it to the early 1930s. It put looms and embroidery frames into paid women’s hands, and in 1961 it opened a home
for the town’s old women{c('Shāhīn (1982), “Societies”: the Nahda (1925), the Infant Welfare Society (1927, Mrs Neʿmeh Joseph Kaddoura), the Women’s Union (1939), the Girl Guides (1942), and the Handicraft Cooperative (1954, Miriam Yaʿcoub Zaʿroor — in Shāhīn’s words the first cooperative society in Palestine, which we have not been able to confirm; fifty women, all skilled embroiderers). The Palestinian Museum Digital Archive describes the Women’s Union as “founded in Ramallah during the early 1930s to care for the elderly,” with papers that include “sessions held in 1939.”')}.</p>
<p>Khaleel Abu Rayya opened the National College in 1947 and kept it running until 1971, the last
fourteen years partly paralysed by a stroke. Then he took charge of the Ramallah Public Library he had
founded. Dr Saʿadallah Kassees was both doctor and mayor. His niece, Laila Kassees, became <b>the first
woman of Ramallah to qualify as a doctor</b>, and practises in Memphis. And Joseph Jiryes Kaddoura,
pharmacist and mayor, wrote the town’s first history (its story comes in the next chapter){c('Shāhīn (1982), the education and notable-individuals chapters; Cadora’s mayoralty and his 1954 book, on which see “Our first history, written in New York”.')}.</p>
<p>Most of these people were born into, or married into, the eight clans of our town. That is what a
ḥamūla, a clan, was for. But not all of them were. Others we have met came from outside: Katie Gabriel was Lebanese, Dr Maʿlouf came from
Beirut, and Matiel Mogannam was born in Lebanon and only settled here in 1938. Our town was served by
people it never absorbed. In a history of how our town took people in, that is worth saying.</p>"""),

CH(14)

ent('I', 'attested', True, 'Our origins',
 '<b>We can be as sure here as origins of this kind allow, and we say exactly how far.</b> <b>The dynasty our family claims</b> is real, and it is named in sources of its own time at generations 33–34: Procopius writes of al-Ḥārith in Greek, in al-Ḥārith’s lifetime. <i>Our family’s descent from that dynasty is not proven, and we do not say it is.</i> The dynasty is credited with sixth-century church mosaics at Nitl, ten kilometres from Maʿīn on the road the tradition names. A Ghassān population is still recorded in Transjordan, at Gharandal far to the south, as late as al-Yaʿqūbī, about 890. And the gap in the chart is not a scandal but a number: <b>about thirty-one generations in that stretch, thirty of them with no name at all</b>. Our chart prints them openly as a gap, where other families forged pedigrees.',
 f"""
<p>Our story is told, and the evidence behind it has been laid out chapter by chapter. Here we weigh
three claims on all of it: our origins, our contribution, and the founding of Ramallah.</p>
<p><b>Go back to Figure 1 and read the grade column downward.</b> Nine links carry our family from
Adam to this morning, and they do not all rest on the same kind of evidence.</p>
<p>A doubter always aims at link two, which matches Joktan in the Bible with Qaḥṭān, ancestor of the
southern Arabs. But that link is a thousand years old, and every Qaḥṭānī Arab in the world stands on
it. <b>The real weak point is link seven, the gap</b>, and our family’s own chart is what says so.</p>
<p>The deep line above generation 30 rests on scripture and classical scholarship, and we present and
defend it as such. Generation 29 enters the name Al-Ghassānī, and that matches the classical sources
exactly. <i>Nobody arranged that.</i> But the strongest argument for our chart is not what it claims.
It is what it refuses to claim.</p>
<div class="fix"><div class="fixhead">The families we compare ourselves with</div>
<div style="font-size:.95rem;line-height:1.6;color:#46423B">
<p style="max-width:none"><b>Issa Maalouf</b>, a Lebanese Orthodox historian, wrote his family’s
history with <i>no</i> Ghassanid claim in it. Around <b>1906</b> he added, in his own hand, the
sentence “the correct view is that they are Ghassanids”; by <b>1908</b> he had published a specific
chain of named ancestors running back to a Ghassanid king. Ottoman documents of <b>1524, 1525 and
1533</b> record the same family with no such lineage{c('On the Maʿlūf genealogical claim and its documentary refutation from Vatican Syriac MS 333 (1524) and the Ottoman <i>tapu taḥrīr</i> registers of 1525 and 1533. The critical study is available online; this project has not read the printed version and flags the author attribution as unconfirmed.')}. <b>The pedigree was invented, in
writing, inside two years, for the politics of its moment.</b> Several other Levantine Christian
families made claims of the same shape in the same period.</p>
<p style="max-width:none"><b>And unlike Maalouf’s, our family’s claim was first written down by
somebody with no stake in it.</b> When Frederick Peake recorded the Karak Ḥaddādīn’s Ghassanid
descent in 1934, he wrote down the claim <i>and his own doubt about it in the same breath</i>. A
tradition preserved by a sceptic is better provenanced than one asserted by a descendant.</p>
<p style="max-width:none"><b>And there is a third case, from Lebanon, which is the most useful of
all — because it is honest.</b> In <b>1948</b> a priest, Ighnāṭiyūs Ṭannūs al-Khūrī, published a
monograph on the Sheikhs Āl al-Shammar, notables of Akoura and the Zāwiya district of Zgharta. Its
fourth chapter is headed <span class="ar">بنو غسان وفرعهم بنو شمر</span> — <i>“Banū Ghassān and their
branch the Banū Shammar.”</i> And this is how he opens it:</p>
<p style="max-width:none" class="pull"><span class="ar">هو زعم وجيه وتقليد عريق أن المشايخ آل الشمر
متأصلون … من آل جفنة</span><br>
<b>“It is a respectable <i>claim</i> and an ancient <i>tradition</i> that the Sheikhs Āl al-Shammar
are descended … from the house of Jafna.”</b></p>
<p style="max-width:none"><b><span class="ar">زعم</span> — <i>zaʿm</i>, an assertion.</b> The man
writing the family’s own book calls its Ghassanid descent a claim and a tradition in his first
sentence on the subject. Then he sets out the Jafnid kings from Jabala down through al-Ḥārith
al-Akbar, al-Mundhir, al-Nuʿmān and Ḥujr — and stops to say
<span class="ar">وبعد حجر هذا تنقطع السلسلة حتى جبلة بن الأيهم</span>: <b>“and after this Ḥujr the
chain is broken, until Jabala ibn al-Ayham.”</b> <i>His chain breaks inside the sixth century, and he
prints the break.</i> His authorities for the Ghassanid part are Ibn Khaldūn, Ibn Qutayba,
al-Balādhurī, Jurjī Zaydān and <b>Nöldeke in Arabic translation</b> — <i>the same published tables
our family’s own chart was compiled from, in another country, at the same
period</i>{c('Ighnāṭiyūs Ṭannūs al-Khūrī, <span class="ar">المشايخ آل الشمر حكام العاقورة والزاوية</span> (1948), read for this book in the scanned copy on the Internet Archive; the passages quoted are from the chapter <span class="ar">اسم الأسرة الشمرية وأصلها</span> and the chapter on Banū Ghassān. He cites Ibn Khaldūn for thirty-two Ghassanid kings over six hundred years and Nöldeke, <i>Die ghassânischen Fürsten</i>, in the Arabic version of Bandaliyya and Nadīq, for thirty-seven. <b>That monograph has since been pressed into service, in our own century, to support a claim of surviving royal descent and title. This book takes no view on that beyond one observation: its author took no such view either.</b> He wrote <i>zaʿm</i>, and he printed where his chain broke.')}.</p>
<p style="max-width:none"><b>So this was a common pattern, and it is not a scandal.</b> Christian
families across the Levant fixed a Ghassanid descent in writing in the first half of the twentieth
century, compiling the deep end from the same nineteenth-century European and Arabic tables. Some
printed it as a claim. One invented a chain of names. <b>What distinguishes them is not whether they
had a gap — they all had the same gap — but what each of them did with it.</b></p>
<p style="max-width:none">Our family has that gap and does not fill it. Ours runs from
<b>569 to about 1500</b>: thirty generations with no name of any kind, and we print them as a
void, thirty blank slots on every ladder in it. <i>The difference between a history and a pedigree is
what you do with the blank.</i> John Mogannam’s chart prints generation 35 as a void where Maalouf
filled the gap with names, and al-Khūrī printed <i>zaʿm</i>. <b>Two of those three are honest documents, and
ours is one of them.</b></p></div></div>"""),

ent('II', 'attested', True, 'Our contribution to the Palestinian people',
 '<b>Our family is one arrival among ten that became one people.</b> The genetics say the people of this land took in every newcomer for four thousand years. Our family’s stream, Christian Arabs out of the Ghassanid south, was taken in like the rest. Then it did its own taking in. Eight outsider families were folded into the clans from 1750. A Muslim neighbour was taken into the clan structure in 1923, in a town that had had Muslim households since 1538–39. And some nine thousand refugees were taken in by a town the government had counted at 5,080 in 1945. <i>The tradition says we came from somewhere. The ground says we have been here the whole time. Both are true at once, and in this country they always have been.</i>'),

ent('III', 'documents', True, 'The founding of Ramallah',
 'The documents give these dates: <b>named 1186</b>; endowed to Hebron 1279–80; uninhabited endowment land 1525–28; four households 1538–39; the group at Beit Jala 1553–54; the Christian settlement, agreed 1561 and counted 1562; the deed in court 1565; eighty households counted 1596, whose names are still unread in Ankara. The tradition gives Rāshid, the ford, the forge, the purchase from the Ghazāwneh, and “about 1550.” <b>The document and the memory are twelve years apart, and the memory loses nothing by the correction.</b>',
 f"""
{NUMTABLE('THE KEY DATES — one page, for the book',
 ['Date', 'Event', 'Carried by'],
 [['8th–7th c. BCE', 'The Maʾrib dam is built, in the country scripture assigns the line', 'inscription + both family texts'],
  ['528–569', 'Al-Ḥārith ibn Jabala, phylarch — generation 34', 'Procopius, contemporary'],
  ['543–548', 'The dam breaks (Abraha’s repair, CIH 541); final collapse follows', 'inscription'],
  ['c. 890', 'Last named Ghassān population in Transjordan — Gharandal', 'al-Yaʿqūbī'],
  ['1186', 'Rām Allāh first named — as the place a Crusader king’s road leads to', 'Strehlke no. 20; Ḥammūdeh (2014), p. 39'],
  ['1279–80', 'The hill endowed to the Ibrāhīmī sanctuary at Hebron', 'sijill 48, p. 88 (1565)'],
  ['<b>c. 1300</b>', '<b>Ghassān still entered as a living people — al-Balqāʾ, the Yarmūk, Ḥimṣ</b>', 'al-Ḥamdānī the <i>mihmandār</i>, via al-ʿUmarī and al-Qalqashandī'],
  ['1495', 'Mujīr al-Dīn, at Jerusalem, mentions the Ghassānids once and formulaically', '<i>al-Uns al-jalīl</i>, searched complete in two editions'],
  ['c. 1500', 'Rāshid al-Ḥaddādīn — generation 66', 'both family texts'],
  ['<b>1561–62</b>', '<b>The Christian settlement: terms agreed in court in 1561; counted in 1562 as 71 Christian taxpayers, 63 households and 8 single men, beside 10 Muslim households already on the hill</b>', 'the court record of 968/1561; the register of 970/1562, transcribed in full'],
  ['1596–97', 'The register counts 80 households, 71 Christian — the names are in Ankara, not yet read by us', 'the defter'],
  ['1850 · 1852', 'The present church — portal datestone 1850, inauguration usually given as 1852', 'Shāhīn + the carved portal'],
  ['1901', 'The first four sail for America', 'Shāhīn, name by name'],
  ['1908', 'Ramallah a city — one councilman per clan', 'the town record'],
  ['1916', 'Typhus — Shāhīn puts the losses near a third; no independent record survives', 'Shāhīn, as family memory'],
  ['1948', 'The town triples with refugees', 'the local count of 1953'],
  ['1952 · 1959 · 1963', 'The Federation: its magazine begun, the Federation constituted at Detroit on 7 September 1959, and recognised by the IRS', '<i>Pictorial History</i> II, ch. 32; the convention roster; IRS ruling'],
  ['20 May 1963', 'The hospital the diaspora paid for opens', 'the Foundation’s record']],
 'Entries carried by both key texts — Shāhīn (1982) and the Mogannam chart/presentation — are the spine; documents refine them. <b>Two entries rest on memory alone or on memory in conflict, and are marked as such:</b> the typhus toll of 1916 and the four who first sailed in 1901.')}
{fig(R.fig_master(),'The whole story on one scale',
 'Adam to the present, with the evidence that carries each stretch. Read left to right, the chart is a map of what kind of thing holds the story up at each point — and where the joints are.',
 'This book, throughout; the six grades applied consistently.')}
<p><i>At the end, after the bibliography, we list all thirty-six claims that can be checked, one by
one, with what we found for each.</i></p>
<p><b>What we still don’t know.</b> Some answers are waiting in known places. Ramallah City Hall holds
two of them in one building. The first is <b>ʿAdnān al-Ḥaddādīn’s handwritten manuscript of 8 August
1953</b>, whose account of the migration Shāhīn prints in full. The second is <b>the Turkish census book
Shāhīn himself found and used there</b>. He cites it for a figure of 13,600 souls, almost certainly the
district rather than the town. Others are the Jerusalem sijill, the court register, 48, p. 54, read in the original; <i>Mirʾāt
al-Sharq</i>, 1,132 digitised issues with 1,535 mentions of the town; and the Federation’s own
incorporation papers. And, if the family wishes it, there is Y-DNA, the only truly new evidence our
history can still gain{c('The open leads in full, with their targets named, in the project’s research notes; the Maalouf case (a Ghassanid pedigree demonstrably invented 1901–1908) is the standard the family’s claim was measured against — and survives, precisely because the chart printed a void where Maalouf printed a forgery.')}. Readers who can reach any of these can help us finish the work.</p>
<p class="closing"><b>A family that can tell the difference between what it remembers and what it can
prove, and gives both, has a history, not a story about itself.</b> This is that history: one line,
from Adam and Eve to this morning, with the evidence attached at every date where evidence exists,
and the gaps drawn where it does not.</p>""")

# ═════════════════════════════ ASSEMBLY ═════════════════════════════
def scope_css(css, scope):
    out = []; i = 0; n = len(css)
    def prefix(sel):
        parts = []
        for x in sel.split(','):
            x = x.strip()
            if not x: continue
            if x in (':root', 'html', 'body', '*'):
                parts.append(scope if x != '*' else scope + ' *')
            elif x.startswith('body'):
                parts.append(scope + x[4:])
            else:
                parts.append(scope + ' ' + x)
        return ','.join(parts)
    while i < n:
        j = css.find('{', i)
        if j < 0: break
        sel = css[i:j].strip()
        d = 0; k = j
        while k < n:
            if css[k] == '{': d += 1
            elif css[k] == '}':
                d -= 1
                if d == 0: break
            k += 1
        bodyc = css[j+1:k]
        if sel.startswith('@'):
            if sel.startswith('@media'):
                if 'prefers-color-scheme' in sel or 'print' in sel:
                    pass
                else:
                    out.append(sel + '{' + scope_css(bodyc, scope) + '}')
            else:
                out.append(sel + '{' + bodyc + '}')
        else:
            out.append(prefix(sel) + '{' + bodyc + '}')
        i = k + 1
    return '\n'.join(out)

def appendix_bibliography():
    src = open(_asset('AFRP_Ramallah_Bibliography_v4.html'), encoding='utf-8').read()
    m = re.search(r'<style>(.*?)</style>', src, re.S)
    css = scope_css(m.group(1), '.appx')
    i = src.find('<main>'); j = src.find('<footer')
    bodyc = src[i+len('<main>'):j].replace('</main>', '')
    bodyc = re.sub(r'<div class="controls">.*?</div>\s*</div>', '', bodyc, flags=re.S)
    bodyc = re.sub(r'id="(s[a-z0-9]+|x{1,3}[a-z]*\d*)"', lambda m: 'id="b_' + m.group(1) + '"', bodyc)
    bodyc = re.sub(r'href="#(s[a-z0-9]+|x{1,3}[a-z]*\d*)"', lambda m: 'href="#b_' + m.group(1) + '"', bodyc)
    # The bibliography and the One Line share several class names — .entry above
    # all, which is a timeline row here and a source card there. Everything the
    # host stylesheet would otherwise impose on the appendix is undone first,
    # then the appendix is set for reading rather than for reference.
    fixc = (
      # 1. tables never widen the page
      '.appx table{width:100%!important;max-width:100%!important;table-layout:fixed!important;border-collapse:collapse}'
      '.appx td,.appx th{white-space:normal!important;word-break:break-word;overflow-wrap:anywhere;vertical-align:top;'
        'padding:7px 10px!important;line-height:1.55!important}'
      '.appx code,.appx .fn{white-space:normal!important;overflow-wrap:anywhere}'
      '.appx img,.appx svg{max-width:100%;height:auto}.appx *{max-width:100%}'
      # 2. undo the timeline layout leaking into the source cards
      '.appx .entry{display:block!important;grid-template-columns:none!important;gap:0!important;'
        'position:static!important;margin:0 0 14px!important;padding:17px 20px!important;'
        'border:1px solid #E4DFD3!important;border-left:3px solid #DCD6C9!important;border-radius:5px!important;'
        'background:#FCFBF8!important}'
      '.appx .entry::before,.appx .entry::after{content:none!important;display:none!important}'
      '.appx .entry.star,.appx .entry:has(.star){border-left-color:#B98A4E!important}'
      # 3. set the appendix for reading
      '.appx{font-size:1.005rem;line-height:1.72}'
      '.appx .entry .t{display:block!important;font-size:1.06rem!important;line-height:1.5!important;'
        'font-weight:700!important;color:#1A1A1A!important;margin:0 0 4px!important}'
      '.appx .entry .imp{display:block!important;margin:0 0 8px!important;color:#77726A!important;'
        'font-style:italic!important;font-size:.95rem!important}'
      '.appx .entry .an{font-size:1rem!important;line-height:1.72!important;color:#46423B!important;'
        'margin:0 0 10px!important;max-width:70ch}'
      '.appx .entry .n,.appx .entry .nores{font-size:.95rem!important;line-height:1.65!important}'
      # 4. badges: one clear row, never mid-sentence
      '.appx .badge{display:inline-block;margin:2px 6px 2px 0;padding:2px 8px;border-radius:3px;'
        'font-size:.72rem;letter-spacing:.06em;line-height:1.7;vertical-align:middle}'
      # 5. section headings get air and a rule, so the shelves are findable
      '.appx h2:not(.parthead){margin:46px 0 6px!important;padding:0 0 8px!important;font-size:1.42rem!important;'
        'border-bottom:2px solid #B98A4E!important;color:#004A26!important}'
      '.appx h2.parthead{margin:56px 0 0!important;padding:26px 30px 18px!important;'
        'background:#004A26!important;color:#F3ECDD!important;border:0!important;border-radius:8px!important;'
        'font-size:1.8rem!important;line-height:1.25!important}'
      '.appx h2.parthead .pnum{display:block!important;font-size:.62rem!important;letter-spacing:.26em!important;'
        'color:#9BC3A8!important;font-weight:700!important;margin-bottom:9px!important}'
      '.appx h3{margin:28px 0 8px!important;font-size:1.12rem!important;color:#1A1A1A!important;'
        'border-bottom:1px solid #ECE6D9!important;padding-bottom:5px!important}'
      '.appx h4{margin:20px 0 6px!important}'
      '.appx .secnote{font-style:italic;color:#77726A;margin:0 0 16px!important;max-width:70ch}'
      '.appx .toc,.appx .policy,.appx .shelf,.appx .queue,.appx .gaps{border-radius:6px!important}'
      '.appx ol,.appx ul{line-height:1.8}'
      '.appx li{margin-bottom:4px}'
      # 6. filenames and links stay legible at reading size
      '.appx .fn{font-size:.86rem!important;background:#F4F1E9;padding:1px 5px;border-radius:3px;color:#5A554C}'
      '.appx a{overflow-wrap:anywhere}'
      '.appx .qhave,.appx .qw,.appx .qn{white-space:normal!important;overflow-wrap:anywhere;'
        'display:inline-block;max-width:100%}')
    newin = """
<div class="howto" style="margin:0 0 30px;border-left-color:#004A26">
<h4 style="color:#004A26">New in this edition — and it closes an open lead</h4>
<p><b>Cadora, Joseph Jiryes.</b> <span class="ar">تاريخ مدينة رام الله</span>
[<i>History of the City of Ramallah</i>]. New York: al-Hudá Press, 1954. 159 pp. — and its English
translation, <b><i>Remembering Ramallah: A Preservation of History</i></b>, translated and annotated by
<b>Samira Rafidi Meghdessian</b>, edited by Paula Whitacre, foreword by Frederic J. Cadora
(privately printed, 2023). ISBN 979-8-3507-0767-0.</p>
<div class="mgrid2">
<div><b>Why it matters.</b> The first history of Ramallah ever written, by a man who had been the
town&rsquo;s mayor from 1943 to 1947. Sāmiḥ Ḥammūdeh&rsquo;s archival work on the founding — the work
behind the 1562 entries in this book — quotes it throughout and credits it. Shāhīn takes his census
figures from it, citing &ldquo;pp. 136&ndash;37.&rdquo;</div>
<div><b>Why the project could not find it.</b> It had been sought as &ldquo;Qadūra, <i>The History of
Ramallah</i>, Huda Press.&rdquo; <b>Cadora and Qadūra are the same surname and the same man</b>, and the
imprint is al-Hudá. That is the whole reason the search failed.</div>
<div><b>What is in it.</b> Per the translator&rsquo;s own account: daily life, sects, schools and
societies; foods, weddings and festivals; a section of <b>folk songs translated out of the local
dialect</b>; infrastructure — water, electricity, the hospital, banks, hotels; and <b>appendices
tracing the clans to the five sons of Rāshid al-Ḥaddādīn</b>.</div>
<div><b>Where to get it.</b> Print only; no ebook, and <b>no library copy has been traced
anywhere</b>. Sold by the Palestine Museum US at $30 and directly by the family.
<i>The AFRP does not hold it, and should.</i></div>
<div><b>Also new, and now identified.</b> <b>Munther Haddadin</b>, <span class="ar">دولة الغساسنة؛
أصيلها ورحيلها</span> (<i>The Ghassanid State: Its Origin and Its Departure</i>). Amman:
<span class="ar">دار ورد الأردنية للنشر والتوزيع</span>, 2024. ISBN 978-9923-76-975-1.
<b>This is the source of the Karak wheel</b> — plate 84 — which the family presentation captions as a
separate 2025 title. <i>There is no separate 2025 title. “Warda Books” is <span class="ar">دار
ورد</span>.</i> The AFRP does not hold it, and should.</div>
</div>
</div>
"""
    # the extracted body has historically come out one </div> heavy, which used
    # to close the host page's own wrapper and let everything after the appendix
    # run edge to edge. Balance it explicitly rather than counting by hand.
    d = bodyc.count('<div') - bodyc.count('</div>')
    if d > 0:
        bodyc += '</div>' * d
    elif d < 0:
        bodyc = '<div>' * (-d) + bodyc
    return ('<style>' + css + fixc + '</style>\n<div class="appx"><div class="wrap">'
            + newin + bodyc + '</div></div>')

CSS = """
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:#FFFAF0;color:#1A1A1A;
  font:17px/1.68 "Times New Roman",Times,"Liberation Serif",Georgia,serif;
  -webkit-text-size-adjust:100%}
.wrap{max-width:900px;margin:0 auto;padding:0 26px}
.ar{font-family:"Geeza Pro","Noto Naskh Arabic","Times New Roman",serif;unicode-bidi:isolate}
.gk{font-family:"Times New Roman",Times,serif}
.pbar{position:fixed;top:0;left:0;right:0;height:3px;z-index:60}
.pbar i{display:block;height:100%;width:0;background:#B98A4E}

header.masthead{background:#FFFAF0;border-bottom:1px solid #DCD6C9;padding:26px 0 34px}
.updated{margin:0 0 6px;font-size:.88rem;font-weight:700;color:#007a3d;letter-spacing:.04em}
.mastrow{display:flex;justify-content:space-between;align-items:baseline;
  font:11px/1.4 "Times New Roman",Times,serif;letter-spacing:.22em;text-transform:uppercase}
.mastrow .l{color:#B98A4E;font-weight:700}
.mastrow .r{color:#77726A;letter-spacing:.12em}
.mastrule{border:0;border-top:1px solid #DCD6C9;margin:9px 0 30px}
header h1{font-size:2.7rem;line-height:1.1;letter-spacing:-.015em;margin:0 0 12px;font-weight:700}
header .sub{color:#77726A;font-style:italic;font-size:1.16rem;margin:0 0 14px;max-width:36em}
header .meta{color:#9A958C;font-size:.86rem;letter-spacing:.04em}
.rule-gold{border:0;border-top:3px solid #B98A4E;width:132px;margin:22px 0 0}
.standfirst{font-size:1.06rem;color:#46423B;max-width:38em;margin:26px 0 0}
.standfirst b{color:#1A1A1A}
.howto{background:#FFFFFF;border:1px solid #DCD6C9;border-left:3px solid #B98A4E;border-radius:4px;
  padding:20px 24px;margin:30px 0 0;font-size:.95rem;color:#46423B}
.howto h4{margin:0 0 10px;font-size:.72rem;letter-spacing:.2em;text-transform:uppercase;color:#B98A4E}
.howto .g{margin-right:5px}
.howto p{max-width:none;margin:0 0 10px}

/* era bands */
.eraband{background:#004A26;color:#F3ECDD;border-radius:12px;margin:84px 0 40px;padding:30px 34px;position:relative;z-index:2}
.erahead .eraband{border-radius:12px 12px 0 0}
.eraband .ek{font-size:.62rem;letter-spacing:.28em;color:#9BC3A8;font-weight:700;margin-bottom:9px;text-transform:uppercase}
.eraband h2{margin:0 0 8px;font-size:2rem;letter-spacing:-.012em;color:#F3ECDD}
.eraband .es{color:#CFE3D6;font-style:italic;font-size:1.04rem}
.eraband .es::before{content:"";display:block;width:120px;border-top:3px solid #3E7A56;margin:10px 0 12px}

/* entries — the unbroken line */
.chron{position:relative}
.chron::before{content:"";position:absolute;left:104px;top:0;bottom:0;width:2px;background:#DCD6C9}
.entry{position:relative;display:grid;grid-template-columns:88px 1fr;gap:34px;margin:0 0 42px}
.entry::before{content:"";position:absolute;left:98px;top:8px;width:14px;height:14px;border-radius:50%;
  background:#FFFAF0;border:3px solid #B98A4E}
.entry.major::before{background:#B98A4E}
.ewhen{text-align:right;padding-top:2px}
.ewhen .d{display:block;font-weight:700;color:#9A6324;font-size:1.02rem;line-height:1.25}
.ewhen .g{display:inline-block;margin-top:7px;padding:3px 7px;border-radius:3px;
  font:8.6px/1.4 "Times New Roman",Times,serif;font-weight:700;letter-spacing:.09em}
.ewhen .w2{display:inline-block;margin-top:5px;padding:3px 7px;border-radius:3px;
  background:#004A26;color:#F3ECDD;font:8.6px/1.4 "Times New Roman",Times,serif;
  font-weight:700;letter-spacing:.09em}
.ebody h3{margin:0 0 8px;font-size:1.24rem;letter-spacing:-.005em;line-height:1.3}
.ebody .note{color:#46423B;font-size:1rem;max-width:40em}
.ebody .note b{color:#1A1A1A}
.ebody .more{margin-top:14px}
p{margin:0 0 16px;max-width:40em}
.w2{white-space:nowrap}
span.w2{background:#004A26;color:#F3ECDD;padding:2px 7px;border-radius:3px;
  font-size:.7em;font-weight:700;letter-spacing:.09em}
.ewhen .w2.sh{background:#F6EEDF;color:#7A5A28;border:1px solid #E0CFAE}

.erahead{position:relative;z-index:2;margin:84px 0 48px}
.partband{position:relative;z-index:2;margin:110px 0 0;padding:44px 0 18px;text-align:center;border-top:4px double #007a3d}
.partband .pk{font-size:.7rem;letter-spacing:.32em;color:#9a6324;font-weight:700;text-transform:uppercase}
.partband h2{margin:8px 0 0;font-size:2.4rem;color:#004A26;letter-spacing:-.01em}
.partband+.erahead{margin-top:28px}
@media print{.partband{break-before:page}}
.erahead .eraband{margin:0}
.erahead:first-child{margin-top:0}
.linkat{margin:0;padding:16px 34px 18px;background:#FCFBF8;
  border:1px solid #DCD6C9;border-top:0;border-radius:0 0 12px 12px}
.linkat::before{content:"";position:absolute;left:0;width:4px;top:0;bottom:0;background:transparent}
.linkat .lkhead{font:700 9.4px/1 "Times New Roman",Times,serif;letter-spacing:.22em;
  text-transform:uppercase;color:#B98A4E;margin-bottom:9px}
.linkat .lkrow{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px}
.linkat .lkname{font-weight:700;color:#1A1A1A;font-size:1.05rem;flex:1 1 auto}
.linkat .g{flex:0 0 auto}
.linkat .lknote{margin-top:6px;color:#46423B;font-size:.97rem;line-height:1.6;max-width:64em}
.linkat .lkladder{margin-top:14px;padding-top:12px;border-top:1px solid #ECE6D9}
@media print{.erahead{break-inside:avoid}}

.sect{position:relative;z-index:1;margin:36px 0 26px;padding:0 0 0 122px}
.sect::before{content:"";position:absolute;left:105px;top:9px;width:9px;height:9px;
  border-radius:50%;background:#FFFAF0;border:2px solid #DCD6C9}
.sect .sl{display:block;font:700 9.6px/1 "Times New Roman",Times,serif;letter-spacing:.22em;
  text-transform:uppercase;color:#B98A4E;margin-bottom:5px}
.sect .ss{display:block;font-style:italic;color:#77726A;font-size:1.02rem;line-height:1.4;
  padding-bottom:9px;border-bottom:1px solid #E8E2D5}
@media(max-width:760px){.sect{padding-left:26px}.sect::before{left:-3px}}
.wwsdk{position:relative;z-index:1;margin:30px 0 40px 122px;padding:16px 22px;border:1px solid #E4DCCB;border-left:4px solid #9a6324;background:#FCFAF5}
.wwsdk h4{margin:0 0 8px;font:700 .8rem/1.2 "Times New Roman",Times,serif;letter-spacing:.14em;text-transform:uppercase;color:#9a6324}
.wwsdk p{margin:.5em 0;max-width:none}
@media(max-width:760px){.wwsdk{margin-left:0}}
/* v66: the reading list that closes each chapter */
.scholars{position:relative;z-index:1;margin:30px 0 18px 122px;padding:16px 22px;border:1px solid #D9E6DD;border-left:4px solid #007a3d;background:#F8FBF8}
.scholars h4{margin:0 0 10px;font:700 .8rem/1.2 "Times New Roman",Times,serif;letter-spacing:.14em;text-transform:uppercase;color:#007a3d}
.scholars ul{list-style:none;margin:0;padding:0}
.scholars li{margin:0 0 12px;line-height:1.5}
.scholars .sw{display:block;font-weight:700;color:#1A1A1A}
.scholars .sp{display:block;font-size:.86rem;color:#77726A}
.scholars .sl2{display:block;font-size:.98rem;color:#46423B}
.scholars .sfoot{margin:6px 0 0;font-size:.86rem;color:#77726A;max-width:none}
@media(max-width:760px){.scholars{margin-left:0;padding:14px 16px}}
figcaption .made{font-variant:small-caps;letter-spacing:.04em;color:#9a6324;font-weight:700}

.byline{margin:8px 0 0;font-size:1.06rem;letter-spacing:.05em;color:#1A1A1A}
.front{margin:22px 0 4px;max-width:44em}
figure.frontis{margin:18px 0 10px;border:0;background:none;text-align:center;max-width:44em}
figure.frontis img{display:inline-block;width:100%;max-width:520px;height:auto;mix-blend-mode:multiply}
figure.frontis figcaption{padding:4px 0 0;font-style:italic;color:#6B6760;font-size:.9rem;text-align:center}
figure.frontis::after{content:"";display:block;width:180px;height:1px;margin:14px auto 0;background:#9A6324}
figure.photo{margin:24px 0 30px;padding:14px 14px 0;position:relative;z-index:1}
figure.photo::before{content:"Photograph";display:flex;align-items:center;gap:10px;color:#9A6324;
  font:700 10px/1 "Times New Roman",Times,serif;letter-spacing:.26em;text-transform:uppercase;margin:0 4px 10px}
figure.photo img{display:block;width:auto;max-width:min(100%,820px);max-height:640px;height:auto;border-radius:0;
  border:1px solid #007A3D;padding:5px;background:#FFFFFF;box-sizing:border-box;
  filter:grayscale(.2) sepia(.12) contrast(1.03)}
figure.photo figcaption{max-width:820px;padding:10px 4px 14px;font-style:italic}
figure.photo figcaption .src{font-style:normal}
figure.photo.srcpage::before{content:"From the source"}
figure.photo.srcpage img{filter:none;max-height:780px}
figure.photo.period::before{content:"From the period"}
.front h3{font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;color:#8A6A2E;margin:22px 0 6px}
.front .ded{font-style:italic;font-size:1.05rem;line-height:1.6;margin:0}
.front p{line-height:1.6;margin:0 0 10px}
.credit{margin:6px 0 0;font-size:.86rem;line-height:1.5;color:#77726A;max-width:44em}
.credit b{color:#46423B}
.contents{margin:26px 0 0;padding:20px 24px 16px;background:#FCFBF8;border:1px solid #DCD6C9;border-radius:6px}
.contents h4{margin:0 0 12px;font:700 10.5px/1 "Times New Roman",Times,serif;letter-spacing:.22em;
  text-transform:uppercase;color:#B98A4E}
.contents ol{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:0 34px}
.contents li{margin:0;display:flex;align-items:stretch;border-bottom:1px solid #F1EDE3}
.contents a{display:flex;gap:12px;align-items:baseline;width:100%;padding:7px 0;
  color:#1A1A1A;text-decoration:none}
.contents a:hover{color:#004A26}
.contents .cnum{flex:0 0 5.6em;color:#9A958C;font-size:.76rem;line-height:1.55;
  letter-spacing:.12em;text-transform:uppercase}
.contents .ctit{flex:1;font-weight:600;line-height:1.45}
.contents .cgen{display:block;font-weight:400;font-size:.8rem;color:#9A958C;letter-spacing:.03em}
.contents .cend{margin:14px 0 0;font-size:.9rem;color:#77726A}
.contents .cend a{display:inline;border:0;color:#004A26}
@media(max-width:760px){.contents ol{grid-template-columns:1fr}.contents .cnum{flex-basis:5em}}

/* v61: every figure and photograph takes the family tree book's plate:
   white paper, a green double rule above, a thin green rule below, an ochre
   figure number on a green diamond rule, Times throughout. */
figure{margin:30px 0;padding:0;border:0;border-top:3px double #007A3D;border-bottom:1px solid #007A3D;
  border-radius:0;background:#FFFFFF;overflow:hidden;font-family:"Times New Roman",Times,serif}
.fignum{display:flex;align-items:center;gap:10px;background:none;color:#9A6324;
  font:700 10px/1 "Times New Roman",Times,serif;letter-spacing:.26em;text-transform:uppercase;
  padding:12px 18px 6px;border:0}
.fignum::before{content:"";flex:0 0 7px;height:7px;background:#007A3D;transform:rotate(45deg)}
.fignum::after{content:"";flex:1;height:1px;background:linear-gradient(90deg,#9A6324,rgba(154,99,36,0))}
.figtitle{font-size:1.1rem;font-weight:700;padding:6px 18px 0;color:#1A1915}
.figwrap{padding:8px 12px 4px}
.figwrap svg{display:block;width:100%;height:auto}
figcaption{padding:6px 18px 16px;color:#3D3A35;font-size:.92rem;line-height:1.55;max-width:none}
figcaption .src{display:block;margin-top:8px;padding-top:7px;border-top:1px solid #E9D7BD;
  color:#9A6324;font-size:.8rem;font-style:italic}

blockquote{margin:22px 0;padding:18px 22px;background:#fff;border:1px solid #DCD6C9;
  border-left:3px solid #007A3D;border-radius:4px;font-size:1.05rem;max-width:40em}
blockquote .cite{display:block;margin-top:10px;color:#77726A;font-size:.88rem;font-style:italic}

.fix{background:#FFFFFF;border:1px solid #E8D9BE;border-left:4px solid #A85210;border-radius:4px;
  padding:16px 20px;margin:22px 0}
.fix .fixhead{font-size:.68rem;letter-spacing:.2em;text-transform:uppercase;color:#A85210;font-weight:700;margin-bottom:10px}
.fix .pull{margin:14px 0;padding:12px 16px;background:#FCFBF8;border-left:3px solid #B98A4E;border-radius:3px;font-size:1.02rem}
.fix .pull .ar{font-size:1.12rem;line-height:1.9}
.fixgrid{display:grid;grid-template-columns:1fr 1fr 1.2fr;gap:16px}
.fixgrid > div{font-size:.92rem;line-height:1.5;color:#46423B}
.fixgrid .fl{display:block;font-size:.62rem;letter-spacing:.14em;text-transform:uppercase;color:#9A958C;margin-bottom:4px}

.ntwrap{margin:22px 0;border:1px solid #DCD6C9;border-radius:4px;overflow:hidden;background:#fff}
.nthead{background:#F6F3EC;color:#9A6324;font:10.5px/1.4 "Times New Roman",Times,serif;
  font-weight:700;letter-spacing:.18em;text-transform:uppercase;padding:11px 16px;border-bottom:1px solid #DCD6C9}
table.ntable{width:100%;border-collapse:collapse;font-size:.94rem}
table.ntable th{background:#FCFBF8;text-align:left;font-weight:700;color:#77726A;
  font-size:.78rem;letter-spacing:.1em;text-transform:uppercase;padding:9px 16px;border-bottom:1px solid #DCD6C9}
table.ntable td{padding:8px 16px;border-bottom:1px solid #F1EDE4;color:#46423B}
table.ntable tr:last-child td{border-bottom:0}
table.ttable{width:100%;border-collapse:collapse;font-size:.92rem}
table.ttable th{background:#FCFBF8;text-align:left;font-weight:700;color:#77726A;
  font-size:.74rem;letter-spacing:.1em;text-transform:uppercase;padding:9px 14px;border-bottom:1px solid #DCD6C9}
table.ttable td{padding:10px 14px;border-bottom:1px solid #F1EDE4;vertical-align:top}
table.ttable td.when{white-space:nowrap;color:#9A6324;font-weight:700;width:1%}
table.ttable td.gr{width:1%;white-space:nowrap;text-align:right}
table.ttable td.what b{color:#1A1A1A}
table.ttable .tn{display:block;margin-top:3px;color:#46423B;font-size:.86rem;line-height:1.5}
table.ttable tr:last-child td{border-bottom:0}
.mgrid2{display:grid;grid-template-columns:1fr 1fr;gap:12px 24px;margin:14px 0 0}
.mgrid2 > div{font-size:.92rem;line-height:1.52;padding-left:12px;border-left:2px solid #DCD6C9}
@media (max-width:760px){.mgrid2{grid-template-columns:1fr}}
.tfoot{padding:11px 16px;background:#FCFBF8;border-top:1px solid #EFEBE2;font-size:.85rem;color:#77726A;font-style:italic;line-height:1.5}

code.fn{font:12.5px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;background:#F3F0E8;
  white-space:normal;overflow-wrap:anywhere;word-break:break-word;max-width:100%;
  border:1px solid #E5E0D4;border-radius:3px;padding:1px 5px;color:#6B6459}
sup.cn{font-size:.68em;line-height:0}
sup.cn a{color:#007A3D;text-decoration:none;padding:0 1px}
.notes ol{padding-left:26px;max-width:44em}
.notes li{margin:0 0 8px;font-size:.88rem;color:#46423B;line-height:1.55}
.notes li a{color:#B98A4E;text-decoration:none}
p.closing{font-size:1.12rem;border-top:2px solid #B98A4E;padding-top:18px;margin-top:26px}
.appx{margin-top:16px}
.appx .wrap{padding:0}
footer.end{border-top:1px solid #DCD6C9;margin-top:70px;padding:26px 0 90px;color:#9A958C;font-size:.84rem}
@media (max-width:720px){
  header h1{font-size:2rem}
  .chron::before{left:8px}
  .entry{grid-template-columns:1fr;gap:8px}
  .entry::before{left:2px}
  /* the rail sits at 8px, so the whole entry, not just its date, steps clear of it */
  .entry{padding-left:26px}
  .ewhen{text-align:left;padding-left:0}
  .mastrow{flex-direction:column;gap:4px}
  .eraband h2{font-size:1.5rem}
  .fixgrid{grid-template-columns:1fr}
}

/* ═══════════ reading it on a telephone ═══════════
   Two problems, and they are different problems.

   The plates are drawn on an 860-unit sheet. Poured into a 390px screen that is
   a scale of 0.36, and a 9pt label becomes 3pt — present, and unreadable. So on
   a narrow screen the plate keeps a floor width and the reader swipes it
   sideways, which is what one does with a large map on a small table. The same
   goes for the wide tables: columns intact, moved under the thumb, rather than
   reflowed into towers.

   And the book is four hundred thousand pixels tall. content-visibility lets the
   browser skip layout and paint for everything off-screen, which is nearly all of
   it. Find-in-page still reaches inside; the reserved heights keep the scrollbar
   from lurching. */
@media (max-width:760px){
  /* A grid or flex item defaults to min-width:auto, so a 720px plate inside one
     stretches its own track and quietly pushes the prose off the screen instead
     of scrolling. Every box between the entry and the plate has to be told it
     may be narrower than its contents. */
  .entry,.ebody,.more,.entry>*,figure,.figwrap{min-width:0}
  figure,.figwrap{max-width:100%}
  .figwrap{overflow-x:auto;overflow-y:hidden;-webkit-overflow-scrolling:touch;
    overscroll-behavior-x:contain;padding:6px 0 12px}
  .figwrap svg{width:720px;min-width:720px;max-width:none;height:auto}
  .fignum::after{content:"swipe the plate →";flex:1;height:auto;background:none;text-align:right;letter-spacing:.12em;color:#8F8A80}
  .ntwrap{overflow-x:auto;-webkit-overflow-scrolling:touch}
  table.ntable{min-width:580px}
  .entry{content-visibility:auto;contain-intrinsic-size:auto 620px}
  figure{content-visibility:auto;contain-intrinsic-size:auto 700px}
  /* A footnote can be three hundred thousand pixels away. Animating that is
     several seconds of the page flying past; on a telephone it should just
     arrive. */
  html{scroll-behavior:auto}
  blockquote{padding:14px 16px;font-size:1rem}
  .fix{padding:14px 16px}
  figcaption{padding:6px 14px 14px}
  .figtitle{padding:12px 14px 0;font-size:1rem}
}
/* v65.1: reading on a phone (David, 8 Nov 2026). Narrower gutters so a line
   holds more words, a Chapters button that is always under the thumb, the
   chain ladder swiped like the plates, and a hint on every wide table. */
.tocbtn{display:none}
@media (max-width:760px){
  .wrap{padding:0 14px}
  .entry{padding-left:18px}
  .chron::before{left:4px}
  .entry::before{left:-2px}
  .sect{padding-left:18px}
  .linkat{padding:14px 16px 16px}
  .linkat .lkladder{overflow-x:auto;-webkit-overflow-scrolling:touch}
  .linkat .lkladder svg{width:640px;min-width:640px;max-width:none;height:auto}
  .ntwrap{position:relative}
  .ntwrap::before{content:"swipe the table →";display:block;text-align:right;font-size:.72rem;letter-spacing:.12em;color:#8F8A80;padding:0 4px 4px}
  .eraband{padding-left:18px;padding-right:18px}
  .ebody h3{font-size:1.28rem;line-height:1.3}
  .note,.more p{font-size:1.04rem;line-height:1.62}
  .tocbtn{display:block;position:fixed;right:12px;bottom:14px;z-index:50;background:#007a3d;color:#fff;
    font:700 .8rem/1 "Times New Roman",Times,serif;letter-spacing:.08em;text-transform:uppercase;
    padding:11px 14px;border-radius:22px;box-shadow:0 2px 8px rgba(0,0,0,.25);text-decoration:none}
  .contents{scroll-margin-top:12px}
}
@media print{.tocbtn{display:none}}
@media (max-width:760px) and (prefers-reduced-motion:no-preference){
  .figwrap{scroll-behavior:smooth}
}
@media print{
  body{font-size:10.5pt;background:#fff}
  .pbar{display:none}
  figure,.ntwrap,.fix,blockquote{break-inside:avoid}
  .eraband{break-before:page}
  .erahead{break-before:page}
  .erahead .eraband{break-before:auto}
  a{color:inherit;text-decoration:none}
}
"""

PHOTOS = {
 1: [('ppmsca/13100/13196v.jpg', '2007675853', 'A Ramallah family outside their stone house, about 1900–1910.', 'American Colony Photo Department; the original caption reads “Peasant family of Ramallah.”')],
 2: [('matpc/04100/04114v.jpg', '2019694418', 'The walls of Tell es-Sulṭān, ancient Jericho, during the excavations of the 1930s, with Jabal Qurunṭul behind.', 'American Colony Photo Department, 1934–39.')],
 3: [('matpc/05500/05506v.jpg', '2019696806', 'The highland country of the Ramallah plateau, looking south-west from Tell en-Naṣba towards Nabī Ṣamwīl.', 'American Colony Photo Department, 1926.')],
 4: [('matpc/22900/22915v.jpg', '2019705575', 'The Iron Age city gate at Tell en-Naṣba, on the Jerusalem road, south of al-Bīra.', 'Matson Photo Service.')],
 5: [('matpc/01700/01719v.jpg', '2019693196', 'Qaṣr al-ʿAbd at ʿIrāq al-Amīr, a Hellenistic palace east of the Jordan and one of the few buildings of the period still standing.', 'American Colony Photo Department, about 1900–1920.')],
 6: [('matpc/22100/22165v.jpg', '2019713050', 'The Roman roads to Samaria and to Caesarea, forking on the ridge about four miles north of Jerusalem, from the air in 1931.', 'American Colony Photo Department.')],
 7: [('matpc/05300/05329v.jpg', '2019695358', 'The sixth-century mosaic map of the Holy Land in the Greek Orthodox church of St George at Mādabā.', 'American Colony Photo Department, about 1900–1920.')],
 8: [('matpc/03700/03718v.jpg', '2019694114', 'The east gate of the Umayyad palace at Khirbat al-Mafjar, near Jericho, during the excavations of the 1930s.', 'American Colony Photo Department, 1934–39.')],
 9: [('matpc/06900/06951v.jpg', '2019698794', 'Al-Karak: the town and its castle, built by the Crusaders and rebuilt by the Ayyubids and Mamluks.', 'American Colony Photo Department, 1898–1914.')],
 10: [('matpc/17000/17063v.jpg', '2019707840', 'Al-Shawbak castle from the air, 1937.', 'Matson Photo Service.')],
 11: [('matpc/22100/22174v.jpg', '2019713059', 'Bayt Jālā and its terraces from the air, 1931 — the town the Kasābra families came up from.', 'American Colony Photo Department.')],
 12: [('matpc/01000/01047v.jpg', '2019692544', 'Ramallah from the north, about 1900–1920.', 'American Colony Photo Department.'), ('matpc/00600/00662v.jpg', '2019692264', 'A Ramallah woman in the embroidered dress of the town.', 'American Colony Photo Department, negative 1898–1914.')],
 13: [('matpc/17700/17778v.jpg', '2019708548', 'Women of the Arab Women’s Union of Ramallah at work in the Union’s workrooms, late 1930s.', 'Matson Photo Service, 1934–39.'), ('matpc/03300/03332v.jpg', '2019696621', 'The broadcasting towers at Ramallah, the main transmitter of the Palestine Broadcasting Service from 1936.', 'American Colony Photo Department, 1934–39.')],
}
PHOTO_BASE = 'https://tile.loc.gov/storage-services/service/pnp/'

# v61: photographs and documents from Naseeb Shaheen, A Pictorial History of
# Ramallah, Part II (Birzeit University Press, 2005). David Saah: AFRP holds
# the rights to the book and to all the photographs in it. Files are web copies in img/shaheen/, named by PDF page.
SHAHEEN = {
 9: [('p030_1.jpg', 29, 'The charter of 7 March 1186, in the printed Latin that Shaheen reproduces. King Guy pledges a <i>casellum</i>, a small farm estate, to the Hospital of St Mary of the Germans. It lies near the royal road <i>qua vaditur Ramelie</i>, “by which one goes to Ramallah”. This is the first time the name is written down.')],
 11: [('p024_1.jpg', 23, 'The census of Bayt Jālā of 1553–54 (register 289), with the thirty-six families living there for the time being. Nine years later, in the census of 1562, they were no longer at Bayt Jālā. They had moved to Ramallah.')],
 12: [('p012_1.jpg', 11, 'Shaheen’s map of the places tied to the settlement of Ramallah, from al-Karak and al-Shawbak up to Bayt Jālā and Ramallah.'),
      ('p038_1.jpg', 37, 'A map of Palestine of 1639, with Ramallah on it as “Rammula”.'),
      ('p231_1.jpg', 230, 'Jacob Hishmeh of Ramallah with his son Shukri, a studio portrait from the 1870s on a card of the Bonfils studio and one of the oldest photographs of Ramallah people.'),
      ('p371_1.jpg', 370, 'An agreement of 15 June 1896: Ibrahim Daoud Harb lends Daoud Yaʿcoub Harb seven French gold liras, without interest, for a year and a half. The witnesses sign at the foot.'),
      ('p238_1.jpg', 237, 'A weaver at his loom in Ramallah, about 1890–1900. Elihu Grant counted about twelve weavers in the town at the turn of the century.'),
      ('p202_1.jpg', 201, 'A bride arrives at the house of the groom, Ramallah, 1900. Shaheen reads her dark coat as the red <i>aṭlas</i> of the groom’s Qaysī side; she carries a sword before her.')],
 13: [('p244_1.jpg', 243, 'The family of Elias ʿAudi, about 1905. He stands at the centre rear and was the first mayor of Ramallah, from the founding of the municipality until 1921. The family home was bulldozed by night in the spring of 2001.'),
      ('p172_1.jpg', 171, 'Ramallah from the south, about 1910: the town on its hill above terraced fields and vineyards.'),
      ('p245_2.jpg', 244, 'The Friends Meeting House on Main Street, about 1912, with the congregation outside. Vines still grew where office buildings stand today.'),
      ('p250_1.jpg', 249, 'Ibrahim Rasheed Hishmeh as a soldier in the Ottoman army, about 1916.'),
      ('p206_1.jpg', 205, 'The wedding of ʿAwad Shaheen and Maria Hanna Muhawi, 13 July 1930. Both were of the Sharaka clan. The photograph is by the Armenian photographer A. G. Krikorian of Jerusalem.'),
      ('p185_1.jpg', 184, 'A school for refugee children held in a Ramallah church, August 1949, a year after the expulsions from Lydda and Ramle filled the town.'),
      ('p228_1.jpg', 227, 'Manara Square, about 1953, with the column whose five lions stand for the five sons of Rāshid.'),
      ('p161_3.jpg', 160, 'Members of the Arab Women’s Union of Ramallah in the 1960s. Matiel Mogannam, who by Shāhīn’s account founded the Ramallah society in 1939, sits third from the right in the black dress.'),
      ('p162_2.jpg', 161, 'After the war of 1967 the Women’s Union fed as many as two hundred refugee children a hot noon meal. Standing are Ellen ʿAkel, Labeebeh Hishmeh Sayegh and Juliette Mogannam, about 1968–69.')],
}
LOCAL_PHOTOS = {
 12: [('memorial_bronze.jpg', 'The bronze memorial to the first family of Ramallah: Rāshid with his staff, his wife holding their daughter, and their five sons around them.',
       'Photograph from the AFRP family-tree archive. The same group, drawn in pencil, opens this book and the <i>Ramallah Family Tree</i>.')],
 13: [('period/spinning_1919.jpg', 'An old man of Ramallah in a sheepskin coat, spinning wool with a hand spindle, 1919.',
       'American Colony Photo Department, 1919. Public domain.')],
}
SHAHEEN_SRC = ('Naseeb Shaheen, <i>A Pictorial History of Ramallah, Part II</i> (Birzeit University Press, 2005), p. {p}. '
               'Reproduced courtesy of the American Federation of Ramallah, Palestine.')

def photos_for(num):
    out = []
    for path, item, cap, who in PHOTOS.get(num, []):
        out.append(f'<figure class="photo"><img src="{PHOTO_BASE}{path}" alt="{cap}" loading="lazy" decoding="async">'
                   f'<figcaption>{_made(path)}{cap}<span class="src">{who} Library of Congress, Prints &amp; Photographs Division, Matson Collection, '
                   f'<a href="https://www.loc.gov/item/{item}/">loc.gov/item/{item}</a> — no known restrictions on publication.</span></figcaption></figure>')
    for fn, cap, src in LOCAL_PHOTOS.get(num, []):
        alt = re.sub(r'<[^>]+>', '', cap)
        out.append(f'<figure class="photo"><img src="../img/{fn}" alt="{alt}" loading="lazy" decoding="async">'
                   f'<figcaption>{_made(fn)}{cap}<span class="src">{src}</span></figcaption></figure>')
    for fn, pg, cap in SHAHEEN.get(num, []):
        alt = re.sub(r'<[^>]+>', '', cap)
        out.append(f'<figure class="photo"><img src="../img/shaheen/{fn}" alt="{alt}" loading="lazy" decoding="async">'
                   f'<figcaption>{_made(fn)}{cap}<span class="src">{SHAHEEN_SRC.format(p=pg)}</span></figcaption></figure>')
    return ''.join(out)

# v61: pages from the sources themselves, and period plates, set inside the
# entries that use them. Files are web copies in img/sources/.
SOURCE_PAGES = [
 ('The name appears in 1186', 'srcpage', 'sources/strehlke_1869_p18_no20.jpg',
  'The charter of 7 March 1186 as Strehlke printed it in 1869, with <i>qua vaditur Ramelie</i>, “by which one goes to Ramallah”, boxed. This is the first time the name is written down.',
  'Ernst Strehlke, ed., <i>Tabulae Ordinis Theutonici</i> (Berlin, 1869), p. 18, no. 20. Public domain.'),
 ('The name appears in 1186', 'period', 'period/vesconte_c1320.jpg',
  'The Holy Land on the grid map Pietro Vesconte drew for Marino Sanudo’s crusade plan about 1320. This is the world in which the Mamluk endowment of 1279 already named Rām Allāh.',
  'After Pietro Vesconte, for Marino Sanudo, <i>Liber secretorum fidelium crucis</i> (c. 1320), in the engraved copy printed by Jacques Bongars, <i>Gesta Dei per Francos</i> II (Hanau, 1611). Public domain.'),
 ('Magna Mahumeria', 'period', 'period/bireh_church_1881.jpg',
  '“Ruins of Crusaders’ church at el Bîreh”: the three apses and north wall of the Frankish church at al-Bīra, Magna Mahumeria, with a cornfield growing inside it.',
  '<i>Picturesque Palestine, Sinai and Egypt</i>, ed. Charles W. Wilson (London, 1880–84), engraving. Public domain.'),
 ('The twin town', 'period', 'period/pef_1880_sheet17.jpg',
  'Râm Allah and el Bîreh, as the British surveyors wrote them, side by side on the road north from Jerusalem. The sheet was surveyed in 1878 and published in 1880.',
  'Palestine Exploration Fund, <i>Survey of Western Palestine</i>, 1 inch to the mile, sheet XVII (London, 1880), detail. Public domain.'),
 ('The twin town', 'period', 'period/bireh_khan_1881.jpg',
  '“A halt for the night in the khan of el Bîreh”: travellers and their camels round a fire under the vaults of al-Bīra’s caravan inn, which stood by the town’s main spring.',
  '<i>Picturesque Palestine, Sinai and Egypt</i>, ed. Charles W. Wilson (London, 1880–84), engraving. Public domain.'),
 ('What the family remembers', 'srcpage', 'sources/shahin_1982_p10.jpg',
  'The founding as ʿAzīz Shāhīn tells it, in his Arabic. The page opens: '
  '<span class="ar" dir="rtl">ويعرف اهالي رام الله ان راشدا الحداد واخاه صبره هما اول من سكن هذه المدينة</span>, '
  '“The people of Ramallah know that Rāshid al-Ḥaddād and his brother Ṣabra were the first to live in this town.” '
  'They do not agree on when, he goes on: some say the seventeenth century, others a century earlier. He then names the two texts the town has: '
  'ʿAdnān al-Ḥaddādīn’s account, written in a notebook kept at the Ramallah municipality and dated 8 August 1953, and the one Yūsuf Qaddūra gives in his <i>History of the City of Ramallah</i> (1954).',
  'ʿAzīz Shāhīn, <i>Kashf al-niqāb</i> (1982), p. 10. Digitised by Birzeit University Library.'),
 ('The Christian settlement', 'srcpage', 'sources/defter_1562_p73.jpg',
  'Ramallah in the endowment register of 1562, as the modern Turkish edition prints it (the two entries are boxed). '
  'On the right, <i>Karye-i Ramallah … tamāmen, hāsıl maʿa rüsūm 2905</i>: the whole village, endowed to the shrine of Abraham at Hebron, yielding 2,905 akçe with its dues. '
  'Below left, <i>Nasārā der-karye-i Ramallah … 71 neferen, fī 80, 5680</i>: the Christians of Ramallah, seventy-one persons at 80 akçe each, 5,680 akçe. '
  'This is the line that counts the families who came up from Bayt Jālā.',
  '<i>Defter-i Evkaf-ı Liva-i Kuds-i Şerif</i>, ed. Sevgi Işık (Ankara: Tapu ve Kadastro Genel Müdürlüğü, 2015), p. 73, an edition of TKG.KK.TTd. 406, folio 1. Transcription only; the Ottoman folio itself is not reproduced in the edition.'),
 ('The peasants’ revolt', 'srcpage', 'sources/robinson_1841_p263.jpg',
  'Edward Robinson at Jifnā on 13 June 1838, four years after the revolt. He eats lunch under a walnut tree inside the ruined church that the village’s Christian shaykh tells him was St George’s, where mass is still said now and then, and he ends: '
  '“The present inhabitants of Jufna are all Christians; they number only forty-two taxable men.”',
  'Edward Robinson and Eli Smith, <i>Biblical Researches in Palestine</i>, p. 263 of a later edition; the margin gives the pages of the first edition (Boston, 1841), vol. III, pp. 77–78. Public domain.'),
 ('The present Greek Orthodox church is built', 'srcpage', 'sources/guerin_1875_p40.jpg',
  'Victor Guérin pitches his tents at Ramallah on 25 May 1870 and writes the name in Arabic beside the French. '
  '“This town has about two thousand inhabitants, almost all belonging to the Greek Orthodox religion. Eighteen years ago they built a church there, constructed partly with the remains of an ancient church at Kharbet et-Thireh.” '
  'A Latin parish and school had been founded too, and the missionary told him he had barely a hundred and fifty parishioners.',
  'Victor Guérin, <i>Description géographique, historique et archéologique de la Palestine: Samarie</i>, vol. II (Paris, 1875), ch. 35, p. 40. Public domain. Guérin writes “grecque schismatique”, the French Catholic term of his day for Orthodox.'),
 ('The parish proves itself', 'srcpage', 'sources/seetzen_1854_p197.jpg',
  'Ulrich Jasper Seetzen on the road north of Jerusalem in 1806: “On our right we left the village of Taréndy, and further right of it Râm-Allah, a considerable village, inhabited mostly by Greek Christians, which cannot be seen from the road.” '
  'A little further on he passes al-Rām, the “small village of Râm”, with the ruins of a church.',
  'Ulrich Jasper Seetzen, <i>Reisen durch Syrien, Palästina, Phönicien, die Transjordan-Länder, Arabia Petraea und Unter-Aegypten</i>, ed. Fr. Kruse, vol. II (Berlin, 1854), p. 197. Public domain; scan from Heidelberg University Library.'),
 ('Elihu Grant writes', 'photo', 'sources/grant_1907_lane.jpg',
  '“Râm Allâh, as Entered by the Sinuous, Walled Lane, from the East”: the town as Elihu Grant knew it, stone field walls along the lane and the houses of the old town on the rise beyond.',
  'Elihu Grant, <i>The Peasantry of Palestine</i> (Boston: Pilgrim Press, 1907), plate. Public domain.'),
 ('Elihu Grant writes', 'photo', 'sources/grant_1907_schools.jpg',
  '“Mission Schools (sustained by the American Friends)”: pupils and teachers of the Friends schools at Ramallah, which Grant ran from 1901 to 1904.',
  'Elihu Grant, <i>The Peasantry of Palestine</i> (Boston: Pilgrim Press, 1907), plate. Public domain.'),
 ('The town votes', 'srcpage', 'sources/ramallah_1946_notice.jpg',
  'The committee’s notice of 6 April 1946: three districts filled without a contest, and five men nominated for the four seats of district 2, the Ḥaddāda, with the poll set for Monday 15 April.',
  'Notice signed by Mousa Khalil, chairman of the electoral committee for the Municipal Commission of Ramallah, 6 April 1946. Israel State Archives, P-213/40, PDF p. 91.'),
 ('The town votes', 'srcpage', 'sources/ramallah_1946_results_ar.jpg',
  'The committee’s own account, in Arabic, ending with item 13, the result: '
  '<span class="ar" dir="rtl">كانت نتيجة التصويت كما يلي</span>, “the result of the vote was as follows”: Jamīl Ṭūṭaḥ 255, Yūsuf Qaddūra 236, Khalīl Ṣalāḥ 222, Jalīl Ḥarb 215, Ḥannā Jābir 154.',
  'Ramallah municipality, “Intikhābāt baladiyyat Rām Allāh”, p. 2. Israel State Archives, P-213/40, PDF p. 72.'),
 ('The town votes', 'srcpage', 'sources/ballot_1946_p142.jpg',
  'The ballot paper for district 2, the Ḥaddāda: five nominees for four seats, Monday 15 April 1946.',
  'Israel State Archives, P-213/40, PDF p. 142.'),
 ('The people our town produced', 'srcpage', 'sources/mirat_al_sharq_1919.jpg',
  'The first issue of <i>Mirʾāt al-Sharq</i>, “Mirror of the East”, Jerusalem, Wednesday 17 September 1919. '
  'The masthead, top right, names its licence-holder and editor, <span class="ar" dir="rtl">بولس شحادة</span>, Boulos Shehadeh of Ramallah, and calls it “a free Arabic political newspaper, appearing once a week for the present”. '
  'His opening article begins: “Today we publish among our people a newspaper called <i>Mirʾāt al-Sharq</i>, and we issue it from the city of Jerusalem.”',
  '<i>Mirʾāt al-Sharq</i>, no. 1, 17 September 1919, p. 1. Public domain.'),
]

def _srcfig(kind, fn, cap, src):
    alt = re.sub(r'<[^>]+>', '', cap)
    cls = {'srcpage': 'photo srcpage', 'period': 'photo period'}.get(kind, 'photo')
    return (f'<figure class="{cls}"><img src="../img/{fn}" alt="{alt}" loading="lazy" decoding="async">'
            f'<figcaption>{cap}<span class="src">{src}</span></figcaption></figure>')

for key, kind, fn, cap, src in SOURCE_PAGES:
    hits = [i for i, e in enumerate(E) if e[0] == 'e' and e[5].startswith(key)]
    assert len(hits) == 1, (key, hits)
    i = hits[0]
    E[i] = E[i][:7] + (E[i][7] + _srcfig(kind, fn, cap, src),) + E[i][8:]

# ---------------------------------------------------------------------------
# v65: one timeline (David, 8 Nov 2026). Twelve eras in date order, and each
# era tells its story first and then shows the evidence for it. The separate
# "How we know" part is gone: its entries sit in the era they prove. Entries
# are moved, not reworded: each is matched by the start of its title.
# The build checks itself: every story entry must overlap its era's dates
# and run in date order, and every picture must show something from its era.
# ---------------------------------------------------------------------------
_OLD_CHAPTERS = CHAPTERS
CHAPTERS = [
 (1,'CHAPTER ONE','The land and its first peoples &middot; to 1200 BC',
  'How the world began, as scripture tells it, and what the ground of these hills shows: the first people, the first villages and the terraces still farmed today.'),
 (2,'CHAPTER TWO','Kingdoms on the ridge &middot; 1200–539 BC',
  'The highlands fill with villages, neighbours rise across the Jordan, and Assyria writes the land down. Far to the south, the great dam of Maʾrib is built.'),
 (3,'CHAPTER THREE','Persians, Greeks and Romans &middot; 539 BC – AD 324',
  'Six sovereigns rule the ridge in turn. The villages stay, and Rome builds the road that runs past the future town.'),
 (4,'CHAPTER FOUR','Ghassān and a Christian countryside &middot; AD 250–638',
  'The tribe our family remembers comes north, and the hills become Christian.'),
 (5,'CHAPTER FIVE','Early Islamic Palestine &middot; 638–1099',
  'The conquest changes the rulers, not the people. The Christian villages of this ridge stay Christian, and Ghassān is still found across the Jordan.'),
 (6,'CHAPTER SIX','Crusaders and Mamluks, and the name appears &middot; 1099–1517',
  'Rulers change around villages that stay put, and in 1186 the name Rām Allāh is written down for the first time.'),
 (7,'CHAPTER SEVEN','From Karak to Ramallah &middot; about 1500–1562',
  'Rāshid al-Ḥaddādīn and his family, the road from Karak by way of Bayt Jālā, and the agreement of 1561 that settled them on this hill.'),
 (8,'CHAPTER EIGHT','The founding families &middot; 1562–1834',
  'The five sons become the clans, the parish proves itself in writing, newcomers arrive, and the town lives through its feuds.'),
 (9,'CHAPTER NINE','Churches, schools and village life &middot; 1834–1900',
  'The peasants’ revolt of 1834, then a new church, new schools, the first doctors, and how the town lived, worked and kept its feasts.'),
 (10,'CHAPTER TEN','Emigration and the Mandate &middot; 1901–1947',
  'The first families sail for America, Ramallah becomes a town with a council, and war, typhus, revolt and elections follow.'),
 (11,'CHAPTER ELEVEN','1948 and after &middot; 1948–1967',
  'The refugees of Lydda and Ramle arrive and the town takes them in. The diaspora builds a hospital, writes our first history and founds the Federation.'),
 (12,'CHAPTER TWELVE','The city today &middot; 1967 to now',
  'The town is counted under occupation, Shāhīn closes the record, and our people build a city from both sides of an ocean.'),
 (13,'CLOSING','What is proven',
  'Three claims, weighed on all the evidence in the chapters before, and the key dates on one page.'),
]
PARTS = {}
# chapter: (story titles in date order, evidence titles)
_ORDER = {
 1: (['Adam and Eve', 'The three Bibles', 'Joktan', 'What this land is made of', 'The Natufians', 'Jericho',
      'The first villages', 'The Canaanite population', 'The terraces and their'],
     ['The Amarna letters']),
 2: (['The highlands fill up', 'The neighbours', 'The great dam'],
     ['The Bible as a map', 'Assyria writes']),
 3: (['Six sovereigns', 'The Samaritans', 'The roads Jesus used', 'Life on the ridge in AD 30', 'Rome returns'],
     ['Rome writes', '“A city called Ephraim']),
 4: (['The hills become Christian', 'The dam breaks', 'Amorkesos', 'Al-Ḥārith ibn Jabala', 'The scattering', 'Yarmūk'],
     ['Ghassān named in stone', 'A traveller lists', 'The name in the water', 'The dam cannot', 'Were the Ghassanids',
      'The silence starts later', 'What they left']),
 5: (['The towns do not die', 'Marj Rāhiṭ', 'al-Yaʿqūbī', 'A village church'],
     ['Thirty-one generations', 'The generation length']),
 6: (['Magna Mahumeria', 'The name appears in 1186', 'The ridge and the plateau', 'One Christian, one debt'],
     ['Ghassān is still there', 'The word underneath', 'The man who should', 'The tradition’s own word',
      'What the other archive', 'Five searches', 'The gap is not']),
 7: (['Rāshid al-Ḥaddādīn', 'What the family remembers', 'The people of Ramallah speak', 'The Christian settlement'],
     ['The registers begin', 'The registers do give names', 'Karak was a Christian town', 'Musil asked',
      'Who was Rāshid’s father', 'The Karak chart', 'When the Ḥaddādīn name', 'Two false leads']),
 8: (['The five sons', 'New families arrive', 'Feuds, a pasha'],
     ['The parish proves itself']),
 9: (['The peasants’ revolt', 'The present Greek Orthodox church', 'The town gains', 'How the town lived', 'The festivals',
      'A teacher and a doctor', 'The first doctors', 'What a day was worth'],
     ['The twin town']),
 10: (['The first four sail', 'Ramallah becomes a city', 'The last big fight', 'The war, the locusts',
       'The revolt reaches', 'The town votes', 'The people our town produced'],
      ['Elihu Grant writes', 'The Patriarchate counts', 'The counting years']),
 11: (['The catastrophe', 'Where the refugees lived', 'The diaspora builds', 'The Federation'],
      ['Our first history']),
 12: (['The city, counted'],
      ['Shāhīn closes']),
 13: (['Our origins', 'Our contribution', 'The founding of Ramallah'], []),
}
EVIDENCE_SUB = 'The sources for this chapter, and how we read them'
def _restructure():
    ents = [e for e in E if e[0] == 'e']
    title = lambda e: re.sub(r'<[^>]+>', '', e[5])
    used, new = set(), []
    for ch, (story, evid) in _ORDER.items():
        for label, keys in (('The story', story), ('The evidence', evid)):
            if not keys:
                continue
            if ch != 13:
                new.append(('s', ch, label, EVIDENCE_SUB if label == 'The evidence' else ''))
            for k in keys:
                hits = [i for i, e in enumerate(ents) if title(e).startswith(k) and i not in used]
                assert len(hits) == 1, (ch, k, len(hits))
                used.add(hits[0]); e = ents[hits[0]]
                new.append(('e', ch) + tuple(e[2:]))
    missing = [title(e) for i, e in enumerate(ents) if i not in used]
    assert not missing, missing
    E[:] = new
_restructure()

# --- the era check -----------------------------------------------------------
ERA_YEARS = {1: (-99999, -1200), 2: (-1200, -539), 3: (-539, 324), 4: (250, 638), 5: (638, 1099),
             6: (1099, 1517), 7: (1500, 1562), 8: (1562, 1834), 9: (1834, 1900), 10: (1901, 1947),
             11: (1948, 1967), 12: (1967, 2100)}
_MONTHS = 'January|February|March|April|May|June|July|August|September|October|November|December'
def date_years(d):
    """The years a date string covers, as signed integers (BC negative); [] when undated."""
    d = re.sub(r'<[^>]+>', '', d)
    d = re.sub(r'(\d),(\d{3})', r'\1\2', d)
    d = re.sub(r'\b\d{1,2} (%s)' % _MONTHS, '', d)
    d = re.sub(r'(\d{3,4})/\d{1,2}\b', r'\1', d)
    parts = re.split(r'→|·| against ', d)
    out, bc = [], [('BC' in p) for p in parts]
    for i, p in enumerate(parts):
        isbc = bc[i] or (not re.search(r'\bCE\b|AD', p) and any(bc[i+1:]) and 'BC' in parts[-1])
        cent = re.findall(r'(\d{1,2})(?:st|nd|rd|th)', p)
        if cent and ('c.' in p or 'century' in p):
            nums = []
            for x in cent:
                n = int(x)
                nums += [n * 100, (n - 1) * 100] if isbc else [(n - 1) * 100, n * 100 - 1]
        elif re.search(r'\d{4}s\b', p):
            nums = []
            for x in re.findall(r'(\d{4})s\b', p):
                n = int(x)
                nums += [n, n + (99 if n % 100 == 0 else 9)]
        else:
            nums = [int(x) for x in re.findall(r'\d+', p)]
            if '–' in p and len(nums) == 2 and not isbc and nums[1] < 100 and nums[0] > 100:
                nums[1] = nums[0] // 100 * 100 + nums[1]
        out += [-n if isbc else n for n in nums]
    return out

# An entry that spans more than fifty years is a survey, not an event, and is
# not held to date order. These few are placed by hand, with the reason.
DATE_ORDER_EXCEPTIONS = {
 'The diaspora builds a hospital',  # fund-raising began in 1944; the hospital belongs to the years after 1948
}
ERA_EXCEPTIONS = {
 'What the family remembers',  # dated 1953, when the account was written down; it tells of the founding
}
def _check_eras():
    title = lambda e: re.sub(r'<[^>]+>', '', e[5])
    cur, label, last = None, None, None
    for e in E:
        if e[0] == 's':
            label, last = e[2], None
            continue
        ch = e[1]
        if ch != cur:
            cur, last = ch, None
        if ch not in ERA_YEARS or label != 'The story':
            continue
        ys = date_years(e[2])
        if not ys:
            continue
        if title(e).startswith(tuple(ERA_EXCEPTIONS)):
            continue
        lo, hi = ERA_YEARS[ch]
        assert min(ys) <= hi and max(ys) >= lo, ('story entry outside its era', ch, title(e), e[2], ys)
        if title(e).startswith(tuple(DATE_ORDER_EXCEPTIONS)) or max(ys) - min(ys) > 50:
            continue
        if last is not None:
            assert min(ys) >= last, ('story entries out of date order', ch, title(e), e[2])
        last = min(ys)
_check_eras()

LINKAT = {n: LINKAT[o] for n, o in ((1, 1), (2, 4), (3, 5), (4, 7), (5, 8), (6, 9), (7, 11), (8, 12), (10, 13))}
def _regroup(d, plan):
    assert set(d) <= set(plan), set(d) - set(plan)
    out = {}
    for old, targets in plan.items():
        items = d.get(old, [])
        if isinstance(targets, int):
            targets = [targets] * len(items)
        assert len(targets) == len(items), (old, len(items))
        for it, n in zip(items, targets):
            out.setdefault(n, []).append(it)
    return out
PHOTOS = _regroup(PHOTOS, {1: 10, 2: 1, 3: 1, 4: 2, 5: 3, 6: 3, 7: 4, 8: 5, 9: 7, 10: 7, 11: 7, 12: 10, 13: 10})
LOCAL_PHOTOS = _regroup(LOCAL_PHOTOS, {12: 7, 13: 10})
SHAHEEN = _regroup(SHAHEEN, {9: 6, 11: 7, 12: [7, 8, 9, 9, 9, 9], 13: [10, 10, 10, 10, 10, 11, 11, 11, 12]})

# Every picture: the year of what it shows, and, when it was made long after
# that, a short label saying so. The build refuses a picture outside its era.
PIC_DATES = {
 'ppmsca/13100/13196v.jpg': (1905, None),
 'matpc/04100/04114v.jpg': (-2000, 'Photographed 1934–39'),
 'matpc/05500/05506v.jpg': (-3000, 'Photographed 1926'),
 'matpc/22900/22915v.jpg': (-900, 'A modern photograph'),
 'matpc/01700/01719v.jpg': (-180, 'Photographed about 1900–1920'),
 'matpc/22100/22165v.jpg': (100, 'Photographed 1931'),
 'matpc/05300/05329v.jpg': (560, 'Photographed about 1900–1920'),
 'matpc/03700/03718v.jpg': (740, 'Photographed 1934–39'),
 'matpc/06900/06951v.jpg': (1500, 'Photographed 1898–1914'),
 'matpc/17000/17063v.jpg': (1500, 'Photographed 1937'),
 'matpc/22100/22174v.jpg': (1550, 'Photographed 1931'),
 'matpc/01000/01047v.jpg': (1910, None),
 'matpc/00600/00662v.jpg': (1905, None),
 'matpc/17700/17778v.jpg': (1938, None),
 'matpc/03300/03332v.jpg': (1936, None),
 'memorial_bronze.jpg': (1561, 'A modern memorial'),
 'period/spinning_1919.jpg': (1919, None),
 'p030_1.jpg': (1186, None), 'p024_1.jpg': (1553, None), 'p012_1.jpg': (1550, 'A modern map'),
 'p038_1.jpg': (1639, None), 'p231_1.jpg': (1875, None), 'p371_1.jpg': (1896, None),
 'p238_1.jpg': (1895, None), 'p202_1.jpg': (1900, None), 'p244_1.jpg': (1905, None),
 'p172_1.jpg': (1910, None), 'p245_2.jpg': (1912, None), 'p250_1.jpg': (1916, None),
 'p206_1.jpg': (1930, None), 'p185_1.jpg': (1949, None), 'p228_1.jpg': (1953, None),
 'p161_3.jpg': (1965, None), 'p162_2.jpg': (1968, None),
}
def _check_pictures():
    for n, groups in ((n, (PHOTOS.get(n, []), LOCAL_PHOTOS.get(n, []), SHAHEEN.get(n, []))) for n in ERA_YEARS):
        for g in groups:
            for it in g:
                shows, _lab = PIC_DATES[it[0]]
                lo, hi = ERA_YEARS[n]
                assert lo <= shows <= hi, ('picture outside its era', n, it[0], shows)
    every = [it[0] for d in (PHOTOS, LOCAL_PHOTOS, SHAHEEN) for g in d.values() for it in g]
    assert set(every) == set(PIC_DATES), set(every) ^ set(PIC_DATES)
_check_pictures()
def _made(key):
    lab = PIC_DATES.get(key, (0, None))[1]
    return f'<span class="made">{lab}.</span> ' if lab else ''


assert not ADD70, list(ADD70)
assert not ADD72, list(ADD72)

def render():
    out = []
    for num, kicker, title_c, sub_c in CHAPTERS:
        grp = [e for e in E if e[1] == num]
        if not grp:
            continue
        band = (f'<div class="eraband"><div class="ek">{kicker}</div>'
                f'<h2>{title_c}</h2><div class="es">{sub_c}</div></div>')
        if num in PARTS:
            pk, pt = PARTS[num]
            out.append(f'<div class="partband" id="part{num}"><div class="pk">{pk}</div><h2>{pt}</h2></div>')
        out.append(f'<div class="erahead" id="ch{num}">{band}{linkat(num)}</div>')
        out.append(photos_for(num))
        open_q = []
        for e in grp:
            if e[0] == 's':
                _, _c, lab, sub = e
                sb = f'<span class="ss">{sub}</span>' if sub else ''
                out.append(f'<div class="sect"><span class="sl">{lab}</span>{sb}</div>')
                continue
            _, _ch, date, grade, w2, title, note, bodyc = e
            # "What we still don't know" paragraphs are gathered at the end of the chapter
            open_q += WWSDK_RE.findall(bodyc)
            bodyc = WWSDK_RE.sub('', bodyc).strip()
            gf, gc, gl = GRADE[grade]
            if w2 == 'shared':
                w2h = '<span class="w2 sh">ONE TRADITION</span>'
            elif w2:
                w2h = '<span class="w2">TWO WITNESSES</span>'
            else:
                w2h = ''
            major = ' major' if bodyc else ''
            more = f'<div class="more">{bodyc}</div>' if bodyc else ''
            out.append(
                f'<div class="entry{major}"><div class="ewhen"><span class="d">{date}</span>'
                f'<span class="g" style="background:{gf};color:{gc}">{gl}</span>{w2h}</div>'
                f'<div class="ebody"><h3>{title}</h3><div class="note">{note}</div>{more}</div></div>')
        if SCHOLARS.get(str(num)):
            out.append('<div class="scholars"><h4>What the scholars say</h4><ul>'
                       + ''.join(f'<li><span class="sw">{w["who"]}</span>'
                                 f'<span class="sp">{w["pub"]}</span>'
                                 f'<span class="sl2">{w["line"]}</span></li>' for w in SCHOLARS[str(num)])
                       + '</ul><p class="sfoot">Full details in <a href="#appA">the bibliography</a>.</p></div>')
        open_q += WWSDK_EXTRA.get(num, [])
        if open_q:
            out.append('<div class="wwsdk"><h4>What we still don’t know</h4>'
                       + ''.join(f'<p>{q}</p>' for q in open_q) + '</div>')
    return ''.join(out)
import json as _json
# v66: each chapter's reading list, chosen from the annotated bibliography
_SCH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'scholars.json')
SCHOLARS = _json.load(open(_SCH, encoding='utf-8')) if os.path.exists(_SCH) else {}
# v68: the three chapters whose entries carried no "What we still don't know" paragraph
WWSDK_EXTRA = {
 2: ['We don’t know the source of the southern-European-related ancestry the Philistines brought. '
     'No excavation has found an Iron Age village under Ramallah’s old town. The nearest, Khirbet Raddana, '
     'on the edge of Ramallah and al-Bīra, has since been built over, so we may never know more about who '
     'lived on our ridge in these centuries. If you know of a record or a dig that speaks to either, we would like to hear from you.'],
 4: ['We don’t know where the water called Ghassān really was: the old scholars give four places for it, '
     'and they cannot all be right. We don’t know what became of al-Ḥārith’s family after the Greek writers '
     'stop naming them in 593–594. The last dated repair of the dam at Maʾrib is from 557/558, and nothing '
     'fixes when it finally failed. Much of the Ghassanid century on the Jordanian steppe was passed over, '
     'and nobody dug it. If you know of an inscription, a manuscript or a site from these centuries, we would '
     'like to hear from you.'],
 8: ['We cannot yet name the first families of each clan in the parish records before 1700, and we know '
     'little of the town between the boundary case of 1565 and the early 1800s. The written accounts of 1820 '
     'do not agree on whose feud it was: Shahin (1982) says the Shakara, Shaheen (1992, 2005) the Sharaka. '
     'If your family kept papers from these years, they may hold the answer.'],
}
WWSDK_RE = re.compile(r'<p><b>What we still don’t know\.</b>\s*(.*?)</p>', re.S)

CONTENTS = ('<a class="tocbtn" href="#toc" aria-label="Jump to the list of chapters">Chapters</a>'
            '<div class="contents" id="toc"><h4>Contents</h4><ol>' + ''.join(
    f'<li><a href="#ch{n}"><span class="cnum">{k.replace("ERA ","").strip().title()}</span>'
    f'<span class="ctit">{t.split("&middot;")[0].strip()}'
    + (f'<span class="cgen">{t.split("&middot;")[1].strip()}</span>' if "&middot;" in t else '')
    + '</span></a></li>'
    for n, k, t, _sub in CHAPTERS) +
    '</ol><p class="cend"><a href="#appA">Appendix &middot; The Annotated Bibliography</a> &nbsp;&middot;&nbsp; '
    '<a href="#appC">John Mogannam&rsquo;s Chart</a> &nbsp;&middot;&nbsp; '
    '<a href="#appB">The Test Harness &mdash; thirty-six claims</a></p></div>')

CHAINFIG = fig(F3.fig_chain_new(),
 'The chain, link by link — built from the sources',
 'Our own family line, in nine links, <b>each one defined by the source that carries it rather than by '
 'any family document</b>. Every era of this book opens with a strip saying which of these links we '
 'have reached and what evidence there is for it in that era — and for four of the nine eras the '
 'honest answer is none. Each link also carries, printed here for the first time, <b>what would break '
 'it</b>: the evidence that would falsify that link if anyone found it. <i>Read the grade column '
 'downward and the shape of the whole argument is visible before a word of it is read — scripture, '
 'then classical scholarship, then a contemporary Greek historian, then a hole, then four hundred and '
 'sixty-four years of paper.</i>',
 'Genesis 5, 10 and 11; al-Ṭabarī; Ibn al-Kalbī, Ibn Ḥazm and Ibn Durayd; Ḥamza al-Iṣfahānī and '
 'al-Masʿūdī; Procopius, the Nitl mosaics and CIH 541; the Ottoman defters of 1525–1596; the parish '
 'books and the censuses. John Mogannam’s chart is printed separately, in the appendix.')

FRONT = """<div class="front">
<figure class="frontis"><img src="../img/memorial_drawing.jpg" alt="Drawing of the memorial to the first family of Ramallah: Rāshid, his wife holding their daughter, and their five sons" decoding="async"><figcaption>From the memorial to the first family of Ramallah</figcaption></figure>
<h3>Dedication</h3>
<p class="ded">To the people of Ramallah: to those who stayed on the hill, to those who carried it
with them to every city they went to, and to those, in every generation, who kept the names.</p>
<h3>Preface</h3>
<p>This is a history of a Palestinian Christian town told by its own people. Ramallah’s families have
always known where they came from. They have told it at weddings and funerals, written it in notebooks,
and carried it to San Francisco, Detroit and Jacksonville. What they have not had is the story set
out, date by date, beside the records that can be checked.</p>
<p>That is what we have tried to do. Our history is one timeline in twelve chapters. Each chapter tells
the story of its years first, then shows how we know it. Throughout, we follow two threads at once. One is the family’s own account,
reaching back through Rāshid al-Ḥaddādīn to Karak and to Ghassān. The other is what the land and the
documents say: the archaeology of these hills, the Crusader charter, the Mamluk endowment, the Ottoman
registers, the Jerusalem court, and the Mandate and Jordanian censuses. Where the two agree, we say so.
Where they disagree, we print both. Where we had something wrong, we have corrected it in the open, in
a box that shows what stood before.</p>
<p>Every entry carries a label that says what kind of evidence stands behind it, from scripture and
the classical writers to documents and oral tradition. Oral tradition is evidence, and we treat it as
such. It is the town’s memory of itself. We have printed it in its own words and marked it as memory,
so that no reader mistakes it for a register and no register is allowed to silence it.</p>
<p>We have not finished. Names wait unread in the Ankara registers, and pages wait in archives we
have not yet reached. Readers who hold a document, a photograph or a story that belongs here are asked
to send it, so that our next version is more complete than this one.</p>
<h3>Acknowledgements</h3>
<p>We stand on the work of those who wrote Ramallah’s history before us. We are indebted to
<b>ʿAzīz Shāhīn</b>, whose book of the family trees (1982) is the foundation of everything here, and to
<b>Naseeb Shaheen</b>, whose pictorial histories preserved the town’s photographs and its two founding
accounts. We are indebted to <b>ʿAdnān al-Ḥaddādīn</b>, who wrote down the Ḥaddādīn account in 1953;
to <b>Joseph Kaddoura</b>, who wrote the town’s history in New York in 1954; to <b>Khalīl Abū Rayya</b>
and <b>ʿAbdallah Mogannam</b>, who crossed the Jordan in 1953 to ask; and to <b>Khalil Totah</b>, whose
diary kept the revolt of 1938 in the town’s own words.</p>
<p>We thank <b>Sāmiḥ Ḥammūdeh</b>, whose work in the Ottoman registers and the Jerusalem court records
put the families’ names back on paper; the Palestinian scholars and archaeologists of <b>Birzeit
University</b>, <b>al-Quds University</b> and the <b>Institute for Palestine Studies</b>; the
<b>Municipality of Ramallah</b>; and the Ḥaddādīn of Karak, who have kept their side of the story and
received Ramallah’s delegation as kin.</p>
<p>We compiled this history for the <b>American Federation of Ramallah, Palestine</b>. Its errors are
ours, and we will correct them in the open.</p>
<p style="color:#77726A;font-size:.86rem">David Saah, PhD &middot; John Mogannam</p>
</div>"""

HOWTO = f"""
<div class="howto"><h4>How to read this book</h4>
<p><b>Our history is one timeline.</b> Twelve chapters run from the first people on these hills to
today, in date order. <b>Every chapter has two halves, always in the same order.</b> <b>The story</b>
tells what happened in those years, with the photographs, maps and charts that go with it.
<b>The evidence</b> then sets out the sources for the same years and how we read them: the
registers, the inscriptions, the family charts and the harder questions. Each chapter ends with
<b>what we still don’t know</b>. Read the story halves for the history. Read on into the evidence
when you want to see how we reached it.</p>
<p><b>Every photograph sits in the chapter of what it shows.</b> When a picture was taken long after
the time it shows, as with a photograph of a Roman road taken from the air in 1931, its caption opens
by saying so.</p>
<p><b>Two texts guide us:</b> ʿAzīz Shāhīn’s history of 1982, which is a source, and John Aziz
Mogannam’s chart of thirty-six generations, which is our family’s own guide. Where both carry an entry
<i>and testify independently</i>, it carries the label <span class="w2">TWO WITNESSES</span>. From 1500 onward they do testify independently, because
Shāhīn writes the town’s own history from local memory and local records, while the chart is a
genealogy. <b>Before 1500 they do not.</b> There the chart follows the classical Arabic
<i>ansāb</i> tradition, the Arabic books of descent, which is also where Shāhīn’s deep lineage comes from. So those entries
carry the label <span class="w2 sh">ONE TRADITION</span> instead: both texts carry the claim, but they are drinking
from the same well. <i>We draw this line because the family history presented in 2026 (described in the
appendix) turned out to repeat a modern reconstruction, not an independent source.</i>
Every entry also carries a label, shown as a small badge, saying what kind of thing holds it up:
<span class="g" style="background:#D5E9DF;color:#1A1A1A">SCRIPTURE</span>
<span class="g" style="background:#A9CDB8;color:#1A1A1A">CLASSICAL</span>
<span class="g" style="background:#79B491;color:#1A1A1A">ATTESTED</span>
<span class="g" style="background:#007A3D;color:#fff">DOCUMENTS</span>
<span class="g" style="background:#F6EEDF;color:#7A5A28">ORAL TRADITION</span>
<span class="g" style="background:#FDF6EC;color:#8A5A1E">NO EVIDENCE</span>.
A document outranks a memory, and the memory is kept anyway; an inference is drawn as an inference;
a conflict is printed as a conflict; and where the record corrects the family, the correction
appears in a marked box at the date where it happens.</p>
<p><b>The chapters follow the land from its first peoples to the city it holds today.</b> <i>The land is the
thread that holds the story together, and our families are part of what happened on it.</i></p>
<p><b>Our own family line runs through the story as a chain of nine links.</b> Every chapter
opens with a strip showing where that chain stands: which link we have reached, and what evidence
there is for it at that point. Often there is <i>none</i>, and the strip says so. Figure 1 sets out all nine
links at once, each with the source that carries it and, printed here for the first time,
<b>what would prove it wrong</b>.</p>
<p><b>One change of method matters more than any of the others.</b> John Mogannam’s chart of
thirty-six generations, which our earlier versions were built on, <i>is no longer treated as
a source</i>. <b>Its compiler is one of the two of us writing this history</b>, which makes the point sharper
rather than softer. A chart cannot be its own evidence, least of all when the people printing it are
the people who drew it. So it is set out whole in the appendix as the family’s own guide, and a very
good one, with the points at which the texts correct it marked. Everything in the chain here is
built from Genesis, the Arabic genealogists, Procopius and the registers directly. <i>Every
correction we make to that chart is a correction we make to ourselves.</i></p>
<p><b>And the chart’s count is corrected here for the first time.</b> Its generation 35 draws
nine hundred and thirty-one years as a single line. That stretch is about <b>thirty-one</b>
generations, so the line from Adam to Rāshid is <b>sixty-six generations, not thirty-six</b> —
thirty-six of them named, thirty with no name at all. <i>The ladder in the strip that opens each chapter is drawn on that count.</i></p>
<p><b>How the generations are numbered — two numbers, and they are not the same.</b>
<b>The chart’s number</b> counts its own thirty-six rows, one of which is a nine-hundred-year void
drawn as a single line. <b>Our number</b> counts generations: <b>sixty-six</b> from Adam and
Eve to Rāshid, and about eighteen more to this morning, <b>eighty-four in all</b>. So <i>“the
Mogannam chart, generation 36”</i> means Rāshid’s row on the chart, and <i>“generation 66”</i> means
Rāshid. Generations 1 to 34 carry the same number in both.</p>
<p><b>We close with what the evidence shows</b> about three things: where we come from, how we
became part of the Palestinian people, and when and how Ramallah was founded, with the key dates on one
page. <b>After the bibliography comes an appendix that checks the family history presented in
2026</b>: all thirty-six of its claims that can be checked, each with what we found, so that anyone can check them again.</p>
</div>
{CONTENTS}
{CHAINFIG}
"""

CHART_SECTION = (
 '<h2 id="appC" class="eraband" style="display:block"><div class="ek">Appendix</div>'
 'John Mogannam’s Chart — the Family’s Own Guide'
 '<div class="es">The document this project worked from for years, printed in full — and measured, '
 'for the first time, against the texts it comes from. Its compiler is a co-author of this book: '
 'what follows is a self-audit, not a verdict on somebody else’s work.</div></h2>'
 '<div class="testsec">'
 '<div class="howto" style="border-left-color:#004A26;margin:0 0 26px">'
 '<h4 style="color:#004A26">Why this is an appendix and not a source</h4>'
 '<p><b>Earlier editions of this book were built on this chart.</b> That was the wrong way round, and '
 'this edition reverses it. A family genealogy compiled in the present from published tables is a '
 '<i>guide</i> to a line — an excellent one, and the reason this project knew where to look — but it '
 'is not evidence for the line. The evidence is Genesis, the Arabic genealogists, Procopius, the '
 'Ottoman defters and the parish books, and the chain in Figure 1 is built from those directly.</p>'
 '<p><b>The one number in it that this edition changes is the count.</b> Generation 35 draws nine '
 'hundred and thirty-one years as a single row and labels it “45 generations.” Forty-five implies a '
 'male-line generation of about twenty-one years, which no observed population sustains; the stretch is '
 '<b>about thirty-one</b>. Counted that way the chart’s thirty-six rows are <b>sixty-six '
 'generations</b> — thirty-six of them named, thirty with no name at all. <i>The rows are not wrong. '
 'One of them is thirty-one rows deep.</i></p>'
 '<p><b>What the chart still deserves credit for is the thing most family genealogies refuse to do.</b> '
 'At generation 35 it prints a void — a blank standing for nine hundred years — in the same typeface '
 'as every other line. <i>It could have invented names there, as others demonstrably have, and it did '
 'not.</i> That single choice is why it can be tested at all, and why it is printed here in full '
 'rather than quietly dropped.</p></div>'
 + fig(R.fig_gens(), 'John Mogannam’s chart of thirty-six named generations',
   'Adam and Eve to Rāshid, in Arabic and English, coloured here by what holds each stretch of the line. '
   'The hatched band at generation 35 is the family’s own printed void.',
   'Researched and compiled by John Aziz Mogannam; the deep lineage after al-Suwaydī and Wüstenfeld, both in the family library.')
 + NUMTABLE('WHERE THE CHART AND THE SOURCES DIVERGE',
   ['What the chart says', 'What the sources say', 'What this book does'],
   [['<b>Thirteen</b> generations from Adam to ʿĀbir',
     'Genesis gives <b>fourteen</b> in the Masoretic text and <b>fifteen</b> in the Septuagint, which inserts Kainan; Luke 3:36 follows the Septuagint',
     'Follows Genesis, and prints the difference. It changes nothing in the argument.'],
    ['Generation 35 stands for <b>“45 generations”</b>',
     'The span is 931 years, from al-Ḥārith’s death in 569 to Rāshid about 1500. At <b>an assumed</b> male-line interval of 25–35 years that is <b>27 to 37 generations</b>, most probably about 31 — which makes the whole line 66 generations, not 36. Forty-five would require a generation of 21 years, shorter than any observed population sustains',
     'Prints about 31, in a range, shows the arithmetic, and recounts the line at 66 generations. Corrected by division, not by a source.'],
    ['<b>Two links</b> are drawn across the void',
     'No source of any kind names a father inside it',
     'Draws the void as a void, and measures it. This is the family’s own honesty and the book keeps it.'],
    ['The chart is one of <b>two key texts</b>',
     'The chart reproduces a modern reconstruction; where its deep lineage and Shāhīn’s agree, they are drinking from the same well',
     'Restricts the TWO WITNESSES badge to entries after 1500. Before that, ONE TRADITION.']],
   'Four divergences, none of them fatal, and all of them printed. A guide that survives being measured is a better guide afterwards.')
 + '<p class="closing" style="margin-top:26px"><b>The chart is not the evidence for this family’s line. '
   'It is the map somebody drew of it, from the best published tables available, and it is close enough '
   'to the sources that the differences fit in one small table.</b> <i>That is a real achievement, and '
   'it is why this book could be written at all.</i></p>'
 '</div>')

TEST_SECTION = (
 '<h2 id="appB" class="eraband" style="display:block"><div class="ek">The Test Harness</div>'
 'The Family’s Account, Tested Claim by Claim'
 '<div class="es">Thirty-six checkable claims from the family’s own presentation, each read against '
 'ʿAzīz Shāhīn’s 1982 history and against the external record. This is the audit the rest of the book '
 'rests on, printed in full so that anyone can re-run it.</div></h2>'
 '<div class="testsec">'
 '<div class="howto" style="border-left-color:#004A26;margin:0 0 26px">'
 '<h4 style="color:#004A26">How the test was run</h4>'
 '<p>Every datable statement in the family presentation was extracted, then checked in three places: '
 '<b>Shāhīn’s Arabic text</b> (OCR’d in full and read complete in English), <b>the external documentary '
 'record</b> (the Ottoman registers, the census reports, the classical and medieval sources), and '
 '<b>the modern scholarship</b>. Each claim then received one of six verdicts. <b>A claim is only '
 'marked <i>corrected</i> where a document contradicts it, and only marked <i>in conflict</i> where two '
 'sources of comparable weight disagree and neither can be retired.</b> Nothing was quietly dropped: '
 'the three corrections and the one conflict are all printed at their own dates earlier in this book.</p>'
 '<p><b>The result: 13 confirmed · 15 new · 3 refined · 3 corrected · 1 in conflict · 1 untestable.</b> '
 '<i>Three corrections and one open conflict out of thirty-six is a better survival rate than most '
 'published local histories would manage — and the family should say so plainly.</i></p></div>'
 + fig(VERDICT_CHART, 'The family’s account of itself, tested',
   'The thirty-six claims by verdict. The long gold bar is the important one: in fifteen cases the family’s own 1982 history supplies something the presentation did not have, which means the test did not merely audit the account — it enlarged it.',
   'The timeline test, this project, August 2026; run against Shāhīn (1982) and the external record.')
 + testtable()
 + '<p class="closing" style="margin-top:26px"><b>This table is the reason the rest of the book can be '
   'trusted.</b> A history that publishes its own audit — including the places where it was wrong — is '
   'making a different kind of claim from one that does not.</p>'
 '</div>')

import datetime as _dt
_TODAY = _dt.date.today()
LAST_UPDATED = f'{_TODAY.day} {_TODAY:%B %Y}'
html_parts = ['<div class="pbar"><i></i></div>',
f"""<header class="masthead"><div class="wrap">
<p class="updated">Last updated {LAST_UPDATED}</p>
<div class="mastrow"><span class="l">The Ramallah Family Tree Book</span>
<span class="r">The Roots of Ramallah &middot; fifth edition</span></div>
<hr class="mastrule">
<h1>The Roots of Ramallah</h1>
<p class="sub"><b>A History of Its People</b></p>
<p class="byline">David Saah, PhD &nbsp;&middot;&nbsp; John Mogannam</p>
<p class="sub">The whole history of the Ramallah family as a single unbroken timeline — from Adam
and Eve to today, with the evidence attached at every date.</p>
<p class="credit"><b>Genealogical compilation by John Mogannam</b> &mdash; the line from Adam and Eve
to Rāshid al-Ḥaddādīn, after al-Suwaydī’s <span class="ar">سبائك الذهب</span> and Wüstenfeld’s tables;
the clan descent from Rāshid’s five sons; and the English transliterations of the Ottoman registers of
1553 and 1562.</p>
<p class="meta">Compiled for the American Federation of Ramallah, Palestine &middot; keyed throughout
to ʿAzīz Shāhīn, <span class="ar">كشف النقاب</span> (1982), and to the co-authors’ own chart of
thirty-six named generations</p>
<hr class="rule-gold">
{FRONT}
<hr class="rule-gold">
{HOWTO}
</div></header>
<main><div class="wrap"><div class="chron">""",
render(),
'</div>',
'<h2 id="appA" class="eraband" style="display:block"><div class="ek">Appendix</div>'
'The Annotated Bibliography, Fourth Edition'
'<div class="es">Every source in the family library, and what each one is good for.</div></h2>',
appendix_bibliography(),
CHART_SECTION,
TEST_SECTION,
'<div class="eraband"><div class="ek">Notes</div><h2>References</h2>'
'<div class="es">Every citation, in order; filenames in monospace are the copies shelved in the family’s Drive.</div></div>',
'<div class="notes"><ol>' + ''.join(
    f'<li id="n{i}">{t} <a class="backto" href="#r{i}">&#8617;</a></li>'
    for i, t in enumerate(CITES, 1)) + '</ol></div>',
f"""</div></main>
<footer class="end"><div class="wrap">
<p><b>The Roots of Ramallah: A History of Its People</b> &middot; {FIGN[0]} figures &middot; {len(CITES)} notes &middot; one timeline,
Adam to today &middot; built from the family library of 88 titles, the Ottoman registers, and the
family’s own two key texts.</p>
</div></footer>
<script>(function(){{var b=document.querySelector('.pbar i');function u(){{var h=document.documentElement.scrollHeight-window.innerHeight;if(b)b.style.width=(h>0?(window.pageYOffset/h*100):0)+'%';}}window.addEventListener('scroll',u,{{passive:true}});window.addEventListener('resize',u);u();}})();</script>"""]

# ── put the figure and note numbers back into document order ─────────
# Entries are authored in one order and assembled in another (chapter order),
# so both sequences have to be renumbered against the finished document.
def renumber(body, cites):
    seq = [int(m.group(1)) for m in re.finditer(r'id="r(\d+)"', body)]
    seen, order = set(), []
    for n in seq:
        if n not in seen:
            seen.add(n); order.append(n)
    for n in range(1, len(cites) + 1):          # any note never referenced
        if n not in seen:
            order.append(n)
    remap = {old_n: i for i, old_n in enumerate(order, 1)}
    body = re.sub(r'<sup class="cn"><a href="#n(\d+)" id="r\1">\1</a></sup>',
                  lambda m: '<sup class="cn"><a href="#n%d" id="r%d">%d</a></sup>'
                            % ((remap[int(m.group(1))],) * 3), body)
    fign = [0]
    def bump(m):
        fign[0] += 1
        return '<div class="fignum">Figure %d</div>' % fign[0]
    body = re.sub(r'<div class="fignum">Figure \d+</div>', bump, body)
    return body, [cites[old_n - 1] for old_n in order], fign[0]

_body = ''.join(html_parts[1:-3])   # drop the pre-built notes band and list
_body, CITES_ORDERED, NFIGS = renumber(_body, CITES)
html_parts = [html_parts[0], _body,
  '<div class="eraband"><div class="ek">Notes</div><h2>References</h2>'
  '<div class="es">Every citation, in the order it appears; filenames in monospace are the copies '
  'shelved in the family\u2019s Drive.</div></div>'
  '<div class="notes"><ol>' + ''.join(
     f'<li id="n{i}">{t} <a class="backto" href="#r{i}">&#8617;</a></li>'
     for i, t in enumerate(CITES_ORDERED, 1)) + '</ol></div>',
  html_parts[-1].replace(f'{FIGN[0]} figures', f'{NFIGS} figures')]

html = ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>The Roots of Ramallah: A History of Its People</title>'
        '<style>' + CSS + '</style></head><body>' + ''.join(html_parts) + '</body></html>')

from restyle import restyle
html = restyle(html)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w', encoding='utf-8', newline='\n').write(html)
print('WROTE', OUT, f'{len(html):,} bytes ·', FIGN[0], 'figures ·', len(CITES), 'notes')
