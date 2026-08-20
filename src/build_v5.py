# -*- coding: utf-8 -*-
"""THE ONE LINE, fifth edition — the whole book as a single unbroken chronicle.
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
  'Rome paves the ridge road, ranks this district second after Jerusalem, and writes its villages down — and the Gospels put the Lord on that road twelve kilometres from the future town.'),
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
 'Every dot is a site with a published excavation and a calibrated date, and every distance is measured from the centre of Ramallah. The nearest of them, Tell en-Naṣba, is three kilometres away. <b>What the map cannot show is how little of these highlands has been dug</b>: the blank spaces are gaps in the survey record, not gaps in the past, and this book says so rather than implying the district was empty.',
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
 'Twenty-three kilometres down the eastern slope from this ridge, at <b>Tell es-Sultan</b>, people stopped moving and stayed. Permanent settlement from about <b>9600 BC</b>; a round stone tower <b>8.5 metres high with twenty-two steps inside it</b>, built about <b>9000 BC</b>; a wall 3.6 metres high and 1.8 metres thick at the base{}. <i>It is twenty-three kilometres from Ramallah as the crow flies, and it is one of the earliest permanent settlements known anywhere on earth.</i>'.format(c('Kathleen M. Kenyon &amp; T. A. Holland (eds), <i>Excavations at Jericho, Vol. 3: The Architecture and Stratigraphy of the Tell</i> (London: British School of Archaeology in Jerusalem, 1981). The tower is c. 8.5 m high and c. 9 m across at the base, tapering to c. 7 m, with an internal staircase of twenty-two stone steps; the wall over 3.6 m high and 1.8 m thick at the base. Earlier work: Sellin and Watzinger 1907–11; Garstang 1930–36, whose Bronze Age dating Kenyon overturned.')),
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
years old — around 9000 BC. This book uses the calibrated figures throughout.</p>""".format(
  a=c('On the occupation gaps and the making of the “oldest city” claim, see Rachael Sparks, Bill Finlayson, Bart Wagemakers &amp; Josef Briffa (eds), <i>Digging Up Jericho: Past, Present and Future</i> (Oxford: Archaeopress, 2020) — the best single volume on the evidence and its historiography. For the older towers: R. F. Mazurowski &amp; Y. Kanjou (eds), <i>Tell Qaramel 1999–2007</i> (Warsaw: PCMA, 2012), with radiocarbon in Mazurowski et al., <i>Radiocarbon</i> 51:2 (2009), 771–81: the earliest tower c. 10,900–9,670 cal BC.'),
  b=c('UNESCO World Heritage List no. 1687, “Ancient Jericho/Tell es-Sultan,” inscribed 2023 at the extended 45th session of the World Heritage Committee, Riyadh, under the State of Palestine, on criteria (iii) and (iv). The statement of Outstanding Universal Value describes deposits “dating back to about 10,500 BC” and a “sizeable permanent settlement.” <a href="https://whc.unesco.org/en/list/1687/">whc.unesco.org/en/list/1687</a>.'),
  d=c('Kenyon &amp; Holland (1981) for the defensive reading; Ofer Bar-Yosef, “The Walls of Jericho: An Alternative Interpretation,” <i>Current Anthropology</i> 27:2 (1986), 157–62, for flood defence and the absence-of-warfare argument; Danny Naveh, “PPNA Jericho: A Socio-Political Perspective,” <i>Cambridge Archaeological Journal</i> 13:1 (2003), 83–96; Ran Barkai &amp; Roy Liran, “Midsummer Sunset at Neolithic Jericho,” <i>Time and Mind</i> 1:3 (2008), 273–83.'))),

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
 'Not a general claim about “the region” — <b>named, excavated, dated sites within a few kilometres of the town</b>. <b>Tell en-Naṣba</b>, on the edge of al-Bīra and three kilometres from Ramallah’s centre, is a Late Chalcolithic and Early Bronze I village of about 3500–3300 BC{}. <b>et-Tell</b>, five kilometres east, is an Early Bronze town occupied 3200–2400 BC{}. <b>ʿAin Samiya</b>, fifteen kilometres north-east, holds an Intermediate Bronze shaft-tomb cemetery of 2300–2000 BC — the source of the famous ʿAin Samiya goblet{}.'.format(
  c('Tell en-Naṣba, identified with biblical Mizpah, on the edge of al-Bīra. Excavated in five seasons, 1926–1935, by William Frederic Badè for the Pacific School of Religion. The Late Chalcolithic / Early Bronze I village is Stratum 5, c. 3500–3300 BC, after which the site was long abandoned.'),
  c('et-Tell, generally identified with biblical Ai, 5.3 km east of Ramallah. Excavated by John Garstang (1928), Judith Marquet-Krause (1933–35), Joseph Callaway (1964–72) and Hani Nur el-Din (2005–07). Occupation runs from Early Bronze I through Early Bronze III, c. 3200–2400 BC.'),
  c('ʿAin Samiya and the neighbouring Dhahr Mirzbaneh, 13 km north-east of Ramallah: Intermediate Bronze Age (Early Bronze IV) shaft-tomb cemeteries, c. 2300–2000 BC. Paul Lapp excavated Dhahr Mirzbaneh in 1963; Zvi Yeivin excavated ʿAin Samiya in 1970–71. The ʿAin Samiya goblet is an Intermediate Bronze piece, not a Chalcolithic one.')),
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
replaced.</b> The Philistines are the case that can be measured: they arrived about 1175 BCE, from
the Aegean, visible in the genome at Ashkelon — and then, <b>“within no more than two centuries,
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

ent('c. 1350 BCE', 'documents', False, 'The Amarna letters',
 'Jerusalem, Shechem, Gezer and Lachish write to Egypt in Akkadian{}. These are the city-states of this landscape, and they are Canaanite. Even the town’s own name keeps the era’s sound: <span class="ar">رام</span> is a Semitic root meaning <i>height</i> — Canaanite-era vocabulary still doing its job{}.'.format(
  c('The Amarna correspondence, 14th c. BCE.'),
  c('al-Dabbāgh, <span class="ar">بلادنا فلسطين</span>, viii/2, on <span class="ar">رام</span>; the same root as Hebrew <i>rām</i> and Aramaic <i>rāmā</i>.'))),

CH(3)

ent('c. 1175–840 BCE', 'attested', False, 'The neighbours: Philistines, Phoenicians, Arameans — and the kingdoms across the Jordan',
 'While the highland villages went on terracing the same slopes, the coast and the plateau filled up with peoples whose names are still in the language: the <b>Philistines</b> at Gaza, Ashkelon and Ashdod; the <b>Phoenicians</b> at Tyre and Sidon; the <b>Arameans</b> inland at Damascus; and across the river <b>Moab, Ammon and Edom</b>. <i>Every one of them was eventually absorbed into the population of this region. Not one of them replaced it.</i>',
 """
<p><b>One of these neighbours matters directly to this family.</b> The plateau the tradition names as
its road out — Karak and Shawbak — is ancient <b>Moab</b> and ancient <b>Edom</b>; Karak itself is
generally identified with the Kir of Moab of the Hebrew Bible. And Moab left a document. The
<b>Mesha Stele</b>, cut about 840 BCE and found at Dhībān in 1868, is the longest Iron Age
inscription anyone has recovered from this landscape, written in Moabite — a language so close to
Hebrew that it can be read straight off the stone. <i>The plateau the family remembers as a place of
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

sect('Meanwhile, in the land', 'Assyria, and the road that already joined the two ends of this story')
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
 'The sanctuary on Gerizim is dated archaeologically to the <b>mid-fifth century BCE</b>; when the separation from Judaism became final is disputed, and the decisive rupture is usually placed at the Hasmonean destruction of the temple there, about <b>110 BCE</b>{}. What is not disputed is the sequel: the Samaritans are <b>still on that mountain</b> — reduced from a Byzantine-era population in the hundreds of thousands to about 150 souls by 1900, and recovering to some 900 today{}. <b>Continuity in this landscape is observable, not rhetorical.</b>'.format(
  c('Y. Magen, <i>Mount Gerizim Excavations</i> I–II (Israel Antiquities Authority, 2004, 2008), for the mid-fifth-century sanctuary; Gary Knoppers, <i>Jews and Samaritans: The Origins and History of Their Early Relations</i> (Oxford, 2013), ch. 1, for the range of dates proposed — from Ezra to 70 CE; Josephus, <i>Antiquitates</i> XIII.255–56, for John Hyrcanus and the destruction of the Gerizim temple. <b>Earlier editions of this book printed a flat “c. 400 BCE,” which no source supports.</b>'),
  c('On Samaritan demographic history: the Byzantine-era revolts of 484, 529 and 555 and the collapse that followed; census counts of 163 (1922) and 182 (1931); c. 900 today at Holon and Kiryat Luza.'))),

CH(6)
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
prayed on for some seven hundred years, from the Roman period until the earthquake of 749{c('Salah al-Houdalieh’s excavations at Khirbet et-Tireh, from 2013 — two contemporaneous churches, a monastery and an oil press, two kilometres west of the present town centre; the site was abandoned after the earthquake of 749 and reoccupied only in the Ottoman period. Hamdan Taha at ʿAbūd. See the bibliography, §XVIII and §XXIX. <b>Earlier editions said “a thousand years before the founding,” which implied an unbroken occupation the excavation does not show.</b>')}. <i>Only the name Ramallah is missing from
every text — the neighbours are Roman, the ground is Byzantine, the name will be Mamluk.</i></p>"""),

ent('c. 30 CE', 'documents', False, '“A city called Ephraim, and there continued with his disciples”',
 'John 11:54. The city is generally identified with <b>Ṭaybeh, twelve kilometres from Ramallah</b>{} — still, today, the last entirely Christian town in Palestine.'.format(c('John 11:54: <span class="gk">εἰς Ἐφραὶμ λεγομένην πόλιν</span>. The identification with eṭ-Ṭayyibeh is standard from Robinson (1841) and the <i>Survey of Western Palestine</i>, resting on Eusebius and the villagers’ retained memory of the older name; Albright preferred ʿAyn Sāmiya.')),
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

CH(6)

sect('And in our own line', 'The name enters at a spring in Yemen — four thousand miles from this ridge')
ent('c. 250 → c. 350', 'documents', False, 'THE NAME, IN STONE — Ghassān in two Sabaic inscriptions',
 'Everything the family carries hangs on one word, and until now this book took that word entirely from the Arabic genealogists, writing five hundred years after the fact. <b>It does not have to.</b> Ghassān is named twice in South Arabian inscriptions cut while the Jafnids were still unheard of{}.'.format(c('<b>ʿInān 75</b>, mid-third century AD, recording an embassy to “the kings of the peoples (<span class="ar">أشعب</span>) of Ghassān, al-Asd, Nizār and Madhḥij”; <b>ʿAbadān 1</b>, roughly a century later, on a Ḥimyarite campaign “between the land of Nizār and the land of Ghassān.” Both in the Sabaic corpus; see the DASI database (Università di Pisa / CNR) and the discussion in Christian Julien Robin’s work on the Arab peoples of the pre-Islamic peninsula.')),
 f"""
<p><b>ʿInān 75</b>, from the middle of the third century AD, records a Sabaean embassy sent to
<i>“the kings of the peoples of <b>Ghassān</b>, al-Asd, Nizār and Madhḥij.”</i> <b>ʿAbadān 1</b>,
about a century later, has a Ḥimyarite army campaigning <i>“between the land of Nizār and the land of
<b>Ghassān</b>.”</i> In both, Ghassān is a <i>shaʿb</i> — a large territorial grouping with kings of
its own — and in both it is placed in north-central Arabia, on the road out.</p>
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
twenty-seven Christian households come up the ridge road in 1562, <b>they are not bringing
Christianity to these hills. They are joining a Christian population that has been in this district,
continuously, since before Arabic was the language of it.</b> The family’s faith is the oldest thing
about this story that can be verified without reference to any genealogy at all.</p>"""),

ent('473', 'attested', False, 'Amorkesos signs a treaty with Byzantium',
 'A well-dated fifth-century federate arrangement covering Palaestina Tertia — <b>though not the earliest: Queen Mavia’s treaty with Valens is a century older</b>{}. The system the family’s ancestors are said to have led is already running.'.format(c('The Amorkesos episode is known from a fragment of Malchus preserved by Photius (fr. 1, ed. Blockley); Shahîd, <i>Byzantium and the Arabs in the Fifth Century</i> (Dumbarton Oaks, 1989), 61–113, reconstructs it as a formal <i>foedus</i>, which others dispute. <b>Mavia’s treaty with Valens, c. 377–378, is nearly a century earlier and is attested by four independent church historians — Rufinus, Socrates, Sozomen and Theodoret. Earlier editions of this book called Amorkesos “the earliest,” which is wrong.</b>'))),

CH(7)
sect('And in our own line', 'The dynasty, in contemporary Greek — and the water that failed')
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

CH(8)

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

ent('1058', 'documents', False, 'A village church is rebuilt at ʿAbūd — dated, inside the silence',
 'About eighteen kilometres north-west of the future Ramallah, the church at <b>ʿAbūd</b> is rebuilt, and the work is dated{}. <i>Nothing in the family record covers this year. The hills do.</i>'.format(c('The rebuilding of the church at ʿAbūd, dated 1058, among the dated Christian records of these hills between the seventh and sixteenth centuries; Hamdan Taha\u2019s work at \u02bfAb\u016bd. See the bibliography, \u00a7XXIX.'))),

CH(9)

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
 'Four dated traces, none of them written by anyone in this family, all of them inside the blank the chart prints: <b>a Frankish charter of 1182 signed by one <i>Raymundus de Jafenia</i></b>; the pilgrim <b>Thietmar at Shawbak on his journey of 1217–18</b>, hosted and fed by a Frankish widow living in the suburb, where Christians and Muslims lived side by side; <b>a Christian majority still at Shawbak in 1321</b>; and <b>men of Jifnā named in the Jerusalem Ḥaram al-Sharīf documents</b>, a corpus overwhelmingly of 793–794 AH / 1391–92{}.'.format(c('The Jifnā inscription of 1179 and the Jerusalem Ḥaram documents of 1374 (Little, <i>A Catalogue of the Islamic Documents from al-Ḥaram aš-Šarīf</i>); Thietmar, <i>Peregrinatio</i>, the journey of 1217–18; the stop at Shawbak (Mons Regalis) is dated 1217 in the Transjordanian survey literature and 1218 elsewhere, so this book gives the journey rather than the year; the Christian majority at Shawbak in 1321 from the Mamluk-period record.')),
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
the first Ḥaddādīn named in an Ottoman register, there were continuously Christian populations at
both ends of the road the tradition describes — the Karak–Shawbak plateau in the south, and this
ridge in the north. <i>A migration story requires a population at each end. Both ends are documented.
The journey between them is not.</i></p>""" + FIX(
 'A grey-haired Greek bishop brings the pilgrim Thietmar bread and cheese at Karak in 1217.',
 'The pilgrim <b>Thietmar</b> was hosted at <b>Shawbak</b>, on his journey of <b>1217–18</b>, by <b>a Frankish widow</b> living in the suburb — <b>not by a bishop, and not at Karak</b>.',
 'Thietmar’s own <i>Peregrinatio</i> is explicit about the place and the person; earlier editions of this book conflated two separate episodes. <b>The year is the one part still loose</b> — the Transjordanian survey literature dates the Shawbak stop to 1217, other accounts to 1218 — so this book prints the journey, 1217–18, rather than choosing. <b>The corrected reading is weaker as an anecdote and stronger as evidence</b>: a resident Frankish widow, in a suburb where Christians and Muslims lived side by side, shows an ordinary settled population, where a visiting bishop would have shown only a visit.')),

ent('1186 → 1330', 'documents', False, 'THE NAME APPEARS — a hundred years earlier than this book has been saying',
 f"""<b>Two Crusader documents name this place a century before the Mamluks.</b> On <b>7 March 1186</b>
Guy de Lusignan, king of Jerusalem, owes money to the German hospital in the city, and pledges that if
he cannot pay within the year <b>the village of Ramallah becomes the hospital’s property</b>. And Rey
found <i>Ramalei</i> in a manuscript of <b>1198</b>, farmland in the hinterland of
Jerusalem{c('Sāmiḥ Ḥammūdeh, “New Light on Ramallah’s Origins in the Ottoman Period,” <i>Jerusalem Quarterly</i> 59 (2014), p. 39, citing Nayrūz and E. G. Rey, <i>Les colonies franques de Syrie aux XIIe et XIIIe siècles</i>, and Yūsuf Qaddūra for a second twelfth-century agreement. <b>Earlier editions of this book said the name first appears in 1279. It appears in 1186 — in an article this project already held.</b> ' + D('2014_Hammoudeh_New_Light_Ramallah_Ottoman_JQ59.pdf') + '.')}.
<i>Ramallah was a working hillside with a name and a price on it while the Crusader kingdom still
stood.</i>""",
 f"""
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
divided by the observed male-line generational interval of twenty-five to thirty-five years, is
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
 'Before looking for the missing generations it is worth checking the count that is usually quoted. Forty-five generations across a thousand years implies a male-line generation of twenty-two years, shorter than any observed population sustains. Thirty-one generations at thirty-two years each fits. <b>Correcting the arithmetic does not close the void — it measures it.</b>',
 'Generational-interval range after the standard genealogical-demography literature; the span from Jafna (fl. c. 520) to Rāshid (fl. c. 1500).')}
{FIX('A fixed count of generations between Jafna and Rāshid.',
 '<b>A range: about 27 to 37 generations</b>, most probably around 31 — and the line recounted at sixty-six, not thirty-six.',
 'Arithmetic, not a source: Jafna (fl. c. 520) to Rāshid (fl. c. 1500) is roughly 980 years; divided by the observed male-line interval of 25–35 years, that is 28–39 links, of which the chart draws two. No source is needed for a division, and none is claimed.')}
{fig(F.fig_void_solved(),'The void, measured — and shortened',
 'The genealogical void runs 931 years, from al-Ḥārith (d. 569) to Rāshid (fl. c. 1500), and needs about thirty-one generations to cross. The documentary void is three hundred years shorter — a named Ghassān population is attested to about 890 — and five dated records fall inside the blank: ʿAbūd’s rebuilt church in 1058, a man of Jifnā signing a Frankish charter in 1182 and men of Jifnā in the Jerusalem Ḥaram documents, the pilgrim Thietmar hosted in Shawbak’s suburb on the journey of 1217–18, a Christian majority at Shawbak in 1321. What no source supplies is a chain of fathers. So the chart should print the number, not a blank.',
 'Procopius; Shahîd, BASIC I.1 (1995), 554–60; Kennedy (2010), p. 198, citing al-Yaʿqūbī; the ʿAbūd, Jifnā, Thietmar and Shawbak records.')}
<p><b>The silence in the family’s line is not a silence in the family’s world.</b> Chapters seven and
eight have just walked through it dated record by dated record: a people still named in 684, still
located in 890, a church rebuilt in 1058, names in stone in 1179, a pilgrim fed at Shawbak in 1217–18,
a Christian majority there in 1321, men of Jifnā in the Ḥaram registers in 1374, and the town’s own
name on a sultan’s deed in 1279. <i>Everything survives across those nine hundred years except the
one thing a genealogy needs — and the chart is the document that admits it.</i></p>"""),


ent('the shape of the hole', 'documents', False, 'THE VOID IS NOT THIS FAMILY’S FAILURE',
 'One more thing has to be said about the nine hundred years, and it changes what they mean. <b>The family is documented right down to the floor of the archive.</b> The registers that name Rāshid’s children — 1553–54, 1561, 1562, 1565, 1596 — are the <i>first generation of records in which a family of this class could appear at all</i>, anywhere in Palestine.',
 f"""
<p><b>Consider what would have to exist for the void to be filled.</b> Ordinary village families in
Bilād al-Shām do not have documented descent before the sixteenth century, and the ones that do are
not ordinary: they are noble houses with waqf deeds, clerical dynasties with patriarchal archives,
monastic communities with manuscript colophons, or the Cairo Genizah’s Jewish merchants. <b>For a
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
has been found before the nineteenth century</b>{c('The 1553–54 register of Bayt Jālā names the group <span class="ar">الكسابرة</span> and lists 36 Christian heads of household by given name and patronymic — Ḥammūdeh (2014), 44–45. On the wider search: no pre-1800 occurrence of <span class="ar">الحدادين</span> as a Levantine Christian family name has been established. The earliest documented naming of a Ḥaddādīn clan at Karak reachable in this project is Latin Patriarchate material of the 1870s–80s; the earliest scholarly record is Peake (1934). <b>Corpora still unsearched, and named here so the negative can be tested:</b> the Jerusalem sharīʿa <i>sijillāt</i> from 1529 onward beyond register 48; the Karak and Shawbak <i>tahrir defterleri</i>, which are <i>not</i> in Hütteroth and Abdulfattah; the Ḥaram al-Sharīf corpus; Franciscan and Greek Orthodox parish registers; and Christian Arabic manuscript colophons at Sinai, Jerusalem, Balamand and Dayr al-Mukhalliṣ. <i>A caution: <span class="ar">الحدادين</span> is not a unique name — there is an unrelated group among the Banū Asad in Iraq — so any hit must be shown to be Levantine and Christian before it counts.</i>')}.</p>
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
plateau; the second cannot carry a sixth-century origin, because al-Ḥudayda is not a place of any
consequence before the Ottoman centuries.</i> <b>The family’s own historians disagree with each other
about where its name comes from, and that disagreement belongs in this book.</b></p>"""),

CH(11)

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
brought the Kasābra up the ridge road in 1562, with twenty-seven further Bayt Jālā households behind
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

ent('1517–1554', 'documents', False, 'The registers begin — and close in on the founding',
 'Ottoman conquest, 1517. In <b>1525–28 the site of Ramallah is uninhabited</b> — agricultural land of the Ibrāhīmī waqf, exactly the legal status the 1279 deed describes. Four Muslim households appear by 1538–39. And in <b>1553–54 the group called the Kasābra — 36 Christian households — is registered at Bayt Jālā</b>, twenty kilometres south. <i>They are not yet at Ramallah.</i>{}'.format(c('The pre-1596 registers come from Ḥammūdeh (2014), pp. 40–47, working from the Istanbul <i>tapu tahrir</i> series; <b>Hütteroth and Abdulfattah (1977) published only the 1005 AH / 1596–97 <i>mufaṣṣal</i> registers</b> (TK 72, 100, 112, 181, 185, 192, Tapu ve Kadastro archive, Ankara), and earlier editions of this book wrongly credited the whole series to them. '+D('1977_Hutteroth_Abdulfattah_Historical_Geography_of_Palestine.pdf')+'.'))),

CH(12)
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
 '<b>The thirty-six Christian families the register calls the Kasābra, recorded at Bayt Jālā in 1553–54, come up the ridge road</b> — and twenty-seven further Christian families and eight unmarried men come with them. <b>Some sixty-three Christian households, against the ten Muslim families already living on the hill</b>{}.'.format(c('The detailed Ottoman census (<i>tapu tahrir mufaṣṣal</i>) of 970/1562, in Ḥammūdeh (2014), pp. 45–47. Ramallah’s revenue was assigned to endowment, but the document is a fiscal cadastre, not a waqf register, and earlier editions of this book called it one.')),
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
that already had a name, and paid Hebron for the privilege.</i></p>"""),

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
years, and the Ramallah list is larger because twenty-seven further Christian families and eight
unmarried men came with them. <i>This is the strongest documentary moment in the whole book, and it
was in the house.</i></p>
<div class="fix"><div class="fixhead">And now the hard part</div>
<div class="fixgrid">
<div><span class="fl">Nobody is called Rāshid</span><b>Not one of the sixty-three Christian household
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

ent('1820 · 1834 · 1844', 'oral', True, 'Feuds, a Pasha, and a faction',
 'The ʿAzzouz incident of 1820 scatters the whole town to eight villages for months; Ibrāhīm Pasha occupies Ramallah in 1834 <b>without resistance</b> — about 150 families, who feed his army’s oxen and get them back; and in the Qays–Yaman fighting of 1844, <b>Ramallah is the Qays headquarters</b>{}.'.format(c('Shāhīn (1982), ch. 3: the ʿAzzouz incident and the village-by-village dispersal; Ibrāhīm Pasha’s occupation; the 1844 war — the sixteen-man garrison at Beitunia, Suleiman El Samhan’s killing of Taha Abu Ghosh, Patriarch Keirollus’s intervention, and Abu Ghosh’s year of exile in Constantinople.')),
 FIX('“No source found in this research assigns Ramallah itself to Qays or to Yaman” (the family presentation).',
 '<b>Ramallah was the Qaysī headquarters in 1844.</b> Beitunia, next door, was the Yemeni one — and the Shakara declared themselves Yemen simply to protect their lands near Beitunia.',
 'Shāhīn (1982) devotes a chapter to the 1844 war and assigns the town explicitly. The deeper point survives him: the faction language was genealogical, but families chose sides for local reasons — descent language in this country has always described belonging as much as biology.')),

ent('1850', 'documents', True, 'The present Greek Orthodox church is built',
 'On the site of the first church of 1807, built by Fr Mitry Elias Kassees near the present bus station{}.'.format(c('Shāhīn (1982): the 1807 first church and its builder; the present church of 1850; the outstanding-dates list confirms both.')),
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
 'Everything this book knows about how Ramallah actually lived comes from <b>ʿAzīz Shāhīn, who lived it</b>. <b>Elihu Grant</b> — superintendent of the American Friends Schools at Ramallah and Jerusalem from 1901 to 1904 — happened to be counting the same houses at the time, which lets us <i>date</i> what Shāhīn remembered. <b>Shāhīn is the source; Grant is the clock.</b> Grant and in 1907 published <i>The Peasantry of Palestine</i> — two hundred and fifty-five pages on village life, with a chapter given over to <b>Ramallah and al-Bīra by name</b>{}.'.format(c('Elihu Grant, <i>The Peasantry of Palestine: The Life, Manners and Customs of the Village</i> (Boston: Pilgrim Press, 1907), 255 pp. with 39 leaves of plates — the c. 340-page figure belongs to the enlarged edition of 1921, <i>The People of Palestine</i>; the title page describes him as “Resident (1901–1904).” Chapter IX, from p. 187, is “Village life in the concrete. Description of actual villages, Ram Allah and el-Bireh”; chapter X covers eṭ-Ṭīreh, ʿAyn ʿArīk, Baytīn, Dayr Dīwān, eṭ-Ṭayyibeh, Jifnā, ʿAyn Sinya, Bīr Zayt, ʿAbūd and Mukhmās — nearly every village on this book’s district map. ' + D('peasantryofpales00gran.pdf') + '.')),
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
Christian villages of the central highlands — <b>Ramallah, Bayt Jālā, eṭ-Ṭayyibeh and Jifnā</b>, with
Christians outnumbering Muslims at Bīr Zayt, ʿAyn ʿArīk and ʿAbūd — the same band along the ridge
that the Ottoman register of 1596 describes three hundred years earlier, and that the Byzantine
churches describe a thousand years before that. <b>Different observer, different language, different
century, same map.</b></p>"""),

ent('1902 · 1908', 'documents', True, 'The state arrives; the clans become a constitution',
 'In 1902 Ramallah is made a district seat over thirty villages — <b>“Till 1902 there had been no government rule in the villages and small towns of Palestine”</b>{} — and in 1908 it is incorporated as a city under Elias ʿAudi, its first mayor, with <b>one council representative from each clan</b>. The ḥamūla structure of 1562 becomes, literally, the constitution.'.format(c('Shāhīn (1982): the district of 1902 under mudīr Ahmad Murad, and the incorporation of 1908 — Elias ʿAudi mayor, Assʿad Ibrahim Kassees secretary-treasurer; compare Zeʾevi, <i>An Ottoman Century</i> (1996).')),
 fig(F3.fig_town_plan(),'The town, as Shāhīn drew it',
  'Central Ramallah after the sketch map in his own book. The dashed ring is the original village — the eight clans’ quarters and their guest houses, all of it walking distance. Everything numbered outside it was built by the century this book has just described: the church of 1850, the Catholic mission of 1857, the Friends schools, the Meetinghouse of 1910, and the hospital the diaspora paid for in 1963. Note the two roads south: the old track from El Sharafa, where the town said goodbye to its emigrants, and the carriage road of 1901 through El Bireh that replaced it.',
  'After Shāhīn (1982), p. 69, simplified; institution dates from his own chapters.')),

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

ent('1948', 'documents', False, 'The catastrophe — and the town transformed',
 'On <b>11 July 1948</b> Israeli forces took Lydda; Ramle surrendered the next day. At half past one on <b>12 July Yitzhak Rabin signed the order to expel the inhabitants</b>, and on the morning of the 13th the people of Lydda were marched east on foot in the July heat — somewhere between fifty and seventy thousand people driven out of the two towns, and an unknown number dead on the road. The Arab Legion picked up the survivors and brought them to Ramallah. <b>Ramallah was not destroyed. Ramallah opened its doors and was tripled</b> — every madāfa, every schoolroom, every qaṣr in the fig groves. By a local count of 1953: some 13,500 souls, of whom about nine thousand are refugees and four and a half thousand are Ramallah natives — the figure that, with 2,580 in America, gives Shāhīn’s total of 7,080 Ramallah people in the world{} — <i>Jordan held no census that year; its censuses are 1952 and 1961</i>. And its own money went at the same time: the deposits in <b>Bank al-Umma</b> were frozen, not lost — part of the wholesale freezing of Palestinian bank accounts that year — the swine-raising venture collapsed with over <b>$400,000</b> in it, and some 200 Mandate salaries simply stopped{}. <i>“The future looked grim and the morale of the people was at its lowest ebb”</i> — Shāhīn saw it himself in 1951–52.'.format(
  c('Shāhīn (1982), “The Great Influx of 1948,” with the 1953 census figures.'),
  c('Shāhīn (1982): the swine venture, the Bank El Ummeh closure, and the 200 lost government jobs — “all of these misfortunes occurred within three or four years.”'))),

ent('1944–1963', 'documents', True, 'The diaspora builds the town a hospital',
 'The Ramallah Foundation, Inc. of New York is formed in 1944; a three-man delegation — Peter George Shihadeh, Yousef Abdallah Bateh, <b>and ʿAzīz Shāhīn himself</b> — tours every US Ramallah community in 1944–45 and collects over <b>$90,000</b>{}. The Summer Resorts Company (1945, capitalised at £P50,000 — there was no dinar in Palestine until 1950 — mostly diaspora stockholders) brings the water from ʿAin Fara in 1951; and on <b>20 May 1963 the Ramallah New Hospital opens</b> — fifty beds, on 26 dunams, its assets vested in the New York Foundation. <i>The money came back along the road the people left on.</i>'.format(c('Shāhīn (1982), “Societies”: the Foundation of 1944, the delegation and the $90,000; the Hospital Society of c. 1945 and the 26 dunams; the hospital’s completion in 1961–63, third floor 1966–68, out-patient clinic 1977.'))),

ent('1954 · 2023', 'documents', False, 'The town’s first history is written in New York — twice',
 '<b>Joseph Jiryes Cadora</b> — pharmacist, mayor of Ramallah 1943–52 — publishes <span class="ar">تاريخ مدينة رام الله</span> at al-Hudá Press, New York, 1954; Shāhīn takes his census apparatus from it, “pp. 136–37”{}. Seventy years later the author’s niece by marriage, Samira Rafidi Meghdessian, publishes it in English as <i>Remembering Ramallah</i> (2023), annotated, with a foreword by his son. <i>The book this project hunted for years as “Qadūra” was in the family’s hands the whole time — Cadora and Qadūra are the same name.</i>'.format(c('Kaddoura/Cadora, <i>The History of Ramallah</i> (New York: Huda Press, 1954), 159 pp.; <i>Remembering Ramallah: A Preservation of History</i>, trans. Meghdessian (2023), ISBN 979-8-3507-0767-0; Shāhīn (1982) cites the census figures to Kaddoura pp. 136–37.'))),

ent('1958 / 1959', 'oral', True, 'The Federation',
 'The American Federation of Ramallah, Palestine — the body this book is written for.',
 FIX('Founded 1952, federated in Detroit on 7 September 1959 (the family presentation).',
 '<b>Unresolved.</b> Shāhīn: incorporated in Detroit, 1958. Both dates stand until one is retired.',
 'Nothing in this book can decide it — and the thing that can is close: <b>the Federation’s own incorporation papers, or the Michigan corporate register, would settle it in an afternoon.</b> The easiest open question in this book to close.')),

ent('1961–2024', 'documents', False, 'The city, counted to the present',
 'Jordan’s census, 1961: <b>14,759</b>. Israel’s, after the occupation of 1967: <b>12,134</b> — <i>and that is not simply emigration.</i> The count was taken under curfew weeks after the war; it recorded only those standing in the town on the day, and <b>every Ramallah person who happened to be abroad lost the right to come home</b>. The dip is an act of the occupation, recorded as a statistic. Birzeit College begins four-year degrees in 1972 and becomes Birzeit University in 1975; <b>Ramallah did not become a capital by accident.</b> It became one because its people made it ungovernable from outside — Birzeit’s students from 1972 onward, the strike committees of the first intifada, the town the Muqāṭaʿa was built to hold down and could not. That compound ran through every hand in turn — Tegart fort, Jordanian HQ, Israeli headquarters, and after the redeployment of December 1995 the seat of the Palestinian Authority, with Arafat moving in in 1996. In 2002 the Israeli army came back into the city and besieged it, and the town lived under curfew for weeks. <i>The census numbers are what survived that.</i> PCBS: <b>17,851 (1997) · 27,460 (2007) · 38,998 (2017) · 43,880 projected (2024)</b>{}. And the diaspora curve crosses the town’s: 1,500 in the US by 1946, over 4,000 by 1960, over 10,000 by 1975 — <b>“over 85% of Ramallah people are now in the States”</b> — <i>a formula his own figures will not carry, and which can only be read as a claim about descendants of the pre-1948 town rather than about the town’s population</i>{}.'.format(
  c('The census series: Jordan 1961; Israel 1967; PCBS 1997, 2007, 2017 and the 2024 projections; Christians 32% of Ramallah in 1997.'),
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
al-Qasṭal, al-Zarqāʾ, Adhruḥ, al-Jarbāʾ, Maʿān{c('Al-Dabbāgh, <span class="ar">القبائل العربية</span>, 151–52. His only Palestinian instances are the place-names themselves — Dayr Ghassāna, and a suggestion that Jifnā in the Ramallah district may be named for <span class="ar">آل جفنة</span>, again hedged with <span class="ar">ولا يستبعد</span>, “it is not to be ruled out.” <i>The evidence for the settlement is the place-name; the evidence for the place-name is the settlement.</i> Every Arab authority that specifies where the Ghassanids actually were — al-Qalqashandī, al-Hamdānī, Ibn Faḍl Allāh al-ʿUmarī, Jawād ʿAlī, Kurd ʿAlī, and al-Dabbāgh himself — puts them east and north.')}. <i>The Palestinian record puts our claimed people
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
school, the Girls Training Home, in 1889, and took the name Friends Girls School in 1919. she taught four years, then married and left, and the school
she started is still open{c('Shāhīn (1982), the education chapter. She was not a native of Ramallah but lived there several years; she married Hanna Bayyuk of Jerusalem.')}. <b>Katie Gabriel</b>, Lebanese, ran the boarding school
from 1889 and gave the Friends forty years.</p>
<p><b>Dr Philip Assʿad Maʿlouf</b> came from Beirut in 1891, opened his own clinic in 1895, and for
years was <i>the only doctor in the entire Ramallah district</i>. The town called him <b>Hakeem Abu
Iskandar</b>. In 1906 he pulled a twelve-year-old boy through forty days of typhoid fever; the boy
was ʿAzīz Shāhīn, who lived to write this history. <b>Maʿlouf himself died in the typhus of
1916.</b> He used to say that a doctor got no credit in Ramallah: the people waited until a man was
nearly dead to call him, and then blamed him if the man died{c('Shāhīn (1982), “Medical Treatment.” His predecessor, Dr George Hassenauer of the Friends clinic (1883–89), was called <b>Dr Hassan Nawar</b> because the town could not pronounce his name.')}.</p>
<p><b>Boulos Shehadeh</b>, born in Ramallah in 1882, founded <i>Mirʾāt al-Sharq</i> in Jerusalem on
17 September 1919 — 1,770 surviving issues, digitised, with 1,535 mentions of his home town.
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
<p style="max-width:none"><b>The Ḥaddādīn claim is of the same evidentiary class as its peers</b>:
first fixed in writing in twentieth-century family history, describing a real and well-attested kind
of population, without a documentary chain back to the sixth century. What makes it <i>more
restrained than any of them</i> is precisely what looks like its weakness. <b>It does not fill the
gap.</b> John Mogannam’s chart prints generation 35 as a void where Maalouf printed a forgery.
<i>That single choice is the difference between the two documents, and it is entirely to this
family’s credit.</i></p></div></div>"""),

ent('II', 'attested', True, 'Our contribution to the Palestinian people',
 '<b>The family is one arrival among ten that became one people.</b> The genetics say the population of this land absorbed every newcomer for four thousand years; the family’s stream — Christian Arabs out of the Ghassanid south — was absorbed like the rest, and then did its own absorbing: eight outsider families folded into the clans from 1750, a Muslim neighbour taken into the clan structure in 1923 — in a town that had had Muslim households since 1538 — some nine thousand refugees taken in by a town the government had counted at 5,080 in 1945. <i>The tradition says we came from somewhere. The ground says we have been here the whole time. Both are true at once, and in this country they always have been.</i>'),

ent('III', 'documents', True, 'The founding of Ramallah',
 'On the documents: <b>named 1279 · uninhabited waqf land 1525–28 · four households 1538–39 · the group at Bayt Jālā 1553–54 · THE FOUNDING 1562 · the deed in court 1565 · the Ḥaddādīn named 1596</b>. On the tradition: Rāshid, the ford, the forge, the purchase from the Ghazāwneh, “about 1550.” <b>The document and the memory are twelve years apart, and the memory loses nothing by the correction.</b>',
 f"""
{NUMTABLE('THE KEY DATES — one page, for the book',
 ['Date', 'Event', 'Carried by'],
 [['8th–7th c. BCE', 'The Maʾrib dam is built, in the country scripture assigns the line', 'inscription + both family texts'],
  ['528–569', 'Al-Ḥārith ibn Jabala, phylarch — generation 34', 'Procopius, contemporary'],
  ['543–548', 'The dam breaks (Abraha’s repair, CIH 541); final collapse follows', 'inscription'],
  ['c. 890', 'Last named Ghassān population — Gharandal, Transjordan', 'al-Yaʿqūbī'],
  ['1186', 'Rām Allāh first named — pledged by a Crusader king against a debt', 'Ḥammūdeh (2014), p. 39'],
  ['1279', 'The hill endowed to the Ibrāhīmī sanctuary at Hebron', 'sijill 48, p. 88 (1565)'],
  ['c. 1500', 'Rāshid al-Ḥaddādīn — generation 66', 'both family texts'],
  ['<b>1562</b>', '<b>The founding: 27 families up from Bayt Jālā</b>', 'the waqf defter of 970/1562'],
  ['1596–97', 'The register names al-Ḥaddādīn — 80 households, 71 Christian', 'the defter'],
  ['1850 · 1852', 'The present church — portal datestone 1850, inauguration usually given as 1852', 'Shāhīn + the carved portal'],
  ['1901', 'The first four sail for America', 'Shāhīn, name by name'],
  ['1908', 'Ramallah a city — one councilman per clan', 'the town record'],
  ['1916', 'Typhus — Shāhīn puts the losses near a third; no independent record survives', 'Shāhīn, as family memory'],
  ['1948', 'The town triples with refugees', 'the local count of 1953'],
  ['20 May 1963', 'The hospital the diaspora paid for opens', 'the Foundation’s record'],
  ['7 Sept 1959', 'The Federation constituted at the first convention, Detroit', 'the AFRP’s own published history']],
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
  .ewhen{text-align:left;padding-left:26px}
  .eraband h2{font-size:1.5rem}
  .fixgrid{grid-template-columns:1fr}
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
     'The span is 931 years, from al-Ḥārith’s death in 569 to Rāshid about 1500. At the observed male-line interval of 25–35 years that is <b>27 to 37 generations</b>, most probably about 31 — which makes the whole line 66 generations, not 36. Forty-five would require a generation of 21 years, shorter than any observed population sustains',
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
<span class="r">The One Line &middot; fifth edition</span></div>
<hr class="mastrule">
<h1>The One Line</h1>
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
<p><b>The One Line</b> &middot; {FIGN[0]} figures &middot; {len(CITES)} notes &middot; one timeline,
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
        '<title>The One Line — The Ramallah Family</title>'
        '<style>' + CSS + '</style></head><body>' + ''.join(html_parts) + '</body></html>')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w', encoding='utf-8', newline='\n').write(html)
print('WROTE', OUT, f'{len(html):,} bytes ·', FIGN[0], 'figures ·', len(CITES), 'notes')
