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
  'The land changes hands around an unmoved population — and in 1279 the name <i>Rām Allāh</i> appears in a sultan’s endowment deed, 283 years before the family arrives to live under it.'),
 (10,'INTERLUDE','The Missing Centuries',
  'Four eras have just passed. In every one of them the land is documented and our own line is not. <i>This interlude stops and measures the hole rather than filling it.</i>'),
 (11,'ERA TEN','Ottoman Palestine and the First Traceable Families &middot; 1517–1562',
  'The state starts writing everyone down, village by village and household by household — and for the first time an ancestor of ours is inside a document.'),
 (12,'ERA ELEVEN','Ramallah and Its Founding Families &middot; 1562–1900',
  'Twenty-seven households come up the ridge road from Bayt Jālā, divide the land in fifths, and spend three centuries becoming a town.'),
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

def ent(date, grade, w2, title, note, body=''):
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
           (1967,12134,'c'),(1997,17851,'c'),(2007,27460,'c'),(2017,38998,'c'),(2024,43880,'p')]
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
    s.append(txt(40,H-34,'Two counts disagree: Guérin estimated about 1,100 in 1870, but the census Shāhīn cites for the same year counted 2,000. The chart follows the census.',10,BODY))
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
 'The line this book follows begins where Genesis begins. <b>Adam to ʿĀbir (Eber) is Genesis 5 and 11</b>{}, and nothing else — no document, no inscription, no excavation reaches it, and none is claimed.'.format(c('Genesis 5:3–32 and 11:10–14. Fourteen names from Adam to Eber in the Masoretic text; fifteen in the Septuagint, which inserts Kainan. The family chart counts thirteen. See the branch figure below, and the appendix.')),
 f"""
<p>Before anything else is said, the <i>form</i> of a claim like this should be recognised. Medieval
peoples across three continents wrote their descent to a universal ancestor: the House of Wessex to
Woden and thence to Noah, the Irish kings to Míl, the Georgian kings to a grandson of Noah{c('<i>The Anglo-Saxon Chronicle</i>, s.a. 855, the genealogy of Æthelwulf; the Irish Milesian genealogies; the Georgian royal genealogies from Kartlos.')}.
<b>What such a line asserts is membership in the human story, not a chain of verified fathers</b> —
and reading it as the latter, then finding it wanting, is a category error.</p>
<p><b>A note on method, because it changed for this edition.</b> The family has its own guide to this
line: <b>John Aziz Mogannam’s chart of thirty-six named generations</b> — this book’s co-author’s
own prior work — Adam to Rāshid, in Arabic
and English. <i>This book no longer treats that chart as a source.</i> The line here is built from
the texts and the documents directly — Genesis, the Arabic genealogists, Procopius, the Ottoman
registers — and the chart is printed in the appendix as what it is: <b>the family’s own working
guide, and a very good one, which the sources are allowed to correct</b>{c('John Aziz Mogannam, chart of thirty-six named generations, Adam and Eve to Rāshid, in Arabic and English; the deep lineage compiled after al-Suwaydī, <i>Sabāʾik al-dhahab</i>, and Wüstenfeld’s tables, both in the family library. Printed in full in the appendix to this book, with the points at which it diverges from the sources. <b>Its compiler is a co-author of this book. Every correction to it printed here is therefore a self-correction, made in the open and in our own voice — which is the only kind this book is entitled to make.</b>')}. Where the two differ, the
difference is printed rather than reconciled.</p>
<p><b>The one text that is still a key is ʿAzīz Shāhīn’s history of 1982</b>{c('ʿAzīz Shāhīn, <span class="ar">كشف النقاب عن تاريخ رام الله والأنساب</span> (1982), 894 pp., OCR’d in full for this project; the English edition read complete. '+D('1982_Shahin_Kashf_al-Niqab_OCR_TEXT.txt')+'.')} — a documentary
history of the town, written from local memory and local records, and testable line by line. Where
Shāhīn and the chart independently carry an entry, it wears the badge
<span class="w2">TWO WITNESSES</span>; where they are drinking from the same well, it wears
<span class="w2 sh">ONE TRADITION</span> instead.</p>"""),

ent('—', 'scripture', False, 'The three Bibles disagree about the date of creation',
 'By as much as <b>1,366 years</b>: the span from creation to Abraham is 1,948 years in the Masoretic text, 3,314 in the Septuagint, 2,249 in the Samaritan.',
 f"""
{fig(R.fig_chron(),'A line to Adam implies a date for Adam',
 'The three surviving forms of the Old Testament give systematically different ages for the patriarchs. The choice of text is itself confessional — and the family’s, as a Rūm Orthodox house, is the Septuagint.',
 'Genesis 5 and 11 in the Masoretic, Septuagint and Samaritan recensions.')}
<p>These are scripture, not chronology, and were never meant as chronology{c('The Byzantine <i>anno mundi</i> era, built on the Septuagint chronology, was the reckoning of the Orthodox churches; the Masoretic figures underlie the Western <i>anno mundi</i>.')}. The
first thirteen generations of the chart make no claim a laboratory could test — <i>and assert
something no laboratory could touch: that this family belongs to the whole human story.</i></p>"""),

CH(1)
ent('—', 'scripture', False, 'Joktan’s thirteen sons — and a homeland',
 'Genesis 10:26–29 names thirteen sons of Joktan. <b>Several of them can be put on a map, and they are all in South Arabia — Hazarmaveth is Ḥaḍramawt and Sheba is Sabaʾ beyond serious doubt, with Ophir, Havilah and Uzal also generally placed there</b>{}. <i>Scripture itself places this branch in the exact country every later chapter of the family tradition walks out of.</i>'.format(c('Genesis 10:26–29, and the closing formula at 10:29b, “all these were the descendants of Joktan.” <b>Ḥaṣarmāweṯ = Ḥaḍramawt</b> is the securest identification in the list: the consonantal skeleton ḥ-ḍ-r-m-w-t matches the South Arabian kingdom <i>ḥḍrmt</i> attested in Sabaic inscriptions and in Pliny (<i>NH</i> VI.32, <i>Atramitae</i>) and Ptolemy (<i>Chatramotitai</i>). The Hebrew form invites a folk-etymology “court of death”, which is secondary. <b>Šəḇā = Sabaʾ</b> is secure as a place; note that Genesis gives a Sheba three times over (10:7 via Cush, 10:28 via Joktan, 25:3 via Abraham and Jokshan), and which line the Sabaeans belong to is an old crux. <b>Ophir and Havilah are disputed</b> — Ophir has been placed in south-west Arabia, on the African Red Sea coast and in India, and no location commands agreement. The remaining nine are names that fit South Arabian onomastics and nothing more.')),
 f"""
{fig(F4.fig_branch(),'The branch at ʿĀbir — where this line leaves Abraham’s',
 'Genesis 10:25 gives ʿĀbir (Eber) two sons and says so in a pun: <i>Peleg</i>, “because in his days the earth was divided” — <i>niplegāh</i>, from the same root as the name. Peleg’s line runs on through Reu, Serug, Nahor and Terah to <b>Abraham</b>, and from Abraham through Isaac, Jacob, Levi, Kohath and Amram to <b>Moses</b>. Joktan’s line is ours. <b>The two branches part three generations after the Flood — four in the Septuagint, which inserts Kainan — and six generations before Abraham</b> — so the honest answer to “where do we split from Abraham?” is that we never joined him. We share Noah, Shem and ʿĀbir with that line, and part company at ʿĀbir’s two sons.',
 'Genesis 5; 10:21–29; 11:10–26; Exodus 6:16–20. The Septuagint reading of Genesis 11:12–13 and Luke 3:36 for Kainan.')}
<p><b>Where Moses sits, and how far away he is.</b> Counting inclusively, Moses is the seventh name
from Abraham — Abraham, Isaac, Jacob, Levi, Kohath, Amram, Moses — and he stands on the far branch,
not on ours{c('Genesis 11:26 for Abraham; Exodus 6:16–20 for Levi, Kohath, Amram and Moses; the same line at Numbers 26:57–59 and 1 Chronicles 6:1–3.')}. That short chain is itself a known problem inside the text: three generations cannot
span the four hundred and thirty years the same book assigns to the sojourn in Egypt, and the usual
resolution is that the list is a clan genealogy telescoped into personal names{c('Exodus 12:40–41 gives the sojourn in Egypt as 430 years, which three generations cannot span; Numbers 3:27–28 already counts 8,600 Kohathite males in the wilderness, impossible if Amram were Moses’s biological father. The standard reading is that “Amram” names the Amramite clan (Numbers 3:27) rather than a father — the list is telescoped. Genesis 15:16, “the fourth generation,” reflects the same short schema.')}. <i>It is worth
saying plainly, because it is the same kind of problem this book has at generation 35 — and the
Bible does not solve it either.</i></p>
<p><b>And a divergence worth printing.</b> The family chart counts <b>thirteen</b> names from Adam to
ʿĀbir. Genesis in the Masoretic text gives <b>fourteen</b>; the Septuagint gives <b>fifteen</b>,
inserting <b>Kainan</b> between Arpachshad and Shelah — and Luke follows the Septuagint{c('Masoretic Genesis 5:3–32 and 11:10–14 give fourteen names from Adam to Eber. The Septuagint inserts Kainan at Genesis 11:12–13, and again at LXX Genesis 10:24 and LXX 1 Chronicles 1:18; Jubilees 8:1–5 has him too. Luke 3:36 follows the Septuagint, though the name is absent from Codex Bezae. Fourteen names in the Masoretic text against fifteen in the Septuagint.')}. The
difference is one or two names in a list nobody can check, and it changes nothing about the argument.
<i>It is printed because a chart the family uses as a guide should be measured against the text it
comes from, not the other way round.</i></p>"""),


sect('What the ground says', 'The other account of how this started — and it begins in this governorate')

ent('c. 13,000 – 9,600 BC', 'attested', False, 'The Natufians — and the cave the whole culture is named after',
 'Scripture’s account of the beginning has just been given. <b>Here is the ground’s.</b> The first people in this land to build regularly in stone and hold a camp through the year are called <b>Natufians</b> — and they are called that because the culture was first identified, in 1928, in a cave on the north bank of <b>Wādī an-Naṭūf, in the Ramallah and al-Bīra governorate, some eighteen kilometres west-north-west of Ramallah</b>{}. <i>The oldest named thing in this entire book is local.</i>'.format(c('Shuqba Cave, north bank of Wādī an-Naṭūf, Ramallah and al-Bīra Governorate; 31.9819° N, 35.0436° E — some 17.7 km west-north-west of Ramallah. The figure of 28 km often attached to the cave is its distance from Jerusalem, not from Ramallah.')),
 f"""
{fig(ATLAS.fig_oldest(),'The oldest ground within a morning’s walk of Ramallah',
 'Every dot is a site with a published excavation and a calibrated date, and every distance is measured from the centre of Ramallah. The nearest of them, Tell en-Naṣba, is under two kilometres away. <b>What the map cannot show is how little of these highlands has been dug</b>: the blank spaces are gaps in the survey record, not gaps in the past, and this book says so rather than implying the district was empty.',
 'Garrod (1928, 1932); Boyd &amp; Crossland, Antiquity 74 (2000); Badè at Tell en-Naṣba (1926–35); Marquet-Krause and Callaway at et-Tell; Yeivin at ʿAin Samiya; Khalaily and Vardi at Motza; Perrot and Khalaily at Abu Ghosh; Kenyon at Tell es-Sultan.')}
<p><b>Dorothy Garrod dug the cave at Shuqba for the British School of Archaeology in Jerusalem in
1928</b>, and named the industry she found there after the wadi{c('D. A. E. Garrod, “Excavation of a Palaeolithic cave in western Judaea,” <i>Quarterly Statement of the Palestine Exploration Fund</i> 60 (1928), 182–85; and “A new Mesolithic industry: the Natufian of Palestine,” <i>Journal of the Royal Anthropological Institute</i> 62 (1932), 257–69 — the formal naming paper. The full excavation report is Garrod &amp; D. M. A. Bate, “Excavations at the cave of Shukbah, Palestine, 1928,” <i>Proceedings of the Prehistoric Society</i> 8 (1942), 1–20.')}. She did not find it first —
Fr Alexis Mallon had noted the cave in 1924 and urged the School to take it on — but hers is the
excavation that gave the culture its name, and the name is a Palestinian place-name{c('Alexis Mallon, “Quelques stations préhistoriques de Palestine,” <i>Mélanges de l’Université Saint-Joseph</i> 19 (1925), 191–92. Fieldwork was resumed at the cave and in the wadi by Brian Boyd and Zoë Crossland, “New fieldwork at Shuqba Cave and in Wadi en-Natuf, Western Judea,” <i>Antiquity</i> 74:286 (2000), 755–56.')}.</p>
<p><b>What is claimed here, and what is not.</b> The Natufians are often called the first sedentary
people in the world. <i>That is more than the evidence carries.</i> Brush huts with prepared floors
and bedding at Ohalo II, on the Sea of Galilee, are some eight thousand years older, and how complete
Natufian sedentism was is actively argued{c('Chronology after L. Grosman, “The Natufian Chronological Scheme — New Insights and their Implications,” in Bar-Yosef &amp; Valla (eds), <i>Natufian Foragers in the Levant</i> (2013), 622–37: roughly 13,050–9,550 cal BC, conventionally split into an Early and a Late phase — though T. Richter et al., <i>Scientific Reports</i> 7 (2017), 17025, show the two overlap. For the earlier huts: D. Nadel et al., “Stone Age hut in Israel yields world’s oldest evidence of bedding,” <i>PNAS</i> 101:17 (2004), 6821–26. For the sceptical case on sedentism: Brian Boyd, “On ‘sedentism’ in the Later Epipalaeolithic (Natufian) Levant,” <i>World Archaeology</i> 38:2 (2006), 164–78.')}. <b>What is defensible is narrower and still remarkable:
they were the first here to build routinely in stone, and the first with base camps occupied through
much or all of the year — before farming.</b> The best single piece of evidence is not architectural
at all: the <b>house mouse</b> displaces its wild cousin only where people stay put long enough to
sustain it, and the house mouse appears at Natufian sites{c('L. Weissbrod, F. B. Marshall, F. R. Valla, H. Khalaily, G. Bar-Oz, J.-C. Auffray, J.-D. Vigne &amp; T. Cucchi, “Origins of house mice in ecological niches created by settled hunter-gatherers in the Levant 15,000 y ago,” <i>PNAS</i> 114:16 (2017), 4099–4104. Cited here as strong but not unchallenged; it drew a published comment and reply in the same journal.')}.</p>
<p><b>And below the Natufian floor of that same cave, something older still.</b> Garrod recovered a
single tooth from the Mousterian layer beneath — a child’s <b>permanent</b> lower first molar, from an
individual of about seven to twelve years. In 2021 a re-examination by
micro-CT identified it as <b>Neanderthal — the southernmost Neanderthal yet securely identified</b>,
and — <i>on the excavators’ reading, which is disputed</i> — found with Nubian Levallois
stone-working, a technique previously treated as a signature of <i>Homo sapiens</i>{c('J. Blinkhorn, C. Zanolli, T. Compton, H. S. Groucutt, E. M. L. Scerri, L. Crété, C. Stringer, M. D. Petraglia &amp; S. Blockley, “Nubian Levallois technology associated with southernmost Neanderthals,” <i>Scientific Reports</i> 11 (2021), 2869, DOI 10.1038/s41598-021-82257-6. The specimen is NHMUK PA EM 3869, a lower right first molar of a child from Layer D; it should not be confused with the Natufian burials Garrod found in Layer B above it, and there is still no direct chronometric date on Layer D. <b>The Nubian association was rebutted the following year in the same journal</b> — Hallinan, Barzilai, Bicho, Cascalheira, Demidenko, Goder-Goldberger, Hovers, Marks, Oron &amp; Rose, “No direct evidence for the presence of Nubian Levallois technology and its association with Neanderthals at Shukbah Cave,” <i>Scientific Reports</i> 12 (2022), DOI 10.1038/s41598-022-05072-7 — on the grounds that Layer D is a brecciated palimpsest that cannot be treated as one undisturbed deposit. <b>The tooth is Neanderthal. What it was found with is still argued.</b>')}. <i>Eighteen kilometres from Ramallah, in
a cave in this governorate, and there is still no direct date on the layer.</i></p>"""),

ent('c. 9600 BC', 'attested', False, 'Jericho: a town, a tower and a wall — twenty-three kilometres away',
 'Twenty-three kilometres down the eastern slope from this ridge, at <b>Tell es-Sultan</b>, people stopped moving and stayed. Permanent settlement from about <b>9600 BC</b>; a round stone tower <b>8.5 metres high with twenty-two steps inside it</b>, built about <b>9000 BC</b>; a wall 3.6 metres high and 1.8 metres thick at the base{}. <i>It is twenty-three kilometres from Ramallah as the crow flies, and it is one of the earliest permanent settlements known anywhere on earth.</i> <b>And it is the same mound as the Jericho of Joshua 6</b> — but that town, if it is anywhere in this tell, lies near the <i>top</i> of it, some eight thousand years higher in the stratigraphy than the tower this entry is about{}. <i>One hill, forty layers, and this book is standing on the bottom one.</i>'.format(c('Kathleen M. Kenyon &amp; T. A. Holland (eds), <i>Excavations at Jericho, Vol. 3: The Architecture and Stratigraphy of the Tell</i> (London: British School of Archaeology in Jerusalem, 1981). The tower is c. 8.5 m high and c. 9 m across at the base, tapering to c. 7 m, with an internal staircase of twenty-two stone steps; the wall over 3.6 m high and 1.8 m thick at the base. Earlier work: Sellin and Watzinger 1907–11; Garstang 1930–36, whose Bronze Age dating Kenyon overturned.'), c('The Jericho of Joshua 6 would belong to the Late Bronze Age, at the top of a mound whose base is Pre-Pottery Neolithic A. Whether there was a walled Late Bronze town there at all is one of the longest-running arguments in the archaeology of this country — Garstang read the destruction as Joshua’s, Kenyon re-dated it, and the debate has not closed. <b>This book takes no position on it</b>, because its subject here is the bottom of the mound and not the top. See Sparks, Finlayson, Wagemakers &amp; Briffa (eds), <i>Digging Up Jericho</i> (2020).')),
 """
<p><b>Two things usually said about Jericho should not be said.</b> It is <i>not</i> “the oldest
continuously inhabited town in the world”: the tell has documented gaps — several centuries between
the Pre-Pottery Neolithic A and B, more in the Pottery Neolithic, abandonment around 1950 BC, and
effective abandonment after the Iron Age — and the modern town sits <i>beside</i> the mound, not on
it. Nor is it safely the oldest walled town: the round towers at <b>Tell Qaramel</b> in northern
Syria are some two thousand years older, and Jericho’s wall has never been traced around the whole
settlement{a}. <b>UNESCO, inscribing the site in 2023 under the State of Palestine, calls it a sizeable
permanent settlement and ties it to the shift to a sedentary way of life — and this book follows that
wording rather than the tourist one</b>{b}.</p>
<p><b>And what the tower was for is genuinely unresolved.</b> Kathleen Kenyon, who found it in 1952,
read tower and wall as fortification. Ofer Bar-Yosef argued they were flood and mudflow defences, and
made the strongest single point in the debate: <i>there is no evidence of burnt settlements, mass
casualties or comparable fortifications anywhere in the Levant before the sixth millennium BC — some
three thousand years later</i>. A
defensive reading has to explain that absence. Others have read the tower as a monument of political
authority over a prime spring, or as a solstice marker{d}. <b>No explanation commands agreement, and
this book prints the disagreement rather than picking a side.</b></p>
<p><i>One caution on dates, because it is a trap.</i> The figure “8000 BC,” still common in books, is
an <b>uncalibrated</b> radiocarbon date from Kenyon’s samples. Calibrated, the Pre-Pottery Neolithic A
at Tell es-Sultan runs roughly 9700/9600 to 8600/8500 BC, and the tower is about eleven thousand
years old — around 9000 BC. This book uses the calibrated figures throughout.</p>
<p><b>And something has to be said about who has been doing the digging.</b> Every excavator named so
far in this entry is European or Israeli, and that is how this entry stood in earlier editions of
this book — <i>which is not how the mound has actually been dug for the last thirty years.</i> Since
<b>1997</b> Tell es-Sultan has been excavated by a joint expedition of the <b>Palestinian Department
of Antiquities and Cultural Heritage</b>, under the Ministry of Tourism and Antiquities, and Rome
«La Sapienza» — directed by <b>Hamdan Taha</b> and <b>Lorenzo Nigro</b>, with Nicolò Marchetti in the
early seasons — and it is still running, with an interim report on the Bronze and Iron Age towns
covering the seasons of 2019–2023, published by <b>Lorenzo Nigro and Jehad Yasine</b>{e}. It is their work, and not Kenyon’s, that now describes the
<i>town</i> that stood around the tower: an urban plan and a massive fortification system in place by
<b>Early Bronze II, about 3000–2700 BC</b>; a double city wall traced at the southern and
south-western edges of the mound; a palace-centred society in <b>Early Bronze III</b>; and occupation
spreading outside the Middle Bronze wall. <b>The nomination file on which UNESCO inscribed the site in
2023 was prepared by a Palestinian team under that same ministry</b>{f}.</p>
<p><i>The tower is still Kenyon’s find, and what it was for is still unresolved.</i> But the town
around it has been re-excavated, re-dated and published by the people whose town it is, and from this
edition onward this book cites them for it.</p>
{g}""".format(
  a=c('On the occupation gaps and the making of the “oldest city” claim, see Rachael Sparks, Bill Finlayson, Bart Wagemakers &amp; Josef Briffa (eds), <i>Digging Up Jericho: Past, Present and Future</i> (Oxford: Archaeopress, 2020) — the best single volume on the evidence and its historiography. For the older towers: R. F. Mazurowski &amp; Y. Kanjou (eds), <i>Tell Qaramel 1999–2007</i> (Warsaw: PCMA, 2012), with radiocarbon in Mazurowski et al., <i>Radiocarbon</i> 51:2 (2009), 771–81: the earliest tower c. 10,900–9,670 cal BC.'),
  b=c('UNESCO World Heritage List no. 1687, “Ancient Jericho/Tell es-Sultan,” inscribed 2023 at the extended 45th session of the World Heritage Committee, Riyadh, under the State of Palestine, on criteria (iii) and (iv). The statement of Outstanding Universal Value describes deposits “dating back to about 10,500 BC” and a “sizeable permanent settlement.” <a href="https://whc.unesco.org/en/list/1687/">whc.unesco.org/en/list/1687</a>.'),
  d=c('Kenyon &amp; Holland (1981) for the defensive reading; Ofer Bar-Yosef, “The Walls of Jericho: An Alternative Interpretation,” <i>Current Anthropology</i> 27:2 (1986), 157–62, for flood defence and the absence-of-warfare argument; Danny Naveh, “PPNA Jericho: A Socio-Political Perspective,” <i>Cambridge Archaeological Journal</i> 13:1 (2003), 83–96; Ran Barkai &amp; Roy Liran, “Midsummer Sunset at Neolithic Jericho,” <i>Time and Mind</i> 1:3 (2008), 273–83.'),
  e=c('The Italian–Palestinian Expedition to Tell es-Sultan, from 1997: Rome «La Sapienza» with the Palestinian Ministry of Tourism and Antiquities, Department of Antiquities and Cultural Heritage (MOTA-DACH). Season reports are published jointly under Lorenzo Nigro and Hamdan Taha, with Nicolò Marchetti in the first seasons — e.g. Marchetti, Nigro &amp; Taha, “Preliminary Report on the Third and Fourth Seasons… 1999–2000,” in I. Thuesen (ed.), <i>Proceedings of the Second ICAANE</i> (Bologna, 2016), 581–97; Nigro &amp; Taha, “The Early Bronze Age Palace and Fortifications at Tell es-Sultan/Jericho: the 6th–7th seasons (2010–2011)”; and the interim report on the Bronze and Iron Age cities covering 2019–2023. See also Nigro, <i>Aside the Spring: Tell es-Sultan / Ancient Jericho — the Tale of an Early City and Water Control in Ancient Palestine</i>.'),
  f=c('Hamdan Taha, “Tell es-Sultan, Ancient Jericho,” <i>This Week in Palestine</i>: “Following the transfer of authority to the Palestinian Authority in 1994, the Palestinian Department of Antiquities, working jointly with La Sapienza University of Rome, resumed the work at Tell es-Sultan,” and the nomination file was “being prepared by a team of experts under the auspices of the Ministry of Tourism and Antiquities.” Inscribed 2023 as World Heritage no. 1687, under the State of Palestine.'),
  g=FIX('Jericho told entirely through Sellin and Watzinger, Garstang, Kenyon and Bar-Yosef — every excavator named in the entry European or Israeli.',
        'The current excavation is <b>Palestinian–Italian and has run since 1997</b>: MOTA-DACH with Rome «La Sapienza», <b>Hamdan Taha</b> and <b>Lorenzo Nigro</b> directing. Their sequence for the Bronze Age town is the one this book now follows, and the 2023 UNESCO nomination is a Palestinian document.',
        'Not a factual correction but a correction of attribution, and the book’s own standard requires it: <i>Palestinian and Arab scholarship is cited as the source, and the foreign partner as the route.</i> The Neolithic tower remains Kenyon’s discovery and is still credited to her; what changes is that the Bronze Age town, the fortifications and the site’s present interpretation are credited to the expedition that produced them.'))),

ent('the whole of it', 'attested', False, 'What this land is made of',
 'Before the story starts moving, one picture of the whole thing: <b>fifteen thousand years of habitation on this ridge and around it, drawn as a section through a tell</b> — and the layer, four from the top, where our own family walks in.',
 fig(F4.fig_layers(),'The land, drawn as a tell — fifteen thousand years of layering',
  'Read it from the bottom, the way a section is dug. <b>Nothing in this column replaces the layer beneath it.</b> Arrivals are absorbed; only the Franks, in the thin purple band, come and go again. The family arrives in the Ottoman layer, four from the top, into ground that had already been lived on continuously for more than eleven thousand years. <i>Layer thicknesses are drawn for legibility, not to scale in time; every date in the column is calibrated and sourced in the entries around this figure.</i>',
  'This book, throughout; the deep layers from the entries above, the later ones from the eras that follow.')),

CH(4)
sect('And in our own line', 'A dam in Joktan’s country, and a road that ends at Gaza')
ent('8th–7th c. BCE', 'attested', 'shared', 'The great dam of Maʾrib is built — in Joktan’s country',
 'The monumental sluice works of the Sabaean dam are dated by inscription and excavation to about the eighth and seventh centuries BCE{}. The family’s own account — ʿAdnān al-Ḥaddādīn’s 1953 manuscript, printed by Shāhīn — remembers it “built as early as the 7th century B.C.” <i>A memory that lands on the right phase — see the qualification below.</i>'.format(c('The Maʾrib sluice structures, Sabaean period, c. 8th–7th c. BCE, with earlier earthworks beneath; ʿAdnān al-Ḥaddādīn, <i>A Brief History of the Haddadeen</i> (MS, Ramallah City Hall, 8 August 1953), as printed in Shāhīn (1982), ch. 1.')),
 f"""
<p>It is worth pausing on what this thing actually was, because <b>the whole first half of this
family’s story is a story about water</b>. The dam was not a reservoir. It was a diversion wall —
some five hundred and eighty metres of packed earth faced with stone, thrown across the Wādī Dhana
where it breaks through a gap between two mountains — and its purpose was to catch the flash-floods
that come off the Yemeni highlands twice a year and push them, through two great masonry sluice
towers, into a network of canals{c('On the structure and its phases: the Sabaean earthworks of the 8th–7th centuries BCE, the monumental sluice towers of the 6th, and the successive raisings of the wall recorded in the Sabaic inscriptions of the mukarribs. The irrigated area is generally estimated at some 9,600 hectares.')}. It watered something on the order of ninety-six square
kilometres of desert — <b>and it did so, with repairs, for something close to thirteen hundred
years</b> — a working life almost nothing else in the ancient world matched, though the Dujiangyan
irrigation works in Sichuan, begun about 256 BC, are still running today{c('UNESCO World Heritage List no. 1001, “Mount Qingcheng and the Dujiangyan Irrigation System,” inscribed 2000: built c. 256 BC and still in operation. Earlier editions of this book said nothing else in the ancient world ran as long as the Maʾrib dam; that is not true, and the claim is now stated as a comparison rather than a record.')}.</p>
{fig(F3.fig_dam_eng(),'The machine that watered a kingdom',
 'The dam of Maʾrib in schematic: the wadi, the gap between the two Balaq mountains, the wall, the two sluices, and the two irrigated gardens on either bank. The Qurʾān’s phrase for Sabaʾ — “two gardens, on the right hand and on the left” — is a literal description of this diagram.',
 'The Sabaic inscriptions and the excavation record; Qurʾān 34:15.')}
<p>And here a <b>third text</b> joins the family’s two. The Qurʾān describes this exact place, in
these exact terms: <i>“There was for Sabaʾ, in their dwelling-place, a sign: two gardens, on the
right hand and on the left”</i>{c('Qurʾān 34 (Sūrat Sabaʾ):15. The chapter takes its name from the kingdom.')}. <b>Genesis puts Joktan’s sons in this country; the Qurʾān
describes its gardens; the family’s 1953 manuscript dates the dam’s monumental phase to the seventh
century BC; and the inscriptions bear that phase out.</b></p>
<p><i>Two honest qualifications, because this book does not get to have it both ways.</i> Genesis says
nothing whatever about a dam — it is a witness to the <i>country</i>, not to the structure. And a
1953 Arabic manuscript giving a date in the form “the 7th century B.C.” is far more likely to be
repeating published European scholarship on Maʾrib than remembering anything: <b>it is the ONE
TRADITION problem in miniature, and it applies to the family’s own text.</b> Dam-building at the
Wādī Dhana also begins around 1750–1700 BC, a thousand years before the monumental sluices, so
“as early as the 7th century B.C.” is right about one phase and late by a millennium about the
site.</p>"""),

CH(2)

sect('What the ground says', 'The first people of this land, and the layers they left')
ent('c. 3500 – 2400 BC', 'attested', False, 'The first villages of this district',
 'Not a general claim about “the region” — <b>named, excavated, dated sites within a few kilometres of the town</b>. <b>Tell en-Naṣba</b>, on the edge of al-Bīra and <b>under two kilometres</b> from Ramallah’s centre, is a Late Chalcolithic and Early Bronze I village of about 3500–3300 BC{}. <b>et-Tell</b>, five kilometres east, is an Early Bronze town occupied 3200–2400 BC{}. <b>ʿAin Samiya</b>, fifteen kilometres north-east, holds an Intermediate Bronze shaft-tomb cemetery of 2300–2000 BC — the source of the famous ʿAin Samiya goblet{}.'.format(
  c('Tell en-Naṣba, identified with biblical Mizpah, on the edge of al-Bīra. Excavated in five seasons, 1926–1935, by William Frederic Badè for the Pacific School of Religion. The Late Chalcolithic / Early Bronze I village is Stratum 5, c. 3500–3300 BC, after which the site was long abandoned.'),
  c('et-Tell, generally identified with biblical Ai, 5.3 km east of Ramallah. Excavated by John Garstang (1928), Judith Marquet-Krause (1933–35), Joseph Callaway (1964–70) and Hani Nur el-Din (2005–07). Occupation runs from Early Bronze I through Early Bronze III, c. 3200–2400 BC.'),
  c('ʿAin Samiya and the neighbouring Dhahr Mirzbaneh, about 13 km north-east of Ramallah on the coordinates this book plots — <b>the site’s exact position is not independently verified here and should be checked before the figure is quoted</b>: Intermediate Bronze Age (Early Bronze IV) shaft-tomb cemeteries, c. 2300–2000 BC. Paul Lapp excavated Dhahr Mirzbaneh in 1963; Zvi Yeivin excavated ʿAin Samiya in 1970–71. The ʿAin Samiya goblet is an Intermediate Bronze piece, not a Chalcolithic one.')),
 """
<p><i>Two corrections worth making, because both errors are common in local writing.</i>
<b>ʿAin Samiya is routinely called Chalcolithic. It is not</b> — it is Intermediate Bronze Age, some
fifteen hundred years later. And <b>et-Tell has no Chalcolithic phase at all</b>: its earliest
occupation is Early Bronze I, about 3200 BC.</p>
<p>The point of naming them is simple. When this book says the population of these hills was never
replaced, it is not arguing from a general theory about the Levant. <b>It is arguing from ground you
can walk to from Ramallah in an afternoon, which has been dug, dated and published.</b></p>"""),

ent('c. 1500 BCE', 'attested', False, 'The Canaanite population of these highlands',
 'Everything that follows is added to this. <b>Present-day Lebanese draw more than ninety per cent of their ancestry from the Bronze Age Canaanite population</b>, and present-day southern Levantine populations — this town among them — carry a large Bronze Age component of the same kind alongside later admixture{}.'.format(c('Haber et al., “Continuity and Admixture in the Last Five Millennia of Levantine History,” <i>AJHG</i> 101:2 (2017), 274–82 — the >90% figure is measured for <b>present-day Lebanese</b> against Bronze Age Sidon, and earlier editions of this book wrongly generalised it to “Levantine ancestry.” For the southern Levant: Agranat-Tamir et al., <i>Cell</i> 181:5 (2020), 1146–57.')),
 f"""
{fig(F.fig_confluence(),'How a people is made',
 'Ten arrivals and one people. Each bar begins when that group enters the record and fades into the common green as it is absorbed. Only the Samaritans keep their own colour to the present; only the Franks stop. The family’s own stream — Arabs, and Ghassān — is the ninth bar. It was absorbed like the rest, and that is the argument of this whole book in one picture.',
 'Haber et al. (2017); Feldman et al. (2019); Agranat-Tamir et al. (2020); Haber et al. (2019) on the Crusader pulse; Killebrew (2005); Ehrlich (2022) on conversion.')}
<p><b>There is no point in the last four thousand years at which the people of this country were
replaced.</b> The Philistines are the case that can be measured: they arrived about 1175 BCE
carrying a southern-European-related ancestry whose source population is still not pinned
down, visible in the genome at Ashkelon — and then, <b>“within no more than two centuries,
this genetic footprint … is no longer detectable.”</b>{c('Feldman et al., “Ancient DNA sheds light on the genetic origins of early Iron Age Philistines,” <i>Science Advances</i> 5:7 (2019), eaax0061.')} They were not driven out. They married
the neighbours. The Idumaeans were absorbed by 70 CE; the Nabataeans’ kingdom became a Roman
province in 106 while its people stayed put; the country turned Christian, then largely Muslim, by
conversion and not by replacement{c('Michael Ehrlich, <i>The Islamization of the Holy Land, 634–1800</i> (Arc Humanities, 2022); Milka Levy-Rubin on Arabization versus Islamization.')}. The Samaritans, who never merged, are still on Mount
Gerizim — the living control. And the Franks, who genuinely left, prove the rule by breaking it:
replacement leaves a signature, and only they left one{c('Haber et al., “A Transient Pulse of Genetic Admixture from the Crusaders in the Near East,” <i>AJHG</i> 104:5 (2019): “present-day populations derive most of their ancestry from local people who preceded the Crusades.”')}.</p>
<p><b>So a Christian family claiming descent through Ghassān from Yemen, and a Muslim family of the
next village claiming the Ḥijāz, and the Samaritans of Nablus claiming to have gone nowhere, are not
making rival claims. They are describing different arrivals into the same people.</b> Hold that
thought; the family’s own arrival is four bars down.</p>"""),

ent('nobody can date it, and it is still in use', 'attested', False,
    'THE TERRACES — and the hundred and sixty-seven towers standing in them',
 f'''The hills around Ramallah are not hills. <b>They are staircases.</b> Every workable slope within
sight of the town has been cut into level treads held up by dry-stone risers — <span class="ar">سناسل</span>,
the local word — and nothing holds a riser up but the weight of the stones in it: no mortar, no
foundation, no bonding material of any kind{c('Shadi Ghadban, “Palestinian Dry Stone Structures — An Endogenous Expression of Cultural Landscape,” <i>Journal “Sustainable Development, Culture, Traditions”</i> 1b (2015), 34–46, at 44: the structures are “generally constructed from rubble natural stones with irregular and polygonal forms without using any bonding material,” the stones “simply fitted in harmony with their natural form and not in regular layers.” ' + D('2015_Ghadban_Palestinian_Dry_Stone_Structures_SDCT_1b.pdf') + '.')}. Standing in those fields are small round huts with
corbelled stone roofs, built by the farmers themselves so that somebody could sleep beside the crop
while it ripened. <b>In 2013 two Palestinian scholars went out and counted them.</b> In al-Tireh
quarter and the village of ʿAin Qinia alone — the ground on Ramallah’s own western and northern
edge — they recorded <b>one hundred and sixty-seven watchtowers over some three thousand
dunums</b>{c('Salah Hussein Al-Houdalieh &amp; Shadi Sami Ghadban, “Agricultural Watchtowers in Al-Tireh Quarter and ʿAin Qinia Village, Ramallah, Palestine,” <i>International Journal of Architectural Heritage</i> 7:5 (2013), 509–535, DOI 10.1080/15583058.2011.654049. The survey documented <b>167 watchtowers distributed over an area of approximately 3,000 dunums</b>, by site documentation, fieldwork and interviews with residents. Al-Houdalieh is the same al-Quds University archaeologist who excavated Khirbet et-Tireh; Ghadban is professor of architectural engineering at Birzeit.')}.''',
 f"""
{fig(F4.fig_terraces(), 'The terraces, and one of the towers standing in them',
 'A hillside above Ramallah drawn in section. Every riser is a dry-stone wall; every tread is a field; the small domed hut on the third terrace is one of the hundred and sixty-seven. The cutaway shows how the roof closes — each course of stone oversailing the one below until the last two meet, with nothing binding them. <b>The strip along the bottom is the year:</b> the tower is occupied for grain in May and June, for figs and grapes from July to September, and for the olives in October and November.',
 'Al-Houdalieh &amp; Ghadban, <i>International Journal of Architectural Heritage</i> 7:5 (2013), 509–35, for the count and the survey; Ghadban (2012, 2015) for the construction and the seasons.')}
<p><b>Nobody can date them, and that is the honest finding rather than a gap in the research.</b>
Corbelled dry-stone building is old in this region — probably Early Bronze Age in origin — but a
terrace wall is not a monument, it is a machine, and a machine in use gets repaired. The stone that
fell out last winter went back in this spring, and the stone beside it may have been set by a
Canaanite. <i>There is no stratigraphy in a wall that has never been allowed to fall down.</i>
The survey says so plainly: there is no concrete evidence for when the dry-stone structures of
Palestine first appeared{c('Ghadban (2015), 37 and 39: corbelled structures “originated mainly in the Near East of the Mediterranean Basin probably at the beginning of the Early Bronze Age,” but there is “no concrete evidence regarding when exactly the dry-stone structures first appeared” in Palestine. <b>This book therefore gives the terraces no date at all rather than an invented one.</b>')}.</p>
<p><b>What can be dated is the work, because the work is seasonal and has not changed.</b> The tower
is used when there is something in the field worth losing: the grain and the early fruit in May and
June, the figs and the grapes from July through September, the olives in October and November.
<i>That is seven months of the year in which somebody from the household is sleeping out on the
land.</i> The huts were built cooperatively — several men to a tower — and the owner of the ground
fed them while they built it{c('Ghadban (2015), 40 and 43, on the three harvest seasons — “early fruit and grain harvest… May and June,” “figs and grape-vines… July through September,” “olive harvesting… October and November” — and on cooperative building: “peasants would mostly collaborate in building the structures,” with the owner providing food. Also Ghadban, “The Architecture of the Palestinian Dry-Stone Hut — Al-mantarah,” <i>Journal of Comparative Cultural Studies in Architecture</i> 6 (2012), 16–25.')}.</p>
<p><b>This is the district’s own technology, and it is the only thing in this chapter that the
family’s own ancestors certainly made with their hands.</b> The churches were built by patrons; the
registers were written by clerks; the armies belonged to somebody else. The terraces were built by
whoever was going to eat off them, and they are still there, and people are still eating off
them.</p>
<p><i>They are also going.</i> Ghadban’s parallel survey of the walls themselves found roughly
<b>eighty-seven per cent of them partially collapsed</b> — from land confiscation and settlement
expansion, from the separation wall cutting farmers off from their own plots, from the sprawl of the
town up its own hillsides, and from the plain fact that fewer people now farm{c('Ghadban (2015), 36 and 42: “approximately 87% of the individual walls are partially destroyed,” under pressure from land confiscation, settlement expansion, the separation wall, the declining economic weight of agriculture and “rapid and largely sprawl urban expansion.” <b>The 87 per cent is measured on the walls, not on the towers; the 167 towers are those still standing.</b>')}. <b>A wall that is
repaired every year survives four thousand years. A wall that nobody walks to falls down in
twenty.</b></p>"""),

ent('c. 1350 BCE', 'documents', False, 'THE AMARNA LETTERS — a file about who works the fields',
 f'''Jerusalem, Shechem, Gezer and Lachish write to Egypt in Akkadian{c('The Tell el-Amarna correspondence, fourteenth century BCE: some 350 letters and administrative texts from the Egyptian capital at Akhetaten, found in 1887. The standard edition is William L. Moran, <i>The Amarna Letters</i> (Baltimore: Johns Hopkins, 1992); see also Anson F. Rainey, <i>The El-Amarna Correspondence</i>, 2 vols (Leiden: Brill, 2015).')}. These are the city-states of this landscape, and they are Canaanite. Even the town’s own name keeps the era’s sound: <span class="ar">رام</span> is a Semitic root meaning <i>height</i> — Canaanite-era vocabulary still doing its job{c('al-Dabbāgh, <span class="ar">بلادنا فلسطين</span>, viii/2, on <span class="ar">رام</span>; the same root as Hebrew <i>rām</i> and Aramaic <i>rāmā</i>.')}. <b>But the letters are usually read for the wrong thing.</b> They are read as diplomacy — kings, tribute, the <i>ʿapiru</i>, who is loyal and who is not. <i>Read them as an employer reads a file, and they are about labour: who goes up the hill, and who ploughs.</i>''',
 f"""
<p>The clearest sentence in the whole archive on that question is a small tablet in the Louvre,
six and a half centimetres by six, catalogued <b>EA 365</b>. Moran gives it the heading
<i>Furnishing corvée workers</i>. It is from <b>Biridiya, the mayor of Megiddo</b>, and after the
formula of prostration it says this{c('EA 365, Louvre, Antiquités orientales AO 7098; 6.5 × 6.0 cm. Translations: Moran (1992); Anson F. Rainey (1970); earlier Mercer (1939) and Albright in <i>ANET</i> (1969). The rendering quoted here follows the standard English of the passage.')}:</p>
<blockquote>Let the king, my lord, be aware regarding his servant and his city.
<b>Behold, I alone am cultivating in the city of Shunama; and, as for me, I provide forced
labourers.</b> Now, behold, the mayors who are near me do not do as I do. They do not cultivate
in the city of Shunama, and they do not provide forced labourers. <b>I alone provide forced
labourers.</b>
<span class="cite">Amarna letter EA 365, Biridiya of Megiddo to the king of Egypt · Louvre AO 7098</span></blockquote>
<p><b>The word he uses is <i>massu</i></b> — the same Semitic word that stands in the Hebrew Bible as
<i>mas</i>, the levy of forced labour a king raises out of his own people{c('Akkadian <i>massu</i> / <i>mas</i>, corvée labour imposed on subject populations for building, quarrying and agricultural work; the same term appears in Biblical Hebrew as <span class="ar">מס</span> <i>mas</i>, e.g. 1 Kings 5:13–14 and 9:15. See Moran (1992), glossary s.v.; Rainey, <i>El-Amarna Correspondence</i>, ii, on the labour vocabulary of the Megiddo letters.')}. Biridiya is not
complaining about an invasion. He is complaining that his neighbours are not sending men, and that
the whole gang on that field is his. <i>He is filing a labour return.</i></p>
<p><b>This letter is not about this ridge, and it should not be made to be.</b> Shunama is Shunem,
in the Jezreel valley, some sixty kilometres north; the ridge above Ramallah lay in the territory
the king of Jerusalem wrote about. It is quoted here for a different reason. Every document in this
book from here to the Ottoman registers is written by somebody counting other people — a mayor, a
scribe, a bishop, a tax clerk — and in every one of them the people being counted are the same
people: the ones in the field. <b>The archive names the mayors. The corvée is everybody else, and
everybody else is the ancestors.</b></p>
<p><i>Three thousand years later a qāḍī in Jerusalem will write down six men from the village of
Ramallah who have promised to plough a hill, and he will name all six.</i> That is the whole
difference between the two ends of this book: not who was working, but whether anyone wrote down
their names.</p>"""),

CH(3)

sect('What the ground says', 'Who else was on this coast and this plateau — and what became of every one of them')
ent('c. 1200 → 1000 BCE', 'attested', False,
    'WHO WAS ON THIS RIDGE — the highlands fill up, and nobody arrives',
 f'''Across the two centuries after the Late Bronze collapse the central hill country goes from
roughly <b>twenty-five settlements to roughly two hundred and fifty</b>, and from a scatter of people
to something near <b>forty-five thousand</b>. The new villages are small, unwalled, agricultural, and
founded on hilltops nobody had bothered with before{c('The figures are from the archaeological surveys of the central hill country, summarised in Israel Finkelstein, <i>The Archaeology of the Israelite Settlement</i> (Jerusalem: Israel Exploration Society, 1988), and revisited in Finkelstein &amp; Neil Asher Silberman, <i>The Bible Unearthed</i> (New York: Free Press, 2001). For the population estimate and the ethnogenesis models, Ann E. Killebrew, <i>Biblical Peoples and Ethnicity</i> (Atlanta: SBL, 2005). <b>These are survey counts, not excavation counts</b> — the great majority of the 250 sites have been walked and sherded, not dug.')}. <i>Nothing comparable happens on the coast, or in the
Jordan valley, or anywhere a migration would have had to come from.</i>''',
 f"""
{fig(F4.fig_highland_fill(), 'The highlands fill up, and nowhere else empties out',
 'One dot for every settlement the surveys found. <b>The jump is real and it is local.</b> A tenfold increase in two centuries is a great deal of people — but they appear in the hills without appearing to leave anywhere else, and they arrive carrying the same cooking pots as the country they are already in.',
 'Finkelstein (1988); Finkelstein &amp; Silberman (2001); Killebrew (2005).')}
<p><b>Three things the surveys do not find, and each of them is an argument.</b> <b>No destruction
horizon</b> — the highland villages are new foundations on empty ground, not burnt towns taken over.
<b>No new pottery tradition</b> — the cooking wares continue the local Late Bronze repertoire, and a
population arriving from outside brings its own kitchen. <b>No matching emptying-out</b> — if these
tens of thousands had walked in from the coast or the valley, the coast and the valley would show
it, and they do not{c('On the absence of a destruction horizon and the continuity of the ceramic repertoire, William G. Dever, <i>Who Were the Early Israelites and Where Did They Come From?</i> (Grand Rapids: Eerdmans, 2003); Avraham Faust, <i>Israel’s Ethnogenesis</i> (London: Equinox, 2006), which argues for a distinct highland identity forming <i>in situ</i> rather than arriving; and Killebrew (2005) for the multi-origin model — local Canaanites, sedentarising pastoralists, and marginal groups the Egyptian records call <i>ʿapiru</i> and <i>Shasu</i>.')}.</p>
<p><i>So where did they come from?</i> <b>From the country.</b> The reading the evidence supports is
formation in place: highland farmers already there, pastoralists settling down, and people moving up
off the failing lowland city-states when the Late Bronze order came apart. It is not one origin. It
is the ordinary churn of a region reorganising itself after a collapse — <b>and every strand of it is
already local</b>.</p>
{fig(F4.fig_iron_ridge(), 'The ridge in the Iron Age, and the gap in the middle',
 'Every excavated Iron Age site within a morning’s walk. <b>Khirbet Raddana lies inside al-Bīra</b> — a village of the twelfth and eleventh centuries BC, on Ramallah’s doorstep, excavated over four salvage seasons between 1969 and 1974 and since built over by the town’s own growth. The dashed ring is Ramallah, which is not there yet and will not be for two and a half thousand years.',
 'Callaway and Cooley at Khirbet Raddana and et-Tell; Badè at Tell en-Naṣbeh; al-Houdalieh &amp; Sauders (2009) on what urban growth has since done to these sites.')}
<p><b>Now the name.</b> The word <i>Israel</i> first appears in 1208 BC, on a victory stele of the
pharaoh <b>Merneptah</b> — and it is written with the Egyptian determinative for <b>a people</b>, not
for a city or a land{c('The Merneptah stele, Cairo Museum JE 31408, from Thebes, year 5 of Merneptah, c. 1208 BC. In the closing lines Israel is the only entity of the group written with the determinative for a people rather than a foreign land — <i>a group of people, located somewhere in Canaan, without a territory of its own attached to the name.</i> Every other place in the passage — Ashkelon, Gezer, Yanoam — takes the city or land determinative.')}. A people in
Canaan, with no territory attached to the name. <i>That is what the earliest external witness says
Israel is: a group of people living in this country, among the people of this country.</i></p>
<p><b>And that is the shape of this whole book in one paragraph.</b> The population on this ridge is
continuous — Canaanite, then Israelite and Judaean, then Hellenised, then Christian by conversion,
then in large part Muslim by conversion, then Palestinian. <b>Those are names taken by a people, not
peoples replacing one another.</b> The family this book follows is inside that continuity, and so is
everyone else who ever farmed these terraces. <i>Nobody on this ridge is a newcomer, and nobody on it
is the only one who was here.</i></p>"""),

ent('the names on the ground', 'documents', True,
    'THE BIBLE IS A MAP OF THIS DISTRICT — and Palestinian villagers are why it can be read',
 f'''Here is something that ought to be said louder than it usually is. <b>Nobody found the biblical
places by reading the Bible.</b> They were found by walking into Palestinian villages and asking the
people who lived there what they called home — and the answers turned out to be the ancient names,
carried in Arabic, on the tongues of farming families, for three thousand years{c('Edward Robinson and Eli Smith travelled Palestine in 1838 and published <i>Biblical Researches in Palestine, Mount Sinai and Arabia Petraea</i> in 1841. Robinson’s method was to record the Arabic name in local speech and test it against the Hebrew or Greek form. Rana Issa describes it as “phonology as a kind of anthropological archaeology,” drawing its information “from the lips of the natives.” '+D('1841_Robinson_Biblical_Researches_v2.pdf')+'.')}. <i>ʿAin Shams is Beth Shemesh.
ʿĀqir is Ekron. Beitin is Bethel. Seilūn is Shiloh. Mukhmās is Michmash.</i>''',
 f"""
{fig(F4.fig_bible_ridge(), 'Every biblical place within a day’s walk, and the village it survived as',
 'The right-hand grade is for <b>the identification</b>, not for the scripture — whether the ground has confirmed the name, merely agrees with it, or is still argued. <b>Nine places, and the furthest is nineteen kilometres from Ramallah.</b> Ramallah is not among them, because Ramallah is not there yet; but al-Bīra next door may be Beeroth, and the ground the town would be built on lay in the middle of all of it.',
 'Robinson &amp; Smith (1841); Pritchard at al-Jib (1956–59); Badè at Tell en-Naṣbeh; Albright and Kelso at Beitin; Marquet-Krause, Callaway and Hani Nur el-Din at et-Tell.')}
<p><b>And at one of these places the ground answered in writing.</b> At <b>al-Jib</b>, six kilometres
from Ramallah, James Pritchard dug between 1956 and 1959 and found <b>more than sixty jar handles
inscribed <span class="he">גבען</span> — Gibeon</b>, in eighth- and seventh-century Hebrew
script{c('James B. Pritchard, <i>Hebrew Inscriptions and Stamps from Gibeon</i> (Philadelphia: University Museum, 1959), and <i>Gibeon: Where the Sun Stood Still</i> (Princeton, 1962). The handles carry the formula <i>gbʿn gdr</i> followed by a personal name. It has been called as strong a site identification as anyone is ever likely to find in biblical archaeology — at the time, only the fourth ancient Palestinian place-name confirmed at its own site by excavated inscriptions.')}. <i>The village had been called al-Jib for as long as anyone could
remember, and the jars in the ground agreed with the villagers.</i></p>
<p><b>One of the nine cuts the other way, and this book prints it as gladly as the rest.</b>
<b>et-Tell</b>, five kilometres east, is biblical <b>Ai</b>, and the Hebrew <i>ha-ʿAi</i> means
<b>“the ruin.”</b> The excavation found exactly that: an Early Bronze town destroyed about 2400 BC,
then empty for more than a thousand years, then an Iron I village built quietly on the abandoned
mound{c('Judith Marquet-Krause (1933–35); Joseph A. Callaway for the American Schools of Oriental Research (1964–70); Hani Nur el-Din, al-Quds University (2005–07). John Garstang trenched the site in 1928. The absence of a Late Bronze town at et-Tell is long-established and much discussed; what is not in doubt is the sequence — Early Bronze town, long abandonment, Iron I village.')}. <i>The name and the ground say the same thing.
Whoever named that hill knew what was on it.</i></p>
<p><b>What this is worth to a family from Ramallah.</b> The landscape of scripture is not somewhere
else. It is the ground between al-Bīra and Ṭaybeh, and the names on it were kept — not in a library,
not by a church, not by a state, but <b>by the people who farmed those hills and went on saying the
words</b>. <i>When this book says the population of this ridge was never replaced, the map of the Bible
is one of the proofs. A replaced people forgets the names.</i></p>"""),

ent('c. 1175–840 BCE', 'attested', False, 'The neighbours: Philistines, Phoenicians, Arameans — and the kingdoms across the Jordan',
 'While the highland villages went on terracing the same slopes, the coast and the plateau filled up with peoples whose names are still in the language: the <b>Philistines</b> at Gaza, Ashkelon and Ashdod; the <b>Phoenicians</b> at Tyre and Sidon; the <b>Arameans</b> inland at Damascus; and across the river <b>Moab, Ammon and Edom</b>. <i>Every one of them was eventually absorbed into the population of this region. Not one of them replaced it.</i>',
 f"""
<p><b>One of these neighbours matters directly to this family.</b> The plateau the tradition names as
its road out — Karak and Shawbak — is ancient <b>Moab</b> and ancient <b>Edom</b>; Karak itself is
generally identified with the Kir of Moab of the Hebrew Bible. And Moab left a document. The
<b>Mesha Stele</b>, cut about 840 BCE and found at Dhībān in 1868, is the longest Iron Age
inscription anyone has recovered from this landscape, written in Moabite — a language so close to
Hebrew that it can be read straight off the stone. <b>And it can be checked against scripture, because
both sides wrote it down.</b> The stele is King Mesha’s account of throwing off Israelite overlordship;
<b>2 Kings 3 is the same war from the other side</b>, and names the same king — <i>“Mesha king of Moab
was a sheep-master”</i>{c('2 Kings 3:4–27, and the Mesha Stele (the Moabite Stone), Louvre AO 5066, found at Dhībān in 1868. The stele names <span class="he">מלך ישראל</span> — the king of Israel — and the god <span class="he">יהוה</span>, the earliest occurrence of the divine name in an inscription outside the Bible. The two accounts agree on the participants and the shape of the conflict and disagree, as one would expect, about who won.')}. <i>Two accounts of one campaign, one on stone and one in scripture, and
each of them the enemy’s version of the other.</i> <i>The plateau the family remembers as a place of
exile has been literate, settled and self-describing for nearly three thousand years.</i></p>
<p><b>And one of them is the control experiment for this whole book.</b> The Philistines arrived
about 1175 BCE carrying a southern-European-related ancestry whose source population is not yet pinned down, and the arrival is visible in the genome at Ashkelon — and then,
within no more than two centuries, the signal is gone. They did not leave. They married the
neighbours. That is what happens in this country to everybody who comes, and it is what happened to
this family too, three thousand years later.</p>""" + fig(R.fig_peoples(),
 'The peoples of this land do not replace one another — they overlap',
 'Each band is a language and an identity, not a population. They run into and over one another for four thousand years, and the genetics now say the population underneath them is largely continuous. <b>Only the Samaritans kept a separate identity to the present; only the Franks genuinely left.</b> The gold line is 1562, the year the family arrives on the ridge — into a landscape that has been continuously inhabited since long before the first band on this chart.',
 'Haber et al. (2017, 2019); Feldman et al. (2019); Agranat-Tamir et al. (2020); Killebrew (2005); the Amarna correspondence; Samaritan census figures.')),

CH(4)

sect('What the ground says', 'Assyria, and the road that already joined the two ends of this story')
ent('745–681 BCE', 'documents', False, 'Assyria writes this landscape down — and a caravan road ties the two ends of this story together',
 'From <b>Tiglath-pileser III (745–727)</b> onward the Assyrian empire records this country in cuneiform: tribute lists, provincial reorganisations, deportations, and Sennacherib’s siege of Lachish carved in relief for the walls of Nineveh{}. <i>The point here is not who paid whom. It is that from the eighth century BCE this landscape is continuously documented by outside powers — and in none of those documents is it ever empty.</i>'.format(c('The Assyrian royal inscriptions of Tiglath-pileser III, Sargon II and Sennacherib; the Lachish reliefs from Sennacherib’s palace at Nineveh, now in the British Museum. Standard editions in the <i>Royal Inscriptions of the Neo-Assyrian Period</i> series.')),
 """
<p><b>And in the same centuries, at the other end of the family’s story, the incense road is
running.</b> Pliny describes it in detail. The frankincense of South Arabia was gathered at
<b>Sabota</b> — Shabwa, in <b>Ḥaḍramawt</b>, one of Joktan’s thirteen sons in the Genesis list this
chart begins with — where a tenth was tithed to the god at a single gate; from <b>Thomna</b>, the
Gebbanite capital, it then went <b>1,487½ miles by camel to Gaza on the Palestinian coast, in
sixty-five stages</b>. He even totals the bill: water, fodder, lodging and tolls came to
<b>688 denarii a camel</b> before a single Roman customs officer was paid{}.</p>
<p><i>This is worth stopping on.</i> More than a thousand years before the dam broke, and more than
two thousand years before Rāshid crossed the Jordan, <b>there was already a permanent, tolled, mapped
commercial road joining the country scripture assigns this family to the country the family now
lives in</b> — and it ended at Gaza, some eighty kilometres south-west of the ridge. The migration the tradition remembers
did not need to invent a route. It only needed to use one that had been open, in both directions,
for the better part of a millennium.</p>""".format(
  c('Pliny, <i>Naturalis Historia</i> XII.63–65: the incense tithed at Sabota (Shabwa) in Ḥaḍramawt, then carried from Thomna, capital of the Gebbanitae, 1,487½ Roman miles to Gaza in sixty-five camel stages, with charges at every halt totalling 688 denarii a camel.'))),

CH(5)

sect('What the ground says', 'Five empires in five centuries, and a village that does not move')
ent('539–63 BCE', 'documents', False, 'Six sovereigns over one ridge, and nobody moves',
 'Cyrus takes Babylon in <b>539</b> and the edict of return is conventionally dated <b>538</b>; Alexander comes in <b>332</b>; then the Ptolemies, the Seleucids, the Hasmoneans — and Pompey in <b>63 BCE</b>. <b>Five changes of sovereign in five centuries, and no change of population.</b> The administrative district around Jifnā that Rome will inherit and Pliny will write down is Hellenistic in origin; Rome did not invent this landscape, it took delivery of it.',
 """
<p>The period leaves ordinary paperwork, which is the best kind of evidence there is. The
<b>Zenon papyri</b> — the working correspondence of an agent of Ptolemy II’s finance minister, who
was travelling through this country in <b>259 BCE</b>, on a tour begun late in 260 — record estates, grain, slaves, wine and olive oil
moving through Palestinian towns, in Greek, as routine commercial business{}. <i>Nobody writes
letters like that about an empty country.</i></p>""".format(
  c('The Zenon archive (P. Cair. Zen.), 261–229 BCE; Zenon’s Palestinian journey of 259 BCE on behalf of Apollonios, dioiketes of Ptolemy II Philadelphus.'))),

ent('5th–2nd c. BCE', 'attested', False, 'The Samaritans, and Mount Gerizim',
 'Magen dates the sanctuary on Gerizim archaeologically to the <b>mid-fifth century BCE</b>, and the dating is disputed; when the separation from Judaism became final is disputed, and the decisive rupture is usually placed at the Hasmonean destruction of the temple there, about <b>110 BCE</b>{}. What is not disputed is the sequel: the Samaritans are <b>still on that mountain</b> — reduced from a Byzantine-era population in the hundreds of thousands to about 150 souls by 1900, and recovering to some 900 today{}. <b>Continuity in this landscape is observable, not rhetorical.</b> <i>And the Gospel sets a conversation on that same mountain — “our fathers worshipped in this mountain, and ye say that in Jerusalem is the place where men ought to worship”</i>{}.'.format(
  c('Y. Magen, <i>Mount Gerizim Excavations</i> I–II (Israel Antiquities Authority, 2004, 2008), for the mid-fifth-century sanctuary — excavated and published by the Staff Officer of Archaeology under the Civil Administration, on a mountain in occupied territory, and cited here for its stratigraphy and not for its frame (see the bibliography, §XXX). The Persian-period date is disputed; Gary Knoppers, <i>Jews and Samaritans: The Origins and History of Their Early Relations</i> (Oxford, 2013), ch. 1, for the range of dates proposed — from Ezra to 70 CE; Josephus, <i>Antiquitates</i> XIII.255–56, for John Hyrcanus and the destruction of the Gerizim temple. <b>Earlier editions of this book printed a flat “c. 400 BCE,” which no source supports.</b>'),
  c('On Samaritan demographic history: the Byzantine-era revolts of 484, 529 and 555 and the collapse that followed; census counts of 163 (1922) and 182 (1931); c. 900 today at Holon and Kiryat Luza.'),
  c('John 4:20, the Samaritan woman at the well near Sychar; the well itself is at Bālāṭa outside Nablus, at the foot of Gerizim, and the mountain in the verse is the one this entry is about. <b>The dispute the verse records is the one the archaeology dates.</b>'))),

CH(6)
sect('What the ground says', 'Rome paves the ridge, ranks the district, and writes its villages down')
ent('63 BCE → 77 CE', 'documents', False, 'Rome writes the district down — and ranks it second',
 'Pompey takes Judaea from the Hasmoneans in 63 BCE, and a century and a half later the empire has the place on paper. Pliny lists <b>Gophna</b> — Jifnā, about seven kilometres due north of the ridge — among the ten toparchies of Judaea; Josephus calls it <b>“the second of those cities”</b> after Jerusalem itself{}.'.format(c('Pliny, <i>Naturalis Historia</i> V.70; Josephus, <i>Bellum Judaicum</i> III.54–55; also IV.551 (Vespasian takes the toparchy, 68 CE), V.50 and VI.115.')),
 f"""
{fig(ATLAS.fig_roman(),'The district when Rome wrote it down',
 'Ramallah’s neighbours in the Roman and Byzantine record, with the imperial road that runs the length of this ridge. Every green dot is named in a surviving text. The gold circle is the site of Ramallah — named in none of them, and in none at all until 1279.',
 'Pliny, NH V.70; Josephus, BJ III.54–55; Eusebius, Onomasticon; the Madaba mosaic; Tappy, NEA 75 (2012); al-Houdalieh on Khirbet et-Tireh.')}
<p>The hills the family would one day reach were not a wilderness. They were an imperial district
with a paved highway down the middle — the road from Aelia Capitolina to Neapolis, milestoned and
measured, which Eusebius later used as his surveyor’s baseline: Bethel, he writes, is <i>“twelve
miles from Jerusalem, to the right of the road going to Neapolis.”</i>{c('Eusebius, <i>Onomasticon</i>, s.vv. Baithel, Silo; ed. Klostermann (1904); Notley &amp; Safrai (Brill, 2005). The road’s milestones catalogued by Thomsen, <i>ZDPV</i> 40 (1917).')} <b>When the family
walks up this ridge in 1562, and when the first emigrants ride down it in 1901, they are using a
road Rome paved.</b> Two kilometres from the future town centre, Khirbet et-Tireh — two churches, a
monastery, an oil press, excavated by Salah al-Houdalieh — shows the ground itself was worked and
prayed on for some seven hundred years, from the Roman period onward{c('Salah al-Houdalieh (al-Quds University), excavations at Khirbet et-Tireh from 2013 — two contemporaneous churches, a monastery and an oil press, two kilometres west of the present town centre; the settlement covers some thirty thousand square metres. Hamdan Taha at ʿAbūd. See the bibliography, §XVIII and §XXIX. <b>Two corrections here. Earlier editions said “a thousand years before the founding,” which implied an unbroken occupation the excavation does not show. And earlier editions said the site was abandoned after the earthquake of 749 and reoccupied only in the Ottoman period — al-Houdalieh’s own publication of the press says the opposite: “we believe that the press facility itself was maintained in continuous use from the Byzantine through the late Ottoman periods.” The 749 abandonment is withdrawn.</b> Salah Hussein al-Houdalieh, “The Oil Press Complex of Khirbat al-Tira,” <i>Jerusalem Quarterly</i> 62 (2015), 84–96.')}. <i>Only the name Ramallah is missing from
every text — the neighbours are Roman, the ground is Byzantine, the name will be Mamluk.</i></p>"""),

ent('c. 30 CE', 'documents', False, '“A city called Ephraim, and there continued with his disciples”',
 'John 11:54. The city is generally identified with <b>Ṭaybeh, eleven kilometres from Ramallah</b>{} — still, today, the last entirely Christian town in Palestine.'.format(c('John 11:54: <span class="gk">εἰς Ἐφραὶμ λεγομένην πόλιν</span>. The identification with eṭ-Ṭaybeh is standard from Robinson (1841) and the <i>Survey of Western Palestine</i>, resting on Eusebius and the villagers’ retained memory of the older name; Albright preferred ʿAyn Sāmiya.')),
 f"""
<blockquote><span class="gk">Εφρων ἡ Εφραια ἔνθα ἦλθεν ὁ Κ(ύριο)ς</span><br>
“Ephron, also Ephraia, <b>where the Lord went.</b>”
<span class="cite">The Madaba mosaic map, sixth century — the caption still in the church floor at
Madaba{c('Avi-Yonah, <i>The Madaba Mosaic Map</i> (1954), no. 41; Donner no. 43; Piccirillo no. 44.')}</span></blockquote>
<p>And the road he used is this road. Josephus: <b>“It was the custom of the Galileans, when they
came to the holy city at the festivals, to take their journeys through the country of the
Samaritans”</b>{c('Josephus, <i>Antiquitates</i> XX.118; cf. <i>BJ</i> II.232. The Gospels assume both routes: Luke 9:51–53 and John 4:3–5 the ridge, Mark 10:1 the Jordan valley.')} — the ridge route, past the site of Ramallah. Over the following three or four centuries the
country became largely Christian without anybody moving — by conversion, not replacement, and with
Jewish and Samaritan communities remaining throughout; in 451 Jerusalem became a Patriarchate at Chalcedon,
and the church this family still belongs to acquired the form it still has{c('The see of Jerusalem elevated to patriarchal rank at the Council of Chalcedon, 451; on the continuity of its structures through the early Islamic period, Milka Levy-Rubin, <i>ARAM</i> 15 (2003).')}.
<b>This family’s faith is not something that arrived with it in 1562. It was already here — and it
is one of the things that never left.</b></p>"""),

ent('c. 27–30 CE', 'scripture', False, 'THE ROADS HE USED — and every Gospel place within a day of this hill',
 f'''The Gospels are not set <i>near</i> this district. <b>They are set in it.</b> Put every place they name at its real coordinates and the whole of it fits inside a day’s walk of the hill Ramallah would be founded on fifteen centuries later — Jerusalem at fourteen kilometres, Bethany at fifteen, Jericho at twenty-three, and <b>Ephraim at eleven</b>{c('Distances are great-circle measurements from the centre of present-day Ramallah (31.8996° N, 35.2042° E) to the accepted site of each place. Every distance printed on a plate in this book is now computed from that point and the site’s own plotted coordinates, so a label cannot drift away from the dot it belongs to. <b>Earlier editions printed eṭ-Ṭaybeh at twelve kilometres throughout; the measurement is 10.7, and the book now prints eleven.</b>')}.''',
 f"""
{fig(F4.fig_jesus_road(), 'The roads he used, and the ridge they run along',
 'Left, the country: the two roads between Galilee and Jerusalem, and where this ridge sits on one of them. Centre, the district within a day’s walk. Right, what the Gospels say is at each place. <b>Every marker is graded on the identification of the site, never on the verse.</b> Green is named in the Gospels at a securely identified place; grey is named in the Roman record but not in the Gospels; the dashed violet rings are medieval pilgrim tradition, printed and labelled as tradition.',
 'John 11:54; Luke 2:41–46, 10:30, 19:1, 24:13; Josephus, Ant. XX.118 and BJ IV.550–51, VI.113–15; Robinson &amp; Smith (1841); Pringle, Churches of the Crusader Kingdom.')}
<p><b>Start with the road, because the road is the part that is certain.</b> There were two ways
from Galilee to Jerusalem: down the Jordan valley and up through Jericho, or straight down the
watershed through Samaria. Josephus says plainly which one Galilean pilgrims used — <i>“It was the
custom of the Galileans, when they came to the holy city at the festivals, to take their journeys
through the country of the Samaritans”</i>{c('Josephus, <i>Antiquitates</i> XX.118; the same episode at <i>BJ</i> II.232. The Gospels assume both routes are available: Luke 9:51–53 and John 4:3–5 take the ridge, Mark 10:1 the valley.')}
— and the watershed road runs along the top of this ridge, within sight of the future town, and was
paved and milestoned by Rome{c('Eusebius uses the Jerusalem–Neapolis road as his surveyor’s baseline in the <i>Onomasticon</i>, locating Bethel “twelve miles from Jerusalem, to the right of the road going to Neapolis”; the milestones were catalogued by Thomsen, <i>ZDPV</i> 40 (1917).')}. <b>Three times a year — Passover, Pentecost, Tabernacles —
the pilgrim traffic of Galilee came down past this hill.</b> That is not a devotional claim. It is a
road, a custom recorded by a hostile witness, and a milestone count.</p>
<p><b>Now the one town on this ridge the Gospels actually name.</b> John says that when it became
unsafe for him near Jerusalem he <i>“withdrew to a city called Ephraim, in an area near to the
wilderness, and there continued with his disciples”</i>{c('John 11:54: <span class="gk">εἰς Ἐφραὶμ λεγομένην πόλιν</span>. The identification with eṭ-Ṭaybeh is standard from Robinson (1841) and the <i>Survey of Western Palestine</i>, and is supported by the sixth-century Madaba mosaic, which captions the place <span class="gk">Εφρων ἡ Εφραια ἔνθα ἦλθεν ὁ Κ(ύριο)ς</span> — “Ephron, also Ephraia, where the Lord went.”')}. <i>Look at where eṭ-Ṭaybeh
sits on the map.</i> It is on the last inhabited edge of the ridge; east of it the land falls away
into the wilderness of the Jordan rift. <b>The verse is not describing a place vaguely. It is
describing this place accurately</b> — a town at the end of the settled country, with the desert
starting at its feet, which is exactly what a man withdrawing from Jerusalem would want. <i>And it is
still, today, the last entirely Christian town in Palestine.</i></p>
<p><b>Two more places on this map belong to the neighbours rather than to the evidence, and this book
prints them as such.</b> At <b>al-Bīra</b> — one and a half kilometres from the centre of Ramallah —
there is a Crusader church, in the record by 1128 and described by the German pilgrim Theodoric in
1172; by the fourteenth century the Latins held that this was the day’s-journey halt of Luke 2:44,
where Mary and Joseph discovered the boy was not with the company{c('On the church of St Mary at al-Bīra: in the record from September 1128 under the jurisdiction of the Holy Sepulchre, and described by Theodoric in 1172; a Romanesque basilica of roughly 22 × 35 metres. The Holy Family association is attested from the fourteenth century. See Denys Pringle, <i>The Churches of the Crusader Kingdom of Jerusalem</i>, s.v. al-Bīra; and the Palestinian Ministry of Tourism and Antiquities site record. <b>The identification of al-Bīra with the Beeroth of Joshua 9:17 is Robinson’s and remains disputed; the Holy Family association is later still, and rests on nothing earlier than the Crusader period.</b>')}. At <b>al-Qubeiba</b>,
nine kilometres to the south-west, there is a Crusader village and a fort called <i>Castellum
Emmaus</i>; pilgrims began calling it the Emmaus of Luke 24:13 in the thirteenth century and the
Franciscans adopted it in 1335{c('Al-Qubeiba is one of four candidates for Emmaus, with ʿImwās/Nicopolis, Abū Ghōsh and Moẓa/Qālūniya. The choice turns partly on a manuscript split at Luke 24:13 — sixty stadia in most witnesses, a hundred and sixty in Sinaiticus and others — which suits Nicopolis at roughly 160 stadia and al-Qubeiba at about 65. Franciscan pilgrimage from 1335; excavated by Bellarmino Bagatti, 1940–44.')}. <b>Neither is evidence about the first century, and this
book does not pretend otherwise.</b> <i>What they are evidence of is something else, and worth
saying: for eight hundred years the people living beside this ridge have believed the Gospel happened
at their own door.</i> That belief is itself a dated, documented, physical fact — it has a church
with foundations. The book grades the two of them violet and dashed, and leaves the reader to weigh
them.</p>"""),

ent('c. 30 CE', 'documents', False, 'AND WHAT THIS RIDGE WAS DOING WHILE HE WALKED IT',
 f'''A tax district, a highway and a harvest. <b>The people on these hills in the year of the Gospels were villagers of the Gophna toparchy</b> — one of the ten administrative districts of Judaea, with its capital at Jifnā, six and a half kilometres from the future town{c('Pliny, <i>Naturalis Historia</i> V.70, listing Gophna among the ten toparchies of Judaea; Josephus, <i>BJ</i> III.54–55, where Gophna heads the list after Jerusalem. The toparchy is Hellenistic in origin and was inherited, not invented, by Rome.')} — growing olives and vines on terraces their grandparents had built, pressing oil, and paying it to Rome.''',
 f"""
<p><i>This is the honest shape of the answer, and the honesty matters more than the answer.</i>
<b>We cannot name one person who stood on Ramallah’s own hill in AD 30.</b> There is no Ramallah yet;
the excavations at Khirbet et-Tireh, two kilometres away, show the ground was worked and prayed on
from the Roman period onward, but no text names a soul on it{c('Salah al-Houdalieh’s excavations at Khirbet et-Tireh, from 2013: two contemporaneous churches, a monastery and an oil press, in use from the Roman period until the earthquake of 749. The Roman-period phase is the relevant one here; the churches are later.')}. <b>What can be named is
everything around a person</b> — the district, the road, the crop, the press and the tax. That is
more than most families can say about their ground in any century, let alone the first.</p>
<p><b>The terraces are the strongest single piece of it.</b> They are the same system this book has
already described: dry-stone walls with no mortar of any kind, built to hold soil and water on a
slope, and worked continuously for so long that no one can date their beginning{c('On the dry-stone technique and its continuity: Shadi Ghadban, “Palestinian Dry Stone Structures — An Endogenous Expression of Cultural Landscape,” <i>Journal “Sustainable Development, Culture, Traditions”</i> 1b (2015), 34–46.')}. <i>The
terraces on the hills he walked through are the terraces the family would one day farm.</i> Nobody
rebuilt this landscape between the two dates. It was maintained, wall by wall, by whoever was living
on it.</p>
<p><b>And the road was busy, and dangerous.</b> Josephus records a Galilean pilgrim murdered at the
Samaritan village of Ginae on his way up to a festival, and the reprisals and Roman hearings that
followed — an episode that is only intelligible if the ridge route carried heavy, regular,
mixed traffic{c('Josephus, <i>Antiquitates</i> XX.118–136; <i>BJ</i> II.232–246. Under the procurator Cumanus, c. 51 CE. The affair reached the emperor Claudius.')}. <i>Whoever was farming this ridge in the first century
was not living in a backwater. They were living on the main road, watching the whole country walk
past their terraces three times a year.</i></p>"""),

ent('69 → 70 CE', 'documents', False, 'AND AFTER — the two towns garrisoned, and the priests held six kilometres away',
 f'''When Rome came back to settle the revolt, it came up this road, and Josephus names the stops. Vespasian <i>“went up to the mountainous country, and took those two toparchies that were called the Gophnitick and Acrabattene”</i>; and then — the sentence that ought to stop a reader of this book — <b><i>“after which he took Bethel and Ephraim, two small cities; and when he had put garrisons into them, he rode as far as Jerusalem.”</i></b>{c('Josephus, <i>BJ</i> IV.550–551 (Whiston IV.9.9), the campaign of AD 69. Bethel is Beitin, 4.4 km from Ramallah; Ephraim is eṭ-Ṭaybeh, twelve. The same march has Cerealis sent against upper Idumaea, where he stormed and burned Hebron.')}''',
 f"""
<p><b>Read those two names together.</b> Bethel and Ephraim: the town of Jacob’s ladder and the town
John says he withdrew to — <b>four kilometres and eleven kilometres from the centre of the present
Ramallah</b> — are the two places the Roman army thought worth garrisoning on its way to besiege
Jerusalem. <i>The Gospel geography and the Roman military geography of this ridge are the same
geography.</i> They are the same small towns, on the same road, forty years apart.</p>
<p><b>Then the district is used one more time, and it is the most human detail in the whole
chapter.</b> During the siege, Titus took the surrender of a group of Jerusalem’s notables — among
them the high priests <b>Joseph and Jesus</b>, and the sons of leading families — and <i>“sent them
to Gophna, and desired them to remain there for the present,”</i> promising that when the war was
over he would restore every man his property. The rebels inside the city then put about that the
Romans had butchered them, to stop anyone else deserting; so Titus <b>brought the same men back from
Gophna and walked them round the walls with Josephus, alive, where the defenders could see
them</b>{c('Josephus, <i>BJ</i> VI.113–115 (Whiston VI.2.2). Gophna is Jifnā, 6.7 km from the centre of Ramallah.')}.</p>
<p><i>So in the summer of AD 70, the surrendered priesthood of Jerusalem was being housed in a
village six and a half kilometres from a hilltop that had no name yet.</i> <b>This is what the ridge
was doing after his life: it was the last stage of the road to Jerusalem, and then it was the place
Jerusalem’s survivors were put.</b></p>
<p><b>And then — nothing happens to the population.</b> The villages of the Gophna toparchy are not
destroyed and not emptied; the terraces are not abandoned; the same names go on being used. Within
three centuries these hills are Christian, and the entry that follows shows it happened
<b>by conversion, not by replacement</b>. <i>The people who watched the pilgrims pass in AD 30, and
who watched the legions pass in AD 69, are the people who were still on this ridge when
sixty-four Christian households walked up it in 1562.</i></p>"""),

CH(6)

sect('And in our own line', 'The name enters at a spring in Yemen — four thousand miles from this ridge')
ent('c. 250 → c. 350', 'documents', False, 'THE NAME, IN STONE — Ghassān in two Sabaic inscriptions',
 'Everything the family carries hangs on one word, and until now this book took that word entirely from the Arabic genealogists, writing five hundred years after the fact. <b>It does not have to.</b> Ghassān is named twice in South Arabian inscriptions cut while the Jafnids were still unheard of{}.'.format(c('<b>ʿInān 75</b>, mid-third century AD, recording an embassy to “the kings of the peoples (<span class="ar">أشعب</span>) of Ghassān, al-Asd, Nizār and Madhḥij”; <b>ʿAbadān 1</b>, roughly a century later, on a Ḥimyarite campaign “between the land of Nizār and the land of Ghassān.” Both in the Sabaic corpus; see the DASI database (Università di Pisa / CNR) and the discussion in Christian Julien Robin’s work on the Arab peoples of the pre-Islamic peninsula.')),
 f"""
<p><b>ʿInān 75</b>, from the middle of the third century AD, records a Sabaean embassy sent to
<i>“the kings of the peoples of <b>Ghassān</b>, al-Asd, Nizār and Madhḥij.”</i> <b>ʿAbadān 1</b>,
about a century later, has a Ḥimyarite army campaigning <i>“between the land of Nizār and the land of
<b>Ghassān</b>.”</i> In both, Ghassān is a <i>shaʿb</i> — a large territorial grouping with kings of
its own — and in both it is placed in <b>western Arabia</b>, out of Yemen and on the road north.</p>
<p><i>This is the single most useful thing this project has found about the name.</i> It does not
prove any family’s descent and it never could. <b>What it proves is that “Ghassān” was a real,
sizeable, politically organised people, named by outsiders, on stone, before any Arabic genealogist
wrote a word about it.</b> The tradition the family inherited is not describing a literary invention.
It is describing something that existed.</p>
<p><b>And now the disagreement, printed as this book prints disagreements.</b> The classical
authorities all say Ghassān is a water rather than a man — and then give <b>four incompatible
locations for it</b>: between Rimaʿ and Zabīd in the Yemeni Tihāma (Ibn al-Kalbī, the oldest and
best-supported); at the Maʾrib dam itself (Ibn Hishām); at al-Mushallal near al-Juḥfa, on the
Mecca–Medina road; and one report that it is not a place at all but an animal that fell into a
water{c('Yāqūt al-Ḥamawī, <i>Muʿjam al-buldān</i>, s.v. <span class="ar">غسان</span>, who assembles the variants: Ibn al-Kalbī via Ibn Ḥabīb and Naṣr al-Iskandarī for Rimaʿ/Zabīd; Ibn Hishām (d. 218/833) for the dam at Maʾrib; an anonymous <i>wa-yuqāl</i> for al-Mushallal near al-Juḥfa; and a <i>wa-qīla</i> that the water was named after an animal that fell into it. The three geographical variants are hundreds of kilometres apart and mutually exclusive; none of the authorities had independent evidence.')}. <b>They also disagree about who is entitled to the name</b>: Yāqūt includes the Anṣār of
Medina, Ibn Ḥazm expressly excludes them and admits only four sons of ʿAmr Muzayqiyāʾ, and al-Samʿānī
rules out Khuzāʿa, Aslam, Bāriq and the Azd of Oman on the ground that they did not drink{c('Yāqūt, s.v. <span class="ar">غسان</span>, for the Banū Māzin b. al-Azd “who are the Anṣār,” with Banū Jafna and Khuzāʿa; Ibn Ḥazm, <i>Jamharat ansāb al-ʿArab</i>, admitting only al-Ḥārith, Jafna, Mālik and Kaʿb, the four sons of ʿAmr Muzayqiyāʾ, and excluding the Anṣār; al-Samʿānī, <i>al-Ansāb</i>, s.v. al-Ghassānī, following Ibn al-Kalbī in excluding Khuzāʿa, Aslam, Bāriq and Azd ʿUmān.')}.
<i>Even the medieval genealogists could not agree on who was entitled to be called Ghassānī.</i></p>
<div class="fix"><div class="fixhead">A trap this book will not fall into</div>
<div style="font-size:.95rem;line-height:1.65;color:#46423B">
<p style="max-width:none"><b>The written form <span class="ar">الغساني</span> is not, by itself,
evidence of Ghassanid descent — and it was not in the classical period either.</b> Al-Samʿānī’s own
entry on the nisba contains three separate traps on the same pages: <b><span class="ar">الغُساني</span></b>
with a <i>ḍamma</i> is a different nisba altogether, to a clan of Ḥaḍramawt; <b>al-Ghassāniyya</b> is
a Murjiʾī theological sect of Kufa named after some man called Ghassān; and at least one famous
bearer, Ibrāhīm b. Ṭalḥa, is simply <i>named after a great-grandfather who happened to be called
Ghassān</i>. Unvocalised manuscripts do not distinguish any of these{c('Al-Samʿānī, <i>al-Ansāb</i>, s.v. <span class="ar">الغساني</span>: <span class="ar">الغُساني</span> with <i>ḍamma</i>, to Ghassān b. Judhām b. al-Ṣadif, a <i>baṭn</i> of Ḥaḍramawt, on the authority of al-Dāraquṭnī; al-Ghassāniyya, the Murjiʾī sect of Kufa; and Ibrāhīm b. Ṭalḥa, <span class="ar">نُسب إلى جدّه الأعلى</span>, “named after his great-grandfather.” Ibn Ḥibbān moreover calls Yaḥyā b. Yaḥyā al-Ghassānī a <i>Kindī</i>.')}.</p>
<p style="max-width:none"><i>So when this family’s oldest named ancestor is written </i>Rāshid
al-Ḥaddādīn al-Ghassānī<i>, the last word is a claim, not a proof — and this book has said from the
beginning that the claim is a claim.</i> <b>What the inscriptions add is that the thing being claimed
was real.</b></p></div></div>"""),

ent('c. 260–280', 'documents', False,
    'A MAN WALKED THIS ROAD AND HAD IT CARVED — twelve lands, from the Azd to Ghassān',
 f'''There is a third inscription, published in 2016, and no earlier edition of this book knew about
it. In a dedication to <b>Taʾlab Riyām</b> — the god of the tribes of Ḥashid and Ḥumlān — the authors
thank him for bringing their steward home <i>“from the land of the North,”</i> and then list, in
order, every land the man crossed: <b>Asd, Nizār, Tanūkh, Liḥyān, Tadmur, Nabaṭ, Rūmān, Lakhm,
Ghassān, Maʿadd, Ṭayyiʾ, Khaṣaṣat</b>{c('Riyam 2006-17, from the village of Riyām in the Yemeni highlands, published by Jérémie Schiettecatte &amp; Mounir Arbach, “The political map of Arabia and the Middle East in the third century AD revealed by a Sabaean inscription,” <i>Arabian Archaeology and Epigraphy</i> 27:2 (2016), 176–196, DOI 10.1111/aae.12071. The text is one of a group of ten dated to the first–third century AD on palaeographic grounds; the authors place this one in the third century, probably c. 260–280. Lines 15–20 carry the list of lands. '+D('2016_Schiettecatte_Arbach_Political_Map_of_Arabia_3rd_c_AAE_27.pdf')+'.')}. <i>It is an itinerary, cut into stone, by somebody who had
just walked it.</i>''',
 f"""
{fig(F4.fig_riyam_road(), 'Twelve lands, in the order he crossed them',
 'The stops are the inscription’s own, in the inscription’s own order. <b>The land of the Azd is the first; the land of Ghassān is the ninth</b>, and between them lie Palmyra, the Nabataeans, Rome and Lakhm — the whole northern client system, seen from Yemen and named in Sabaic. The two green stops are the two names the family’s tradition depends on, and in the third century AD they are not in the same place.',
 'Riyam 2006-17, lines 15–20; Schiettecatte &amp; Arbach, <i>Arabian Archaeology and Epigraphy</i> 27 (2016), 176–196.')}
<p><b>Three things this is worth to a family history, and one caution.</b></p>
<p><b>First, Ghassān has a position.</b> Not a genealogy, not an eponym, not a water somewhere in the
Tihāma — <i>a place in a sequence of places</i>, between Lakhm and Maʿadd, listed by a man who had
been there. The name our own chart hangs on turns out to be a piece of third-century political
geography.</p>
<p><b>Second, the Azd and Ghassān are two different stops.</b> Stop one and stop nine, with eight
lands between them. Whatever relation the genealogists later drew between al-Azd and Ghassān, in the
third century a Sabaean envoy crossed one, then crossed seven other territories, and then crossed the
other.</p>
<p><b>Third, the road in this inscription is the road this whole book is about.</b> Palmyra, the
Nabataeans, Rome, al-Ḥīra — and the Nabataean land he names is <i>this country</i>. The route from
Yemen to the Roman frontier was open, known, walkable and worth carving in the third century AD,
which is precisely the period the family’s tradition has its ancestors taking it.</p>
<p><i>And the caution, because this book prints them.</i> <b>The list is not certainly a step-by-step
route.</b> It may be a register of lands reached rather than an ordered march, and the editors say so;
Rome, Palmyra and the Nabataeans in sequence make geographical sense, Tanūkh in lower Mesopotamia at
position three does not. <b>The dating is palaeographic, not absolute.</b> What the stone fixes beyond
argument is not the itinerary but the <i>inventory</i>: these twelve lands existed, under these names,
and a Sabaean government knew all of them.</p>"""),
ent('c. 250–500', 'classical', 'shared', 'The name in the water: Ghassān moves north',
 'The dominant tradition is that Ghassān is not a man but <b>a water</b>. Ibn al-Kalbī: <span class="ar">وإنّما غسّان ماء شربوا منه فسُمّوا به</span> — <b>“Ghassān is simply a water they drank from, and so were named after it”</b> — and he places it between Zabīd and Rimaʿ, in the Tihāma of Yemen{}. <i>The sources are not unanimous about where the water was, or whose sons drank there.</i>'.format(c('Ibn Durayd (d. 933), <i>al-Ishtiqāq</i>, s.v. Ghassān; Ibn al-Kalbī (d. 819) locates the water between Zabīd and Rimaʿ: <span class="ar">إنما غسان ماء شربوا منه فسُمّوا به</span>. '+D('0819_Ibn_al-Kalbi_Jamharat_al-nasab.pdf')+'.')),
 f"""
{fig(ATLAS.fig_road(),'The road, and the ground it passes',
 'Yemen to the Levant: the migration the tradition remembers, over the country the classical geographers describe. The chart’s generations 15–29 travel this map; at generation 29, with ʿAmr Muzayqiyāʾ, the name Al-Ghassānī enters — exactly where the classical sources put the naming at the spring.',
 'al-Hamdānī, Ṣifat Jazīrat al-ʿArab; Ibn al-Kalbī; al-Masʿūdī; the chart, generations 15–29.')}
<p>Both key texts carry this stretch — the chart names the generations, Shāhīn tells the
migration — and the classical scholars supply the system it fits{c('The Azdī pedigree (al-Azd → Māzin → … → ʿAmr Muzayqiyāʾ → Jafna) in al-Suwaydī, <i>Sabāʾik al-dhahab</i>, tabulated by Wüstenfeld (1852–53); the identification Joktan = Qaḥṭān stated by al-Ṭabarī c. 915 — a harmonisation with Genesis 10, made a thousand years before this family repeated it. <b>It is not the load-bearing joint of Qaḥṭānī genealogy</b> — the Arabic tradition runs Qaḥṭān through Yaʿrub and Hūd without needing Joktan at all — so removing it costs the chart nothing.')}. Three of that tradition’s
greatest authorities draw Ghassān’s boundary in three different places — Ibn al-Kalbī wide, Ibn Ḥazm
narrow, Ibn Durayd narrower still — and Ibn Khaldūn, the sharpest critic the tradition ever
produced, warns that the memory of a common ancestor beyond a few generations is an assertion, not a
knowledge{c('Ibn Ḥazm, <i>Jamharat ansāb al-ʿArab</i>, at only the four sons of ʿAmr Muzayqiyāʾ who drank; Ibn Khaldūn, <i>Muqaddimah</i>, Book One, ch. 2 — naming this branch. '+D('1064_Ibn_Hazm_Jamharat_ansab_al-Arab.pdf')+'.')}. <b>This does not weaken the claim so much as change its kind</b>: Ghassanid identity
was never a bloodline out of one man; it was a people who arrived somewhere and were named for it —
which is exactly the sort of thing a family that walked from Karak to a ridge should recognise.</p>"""),

CH(7)

sect('What the ground says', 'The hills turn Christian, and stay that way')
ent('324 → 638', 'attested', False, 'The hills become Christian — and simply stay that way',
 'Within three or four centuries of the road through Ephraim the country is overwhelmingly Christian, and it happened <b>mostly by conversion rather than by replacement</b> — though Samaritan Samaria and Jewish Galilee remain, and the Samaritan revolts of 484, 529 and 555 are fought within sight of this ridge. Palestine in the Byzantine centuries reaches a density of population it will not regain until the twentieth century, and the ridge north of Jerusalem fills with village churches, monasteries and oil presses{}.'.format(c('On the Byzantine demographic peak and the density of rural churches on this ridge: Piccirillo, <i>The Mosaics of Jordan</i> and the Madaba map corpus; al-Houdalieh’s excavations at Khirbet et-Tireh (from 2013); Hamdan Taha at ʿAbūd. See the bibliography, §XVIII and §XXIX.')),
 """
<p>The evidence is in the ground within walking distance of the future town. <b>Khirbet et-Tireh</b>,
two kilometres from the present town centre, has two churches, a monastery and an oil press.
<b>ʿAbūd</b>, about eighteen kilometres north-west, has a church old enough that its rebuilding in 1058 is
itself a dated medieval event. <b>Ṭaybeh</b> — the Ephraim of John 11:54 — has its Byzantine church
still standing in ruin. And the great mosaic map laid in the church floor at <b>Madaba</b> in the
sixth century labels this district with the confidence of an administrator working from an official
list.</p>
<p><i>This is the single most important fact about the ground the family will settle on.</i> When
sixty-four Christian households come up the ridge road in 1562, <b>they are not bringing
Christianity to these hills. They are joining a Christian population that has been in this district,
continuously, since before Arabic was the language of it.</b> The family’s faith is the oldest thing
about this story that can be verified without reference to any genealogy at all.</p>"""),

CH(7)
sect('And in our own line', 'The water fails, the dynasty is already north, and a Greek historian writes one of them down')
ent('455 → c. 575', 'documents', 'shared', 'THE DAM BREAKS',
 'The tradition dates the family’s departure from Yemen to the bursting of the dam “about 300 AD.” <b>The dam’s failures are dated, and they are later:</b> a breach repaired under Sharaḥbiʾīl Yaʿfur in <b>455</b>, a further breach in <b>542/543</b>, the great breach of <b>547</b> repaired in <b>548</b>, and a last recorded restoration in <b>557/558</b>{}.'.format(c('Norbert Nebes, “A New ʾAbraha Inscription from the Great Dam of Mārib,” <i>Proceedings of the Seminar for Arabian Studies</i> 34 (2004), 221–30, esp. 223–24. CIH 540, Sharaḥbiʾīl Yaʿfur’s rupture-and-repair text, is dated Himyarite year 565 = <b>AD 455</b> on the 110 BC epoch Nebes uses; the figure of 449–450 printed in earlier editions of this book reflects the older 115 BC epoch and <b>contradicts the very study cited beside it</b>. CIH 541 records the breach of 657 HE (547) repaired in 658 HE (548). '+D('2004_Nebes_New_Abraha_Inscription_Marib_Dam.pdf')+'.')),
 f"""
<p>We know this in extraordinary detail, because the last great repair left <b>an inscription</b>.
In 548 the Ethiopian-born king <b>Abraha</b> cut into the stone a record of the work: the breach, the
levies raised, the tribes summoned to labour, and a plague that struck the workforce. <i>In a separate
passage of the same stone</i> he records the delegations he received at Maʾrib — from <b>Aksum</b>,
Byzantium, Persia, and the Arab kings of al-Ḥīra and Ghassān{c('CIH 541, the Abraha inscription of 548 — 136 lines, one of the longest pre-Islamic Sabaic inscriptions known. The dam repair occupies lines 55–61 and 92–117; the diplomatic reception is a distinct episode at lines 87–92, after Abraha’s campaigns and his return to Maʾrib. <b>Earlier editions of this book said the embassies came to witness the repair, and omitted Aksum — the first delegation named, and the one Abraha himself came from.</b> Christian Julien Robin, “Abraha and Ethiopia,” in S. F. Johnson (ed.), <i>The Oxford Handbook of Late Antiquity</i> (2015), 247–332, at 292.')}. <i>It is a maintenance
report, carved in stone, from the collapse of the world this family says it came from.</i></p>
<p>The Qurʾān records the same catastrophe from the other side — as the end of a people’s
prosperity: <b>“they turned away, and We sent against them the flood of al-ʿArim”</b>, the flood of
the dam, and the two gardens became gardens of bitter fruit{c('Qurʾān 34:16: <span class="ar">فَأَعْرَضُوا فَأَرْسَلْنَا عَلَيْهِمْ سَيْلَ الْعَرِمِ</span> — “the flood of al-ʿArim,” generally understood as the dam or its embankment.')}. And it draws the moral that
became a proverb, and then a genealogy: <b>“We made them tales, and scattered them utterly.”</b>{c('Qurʾān 34:19: <span class="ar">فَجَعَلْنَاهُمْ أَحَادِيثَ وَمَزَّقْنَاهُمْ كُلَّ مُمَزَّقٍ</span>. The Arabic proverb <i>tafarraqū aydī Sabaʾ</i> — “they scattered like the people of Sabaʾ” — is still current.')}</p>
{FIX('The family left Yemen “about 300 AD,” when the dam broke.',
 'The dam’s dated failures are <b>455, 542/543 and 547–548</b>, with a last recorded restoration in 557/558 and abandonment conventionally placed at <b>570 or 575</b>. The migration tradition stands; the century attached to it moves forward by some 250 years.',
 'Abraha’s repair inscription of 548 (CIH 541) fixes the mid-sixth-century breach absolutely. <b>The final failure is fixed by nothing:</b> every South Arabian text about the dam is a repair text, the last dated 557/558, and the conventional 570 or 575 rests on later Arabic tradition, not on epigraphy or excavation. This book prints that rather than the confident “c. 575–580” of earlier editions. <b>This correction costs the story nothing and gains it everything:</b> moved forward, the departure lands in exactly the century when the family’s claimed dynasty was at its height on the Roman frontier — which is where the next entries find them.')}
{fig(R.fig_dam(),'The dam, and a date that has to move',
 'The tradition’s “about 300 AD” against the dated breaches. A correction, not a demolition.',
 'Nebes, PSAS 34 (2004); CIH 541; the family tradition in both key texts.')}"""),

ent('c. 250 against 455', 'documents', False,
    'THE DAM CANNOT HAVE SENT THEM NORTH — the tradition tested against this book’s own best evidence',
 f'''The tradition’s chain has three links: the dam failed, the Azd scattered, Ghassān went north. The
entry above dates the first link. Two entries in the era before this one date the last. <b>They do not fit, and
this book has printed both without ever setting them side by side.</b> Ghassān is named as a people
with kings of its own in <b>ʿInān 75, in the middle of the third century AD</b>, and again about a
century later in <b>ʿAbadān 1</b> — both times in western Arabia, out of Yemen and on the road north. And in
<b>Riyam 2006-17</b>, cut around 260–280, a Sabaean envoy crosses the land of the Azd as his first
stop and the land of Ghassān as his ninth. The dam’s first dated breach is <b>455</b>. <i>On the evidence this book itself assembled, Ghassān was in the
north at least two hundred years before the water failed.</i>''',
 f"""
<p><b>There are three ways out of this, and only one of them survives contact with the stones.</b></p>
<p><b>One: the inscriptions name a different Ghassān.</b> They do not. Same name, same region, same
road, and no competing candidate anywhere in the South Arabian corpus. This is the weakest escape and
it should be named only to be closed.</p>
<p><b>Two: 455 is merely the first breach anyone wrote down.</b> This is fair, and partly true — the
dam had been maintained for a thousand years and every South Arabian text about it is a repair text.
But a maintenance record is not a catastrophe, and a slow silting of the Jawf does not produce the
single dramatic morning the tradition describes. It softens the problem; it does not remove it.</p>
<p><b>Three — and this is what this book prints — the dam is not the cause. It is the memory.</b>
The dispersal of the Azd was not an event. It was a drift north along the caravan roads across
several centuries, which is exactly what the decline of a trading system looks like from the inside:
nobody leaves, everybody has already left. <i>What the dam gave the tradition was not a reason. It
gave it a date and an image.</i> Peoples do not remember two hundred years of falling caravan
revenue. They remember the day the water came through the wall{c('On the long decline of the South Arabian caravan economy rather than a single catastrophe: Christian Julien Robin on the political fragmentation of the second and third centuries, and Alessandra Avanzini, <i>By Land and By Sea: A History of South Arabia before Islam Recounted from Inscriptions</i> (Rome: L’Erma di Bretschneider, Arabia Antica 10, 2016), which reconstructs the whole period from the epigraphy rather than from later Arabic tradition. '+D('2016_Avanzini_By_Land_and_By_Sea_South_Arabia_before_Islam.pdf')+'.')}.</p>
<p><b>This is not a demolition of the family story, and it should not be read as one.</b> Every
element of the tradition survives: the South Arabian origin, the Azd, the road north, the name
Ghassān. What does not survive is the <i>mechanism</i> — the neat causal sentence in which a dam
bursts and a people picks up and walks. The genealogists were not inventing a migration. They were
supplying, several centuries afterwards, the one dramatic cause available to them for a movement
whose real cause was slow and had no story in it{c('Brian Ulrich, <i>Arabs in the Early Islamic Empire: Exploring Al-Azd Tribal Identity</i> (Edinburgh, 2019), 13, 29–31, on the “Scattering of Azd” as an eighth-to-tenth-century literary construction; and Mounir Arbach, Jérémie Schiettecatte &amp; Muḥammad al-Ḥājj, “The Kingdom of Sabaʾ in the Second Century CE — A Reassessment,” in Darles, Khalidi &amp; Arbach (eds), <i>Contacts between South Arabia and the Horn of Africa</i> (Toulouse: Presses Universitaires du Midi, 2021), 69–84, for the political fragmentation already under way three centuries before the dam’s recorded failures. '+D('2021_Arbach_Schiettecatte_Kingdom_of_Saba_2nd_c_CE.pdf')+'.')}.</p>
{FIX('Moved forward, the departure “lands in exactly the century when the family’s claimed dynasty was at its height on the Roman frontier.”',
 'It cannot. <b>The dynasty is on the Roman frontier because Ghassān had left the south long before the water failed.</b> ʿInān 75 puts the name in western Arabia in the mid-third century — some two hundred years before the dam’s first recorded breach — and its editor places the tribe’s centre in that period at Yathrib, not on the frontier. <i>The inscriptions do not put Ghassān in Syria by 250; they put it out of Yemen by 250, which is enough.</i> Correcting the dam’s date forward does not rescue the causal chain — it breaks it from the other end.',
 'The correction in the entry above is right about the dam and wrong about what the dam explains, and this book does not get to keep both. <b>The Sabaic inscriptions are the strongest thing this project has found about the name</b>, and a find that strong has to be allowed to constrain the story it sits inside rather than decorate it. <i>What survives is the migration. What goes is its trigger.</i> The tradition is not thereby weakened; it is relocated — from history of events to history of memory, which is where most family traditions of this age actually live.')}
<p><i>One consequence worth holding on to.</i> The scattering entry that follows quotes Brian Ulrich’s
caution that the “Scattering of Azd” is itself a literary construction of the eighth to tenth
centuries. In earlier editions that sat in a footnote as a scholarly hedge. <b>On the chronology set
out here it stops being a hedge and becomes the finding.</b></p>"""),

ent('473', 'attested', False, 'Amorkesos signs a treaty with Byzantium',
 'A well-dated fifth-century federate arrangement covering Palaestina Tertia — <b>though not the earliest: Queen Mavia’s treaty with Valens is a century older</b>{}. The system the family’s ancestors are said to have led is already running.'.format(c('The Amorkesos episode is known from a fragment of Malchus preserved by Photius (fr. 1, ed. Blockley); Shahîd, <i>Byzantium and the Arabs in the Fifth Century</i> (Dumbarton Oaks, 1989), 61–113, reconstructs it as a formal <i>foedus</i>, which others dispute. <b>Mavia’s treaty with Valens, c. 377–378, is nearly a century earlier and is attested by four independent church historians — Rufinus, Socrates, Sozomen and Theodoret. Earlier editions of this book called Amorkesos “the earliest,” which is wrong.</b>'))),

ent('528–569', 'attested', 'shared', 'Al-Ḥārith ibn Jabala — generation 34, in contemporary Greek',
 'Justinian sets him over “as many clans as possible” of the Saracens of Arabia and bestows on him <b>“the dignity of king, a thing which among the Romans had never before been done”</b> — and Procopius, a contemporary who disliked him, writes it down{}.'.format(c('Procopius, <i>Wars</i> I.17.45–48, Loeb ed. Dewing (1914), i.158–59: <span class="gk">βασιλέως ἀξίωμα</span>, “the dignity of king.” <b>Earlier editions of this book printed the honorific <i>patrikios</i> here; Procopius does not use it in this passage, and what he does say is stronger.</b> '+D('0550_Procopius_History_of_the_Wars_I-II_Loeb.pdf')+', 610 pp. The modern treatment: Shahîd, <i>Byzantium and the Arabs in the Sixth Century</i> I.1 (1995); the field now prefers “Jafnid dynasty” to “Ghassanid kingdom” — Fisher (2011, 2018), Genequand &amp; Robin (2015).')),
 f"""
<p>This is where the family’s line walks out of literature and into history. <b>No contemporary
Greek, Syriac or Latin source ever uses the word “Ghassanid”</b> — they name individuals, and the
individuals are real{c('Hoyland’s observation; the scholarly shift from “kingdom” to “dynasty of Byzantine-appointed supreme phylarchs” in Fisher, <i>Between Empires</i> (2011) and Genequand &amp; Robin, <i>Les Jafnides</i> (2015).')}. In 542 al-Ḥārith petitions the empress Theodora and produces the
consecration of Jacob Baradaeus — the best-attested fact tying the dynasty to the eastern
church{c('John of Ephesus, <i>Ecclesiastical History</i> and <i>Lives of the Eastern Saints</i>, on the 542 petition and the ordinations of Jacob Baradaeus and Theodore.')}. In 554 he breaks the Lakhmid king at Chalcis. And on the plateau beside Madaba — <i>the
very plateau the family remembers as its road</i> — a sixth-century church at <b>Nitl</b> carries
mosaic inscriptions naming <b>“Thaʿlaba, the most illustrious phylarch”</b> and <b>“Arethas son of
Arethas”</b>: the most important Jafnid-associated
monument in Jordan — though the identification rests on the names alone, and both readings are partly
restored. <b>The unambiguous royal inscriptions are in Syria: the Arabic text at Jabal Usays, dated 423 of the era of Bostra — 528 CE — first read and published by the Syrian scholar <b>Muḥammad Abū al-Faraj al-ʿUsh</b>,
which names al-Ḥārith the king outright, and the tower inscription of al-Mundhir at Ruṣāfa</b>{c('Piccirillo, “The Church of Saint Sergius at Nitl,” <i>Liber Annuus</i> 51 (2001); the al-Mundhir audience hall at Ruṣāfa (562–583) and the Ḥarrān inscription of 568 complete the epigraphic core.')}.</p>
<p>Then the empire turns. Al-Mundhir is arrested in 581, shipped to Constantinople, and exiled to Sicily on Maurice’s accession in 582; al-Nuʿmān is tried and
exiled after him; the phylarchate is broken up among many smaller
phylarchs and, so far as the record shows, never reconstituted under one house{c('Shahîd I.1, 530–563, on the exiles, the dissolution of 582–585 and the restoration of 585–587.')}. <b>In 593–594 the individual names stop appearing in Greek
altogether.</b> The silence that the chart prints as generation 35 has a start date, and this is
it{c('Irfan Shahîd, <i>Byzantium and the Arabs in the Sixth Century</i> I.1 (Dumbarton Oaks, 1995), 554–60, for the disappearance of the Jafnid names from Greek after 593/594. <b>Earlier editions of this book credited this to Serikoff (2017), which is a philological note on Greek loanwords and not about the Ghassanids at all.</b>')}.</p>"""),

ent('after 543', 'classical', 'shared', 'The scattering — one catastrophe, five destinies',
 'The classical genealogists trace the entire dispersal of the Azd to the failing of the dam, and the Arabic language keeps the memory in a proverb still spoken: <b><i>tafarraqū aydī Sabaʾ</i></b> — “they scattered like the people of Sabaʾ.”{}'.format(c('Ibn al-Kalbī and the Azdī pedigree tradition; al-Masʿūdī, <i>Murūj al-dhahab</i>, on the dispersal. Brian Ulrich, <i>Arabs in the Early Islamic Empire</i> (Edinburgh, 2019), 13, 29–31, cautions that the “Scattering of Azd” is itself a literary construction of the eighth to tenth centuries — the tradition’s shape, not necessarily its detail, is what survives scrutiny.')),
 f"""
{fig(F3.fig_scattering(),'“They scattered like the people of Sabaʾ”',
 'Where the Azd tribes went when the water failed. Each arrow became a famous people: the Khuzāʿa who kept Mecca, the Aws and Khazraj who received the Prophet at Medina and are remembered as the Anṣār, the seafaring Azd of Oman — and, north along the caravan roads to the Roman frontier, Ghassān. The family’s tradition is not an eccentric private claim; it is a branch of the best-known migration story in the Arabic language.',
 'Ibn al-Kalbī; al-Masʿūdī; Qurʾān 34:15–19; Ulrich (2019) for the modern caution.')}
<p><b>This is the moment that makes the family’s story ordinary — in the best sense.</b> A house
claiming descent from Ghassān is claiming a place in the same dispersal that produced the guardians
of Mecca and the helpers of Medina. The tradition is shared, ancient, and enormous; what this book
tests is only the family’s particular thread through it.</p>"""),

ent('563/4 · 569 → 581/2', 'attested', False, 'The silence starts later than the chart does — two inscriptions',
 '<b>The family’s line stops at al-Ḥārith, who dies in 569. The dynasty’s record does not.</b> Two finds, one of them published this year, carry the Jafnids further than any text does — and both are in Jordan{}.'.format(c('Both were found and published in Jordan, on the plateau and the desert edge the family’s tradition names as its road — not in Syria, where the dynasty’s capitals were.')),
 f"""
<p><b>At Tall al-ʿUmayrī East</b>, on the Balqāʾ plateau near Amman, a three-and-a-half-metre Greek
mosaic inscription laid in red tesserae names <b>Alamoundaros</b> — al-Mundhir, al-Ḥārith’s son —
with the titles <i>megaloprepestatos</i> and <i>komes</i>, and invokes the God of Saint Sergius over
and over. It is dated to about <b>563/4</b>, while his father was still alive{c('George Bevan, Greg Fisher and Denis Genequand, “The Late Antique Church at Tall al-ʿUmayrī East: New Evidence for the Jafnid Family and the Cult of St Sergius in Northern Jordan,” <i>Bulletin of the American Schools of Oriental Research</i> 373 (2015), 49–68. The terminal date of the inscription is lost; the authors place it in al-Ḥārith’s tenure, with al-Mundhir holding an intermediate rank before succeeding about 568/9.')}.</p>
<p><b>And in 2024 a stone was found in the north-eastern Jordanian ḥarrah</b>, at Wādī al-Shuwayṭī,
carrying a <b>Paleo-Arabic inscription dated by the regnal year of al-Mundhir the king</b> — “year
six of the reign of al-Mundhir.” It carries a three-generation genealogy of ordinary men, which is
what makes it remarkable: <i>not a king’s monument, but somebody counting the years by a Jafnid
king’s reign, in Arabic, on the desert edge.</i> It was published in 2026{c('Ahmad Al-Jallad, Ali al-Manaser and Greg Fisher, “A Dated Paleo-Arabic Inscription Mentioning al-Mundhir (ʾmndr) the King,” <i>Arabian Archaeology and Epigraphy</i> 70:1 (2026), doi:10.1111/aae.70013. The text is dated to year six of al-Mundhir’s reign, placing it between 569 and his exile in 581/2, and carries the genealogy Zubaydah/Ziyaydah b. ʾhd b. Kuwayṯ; a second text names ʿAlqamah b. ʿAntarat. <b>This is the newest Jafnid epigraphy known and it was published while this book was being written.</b>')}.</p>
<p><b>What this does to the void.</b> The chart’s last named ancestor still dies in 569. But the
<i>documentary</i> silence about the dynasty now begins around <b>581/2</b> rather than 569, and the
Greek narrative sources run to 593/4. <i>The hole in the family’s line and the hole in the record are
two different holes, and this book has been careless about saying so.</i></p>"""),

ent('the frontier, in stone', 'attested', False,
    'WHAT THEY LEFT — a Roman fort, a Ghassanid hall and an Umayyad palace, inside the same walls',
 f'''Everything this book has offered for the Ghassanids so far is <i>writing</i>: Procopius, two
Sabaic inscriptions, a Greek dedication, an itinerary. <b>There is also a building.</b> At <b>Qaṣr
al-Ḥallābāt</b>, on the Jordanian steppe, a Roman fort of the <i>limes Arabicus</i> was rebuilt as a
monastic and Ghassanid complex and then refurbished again as an Umayyad palace — <i>three regimes,
one set of walls, and no destruction layer between them</i>{c('Ignacio Arce, “Romans, Ghassanids and Umayyads and the Transformation of the <i>Limes Arabicus</i>: from Coercive and Deterrent Diplomacy towards Religious Proselytism and Political Clientelarism,” in Guido Vannini &amp; Michele Nucciotti (eds), <i>La Transgiordania nei secoli XII–XIII e le “frontiere” del Mediterraneo medievale</i>, Limina/Limites 1, BAR International Series 2386 (Oxford: Archaeopress, 2012), ISBN 978-1-4073-0978-1. The article is dedicated to Michele Piccirillo, Svend Helms and Irfan Shahid. '+D('2012_Arce_Romans_Ghassanids_Umayyads_and_the_Limes_Arabicus_BAR_S2386.pdf')+'.')}.''',
 f"""
<p><b>Arce’s argument is about how a frontier stops being a wall.</b> Rome held this line with forts
and garrisons — coercion, and the threat of it. What replaced that was not collapse but a different
instrument: <i>client kings, and a shared religion</i>. The Ghassanid phylarchs were paid, titled,
and made Christian, and the forts they inherited became audience halls and churches. The Umayyads
then inherited the same buildings and the same method and changed the religion. <b>The physical
continuity is the argument: the same walls serve three states because the states are doing the same
job by gentler means each time.</b></p>
<p><b>And there is a historiographical point in it that this book should say out loud, because it is
our own problem in someone else’s field.</b> Arce notes that the Ghassanid century has been almost
invisible in the archaeology — classical archaeologists passed over it as a barbarian takeover of
Roman ground, even though the takers were Christian Arabs; Islamic archaeologists passed over it as
the tired last decades before the conquest. <i>It fell between two disciplines and nobody dug it.</i>
<b>A gap in a record is not always an absence in the world. Sometimes it is an absence of people
looking</b>{c('Arce, in Vannini &amp; Nucciotti (2012), on the “academic frontier” between classical and Islamic archaeology in Transjordan, and on the excavation and restoration of Qaṣr al-Ḥallābāt directed by the author from 2002. On the same ground: Michele Piccirillo, <i>The Mosaics of Jordan</i> (Amman: ACOR, 1993), for the Nitl church and its Ghassanid dedications.')}. — which is exactly the argument the interlude of this
book will make about our own nine hundred years.</p>"""),
ent('the question behind the question', 'attested', False, 'WERE THE GHASSANIDS SOVEREIGN? — and why it is being asked',
 f"""Procopius says Justinian gave al-Ḥārith <b>“the dignity of king”</b> — and that is where a
modern argument begins, because if the Ghassanids were sovereigns then somebody today might inherit
something. <b>The family should know how that question actually works before anybody answers it on
their behalf.</b>""",
 f"""
<p><b>Start with what the word is doing.</b> Procopius writes <span class="gk">βασιλέως
ἀξίωμα</span> — the <i>dignity</i>, the rank, of a king — and adds that it had never been done
before. He is describing <b>a promotion inside an empire</b>, in the voice of a Constantinopolitan
who disliked the man. <i>That is an imperial writer telling us what Rome conferred. It is not a
statement about what al-Ḥārith already was.</i></p>
<p><b>Now hear it in Arabic.</b> At Jabal Usays in 528 an ordinary frontier guard — <b>Ruqaym son of Maʿarrif the Awsite</b> — records
that <b>al-Ḥārith the king</b> — <span class="ar">الحارث الملك</span> — sent him. He does not ask
Constantinople's permission for the word, and he is not writing for Constantinople. <i>One man calls
him king because an emperor said so; the other calls him king because that is what he was called on
the ground.</i> <b>Those are two different kinds of evidence and the second is ours.</b></p>
<div class="fix"><div class="fixhead">The category is younger than the men in it</div>
<div style="font-size:.95rem;line-height:1.65;color:#46423B">
<p style="max-width:none">“Sovereign” in the sense the modern argument needs — a state, a
territory, a crown that descends and can be inherited or lost — is a <b>European vocabulary of the
seventeenth century onward</b>, and it fits the sixth-century Levant badly. The comparanda are
instructive and none of them resolves cleanly:</p>
<p style="max-width:none"><b>Persian Yehud.</b> Sheshbazzar and Zerubbabel were Davidic
descendants appointed governors of a Persian province. The empire used the prestige of the dynasty
precisely <i>because</i> it was a dynasty — and that is not the same thing as the dynasty ruling{c('Nadav Naʾaman, “Royal Vassals or Governors? On the Status of Sheshbazzar and Zerubbabel in the Persian Empire,” <i>Henoch</i> XXII (2000). <b>The pattern matters more than the case:</b> an imperial power appointing members of local dynasties as its officers, and both sides finding the arrangement useful.')}.</p>
<p style="max-width:none"><b>The Keneges of Shahrisabz.</b> Their own royal chronicle has them
inheriting their domain from Timur and never being defeated. The surrounding record has them as
one more emirate inside somebody else's order. <i>A dynasty writing its own sovereignty into its own
chronicle is a normal thing for a dynasty to do</i>{c('James Pickett, “Written into Submission: Reassessing Sovereignty through a Forgotten Eurasian Dynasty,” <i>American Historical Review</i> Forum. The essay is about exactly this: how the paperwork of sovereignty is produced, and by whom.')}.</p>
<p style="max-width:none"><b>And Byzantium itself is a contested category.</b> The people we call
Byzantines called themselves Romans; “Byzantine” is a later coinage, and the field now argues about
how much of the identity was constructed by the people who later wrote about it{c('Anthony Kaldellis, “Provincial Identities in Byzantium” (Routledge, 2022); Yannis Stouraitis, “Is Byzantinism an Orientalism? Reflections on Byzantium’s Constructed Identities and Debated Ideologies”; Koray Durak and Ivana Jevtić (eds.), <i>Identity and the Other in Byzantium</i>, Fourth Sevgi Gönül Byzantine Studies Symposium, Istanbul 2016. <b>These are cited here as what they are — a frame for the question, not evidence about this family.</b>')}. <b>If the empire's own name for itself is
an argument, the status of its Arab allies will not be settled by a phrase in Procopius.</b></p>
</div></div>
<p><b>So the honest answer is three sentences.</b> Al-Ḥārith held real authority over real people and
was called a king in two languages. Rome treated him as its instrument and said so. <b>Whether that
adds up to “sovereignty” depends entirely on a definition supplied from outside the sixth
century</b> — and the field has stopped using “the Ghassanid kingdom” in favour of “the Jafnid
dynasty” for that very reason{c('Greg Fisher, <i>Between Empires: Arabs, Romans and Sasanians in Late Antiquity</i> (2011) and <i>Arabs and Empires before Islam</i> (2015); Denis Genequand and Christian Robin (eds.), <i>Les Jafnides: des rois arabes au service de Byzance</i> (Paris: De Boccard, 2015) — <i>“Arab kings in the service of Byzantium,”</i> and the tension in that subtitle is the whole argument.')}.</p>
{FIX('The interesting question is whether the Ghassanids were sovereign.',
 'The interesting question is <b>why anyone needs them to have been</b>.',
 'Nothing in this family’s history turns on the answer. Rāshid al-Ḥaddādīn was a farmer with five sons who moved up a ridge and paid a tithe to Hebron; <b>he is not more or less real depending on whether a man in Ruṣāfa nine hundred years earlier met a seventeenth-century European definition of a crown.</b> The question is being asked hard, in our own century, by people for whom the answer has consequences. <b>That is a fact about our century, not about Ghassān</b> — and it is the reason this entry exists at all.')}
<p><i>This book’s grade for this link does not move. It was</i> <b>ATTESTED</b> <i>because a
contemporary Greek historian and a dated Arabic inscription both name the man. It stays</i>
<b>ATTESTED</b>. <i>Sovereignty was never what held it up.</i></p>"""),

CH(8)

sect('And in our own line', 'The dynasty’s last century in the record — and then nothing for four hundred years')
ent('636', 'oral', False, 'Yarmūk — and the story that has no witness',
 'Jabala ibn al-Ayham is said to have led the Ghassanid contingent, converted, quarrelled with the caliph over a broken nose, and fled to Byzantium. <b>No contemporary source names him at all</b> — the whole story is Abbasid-era literature, written 150 to 550 years later, and scholars read Jabala as semi-legendary{}. <i>The most famous Ghassanid story is the worst-attested claim in this book, and the family should know that before repeating it.</i>'.format(c('Fisher, <i>Rome, Persia, and Arabia</i> (2020): “there are no contemporary sources about Jabala.” The narrative sources are al-Balādhurī (d. 892), al-Ṭabarī (d. 923), and Ibn ʿAsākir (d. 1176).'))),

ent('684', 'documents', False, 'Marj Rāhiṭ: still a people, forty-eight years on',
 'At Jābiya, the old Ghassanid capital, a <i>shūrā</i> convened by the <b>Banū Kalb</b> makes Marwān I caliph — and Damascus is secured for him by a Ghassanid nobleman, <b>Yazīd ibn Abī l-Nims</b>{}. Named Ghassanid men — a governor of Mosul, a “leader of the people of Damascus,” a family of scholars — hold office in Damascus into the 830s{}.'.format(
  c('Crone, <i>Slaves on Horses</i> (1980), 34–36; Kennedy, “Syrian Elites from Byzantium to Islam,” in Haldon (2010), 196–198.'),
  c('Khalek, <i>Damascus after the Muslim Conquest</i> (2011), 43–46, 66–67; Madelung, <i>JSAI</i> 24 (2000), 333.'))),

ent('c. 890', 'documents', False, 'al-Yaʿqūbī finds Ghassān — in Transjordan',
 'The geographer, describing his own present, records the Ghassān living in the Ghūṭa of Damascus <b>and at Gharandal, in Transjordan</b>{} — the last time a geographer describing his own present <i>locates a settled Ghassān population on the ground</i>. <b>It is on the very plateau the family remembers as its road.</b>'.format(c('al-Yaʿqūbī (d. 897), cited in Kennedy (2010), 198. Gharandal (Arindela) lies on the plateau south of Karak.')),
 """
<p>Three hundred and twenty-one years after al-Ḥārith’s death, and two hundred and ninety-six
after the Greek sources stopped saying the word at all, a Muslim geographer writing in
Arabic still knows where the Ghassān live — and one of the two places he gives is the southern
Transjordanian plateau. <b>That single sentence shortens the documentary silence by three
centuries</b>, from roughly nine hundred years to about six hundred and ten, and it puts the family's
claimed people on the exact ground the family's own migration story starts from.</p>
<p><i>It is not a chain of fathers, and this book will not pretend otherwise. It is something more
modest and more useful: evidence that the population the tradition names was still there, still
named, and still in the right place, long after the kingdom that made it famous had gone.</i></p>"""),

sect('What the ground says', 'Meanwhile on this ridge, the Christian villages go on being Christian villages')
ent('c. 550 → 750', 'attested', False,
    'THE TOWNS DO NOT DIE — Pella, Jarash and ʿAmmān across the conquest',
 f'''This era’s claim — <i>the conquest changes the rulers, not the people</i> — has so far been carried
by argument. <b>It can be carried by excavation.</b> Across the river, at <b>Pella</b>, <b>Jarash</b>
and <b>ʿAmmān</b>, the two centuries either side of 636 show occupation, markets, building and
church repair running straight through the conquest, with no destruction horizon and no
abandonment{c('Alan Walmsley, “Pella, Jarash and ʿAmman: Old and New in the Crossing to Arabia, ca. 550–750 C.E.” The paper opens from the Nessana papyri — the administrator of Nessana, in the <i>kūra</i> of Ghazza within <i>jund Filasṭīn</i>, receiving a requisition for two camels and two drovers about 685 — and works east into the highland towns of Jordan. '+D('19xx_Walmsley_Pella_Jarash_and_Amman_550-750_CE.pdf')+' <b>The offprint carries no year of publication; this book therefore prints none.</b>')}. <i>The names of the governors change on the documents. The
pottery does not change at all.</i>''',
 f"""
<p><b>This matters here for one specific reason.</b> The family’s tradition puts its ancestors on the
Transjordanian plateau — Karak, Shawbak, the country these three towns anchor — for exactly the
centuries when the standard story says the region emptied out. <b>It did not empty out.</b> The
excavation of the towns says the population stayed, kept trading, kept worshipping, and simply
acquired new rulers, which is the same thing this book argues happened on this ridge and for the same
reasons.</p>
<p><i>What it does not do is find anybody of ours.</i> Continuity of settlement is not continuity of
a family, and no name from any of these three towns is ours. It removes an objection rather than
supplying a proof: <b>nobody can now say the plateau was empty when the tradition says our people
were on it.</b></p>"""),
ent('1058', 'documents', False, 'A village church is rebuilt at ʿAbūd — dated, inside the silence',
 'About eighteen kilometres north-west of the future Ramallah, the church at <b>ʿAbūd</b> is rebuilt, and the work is dated{}. <i>Nothing in the family record covers this year. The hills do.</i>'.format(c('The rebuilding of the church at ʿAbūd, dated 1058, among the dated Christian records of these hills between the seventh and sixteenth centuries; Hamdan Taha\u2019s work at \u02bfAb\u016bd. See the bibliography, \u00a7XXIX.'))),

CH(9)

sect('What the ground says', 'Four centuries in which the land is thoroughly documented and our own line is not')
ent('1099 → 1187', 'documents', False, 'Magna Mahumeria: the Franks arrive, and name nobody local',
 'Crusader al-Bīra — the next hill over — becomes <b>Magna Mahumeria</b>, one of the largest Frankish rural settlements in the kingdom of Jerusalem. Its charter of <b>1156</b> rolls ninety-two Frankish burgesses by name — some fifty more are added over the next thirty years{}. <b>Not one local Christian is listed</b> — and the local Christians were plainly there, because the Franks had to farm around them. Saladin takes the place back in 1187, and Yāqūt, writing a generation later, reports having seen the ruin himself{}'.format(
  c('The 1156 charter in the cartulary of the Holy Sepulchre, often cited as of 11 February, a day this project has not verified against the cartulary itself; Ellenblum, <i>Frankish Rural Settlement in the Latin Kingdom of Jerusalem</i> (1998); Pringle, <i>The Churches of the Crusader Kingdom of Jerusalem</i>, I. '+D('1993_Pringle_Churches_of_the_Crusader_Kingdom_v1.pdf')+'.'),
  c('Yāqūt al-Ḥamawī, <i>Muʿjam al-buldān</i>, s.v. <span class="ar">البيرة</span>. <b>Earlier editions of this book quoted a first-person <span class="ar">رأيتها</span> here; this project has not been able to verify that word in the text and no longer prints it.</b> The secondary literature says only that Yāqūt mentions having seen the ruins.')),
 f"""
{fig(ATLAS.fig_district(),'The hills around Ramallah — what has been dug, what was written, who ruled',
 'Everything within a few kilometres of the future town: the excavated Byzantine sites, the Frankish settlement at al-Bīra, the inscription at Jifnā, the throne villages that ran this district for the Ottomans, and the watershed ridge road that all of it hangs off. Ramallah itself is the one dot with nothing under it before 1562 — which is exactly what a hill of endowment land should look like.',
 'al-Houdalieh on Khirbet et-Tireh; Taha at ʿAbūd; Pringle on the Frankish churches; the Ottoman defters; Conder and Kitchener, <i>Survey of Western Palestine</i>.')}
<p><b>The Franks are the exception that proves this book\u2019s rule.</b> They are the one arrival in
four thousand years that genuinely left: a transient pulse of European ancestry, found in the
nine men of the Crusaders’ pit at Sidon — of whom only two were part-European and part-local — and
gone within a few generations{c('Haber et al., “A Transient Pulse of Genetic Admixture from the Crusaders in the Near East,” <i>AJHG</i> 104:5 (2019), DOI 10.1016/j.ajhg.2019.03.015. The study sequenced thirteen individuals from Lebanon across a thousand years, of whom <b>nine</b> are from the Sidon pit. <b>The negative result is Lebanese</b> — the same test has not been run on this ridge.')}. Everybody else whose arrival has been
tested for stayed and married into it, and in Lebanon, where the test has been run, the Frankish
ancestry is simply gone. <i>The family’s own arrival, four centuries later, is of the
second kind.</i></p>"""),

ent('1182 · 1217/18 · 1321 · 14th c.', 'documents', False, 'The ridge and the plateau stay Christian — in other people’s documents',
 'Four dated traces, none of them written by anyone in this family, all of them inside the blank the chart prints: <b>a Frankish charter of 1182 signed by one <i>Raymundus de Jafenia</i></b>; the pilgrim <b>Thietmar at Shawbak on his journey of 1217–18</b>, hosted and fed by a Frankish widow living in the suburb, where Christians and Muslims lived side by side; <b>a Christian majority still at Shawbak in 1321</b>; and <b>men of Jifnā named in the Jerusalem Ḥaram al-Sharīf documents</b>, a corpus overwhelmingly of 793–794 AH / 1391–92{}.'.format(c('The Jifnā charter of 1182, signed by Raymundus de Jafenia, and the Jerusalem Ḥaram documents of 1374. <b>Earlier editions of this book also printed “the Jifnā inscription of 1179”; the project has not been able to verify that a separate inscription of that year exists, and has retired the date rather than print an object it cannot find.</b> (Little, <i>A Catalogue of the Islamic Documents from al-Ḥaram aš-Šarīf</i>); Thietmar, <i>Peregrinatio</i>, the journey of 1217–18; the stop at Shawbak (Mons Regalis) is dated 1217 in the Transjordanian survey literature and 1218 elsewhere, so this book gives the journey rather than the year; the Christian majority at Shawbak in 1321 from the Mamluk-period record.')),
 f"""
<div class="fix"><div class="fixhead">An expert verdict that cuts against the tradition</div>
<div style="font-size:.95rem;line-height:1.65;color:#46423B">
<p style="max-width:none"><b>The family’s tradition asserts continuous Christian residence on the
Shawbak–Karak–Maʿīn plateau from late antiquity to about 1500. The leading archaeologist of Christian
southern Jordan says that is not what the ground shows.</b> Robert Schick’s position is that the
plateau was solidly Christian in the sixth century — some fifty churches, hundreds of Christian
tombstones — that its churches <i>cease Christian use by the ninth or tenth century and often
earlier</i>, that Christians are “scarcely attested in historical sources” from the eighth, and that
in the tenth to twelfth centuries <b>the absence of evidence genuinely reflects population decline
rather than poor survival</b>. Christians reappear briefly with the Crusader presence and then
largely vanish again{c('Robert Schick, <i>The Christian Communities of Palestine from Byzantine to Islamic Rule</i> (Princeton: Darwin Press, 1995), whose survey stops at 813; and his later and harder position in “The Decline of Christianity in Southern Jordan after the Muslim Conquest,” given at the Khalili Research Centre, Oxford. <b>Cited here against the family’s tradition, not for it.</b>')}.</p>
<p style="max-width:none"><i>This book prints that, because its method requires it.</i> <b>What
stands against it is not nothing:</b> a bishop of Karak about 800, a Latin cathedral there in 1167,
a bishop at Shawbak in 1217, a church of St George at Karak in 1329, and a Christian community
paying <i>jizya</i> at Shawbak in the register of 1596. <b>The honest reading is a much-reduced and
possibly interrupted Christian presence, not an unbroken one — and a family tradition of continuous
residence there is asserting more than the archaeology will carry.</b></p></div></div>
<p>These are not the family’s records and they do not name the family. <b>What they establish is the
thing the family’s tradition actually needs</b>: that between the last Ghassanid named in Greek and
the first Ḥaddādīn named in any register at all, there were continuously Christian populations at
both ends of the road the tradition describes — the Karak–Shawbak plateau in the south, and this
ridge in the north. <i>A migration story requires a population at each end. Both ends are documented.
The journey between them is not.</i></p>""" + FIX(
 'A grey-haired Greek bishop brings the pilgrim Thietmar bread and cheese at Karak in 1217.',
 'The pilgrim <b>Thietmar</b> was hosted at <b>Shawbak</b>, on his journey of <b>1217–18</b>, by <b>a Frankish widow</b> living in the suburb — <b>not by a bishop, and not at Karak</b>.',
 'Thietmar’s own <i>Peregrinatio</i> is explicit about the place and the person; earlier editions of this book conflated two separate episodes. <b>The year is the one part still loose</b> — the Transjordanian survey literature dates the Shawbak stop to 1217, other accounts to 1218 — so this book prints the journey, 1217–18, rather than choosing. <b>The corrected reading is weaker as an anecdote and stronger as evidence</b>: a resident Frankish widow, in a suburb where Christians and Muslims lived side by side, shows an ordinary settled population, where a visiting bishop would have shown only a visit.')),

ent('26 July 1374', 'documents', False,
    'ONE CHRISTIAN, ONE DEBT — and a place-name with a question mark over it',
 f'''Inside the void, a single sheet of paper. On <b>7 Ṣafar 776</b> — late July 1374 — a man called
<b>Niʿma ibn Bishāra al-Naṣrānī</b>, “the Christian,” bought a weight of cotton on credit from the
provisioner <b>Ḥājj ʿUmar ibn Muḥammad ibn ʿUmar al-ʿAllāf</b>. The price was <b>218 dirhams</b>,
repayable at <b>six dirhams at the close of every week</b>. Two witnesses signed it, and somebody
later struck the whole thing through — which is how a debt is marked paid. The paper survived in the
Ḥaram al-Sharīf deposit at Jerusalem{c('Text #922/4 (recto), contract 4, in Said Aljoumani, Zahir Bhalloo &amp; Konrad Hirschler, <i>The Ḥaram al-Sharīf Documents: A Catalogue</i> (Berlin: De Gruyter, 2024), 48 and 175, open access, DOI 10.1515/9783111330242. Six lines, two witness clauses, in very good condition with no lacunae. The witnesses are ʿAlī b. Ismāʿīl b. Shākir and ʿAbd al-Raḥmān b. Muḥammad. The Gregorian date is the tabular conversion of 7 Ṣafar 776 and may be a day or two out. '+D('2024_Aljoumani_Bhalloo_Hirschler_Haram_Documents.pdf')+'.')}. <b>And it says where he came from — except that
nobody can read it.</b>''',
 f"""
<p>The scribe wrote <span class="ar">جفنا الجوز؟</span>, and the editors print it exactly like that,
with the question mark, and index it under that queried form. <b>It is not simply “Jifnā.”</b> It is a
compound name, uncertainly read, and the catalogue’s own index of places keeps it separate from
anything else.</p>
{FIX('“Men of Jifnā in the Ḥaram registers in 1374,” listed among the dated records that fall inside the blank.',
 '<b>One man, not men</b> — a single named individual in a single contract. And <b>the village is a queried reading</b> of a compound place-name that the editors do not identify with Jifnā north of Ramallah.',
 'Autopsy of the published catalogue, which this project did not do when it first made the claim. The document is real, the man is real, the date is firm and the fact that he is a Christian is written on the page. <i>What is not firm is the one thing the claim rested on.</i> The entry is kept, and demoted from evidence about this district to evidence about the century.')}
<p><b>It is still worth printing, and here is why.</b> A Christian of the Jerusalem countryside, in
1374, is named with his father’s name, buys goods on credit from a Muslim dealer, and has the terms
written into an instrument good enough to survive six hundred and fifty years. <i>Whatever village he
walked in from, that is what an ordinary Christian life looked like in the middle of the four hundred
years this book cannot cross</i> — and it is exactly the kind of paper our own ancestors would have
generated, if anybody had kept theirs.</p>
<p><b>And now the search, reported whether or not it found anything.</b> McGill University has put the
1978 microfilm of the entire corpus online — four rolls, some nine hundred documents, free to
anyone{c('McGill University Library, <i>Islamic documents from al-Ḥaram al-Sharīf in Jerusalem</i>, four microfilm rolls digitised and open on archive.org, items <code>McGillLibrary-isl_al-haram-as-sarif_CD2019J47L571984_roll1-20453</code> through <code>roll4-20456</code>. The catalogue that makes them usable is Donald P. Little, <i>A Catalogue of the Islamic Documents from al-Ḥaram aš-Šarīf in Jerusalem</i>, Beiruter Texte und Studien 29 (Beirut, 1984), ISBN 3-515-03699-7 — print only.')}. <b>The machine-read text of it is worthless.</b> In three hundred and ten thousand
characters of optically recognised Arabic, drawn from a religious archive in Jerusalem, the words
<span class="ar">القدس</span>, <span class="ar">الحرم</span>, <span class="ar">الشريف</span> and
<span class="ar">قرية</span> occur <b>not once</b>, and <span class="ar">محمد</span> occurs
<b>once</b>. The commonest strings the software produced are <span class="ar">ااا</span> and
<span class="ar">الا</span>. <i>It is reading the strokes and not the words.</i> Fourteenth-century
chancery and court hands, photographed on microfilm in 1978, defeat it completely.</p>
<p>So the search was run instead on <b>the published catalogue</b>, which is a thing a reader can
check. Across the whole of it, the villages of this ridge — <b>Jifnā, ʿAbūd, Ṭaybeh, al-Bīra, Bayt
Jālā, and Ramallah itself</b> — appear exactly twice: the queried
<span class="ar">جفنا الجوز؟</span> above, and a letter of <b>1914</b> about appointing an imam at
Silwād in the nāḥiya of ʿAbawīn, five and a half centuries too late to help{c('#887, a letter of Jumādā I 1332 / 1914 from Muḥammad Kāmil al-Ḥusaynī, deputy judge of the sharīʿa court at Jerusalem, requesting a <i>berat</i> for Shaykh Muḥammad b. Shaykh ʿAbd al-Fattāḥ as imam of the mosque at Silwād. Aljoumani, Bhalloo &amp; Hirschler (2024), 103.')}.</p>
<p><b>That is the result, and it is a real one.</b> It does not say the corpus holds nothing of ours.
It says the <i>published</i> part of it holds nothing of ours, and the unpublished part cannot at
present be read by anybody who is not sitting in a reading room with the originals or working through
Little’s catalogue page by page. <i>The void survives this search, and the search is on the record so
that nobody has to run it twice.</i></p>"""),
ent('1186 → 1330', 'documents', False, 'THE NAME APPEARS — a hundred years earlier than this book has been saying',
 f"""<b>A Crusader charter names this place a century before the Mamluks.</b> On <b>7 March 1186</b>
Guy de Lusignan, owing the German hospital in Jerusalem a hundred and eleven marks of silver, pledges
it a village of his <b>“near the royal road by which one goes to Ramallah”</b> — <i>prope viam regalem,
qua vaditur Ramelie</i> — to become the hospital’s if he cannot pay within a year and a
day{c('Ernst Strehlke, ed., <i>Tabulae Ordinis Theutonici</i> (Berlin, 1869), p. 18, no. 20; the Latin and an English translation are printed in Azeez Shaheen, <i>A Pictorial History of Ramallah</i> (1992), pp. 17–19. Sāmiḥ Ḥammūdeh, “New Light on Ramallah’s Origins in the Ottoman Period,” <i>Jerusalem Quarterly</i> 59 (2014), p. 39, gives the same date. <b>Earlier editions of this book said the name first appears in 1279. It appears in 1186 — in an article this project already held.</b> ' + D('2014_Hammoudeh_New_Light_Ramallah_Ottoman_JQ59.pdf') + ' · ' + D('1992_Shaheen_A_Pictorial_History_of_Ramallah.pdf') + '.')}.
<i>The road already went to Ramallah while the Crusader kingdom still stood — a place well enough known
to give a king’s road its direction.</i>""",
 f"""
{FIX('Guy de Lusignan pledges that if he cannot pay, <b>“the village of Ramallah becomes the hospital’s property”</b>; and “Rey found <i>Ramalei</i> in a manuscript of <b>1198</b>” — as printed in earlier editions.',
 '<b>The village pledged in 1186 is not named.</b> Ramallah is named as the place the royal road beside it leads to — which is still the first time the name is written down. <b>The 1198 document is a forgery</b>, and is withdrawn as evidence.',
 'The charter’s own words are <i>unum casellum nostrum … prope viam regalem, qua vaditur Ramelie</i> — “one hamlet of ours … near the royal road by which one goes to Ramelie.” The “1198” grant to Marseilles, Rey’s source and the one that names an <i>Andreas de Ramella</i>, is one of a set of documents forged at Acre about 1220, identified by Hans Eberhard Mayer from their wrong formulas.' + c('H. E. Mayer, <i>Marseilles Levantehandel und ein akkonensisches Fälscheratelier des 13. Jahrhunderts</i> (Tübingen: Niemeyer, 1972), pp. 1–3; E. G. Rey, <i>Les colonies franques de Syrie</i> (Paris, 1883), p. 389; Mas Latrie, <i>Histoire de l’île de Chypre</i> II (Paris, 1852), pp. 24–25. Summarised in Shaheen (1992), pp. 19–20. <b>Shaheen’s own conclusion is worth keeping: the forger could only use a name everybody already knew.</b>'))}
<p><b>Then the endowment.</b> A Jerusalem court record of 1565 cites a waqf of Sultan Qalāwūn dated
678 AH — 1279–80 — in which <i>Rām Allāh</i> is already a named place, <b>about 283 years before the
traditional founding</b>. <i>The deed itself does not survive.</i>{c('Ḥammūdeh (2014), p. 40 and n. 17: “We do not have the text of Sultan Qalawun’s waqf, but court records (sijill 48, page 88) from the end of Dhu al-Qiʿda 972 AH (29 June 1565 CE) mention the waqf and date it back to 678 AH.” 678 AH runs 14 May 1279 – 3 May 1280. <b>Earlier editions of this book cited “sijill 48, p. 54, 22 June 1565” and described the deed as produced in court with its boundaries. All three were wrong: the page is 88, the date is 29 June, and the deed is lost.</b> The bibliography appendix to this edition still reports a separate entry at <i>p. 54</i>, 23 Dhū al-Qaʿda 972 / 22 June 1565, recording a boundary dispute over <span class="ar">قرية رام الله</span>. <b>That reading comes from a machine decode of the IRCICA scan and has not been checked against the page images; it is not the waqf entry, and until somebody reads the folio it should not be cited.</b>')}</p>
<p>Two things follow, and both matter. <b>First, the family did not name the hill.</b> The name is
older than the settlement, and it is a place-name of the ordinary Semitic kind:
<span class="ar">رام</span>, a height, joined to the divine name. <b>Second, the legal status explains
the archaeology.</b> Land held in <i>waqf</i> — inalienable endowment — is exactly the sort of ground
that turns up in a sixteenth-century Ottoman register as cultivated but uninhabited, which is
precisely what the register of 1525–28 records for this hill.</p>
<p><i>And a waqf is not a category. It is a working arrangement.</i> A sultan does not endow Hebron’s
kitchen with bare rock; he endows it with a tithe, and a tithe means a crop, and a crop means hands.
<b>For two and a half centuries the men of ʿEin Qīniya, Jifnā and al-Bīra came up this ridge, worked
it, and went home at dusk. The Ḥaddādīn were the first to stay the night.</b></p>
<p><b>The better Mamluk evidence is not the lost deed at all.</b> Ramallah is named in documents that
<i>do</i> survive: in the <b>Ḥaram al-Sharīf corpus of the 1390s</b>, where Ramallah cultivators
guarantee a yearly sum to the Hebron endowment; and in <b>Tankiz’s endowment of 1330</b>, where the
village is named as the eastern boundary of ʿEin Qīniya{c('The Ḥaram al-Sharīf documents of 793–796 AH / 1390–95, catalogued by Donald P. Little, <i>A Catalogue of the Islamic Documents from al-Ḥaram aš-Šarīf in Jerusalem</i> (Beirut, 1984); Tankiz’s endowment of 12 Jumādā I 730 / 3 March 1330. These documents exist; Qalāwūn’s deed does not. <b>The figure of “twelve fellāḥīn and 950 dirhams a year” printed in earlier editions of this book cannot be traced to Ḥammūdeh or to Little and is withdrawn until a folio is produced.</b> The surveyed boundaries once attached here to the 1279 deed come from Bakhīt and Sawāriyya and cannot at present be assigned to either instrument with confidence.')}.</p>
<p>And the negative check has been run. <b>Mujīr al-Dīn’s topography of Jerusalem and Hebron,
completed in 900 AH / 1495 and searched in full for this book, has no Ramallah in
it</b>{c('Mujīr al-Dīn al-ʿUlaymī, <i>al-Uns al-jalīl bi-taʾrīkh al-Quds wa-l-Khalīl</i> (1495), searched complete for this project in the copy held in the family library. <b>The silence is weak evidence and is printed as such:</b> <i>al-Uns al-jalīl</i> is a history of Jerusalem and Hebron with an incidental and selective village list, not a gazetteer, and a hamlet of a few households would not be expected in it. ' + D('1495_Mujir_al-Din_al-Uns_al-jalil.pdf') + '.')}.
Between 1186 and 1562 the name is on paper and the hill is barely a hamlet: endowment land with no
residents in 1525–28, <b>four Muslim households by 1538–39</b> — <b>Ḥasan bin Labūd, Khaṭṭāb bin
Ḥasan, Rajab bin Yaʿqūb and Ibrāhīm bin Labūd</b>, the first people of this place whose names we
have — and six by 1553–54. <i>The deed and the registers say the same thing from opposite ends.</i></p>"""),

CH(10)

sect('And in our own line', 'The missing centuries, measured rather than filled')
ent('569 → c. 1500', 'none', False, 'GENERATION 35 IS THIRTY-ONE GENERATIONS — and only one of them has a name',
 'Between al-Ḥārith, who dies in 569 and is named in contemporary Greek, and Rāshid, whom the family’s own texts place about 1500 and whose grandchildren the Ottoman registers reach in 1562, <b>the chart draws two links across 931 years</b>. It cannot be done. <i>The chart says so itself — it prints the gap, in the same typeface as everything else.</i>',
 f"""
<p>This is the weakest link in the family’s chain and the strongest evidence of its honesty, and the
right response to it is arithmetic rather than embarrassment. <b>Nine hundred and thirty-one years,
divided by <b>an assumed</b> male-line generational interval of twenty-five to thirty-five years, is
twenty-seven to thirty-seven generations</b> — most probably about thirty-one. The chart draws two.
So the correct thing to print at generation 35 is not a blank and not a fabrication, but
<b>a number: “about 31 generations.”</b></p>
<p><b>And that number changes how this line has to be counted.</b> The co-authors’ own chart runs to
thirty-six rows because it draws the void as one. Expanded to the thirty-one the arithmetic requires,
the line from Adam to Rāshid is <b>sixty-six generations, not thirty-six</b>: thirty-four down to
al-Ḥārith, thirty-one across the void, Rāshid at sixty-six. <i>The ladder in every era strip of this
book is now drawn on that count.</i></p>
<p>Of those thirty-one, <b>thirty have no name of any kind</b>. <b>One does</b> — the last of them,
generation sixty-five: <b>Ṣaqr</b>, Rāshid’s father, from the Karak wheel. <i>He is named by a single
witness, and the ladder prints him in a broken outline to say so.</i> The alternative reading, from
our own chart — Rāshid bin ʿĪsā bin ʿIyād bin Ḍahdūḥa — would fill generations sixty-three to
sixty-five instead, and is set out two eras on. <b>Either way the count is sixty-six.</b> What changes
is only how many of the last three slots carry a name.</p>
<div class="ntwrap"><div class="nthead">The line, recounted</div>
<table class="ntable"><tr><th>generations</th><th>who</th><th>what carries them</th></tr>
<tr><td><b>1–34</b></td><td>Adam and Eve down to al-Ḥārith b. Jabala, d. 569</td><td>scripture, then the Arabic genealogists, then Procopius in Greek</td></tr>
<tr><td><b>35–64</b></td><td><i>thirty men, and not one name for any of them</i></td><td>nothing. This is the void, measured rather than filled</td></tr>
<tr><td><b>65</b></td><td><b>Ṣaqr</b> <span class="ar">صقر</span></td><td>the Karak wheel, 2024 — one witness, no document</td></tr>
<tr><td><b>66</b></td><td><b>Rāshid al-Ḥaddādīn</b>, fl. c. 1500</td><td>both family texts; the registers reach his grandchildren in 1562</td></tr>
</table></div>
<p><b>Thirty-six of the sixty-six have names. Thirty do not.</b> <i>That is the whole state of this
family’s knowledge of itself, in two numbers, and neither of them is embarrassing.</i></p>
{fig(R.fig_arith(),'Forty-five is the wrong number',
 'Before looking for the missing generations it is worth checking the count that is usually quoted. Forty-five generations across a thousand years implies a male-line generation of twenty-two years, shorter than any population on record sustains. Thirty-one generations at thirty years each fits. <b>Correcting the arithmetic does not close the void — it measures it.</b> <i>The thirty-year figure is an assumption and not a measurement; the entry on the clock says so at length.</i>',
 'Generational-interval range after the standard genealogical-demography literature; the span from Jafna (fl. c. 520) to Rāshid (fl. c. 1500).')}
{FIX('A fixed count of generations between Jafna and Rāshid.',
 '<b>A range: about 27 to 37 generations</b>, most probably around 31 — and the line recounted at sixty-six, not thirty-six.',
 'Arithmetic, not a source: Jafna (fl. c. 520) to Rāshid (fl. c. 1500) is roughly 980 years; divided by <b>an assumed</b> male-line interval of 25–35 years, that is 28–39 links, of which the chart draws two. No source is needed for a division, and none is claimed — <b>but the interval is not a fact, and the entry that follows says where it comes from and why no better one exists.</b>')}
{fig(F.fig_void_solved(),'The void, measured — and shortened',
 'The genealogical void runs 931 years, from al-Ḥārith (d. 569) to Rāshid (fl. c. 1500), and needs about thirty-one generations to cross. The documentary void is far shorter than the genealogical one — Ghassān is entered as a living people, at al-Balqāʾ, the Yarmūk and Ḥimṣ, on the authority of a Mamluk officer who died about 1300 — and dated records fall inside the blank: ʿAbūd’s rebuilt church in 1058, a man of Jifnā signing a Frankish charter in 1182 and a Christian buying cotton on credit at Jerusalem in 1374, the pilgrim Thietmar hosted in Shawbak’s suburb on the journey of 1217–18, a Christian majority at Shawbak in 1321. What no source supplies is a chain of fathers. So the chart should print the number, not a blank.',
 'Procopius; Shahîd, BASIC I.1 (1995), 554–60; Kennedy (2010), p. 198, citing al-Yaʿqūbī; the ʿAbūd, Jifnā, Thietmar and Shawbak records.')}
<p><b>The silence in the family’s line is not a silence in the family’s world.</b> Chapters seven and
eight have just walked through it dated record by dated record: a people still named in 684, still
located in 890, <b>still entered as existing about 1300</b>, a church rebuilt in 1058, a man of Jifnā signing a Frankish charter in 1182, a pilgrim fed at Shawbak in 1217–18,
a Christian majority there in 1321, a named Christian buying cotton on credit at Jerusalem in 1374, and the town’s own
name on a sultan’s deed in 1279. <i>Everything survives across those nine hundred years except the
one thing a genealogy needs — and the chart is the document that admits it.</i></p>"""),


ent('c. 1300 → c. 1418', 'documents', False,
    'GHASSĀN IS STILL THERE IN 1400 — and the void is four hundred years shorter than this book has been saying',
 f'''<b>The blank is not six hundred years long. It is closer to two.</b> Al-Qalqashandī finished
<i>Qalāʾid al-jumān</i> — “Necklaces of Pearls, on the tribes of the Arabs <span class="ar">الزمان</span>, of the present age” —
in the first years of the fifteenth century, and Ghassān is in it, not as a memory but as a people
with addresses: <b>al-Balqāʾ, the Yarmūk, and Ḥimṣ</b>{c('Al-Qalqashandī, <span class="ar">قلائد الجمان في التعريف بقبائل عرب الزمان</span>, ed. Ibrāhīm al-Ibyārī, 2nd ed. (Cairo/Beirut, 1402/1982), <b>p. 97</b>, closing the entry <span class="ar">البطن الثاني من الأزد: غسان</span> at pp. 94–97: <span class="ar">قال في مسالك الأبصار: وبالبلقاء طائفة من غسان. وباليرموك منهم الجمّ الغفير، وبحمص منهم جماعة</span>. The same notice stands in his <span class="ar">نهاية الأرب في معرفة أنساب العرب</span>, ed. Ibyārī, no. 1421, p. 388, where it is credited not to al-ʿUmarī but to <span class="ar">الحمداني</span> — <b>the two attributions together are the transmission chain, visible in one author’s two books.</b>')}.
<i>Somebody in Mamluk service knew where to find them.</i>''',
 f"""
<p><b>And that somebody can be named.</b> The chain runs backwards from al-Qalqashandī to a man whose
job was knowing exactly this. Al-ʿUmarī, writing his <i>Masālik al-abṣār</i> in the 1340s, opens his
chapter on <i>the Arabs existing in our own time and their places</i> by saying where he got it:
<b>“I have relied for most of this on what the trustworthy amīr Badr al-Dīn Abū al-Maḥāsin Yūsuf ibn
Zammākh, known as Ibn Sayf al-Dawla al-Ḥamdānī, <span class="ar">المهمندار</span>, has
recorded”</b>{c('Ibn Faḍl Allāh al-ʿUmarī, <span class="ar">مسالك الأبصار في ممالك الأمصار</span>, ed. al-Majmaʿ al-Thaqāfī (Abu Dhabi), <b>iv.243</b>, opening <span class="ar">في ذكر العرب الموجودين في زماننا وأماكنهم</span>: <span class="ar">واعتمدت في أكثر من ذلك على ما ذكره الأمير الثقة بدر الدين أبو المحاسن يوسف بن أبي المعالي بن زمّاخ المعروف بابن سيف الدولة الحمدانيّ المهمندار</span>. The editor’s note adds that he was <i>the</i> genealogist of his age and that most who came after him on the Arab tribes were in his debt — <span class="ar">عالة عليه</span> — <b>al-ʿUmarī included</b>. Al-Qalqashandī in turn writes <span class="ar">قال الحمداني</span> fifty-eight times in <i>Qalāʾid al-jumān</i> alone.')}.</p>
<p><b>A <span class="ar">مهمندار</span> is not an antiquarian.</b> He is the officer who receives,
lodges and provisions arriving tribal delegations at the sultan’s court — the man who has to know
which tribes exist, how many they are and where they camp, because he is answerable for feeding them.
Al-ʿUmarī prints his first-person account of hosting one such delegation for the sultan Aybak, with
thirty-six thousand dinars of gifts passing <b>“all of it through my own
hands”</b>{c('<i>Masālik</i> iv.340. On the man: Ibn Ḥajar, <span class="ar">الدرر الكامنة</span> vi.227 no. 2605; Ibn Shākir al-Kutubī, <span class="ar">فوات الوفيات</span> iv.349 no. 589, calling him <span class="ar">مهمندار العرب</span>; Bakr Abū Zayd, <span class="ar">طبقات النسابين</span> no. 321, which names his <span class="ar">كتاب الأنساب</span>. <b>Born 602/1205–6; the death date is disputed and this book prints the dispute</b> — Ibn Ḥajar and Abū Zayd give 700/1300, al-Ziriklī (<span class="ar">الأعلام</span> viii.233) and Kaḥḥāla give about 670/1272, balking at an age of ninety-eight.')}.
<i>This is an administrative source that happens to have survived inside a literary one.</i></p>
{NUMTABLE('THE CHAIN, END TO END',
 ['when', 'who', 'what it gives'],
 [['c. 945', 'al-Hamdānī of Yemen, <span class="ar">صفة جزيرة العرب</span>', '<span class="ar">ديار غسان</span> — Ghassān as a named territory'],
  ['538 / 1144', 'Ibn ʿAsākir, at Damascus', 'a family still nicknamed <b>Half the Road</b> for an ancestor who set out after Jabala b. al-Ayham and turned back'],
  ['<b>d. c. 1272–1300</b>', '<b>Ibn Zammākh al-Ḥamdānī, <i>mihmandār al-ʿarab</i></b>', '<b>Ghassān among the tribes of the present day — from the officer paid to know</b>'],
  ['c. 1340s', 'al-ʿUmarī, <i>Masālik al-abṣār</i>', 'transmits him, and places the Ghassān of the Yarmūk, al-Balqāʾ and Ḥimṣ'],
  ['c. 1400', 'al-Qalqashandī, <i>Qalāʾid al-jumān</i>', 'copies it into a handbook whose stated subject is tribes now existing'],
  ['<b>c. 1500</b>', '<b>Rāshid al-Ḥaddādīn</b>', '<b>generation 66</b>']],
 'Read down the column of dates. <b>Between the last administrative notice of Ghassān as a living people and the first man in our own line there is about a century</b> — and the notice itself is a century older than the book that carries it. <i>Six hundred years of silence was never the right number.</i>')}
{FIX('“The documentary void is three hundred years shorter — a named Ghassān population is attested to about 890.”',
 '<b>To about 1300, and quite possibly to about 1400.</b> Ghassān is entered as a currently existing people, with three locations, in a Mamluk chancery handbook, on the authority of the officer whose duty was receiving Arab delegations.',
 'Al-Qalqashandī, <i>Qalāʾid al-jumān</i> (ed. Ibyārī), p. 97, and <i>Nihāyat al-arab</i>, no. 1421, p. 388; al-ʿUmarī, <i>Masālik al-abṣār</i>, iv.243 and iv.358–59. <b>The 890 date stands as the last notice in Transjordan specifically; what changes is the last notice anywhere.</b>')}
<p><b>Three cautions, because this is the best news the tradition has had and that is exactly when a
book should slow down.</b></p>
<p><b>One: the locations are east and north, not here.</b> Al-Balqāʾ, the Yarmūk and Ḥimṣ are all
across the Jordan or beyond. <i>This entry shortens the void. It does not move Ghassān to this
ridge</i> — and chapter nine has already shown that every Arab authority who specifies a place puts
them east.</p>
<p><b>Two: al-Qalqashandī is copying, not observing.</b> The datum is al-Ḥamdānī’s, from about 1300;
al-ʿUmarī relays it about 1340; al-Qalqashandī writes it out about 1400. To say that al-Qalqashandī
saw Ghassān at the Yarmūk in his own lifetime would be to claim four generations more than the page
supports.</p>
<p><b>Three: he also changed a word, and the word he changed is the interesting one.</b> Al-ʿUmarī
wrote that at the Yarmūk there were <span class="ar">صليبة من غسان</span>; al-Qalqashandī replaced
that with <span class="ar">الجمّ الغفير</span>, “a great multitude.” <i>The multitude is
al-Qalqashandī’s. The word underneath it is al-ʿUmarī’s, and it explains the whole
silence.</i></p>"""),

ent('c. 1340', 'documents', False,
    'THE WORD UNDERNEATH — why a people can be present and unrecorded at the same time',
 f'''Al-ʿUmarī does not file these Ghassānids under tribes. He files them under
<b><span class="ar">صليبة العرب</span></b> — <i>Arabs of pure and direct descent</i> — and then says
what has become of them: <b>“in Syria there are, of the pure-stock Arabs, various peoples in the
settled country <span class="ar">قد خرجوا بها عن حكم العرب</span> — they have passed out of the
reckoning of Arabs — and have become townspeople, settled, dwellers who populate
houses”</b>{c('<i>Masālik al-abṣār</i>, ed. al-Majmaʿ al-Thaqāfī, <b>iv.358</b>: <span class="ar">وبالشام من صليبة العرب أقوام شتى في البلاد قد خرجوا بها عن حكم العرب وصاروا بها أهل حاضرة ساكنة، وعمّار ديار قاطنة</span>. <b>An earlier draft of this book read <i>ṣalība</i> as meaning “those who passed out of Arab status.” It does not.</b> It is the standard genealogical term for unmixed, direct descent — the opposite of <i>mawlā</i> — glossed in the ḥadīth manuals as <span class="ar">خالصة النسَب</span>. The passing-out is not the definition; it is what al-ʿUmarī says has happened <i>to</i> them. <i>Correcting the gloss makes the sentence stronger, not weaker.</i> A caution for anyone checking the page: the Abu Dhabi editor’s own footnote confuses <i>ṣalība</i> with the Ṣulubba of the Syrian desert, an unrelated and genealogically déclassé group, and contradicts al-ʿUmarī’s usage two pages later.')}.
<i>They are still of the purest blood. They have simply stopped being the kind of thing a tribal
register records — because they stopped moving.</i>''',
 f"""
<p><b>This is the mechanism of the void, and it is stated in the fourteenth century by the man
compiling the list.</b> A register of tribes records tribes. A village of farmers is not a tribe. When
a lineage settles, it does not vanish; it changes category, and the category it moves into is one
that nobody was keeping. <i>The silence in the record is not the silence of a people dying out. It is
the silence of a people who stopped being written down by the people whose job was writing down those
who move.</i></p>
<p><b>And then there is the list itself, which this book did not expect.</b> Al-ʿUmarī names where
these settled pure-descent Arabs are, and the places are not in Transjordan. They are
<b>here</b>{c('<i>Masālik al-abṣār</i>, iv.358–59: <span class="ar">فبمدينة غزة وبلد الخليل … معمور بني تميم الداريّ. وبوادي بني زيد فرقة من بني جعفر بن أبي طالب، وفرقة من بني عمر بن الخطاب، وبالقدس منهما، وبنابلس كثير من قحطان وطائفة من مضر بن نزار، وبجينين وبلادها أقوام من حارثة ومن بكر بن وائل</span>; then, further on, <span class="ar">وبالبلقاء منهم ومن بني أمية ومن غسّان … وباليرموك صليبة من غسان … وبحمص قوم من غسّان</span>. The Ghassān notice that al-Qalqashandī later abridged sits <b>inside this same section</b>.')}:</p>
{NUMTABLE('AL-ʿUMARĪ’S SETTLED ARABS OF SYRIA, c. 1340 — the Palestinian entries',
 ['where', 'who he says is there'],
 [['<b>Gaza and the country of Hebron</b>', 'the settlement of Banū Tamīm al-Dārī'],
  ['<b><span class="ar">وادي بني زيد</span> — the Banū Zayd valley</b>', '<b>a section of Banū Jaʿfar b. Abī Ṭālib, and a section of the line of ʿUmar b. al-Khaṭṭāb</b>'],
  ['<b>Jerusalem</b>', 'members of both of those'],
  ['<b>Nablus</b>', 'many of Qaḥṭān, and a group of Muḍar b. Nizār'],
  ['<b>Jenin and its country</b>', 'peoples of Ḥāritha and of Bakr b. Wāʾil'],
  ['al-Balqāʾ · the Yarmūk · Ḥimṣ', '<b>Ghassān</b> — al-Balqāʾ with Banū Umayya, the Yarmūk group named <i>ṣalība of Ghassān</i>']],
 '<b>Wādī Banī Zayd is this district.</b> It is the nāḥiya that contains Dayr Ghassāna, and it lies an hour’s walk from the hill this book is about. <i>Al-ʿUmarī is not naming our family — he names two lineages, and neither is ours.</i> But he is doing something this book had assumed no fourteenth-century source did: <b>naming settled Arab lineages of claimed pure descent, by name, in the Ramallah hills, a hundred and sixty years before Rāshid.</b> The category the family belongs to is in the record. Only the family is not.')}
<p><i>That is the shape of the thing, and it is worth saying plainly.</i> <b>The void is not a void in
the world. It is a void in one column of one kind of document</b> — and al-ʿUmarī, who kept that
column, wrote down in so many words why the people he is describing had begun to fall out of
it.</p>"""),

ent('900 / 1495', 'documents', False,
    'AND THE MAN WHO SHOULD HAVE KNOWN — Mujīr al-Dīn, writing in Rāshid’s own generation',
 f'''<b>Now the evidence on the other side, at full strength.</b> Mujīr al-Dīn al-ʿUlaymī finished
<i>al-Uns al-jalīl</i> at Jerusalem in 900 AH — <b>1495</b>, within a few years of Rāshid’s floruit,
in the city this ridge belongs to, in a book about the country of Jerusalem and Hebron and the people
in it. <b>He mentions the Ghassānids exactly once, in the stock list of the Prophet’s letters to
foreign kings — al-Ḥārith the Ghassānid at Damascus — and nowhere else</b>{c('Mujīr al-Dīn al-ʿUlaymī, <span class="ar">الأنس الجليل بتاريخ القدس والخليل</span>, searched complete in <b>two independent printed editions</b> (the Dandīs and the Najaf texts). <span class="ar">غسان</span> and every inflected form return nothing; <span class="ar">الغساني</span> returns one hit in each, the same sentence: <span class="ar">وأرسل إلى الحارث الغساني بدمشق</span>. <span class="ar">الغساسنة</span>, <span class="ar">الأيهم</span>, <span class="ar">تنوخ</span> and <span class="ar">لخم</span> return nothing at all. <b>Controls prove the search reaches the text</b>: <span class="ar">القدس</span> 363 and 307, <span class="ar">غزة</span> 62 and 55. <i>An earlier draft of this entry said “zero times.” It is once, formulaically, and the difference is printed because anybody can check it in five seconds.</i>')}.''',
 f"""
<p><b>Weigh it honestly.</b> Mujīr al-Dīn is a qāḍī of Jerusalem writing local history and topography
for a local readership. If there were a population in his hills that called itself Ghassān, or was
called so by its neighbours, he is the man in the best position in the world to have said so, and he
had every reason to. <i>He does not.</i> Nor does he name Jafna, or al-Ayham, or Tanūkh, or Lakhm.</p>
<p><b>Weigh it honestly in the other direction too.</b> <i>Al-Uns al-jalīl</i> is a history of two
sanctuaries with an incidental village list, not a census and not a tribal register; it is the same
book that has no Ramallah in it either, at a moment when the registers prove there were households on
the hill. <b>An argument from its silence proves less than it seems to.</b></p>
<p><i>So this book prints both pages and lets them stand against each other.</i> <b>The Mamluk
chancery says Ghassān is a living people, at al-Balqāʾ and the Yarmūk and Ḥimṣ, in about 1300. The
qāḍī of Jerusalem, two centuries later and thirteen kilometres away, has never heard of them.</b>
Both are true. Neither cancels the other, and a family history that printed only the first would be a
worse book than one that prints the second underneath it.</p>"""),

ent('828 / 1424', 'attested', False,
    'THE TRADITION HAS ITS OWN WORD FOR THIS — <span class="ar">نسب القطع</span>',
 f'''<b>Arab genealogical science did not pretend chains were unbroken when they were not.</b> It had a
technical term, and Ibn ʿInaba defines it in his chapter on the vocabulary of the trade: <b>“when
there is a group in some region of whom no report has come, and of whom the genealogists know no
trace, they say — <span class="ar">هم في نسب القطع</span> — their lineage is cut off from connection,
<i>even if they were formerly well known</i>”</b>{c('Ibn ʿInaba (Jamāl al-Dīn Aḥmad b. ʿAlī al-Ḥusaynī, d. 828/1424), <span class="ar">عمدة الطالب في أنساب آل أبي طالب</span>, ed. Muḥammad Ḥasan Āl al-Ṭāliqānī, 2nd ed. (Najaf, 1380/1961), <b>p. 372</b>, in the section <span class="ar">فصل في كلمات تداولتها النسابون في كتبهم</span>: <span class="ar">ومن ذلك إذا كان جماعة في صقع من الأصقاع لم يرد لهم خبر ولا عرف لهم عند النسابين أثر قالوا: (هم في نسب القطع) أي مقطوع نسبهم عن الاتصال وإن كانوا من قبل مشهورين</span>. He ascribes the phrase to <span class="ar">النسابون</span> generally — it is the guild’s word, not his coinage. <b>Not to be confused with</b> <span class="ar">منقطع</span>, the ḥadīth critics’ term for a broken chain of transmission. Pagination from the digital text of the Najaf edition; it should be checked against a printed copy.')}.
<i>That is this family’s situation, described four centuries before anybody in it went looking.</i>''',
 f"""
<p><b>And the tradition attaches a rule to the term.</b> Writing of the Idrīsids of the Maghrib, whose
line had run out of the record in exactly this way, Ibn ʿInaba says: <b>“they are in <i>nasab
al-qaṭʿ</i>; <span class="ar">يحتاج من يعتزى إليهم إلى زيادة وضوح في حجته</span> — whoever traces his
descent to them needs additional clarity in his proof — because of their remoteness from us and our
not being informed of their circumstances”</b>{c('<span class="ar">عمدة الطالب</span>, p. 161: <span class="ar">وبنو إدريس كثيرون وهم في نسب القطع يحتاج من يعتزى إليهم إلى زيادة وضوح في حجته لبعدهم عنا وعدم وقوفنا على أحوالهم</span>. <b>Said of the Idrīsids specifically, not as a general maxim</b> — but the reasoning is general, and it is the reasoning this book has been applying without knowing there was a name for it.')}.</p>
<p><i>Read that sentence again and notice what it is not.</i> <b>It is not a modern sceptic applying
a foreign standard to a pre-modern claim.</b> It is the pre-modern standard, in the pre-modern
vocabulary, set out by a working genealogist of Rāshid’s own century: <i>where the record is cut, the
burden on the claimant goes up.</i> This book has spent nine chapters raising that burden and meeting
what can be met. <b>It turns out to have been following a rule that already existed.</b></p>
<p><b>And the greatest of the Arab historians names our people in the paragraph next door.</b> Ibn
Khaldūn, arguing that pure lineage survives only among Arabs who stayed in the desert, lists those
who did not: <b>“the Lakhm, the Judhām, <span class="ar">وغسّان</span>, the Ṭayy, the Quḍāʿa and the
Iyād — <span class="ar">فاختلطت أنسابهم وتداخلت شعوبهم</span>, their lineages became mixed and their
groups intermingled, and it is known that the genealogists differ about every one of these
houses”</b>{c('Ibn Khaldūn, <span class="ar">المقدمة</span>, Book Two, chapter 9 — <span class="ar">الفصل التاسع في أن الصريح من النسب إنما يوجد للمتوحشين في القفر من العرب</span>; Rosenthal (Bollingen) translates the chapter heading “Purity of lineage is found only among the savage Arabs of the desert and other such people.” <b>The cause he gives is the same one al-ʿUmarī gives:</b> settlement, and contact with non-Arabs. <i>Cited by book and chapter rather than by page, because this project has not verified a page in the Bollingen printing.</i>')}.</p>
<p><b>So the two greatest authorities of the century before Rāshid both say, in their own words, that
a claim of this shape is hard to prove and that Ghassān in particular is one of the lines where it is
hardest.</b> <i>The family’s tradition does not fail a modern test. It fails — and is honest about
failing — a fourteenth-century one.</i></p>"""),

ent('the neighbours’ word for us', 'attested', False,
    'WHAT THE OTHER ARCHIVE CALLS THEM — and why “Ghassanid” may be nobody’s word but ours',
 f'''<b>There is a second body of writing that ought to have our people in it, and it is in Syriac.</b>
Six chronicles were searched for this book. <b>Ghassān appears in none of them.</b> <i>But this is
not a silence about Arab Christians</i> — the same chronicles name living Arab Christian peoples
after the Islamic conquest, by name, in the same country: the <b>Tanūkhāyē</b>, five thousand of whom
were forced to apostatise at Aleppo in 778–9 with the martyr <b>Layth</b> named individually; the
<b>Tuʿāyē</b>; the <b>ʿĀqōlāyē</b> — at Aleppo and Boṣrā, the exact terrain the Jafnids held.''',
 f"""
<p><b>The Syriac writers had a vocabulary for these people and it was not ours.</b> They say
<b><span class="ar">ܛܝܝܐ</span> <i>Ṭayyāyē</i></b>, and when they want a dynasty they build it on the
ruler’s name — <b><i>Bēth Ḥārith</i></b>, the house of al-Ḥārith; <b><i>Bēth Mundhir</i></b>, the
house of al-Mundhir{c('Robert G. Hoyland, “Insider and Outsider Sources: Historiographical Reflections on Late Antique Arabia,” in J. H. F. Dijkstra &amp; G. Fisher (eds), <i>Inside and Out: Interactions between Rome and the Peoples on the Arabian and Egyptian Frontiers in Late Antiquity</i> (Leuven: Peeters, 2014), p. 269; and Greg Fisher &amp; Philip Wood, “Writing the History of the ‘Persian Arabs’,” <i>Iranian Studies</i> 49:2 (2016), 247–90, at 250. <b>Neither states that a form</b> Bēth Ghassān <b>never occurs</b>, and this book will not claim a universal negative it has not proved; what is established is that the form is unattested in the corpus these scholars survey.')}.
<i>A house named for a man, not for a tribe.</i></p>
<p><b>And the Greek and Latin are no better for us.</b> Fergus Millar, after going through the whole
contemporary record from inside the Roman empire, states it flatly: <b>“the entire contemporary
evidence discussed here, literary and documentary, in Latin, Greek, Syriac, and Arabic, from within
the empire does not contain a single expression which equates to, or could properly be translated as,
either ‘Ghassanid’ or ‘Jafnid’”</b>{c('Fergus Millar, “Rome’s ‘Arab’ Allies in Late Antiquity: Conceptions and Representations from within the Frontiers of the Empire,” in H. Börm &amp; J. Wiesehöfer (eds), <i>Commutatio et Contentio: Studies in the Late Roman, Sasanian, and Early Islamic Near East</i> (Düsseldorf: Wellem, 2010), p. 200; quoted by Hoyland (2014), p. 268 n. 3. <b>Note the clause “discussed here”</b> — Millar is scoping to the corpus he has surveyed, and this book quotes him with the clause intact. <i>Seen through Hoyland’s quotation; the Börm and Wiesehöfer volume has not been obtained.</i> What the Roman sources do use is personal: <i>Arethas son of Gabalas</i>, <i>phylarch</i>, <i>patricius</i>, <span class="ar">Σαρακηνοί</span>.')}.</p>
<p><i>Take the measure of that.</i> <b>The state these people served, in all four of its written
languages, never once called them by the name their descendants now carry.</b> “Ghassanid” is a
category out of the Arabic genealogical tradition, applied backwards onto a Roman-period frontier
polity by later writers and then by modern ones. <b>That does not make the Jafnids imaginary — they
are in Procopius, in the inscriptions, in the ruins at Ruṣāfa. It makes the <i>name</i> a
reconstruction.</b></p>
{FIX('“Chabot supplies ‘Ghassanide’ in a nineteenth-century footnote to a text that says <i>Ṭayyāyē</i>” — offered as a worked example of an editor becoming a source.',
 '<b>Withdrawn. The footnote is not there.</b> Chabot’s French translation of Michael the Syrian was searched in full: <b>“Ghassan” and its derivatives occur zero times across all three translated volumes, against 593 occurrences of <i>Taiyayé</i>.</b>',
 'Text and footnotes sit in the same searchable stream, and the vocabulary is plainly being read, so a repeated editorial gloss would have surfaced. <b>The general point survives on Millar, Hoyland and Fisher–Wood; the specific anecdote does not, and is removed rather than softened.</b> <i>The Chronicle of 1234, also edited by Chabot, has not been checked and is where anyone wanting the instance should look.</i>')}
<p><b>One further restraint, and it is an uncomfortable one.</b> The standard modern case for Ghassanid
survival after the conquest is Irfan Shahîd’s. <i>This project has been unable to obtain his volumes
and therefore cannot tell the reader what evidence they rest on.</i> <b>Earlier drafts of this entry
asserted that his case rests entirely on eleventh- to fourteenth-century Arabic literature. That
assertion is withdrawn as unverified</b>, and stays out until somebody reads the books{c('Irfan Shahîd, <i>Byzantium and the Arabs in the Sixth Century</i> (Dumbarton Oaks, 1995–2009), 2 vols in 4 parts — not open access, and not obtained by this project. <b>Named here as an outstanding item so that the gap is visible rather than papered over.</b> The critical reviews by Lawrence Conrad and Mark Whittow are the place to begin an audit of his source base.')}.</p>"""),

ent('the name, tested', 'none', False,
    'FIVE SEARCHES AND WHAT THEY ACTUALLY PROVE',
 'The family’s name, the town’s name, and the neighbours’ names were run against the standing digital corpus of pre-modern Arabic literature. <b>The results are printed with their controls, because a search without a control is not a result.</b>',
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
<p><b>So four of the five zeroes prove nothing, and this book says so.</b> Absence from Shāmila is
absence from a particular kind of writing — the kind that was never going to record us. <i>To read
these blanks as evidence against the family would be to mistake the shape of a library for the shape
of the past.</i></p>
<p><b>The first line is different, and it does cut.</b> Five hundred and fifty-three occurrences of
<span class="ar">الحدادين</span>, and the word is doing the same job in almost all of them: it means
the men who work iron. <b>Any argument that finds “Ḥaddādīn” in an early Arabic text and reads it as
this family is reading a guild.</b> <i>Taken with the register of 1553–54, which calls the group the
Kasābra, the conclusion of chapter ten stands and is reinforced: the family name is late, and the
book will not claim it earlier than it can show it.</i></p>"""),

ent('the clock', 'none', False,
    'THE INTERVAL NOBODY MEASURED FOR US — and a marker that fails on inspection',
 f'''<b>Every number in this book that turns years into generations rests on one assumption, and it is
time to name it.</b> The line is counted at sixty-six because nine hundred and thirty-one years
divided by thirty is thirty-one. <b>Thirty is not a measurement. There is no published male-line
generation interval for any Middle Eastern population</b> — the standard compendium of such studies
runs to French Canadians, Icelanders, north Greenland Inuit, the English, and the Confucius
pedigree{c('The ISOGG wiki’s “Generation length” survey, which is the field’s working list: Tremblay &amp; Vézina (2000) on French Canadians, 34.5 years in the male line; Helgason et al. (2003), Iceland, 31.9; Matsumura &amp; Forster (2008), north Greenland Inuit, 32; King &amp; Jobling (2009), England, 35; the Confucius pedigree, China, 32; and a set of British surname projects. <b>No Arab, Levantine or Middle Eastern population appears anywhere on it.</b> <i>The honest claim is that the standard compendium contains no Middle Eastern population — not that no such study exists anywhere on earth.</i>')}.''',
 f"""
<p><b>What the genetics literature on this region actually does is assume a figure, and say so.</b>
And the figures it assumes are at or below the bottom of the range this book has been printing.</p>
{NUMTABLE('WHAT THE LITERATURE ASSUMES, AND WHAT IT IS ASSUMING IT FOR',
 ['study', 'interval', 'but note'],
 [['Haber et al., <i>PLoS Genetics</i> 9:2 (2013) — the Levant, Palestinians included', '<b>25 years</b>', '<b>autosomal.</b> The 25 calibrates admixture-decay dating, not a male line'],
  ['Fernandes et al., <i>PLoS ONE</i> 10:3 (2015) — Arabia', '<b>25 years</b>', '<b>mitochondrial — the maternal line.</b> It has no bearing on a father-to-son count and this book will not cite it as if it had'],
  ['Haber et al., <i>AJHG</i> 101:2 (2017), with Zalloua — Canaanite and present-day Lebanese', '<b>28 years</b>', 'the closest thing to a regional working figure'],
  ['Zhivotovsky et al., <i>AJHG</i> 74 (2004) — the Y-STR clock itself', '<b>—</b>', '<b>the rate is defined per twenty-five <i>years</i>, not per generation</b>, and the paper offers a per-year conversion. <i>Any date taken from this clock and reported as a number of generations has had an interval smuggled into it.</i>']],
 'Calibrated, in Zhivotovsky’s case, on Maori, Cook Islanders and Bulgarian Roma. <b>Not one of these four studies measured a Middle Eastern father-to-son interval, because none of them set out to.</b>')}
<p><b>So here is the honest output, and it is a range.</b> Nine hundred and thirty-one years across
the void gives twenty-seven generations at thirty-five years, thirty-one at thirty, thirty-three at
twenty-eight, and thirty-seven at twenty-five. <b>The whole line from Adam to Rāshid is therefore
between sixty-two and seventy-two generations, and this book prints sixty-six because sixty-six is
what thirty years yields.</b> <i>Sixty-six is a choice inside a range, not a fact, and every ladder in
this book should be read that way.</i></p>
<div class="fix"><div class="fixhead">And the evidence this family has been told to go and buy</div>
<div style="font-size:.95rem;line-height:1.65;color:#46423B">
<p style="max-width:none"><b>A Y-chromosome subclade called <span style="white-space:nowrap">J-Z640</span> circulates as
“the Ghassanid marker.” It will not survive being looked at.</b> The one paper is a 2019 article in a
journal of the former OMICS International stable, now issued by Hilaris; its evidence base is <b>one
hundred and forty-five samples of which eight are academic</b>, the rest being customers of two
commercial testing firms whose tribal affiliation is <b>self-reported</b>{c('M. Waas, D. Yacobi, L. Kull, V. Urasin, G. Magoon, W. Penninx, A. Brown &amp; I. Nogueiro, “Haplogroup J-Z640 — Genetic Insight into the Levantine Bronze Age,” <i>Journal of Phylogenetics &amp; Evolutionary Biology</i> 7:1 (2019), 1000209. First author at the Department of Jewish History, University of Haifa; a co-author is of YFull.com, <b>whose tree then supplies the date the paper is checked against</b> — not misconduct, but not independence either. <b>On the publisher, a precise statement rather than a loose one:</b> OMICS International is on Beall’s list of predatory publishers and was fined by the US Federal Trade Commission; this title is a former OMICS journal now under Hilaris Publishing SRL. <i>This book does not assert that the present publisher is itself listed.</i>')}.</p>
<p style="max-width:none"><b>And the dating destroys the claim outright.</b> YFull’s own tree puts the
formation of J-Z640 and its most recent common ancestor at <b>4,600 years before the present</b>, with
a confidence interval of 5,000 to 4,100{c('YFull YTree v14.05.00, J-Z640: formed 4600 ybp, TMRCA 4600 ybp, 95% CI 5000–4100. The paper’s own independent estimate is a TMRCA of 4,100 ybp with a range of 4,900–3,300. <b>An earlier draft of this book gave ~3,600 ybp. That figure was wrong and is corrected here.</b>')}. <b>That is the Bronze Age.</b> It is
two thousand years before any Arab tribal genealogy existed to belong to, two and a half thousand
before the Jafnids, and the paper’s own title says as much — it is a paper about <i>Levantine Bronze
Age</i> ancestry. <i>A marker that coalesces twenty centuries before a people exists cannot be that
people’s marker.</i></p>
<p style="max-width:none"><b>And one point of simple fairness to the authors: the paper never says
“Ghassān.”</b> The word does not appear in it, and its own tribal claim — about al-Azd — is expressly
hedged as neither confirmable nor disprovable. <b>The Ghassanid framing comes from the project pages
of a commercial testing service, not from the study.</b> <i>The claim and the paper it is attributed
to are two different objects, and this book separates them.</i></p></div></div>
<p><b>There is a deeper problem underneath all of it, and it is not about this family.</b> <i>No
published study of ancestry has ever sampled Palestinian Christians as a distinct
group.</i>{c('The landmark Y-chromosome study of the population, Nebel et al., “High-resolution Y chromosome haplotypes of Israeli and Palestinian Arabs…,” <i>Human Genetics</i> 107:6 (2000), 630–41 — Hebrew University and Hadassah — is explicit in its own abstract that its 143 subjects are <b>Muslim</b> Arabs. Haber et al. (2013) resolves Lebanese Christians, Muslims and Druze into separate clusters and runs its admixture analysis on each — and then treats Palestinians as a single undifferentiated bloc, lumped with “other Muslim populations as distant as Morocco and Yemen.” <b>Christian Arabs do appear in the Israeli medical-genetics literature as a founder population for disease-allele studies</b> — a recurrent BRCA2 duplication, consanguinity surveys — but that is disease genetics, not ancestry. <i>The only Christian-Palestinian Y-DNA datasets in existence are unpublished citizen-science projects.</i>')} <b>The
question this family would be asking is one the field has never been built to answer.</b></p>
<p><b>And the field has a history that explains some of the reticence.</b> In 2001 <i>Human
Immunology</i> deleted an already-published paper on the origins of the Palestinians from its own
archive and asked libraries to tear the pages out{c('A. Arnaiz-Villena et al., “The origin of Palestinians and their genetic relatedness with other Mediterranean populations,” <i>Human Immunology</i> 62:9 (2001), 889–900 — withdrawn after publication. Reported in <i>Nature</i> 414 (22 November 2001), “Genetics paper erased from journal over political content”; the editor cited political comment in the text. <b>A rebuttal in <i>Nature</i> 415 (2002), 115, argued the paper was also scientifically weak, and this book prints that alongside rather than presenting the episode as purely political.</b>')}. <i>Whatever one
makes of that episode, it is the reason a Palestinian family should approach this literature with its
eyes open</i> — <b>and it is why this book has built its case out of registers, deeds and parish books
instead.</b></p>
<p><b>The recommendation stands, narrowed.</b> Y-DNA testing of this family would still be the only
genuinely new evidence this history can acquire — <i>but it would be worth doing to build a dataset
that does not exist, not to confirm a marker that does not mean what it is said to mean.</i></p>"""),

ent('the shape of the hole', 'documents', False, 'THE VOID IS NOT THIS FAMILY’S FAILURE',
 'One more thing has to be said about the nine hundred years, and it changes what they mean. <b>The family is documented right down to the floor of the archive.</b> The registers that name Rāshid’s children — 1553–54, 1561, 1562, 1565, 1596 — are the <i>first generation of records in which a family of this class could appear at all</i>, anywhere in Palestine.',
 f"""
<p><b>Consider what would have to exist for the void to be filled.</b> Ordinary village families in
Bilād al-Shām do not have documented descent before the sixteenth century, and the ones that do are
not ordinary: they are noble houses with waqf deeds, clerical dynasties with patriarchal archives,
monastic communities with manuscript colophons, or the Cairo Genizah’s Jewish merchants. <b>There
is now a fifth kind, and it is worth naming because it is the closest comparison we have:</b> the
Jerusalem household of <b>Burhān al-Dīn</b>, a middling scholar of the 1390s whose books and papers
survived in the Ḥaram al-Sharīf deposit and can be reconstructed almost item by item — a library, an
estate inventory, a family. <i>He lived a day’s walk from this ridge, in the exact century our own
line is silent.</i> What separates his family from ours is not distance, class or literacy. It is
that somebody deposited his papers in a mosque and somebody else never threw them away{c('Said Aljoumani &amp; Konrad Hirschler, <i>Owning Books and Preserving Documents in Medieval Jerusalem: The Library of Burhān al-Dīn</i>, Edinburgh Studies in Classical Islamic History and Culture (Edinburgh University Press, 2023) — open access. Same corpus, and largely the same team, as the 2024 study of the Ḥaram documents already cited in this book. '+D('2023_Aljoumani_Hirschler_Owning_Books_Medieval_Jerusalem_EUP.pdf')+'.')}. <b>For a
Christian farming family on a highland ridge, the realistic earliest horizon <i>is</i> the Ottoman
cadastre — and this family is in the first one that covers its district.</b></p>
<p><i>So the honest sentence is not “our line goes dark for nine hundred years.” It is: the writing
that could have carried our line does not begin until 1525, and we are in it from the beginning.</i>
<b>The void is not a gap in this family’s history. It is the depth of the archive.</b></p>
<div class="fix"><div class="fixhead">And the hardest thing the record says about the name</div>
<div style="font-size:.95rem;line-height:1.65;color:#46423B">
<p style="max-width:none"><b>The earliest document that records this community does not call it
al-Ḥaddādīn.</b> The register of 1553–54 that finds the group at Bayt Jālā calls them the
<b>Kasābra</b>, and lists thirty-six heads of household by first name and father’s name only. <b>No
occurrence of <span class="ar">الحدادين</span> as a family or clan name anywhere in Bilād al-Shām
has been found before the nineteenth century</b>{c('The 1553–54 register of Bayt Jālā names the group <span class="ar">الكسابرة</span> and lists 36 Christian heads of household by given name and patronymic — Ḥammūdeh (2014), 44–45. On the wider search: no pre-1800 occurrence of <span class="ar">الحدادين</span> as a Levantine Christian family name has been established. The earliest documented naming of a Ḥaddādīn clan at Karak reachable in this project is Latin Patriarchate material of the 1870s–80s; the earliest scholarly record is Peake (1934). <b>Corpora still unsearched, and named here so the negative can be tested:</b> the Jerusalem sharīʿa <i>sijillāt</i> from 1529 onward beyond register 48; the Jerusalem sharīʿa <i>sijillāt</i> from 1529 onward beyond register 48; <b>the unpublished folios of the ʿAjlūn <i>mufaṣṣal</i> behind Hütteroth and Abdulfattah’s summary lines</b>; the Ḥaram al-Sharīf corpus; Franciscan and Greek Orthodox parish registers; and Christian Arabic manuscript colophons at Sinai, Jerusalem, Balamand and Dayr al-Mukhalliṣ. <i>A caution: <span class="ar">الحدادين</span> is not a unique name — there is an unrelated group among the Banū Asad in Iraq — so any hit must be shown to be Levantine and Christian before it counts.</i>')}.</p>
<p style="max-width:none"><i>That is not fatal, and it should not be read as such.</i> Occupational
family names of this kind — <span class="ar">الحدّاد</span>, the smith — generally stabilise as
inherited surnames late, and a register that lists men by father’s name is not a register that would
record a clan name even if one existed. <b>But this book will not print “the family name, in a tax
register, in the sixteenth century” again, because the sixteenth-century register uses a different
name.</b></p></div></div>
<p><b>One more caution, from the family’s own Arabic books.</b> Two clan histories exist in Arabic
that this project does not hold — <span class="ar">عشائر الحدادين حتى عام ١٩٩١م</span> and a later
<span class="ar">عشائر الحدادين</span> launched in Amman. The first <b>explicitly rejects the
blacksmith etymology</b> and offers two alternatives: <span class="ar">تحديد</span>, the demarcation
of the clan’s land in the Shawbak–Karak country, and the Yemeni port of
<b>al-Ḥudayda</b>{c('<span class="ar">خلف خليل حدادين ومنير جريس حدادين وعواد جريس حدادين، عشائر الحدادين حتى عام ١٩٩١م</span>, as reported in <span class="ar">الرأي</span>, 27 November 2007. The book is said to reject the blacksmith derivation and to offer <span class="ar">تحديد</span> — the demarcation of the clan’s land at Shawbak and Karak — and descent from the Yemeni port of al-Ḥudayda. The same article records a Karak tradition of <b>two brothers, Ṣabra and Rāshid</b>, which does not appear in the Ramallah tradition and is worth chasing. <i>This project has not obtained either book; both should be acquired.</i>')}. <i>The first is linguistically strained but at least puts the name on the
plateau; the second cannot carry a sixth-century origin — though not for the reason this book gave
last time.</i><div class="fix"><div class="fixhead">A correction, and a narrow one</div>
<div class="fixgrid"><div><span class="fl">As it stood</span>“al-Ḥudayda is not a place of any consequence before the Ottoman centuries.”</div>
<div><span class="fl">Corrected to</span><b>al-Ḥudayda existed, and was a constituted place, eighty years before the Ottomans reached Yemen.</b> The Yemeni chronicler <b>Ibn al-Dayba’</b> (d. 944/1537) has a <i>ṣāḥib</i> — a lord — of al-Ḥudayda in <b>Shawwāl 859 / September 1455</b>, and in <b>868/1464</b> has <b>its lord, its qāḍī and its resident ascetic</b> ride out together to meet the Ṭāhirid sultan. Three offices, one town.</div>
<div><span class="fl">How it is justified</span>Ibn al-Dayba’, <span class="ar">قرة العيون بأخبار اليمن الميمون</span>, ed. Muḥammad b. ʿAlī al-Akwaʿ, pp. <b>407</b> and <b>413</b>; the second notice reads <span class="ar">فتوجه إليه صاحب الحديدة وقاضيها وزاهدها الشيخ إدريس الجبرتي</span>, with a plural verb for three separate men. <i>EI</i>² III, 539 gives the same 859/1454–5 notice as the town’s first appearance as an inhabited place, citing al-Dayba’ <b>and</b> Abū Makhrama. <b>But the sentence is only half wrong, and this book will not overcorrect.</b> <i>EI</i>² also says al-Ḥudayda “had not yet any strategic importance” when the Mamluks raided it in 1516, stayed secondary to Mocha through the seventeenth and eighteenth centuries, and rose only in the nineteenth; and al-Akwaʿ’s own note on the 1455 passage calls the place a cluster of huts of reed, straw and brushwood. <b>So: wrong about whether al-Ḥudayda existed, right about whether it mattered.</b> <i>And the etymology fails on other grounds anyway — a man from al-Ḥudayda is a</i> Ḥudaydī, <i>not a</i> Ḥaddād.</div></div></div> <b>The family’s own historians disagree with each other
about where its name comes from, and that disagreement belongs in this book.</b></p>"""),

CH(11)

sect('And in our own line', 'One name, carried by tradition alone, at the far edge of the void')
ent('c. 1500', 'oral', True, 'Rāshid al-Ḥaddādīn — generation 66',
 '<b>The last ancestor the family’s own texts name, and the first whose children a document reaches.</b> He himself is in no register: the earliest Ottoman survey of this district is 1525–28, a generation after his floruit. The chart ends at his name, and Shāhīn prints the family’s two accounts of his road — then adjudicates between them{}.'.format(c('Shāhīn (1982), ch. 1, printing ʿAdnān al-Ḥaddādīn’s 1953 manuscript account and Joseph Kaddoura’s 1954 account, with his own adjudication.')),
 f"""
<p><b>The Ḥaddādīn account</b>: the family live at Shobak and Karak among the Kaysoom tribes; the
tyrant demands a Christian daughter for his Muslim son; <b>Sabra Haddad</b> answers with the
unsalted feast — <i>“Treachery, O Haddad!”</i> — and the clan flees by night across <b>al-Lisān, the
ford of the Dead Sea</b>, to Ḥalḥūl, then to the Bayt Jālā country. <b>The Kaddoura account</b>:
Rāshid is a blacksmith — a <i>ḥaddād</i> — who plants forged blades in the ford so the pursuers’
horses turn the water red; he settles first at Bīra beside Sheik Tanash, then <b>buys the wooded
hill next door from the Ghazāwneh</b> for the sake of kindling for his forge. Shāhīn weighs both and
rules: the eldest son was named Haddad — hence the <i>Hadadeh</i> — and <b>Sabra was Rāshid’s
brother</b>, who returned to Karak, where the Karak Ḥaddādīn still count themselves his line.</p>
{fig(ATLAS.fig_karak(),'The road the family actually walked',
 'Karak to the ridge in three documented moves. The southern anchors are the plateau’s Christian record — Shawbak, Karak, and Gharandal, where Ghassān is named in 890; the northern legs are carried by the Ottoman registers. The tradition’s Ḥalḥūl matches the registers’ Kusbār-by-Ḥalḥūl; the tradition’s Bayt Jālā stage is where the 1553–54 defter finds the group; the tradition’s purchase matches endowment land acquiring an owner. Two memories and a tax ledger, telling one story in three voices.',
 'Hammoudeh, Jerusalem Quarterly 59 (2014); Hütteroth and Abdulfattah (1977); Piccirillo (2001); al-Yaʿqūbī.')}"""),

ent('1005 / 1596', 'documents', False,
    'KARAK WAS A CHRISTIAN TOWN — the register says so, and it inverts the picture',
 f'''<b>The Ottoman survey of 1596 counts al-Karak, and the count runs the other way from everything
this family has assumed about the place it came from.</b> Not a remnant under pressure. <b>One hundred
and three Christian households against seventy-eight Muslim</b> — with eight Christian bachelors and
two Muslim — <b>a hundred and eighty-one households, of which fifty-seven in every hundred are
Christian</b>{c('Hütteroth &amp; Abdulfattah, <i>Historical Geography of Palestine, Transjordan and Southern Syria in the Late 16th Century</i> (Erlangen, 1977), <b>p. 171</b>, from the <i>mufaṣṣal</i> of liwāʾ ʿAjlūn, 1005/1596. <b>Karak in this survey is not its own liwāʾ</b> — it is the <i>nāḥiya</i> of al-Karak inside liwāʾ ʿAjlūn, alongside the nāḥiyas of Jibāl al-Karak and al-Shawbak; <i>the register was published by Muḥammad ʿAdnān al-Bakhīt and Nūfān Rajā al-Ḥamūd at Amman.</i> <b>This project has not yet seen p. 171 with its own eyes, and says so.</b> The figures are confirmed to the unit by an independent route: Khalīf Muṣṭafā Gharāybeh, working from the same volume, totals al-Karak at <b>191</b> — which is 78 + 2 + 103 + 8 — and his method checks out against three other entries (al-Shawbak 70, al-Ṭafīla 33, al-Salṭ 70). ' + D('1977_Hutteroth_Abdulfattah_Historical_Geography_Palestine_Transjordan.pdf') + '.')}.''',
 f"""
{FIX('“The Karak and Shawbak <i>tahrir defterleri</i> are not in Hütteroth and Abdulfattah” — printed in this book as a list of corpora still unsearched.',
 '<b>They are, and this book should have known it.</b> Karak and Shawbak are <i>nāḥiyas</i> of liwāʾ ʿAjlūn in the survey of 1596, and their settlements are in the gazetteer at pp. 169–173 like everybody else’s.',
 'The error came of assuming a liwāʾ of Karak-Shawbak because a <i>sanjaqbey</i> of Karak-Shawbak existed as a military office. <b>The political command and the fiscal survey unit were not the same thing.</b> <i>The correction costs this book a line of alibi and gains it a page of evidence.</i>')}
<p><b>Take the caution first, because it is the kind that gets skipped.</b> A <i>tahrir</i> counts
taxable households, not souls. The garrison of the castle, the administrative and military personnel,
and everyone exempt are outside it. And “Christian” here is a <i>fiscal</i> category — the
<span class="ar">نصارى</span> liable to the poll tax — not the finding of a census of belief.
<b>The honest sentence is “a Christian majority of the taxable households in the register of
1596,” and this book will not shorten it to “a Christian town” anywhere it matters.</b></p>
<p><b>But the register is not the first to say it. Three centuries earlier, the Mamluk chroniclers
do.</b> In 700 AH — 1301 — Cairo ordered the Christians of the realm into blue turbans and the Jews into
yellow. At Karak the order was not carried out. Al-Nuwayrī, who served the same state and wrote within
a generation, records the excuse that was made for them: <b><span class="ar">أهل الكرك نصارى وأن
المسلمين بها قليل</span></b> — <i>“the people of Karak are Christians, and the Muslims there are
few”</i> — and that marking them would show strangers how many they were. <b>“And so it remained at
Karak and Shawbak to this day.”</b>{c('Al-Nuwayrī, <i>Nihāyat al-arab fī funūn al-adab</i> XXXI, pp. 418–419: <span class="ar">أهل الكرك نصارى وأن المسلمين بها قليل</span> … <span class="ar">فاستقر ذلك بالكرك والشوبك إلى الآن</span>. Al-Maqrīzī, <i>al-Sulūk</i>, ed. Ziyāda, I/3, p. 912 (= ed. ʿAṭā, II, p. 339): <span class="ar">اعتذر بأن أكثر أهل الكرك نصارى … فلم يغيّر أهل الكرك والشوبك من النصارى العمائم البيض</span>. <b>Cite Ziyāda, not ʿAṭā:</b> Ziyāda marks the part of the sentence he restores from al-Nuwayrī, and the name of the official who made the excuse is not secure. Read in the printed editions for this book, 6 October 2026.')}
<i>A Mamluk official, three hundred years before the Ottoman clerk, and the same picture.</i></p>
<p><b>Now the awkward part, and it deserves a table.</b> <i>The 1596 figure is an outlier against
every later count.</i></p>
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
<p><b>And one sentence of Burckhardt’s has been sitting in plain sight the whole time, running the
family’s road backwards.</b> Of the Karak Christians he writes that they are <b>“for the greater
part, descendants of refugees from Jerusalem, Bethlehem, and Beit Djade”</b> — <b>Bayt
Jālā</b>{c('J. L. Burckhardt, <i>Travels in Syria and the Holy Land</i> (London: John Murray, 1822), <b>p. 381</b>, from his stay at Karak in July–August 1812. The same sentence continues on the Muslims: “settlers from all parts of southern Syria, but principally from the mountains about Hebron and Nablous.” <b>Bayt Jālā is the stage the family’s own tradition puts between Karak and this ridge.</b>')}.
<i>The tradition has the family leaving Karak for Bayt Jālā. Burckhardt has the Christians of Karak
arriving from Bayt Jālā.</i> <b>Two roads, the same two ends, opposite directions — and nothing in
either record says they cannot both have been travelled.</b> Christian families on this plateau moved
in both directions for centuries, and a tradition of flight <i>out</i> and a report of refuge
<i>in</i> are not a contradiction. <b>But this book has been printing one of them and not the other,
and that was a choice it never declared.</b></p>"""),

ent('1908', 'oral', False,
    'MUSIL ASKED THEM HIMSELF — and the Karak Ḥaddādīn name a ruin, not a country',
 f'''<b>Alois Musil did the one thing nobody else did: he went round the lineages of Karak and asked
each of them where it came from.</b> He opens the section flatly — <i>“most of the lineages,
</i><span class="ar">حمايل</span><i>, of the fellāḥīn of el-Kerak are, according to their own family
tradition, immigrants from elsewhere”</i> — and then prints the answers in a
table{c('Alois Musil, <i>Arabia Petraea, III. Band: Ethnologischer Reisebericht</i> (Vienna: Kaiserliche Akademie der Wissenschaften, 1908), section <b>El-Kerak</b>, <b>pp. 84–85</b>; the Christian clan list at <b>p. 99</b>. Fieldwork of 1896–1902. Opening sentence: „Die meisten Geschlechter, ḥamâjel, der Fellâḥîn von el-Kerak sind ihrer Familientradition nach von andersher eingewandert.“')}.
<b>The Ḥaddādīn line reads: <i>El-Ḥaddâdîn, stammen aus <span style="white-space:nowrap">ḫ.
el-Ḥaddâd</span></i> — they come from Khirbet al-Ḥaddād.</b> <i>A ruin. Not a country, and not
Palestine.</i>''',
 f"""
{FIX('This project’s own first reading of the page: “the Karak Ḥaddādīn said they came from <i>b. el-Ḥaddād</i> — a lineage name, Banū al-Ḥaddād.”',
 '<b><span class="ar">ḫ.</span> not <span class="ar">b.</span></b> — Musil’s abbreviation for <i>ḫirbe</i>, a ruin-site. <b>The answer is a place-name: Khirbet al-Ḥaddād.</b>',
 'The page was rendered at 500 dots per inch to settle it; two separate machine transcriptions of the volume had both misread the character. The same glyph stands in <i>el-Ḫalîl</i> — الخليل, Hebron — two lines below, against the visibly different <i>Ḥ</i> in <i>el-Ḥaddâd</i> itself. <b>The correction strengthens the finding rather than weakening it:</b> a lineage name is a claim about ancestry, and a ruin is a claim about ground.')}
<p><b>And the ruin can be found.</b> Musil’s own first volume walks past it: a stage of his itinerary
runs <i>“from Ǧaʿfar to ḫ. el-Ḥaddâde”</i> and the next <i>“from ḫ. el-Ḥaddâde to Mâdaba,”</i> with
the site lying south of Khirbet Abū Ḥammūr, on the wadi that drains the el-Feǧǧ depression — <b>from
which, he notes, the fortress of el-Kerak is in sight</b>{c('Musil, <i>Arabia Petraea</i> I (<i>Moab</i>), itinerary stages at pp. 366 and 369, with the topography in the body of the volume. <b>One caution, and it is real:</b> volume III writes <i>el-Ḥaddâd</i> and volume I writes <i>el-Ḥaddâde</i>. The identification is highly probable and one vowel short of certain, and this project could not corroborate it in any modern gazetteer.')}.
<i>The Karak Ḥaddādīn told Musil they came from a ruin on their own plateau, within sight of their own
castle.</i></p>
<p><b>Then look at the whole table, because the pattern is the finding.</b></p>
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
<p><b>Which puts Musil and Burckhardt on opposite sides of the same question — and this is where the
discipline matters.</b> Musil’s traditions <i>corroborate</i> Burckhardt on the Muslim clans: the
Maʿāyṭa from the Hebron highlands, the Ḍmūr from Hebron and Bani Naʿim, exactly the “mountains about
Hebron and Nablous” Burckhardt names. <b>They fail to corroborate him on the Christians at every
single entry.</b> <i>But Musil never cites Burckhardt, never mentions him, and is not arguing with
him</i>{c('The whole of <i>Arabia Petraea</i> III was searched for <i>Burckhardt</i>, <i>Seetzen</i>, <i>Doughty</i> and <i>Travels in Syria</i>: not one occurrence. Volume III is a report of oral tradition collected in the field, with no engagement with earlier travellers at all. <b>So this is divergence between two independently gathered bodies of evidence, not a correction of one man by another</b>, and it must be written that way.')}.
<b>Two men asked, ninety-six years apart, and got different answers. That is a fact about the
evidence, not a verdict on either of them.</b></p>
{NUMTABLE('FOUR ACCOUNTS OF WHERE THE ḤADDĀDĪN CAME FROM',
 ['account', 'the road it describes', 'when and how it was collected'],
 [['<b>Ramallah’s own tradition</b>', 'Ghassanid Christians, flight from Karak north to this ridge', 'written down 1953 and 1954 from family memory; printed by Shāhīn 1982'],
  ['<b>Burckhardt, 1812</b>', '<b>the opposite direction</b> — the Karak Christians are refugees <i>from</i> Jerusalem, Bethlehem and Bayt Jālā', 'a traveller’s report of local information, on the spot'],
  ['<b>Musil, 1896–1902</b>', '<b>no road at all</b> — the Ḥaddādīn come from a ruin on the Karak plateau itself', 'asked of each lineage in the field and tabulated, published 1908'],
  ['<b>The Karak diwan, 2022</b>', 'Rāshid and his brother Ṣabra go <i>from</i> Karak; Ṣabra returns', 'the Karak family’s own printed statement, at a reception for the Ramallah delegation']],
 '<b>These do not reconcile, and this book will not make them.</b> Two say the family left Karak; one says the Karak Christians arrived from the Bayt Jālā country; one says the Ḥaddādīn never came from anywhere but the next valley. <i>Printed as four, with the date and the method of collection attached to each, they are more use to a reader than any one of them smoothed into a story.</i>')}
<p><i>And notice what survives all four.</i> <b>Every account agrees that the Ḥaddādīn were at Karak,
were Christian, and were numerous enough to be worth an explanation.</b> What none of them can settle
is the direction of travel. <b>The family’s memory of a road is older and more detailed than
anything that contradicts it, and it remains the reading this book prints — now with three other
readings standing beside it, which is what an honest page looks like.</b></p>"""),

ent('three names above Rāshid', 'oral', False, 'WHO WAS RĀSHID’S FATHER? — the two traditions disagree',
 'The chart this project worked from for years ends at generation 36 — and it has been carrying <b>three more names all along, inside that generation’s own title</b>, which this book has never unpacked. John Mogannam writes it in full: <b>Rāshid bin Essaye bin Eyad bin Dhahdouheh al-Ghassani</b> — <span class="ar">راشد بن عيسى بن عياد بن ضهدوحة الغساني</span>{}.'.format(c('John Aziz Mogannam, chart of thirty-six named generations, generation 36, given in full as “Rashed bin Essaye bin Eyad bin Dhahdouheh al-Ghassani.” <b>Earlier editions of this book reproduced the chart as a data table and shortened this to “Rāshid,” silently discarding three named ancestors.</b>')),
 f"""
<p><b>So on the Ramallah side the answer is:</b> Rāshid’s father was <b>ʿĪsā</b>, his grandfather
<b>ʿIyād</b>, his great-grandfather <b>Ḍahdūḥa</b>. <i>Three generations the book has printed on
every copy of the chart and never once read out.</i></p>
<p><b>And on the Karak side the answer is different.</b> The Karak Ḥaddādīn diwan says it in print,
and says it about itself:</p>
<blockquote><span class="ar">راشد بن صقر الحدادين وأبناؤه ونسله، وكان قدم إليها مع شقيقه صبرة بن صقر
الحدادين من الكرك… وما لبث صبرة أن عاد إلى قواعده في الكرك</span><br>
“Rāshid <b>son of Ṣaqr</b> al-Ḥaddādīn and his sons and his line — he came to it with <b>his brother
Ṣabra son of Ṣaqr</b> al-Ḥaddādīn from al-Karak… and before long Ṣabra returned to his bases in
al-Karak.”
<span class="cite">The Karak Ḥaddādīn diwan, at a reception given for the Ramallah municipal
delegation, August 2022{c('<i>ʿAmmūn News</i> (Amman), 30 August 2022, reporting a reception given by Dr Munther Haddadin at his home in Dābūq for the Ramallah municipal delegation led by Mayor ʿĪsā Rajāʾ Qassīs. <b>This is the earliest occurrence of the name Ṣaqr in the Karak tradition that this project can find in print.</b> The same report says Ramallah was built “over five centuries,” which would place the founding about 1520 — and which contradicts a 1561 floruit for Rāshid’s father.')}</span></blockquote>
<p><b>Two things in that sentence are a genuine gain, and this book should say so first.</b> The
Karak side, speaking about itself and without prompting from Ramallah, confirms that <b>Ṣabra was
Rāshid’s brother and not his son</b> — which settles a hundred-year-old disagreement two to one in
Shāhīn’s favour against Kaddoura — and it confirms that <b>Ṣabra went back</b>. <i>The two ends of
the tradition, written down independently on opposite sides of the Jordan, tell the same story about
the same two men.</i></p>
<div class="fix"><div class="fixhead">And then they name different fathers</div>
<div class="fixgrid">
<div><span class="fl">Ramallah says</span>Rāshid <b>bin ʿĪsā</b> bin ʿIyād bin Ḍahdūḥa — the
Mogannam chart, generation 36.</div>
<div><span class="fl">Karak says</span>Rāshid <b>bin Ṣaqr</b>, brother of Ṣabra bin Ṣaqr. <b>This is
not a 2022 novelty.</b> Ḥammūdeh prints <i>Rāshid bin Ṣaqir al-Ḥaddādīn</i> in 2014, on the authority
of <b>Khalīl Abū Rayya (1980)</b>; the Karak diwan is the fullest statement of it, not the
first.</div>
<div><span class="fl">What this book does</span><b>Enters Ṣaqr at generation sixty-five</b> and
prints ʿĪsā beside him, because the wheel that carries Ṣaqr agrees with Ramallah on four other points
and our own chart’s three names agree with nobody. <i>It is a judgement, not a proof, and it is
reversible.</i> <b>ʿIyād and Ḍahdūḥa have no independent attestation anywhere</b> — <span class="ar">ضهدوحة</span> returns nothing
at all as a personal name, and its shape is that of a Levantine nickname rather than a given name;
it may be a copying slide from the well-known Christian name <span class="ar">الدحداح</span>. <b>And
Ṣaqr is not attested in any <i>document</i> at all</b> — not in Peake, not in Kaḥḥāla, not in any
Ottoman register. He is well attested in the Arabic family literature from Abū Rayya (1980) onward,
<i>which is why he is drawn in a broken outline on every ladder in this book: named by the tradition,
named by nobody's clerk.</i>{c('Checked and negative for both names: F. G. Peake, <i>History and Tribes of Trans-Jordan</i> ii, the Karak clan tables; Kaḥḥāla, <span class="ar">معجم قبائل العرب</span>, s.v. <span class="ar">الحدادين</span>; the Jordanian clan registers, which all carry one recycled sentence from Peake and no genealogy; and <span class="ar">الرأي</span>, 27 November 2007, digesting <span class="ar">عشائر الحدادين حتى عام ١٩٩١م</span> — which uses no date between the seventh century and 1937. On <span class="ar">عياد</span>: an ordinary and well-attested Levantine Christian name, from <span class="ar">عيد</span> — its very ordinariness argues mildly for authenticity, since nobody inserts it for prestige.')}</div>
</div></div>
<div class="fix"><div class="fixhead">One reading that would make both traditions right</div>
<div style="font-size:.95rem;line-height:1.65;color:#46423B">
<p style="max-width:none"><b><span class="ar">صقر</span> — “falcon” — is a byname, not a baptismal
name.</b> No Christian of sixteenth-century Karak was christened Ṣaqr; Levantine men of this period
routinely carry a given name and a byname, and a family diwan on the east bank is exactly the kind of
memory that keeps the byname and loses the given name, while a genealogy written in Ramallah is
exactly the kind that does the opposite. <b>If Ṣaqr and ʿĪsā are one man, both traditions are
right</b> — and generation sixty-five is <i>ʿĪsā, called Ṣaqr</i>.</p>
<p style="max-width:none"><i>This book cannot prove that and does not assert it.</i> It is set down
because it is testable: a single Karak or Ramallah document giving both names together would settle
it, and because it is the only reading yet proposed under which nobody in this argument is wrong.
<b>Grade: conjecture. It is not entered in the ladder.</b></p></div></div>
<div class="fix"><div class="fixhead">The date at the centre of the Karak chart cannot mean what it looks like</div>
<div style="font-size:.95rem;line-height:1.65;color:#46423B">
<p style="max-width:none">The radial chart reproduced in the family’s own presentation carries
<b><span class="ar">صقر — عام ١٥٦١</span></b> at its hub. <i>Read as Ṣaqr’s lifetime, that is
impossible on the family’s own evidence.</i> <b>Ṣaqr is Rāshid’s father. Rāshid’s grandchildren
brought the Kasābra up the ridge road in 1562, with forty-five further Christian households behind
them.</b> A father cannot flourish in
1561 and have great-grandchildren founding a town the following year.</p>
<p style="max-width:none"><b>It lands on a document.</b> On <b>1 April 1561</b> three men of this
community — Ghunaym bin Sālim <i>al-Kasbūrī</i>, Mūsā bin Baraka and Isḥāq bin Yaʿqūb — stand in a
Jerusalem court and swear to plough this hill, and the qāḍī divides Ramallah in thirds between them
and the Muslim householders. <i>A hub date sitting exactly on the earliest document in which these
families can be found is a document date, or a compiler’s back-count from one — not a birth
year.</i> There is no apparatus in Ottoman Karak that could produce a birth year for a
Christian villager of the 1500s. <b>This book prints 1561 as a date of unknown reference and will
not enter it as a lifetime.</b></p>
<p style="max-width:none"><b>What the rest of that chart does say is the subject of the next
entry</b> — and it is a good deal better than a caution. Read outward from the hub, as a radial
genealogy is meant to be read, the Karak wheel is coherent, it is generous to Ramallah, and on four
separate points it says what Ramallah says.</p></div></div>"""),

ent('the Karak wheel, read outward', 'oral', True, 'THE KARAK CHART, READ PROPERLY — four points where the two sides agree',
 f"""The chart on the Karak side is a wheel: <b>Ṣaqr at the hub, and every ring outward is a
generation down</b>. Read that way — which is the way it was drawn — it is not a rival to Ramallah’s
account. <b>It is a second copy of it, kept for four hundred years on the other side of the
Jordan.</b>{c('<b>Munther Haddadin, <span class="ar">دولة الغساسنة؛ أصيلها ورحيلها</span> [<i>The Ghassanid State: Its Origin and Its Departure</i>] (Amman: <span class="ar">دار ورد الأردنية للنشر والتوزيع</span> / Dār Ward al-Urduniyya, 2024), ISBN 978-9923-76-975-1</b> — the radial chart of the El-Ḥaddādīn clan of al-Karak, plate 84: about one hundred and sixty names in six hand-drawn rings, with the compiler’s own line picked out in green. Reproduced in the family presentation of 2026, which is where this project first met it. <i>The presentation’s English caption — “El-Haddadeen Tribe, Origins and Branches, Warda Books, 2025” — is a loose rendering of that book, not a second book: “Warda Books” is <span class="ar">دار ورد</span>, and the year is one out.</i>')}""",
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
<p><b>So what does it actually give us about Rāshid?</b> Four things it says that Ramallah says too —
and one on which the two sides part.</p>
<div class="fix"><div class="fixhead">Where Karak and Ramallah agree</div>
<div class="fixgrid">
<div><span class="fl">His brother</span>Ṣabra is Rāshid’s <b>brother</b>, and Ṣabra <b>went back</b>.
John Mogannam argued his way to exactly this against Kaddoura — <i>&ldquo;Sabra must have been
Rashed’s brother&rdquo;</i> — from Ramallah, without the Karak chart in front of him.{c('John Aziz Mogannam, <i>The Ramallah Family Tree Book</i>, ch. 2, p. 18: “Second, it appears that Sabra Haddad was the one who returned to Karak… all the Haddadeen in Karak claim that they are descended from Sabra… Sabra must have been Rashed’s brother.” Kaddoura, <i>Taʾrīkh Rām Allāh</i>, makes Ṣabra Rāshid’s <i>son</i> and puts him at the head of the five. <b>The Karak wheel settles it three to one.</b>')}</div>
<div><span class="fl">His five sons</span><b>Ḥaddād, Ibrāhīm, Jiryis, Shuqayr, Ḥasan</b> — the same
five names, in the same order, as the Ramallah tradition’s own division of the land into
fifths.{c('The Karak wheel, inner arc below Rāshid: <span class="ar">حداد · ابراهيم · جريس · شقير · حسن</span>. Mogannam, p. 18: “the children of Rashed Haddad were five: Haddad, Ibrahim, Jirius, Shukair, and Hassaan,” and ch. 8 for the clan chart built on them. The only difference is orthographic — Karak writes <span class="ar">حسن</span>, Ramallah <span class="ar">حسان</span>.')}</div>
<div><span class="fl">Where he went</span>The chart writes <span class="ar">رام الله</span> under his
name. <i>The Karak side records the destination.</i></div>
<div><span class="fl">That the line ends there</span>Rāshid’s branch stops at the five sons. A chart
written to claim Ramallah would have carried it on; this one lets it go and keeps counting its
own.</div>
</div></div>
<p>Set beside the entry before this one, the balance is worth stating plainly. <b>On his brother, his
sons, his destination and the shape of the parting, the two traditions agree — independently, in two
languages, on two sides of the Jordan.</b> They disagree on exactly one thing: <b>his father</b>. And
on his grandfather the Karak side is silent altogether — <i>the wheel has nothing above Ṣaqr at
all</i>, so ʿIyād and Ḍahdūḥa stand or fall on the Mogannam chart alone.</p>
{FIX('Kaddoura: Ṣabra was Rāshid’s son, and the eldest of the five.',
 '<b>Ṣabra was Rāshid’s brother</b>, and the eldest of the five was <b>Ḥaddād</b>.',
 'Four independent witnesses now say so: <b>Khalīl Abū Rayya (1980)</b>; Shāhīn (1982); <b>Ḥammūdeh (2014)</b>, who prints it from the Arabic literature; and the Karak wheel, which puts Ṣabra beside Rāshid at the hub and Ḥaddād first among the sons — with John Mogannam reaching the same conclusion by argument from the clan names, p. 18, without any of them in front of him. <b>Kaddoura’s reading is retired, with thanks — it is the reason the question was ever asked.</b>' + c('Kaddoura, <i>Taʾrīkh Rām Allāh</i>; Shāhīn (1982), ch. 1; Mogannam, ch. 2, p. 18; the Karak wheel, plate 84.'))}
<p><i>One caution survives all of this.</i> The wheel is <b>undated except at its hub</b>, it was
first published in this form in the twenty-first century, and its compiler is a living man with a
Ramallah audience. That does not make it wrong — a family diwan is exactly the kind of source that
keeps this material — but it means the agreement above is the agreement of <b>two traditions</b>, not
of two documents. <b>No Ottoman register names Rāshid, Ṣabra or Ṣaqr.</b> That has not changed.</p>"""),

sect('What the ground says', 'The state begins writing down every household in every village on this ridge')
ent('1517–1554', 'documents', False, 'The registers begin — and close in on the founding',
 'Ottoman conquest, 1517. In <b>1525–28 the site of Ramallah is uninhabited</b> — agricultural land of the Ibrāhīmī waqf, exactly the legal status the 1279 deed describes. Four Muslim households appear by 1538–39. And in <b>1553–54 the group called the Kasābra — 36 Christian households — is registered at Bayt Jālā</b>, twenty kilometres south. <i>They are not yet at Ramallah.</i>{}'.format(c('The pre-1596 registers come from Ḥammūdeh (2014), pp. 40–47, working from the Istanbul <i>tapu tahrir</i> series; <b>Hütteroth and Abdulfattah (1977) published only the 1005 AH / 1596–97 <i>mufaṣṣal</i> registers</b> (TK 72, 100, 112, 181, 185, 192, Tapu ve Kadastro archive, Ankara), and earlier editions of this book wrongly credited the whole series to them. '+D('1977_Hutteroth_Abdulfattah_Historical_Geography_of_Palestine.pdf')+'.'))),

CH(12)
sect('The ground and the line, together', 'From this page on there is only one story: the family is in the land, and the land is in the documents')
ent('1 April 1561', 'documents', False, 'THE PEOPLE OF RAMALLAH SPEAK — six men, a qāḍī, and a promise to plough',
 f"""<b>A year before the census, and this is the first document in which the people of this place
speak for themselves.</b> On <b>16 Rajab 968 — 1 April 1561</b> the judge Abū Wafā al-Ḥanafī, sitting
in Jerusalem with Ḥusām al-Dīn bin Yaʿqūb, deputy overseer of the Ḥaram al-Sharīf, is approached by
six men <b>“all of them from the village of Ramallah”</b>{c('Sāmiḥ Ḥammūdeh, “New Light on Ramallah’s Origins in the Ottoman Period,” <i>Jerusalem Quarterly</i> 59 (2014), pp. 47–48, translating the Jerusalem sharīʿa court record of 16 Rajab 968 AH. ' + D('2014_Hammoudeh_New_Light_Ramallah_Ottoman_JQ59.pdf') + '. <b>This entry did not exist in earlier editions of this book, which had the article on the shelf and read it for its register tables only.</b>')}.""",
 f"""
<div class="ntwrap"><div class="nthead">Named in court, Jerusalem, 1 April 1561</div>
<table class="ntable"><tr><th>who</th><th>which community</th><th>and elsewhere</th></tr>
<tr><td><b>ʿAlī bin Ḥasan</b> and his brother <b>ʿUmar</b></td><td>Muslim, of the Labūd house</td><td>the Labūd are among the four Muslim households of 1538–39</td></tr>
<tr><td><b>Aḥmad bin Muḥammad Qarʿala</b></td><td>Muslim, of Abū al-Thanā</td><td>—</td></tr>
<tr><td><b>Ghunaym bin Sālim</b>, <i>al-Kasbūrī</i></td><td>Christian</td><td><b>in the Bayt Jālā list of 1553 and the Ramallah list of 1562</b></td></tr>
<tr><td><b>Mūsā bin Baraka</b></td><td>Christian</td><td><b>in the Bayt Jālā list of 1553</b></td></tr>
<tr><td><b>Isḥāq bin Yaʿqūb</b></td><td>Christian</td><td><b>in both registers — one of the nineteen</b></td></tr>
</table></div>
<p><b>Read the third column again.</b> All three Christians are men this book has already tracked
through the registers, and one of them carries the road in his own name: <b><i>al-Kasbūrī</i></b> — of
Kusbār, the stage by Ḥalḥūl that the family’s tradition names. <i>The oral tradition and the court
record are using the same word for the same people.</i></p>
<blockquote>They swore an oath that from that day on they will develop the lands of the same village,
and that none of them will farm any other land until all of its lands were cultivated. Should any of
them violate this, he pledges to pay one hundred gold <i>sulṭānī</i> to the charitable kitchen of our
prophet Khalīl al-Raḥmān.
<span class="cite">Jerusalem sharīʿa court, 16 Rajab 968 / 1 April 1561, in Ḥammūdeh (2014), p. 48</span></blockquote>
<p><b>And then the court divides the hill in three.</b> One third to ʿAlī bin Ḥasan, his brother
ʿUmar, Aḥmad bin Muḥammad and their people — the Muslims who were already there. One third to
<b>Ghunaym and his people</b>. One third to <b>Mūsā and Isḥāq and their people</b>. <i>Two thirds of
Ramallah to the newcomers, one third to the men who had held it, agreed in front of a judge and
guaranteed against a fine.</i></p>
<p><b>This is the entry this book was missing.</b> Not a sultan, not a king, not a genealogy: six
farmers standing in a Jerusalem court, promising to plough one hill and no other until it was all
under crop, and dividing it between two religions by agreement. <b>The Ramallah tradition remembers a
division of the land into fifths among Rāshid’s five sons. The court record of 1561 shows a division
into thirds, a year earlier, between Muslims and Christians.</b> <i>Both can be true — one is the
arrangement with the neighbours, the other the arrangement inside the family — and only one of them
is on paper.</i></p>
{FIX('The founding of Ramallah begins in 1562, with the census.',
 'It begins in <b>1561</b>, with an oath — and the people who swore it are named.',
 'The census of 970/1562 records a population; the court record of 968/1561 records a decision. <b>Fourteen months before the clerk counted them, these families had already agreed with the Muslim householders how the hill would be worked and had bound themselves to it in a Jerusalem court.</b> That is what founding a town actually looks like, and it is the reason this book now dates the settlement from 1561 and the count from 1562.' + c('Ḥammūdeh (2014), pp. 47–48. The register of 970/1562 is the count; sijill 48, p. 88 (1565) recites the endowment; the court record of 968/1561 is the agreement. Three instruments, three different things, and earlier editions of this book used only the first.'))}"""),

ent('1562', 'documents', True, 'THE FOUNDING',
 '<b>The thirty-six Christian families the register calls the Kasābra, recorded at Bayt Jālā in 1553–54, come up the ridge road</b> — and they are not alone when they arrive. <b>The register of 1562 lists seventy-one Christian entries at Ramallah — sixty-four households and seven unmarried men — against the ten Muslim households already living on the hill</b>{}.'.format(c('The detailed Ottoman census (<i>tapu tahrir mufaṣṣal</i>) of 970/1562, in Ḥammūdeh (2014), pp. 45–47. Ramallah’s revenue was assigned to endowment, but the document is a fiscal cadastre, not a waqf register, and earlier editions of this book called it one.')),
 f"""
{fig(R.fig_datings(),'Five datings for one town — and they are not rivals',
 'The founding of Ramallah has five different dates attached to it, resting on five different kinds of evidence. Read in order rather than argued over, they describe one coherent sequence: a site that was named endowment land in 1279, uninhabited in 1525, held by a few Muslim households by 1538, bought from the Ghazāwneh by tradition, and settled by the Christian families in 1562. <b>The family did not name the hill. The family settled a hill that already had a name.</b>',
 'Sijill 48, p. 88 (1565, citing a waqf of 1279); Mujīr al-Dīn (1495); the defters of 1525–28 to 1596; al-Dabbāgh; Shāhīn (1982).')}
{fig(R.fig_neighbourhood(),'Ramallah among its neighbours, 1596',
 'The town in its own district in the register of 1596–97. <b>Ramallah at eighty households is one of the larger villages of the nāḥiya</b> — bigger than al-Bīra’s forty-five, nearly four times Jifnā’s twenty-one — and one of only a handful with a Christian majority. <i>This is the company the family kept for the next three hundred years.</i>',
 'Hütteroth and Abdulfattah (1977), pp. 114–21, the nāḥiya of Quds, 1596–97 defter. Note that they record Jifnā as Muslim; Toledano (1984), p. 312, corrects this — the village was wholly Christian in every sixteenth-century defter.')}
{fig(R.fig_households(),'The households, counted',
 'Ramallah in the Ottoman registers of the sixteenth century: from uninhabited endowment land, to a handful of Muslim households, to a village of eighty households — seventy-one Christian and nine Muslim — paying 9,400 akçe, all of it to the endowment. The arrival of 1562 is a visible step. <b>Hütteroth and Abdulfattah publish the 1596 register as counts; the register itself is a <i>mufaṣṣal</i> and names all eighty heads of household, and nobody has yet gone to Ankara for them.</b> The family names we do have come earlier and separately, and that is the hardest fact in this book: <b>al-Kasābra in the Bayt Jālā register of 1553–54, Rāshid’s descendants in a Jerusalem court deed of 1561 and the census of 1562, al-Naqqāsh in a court record of 1604</b>.',
 'Ḥammūdeh, Jerusalem Quarterly 59 (2014), pp. 45–48, for the registers of 1525–28 to 1562 and the court documents; Hütteroth and Abdulfattah (1977), p. 121, for 1596–97.')}
{FIX('The family settled Ramallah “about 1550” (Shāhīn), under Rāshid and his five sons (Kaddoura).',
 '<b>1562</b>, and the movers were <b>Rāshid’s grandchildren</b>.',
 'The detailed census of 970/1562 records the arrival; the 1553–54 register still shows the group at Bayt Jālā; and Hammoudeh’s archival work shows the last leg made by the grandsons, the popular version compressing three generations into one. <b>A remembered date replaced by a documented one twelve years later costs the tradition nothing — and that the memory was only twelve years out is itself evidence of its quality.</b>' + c('Hammoudeh, “New Light on Ramallah’s Origins in the Ottoman Period,” <i>Jerusalem Quarterly</i> 59 (2014). '+D('2014_Hammoudeh_New_Light_Ramallah_Ottoman_JQ59.pdf')+'.'))}
{FIX('Karak “still holds 143 Christian households” in 1562 (as printed in earlier editions of this book).',
 'The documented figure is <b>103 Christian households and 8 Christian bachelors — beside 78 Muslim households and 2 bachelors — at al-Karak in 1596</b>, in the nāḥiya of Karak, Sanjak of ʿAjlūn: register TK 185, Ankara, published in Hütteroth and Abdulfattah (1977), p. 171.',
 'The 1596 count can be pointed to in a named register; the 1562/143 figure was carried second-hand from “the same survey series” and no folio has been produced for it. <b>It is not discarded — it is demoted to unverified</b>, so that a future researcher chases it rather than assuming it was dropped without cause.' + c('Ottoman Defter 185, the Karak register of 1596: 103 Christian households and 8 Christian bachelors. The 143 figure previously printed here awaits a register reference and should not be repeated until one is produced.'))}
<p>Three years later the hill’s legal position is stated in open court. On <b>29 June 1565</b> the
qāḍī of Jerusalem enters into <b>sijill 48, p. 88</b> the fact of an endowment of 678 AH: this ground
belongs to the Ibrāhīmī sanctuary at Hebron. <i>That is not a title for the family.</i> <b>It is the
reason there was room on the hill at all</b> — endowment land, worked by tenants, with the tithe going
south to Hebron and not to a landlord. <i>The family did not name the hill. The family settled a hill
that already had a name, and paid Hebron for the privilege.</i></p>
<p><b>And a second register, kept by a different office for a different purpose, counts the same
seventy-one.</b> The endowment survey of the district of Jerusalem, delivered to the treasury in 970 —
1562–63, the same year as the census — lists Ramallah on its first folio, under the endowment of
Hebron: <b>the whole village, and “71 persons at 80 akçe, 5,680”</b> from its Christians. Bayt Jālā
on the same folio has 218 at the same rate, matching the census there too{c('<i>Defter-i Evkaf-ı Liva-i Kuds-i Şerif</i>, ed. Sevgi Işık (Ankara: Tapu ve Kadastro Genel Müdürlüğü, 2015), an edition of TKG.KK.TTd. 406 (old no. 514/539), folio 1, under <i>Vakf-ı Hazret-i Halīlü’r-Rahman</i>, publication p. 73: <i>Karye-i Ramallah … tamāmen</i>, <i>hāsıl maʿa rüsūm</i> 2,905; <i>Deyr-i Nasārā der-karye-i Ramallah, 71 neferen fī 80 = 5,680</i>. The editor reads the word before <i>Nasārā</i> as <i>deyr</i>; the per-head charge at 80 akçe is the pattern of the Christian poll tax. <b>The edition prints a transcription only, without the Ottoman page, so the word has not been checked against the folio.</b> ' + D('1562_Defter_Evkaf_Kuds_TKGM.pdf') + '.')}.
<i>Two registers, two offices, one number.</i></p>"""),

ent('1553 and 1562, name by name', 'documents', True, 'THE REGISTERS DO GIVE NAMES — all one hundred and nine of them',
 f"""<b>Every household head in both registers has been sitting in this project’s own book for thirty
years.</b> Chapter four of the co-authors’ <i>Ramallah Family Tree Book</i> prints the facsimiles of
Register 289 and Register 516 and, beside each, a full English transliteration: <b>the 36 Christian
households at Bayt Jālā in 1553–54, and the 10 Muslim households, 63 Christian households and 8
bachelors at Ramallah in 1562–63</b>. <i>One hundred and nine households and eight unmarried men, by name
and by father’s name.</i>{c('John Mogannam, <i>The Ramallah Family Tree Book</i>, ch. 4, charts 1–4: facsimiles of Register 289, cols. 79–80 (Bayt Jālā, 961 AH / 1553–54) and Register 516 (Ramallah, 970 AH / 1562–63), each with his own English transliteration. <b>Earlier editions of this book worked from Ḥammūdeh’s counts and never opened the charts beside them.</b> The transliterations carry his query marks and alternative readings, which are kept here exactly as he set them down.')}""",
 f"""
{fig(F4.fig_registers(),'The same people, nine years apart',
 'Both lists in full. <b>Nineteen of the thirty-six households the clerk recorded at Bayt Jālā in 1553 appear again at Ramallah in 1562 under the same name and the same father</b> — Ishaq bin Yaʿcoub, ʿAmeera bin Hassaan, Jareer bin Hadeed, Farah bin Suweid, Musa bin Braik, Khaleel bin Sadaqa, Kaʿoosh bin Zayed, Suweidan bin Khaleel and eleven more. <i>That is not an argument. It is the same men, on two pieces of paper, nine years apart.</i>',
 'Registers 289 and 516, transliterated by John Mogannam; matching and counts by this edition.')}
{FIX('“The registers give counts, not names.”',
 '<b>Not true of any of them.</b> All three are <i>mufaṣṣal</i> — detailed — registers, and a <i>mufaṣṣal</i> names every household head with his father’s name. <b>The eighty names of Ramallah in 1596 are still in Ankara, unread.</b>',
 'The claim confused the register with the book about it. What gives counts and not names is <b>Hütteroth and Abdulfattah’s published tabulation</b> of the 1596 defter, not the defter itself: an <i>icmāl</i> register gives a settlement and a revenue, a <i>mufaṣṣal</i> gives every household head and his patronym, and all three of these are <i>mufaṣṣal</i>. <b>The correction is not a new source. It is a shelf this book had not read to the end — and a folio in Ankara nobody has asked for.</b>')}
<p><b>What the nineteen prove.</b> The identification of the <span class="ar">الكسابرة</span> of Bayt
Jālā with the Christians who founded Ramallah has until now rested on Ḥammūdeh’s reading of the two
registers together — a good argument, and an argument. <b>It can now be shown name by name.</b> More
than half the households move as a body; the rest are the ordinary attrition and accretion of nine
years, and the Ramallah list is larger because forty-five further Christian households and seven
unmarried men are on it who are not on the Bayt Jālā list at all.</p>
<p><b>And here is a small thing that turns out to answer an open question.</b> Ḥammūdeh, reading
the same register, counts <b>twenty-seven further Christian families and eight unmarried men</b>;
the family’s own transcription of the folio counts <b>forty-five further households and seven</b>.
<i>The two readings differ about the households because Ḥammūdeh takes the twenty-seven as coming
from Bayt Jālā with the rest, and the transcription simply counts the names on the page. But they
agree exactly on the total: <b>seventy-one Christian entries</b>.</i> <b>The disagreement is one
line.</b> Ḥammūdeh reads it as a bachelor; the transcription reads it as a household{c('Sāmiḥ Ḥammūdeh, <i>Jerusalem Quarterly</i> 59 (2014), on register I.S. 516: the 36 Kasābra households of Bayt Jālā, “accompanied by an additional 27 Christian families also from Bayt Jala and eight unmarried Christian men,” joining “the ten Muslim families residing in Ramallah.” <b>He nowhere prints a total.</b> 36 + 27 = 63 households and 8 bachelors, against the 64 and 7 in the family’s own transcription of the same folio — and 63 + 8 = 64 + 7 = 71 either way. <b>This retires the “eighth bachelor” from this book’s open questions: he exists, and he is the entry the two readings disagree about.</b>')}. <i>This is the strongest documentary moment in the whole book, and it
was in the house.</i></p>
<div class="fix"><div class="fixhead">And now the hard part</div>
<div class="fixgrid">
<div><span class="fl">Nobody is called Rāshid</span><b>Not one of the sixty-four Christian household
heads at Ramallah in 1562 bears the name Rāshid</b>, and not one of them is recorded as the son of a
Rāshid.</div>
<div><span class="fl">Which the book expected</span>This is what it should look like if the movers
were Rāshid’s <b>grandchildren</b>, as Ḥammūdeh argues and this book follows. Their fathers would be
Rāshid’s sons, and it is the sons’ names we should be looking for in the patronymics — <i>not
Rāshid’s.</i></div>
<div><span class="fl">And there they are — carefully</span>As fathers in the 1562 list:
<b>Ḥassān 5, Hadeed 3, Ibrāhīm 3, Jiryis 1, Shuqayr 0</b> — twelve households out of sixty-three.
<b>Ḥassān and Ibrāhīm are two of the commonest names in the Levant and prove nothing.</b> Jiryis is
one household. Shuqayr is absent altogether. <i>The one worth chasing is Hadeed.</i></div>
</div></div>
<p><b>And the name itself has a Palestinian and Jordanian literature this book had not used.</b> <span class="ar">الحدادين</span> is <i>the blacksmiths</i>, and <b>Hind Abū al-Shaʿr</b> shows that Christian families of Transjordan specialised in the trade and carry the name to this day — with nineteenth-century travellers meeting Christian blacksmiths in the villages of ʿAjlūn in 1868, 1877 and 1884, Tamīmī and Bahjat recording that most Nablus Christians were blacksmiths or leather-dyers, and the Jerusalem court records of the seventeenth century treating blacksmithing as an exclusively Christian trade{c('Hind Abū al-Shaʿr, <span class="ar">تاريخ شرق الأردن في العهد العثماني</span> (Amman: Jordanian Ministry of Culture, 2010), p. 364; Rafīq al-Tamīmī and Muḥammad Bahjat, <span class="ar">ولاية بيروت</span> (1917), p. 123; Maḥmūd ʿAṭāllah on seventeenth-century Jerusalem; all cited in Ḥammūdeh (2014), n. 52. <b>The family name is an occupation, and the occupation was a Christian one in this country. That is not a lesser origin than a dynasty; it is a better-documented one.</b>')}. <i>A trade name is not a pedigree, and it does not contradict one — but it is the explanation the record actually supports, and it should be printed first.</i></p>
<p><b>Which sharpens the register question.</b> <span class="ar">حديد</span> and <span class="ar">حداد</span> — “iron” and
“blacksmith” — are the same root, one letter apart, and in an Ottoman clerk’s hand in an unpointed
register they are barely distinguishable. <b>John transliterated it Hadeed.</b> And it is not new in
1562: <b>Jareer bin Hadeed is in the Bayt Jālā register of 1553 as well</b>, one of the nineteen who
make the move. <i>If that reading is right, the family name is in a document nine years before the
town exists</i>{c('Jareer bin Hadeed appears in both registers; Ghneim bin Hadeed and Ghanayem bin Hadeed appear at Ramallah in 1562. <b>The reading cannot be settled from a transliteration.</b> It requires the Arabic of Registers 289 and 516 — the Istanbul <i>tapu tahrir</i> series, I.S. 289 and I.S. 516 — read for the pointing. Until then this is a lead, not a finding, and it is exactly the kind of surname resemblance this book warns against three eras earlier, in the <span class="ar">الحدادة</span> entry.')}.</p>
{FIX('A finding.',
 '<b>A lead, and the trap named beside it.</b>',
 'This book has already refused one attractive surname match — al-Suwaydī’s <span class="ar">الحدادة</span>, an unrelated North African group — on the ground that a resemblance between a clan name and an ancestor’s name is not evidence of anything. <b>The same rule applies here, to our own advantage rather than against it.</b> Ḥadīd is worth the trip to Istanbul, where registers 289 and 516 are; Ankara holds the 1596 mufaṣṣal. It is not worth a sentence in the family’s history until somebody makes it.')}
<p><b>One number to keep.</b> The ten Muslim households of 1562 are named too — Khaleel bin Hassaan,
ʿAmeer bin ʿOmar, Hasan bin ʿAta, Ahmad bin Muhammad and six more. <b>They were on the hill first,
and the register puts them at the head of the page.</b> This book has said since the fourth edition
that Muslims were never absent from Ramallah. <i>It can now say who they were.</i></p>"""),

ent('after 1562', 'oral', True, 'The five sons, the eight clans',
 'The land is divided in fifths among <b>Haddad, Ibrahim, Jirius, Shukair and Hassaan</b> — Jirius, unsatisfied, gets the extra parcel called Karm ʿAli — and Haddad’s fifth is divided again among his own five sons{}.'.format(c('Shāhīn (1982), ch. 1: the fifths, Karm ʿAli, and the eight clans — four Hadadeh (Sharaka, Jaghab, Yousef, ʿAwwaad-with-ʿAzzouz) and four Hamayel.')),
 f"""
<p>Out of the double division comes the shape every Ramallah family still knows: <b>eight clans —
four Hadadeh and four Hamayel</b>. The names carry the sixteenth century inside them: the
<b>Sharaka</b> are simply “the easterners”; the <b>Jaghab</b> are named for their ancestor shouting
at a stubborn ox at the trough — <i>“Drink, or I will break your horn!”</i> A community that still
organises its conventions in Detroit by these names is organising itself by a joke shouted at an ox
four hundred years ago. <i>That is not a weakness of the record. It is the record.</i></p>
{fig(F3.fig_clans_tree(),'One man, five sons, eight clans — and a town',
 'The social structure of Ramallah in a single diagram, with each clan’s population from the ration-card census of 1944. Nearly four centuries after the division of the land, a British administrator issuing ration books could still count the town by Rāshid’s grandsons.',
 'Shāhīn (1982), ch. 1, for the fifths, Karm ʿAli and the clan etymologies; the 1944 ration-card census for the counts.')}"""),

CH(12)

ent('1671 · 1700 · 1706', 'documents', True, 'The parish proves itself — in Arabic and in Greek',
 'Ramallah workers help repair the roof of the Church of the Nativity in 1671; <b>Yaʿqūb Ilyās of the Yousef clan is ordained in 1700</b>, the first Ramallah native priest; and in 1706 a Ramallah priest earns 20 piasters a month teaching parish boys to read <i>Arabic and Greek</i>{}. The check exists: <b>the Patriarchate’s own registers, printed by Papadopoulos-Kerameus, name Ramallah in 1706 and 1709</b>{}. <i>A Greek publication of 1894 and an Arabic family history of 1982 describe the same parish in the same decade, and neither knew of the other.</i>'.format(
  c('Shāhīn (1982), the seventeenth-century chapter and the 1706 salary record, there credited to Kaddoura.'),
  c('Papadopoulos-Kerameus, <i>Analekta Hierosolymitikēs Stachyologias</i>, II–III (St Petersburg, 1894–97).'))),

ent('c. 1750', 'oral', False, 'The influx begins — and never stops',
 '“Ramallah became a prosperous town and attracted other families... The influx began about 1750.”{} First the ʿAjlounys from ʿAjlūn; the Hishmeh by way of al-Jazzār’s walls at Acre about 1775; the Nazzal from Rafidia about 1805; the ʿAraj, Zagroot and Shahla from Deir Aban about 1810 — each given land, each folded into a clan. <b>The town absorbed its arrivals exactly as the land had always absorbed its own</b> — and in 1923 <b>Muhammad El Jaʿooni, a plumber, is remembered as the first Muslim to buy land and build inside the town itself</b> — though Muslim households are in the tax registers from 1538, nine of the eighty in 1596, and the British census counted 125 Muslims here in 1922{}.'.format(c('Shāhīn (1982), ch. 2, “Outsiders Who Settled in Ramallah,” with the dates and circumstances of each family’s arrival, and the first Muslim resident in 1923.'),
  c('Against the tradition: Ḥammūdeh (2014), pp. 41–42, names Muslim household heads at Ramallah from 1538 — Ḥasan ibn ʿAlī al-Labūd and his sons, Rajab ibn Yaʿqūb, Muḥammad ibn Abī al-Thanāʾ; Hütteroth and Abdulfattah (1977), p. 121, count nine Muslim households of eighty in 1596; Barron, <i>Census of Palestine 1922</i>, counts 125 Muslims in Ramallah. <b>What 1923 records is a first Muslim purchase inside the town, not a first Muslim.</b>'))),

ent('1834', 'documents', False,
    'THE PEASANTS’ REVOLT — the year the shaykhs of these hills were destroyed, and Jifnā paid for it',
 f'''The single largest political event in this hill country between the Ottoman conquest and the reforms, and no earlier edition of this book mentioned it. In April 1834 <b>Ibrāhīm Pasha ordered conscription — one man in five</b> — on top of a new head tax, the <i>farḍa</i>, and the disarming of the villages. <b>The men who rose were the shaykhs ordered to enforce it</b>{c('Beshara Doumani, <i>Rediscovering Palestine: Merchants and Peasants in Jabal Nablus, 1700–1900</i> (California, 1995), pp. 33–34: the rural leaders “began to greatly resent their exclusion from the Advisory Councils… This resentment turned to rebellion when they were ordered to implement the highly unpopular measures of disarming and conscripting the peasantry, as well as collecting a new head tax, the <i>ferde</i>.” '+D('1995_Doumani_Rediscovering_Palestine_Jabal_Nablus.pdf')+'. On the Egyptian measures from the Arabic side: <span class="ar">الموسوعة الفلسطينية</span>, “<span class="ar">الحكم المصري ١٨٣١–١٨٤٠</span>” — 3,000 conscripts demanded from each of the districts of Jerusalem, Nablus and Hebron, and a <i>farḍa</i> of 15–50 piastres a year.')} — Qāsim al-Aḥmad of Jammāʿīn, and with him the shaykhly houses of this district.''',
 f"""
<p>Jerusalem was besieged in May by something like twenty thousand men and taken through a sewer
near the Dung Gate. Ibrāhīm marched up from Jaffa with nine thousand troops; by August the rising
was broken at Dayr al-Ghuṣūn and at Hebron, and Qāsim al-Aḥmad had fled to <b>al-Karak</b> — the town
this family’s own tradition comes out of — where a seventeen-day siege ended with the place
destroyed and Qāsim handed over{c('Judith Mendelsohn Rood, “The Time the Peasants Entered Jerusalem: The Revolt against Ibrahim Pasha in the Islamic Court Sources,” <i>Jerusalem Quarterly</i> 27 (Summer 2006), 28–43, DOI 10.70190/jq.i27.p28 — read directly for this edition, and the source of every quoted detail here. Her own evidence is the Jerusalem Islamic court records and the chronicle of the Greek Orthodox monk <b>Spyridon</b>, resident in the city, at his pp. 88–92. Her fuller narrative is <i>Sacred Law in the Holy City</i> (Brill, 2004), pp. 123–34, which this project has <b>not</b> read; where a detail rests on the book alone it is flagged. Eugene Rogan, <i>Frontiers of the State in the Late Ottoman Empire</i>, pp. 31–32, for the flight to al-Karak and the siege.')}. <i>The road the family says it came up in the sixteenth
century is the road the revolt’s last leader went down in the nineteenth.</i></p>
<p><b>Two shaykhs of the Ramallah highlands were beheaded for it</b> — <b>ʿAbd al-Jābir
Barghūthī</b> of Banī Zayd, whose seat was Dayr Ghassāna, and <b>Ismāʿīl ibn Simḥān</b> of Rās
Karkar{c('R. A. S. Macalister and E. W. G. Masterman, “Occasional Papers on the Modern Inhabitants of Palestine,” <i>PEF Quarterly Statement</i> 37 (1905), 343–356. <b>Earlier editions of this book reported that the sources disagreed about which <i>nāḥiya</i> the Samḥān headed. They do not; the confusion was a table.</b> Macalister and Masterman at p. 354 divide Banī Ḥārith in two: of the <b>northern</b> half the ruling family is <b>Simḥān</b>, “chief sheikh, Ismāʿīl (killed by Ibrāhīm Pasha in 1834),” with chief towns el-Jāniyah and <i>er-Rās</i> — and their own footnote adds “also called Rās Karker.” Its villages include <b>Jifnā</b>, Bīr Zayt, Dayr ʿAmmār, Surdah and Abū Kash. Of the <b>southern</b> half the ruling family is Kaʿraja, seated at Bayt Ibzīʿ. <b>Banī Zayd is a separate nāḥiya</b>, the Barghūthīs’ own, seated at Dayr Ghassāna. A widely circulated table collapses the two halves into one row and parks Rās Karkar in Banī Zayd, citing Doumani p. 35 — where no such table exists; Doumani’s only nāḥiya table is for Jabal Nablus in 1850 and contains none of these names. The Institute for Palestine Studies study of the Abū Ghūsh family confirms the reading: Shaykh Samḥān “was the shaykh of the Banī Ḥārith nāḥiya,” controlling the northern part of the Jerusalem mountains. Ramallah itself sat in <b>Jabal al-Quds</b>, in the quarter administered from al-Bīra, and is listed there among “the other villages of this district” — not as a seat.')}. <b>And the village of this district that paid for it is a Christian one.</b>
Edward Robinson rode into Jifnā four years later and wrote down what he found: a village entirely
Christian, forty-two taxable men, perhaps two hundred souls — and this sentence.
<i>“After the rebellion of 1834, twenty-six men were taken to Egypt and put into the public works,
whence they have never returned. Not long since, one of their two priests went to Egypt to look
after them, and died there.”</i>{c('Edward Robinson and Eli Smith, <i>Biblical Researches in Palestine, Mount Sinai and Arabia Petræa: A Journal of Travels in the Year 1838</i>, vol. III (Boston: Crocker &amp; Brewster; London: John Murray, <b>1841</b>), pp. 78–79. Robinson spells the village <i>Jufna</i>. <b>Cite the 1841 edition: the 1856 second edition renumbers the volumes and this material sits elsewhere.</b> Robinson gives no motive, no accusation and no trial, and he does not describe a rising at Jifnā — the deportation follows the general rebellion. Jifnā’s connection to it is administrative: the village belonged to the northern Banī Ḥārith, whose paramount shaykh Ismāʿīl Simḥān was executed by Ibrāhīm Pasha in the same year.')}</p>
<p><b>Read that carefully, because this book had it wrong four hours ago and the error is
everywhere.</b> The version in general circulation says twenty-six men were <i>exiled for their
alleged participation</i>, and that <i>two priests joined them voluntarily</i>. <b>Neither is in
Robinson.</b> The men were <i>put into the public works</i> — taken for forced labour, not sent into
exile — and they <b>never came back</b>. And the village had two priests; <b>one</b> of them went to
Egypt <i>afterwards</i>, on a pastoral errand, to look after them — <i>and died there.</i>
<b>The phrase that generated the error is “one of their two priests.”</b> Somebody read the two and
dropped the one.</p>
<div class="fix"><div class="fixhead">A correction this book makes to itself, within a day of printing it</div>
<div class="fixgrid">
<div><span class="fl">As it stood</span>Twenty-six men of Jifnā were exiled to Egypt for their part in the rising, and two of their priests went with them voluntarily.</div>
<div><span class="fl">Corrected to</span><b>Twenty-six men of Jifnā were taken to Egypt and put into the public works, and never returned. One of the village’s two priests went afterwards to look after them, and died there.</b></div>
<div><span class="fl">How it is justified</span>Robinson and Smith, 1841, III.78–79, read directly. The superseded reading came to this book through a summary of a summary, and it is the reading printed by the general reference works. <i>It is worth saying what the difference is: the received version makes Jifnā a village of rebels who were punished. What Robinson describes is a village stripped of twenty-six men for a rebellion he does not say they joined — and a priest who followed them into Egypt and did not come home either.</i></div>
</div></div>
<p><b>Which matters, because it cuts against the easy story.</b> On <b>31 May</b>, the day after
Ibrāhīm Pasha re-entered Jerusalem, his soldiers attacked <b>Bayt Jālā</b> — the village this
family came up from in 1562 — and killed <b>thirty-three Christian men and women</b>, on suspicion
of looting{c('Rood, <i>Jerusalem Quarterly</i> 27 (2006): “The following day the village of Bayt Jala was attacked by soldiers and 33 Christian men and women were killed on suspicion of looting.” Her source for the Bayt Jālā and Bethlehem episodes is the chronicle of the monk Spyridon, pp. 88–92. <b>Note the pretext: not rebellion, looting.</b>')}. Christian shops in Jerusalem were looted along with Muslim and Jewish
ones, in the same three days. And after the suppression, conscription was extended to Christians as
well. <i>1834 was a revolt of tax-farming shaykhs and their villages against a centralising state, in
which confession was a variable and not the axis.</i>{c('On the looting of 23–24 May: Rood (2004), p. 128 — “virtually every Muslim, Jewish and Christian-owned shop was raided and damaged.” On conscription extended to Christians after the revolt: Joel Beinin, <i>Workers and Peasants in the Modern Middle East</i>, p. 33. <b>A claim this book will not print:</b> that Bethlehem’s Muslim quarter was destroyed in reprisal on 1 June. It circulates widely, sourced to Rood’s 2004 book at p. 130; her own article says something else for that date — that the Taʿāmira armed themselves to defend Christians in Bethlehem against looting Khedival troops — and this project could not read the book. <b>Withdrawn pending the page.</b>')} <b>Ramallah and al-Bīra
themselves appear in no account of that year that this project has found.</b> Shāhīn records only
that Ibrāhīm Pasha occupied the town without resistance and that its hundred and fifty families fed
his oxen and got them back.</p>
<p><b>And here is what 1834 did to the country the family lives in.</b> It destroyed the
<i>people</i> who ran the throne-village system — the <span class="ar">شيخ الناحية</span>, the
tax-farming lord of a group of villages, ruling from a fortified <i>qaṣr</i>. <b>The institution
itself took another thirty years to die</b>, and it was killed by paperwork rather than by cannon:
the urban advisory councils, the Land Code of 1858, the Vilayet Law of 1864, and the appointed
<i>mukhtār</i> who replaced the shaykh{c('Doumani, <i>Rediscovering Palestine</i>, pp. 111–12 and 169, for the sequence — merchant credit hollowing out the subdistrict chiefs before 1834, the Egyptian councils after it, and the permanent assertion of central authority around 1860; Suad Amiry, <i>Space, Kinship and Gender</i> (PhD, Edinburgh, 1987), p. 43, for the transfer of authority to urban notables and appointed <i>mukhtārs</i>, after which “the influence of their throne villages all but disappeared by the beginning of the twentieth century.” On the throne villages of these hills: Riwaq — Centre for Architectural Conservation, Ramallah, <i>Qurā al-Karāsī</i>.')}.
<i>The Qays–Yaman war of 1844 that the next entry describes therefore sits inside an interregnum</i>
— after the shaykhs were beheaded and before the new administration arrived. <b>That is this book’s
own reading, offered as a reading</b>: no source consulted draws the connection, and the reader is
free to refuse it.</p>
<div class="fix"><div class="fixhead">And what it says about Ramallah’s own standing</div>
<div style="font-size:.95rem;line-height:1.65;color:#46423B">
<p style="max-width:none"><b>Ramallah is on no list of throne villages, and it has no shaykhly house
in any of them.</b> The seats of this hill country were Dayr Ghassāna and Abwein for Banī Zayd,
Dayr Ibzīʿ or Rās Karkar for Banī Ḥārith, Qaryat al-ʿInab for Banī Mālik. Ramallah was registered in
1596 not under a tribal <i>nāḥiya</i> at all but directly under the <i>nāḥiya</i> of al-Quds, with
its revenue assigned to endowment. <i>It was a waqf village, not a lordship.</i></p>
<p style="max-width:none"><b>But this is an argument from silence and the book says so.</b> Sāmiḥ
Ḥammūdeh, who has read the registers, states plainly that the period between about 1600 and 1800 is
almost entirely undocumented for this town. <i>Ramallah is absent from the lists. That is not the
same as having been proved to be nothing.</i></p></div></div>"""),

ent('1820 · 1834 · 1844', 'oral', True, 'Feuds, a Pasha, and a faction',
 'The ʿAzzouz incident of 1820 scatters the whole town to eight villages for months; Ibrāhīm Pasha occupies Ramallah in 1834 <b>without resistance</b> — about 150 families, who feed his army’s oxen and get them back; and in the Qays–Yaman fighting of 1844, <b>Ramallah is the Qays headquarters</b>{}.'.format(c('Shāhīn (1982), ch. 3: the ʿAzzouz incident and the village-by-village dispersal; Ibrāhīm Pasha’s occupation; the 1844 war — the sixteen-man garrison at Beitunia, Suleiman El Samhan’s killing of Taha Abu Ghosh, Patriarch Keirollus’s intervention, and Abu Ghosh’s year of exile in Constantinople.')),
 FIX('“No source found in this research assigns Ramallah itself to Qays or to Yaman” (the family presentation).',
 '<b>Ramallah was the Qaysī headquarters in 1844.</b> Beitunia, next door, was the Yemeni one — and the Shakara declared themselves Yemen simply to protect their lands near Beitunia.',
 'Shāhīn (1982) devotes a chapter to the 1844 war and assigns the town explicitly. The deeper point survives him: the faction language was genealogical, but families chose sides for local reasons — descent language in this country has always described belonging as much as biology.')),

ent('1850', 'documents', True, 'The present Greek Orthodox church is built',
 'On the site of the first church of 1807, built by Fr Mitry Elias Kassees near the present bus station{}. <b>And it is built out of an older one.</b> The dressed stone was carried up from the Byzantine church at Khirbet et-Tireh, on the western edge of the town — Guérin, here about 1870, was told the church had been built eighteen years before “partly with the remains of an ancient church of Kharbet et-Thireh,” and the excavator of et-Tireh confirms that in 1850 the Orthodox community “robbed out a large number of trimmed stones” to build it{}. <i>The town’s church stands on a church the town’s people had prayed in a thousand years before the family arrived.</i> In August 2015 the bones from et-Tireh’s crypt were carried to this church in procession and buried there{}.'.format(
   c('Shāhīn (1982): the 1807 first church and its builder; the present church of 1850; the outstanding-dates list confirms both.'),
   c('V. Guérin, <i>Description de la Palestine: Samarie</i> II (Paris, 1875), ch. XXXIV–XXXV: “Ils y ont élevé, il y a dix-huit ans, une église, construite en partie avec les restes d’une ancienne église du Kharbet et-Thireh”; and of et-Tireh, the old church “a été complètement démoli, il y a un petit nombre d’années, pour servir à la construction de l’église grecque de Ram-Allah.” Its apse still stood in 1863. S. H. A. al-Houdalieh, “The Byzantine Eastern Church of Khirbet et-Tireh,” <i>Archaeological Discovery</i> 4 (2016), 48–67, the section on the dismantling of the walls. ' + D('1875_Guerin_Description_de_la_Palestine_Samarie_II.pdf') + ' · ' + D('2016_Houdalieh_Byzantine_Church_Khirbet_et-Tireh.pdf') + '.'),
   c('Al-Houdalieh (2016): the skeletal remains from the graves were carried “on 4 August 2015 in a solemn funeral procession to the Greek Orthodox Church in Ramallah, where a requiem was celebrated,” at the request of the Patriarchate.')),
 FIX('The present church, built <b>1852</b> (as circulated in the family’s materials).',
 '<b>1850 is the date carved on the portal</b> — most naturally the start of building — and Shāhīn gives 1850 too. <b>Published sources generally give 1852 for the inauguration.</b> Both can be true.',
 'A datestone records when a stone was cut, not when a church opened. This book prints 1850 for the building and notes 1852 for the inauguration, rather than claiming to have overturned the published date.')),

ent('1857–1895', 'attested', True, 'The town acquires its churches and its schools',
 '<b>In 1867 a Ramallah girl of fifteen named Miriam Karam stopped Eli and Sybil Jones in a narrow street and asked them for a school for girls.</b> They asked who would teach it. <i>“I will,”</i> she said — and she could, having been schooled at the Deaconesses’ in Jerusalem, out of a family of teachers. It opened in 1869 with twenty pupils and had fifty within months; it became a boarding school, <b>the Girls Training Home</b>, in 1889, and took the name <b>Friends Girls School</b> in 1925{}. <i>That is the shape of the whole century.</i> The missions came to Ramallah because Ramallah’s people asked them for things and then ran what they were given: the Latin school of 1857–58, Bishop Gobat’s Protestant school of about 1848–50, the Sisters of St Joseph with a girls’ school and a free clinic in 1873, St Andrew’s in 1887, and Our Lady of the Annunciation in 1895 under <b>Fr Yaʿqūb Mughannam</b>{}. <b>Six denominations in fifty years, in a town of two thousand.</b>'.format(
  c('Shāhīn (1982): Miriam Karam’s exchange with Eli and Sybil Jones; the boarding school of 1889 (15 pupils, first principal Katie Gabriel — who gave the school forty-one years, eighteen as principal and more than twenty as matron); the boys’ boarding school of 1901 under Elihu Grant. <b>The Quaker accounts date the street encounter to 1867 and the opening to 1869, and make Miriam fifteen and already schooled at the Deaconesses’ in Jerusalem. The renaming to Friends Girls School is dated 1925 by the school’s own history; earlier editions of this book printed 1919.</b>'),
  c('Shāhīn (1982), the education and denominations chapters, with the dates of each school and church; the Catholic mechanism of close-relative marriages and the 150 Catholics of 1870. <b>The Latin Patriarchate dates its Ramallah school to 1858; St Andrew’s at 1887 is carried by Shāhīn alone and no diocesan record for it has been found.</b>'))),

ent('the 1800s', 'oral', True, 'How the town actually lived',
 'Before the schools, the clinics and the steamships, Ramallah was a farming village of stone cottages built wall to wall for safety, whose people spent the summers in the fig groves and the winters around a clay oven. <b>Shāhīn wrote all of it down</b> — and it is the world every emigrant in this book carried in his head.',
 f"""
<p><b>The guest house.</b> Each clan kept a <i>madafa</i> — a large upper room in the clan leader’s
house where the men gathered in the evening over coffee to settle disputes, appoint the village
watchman and shepherd, and argue about the harvest. At first the whole town had one; then two, one
for the Hadadeh and one for the Hamayel; then, as the clans grew, <b>each of the eight had its
own</b>{c('Shāhīn (1982), ch. 4, “Social Gatherings; the Guest House.” The oldest known photograph of Ramallah’s inhabitants — the ʿAwwaad clan seated outside their madafa, c. 1890 — hangs enlarged in Ramallah’s City Hall.')}. A distinguished guest was given a <i>mensaf</i>: a wooden bowl big enough for
fifteen loaves, bread soaked in lamb broth, a deep layer of rice, and an entire leg of lamb — the
<i>shadah</i> — laid on top for the guest of honour. <b>Twenty to thirty pounds of meat</b>, eaten
with the hands, in three sittings: the men and the guest first, then the older children, then the
women{c('Shāhīn (1982), ch. 4, on the mensaf and the order of eating. The <i>shadah</i> reappears in the 1844 story of Esa Abu Misleh, who seized the sheikh’s hand rather than surrender it.')}.</p>
<p><b>The oven, and the news.</b> Bread was baked in a <i>taboon</i> — a domed clay oven in its own
stone hut, floored with smooth pebbles, heated three times a day with dry manure and hay, never
allowed to go out because relighting took two days. Five or six families shared one and baked in
turns. <b>In winter the women gathered there for warmth and talk, and the Arabic of Ramallah
acquired a phrase for gossip: <i>tawabeen news</i></b> — what you heard at the oven{c('Shāhīn (1982), ch. 4, “The Taboon.” <i>Tawabeen</i> is the plural of <i>taboon</i>.')}.</p>
<p><b>The summer house.</b> From the fig harvest the whole family moved out to the <i>qasr</i>, a
two-storey drystone tower in the groves: provisions and the drying figs below, sleeping quarters
above, a wide window to watch the trees from, and <b>a thick belt of thorn branches around the upper
floor in place of barbed wire</b>{c('Shāhīn (1982), ch. 4, “Agriculture,” with the photograph of a qasr taken in 1955.')}. The 1920 crop gives the scale of that world: 84,000 kilograms
of olive oil, a million and a half kilograms of dried figs, 1.2 million of grapes. Shāhīn, writing
in 1982, adds the line that dates his own generation: <i>“Eighty percent of the land is now
uncultivated. The generations that worked the land have passed away and, alas, the land too is
passing away.”</i></p>
<p><b>A wedding took a week.</b> Three steps came first — the <i>tulbeh</i> (the formal asking), the
engagement, and the buying of the <i>kissweh</i> in Jerusalem and Bethlehem — and then Monday to
Sunday of dancing: the men’s <i>mel‘ab</i> in two facing rows around a fire, the henna on Saturday,
and on Sunday the <i>zaffa</i> to the church, the bride on a horse <b>holding a sword in both hands
to signify that the family would defend its honour with one</b>{c('Shāhīn (1982), ch. 4, “Marriage Arrangements” and “The Wedding.” The dowry about 1900: fifty French gold pieces, worth $3.80 each; half that for a widow.')}. Because the Orthodox
church forbade marriage inside fourth or fifth cousins, three or four families would arrange a ring —
a son of A marrying a daughter of B, a son of B a daughter of C, a son of C a daughter of A —
<i>so that everyone married in, and the church still approved</i>.</p>"""),

ent('the church year', 'oral', True, 'The festivals — how faith was actually kept',
 'Ramallah’s calendar ran on the Julian reckoning of the Greek Orthodox church, with three fasts a year: Lent, forty-eight days; the fortnight of Saint Mary in August; and forty days before Christmas.',
 f"""
<p><b>Palm Sunday belonged to the young.</b> The girls of the town, between fifteen and
twenty-five, put on their best embroidered dresses — or borrowed their mothers’ and aunts’ — and went
to the threshing floor, where they formed <b>two rows of fifteen to twenty, twenty metres apart</b>,
and danced toward each other and back, singing, for most of the day, with the whole town
watching{c('Shāhīn (1982), ch. 4, “Festivals and Holidays.” He notes that the Palm Sunday dances are among the fondest memories of Ramallah women living in the United States.')}. <i>Shāhīn records that it is the memory Ramallah women in America keep
longest.</i></p>
<p><b>Holy Light Saturday belonged to the whole town.</b> Three or four men walked to the Church of
the Holy Sepulchre in Jerusalem, lit a candle at the flame, sealed it in a lantern and <b>carried it
back on foot</b>. The head priest, the clergy, the choir and most of the town waited at the edge of
Ramallah with unlit candles; when the light arrived the church bells rang, everyone lit from it, and
the young men led the procession in a chant with rhyme and metre. Easter itself — <i>el-Hajmeh</i>,
“the sudden rising” — began at one in the morning and ran till four or five{c('Shāhīn (1982), ch. 4; he prints the Holy Light chant in Arabic. He also records, of the years after 1967, that “it is celebrated in a subdued manner.”')}.</p>
<p>Every day of Holy Week had its own name, translated literally out of the Arabic: <b>Long Monday,
God’s Tuesday, Job’s Wednesday, Washing-of-the-Feet Thursday, Sad Friday, Holy Light Saturday, and
Easter Sunday, the great feast of joy</b>. And before Easter the town made a deliberate effort to
reconcile anyone who had quarrelled during the year — <i>a custom Shāhīn notes was still kept when he
wrote</i>.</p>"""),

ent('1883', 'attested', False, 'The first doctor the town ever had',
 'Ramallah’s first doctor was a foreigner at the Friends clinic in 1883 — Dr George Hassenauer, whom the town renamed <b>Dr Ḥassan Nawwār</b> because it could not say his name{}. Its second was its own. <b>From 1891, Dr Philip Asʿad Maʿlūf — <i>Ḥakīm Abū Iskandar</i> — covered the whole district alone for twenty-five years.</b> He pulled the twelve-year-old ʿAzīz Shāhīn through forty days of typhoid in 1906; <i>the book you are reading exists because of it.</i> He died in the typhus of 1916, treating it. Before them both: midwives, bloodletting, hot-oil massage and charms, and a three-hour donkey ride to Jerusalem.'.format(c('Shāhīn (1982), “Medical Treatment”: Hassenauer (1883–89), the C.M.S. ladies and Dr Croper (to 1910), Dr Maʿlouf (1891–1916), and the author’s own illness of 1906.'))),

ent('c. 1900', 'oral', False, 'What a day was worth',
 'Shāhīn preserves the town’s whole price system — and it prices every decision in this story, including the decision to leave.',
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
    'THE TWIN TOWN, AND A FAMILY THAT TELLS OUR STORY BACK TO US — the Rafeedie of al-Bīra',
 f'''One and a half kilometres from the centre of Ramallah there is a second town, older than ours, larger than ours in every Ottoman register, and Muslim where ours is Christian. <b>And living in it, from some point in the nineteenth century, is a Christian family called <span class="ar">الرفيدي</span> — the Rafeedie</b>, who came to al-Bīra from the village of <b>Rafīdiyā</b> in the Nablus district, and whose name is simply that village worn into a surname{c('Sāmiḥ Ḥammūdeh (Birzeit University), <span class="ar">البيرة في فترة الاحتلال والانتداب البريطاني ١٩١٧–١٩٤٨</span>, in <i>Shuʾūn Filasṭīniyya</i>: al-Bīra’s Mandate-era population was the continuation of families settled there in the Mamluk and Ottoman periods — al-Ṭawīl, al-Qarʿān, al-Ḥamāyil, al-Ghazāwna — <span class="ar">وعائلة الرفيدي المسيحية، وقد وفدت إليها من قرية رفيديا، قضاء نابلس في العهد العثماني، في القرن التاسع عشر</span>: “and the Christian Rafeedie family, which came to it from the village of Rafīdiyā, Nablus district, in the Ottoman period, in the nineteenth century.” Ḥammūdeh is the author of <i>Ottoman Ramallah</i> (Institute for Palestine Studies) and of the 2014 article this book’s founding chapter is built on — he is the same historian, reading the same kind of register, for the town next door. <b>An honest qualification, added after the endnotes were obtained: Ḥammūdeh’s note on this sentence (endnote 9) is an explanatory aside about the 1948 refugees, not a citation, and he gives no source for the Rafeedie’s arrival from Rafīdiyā.</b> The nearest reference in the passage is his note 8, to Muṣṭafā Murād al-Dabbāgh, <span class="ar">بلادنا فلسطين</span>, vol. 8 pt. 2, p. 258, which supports the family-names list but which he does not attach to this sentence. <i>The claim is printed here as Ḥammūdeh’s assertion, on his authority as the historian of Ottoman Ramallah, and not as a documented finding.</i> The article appeared in <i>Shuʾūn Filasṭīniyya</i> 275–276 (2019); Ḥammūdeh died on 25 May 2019, aged 59, before the series of city studies he had planned could go further.')}. <i>They are worth a page of this book, and not out of neighbourliness.</i>''',
 f"""
<p><b>Because the Rafeedie carry our own story, told back to us in a different town’s voice.</b>
Rafīdiyā’s account of itself is this: a <b>Christian family of Ghassanid descent fled al-Karak</b>
to escape a forced marriage between one of their women, <b>Rafīd</b>, and a Muslim prince; they
settled beside Nablus and divided the land and the water with the Muslim family already there{c('The Rafīdiyā foundation account, in the form it circulates locally and in the reference literature: a Ghassanid Christian family in flight from al-Karak over a forced marriage, settling beside Nablus alongside the Ḥassūna family, with land and water divided equally. It is a tradition, and it is printed here as one.')}.
<i>Read that sentence again with this book’s own first chapter beside it.</i> Ghassanid Christians.
Al-Karak. A forced marriage refused. A flight north. A new village on a hill.
<b>It is the Ramallah story, with the names changed.</b></p>
<p><b>And this is where the book has to be honest, because the parallel cuts.</b> The Rafīdiyā
tradition dates the flight to the seventeenth century — and the Ottoman defter of <b>1596</b>
already records <b>eighty-five Christian households at Rafīdiyā</b>, beside nine Muslim households
and six bachelors. <i>The Christian community is large and long-established before the date the
story gives for its founding.</i> The tradition cannot be a literal foundation account{c('Hütteroth and Abdulfattah (1977) for the 1596 <i>mufaṣṣal</i> figures at Rafīdiyā: 85 Christian households, 9 Muslim households, 6 bachelors. The arithmetic is the same objection this book has already made to its own “about 1550,” and to the 143 Christian households once claimed at Karak in 1562.')}.</p>
<p><b>So what is it?</b> This book’s answer, printed as an argument and not as a finding:
<b>it is a form.</b> A way that the Christian communities of these hills — Ramallah, Rafīdiyā, and
others — have told their own origins for a very long time. Ghassān for descent, Karak for the road,
a refused marriage for the reason, a hill for the destination. <i>That two towns forty kilometres
apart, who did not compare notes, tell the same shape of story is not evidence that the events
happened twice. It is evidence about how Palestinian Christians remember themselves.</i>
<b>And a form is not a lie.</b> It is what a people uses to carry a truth it cannot document —
in this case: <i>we are old here, we are Christian here, and we came to this hill because staying
where we were had become impossible.</i> Every part of that is true of this family whether or not
Rāshid ever stood at a ford.</p>
<p><b>Now the ground under the neighbours, which is not a tradition at all.</b> Al-Bīra has been
lived in continuously for so long that the shape of the medieval town is still legible in the modern
street plan. The Crusader archaeologist Denys Pringle, who excavated it, writes that the general
layout of medieval al-Bīra <i>remains fairly clear in the twentieth-century street pattern, despite
over eight centuries of continuous habitation</i>{c('Denys Pringle, “Magna Mahumeria (al-Bīra): the Archaeology of a Frankish New Town in Palestine,” in <i>Fortification and Settlement in Crusader Palestine</i> (Routledge, 2023), ch. VI, 147–168, DOI 10.4324/9781003418405-6; and <i>The Churches of the Crusader Kingdom of Jerusalem</i> I (Cambridge, 1993), 161–165. Al-Bīra sits at 860 m on the Nablus road, 16 km north of Jerusalem. Medieval Islamic reoccupation is attested by the thirteenth century, evidenced by a hoard of 116 copper coins, Ayyubid and Mamluk, found in a cistern in 1951.')}.
The Frankish new town there was <b>Magna Mahumeria</b>, whose charter of 1156 rolls ninety-two
burgesses by name; its parish church of St Mary is in the record by <b>1128</b> and was described by
the German pilgrim Theodoric in <b>1172</b>{c('Palestinian Ministry of Tourism and Antiquities, site record for the church at al-Bīra: documented September 1128 under the jurisdiction of the Holy Sepulchre; described by Theodoric, 1172; a Romanesque basilica of roughly 22 × 35 m with three semi-circular apses; known as St Mary’s Parish Church, the Church of the Holy Family and the Church of the Visitation; probably converted to a mosque after Ṣalāḥ al-Dīn retook the town in 1195, and largely demolished by Turkish forces in the First World War for bridge stone.')}.
<b>And the fabric is counted.</b> Riwaq’s registry of historic buildings — a Palestinian survey
that walked 422 localities between 1994 and 2007 and recorded 50,320 buildings — lists <b>168
historic buildings at al-Bīra</b> against <b>381 at Ramallah</b>, the largest concentration in the
governorate; and the al-Bīra list is dominated by the houses of <b>al-Qarʿān, al-Ṭawīl, al-Ḥamāyil
and al-Qarāqira</b> — the same families Ḥammūdeh names, arrived at independently, building by
building{c('Riwaq — Centre for Architectural Conservation, Ramallah, <i>Registry of Historic Buildings in Palestine</i>, browsable free at buildings.riwaq.org: 50,320 buildings in 422 localities, surveyed 1994–2007, with 400+ digitised maps and 45,000+ photographs. Ramallah and al-Bīra governorate: 71 localities, 7,618 historic buildings, of which Ramallah city holds 381 and al-Bīra 168. Three Riwaq restoration projects at al-Bīra, five at Ramallah. <b>The Ramallah list is given house by house under its owners’ names</b> — <span class="ar">دار حنا وجريس عيسى حنا حديد</span>, <span class="ar">دار بشارة حنا عقال</span>, <span class="ar">دار سالم غنام</span>, <span class="ar">دار مغنم</span>, the Ottoman court, the Ramallah hotel and dozens more. It is the nearest thing that exists to a house-by-house gazetteer of this town, it is Palestinian, and it is free.')}.</p>
<p>Underneath all of it, inside the modern streets, is <b>Khirbet Raddana</b> — the Iron I farming
village this book has already mapped, dug in salvage seasons between 1969 and 1974 and since built
over by al-Bīra’s own growth. <i>Iron Age village, Frankish town, Ayyubid coins in a cistern,
Ottoman quarter, modern city, one continuous street plan.</i></p>
<p><b>The two towns are documented together twenty-one years before ours was founded.</b> A Jerusalem
court record of <b>1541</b> has <b>Ḥasan bin ʿAlī of the village of Ramallah</b> transacting with men
<b>from the village of al-Bīra</b>{c('Jerusalem sharīʿa court records, 1541, in Sāmiḥ Ḥammūdeh, “New Light on Ramallah’s Origins in the Ottoman Period,” <i>Jerusalem Quarterly</i> 59 (2014). Note the date: 1541 is twenty-one years before the Christian founding of 1562, and the Ramallah party is one of the Muslim households already on the hill.')} — which is to say that before there was a Christian
Ramallah at all, the Muslim households on this hill were already doing business with the town next
door. <b>The relationship is older than the founding.</b></p>
<div class="fix"><div class="fixhead">And the thing the numbers say, which is the opposite of ours</div>
<div style="font-size:.95rem;line-height:1.65;color:#46423B">
<p style="max-width:none">Al-Bīra’s Christians were always a small minority in a large Muslim town —
<b>none at all in the register of 1596</b> (45 households, all Muslim); <b>72 of 1,479 in 1922</b>;
<b>248 of 2,292 in 1931</b>; <b>280 of 2,920 in 1945</b>. Never more than about a ninth of the
town{c('1596: Hütteroth and Abdulfattah (1977), p. 116 — 45 households, all Muslim, 4,570 akçe. 1922: Barron, <i>Report and General Abstracts of the Census of 1922</i>, p. 16 — 1,479 total, 1,407 Muslim, 72 Christian (61 Orthodox). 1931: Mills, <i>Census of Palestine 1931</i>, p. 48 — 2,292 total, 248 Christian. 1945: <i>Village Statistics, April 1945</i>, p. 26 — 2,920 total, 280 Christian. Of 23,012 dunums in 1945, 22,406 were Arab-owned and none Jewish-owned.')}.
<b>That is the exact inverse of Ramallah</b>, which was 2,972 Christian out of 3,104 in 1922.
<i>Two towns whose streets run into one another, with opposite religious arithmetic, and no record
of that ever having been the point.</i></p>
<p style="max-width:none"><b>What this book will not do is annex them.</b> The Rafeedie are an
al-Bīra family, not a Ramallah clan; in America they have their own society, organised around
descent from their own town, as the Federation is organised around descent from ours. <i>They are
not part of this genealogy.</i> <b>They are part of this history</b> — which is a different claim,
and the truer one.</p></div></div>
<p><i>One documented Rafeedie, so the family is a person and not an abstraction.</i> <b>Wissām
Rafeedie</b>, journalist, of al-Bīra: arrested at his home on 11 August 1994 and held under
administrative detention orders renewed for twenty-one months, until the United Nations Working
Group on Arbitrary Detention declared the detention <b>arbitrary</b> in 1996{c('UN Working Group on Arbitrary Detention, <i>Rafeedie v. Israel</i>, Opinion No. 17/1996, 23 May 1996 — residence given as “El Bireh, West Bank”; arrested 11 August 1994; the Working Group found the detention arbitrary, citing the absence of effective appeal and its duration.')}. He wrote a novel in
prison on Red Cross booklets, had it confiscated, and got a second copy out in miniature handwriting
concealed in pill capsules; it was printed in <b>Ramallah</b>, in 1998{c('Wissām Rafeedie, <span class="ar">الثالوث الأصولي</span> (<i>The Trinity of Fundamentals</i>), written from 1993 in al-Naqab (Ktzi‘ot) prison, printed in Ramallah in 1998 after his release; English translation 2024.')}.
<b>An al-Bīra man’s book, printed in our town.</b> <i>That is what the relationship between these
two places actually looks like, and it did not need a shared genealogy to happen.</i></p>
<div class="fix"><div class="fixhead">Two things this book was offered and would not print</div>
<div class="fixgrid">
<div><span class="fl">Not printed</span><b>That Judge Edward Rafeedie of the U.S. District Court was of the al-Bīra family.</b> He was born in Orange, New Jersey, on 6 January 1929 to Palestinian immigrants, and <i>no source names their town</i>. The surname is a nisba from Rafīdiyā and is carried by families in several places. A famous name is not evidence.</div>
<div><span class="fl">Not printed</span><b>That the Rafeedie are “Nestorian.”</b> One Arabic wiki says so; al-Bīra’s Christians in the Mandate censuses are overwhelmingly Greek Orthodox, and there is no Church of the East community in this district. The claim has no source that will bear weight.</div>
<div><span class="fl">How it is justified</span>The same rule this book applies to its own family: <b>a claim is printed at the strength of the document behind it, and a claim with no document is named as one.</b> The Rafeedie deserve the same care as the Ḥaddādīn — which means not decorating them either.</div>
</div></div>"""),

ent('1901', 'oral', True, 'The first four sail — on a road Rome paved',
 'Ramallah men begin to emigrate to the United States{}; the Turkish carriage road from Jerusalem to Nablus is completed the same year, and the Friends Boys School is founded (it opens in 1918). <i>The ridge road becomes infrastructure, and the first men leave on it.</i>'.format(c('Shāhīn (1982): emigration to the United States begins in 1901 — Esa Izhak ʿEadeh, Hanna ʿAazar Hishmeh, Esa Salah Jaghab and Esa Khashan the first four (1900 or 1901), seven more named in 1903; before 1914 the only entry requirement was eyes free of trachoma.')),
 f"""
<p>The leaving has its own genealogy, and Shāhīn writes it name by name: the first to leave at all,
<b>Ibrahim of the Hassaan clan</b>, in the seventeenth century, for ʿIsifyā near Haifa — four hundred
descendants there today; the first abroad, <b>Hanna Ibrahim Saʿah, 1858</b>, to Constantinople; the
first West, to England, 1895; and in 1898, from Brazil, <b>the first cheque the town had ever
seen</b> — 100 French gold francs, “and it created quite a sensation.” The early emigrants were men
over thirty who meant to return, and almost all did. <b>Their children did not</b> — and that is the
demographic history of this town in one sentence.</p>
{fig(ATLAS.fig_diaspora(),'Where Ramallah went, 1901 onward',
 'The cities the town’s people went to, weighted by the family’s own record — Detroit above all, then Jacksonville, New York, San Francisco. Nobody has ever properly enumerated this diaspora, which is itself a finding.',
 'Shāhīn (1982) for the start date and the named firsts; the Federation’s conventions for the cities.')}"""),

ent('1901–1904', 'documents', False, 'AN OUTSIDER WRITES THE TOWN DOWN — Elihu Grant lives here and takes notes',
 'Everything this book knows about how Ramallah actually lived comes from <b>ʿAzīz Shāhīn, who lived it</b>. <b>Elihu Grant</b> — superintendent of the American Friends Schools at Ramallah and Jerusalem from 1901 to 1904 — happened to be counting the same houses at the time, which lets us <i>date</i> what Shāhīn remembered. <b>Shāhīn is the source; Grant is the clock.</b> Grant and in 1907 published <i>The Peasantry of Palestine</i> — two hundred and fifty-five pages on village life, with a chapter given over to <b>Ramallah and al-Bīra by name</b>{}.'.format(c('Elihu Grant, <i>The Peasantry of Palestine: The Life, Manners and Customs of the Village</i> (Boston: Pilgrim Press, 1907), 255 pp. with 39 leaves of plates — the c. 340-page figure belongs to the enlarged edition of 1921, <i>The People of Palestine</i>; the title page describes him as “Resident (1901–1904).” Chapter IX, from p. 187, is “Village life in the concrete. Description of actual villages, Ram Allah and el-Bireh”; chapter X covers eṭ-Ṭīreh, ʿAyn ʿArīk, Baytīn, Dayr Dīwān, eṭ-Ṭaybeh, Jifnā, ʿAyn Sinya, Bīr Zayt, ʿAbūd and Mukhmās — nearly every village on this book’s district map. ' + D('peasantryofpales00gran.pdf') + '.')),
 f"""
<p><i>He counts things.</i> Down one street south of the market he records <b>twenty-two houses, one
store and one silversmith’s shop</b>, and measures <b>seven hundred and eighty feet</b> to the
threshing floor. He gives the price of meat at Ramallah — <b>eight to twelve cents a pound</b>,
according to season. He dates the carriage road from Jerusalem precisely: <b>opened in May 1901</b>,
fifteen kilometres to al-Bīra{c('Grant (1907), 191–96 for the street survey, the market and the threshing floor; 189 for the road: “It was in May, 1901, that the road mentioned was opened up for use from Jerusalem to el-Bireh, a distance of fifteen kilometers.” <i>Shāhīn dates the same road to 1901; Grant, who used it, gives the month.</i>')}.</p>
<p><b>And he gives the town a stratigraphy in buildings.</b> Grant sets out the sequence he can see
standing side by side in 1903: the old <i>skīfeh</i> huts of stone bedded in earth with dirt roofs on
boughs; then dressed stone and mortar with rolled earth roofs; then the heavy arched stone dome
roofs which by then were the majority in Ramallah and rare in al-Bīra; then the new multi-room houses
with modern windows, paved floors and cisterns that the wealthier villagers were putting up as he
watched. <i>“The development of several centuries in highland peasant homes may thus be traced.”</i>
<b>That is the town’s whole economic history, read off its own walls by a man standing in the
street.</b></p>
<p><b>One observation matters for everything this book has said about land.</b> Grant records that
Ramallah’s people had bought fields in <i>a dozen or more villages</i> — as far out as ʿAyn Qīniya,
Mukhmās and Dayr Dīwān — and that <b>for those outside lands they held no government deeds</b>
(<span class="ar">كوشان</span>, pl. <span class="ar">كواشين</span>), the title resting in the
register with the original village{c('Grant (1907), 191–92: “The needs of Ram Allah are so much in excess of the lands which are legally recorded as belonging to it that its people have bought tracts here and there all about the country… For such outside lands the Rām Allah people have no government deeds (<i>kushān</i>, plural <i>kuwashīn</i>), the title resting, so far as the government records are concerned, with the original village.”')}. <i>A town whose wealth had outgrown its own land, holding much
of it without paper.</i> <b>That is the condition of a place about to start sending its sons to
America — and he wrote it down the same year the first four sailed.</b></p>
<p><i>He also, without meaning to, confirms the argument of this whole book.</i> Grant lists the
Christian villages of the central highlands — <b>Ramallah, Bayt Jālā, eṭ-Ṭaybeh and Jifnā</b>, with
Christians outnumbering Muslims at Bīr Zayt, ʿAyn ʿArīk and ʿAbūd — the same band along the ridge
that the Ottoman register of 1596 describes three hundred years earlier, and that the Byzantine
churches describe a thousand years before that. <b>Different observer, different language, different
century, same map.</b></p>"""),

ent('1902 · 1908', 'documents', True, 'The state arrives; the clans become a constitution',
 'In 1902 Ramallah is made a district seat over thirty villages — <b>“Till 1902 there had been no government rule in the villages and small towns of Palestine”</b>{} — and in 1908 it is incorporated as a city under Elias ʿAudi, its first mayor, with <b>one council representative from each clan</b>. The ḥamūla structure of 1562 becomes, literally, the constitution.'.format(c('Shāhīn (1982): the district of 1902 under mudīr Ahmad Murad, and the incorporation of 1908 — Elias ʿAudi mayor, Assʿad Ibrahim Kassees secretary-treasurer; compare Zeʾevi, <i>An Ottoman Century</i> (1996).')),
 fig(F3.fig_town_plan(),'The town, as Shāhīn drew it',
  'Central Ramallah after the sketch map in his own book. The dashed ring is the original village — the eight clans’ quarters and their guest houses, all of it walking distance. Everything numbered outside it was built by the century this book has just described: the church of 1850, the Catholic mission of 1857, the Friends schools, the Meetinghouse of 1910, and the hospital the diaspora paid for in 1963. Note the two roads south: the old track from El Sharafa, where the town said goodbye to its emigrants, and the carriage road of 1901 through El Bireh that replaced it.',
  'After Shāhīn (1982), p. 69, simplified; institution dates from his own chapters.')),

ent('1904 · 1908', 'documents', False, 'THE PATRIARCHATE COUNTS ITS FLOCK — and the flock starts to argue back',
 '<b>In 1904 the Orthodox Patriarchate of Jerusalem estimated its own people, parish by parish, for its schools.</b> Of 49,596 in the whole Patriarchate, <b>Ramallah had 4,500</b> — more than Bethlehem’s 3,600 and Bayt Jālā’s 4,340, second only to Jerusalem’s 6,000. <b>Karak had 1,600.</b> <i>The two ends of the family’s road, in one table, written by the church they never left.</i>{}'.format(c('Sir Anton Bertram &amp; H. C. Luke, <i>Report of the Commission appointed by the Government of Palestine to inquire into the affairs of the Orthodox Patriarchate of Jerusalem</i> (Oxford, 1921), §9, p. 9 n. 1: “In an official estimate prepared by the Patriarchate for the purposes of its schools in 1904 … Jerusalem 6,000, Bethlehem 3,600, Beit Jala 4,340, Ramallah 4,500 … Es Salt 3,000, Kerak 1,600.” ' + D('1921_Bertram_Luke_Report_Orthodox_Patriarchate_Jerusalem.pdf') + '.')),
 f"""
<p><b>The same report names the quarrel that runs underneath the rest of this book’s church history.</b>
The parishes, the parish priests and the people were Arabic-speaking; the Patriarch and the
Brotherhood of the Holy Sepulchre that governed them were Greek. <b>When the Ottoman constitution was
restored in 1908, the Arab Orthodox laity began a long and bitter fight for a share in running their
own church</b>{c('Bertram &amp; Luke (1921), §§11–14: the laity and parochial clergy “almost exclusively Arabic-speaking”; “the bitter and prolonged struggle with the local Arabic-speaking laity which arose on the declaration of the Turkish Constitution in 1908.” The commissioners were British officials of the Mandate government; their report is used here for its figures and its record of the dispute, not for its judgements.')}.
<i>Ramallah, with the largest Orthodox parish outside Jerusalem, was in that fight from the start.</i></p>"""),

ent('12 June 1905', 'oral', False, 'The last big fight',
 'A wedding procession, a quarrel over clan songs in the narrow streets, and a <b>three-hour stone-throwing battle</b> between Hadadeh and Hamayel from the rooftops — the women refilling the trays of stones — and nobody killed{}. The whole town is jailed together in Jerusalem and released together at the church’s pleading. <i>The 1905 census counts 3,214 people in the eight clans; every one of them seems to have been on a roof.</i>'.format(c('Shāhīn (1982), “Ramallah’s Last Big Fight,” 12 June 1905; the 1905 clan census total of 3,214 from the population chapter.'))),

ent('1914–1918', 'oral', True, 'The war, the locusts, the typhus',
 'About thirty Ramallah men die in the Turkish army; the locusts of 1915 spare no crop; and in <b>1916 typhus kills a large part of the town — Shāhīn puts it near a third</b>{}. <i>No independent record survives, and the figure should be read as family memory rather than a measurement: the counts on either side, 3,214 in 1905 and 3,104 in 1922, do not require a loss on that scale, and heavy emigration accounts for much of the gap.</i> The British Army arrives in December 1917 — <i>the exact day is not recorded in any published source; 27 December, sometimes given, is the date of the Ottoman counter-attack on Jerusalem.</i>'.format(c('Shāhīn (1982): the war dead, the locust plague of 1915, and the typhus of 1916 — “about 30% of Ramallah’s population perished”; among the dead, Dr Maʿlouf, and the child in the family photograph on p. 30.')),
 f"""
{fig(F3.fig_war_strip(),'The dark half-decade, 1914–1918',
 'Four blows in five years. The middle one may be the largest demographic event in the town’s recorded history — and no government count brackets it closely: the Ottoman count of 1905 and the British census of 1922 sit sixteen years apart on either side. It survives because Shāhīn wrote it down, and because his own doctor died in it.',
 'Shāhīn (1982), the war chapters; Schick (1896) and Barron (1922) for the counts that bracket the epidemic without recording it.')}
{FIX('A population curve drawn smoothly through 1896 (2,061) and 1922 (3,104).',
 'The curve must show <b>1916</b>: about 30 per cent mortality, drawn as a labelled inference.',
 'Shāhīn records the epidemic and its scale; no census sits on either side of it, so the chart shows the event as a dashed line explicitly marked “inferred shape, not data.” No figure in this book invents a data point.')}"""),

ent('1922–1944', 'documents', False, 'The counting years',
 'The Mandate counts everything — and for once the town can be tabulated.',
 f"""
{NUMTABLE('EVERY COUNT OF RAMALLAH, 1838–1953 — as Shāhīn assembles them',
 ['Year', 'Count', 'Counted by'],
 [['1838', '800–900', 'Robinson and Smith, travellers'],
  ['1839', '200 Greek Orthodox families', 'Anthemos, secretary of the Patriarch'],
  ['1870', '249 houses; 635 males', 'A. Socin’s Ottoman village list, <i>ZDPV</i> 2 (1879), p. 158, marked uncertain in the original. A household multiplier puts the total near 2,000, but that is inference, not Socin. Guérin the same decade: ~1,100'],
  ['1905', '3,214', 'census, by the eight clans'],
  ['1922', '3,104 — 125 Muslims, 7 Jews', 'British census, 23 October'],
  ['1931', '4,286 in 1,014 homes', 'British census'],
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
 'Mills, 1931: 1,941 men against 2,345 women. A deficit of four hundred men in a town of four thousand is the men who left after 1901, counted by their absence.',
 'E. Mills, Census of Palestine 1931, the Ramallah tables.')}"""),

ent('1938', 'documents', False, 'THE REVOLT REACHES THE TOWN — written down by a teacher at the Friends school',
 '<b>In the autumn of 1938 the great Palestinian revolt against British rule came to Ramallah.</b> The post office and telephones were removed, and six hundred British soldiers were sent to occupy two old hotels. <b>On Saturday 1 October fighters from across the country gathered in the town and British forces attacked them</b> with machine-gun trucks and, after some hours, aircraft, which bombed the thickest of the fighting. <i>About eighty Palestinians were killed.</i> Among them were <b>two women and three men bombed as they ran home from their vineyards</b>{}.'.format(c('Nancy Parker McDowell, <i>Notes from Ramallah, 1939</i> (Richmond, Ind.: Friends United Press, 2002), pp. 9–17: the letters and journal of a young American teacher at the Friends school, September–December 1938 — the six hundred soldiers expected and the hotels taken (p. 9); the battle of 1 October and its dead, from her journal of 8 October (pp. 13–14) and a letter (pp. 16–17); “Ramallah has become a rebel town” (p. 16). ' + D('1939_McDowell_Notes_from_Ramallah.pdf') + '.')),
 f"""
<p><b>It is the first time in this book that the town itself is a battlefield, and the witness is
an outsider</b> — a Quaker teacher watching from the school roof and writing home to her family. <i>The town’s own account of 1938 is still to be collected</i>: the names of the
dead, the houses burned, and what the revolt cost the families that stayed.</p>"""),

ent('1948', 'documents', False, 'The catastrophe — and the town transformed',
 'On <b>11 July 1948</b> Israeli forces took Lydda; Ramle surrendered the next day. At half past one on <b>12 July Yitzhak Rabin signed the order to expel the inhabitants</b>, and on the morning of the 13th the people of Lydda were marched east on foot in the July heat — somewhere between fifty and seventy thousand people driven out of the two towns, and an unknown number dead on the road. The Arab Legion picked up the survivors and brought them to Ramallah. <b>Ramallah was not destroyed. Ramallah opened its doors and was tripled</b> — every madāfa, every schoolroom, every qaṣr in the fig groves. By a local count of 1953: some 13,500 souls, of whom about nine thousand are refugees and four and a half thousand are Ramallah natives — the figure that, with 2,580 in America, gives Shāhīn’s total of 7,080 Ramallah people in the world{} — <i>Jordan held no census that year; its censuses are 1952 and 1961</i>. And its own money went at the same time: the deposits in <b>Bank al-Umma</b> were frozen, not lost — part of the wholesale freezing of Palestinian bank accounts that year — the swine-raising venture collapsed with over <b>$400,000</b> in it, and some 200 Mandate salaries simply stopped{}. <i>“The future looked grim and the morale of the people was at its lowest ebb”</i> — Shāhīn saw it himself in 1951–52.'.format(
  c('Shāhīn (1982), “The Great Influx of 1948,” with the 1953 census figures.'),
  c('Shāhīn (1982): the swine venture, the Bank El Ummeh closure, and the 200 lost government jobs — “all of these misfortunes occurred within three or four years.”'))),

ent('1949 → 1957', 'documents', False,
    'AND WHERE THEY LIVED — four camps, and the one inside the town',
 f'''The last entry ends with the refugees arriving. <b>This book has never said where they went, and that is a hole in it.</b> They went into four camps, three of them within six kilometres of the church, and one of them <b>inside Ramallah itself</b>{c('The camp figures throughout this entry are from the Applied Research Institute–Jerusalem (ARIJ) locality profiles for Qaddura, al-Amʿari, al-Jalazun, Qalandiya and Deir ʿAmmar (2012), which carry PCBS 2007 population counts; and from UNRWA’s camp pages for registered-refugee totals. '+D('2012_ARIJ_Qaddura_Camp_Profile.pdf')+' · '+D('2012_ARIJ_al-Amari_Camp_Profile.pdf')+' · '+D('2012_ARIJ_al-Jalazun_Camp_Profile.pdf')+' · '+D('2012_ARIJ_Qalandiya_Camp_Profile.pdf')+'.')}.''',
 f"""
{NUMTABLE('The camps of this district', ['camp','where','set up','on whose land','who is in it','2017'],
 [['<b>Qaddūra</b>','inside Ramallah city, 0.5 km east of the centre','1948','<b>private land</b> — so UNRWA never recognised it as a camp','Dayr Ṭarīf, al-Lidd, Lifta, al-Ramla, Jaffa, Qālūniya, ʿImwās','924'],
  ['<b>al-Amʿarī</b>','al-Bīra, 1.4 km east of Ramallah centre','1949','leased by UNRWA from the Jordanian government','al-Ramla, al-Lidd, Jaffa, Haifa','4,725'],
  ['<b>al-Jalazūn</b>','5.3 km north of Ramallah','1949, named for a spring','reported three ways; no lease document is public','thirty-six villages of Lydda, Ramle, Haifa and west of Hebron; chiefly Bayt Nabāla and al-Lidd','8,201'],
  ['<b>Qalandiyā</b>','the southern entrance to Ramallah; Jerusalem governorate','1949','leased by UNRWA from the Jordanian government','the Jerusalem-corridor villages — ʿAllār, Lifta, ʿArtūf, Khirbat al-Lawz, ʿIshwaʿ, Ṣarʿa','8,336'],
  ['<b>Dayr ʿAmmār</b>','12 km north-west','1948–49','land of non-refugee villagers of Dayr ʿAmmār and Jammāla','Bayt Nabāla, Dayr Ṭarīf, Ṭīrat Dandan, al-Sāqiya','—']],
 'Populations are PCBS 2017 for the camp localities; UNRWA’s registered-refugee rolls are far larger, because they count the descendants wherever they now live — al-Amʿarī, 97 dunums, carries 15,315 registered refugees.')}
<p><b>Read the origin columns and the map of 1948 assembles itself.</b> Qalandiyā holds the villages
of the Jerusalem corridor; al-Amʿarī and al-Jalazūn hold Lydda, Ramle and Jaffa. <i>The people who
walked east out of Lydda on 13 July stopped where the road stopped, and the camps are where the road
stopped.</i>{c('Lisa Taraki, “Enclave Micropolis: The Paradoxical Case of Ramallah/al-Bireh,” <i>Journal of Palestine Studies</i> 37:4 (2008), p. 10: “The vast majority of refugees who made their way to Ramallah/al-Bireh in the hot days of July 1948 were peasants from villages near al-Lidd (Lydda), Ramla, and Jaffa who settled — often after several temporary relocations — in al-Bireh, Qaddura refugee camp, and later in Amʿari and Jalazon camps.” '+D('2008_Taraki_Enclave_Micropolis_Ramallah_al-Bireh_JPS37.pdf')+'.')}</p>
<p><b>One of those rows will not add up, and the failure is instructive.</b> UNRWA's own page for
al-Jalazūn says "around 9,450 refugees live in Jalazone camp" and, two lines later, gives the camp
as 0.253 km² at "an estimated population density of 51,383 per sq km." <i>51,383 × 0.253 = 13,000.</i>
<b>The density was computed from a population of thirteen thousand and printed beside a headline of
nine thousand four hundred.</b> The discrepancy is not between sources; it is inside one page, and
it is the difference between the people registered and the people counted{c('UNRWA, “Jalazone Camp,” read 7 September 2026. PCBS counts residents — 7,344 in 2007, 8,201 in 2017, 8,858 projected for 2021; UNRWA counts registered refugees and their descendants wherever they live. Khaldun Bshara gives UNRWA c. 13,000 for 2023 against a PCBS estimate of 9,228. <b>On the land: ARIJ says leased by UNRWA from the Jordanian government; Bshara says rented from a private owner in Jifnā; OCHA in 2008 said most plots were state-owned with the remainder belonging to landowners from nearby towns. These are probably one arrangement described at three levels of detail, and Jifnā is exactly a “nearby town” — but no source produces the lease, its date or its parties, and this book will not pretend the question is closed.</b>')}.
<i>A camp is one of the few places on earth where those two numbers are allowed to drift this far
apart without anybody minding.</i></p>
<p><b>The tents came down slowly, and the dates are worth printing.</b> UNRWA began building
permanent structures in 1951 and adopted a shelter programme in 1955; <b>al-Jalazūn had concrete
shelters from 1953, and al-Amʿarī’s last tent was gone by 1957</b>{c('Kjersti G. Berg, “The Evolving Infrastructure of Palestinian Refugee Camps,” <i>Interactive Encyclopedia of the Palestine Question</i> (Institute for Palestine Studies): UNRWA began constructing permanent structures in 1951, adopted a shelter programme in 1955, and “by 1959 most tents were replaced with concrete huts.” Khaldun Bshara, “Al-Jalazone Refugee Camp,” same encyclopedia, for concrete at Jalazone from 1953; UNRWA’s own camp page for al-Amʿari for the 1957 date. UNRWA itself was created by UN General Assembly Resolution 302 (IV) of 8 December 1949 and began operations on 1 May 1950.')}. <i>Nine years from a tent to a
wall.</i> And in <b>1950</b> Jordan annexed the West Bank and gave the refugees citizenship — which
made them, uniquely among Palestinians in exile, <b>refugees and citizens at the same time</b>{c('The Jericho Conference of 1 December 1948 preceded the annexation of April 1950; the Jordanian Nationality Law of 1954 conferred citizenship on “any person who, not being Jewish, possessed Palestinian nationality before 15 May 1948 and resides ordinarily in the Hashemite Kingdom.” Jalal Al Husseini, “Palestinian Refugees in the West Bank,” and “Palestinians in Jordan, 1948–1967,” both in the <i>Interactive Encyclopedia of the Palestine Question</i>, drawing on Myriam Ababsa (ed.), <i>Atlas of Jordan</i> (IFPO, 2013). Some 280,000 refugees were in the West Bank in 1949.')}.</p>
<div class="fix"><div class="fixhead">The demographic question, answered in the right order</div>
<div style="font-size:.95rem;line-height:1.65;color:#46423B">
<p style="max-width:none"><b>Ramallah was 2,972 Christian out of 3,104 in 1922, and is a
Muslim-majority city today. It is worth being exact about how that happened, because the sectarian
version of the story is false.</b></p>
<p style="max-width:none"><b>One.</b> The Christian majority was itself made, not primordial:
the register of 1562 has Christians arriving to join ten Muslim households already on the hill.
<b>Two.</b> The town was already emptying before the Nakba — <i>about 1,500 of some 6,000
Ramallawis had gone to America by 1946</i>. <b>Three.</b> 1948 changed the denominator before it
changed the numerator: the town did not lose Christians in 1948, <b>it gained some nine thousand
mostly Muslim villagers</b> — sixty-seven per cent of a 1953 population of 13,500. <b>Four.</b>
Then the emigration curve steepened: over four thousand Ramallah-born in the United States by 1960,
over ten thousand by 1975 with fewer than two thousand left in the town{c('Taraki (2008), p. 10 and nn. 14, 16, 21, drawing on ʿAzīz/Naṣīb Shāhīn: 1,500 of about 6,000 emigrated by 1946; some 200 Ramallawis employed by Mandate institutions jobless at once in 1948; 4,000+ Ramallah-born in the United States by 1960; over 10,000 by 1975 with fewer than 2,000 remaining; the 1953 Jordanian census at 13,500 with 67 per cent refugees. <b>The “about nine thousand refugees” this book has printed is 67 per cent of 13,500 — the census is the source, and it should have been cited as such from the first edition.</b> Note also that PCBS does not publish religion by locality: the last locality-level figure is 32 per cent Christian in 1997, and the date of the crossover to a Muslim majority is not established.')}.</p>
<p style="max-width:none"><i>So the Christian share of Ramallah fell because Ramallah’s Christians
left for America, and because Ramallah took in the survivors of an expulsion.</i> <b>The second of
those is not a loss. It is the best thing this town ever did</b> — and a family history written from
Detroit and San Francisco should say plainly that the people who filled the houses we left were
driven out of Lydda at gunpoint. <i>Lisa Taraki, who has studied this town harder than anyone, warns
against exactly the frame this book refuses: the Christian villagers of Bīr Zayt and eṭ-Ṭaybeh, she
writes, have more in common with their Muslim neighbours than with the Christian well-off of
Masyūn.</i></p></div></div>"""),

ent('1944–1963', 'documents', True, 'The diaspora builds the town a hospital',
 'The Ramallah Foundation, Inc. of New York is formed in 1944; a three-man delegation — Peter George Shihadeh, Yousef Abdallah Bateh, <b>and ʿAzīz Shāhīn himself</b> — tours every US Ramallah community in 1944–45 and collects over <b>$90,000</b>{}. The Summer Resorts Company (1945, capitalised at £P50,000 — there was no dinar in Palestine until 1950 — mostly diaspora stockholders) brings the water from ʿAin Fara in 1951; and on <b>20 May 1963 the Ramallah New Hospital opens</b> — fifty beds, on 26 dunams, its assets vested in the New York Foundation. <i>The money came back along the road the people left on.</i>'.format(c('Shāhīn (1982), “Societies”: the Foundation of 1944, the delegation and the $90,000; the Hospital Society of c. 1945 and the 26 dunams; the hospital’s completion in 1961–63, third floor 1966–68, out-patient clinic 1977.'))),

ent('1954 · 2023', 'documents', False, 'The town’s first history is written in New York — twice',
 '<b>Joseph Jiryes Cadora</b> — pharmacist, mayor of Ramallah 1943–52 — publishes <span class="ar">تاريخ مدينة رام الله</span> at al-Hudá Press, New York, 1954; Shāhīn takes his census apparatus from it, “pp. 136–37”{}. Seventy years later the author’s niece by marriage, Samira Rafidi Meghdessian, publishes it in English as <i>Remembering Ramallah</i> (2023), annotated, with a foreword by his son. <i>The book this project hunted for years as “Qadūra” was in the family’s hands the whole time — Cadora and Qadūra are the same name.</i>'.format(c('Kaddoura/Cadora, <i>The History of Ramallah</i> (New York: Huda Press, 1954), 159 pp.; <i>Remembering Ramallah: A Preservation of History</i>, trans. Meghdessian (2023), ISBN 979-8-3507-0767-0; Shāhīn (1982) cites the census figures to Kaddoura pp. 136–37.'))),

ent('1958 / 1959', 'oral', True, 'The Federation',
 'The American Federation of Ramallah, Palestine — the body this book is written for.',
 FIX('Founded 1952, federated in Detroit on 7 September 1959 (the family presentation).',
 '<b>Resolved, and the answer is that there are three foundings.</b> <b>1952:</b> six young Ramallah immigrants at Wayne State begin <i>Hāthihi Rām Allāh</i>, the magazine that knits the scattered clubs together. <b>Sunday 7 September 1959, Detroit:</b> delegates from those clubs resolve to constitute a Federation and adopt interim by-laws and a constitution — and the first convention is held that year. <b>August 1963:</b> the IRS recognises the Federation and its education fund.',
 'The convention count settles it arithmetically. The Federation’s own roster of conventions begins at Detroit 1959; the fiftieth fell in Detroit in 2008 and the sixty-third in Dearborn in 2022 — both close on 1959 as the first, and neither closes on 1958. <b>Shāhīn’s “incorporated in Detroit, 1958” is best read as the clubs’ coalition rather than a filing</b>: 1958 appears in the Federation’s own literature too, but always attached to the conventions, never to a document. The IRS Business Master File gives the American Federation of Ramallah Palestine, EIN 38-6096448, 501(c)(4), and the American Ramallah Federation Education Fund, EIN 38-6096449, 501(c)(3), both ruled <b>August 1963</b>, both at Westland, Michigan. <b>What is still not in hand is the Michigan incorporation record itself</b> — a five-minute lookup in the LARA business-entity search for anyone with a browser, and the last thing that would let this entry name a filing date. <i>Note also that the Ramallah Foundation of New York is older and separate: founded 1943, incorporated in New York 1944 by its own account, IRS ruling February 1947.</i>')),

ent('1961–2024', 'documents', False, 'The city, counted to the present',
 'Jordan’s census, 1961: <b>14,759</b>. Israel’s, after the occupation of 1967: <b>12,134</b> — <i>and that is not simply emigration.</i> The count was taken under curfew weeks after the war; it recorded only those standing in the town on the day, and <b>every Ramallah person who happened to be abroad lost the right to come home</b>. The dip is an act of the occupation, recorded as a statistic. Birzeit College begins four-year degrees in 1972 and becomes Birzeit University in 1975; <b>Ramallah did not become a capital by accident.</b> It became one because its people made it ungovernable from outside — Birzeit’s students from 1972 onward, the strike committees of the first intifada, the town the Muqāṭaʿa was built to hold down and could not. That compound ran through every hand in turn — Tegart fort, Jordanian HQ, Israeli headquarters, and after the redeployment of December 1995 the seat of the Palestinian Authority, with Arafat moving in in 1996. In 2002 the Israeli army came back into the city and besieged it, and the town lived under curfew for weeks. <i>The census numbers are what survived that.</i> PCBS: <b>17,851 (1997) · 27,460 (2007) · 38,998 (2017) · 43,880 projected (2024)</b>{}. And the diaspora curve crosses the town’s: 1,500 in the US by 1946, over 4,000 by 1960, over 10,000 by 1975 — <b>“over 85% of Ramallah people are now in the States”</b> — <i>a formula his own figures will not carry, and which can only be read as a claim about descendants of the pre-1948 town rather than about the town’s population</i>{}.'.format(
  c('The census series: Jordan 1961 (14,759); the census conducted by the Israeli Central Bureau of Statistics in the occupied territories in 1967 (12,134); PCBS 1997, 2007 and 2017; and the PCBS projection series, <i>Projected Mid-Year Population for Ramallah &amp; al-Bireh Governorate by Locality 2017–2021</i>, locality code 301810, which gives Ramallah <b>42,122 for 2021</b> — the 2022–26 table is attested by title but PCBS has taken it offline, so this book prints 2021 and no later projection. <b>On religion: the 1967 census is the only locality-level count of Christians and Muslims in Ramallah between 1945 and 1997.</b> It recorded <b>6,966 Christians of 12,134 — 57 per cent</b> — and 5,203 people, 43 per cent of the town, originating from what had become Israel. <i>It is an Israeli state source, produced by the occupying power weeks into the occupation, and this book says so on the page rather than passing the number through a tertiary work.</i> Its tables are now published in full and independently by the Levy Economics Institute of Bard College, so a reader can check them. By the first Palestinian census in 1997 Christians were <b>32 per cent</b> (PCBS, <i>Final Results: Ramallah City</i>, City Reports Series 005, 2000). <b>Between 1967 and 1997 there was no census of any kind, and no municipal, church or scholarly source publishes a religious breakdown for the town in that interval. The crossing from a Christian to a Muslim majority cannot at present be dated more closely than to those thirty years.</b>'),
  c('Shāhīn (1982), the emigration chapter: 1,500 by 1946, 4,000+ by 1960, 10,000+ by 1975 with fewer than 2,000 remaining, and the 85% figure.')),
 f"""
{fig(F3.fig_two_pop(),'Two populations, one town',
 'Ramallah natives at home against Ramallah natives in the United States, on Shāhīn’s own figures. <b>By 1975 he counts more than ten thousand Ramallah people in America — a diaspora that had grown to rival, and by some readings to overtake, the native population still at home.</b> <i>His own “eighty-five per cent” is not supported by the numbers he prints, and this book does not repeat it as a measurement.</i> What is not in doubt is the direction of the money: the hospital, the water supply and the schools at home were paid for from the far side of the ocean.',
 'Shāhīn (1982): the home censuses of 1905–1953 and his diaspora counts — 1,500 by 1946, 2,580 in 1953, 4,000+ by 1960, 10,000+ by 1975.')}
{fig(POP_CHART, 'Every number anyone has ever recorded, 1596–2024',
 'The recorded population on a logarithmic scale, now carrying every count Shāhīn assembled — 1839, 1870, 1905, 1944, 1953 — with the 1916 typhus drawn as a labelled inference and the 1967 dip labelled as what it is: emigration.',
 'The 1596 defter; Robinson and Smith; Anthemos; the censuses of 1870–2017; PCBS projections; the epidemic from Shāhīn (1982).')}"""),

ent('1982', 'documents', False, 'Shāhīn closes the record',
 'ʿAzīz Shāhīn — born 1894, typhoid survivor of 1906, Friends Boys School boarder of 1907–10, fund-raiser of 1944–45 — publishes <span class="ar">كشف النقاب</span>: 894 pages, the book everything here is measured against{}. His history ends: <i>“The foregoing history of Ramallah brings us down to the end of 1978. Every effort has been made to make it as complete and as accurate as possible.”</i> This book has tested that claim line by line, and it holds.'.format(c('Shāhīn (1982); the autobiographical details from his own chapters. The full test of his chronology against the external record: 36 checkable claims — 13 confirmed, 15 new, 3 refined, 3 corrected, 1 in conflict, 1 untestable.'))),

sect('Three things said plainly', 'The Karak evidence, two false leads, and the people this town produced')
ent('1812 → 1934', 'documents', False, 'When the Ḥaddādīn name actually enters the record at Karak',
 'The family’s road runs through Karak, and the Karak end of it can now be dated with some precision — which turns out to be <b>much later than the tradition implies</b>, and worth saying plainly.',
 f"""
<p><b>1812.</b> The Swiss traveller Burckhardt counted about <b>150 Christian families at
Karak</b> — and did not name the Ḥaddādīn among them{c('J. L. Burckhardt, <i>Travels in Syria and the Holy Land</i> (London, 1822), on the Christians of Karak. He names no clans.')}. He also recorded something this book has
until now passed over: that Karak’s Christians were, in the main, <b><i>descendants</i> of refugees
from Jerusalem, Bethlehem and Bayt Jālā</b>{c('J. L. Burckhardt, <i>Travels in Syria and the Holy Land</i> (London: John Murray, 1822), 381: “Kerek is inhabited by about four hundred Turkish, and one hundred and fifty Christian families… The Christians are, for the greater part, descendants of refugees from Jerusalem, Bethlehem, and Beit Djade.” <b>Earlier editions of this book read this as migration Burckhardt observed. It is not — it is what the Christians of Karak told him about their ancestry.</b>')}. <i>That is an origin tradition of unknown depth, not a
migration he watched happen — but it does mean the corridor is remembered as running both ways.</i> That does not break the family’s tradition of coming out of Karak,
but it does mean the corridor by itself proves connection, never direction.</p>
{FIX('A one-way migration corridor: Karak → Palestine.',
 'A <b>corridor remembered in both directions</b>. Burckhardt’s Karak Christians said they were descended from refugees out of Jerusalem, Bethlehem and Bayt Jālā.',
 'The map and the narrative may show the family’s claimed route, but must not use the corridor’s existence as evidence of which way anyone travelled. Direction has to come from a document about <i>this</i> family, not from the road.')}
<p><b>c. 1879 — the first named Ḥaddādīn at Karak.</b> A house in the town is attributed to
<b>Jreis Sulayman Haddadeen</b>{c('Reported attribution of a Karak house to Jreis Sulayman Haddadeen, c. 1879. A deed, building inscription, tax entry, photograph or conservation inventory is still needed to confirm it.')}. <b>1886 — the Latin Patriarchate’s own parish history records
Ḥaddādīn families coming from Karak to resettle Maʿīn</b>{c('Latin Patriarchate of Jerusalem, parish histories of Karak and Maʿīn. A family-history article gives 1892 for the same resettlement; the Patriarchate’s 1886 is preferred here, and the conflict is printed rather than resolved.')} — the strongest
institutional evidence tying the clan to the place. <b>The 1920s</b> bring published confirmation: al-Ziriklī lists
<b>fifteen Greek Orthodox Ḥaddādīn houses at Karak</b> — a figure Kaḥḥāla repeats in his tribal
dictionary of <b>1949</b>, which is a compilation of earlier authorities and not an independent
witness{c('Kaḥḥāla, <i>Muʿjam qabāʾil al-ʿArab</i>, s.v. al-Ḥaddādīn: a Christian Greek Orthodox clan of Karak of fifteen houses. <b>Kaḥḥāla assigns them no Ghassanid ancestry.</b> '+D('1949_Kahhala_Mujam_qabail_al-Arab_v4.pdf')+'.')} — and, importantly, <i>assign them no Ghassanid ancestry.</i></p>
<p><b>1934 — and the claim is written down by a sceptic.</b> Frederick Peake, compiling the tribes of
Transjordan, calls the Karak Ḥaddādīn <b>the oldest Christian tribe of Karak</b>, records their claim
of descent from Banū Ghassān — <b>and states that the claim lacks supporting proof</b>{c('F. G. Peake, <i>History and Tribes of Trans-Jordan</i>, vol. II, the Ḥaddādīn entry. '+D('1935_Peake_Tarikh_sharqi_al-Urdun_wa-qabailiha.pdf')+'.')}.</p>
<p><b>1979 — and a Palestinian authority names the family outright.</b> This book has, until now,
run the Ḥaddādīn–Ghassān question entirely through Peake, Kaḥḥāla and the Lebanese family
literature — an English officer, a Damascene compiler and a Maronite genealogist. <b>It should have
gone to the Palestinian record first.</b> <b>Muṣṭafā Murād al-Dabbāgh</b>, in
<span class="ar">القبائل العربية وسلائلها في بلادنا فلسطين</span> — a whole book on the Arab tribes
of Palestine and their descendants — has a chapter on the Ghassanids, and under
<span class="ar">ومن سلائل الغسانيين</span>, “and among the lines of the Ghassanids,” <b>the first
name he lists is <span class="ar">الحدادين</span></b>{c('<span class="ar">مصطفى مراد الدباغ، القبائل العربية وسلائلها في بلادنا فلسطين</span>, chapter <span class="ar">الغساسنة</span>, 151–55, at 153: <span class="ar">ومن سلائل الغسانيين نذكر: ١ ــ الحدادين</span>. He traces them to Biskintā on the flank of Jabal Ṣannīn and thence to ʿAnbah, Sammūʿ, Khanzīra and Dayr Abū Saʿīd in the ʿAjlūn district and al-Salṭ in the Balqāʾ, and adds <span class="ar">ومن الحدادين جماعات نزلت فلسطين وخاصة بيت المقدس</span>. <b>His footnote for the Transjordanian branch is Peake, <i>Tārīkh sharqī al-Urdunn wa-qabāʾiluhā</i>, 246</b> — the same officer who recorded the claim in 1934 and declined to endorse it. ' + D('1979_Dabbagh_al-Qabail_al-Arabiyya_fi_Filastin.pdf') + '.')}.</p>
<p><i>Two things have to be said about that, and the book says both.</i> <b>It is the strongest
Palestinian statement of the family’s claim that exists</b> — an authority writing from inside the
country, in Arabic, naming the Ḥaddādīn among Ghassanid lines and tracing the branch that crossed
into Transjordan through ʿAjlūn and al-Salṭ, and thence <span class="ar">ومن الحدادين جماعات نزلت
فلسطين</span>, “and of the Ḥaddādīn, groups came down into Palestine.” <b>And his own footnote sends
the reader back to Peake.</b> Al-Dabbāgh is not an independent witness to the descent; he is a
Palestinian scholar collecting, in Arabic, the same tradition this book has been testing — <i>which
is worth having, and is not the same thing as proof.</i></p>
<p><b>And in the same chapter he undercuts the other half of the story.</b> Every place al-Dabbāgh
lists for the Ghassanids themselves is east of the Jordan — Tadmur, Ḥawrān, the Yarmūk, Gharandal,
al-Qasṭal, al-Zarqāʾ, <b>Adhruḥ</b>, al-Jarbāʾ, Maʿān{c('Irfan Shahîd, <i>Byzantium and the Arabs in the Sixth Century</i> II.1 (Washington: Dumbarton Oaks, 2002), pp. 61–62: the Arabic sources associate the Ghassanids of southern Transjordan with al-Dajāniyya, Adhruḥ and Ubayr, and Shahîd accepts the association because a Greek papyrus finds a Ghassanid active at Ṣadaqa, close to all three; his list of Ghassanid sites in Palaestina Tertia begins with Adhruḥ (Augustopolis). <b>Adhruḥ is the Udhruḥ that the Ḥaddādīn route begins from.</b> It places the people in the region in the sixth century; it does not place any one family in the people. ' + D('2002_Shahid_Byzantium_and_the_Arabs_6th_Century_v2p1.pdf') + '.')}{c('Al-Dabbāgh, <span class="ar">القبائل العربية</span>, 151–52. His only Palestinian instances are the place-names themselves — Dayr Ghassāna, and a suggestion that Jifnā in the Ramallah district may be named for <span class="ar">آل جفنة</span>, again hedged with <span class="ar">ولا يستبعد</span>, “it is not to be ruled out.” <i>The evidence for the settlement is the place-name; the evidence for the place-name is the settlement.</i> Every Arab authority that specifies where the Ghassanids actually were — al-Qalqashandī, al-Hamdānī, Ibn Faḍl Allāh al-ʿUmarī, Jawād ʿAlī, Kurd ʿAlī, and al-Dabbāgh himself — puts them east and north.')}. <i>The Palestinian record puts our claimed people
on the plateau the tradition names, and nowhere near these hills until we walked here ourselves.</i>
<b>That is exactly what this book has been arguing from the Ottoman side, arrived at independently
from the Arabic.</b></p>
<p><i>So the honest shape of the Karak evidence is this:</i> <b>the clan is securely at Karak from the
late nineteenth century, and published as such by the 1920s. The Ghassanid claim attached to it is
first recorded in 1934, by an outside observer who declined to endorse it.</b> Everything earlier —
the plateau’s Christian continuity from Nitl to Shawbak to the 1596 register — is context for the
claim, and it is good context. <b>It is not the same thing as a chain of fathers, and this book will
not print it as one.</b></p>"""),

ent('a warning', 'none', False, 'Two false leads, marked so nobody follows them twice',
 'Both are the kind of mistake a family history makes when a name looks familiar.',
 f"""
<p><b>Dayr Ghassāna — and what the Arab record actually says about it.</b> Twenty-five kilometres
north-west of Ramallah there is a village whose name looks like a gift, and it is regularly produced
as proof of Ghassanid settlement in these hills. <b>This book has gone to the Palestinian and Arabic
sources first, and they do not support that — but they say something better than a flat no.</b></p>
<p><b>The earliest text is Arabic, and it refuses to choose.</b> In 1122/1710 the traveller
<b>Muṣṭafā al-Bakrī</b> stood at the village — <span class="ar">ووقفنا على تلك الآثار</span>, “and we
stopped at those remains” — reached for al-Jawharī’s <i>Ṣiḥāḥ</i> and al-Suyūṭī’s <i>Lubb
al-albāb</i>, and set out <b>two different Ghassāns</b>: the Azdī water of the Jafnid kings, and
<b><span class="ar">غسّان بن جذام</span>, a clan of the Ṣadif of Ḥimyar</b> — an entirely different
people. <i>He adjudicated neither, and turned at once to the Barāghitha who actually lived there</i>{c('<span class="ar">مصطفى بن كمال الدين البكري الصديقي، «الخمرة الحسية في الرحلة القدسية»</span>, the journey of 1122/1710, serialised in <span class="ar">مجلة الرسالة</span>, no. 801, p. 38. He quotes al-Jawharī’s <i>Ṣiḥāḥ</i> for the Azdī water of the Jafnids and al-Suyūṭī’s <i>Lubb al-albāb</i> for <span class="ar">غسّان بن جذام بطن من الصدف</span>, and settles neither. <b>Ghussān b. Judhām of the Ṣadif is independently attested — al-Dāraquṭnī, <i>al-Muʾtalif wa-l-mukhtalif</i> ii.976 and iv.1800; al-Samʿānī, <i>al-Ansāb</i> iii.316; Ibn Ḥajar, <i>Tabṣīr al-muntabih</i> iii.1045; al-Bakrī, <i>Muʿjam mā istaʿjam</i> i.317 — and is a different people from the Jafnids entirely.</b>')}.
<b>That second reading is real, old and independently attested, and it was quietly dropped by later
writers.</b> Recovering it is the one correction this book would press.</p>
<p><b>The standard Palestinian entry is hedged, and its own citation points east.</b>
<b>Muṣṭafā Murād al-Dabbāgh</b>, in <span class="ar">بلادنا فلسطين</span>, writes
<span class="ar">يبدو أنّ اسمها يعود إلى أنّ طائفة من الغساسنة نزلتها</span> — <i>“it appears that</i>
its name goes back to a group of the Ghassanids having settled it” — and offers no evidence beyond the
name. <b>The authority he cites, al-Qalqashandī, places Ghassān at al-Balqāʾ, the Yarmūk and Ḥimṣ:
not one location west of the Jordan</b>{c('<span class="ar">مصطفى مراد الدباغ، بلادنا فلسطين، ج ٨ ق ٢، «دير غسّانة»، ص ٢٦٦–٢٧٠</span>. His footnote sends the reader to al-Qalqashandī, <span class="ar">نهاية الأرب في معرفة أنساب العرب</span>, no. 1421, i.388, which locates Ghassān <span class="ar">بالبلقاء… وباليرموك الجمّ الغفير، وبحمص منهم جماعة</span> — al-Balqāʾ, the Yarmūk and Ḥimṣ. <b>Al-Dabbāgh himself also prints al-Bakrī’s Ṣadif alternative on the same pages, without deciding between them.</b> Pagination is that of the Bibliotheca Alexandrina scan; the Dār al-Ṭalīʿa and Dār al-Hudá editions differ.')}. Shurrāb repeats al-Dabbāgh’s sentence word for word, hedge
and all, and drops the Ṣadif alternative{c('<span class="ar">محمد محمد حسن شرّاب، معجم بلدان فلسطين</span> (Damascus–Beirut: Dār al-Maʾmūn li-l-Turāth, 1407/1987), 393–94, reproducing al-Dabbāgh’s <span class="ar">يبدو أنّ</span> verbatim. <i>Two of the three standard Palestinian gazetteers are therefore one source counted twice — and the transmission lost the competing etymology on the way.</i> Shukrī ʿArrāf’s <span class="ar">المواقع الجغرافية في فلسطين</span> has no entry: its remit is sites inside the Green Line.')}.</p>
<p><b>And the sharpest witness is the village’s own son.</b> <b>ʿUmar al-Ṣāliḥ al-Barghūthī</b> of
Dayr Ghassāna, co-author with Khalīl Ṭūṭaḥ of <span class="ar">تاريخ فلسطين</span> (Jerusalem, 1923) —
the first Palestinian national history — writes about his own village and its Barghūthī shaykhs and
<b>says nothing whatever about a Ghassanid origin for its name</b>. <i>He is not shy of Ghassān: he
places the Palestinian Ghassanid remnant among the Balāwina of Banī Ṣaʿb and the Baysān valley, and
he asserts Ghassanid descent for Palestine’s Arab Christians as a national claim. He simply does not
attach it to Dayr Ghassāna.</i>{c('<span class="ar">عمر الصالح البرغوثي وخليل طوطح، تاريخ فلسطين</span> (Jerusalem, 1923): p. 239 for the Barāghitha as amīrs of the Qaysiyya in Banī Zayd, Banī Murra and Banī Sālim <span class="ar">ومركزهم دير غسانة</span> — and no etymology; p. 124 for the Palestinian Ghassanid remnant among <span class="ar">البلاونة</span> of Banī Ṣaʿb, al-Sabʿ and Ghawr Baysān; p. 189 for Palestine’s Arab Christians <span class="ar">وأثبتوا أنهم من أبناء غسان وطيّ وتغلب الذين هم من صميم العرب</span>. <b>The leading man of Dayr Ghassāna, writing the first Palestinian national history, does not claim the Ghassanid etymology for his own village.</b>')}</p>
<p><i>So the honest position, reached entirely through Arab and Palestinian sources: the name has
three candidate origins in the Arabic tradition — the Jafnid water, Ghussān b. Judhām of the Ṣadif,
and the ordinary word </i><span class="ar">غسّانة</span><i>, “handsome,” which Ibn Durayd already gave
and the </i>Lisān al-ʿArab<i> preserves. The Jafnid one is the only one of the three with nothing
behind it but the sound of the word</i>{c('<span class="ar">ابن دريد، الاشتقاق</span>, 435: after stating that the children of Jafna were named for a water <span class="ar">ليس بأبٍ ولا أمٍّ</span>, he adds that where others are called Ghassān the derivation is from <span class="ar">الغُسَن</span>, tresses of hair, <span class="ar">أو يكون من قولهم غَيْسان الشباب</span>, “the first freshness of youth.” The same sense in <span class="ar">ابن منظور، لسان العرب</span> xiii.313; <span class="ar">الأزهري، تهذيب اللغة</span> viii.70, 149; <span class="ar">ابن فارس، مقاييس اللغة</span> iv.405; and Yāqūt s.v. <span class="ar">غسان</span>, who brackets the water-story with four morphological derivations. <i>This etymology is sometimes attributed to modern Western scholarship. It is not modern and it is not Western: it is Ibn Durayd’s, and the Western citation of it is a route to the Arabic, not a substitute for it.</i>')}. <b>The village’s name and this family’s nisba are not the
same evidence, and the family’s claim does not need the village.</b></p>
<p><b>“al-Ḥaddāda” in al-Suwaydī is not us.</b> The classical genealogist has an entry under that
name, and beside it a Banū al-Ṣabr among Ghassān — which looks tantalisingly like <i>Sabra</i>. It is
a coincidence: <b>al-Ḥaddāda is an unrelated Lubayd/Sulaym group in North Africa</b>, and a
resemblance between an Arabic clan-name and an ancestor’s name is not evidence of
anything{c('Muḥammad Amīn al-Suwaydī, <i>Sabāʾik al-dhahab fī maʿrifat qabāʾil al-ʿArab</i>, s.vv. In the family library, '+D('1831_Suwaydi_Sabaik_al-Dhahab_qabail_al-Arab.pdf')+'.')}. <i>Surname similarity is
the most common way family genealogies go wrong, and it is worth naming the trap in the book so no
later editor walks into it.</i></p>
<p><b>And a book this project spent two editions failing to find — because it was looking for the
wrong title.</b> The radial genealogy of the Karak clan in the family presentation is captioned
<i>“El-Haddadeen Tribe, Origins and Branches, Warda Books, 2025.”</i> Earlier states of this chapter
reported that no such book exists in any catalogue, and went looking for a different one. <b>The
caption is not a phantom. It is a loose English rendering of a real, catalogued, obtainable
book</b>: <b>Munther Haddadin, <span class="ar">دولة الغساسنة؛ أصيلها ورحيلها</span></b>
(<i>The Ghassanid State: Its Origin and Its Departure</i>), Amman: <span class="ar">دار ورد
الأردنية للنشر والتوزيع</span>, <b>2024</b>, ISBN 978-9923-76-975-1{c('Munther Haddadin, <span class="ar">دولة الغساسنة؛ أصيلها ورحيلها</span> (Amman: <span class="ar">دار ورد الأردنية للنشر والتوزيع</span>, 2024), ISBN 978-9923-76-975-1; announced in the Jordanian press on publication and listed by Neel wa Furat with the publication date 29 July 2024. <b><span class="ar">دار ورد</span> is “Dār Ward” — the presentation’s “Warda Books.”</b> The English caption also renders <span class="ar">أصيلها ورحيلها</span>, “its origin and its departure,” as “Origins and Branches,” and dates the book a year late.')}.
<i>“Warda Books” is <span class="ar">دار ورد</span>. The year is one out. The title was translated
loosely. Everything else in the caption is right, and the chart under it is that book’s plate 84.</i></p>
{FIX('“<i>El-Haddadeen Tribe, Origins and Branches</i> (Warda Books, 2025) appears in no catalogue anywhere, and the tree attributed to it cannot be assessed until its pages are produced.” Earlier editions went on to propose <span class="ar">عشائر الحدادين</span> by <span class="ar">عباس حدادين</span> (2016) as the book actually meant.',
 '<b>The book is Munther Haddadin, <span class="ar">دولة الغساسنة؛ أصيلها ورحيلها</span>, Dār Ward al-Urduniyya, Amman, 2024</b> — and this book had already found it, printed its ISBN, and then wrongly concluded that it “contains no Karak clan genealogy at all.” <i>It contains the wheel.</i>',
 'A publisher’s name anglicised, a title translated loosely and a year off by one were enough to send two editions of this book down a false trail — and the false trail was published, which is why the retraction is printed here at the same size. <b>The 2016 identification is withdrawn.</b> The earlier titles remain worth having: <span class="ar">عشائر الحدادين</span> (2016) and <span class="ar">عشائر الحدادين حتى عام ١٩٩١م</span> by Khalaf Khalīl, Munīr Jiryis and ʿAwwād Jiryis Ḥaddādīn are real books about this clan, and the question of whether Ṣaqr and 1561 appear in the 1991 volume — before Haddadin 2024 — is still the decisive test of the Karak tradition’s age.' + c('<i>ʿAmmūn News</i>, 9 January 2016, on the launch of <span class="ar">عشائر الحدادين</span> by <span class="ar">عباس حدادين</span> at <span class="ar">جمعية آل حدادين (المعمورة)</span>, Sweifieh, at which Munther Haddadin was a speaker; <span class="ar">الرأي</span>, 27 November 2007, citing <span class="ar">عشائر الحدادين حتى عام ١٩٩١م</span>. <b>Still to be checked, through the Ḥaddādīn diwan in Amman or the Jordanian National Library deposit record: whether Ṣaqr and the date 1561 stand in the 1991 book.</b>'))}
<p><b>What remains true after the correction.</b> The wheel is a published genealogy of 2024, not an
Ottoman attestation, and <b>no register names Ṣaqr, Ṣabra or Rāshid</b>. Naming its source correctly
raises it from an uncheckable caption to a citable book. <i>It does not raise it to a document.</i></p>
<p><b>One consequence matters for this book’s method.</b> The 2026 family presentation reproduces
plate 84 of that same book. <i>The presentation and Haddadin 2024 are therefore one evidentiary
stream, not two independent witnesses</i> — which is why the badges on this line change at 1500 (see
below). Where this book does count two witnesses for Rāshid, they are <b>Haddadin 2024 on the Karak
side and Shāhīn 1982 with the co-authors’ chart on the Ramallah side</b>, which are genuinely
independent of each other.</p>"""),

ent('1869 → 1963', 'attested', True, 'The people this town produced',
 'A village of three thousand souls, on one ridge, in one century — and this is a partial list.',
 f"""
<p><b>Miriam Karam</b> stopped Eli Jones in a narrow street — the Quaker account dates the encounter
to 1867 — and asked him to open a school for girls. He asked who would teach it. <i>“I will,”</i> she
said. <b>It opened in 1869 with twenty pupils and grew quickly to fifty</b>; it became a boarding
school, the Girls Training Home, in 1889, and took the name Friends Girls School in 1925. <b>She herself taught four years</b>, then married and left — and the school
she started is still open{c('Shāhīn (1982), the education chapter. She was not a native of Ramallah but lived there several years; she married Hanna Bayyuk of Jerusalem.')}. <b>Katie Gabriel</b>, Lebanese, ran the boarding school
from 1889 and gave the Friends forty years.</p>
<p><b>Dr Philip Assʿad Maʿlouf</b> came from Beirut in 1891, opened his own clinic in 1895, and for
years was <i>the only doctor in the entire Ramallah district</i>. The town called him <b>Hakeem Abu
Iskandar</b>. In 1906 he pulled a twelve-year-old boy through forty days of typhoid fever; the boy
was ʿAzīz Shāhīn, who lived to write this history. <b>Maʿlouf himself died in the typhus of
1916.</b> He used to say that a doctor got no credit in Ramallah: the people waited until a man was
nearly dead to call him, and then blamed him if the man died{c('Shāhīn (1982), “Medical Treatment.” His predecessor, Dr George Hassenauer of the Friends clinic (1883–89), was called <b>Dr Ḥassan Nawwār</b> because the town could not pronounce his name.')}.</p>
<p><b>Boulos Shehadeh</b>, born in Ramallah in 1882, founded <i>Mirʾāt al-Sharq</i> in Jerusalem on
17 September 1919 — 1,132 surviving issues, digitised, with 1,535 mentions of his home town.
<b>Khaleel Totah</b>, born here in 1886, ran the Friends Boys School and argued Palestine’s case
across the United States for thirty years, leaving diaries that are now a source for the Mandate; the
school’s auditorium — which he raised the money for — carries his name. <b>Dr Fuad Shatara</b> (1892–1942), a physician on the staff of Cumberland
Hospital in Brooklyn, was an early leader of the Ramallah Young Men’s Society of New York — he helped
organise its anti-Balfour demonstration of 8 November 1917 — and later president of the Arab National
League, arguing the Arab case for Palestine on American platforms{c('Shāhīn (1982), “Notable Individuals,” “Societies,” and the education chapter.')}.</p>
<p><b>In 1924 a group of Ramallah women founded the Nahda Women’s Association</b> and registered it
on 1 January 1925 — the town’s first women’s society, and their own. It outlived the Mandate, the
Nakba, the Jordanian years and the occupation, and was still serving about a hundred hot meals a week
when Shāhīn wrote. Into that town came <b>Matiel Mogannam</b>, who had already been a secretary of the
Arab Women’s Executive of 1929 and had argued the Palestinian case in English in <i>The Arab Woman
and the Palestine Problem</i> (London, 1937); from 1938 she lived here, and in 1939 she formed the
Women’s Union Society, which put looms and embroidery frames into paid women’s hands and in 1961
opened a home for the town’s old women{c('Shāhīn (1982), “Societies”: the Nahda (1925), the Infant Welfare Society (1927, Mrs Neʿmeh Joseph Kaddoura), the Women’s Union (1939), the Girl Guides (1942), and the Handicraft Cooperative (1954, Miriam Yaʿcoub Zaʿroor — the first cooperative society in Palestine, fifty women, all skilled embroiderers).')}.</p>
<p><b>Khaleel Abu Rayya</b> opened the National College in 1947 and kept it running until 1971 — the
last fourteen years partly paralysed by a stroke — then took charge of the Ramallah Public Library he
had founded. <b>Dr Saʿadallah Kassees</b> was both doctor and mayor. <b>Laila Kassees</b>, his
niece, became <i>the first woman of Ramallah to qualify as a doctor</i>, and practises in Memphis.
And <b>Joseph Jiryes Cadora</b>, pharmacist and mayor from 1943 to 1952, wrote the town’s first
history and printed it in New York{c('Shāhīn (1982), the education and notable-individuals chapters; Cadora’s mayoralty and his 1954 book, on which see the entry above.')}.</p>
<p><i>Most of them were born into, or married into, the eight clans on the diagram above — that is
what a ḥamūla was for. But not all: Katie Gabriel was Lebanese, Dr Maʿlouf came from Beirut, and
Matiel Mogannam was born in Lebanon and only settled here in 1938. <b>The town was served by people it
never absorbed, and it is worth saying so in a book about absorption.</b></i></p>"""),

CH(14)

ent('I', 'attested', True, 'Our origins',
 '<b>Proven as far as origins of this kind can be — and said exactly:</b> <b>the dynasty this family claims</b> is real and named in contemporary sources at generations 33–34 (Procopius, in Greek, in al-Ḥārith’s lifetime); <i>the family’s descent from it is not, and this book does not say it is.</i> That dynasty is credited with sixth-century church mosaics at Nitl, ten kilometres from Maʿīn on the road the tradition names; a Ghassān population is still recorded in Transjordan — at Gharandal, far to the south — as late as al-Yaʿqūbī, c. 890. And the gap in the chart is not a scandal but a number: <b>about thirty-one generations in that stretch, thirty of them with no name at all, honestly printed as a void where others forged pedigrees</b>.',
 f"""
<p><b>Go back to Figure 1 and read the grade column downward.</b> Nine links carry this family from
Adam to this morning, and they do not rest on the same kind of thing. A sceptic always aims at link
two — the identification of Joktan with Qaḥṭān — but that link is a thousand years old and every
Qaḥṭānī Arab in the world stands on it. <b>The real weak point is link seven, the void — and the
family’s own chart is the thing that says so.</b></p>
<p>The deep line above generation 30 is scripture and classical scholarship, asserted as such and
defended as such — and generation 29’s entry of the name Al-Ghassānī matches the classical sources
exactly, <i>which nobody arranged</i>. But the strongest argument for this chart is not what it
claims. It is what it refuses to claim.</p>
<div class="fix"><div class="fixhead">The standard this claim was measured against</div>
<div style="font-size:.95rem;line-height:1.6;color:#46423B">
<p style="max-width:none"><b>Issa Maalouf</b>, a Lebanese Orthodox historian, wrote his family’s
history with <i>no</i> Ghassanid claim in it. Around <b>1906</b> he added, in his own hand, the
sentence “the correct view is that they are Ghassanids”; by <b>1908</b> he had published a specific
chain of named ancestors running back to a Ghassanid king. Ottoman documents of <b>1524, 1525 and
1533</b> record the same family with no such lineage{c('On the Maʿlūf genealogical claim and its documentary refutation from Vatican Syriac MS 333 (1524) and the Ottoman <i>tapu taḥrīr</i> registers of 1525 and 1533. The critical study is available online; this project has not read the printed version and flags the author attribution as unconfirmed.')}. <b>The pedigree was invented, in
writing, inside two years, for the politics of its moment</b> — and several other Levantine Christian
families made structurally identical claims in the same period.</p>
<p style="max-width:none"><b>And unlike Maalouf’s, this family’s claim was first written down by
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
this family’s own chart was compiled from, in another country, at the same
period</i>{c('Ighnāṭiyūs Ṭannūs al-Khūrī, <span class="ar">المشايخ آل الشمر حكام العاقورة والزاوية</span> (1948), read for this book in the scanned copy on the Internet Archive; the passages quoted are from the chapter <span class="ar">اسم الأسرة الشمرية وأصلها</span> and the chapter on Banū Ghassān. He cites Ibn Khaldūn for thirty-two Ghassanid kings over six hundred years and Nöldeke, <i>Die ghassânischen Fürsten</i>, in the Arabic version of Bandaliyya and Nadīq, for thirty-seven. <b>That monograph has since been pressed into service, in our own century, to support a claim of surviving royal descent and title. This book takes no view on that beyond one observation: its author took no such view either.</b> He wrote <i>zaʿm</i>, and he printed where his chain broke.')}.</p>
<p style="max-width:none"><b>So the pattern is the pattern, and it is not a scandal.</b> Christian
families across the Levant fixed a Ghassanid descent in writing in the first half of the twentieth
century, compiling the deep end from the same nineteenth-century European and Arabic tables. Some
printed it as a claim. One invented a chain of names. <b>What distinguishes them is not whether they
had a gap — they all had the same gap — but what each of them did with it.</b></p>
<p style="max-width:none"><b>This family has that gap and does not fill it.</b> Ours runs from
<b>569 to about 1500</b>: thirty generations with no name of any kind, and this book prints them as a
void, thirty blank slots on every ladder in it. <i>The difference between a history and a pedigree is
what you do with the blank.</i> John Mogannam’s chart prints generation 35 as a void where Maalouf
printed a forgery, and al-Khūrī printed <i>zaʿm</i>. <b>Two of those three are honest documents, and
ours is one of them.</b></p></div></div>"""),

ent('II', 'attested', True, 'Our contribution to the Palestinian people',
 '<b>The family is one arrival among ten that became one people.</b> The genetics say the population of this land absorbed every newcomer for four thousand years; the family’s stream — Christian Arabs out of the Ghassanid south — was absorbed like the rest, and then did its own absorbing: eight outsider families folded into the clans from 1750, a Muslim neighbour taken into the clan structure in 1923 — in a town that had had Muslim households since 1538 — some nine thousand refugees taken in by a town the government had counted at 5,080 in 1945. <i>The tradition says we came from somewhere. The ground says we have been here the whole time. Both are true at once, and in this country they always have been.</i>'),

ent('III', 'documents', True, 'The founding of Ramallah',
 'On the documents: <b>named 1279 · uninhabited waqf land 1525–28 · four households 1538–39 · the group at Bayt Jālā 1553–54 · THE FOUNDING 1562 · the deed in court 1565 · <b>eighty households counted 1596, and their names still unread in Ankara</b></b>. On the tradition: Rāshid, the ford, the forge, the purchase from the Ghazāwneh, “about 1550.” <b>The document and the memory are twelve years apart, and the memory loses nothing by the correction.</b>',
 f"""
{NUMTABLE('THE KEY DATES — one page, for the book',
 ['Date', 'Event', 'Carried by'],
 [['8th–7th c. BCE', 'The Maʾrib dam is built, in the country scripture assigns the line', 'inscription + both family texts'],
  ['528–569', 'Al-Ḥārith ibn Jabala, phylarch — generation 34', 'Procopius, contemporary'],
  ['543–548', 'The dam breaks (Abraha’s repair, CIH 541); final collapse follows', 'inscription'],
  ['c. 890', 'Last named Ghassān population in Transjordan — Gharandal', 'al-Yaʿqūbī'],
  ['<b>c. 1300</b>', '<b>Ghassān still entered as a living people — al-Balqāʾ, the Yarmūk, Ḥimṣ</b>', 'al-Ḥamdānī the <i>mihmandār</i>, via al-ʿUmarī and al-Qalqashandī'],
  ['1495', 'Mujīr al-Dīn, at Jerusalem, mentions the Ghassānids once and formulaically', '<i>al-Uns al-jalīl</i>, searched complete in two editions'],
  ['1186', 'Rām Allāh first named — pledged by a Crusader king against a debt', 'Ḥammūdeh (2014), p. 39'],
  ['1279', 'The hill endowed to the Ibrāhīmī sanctuary at Hebron', 'sijill 48, p. 88 (1565)'],
  ['c. 1500', 'Rāshid al-Ḥaddādīn — generation 66', 'both family texts'],
  ['<b>1562</b>', '<b>The founding: 64 Christian households and 7 unmarried men, against 10 Muslim</b>', 'the register of 970/1562, transcribed in full'],
  ['1596–97', 'The register counts 80 households, 71 Christian — the names are in Ankara, unread', 'the defter'],
  ['1850 · 1852', 'The present church — portal datestone 1850, inauguration usually given as 1852', 'Shāhīn + the carved portal'],
  ['1901', 'The first four sail for America', 'Shāhīn, name by name'],
  ['1908', 'Ramallah a city — one councilman per clan', 'the town record'],
  ['1916', 'Typhus — Shāhīn puts the losses near a third; no independent record survives', 'Shāhīn, as family memory'],
  ['1948', 'The town triples with refugees', 'the local count of 1953'],
  ['20 May 1963', 'The hospital the diaspora paid for opens', 'the Foundation’s record'],
  ['1952 · 1958 · 1959', 'The Federation — begun, incorporated, constituted. The three dates are not yet reconciled', 'unresolved; see the correction']],
 'Entries carried by both key texts — Shāhīn (1982) and the Mogannam chart/presentation — are the spine; documents refine them. <b>Three entries rest on memory alone or on memory in conflict, and are marked as such:</b> the typhus toll of 1916, the four who first sailed in 1901, and the Federation’s founding date.')}
{fig(R.fig_master(),'The whole story on one scale',
 'Adam to the present, with the evidence that carries each stretch. Read left to right, the chart is a map of what kind of thing holds the story up at each point — and where the joints are.',
 'This book, throughout; the six grades applied consistently.')}
<p><i>The full test — all thirty-six checkable claims, one by one, with the verdict on each — is
printed at the end of this book, after the bibliography.</i></p>
<p><b>What remains open, and where it will be settled:</b> Ramallah City Hall — two named targets in one building: <b>ʿAdnān
al-Ḥaddādīn’s handwritten manuscript of 8 August 1953</b>, whose migration account Shāhīn prints
whole, and <b>the Turkish census book Shāhīn personally found and used there</b>, which he cites for
a figure of 13,600 souls (almost certainly the district rather than the town); the Jerusalem sijill
48, p. 54, read in the original; <i>Mirʾāt al-Sharq</i>, 1,770 digitised issues with 1,535 mentions
of the town; the Federation’s own incorporation papers; and, if the family wishes it, Y-DNA — the
only genuinely new evidence this history can still acquire{c('The open leads in full, with their targets named, in the project’s research notes; the Maalouf case (a Ghassanid pedigree demonstrably invented 1901–1908) is the standard the family’s claim was measured against — and survives, precisely because the chart printed a void where Maalouf printed a forgery.')}.</p>
<p class="closing"><b>A family that can tell the difference between what it remembers and what it can
prove — and prints both — has a history, not a story about itself.</b> This is that history: one
line, from Adam and Eve to this morning, with the evidence attached at every date where evidence
exists, and the gaps drawn where it does not.</p>""")

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
town&rsquo;s mayor from 1943 to 1952. Sāmiḥ Ḥammūdeh&rsquo;s archival work on the founding — the work
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

.byline{margin:8px 0 0;font-size:1.06rem;letter-spacing:.05em;color:#1A1A1A}
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

figure{margin:26px 0;padding:0;border:1px solid #DCD6C9;border-radius:6px;background:#FCFBF8;overflow:hidden}
.fignum{background:#F6F3EC;color:#B98A4E;font:10px/1 "Times New Roman",Times,serif;
  font-weight:700;letter-spacing:.24em;text-transform:uppercase;padding:10px 18px 8px;border-bottom:1px solid #EFEBE2}
.figtitle{font-size:1.06rem;font-weight:700;padding:12px 18px 0}
.figwrap{padding:6px 12px 4px}
.figwrap svg{display:block;width:100%;height:auto}
figcaption{padding:6px 18px 16px;color:#46423B;font-size:.92rem;line-height:1.55;max-width:none}
figcaption .src{display:block;margin-top:7px;color:#9A958C;font-size:.82rem;font-style:italic}

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
  .fignum::after{content:" · swipe the plate →";letter-spacing:.12em;color:#9A958C}
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

def render():
    out = []
    for num, kicker, title_c, sub_c in CHAPTERS:
        grp = [e for e in E if e[1] == num]
        if not grp:
            continue
        band = (f'<div class="eraband"><div class="ek">{kicker}</div>'
                f'<h2>{title_c}</h2><div class="es">{sub_c}</div></div>')
        out.append(f'<div class="erahead" id="ch{num}">{band}{linkat(num)}</div>')
        for e in grp:
            if e[0] == 's':
                _, _c, lab, sub = e
                sb = f'<span class="ss">{sub}</span>' if sub else ''
                out.append(f'<div class="sect"><span class="sl">{lab}</span>{sb}</div>')
                continue
            _, _ch, date, grade, w2, title, note, bodyc = e
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
    return ''.join(out)

CONTENTS = ('<div class="contents"><h4>The eras &mdash; one chapter each</h4><ol>' + ''.join(
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

HOWTO = f"""
<div class="howto"><h4>How to read this book</h4>
<p><b>It is one line.</b> Every event, from Adam and Eve to this morning, sits at its own date on a
single unbroken timeline, and the evidence for it — the maps, the charts, the tables, the
corrections — sits directly beneath it, at the same date.</p>
<p><b>Two texts are the keys:</b> ʿAzīz Shāhīn’s history of 1982 and John Aziz Mogannam’s chart of
thirty-six generations. Where both carry an entry <i>and testify independently</i> it wears
<span class="w2">TWO WITNESSES</span> — and from 1500 onward they do testify independently, because
Shāhīn writes the town’s own history from local memory and local records while the chart is a
genealogy. <b>Before 1500 they do not.</b> There the chart follows the classical Arabic
<i>ansāb</i> tradition, which is also where Shāhīn's deep lineage comes from, so those entries wear
<span class="w2 sh">ONE TRADITION</span> instead: both texts carry the claim, but they are drinking
from the same well. <i>This distinction was introduced after research showed that the family’s 2026
presentation reproduces a modern reconstruction rather than an independent source.</i>
Every entry also carries a grade, saying what kind of thing holds it up:
<span class="g" style="background:#D5E9DF;color:#1A1A1A">SCRIPTURE</span>
<span class="g" style="background:#A9CDB8;color:#1A1A1A">CLASSICAL</span>
<span class="g" style="background:#79B491;color:#1A1A1A">ATTESTED</span>
<span class="g" style="background:#007A3D;color:#fff">DOCUMENTS</span>
<span class="g" style="background:#F6EEDF;color:#7A5A28">ORAL TRADITION</span>
<span class="g" style="background:#FDF6EC;color:#8A5A1E">NO EVIDENCE</span>&#8202;.
A document outranks a memory, and the memory is kept anyway; an inference is drawn as an inference;
a conflict is printed as a conflict; and where the record corrects the family, the correction
appears in a marked box at the date where it happens.</p>
<p><b>The chapters are the eras of this land</b>, from the first people who lived on it to the city
it holds today — Natufian, Canaanite, Iron Age, Persian and Hellenistic, Roman, Byzantine, early
Islamic, Crusader and Mamluk, Ottoman, Mandate. <i>The land is the spine of this book, and our own
family is one of the things that happened to it.</i></p>
<p><b>Our own line runs through the eras as a chain of nine links</b>, and every era opens with a
strip saying where that chain stands — which link we are on, and what evidence there is for it in
that era. Often the honest answer is <i>none</i>, and the strip says so. Figure 1 sets out all nine
links at once, each with the source that carries it and, printed for the first time in this edition,
<b>what would break it</b>.</p>
<p><b>One change of method matters more than any of the others.</b> John Mogannam’s chart of
thirty-six generations, which earlier editions of this book were built on, <i>is no longer treated as
a source</i>. <b>Its compiler is one of this book’s two authors</b>, which makes the point sharper
rather than softer: a chart cannot be its own evidence, least of all when the people printing it are
the people who drew it. So it is set out whole in the appendix as the family’s own guide — and a very
good one — with the points at which the texts correct it marked, and everything in the chain here is
built from Genesis, the Arabic genealogists, Procopius and the registers directly. <i>Every
correction to that chart in this book is a correction the co-authors make to themselves.</i></p>
<p><b>And the chart’s count is corrected here for the first time.</b> Its generation 35 draws
nine hundred and thirty-one years as a single line. That stretch is about <b>thirty-one</b>
generations, so the line from Adam to Rāshid is <b>sixty-six generations, not thirty-six</b> —
thirty-six of them named, thirty with no name at all. <i>The ladder in every era strip is drawn on
that count.</i></p>
<p><b>How the generations are numbered — two numbers, and they are not the same.</b>
<b>The chart's number</b> counts its own thirty-six rows, one of which is a nine-hundred-year void
drawn as a single line. <b>This book's number</b> counts generations: <b>sixty-six</b> from Adam and
Eve to Rāshid, and about eighteen more to this morning, <b>eighty-four in all</b>. So <i>“the
Mogannam chart, generation 36”</i> means Rāshid's row on the chart, and <i>“generation 66”</i> means
Rāshid. Generations 1 to 34 carry the same number in both.</p>
<p><b>The line ends by proving three things</b> — where we come from, how we became part of the
Palestinian people, and when and how Ramallah was founded — with the key dates on one page. <b>After
the bibliography comes the test harness</b>: all thirty-six checkable claims from the family's own
presentation, each with the verdict on it, printed so the audit can be re-run by anyone.</p>
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
 'male-line generation of twenty-two years, which no observed population sustains; the stretch is '
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

html_parts = ['<div class="pbar"><i></i></div>',
f"""<header class="masthead"><div class="wrap">
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

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w', encoding='utf-8', newline='\n').write(html)
print('WROTE', OUT, f'{len(html):,} bytes ·', FIGN[0], 'figures ·', len(CITES), 'notes')
