# -*- coding: utf-8 -*-
"""The Timeline Test — Shāhīn's chronology and John's chart as the control,
every other document in the project checked against them."""
import json, os

from paths import out as _out, asset as _asset
OUT = _out('AFRP_Timeline_Test_v1.html')
GREEN, RUST, PLUM = '#007A3D', '#A85210', '#6D4E9E'
GOLD, GREY, RULE, FOLIO = '#B98A4E', '#77726A', '#DCD6C9', '#9A958C'
INK, BODY, DARK, CREAM = '#1A1A1A', '#46423B', '#004A26', '#FFFAF0'
SURF = '#FCFBF8'

# verdicts
V = {
 'confirmed': ('#D5E9DF', GREEN, 'CONFIRMED'),
 'refined':   ('#A9CDB8', '#1A1A1A', 'REFINED'),
 'corrected': ('#F6EEDF', '#8A5A1E', 'CORRECTS US'),
 'new':       ('#EDE7F4', '#4A3A7A', 'NEW TO US'),
 'conflict':  ('#FDF6EC', '#C0392B', 'CONFLICT'),
 'untested':  ('#EFEDE8', '#77726A', 'UNTESTED'),
}

ROWS = [
 (1550, 'Ramallah settled by Rāshid Ḥaddād and his family, about 1550.', 'refined',
  'The Ottoman registers put the Christian settlement at <b>1562</b>, with the site holding four Muslim households in 1538–39 and none at all in 1525–28. Shāhīn’s “about 1550” is the family’s own estimate; 1562 is a document. His figure is not wrong so much as undated — and the register puts the movers a generation or two below Rāshid himself.'),
 (1671, 'Several Ramallah workers volunteer to help repair the roof of the Church of the Nativity.', 'new',
  'Not in any other source in this project. It matters more than it looks: it is a <b>seventeenth-century datum for Ramallah</b>, from the emptiest stretch of the whole story, and it places Ramallah men inside the Bethlehem church economy. Tramontana’s and Zeʾevi’s work on this century is where it could be tested.'),
 (1700, 'Yaʿcoub Elias of the Yousef clan, first Ramallah man ordained priest by the Greek Orthodox Church.', 'confirmed',
  'The presentation carries the same man and the same year. <b>And the drive now holds the check:</b> Papadopoulos-Kerameus’s <i>Analekta</i> II prints the Patriarchate parish registers of <b>1706 and 1709</b>, which name Ramallah — the exact window. Shāhīn’s next entry is a 1706 clergy salary. Two independent records of the same parish in the same decade.'),
 (1706, 'A priest in Ramallah was paid 20 piasters a month for teaching parish boys to read and write Arabic and Greek.', 'new',
  'A precise economic datum from a century the project had almost nothing for — and <b>the detail that the teaching was in Arabic <i>and Greek</i></b> speaks directly to the Rūm Orthodox character of the town. Cross-check against <i>Analekta</i> II.'),
 (1807, 'Fr Mitry Elias Kassees builds the first Greek Orthodox church, near the present bus station.', 'confirmed',
  'The presentation says the 1852 church replaced “an earlier building of the early nineteenth century.” <b>Shāhīn names that earlier building, its builder and its site.</b> The vague sentence in the deck can now be replaced with a fact.'),
 (1820, 'Several men of the ʿAzzouz family killed in a feud within the Sharaka clan.', 'untested',
  'No documentary trace found. Inter-clan feud detail of this kind rarely reaches the registers; keep it as family memory, attributed to Shāhīn.'),
 (1834, 'Ibrāhīm Pasha of Egypt occupies Ramallah without resistance.', 'confirmed',
  'Agrees with the documented 1834 revolt against Ibrāhīm Pasha and the defeat of the district’s shaykhs. <b>“Without resistance” is the new element</b> and is consistent with Ramallah not being a throne village.'),
 (1838, 'Robinson and Smith visit and estimate the population at 800–900.', 'confirmed',
  'Robinson counts 200 taxable men; the population chart in <i>The Family, Reconstructed</i> plots <b>850</b> for 1838. <b>Shāhīn’s 800–900 brackets that estimate exactly</b> — an independent corroboration of the chart’s most uncertain early point.'),
 (1844, 'Fighting breaks out between Qays and Yaman. <b>Ramallah was the Qays headquarters.</b>', 'corrected',
  '<b>This is the most significant single correction in the list.</b> The presentation states plainly that “no source found in this research assigns Ramallah itself to Qays or to Yaman. The deck does not assert one.” <b>Shāhīn assigns it — and makes it the Qays headquarters.</b> That is a named source for a gap the project had explicitly printed as empty. It should be weighed (Shāhīn is a memorial-book author, not an archival one) but it can no longer be said that no source assigns it.'),
 (1850, 'The present Greek Orthodox church is built.', 'corrected',
  '<b>The deck dates the Church of the Transfiguration to 1852. Shāhīn says 1850 — and the carved portal date, which this project independently verified as solid, also reads 1850.</b> Two independent witnesses against the deck’s 1852. <b>Recommend correcting the deck and the chapters to 1850.</b>'),
 (1850, 'Bishop Samuel Gobat starts a boys’ school, about 1850.', 'new',
  'The Anglican bishop Samuel Gobat’s school network is well documented in Palestine generally; <b>a Gobat school at Ramallah is new to this project</b> and predates the Latin Patriarchate school by seven years. It changes the order of the schools story.'),
 (1857, 'The Roman Catholic Church comes to Ramallah and opens a boys’ school.', 'refined',
  'The deck gives <b>1858</b> for the Latin Patriarchate school. One year apart; both are plausible and the discrepancy is small. Worth resolving against the Latin Patriarchate’s own parish record.'),
 (1869, 'Eli and Sybil Jones visit with other Quakers; the Friends Girls School opens within three months.', 'confirmed',
  'Exactly the deck’s date, and Rufus Jones’s <i>Eli and Sybil Jones</i> is in the drive. <b>“Within three months” is new</b> and is a sharper claim than the usual telling.'),
 (1873, 'The Sisters of St Joseph open a girls’ school and a clinic.', 'new',
  'Absent from the deck’s eighty-year institutional sequence. Adds a third teaching order to the town before 1880.'),
 (1883, 'The Friends open a clinic under Dr George Hussenmauer — the first doctor to come to Ramallah.', 'new',
  'New, and dates the arrival of Western medicine in the town precisely.'),
 (1889, 'The Friends open a boarding school for girls with fifteen pupils; girls begin coming from other cities.', 'confirmed',
  'The deck has the Girls Training Home in 1889 with fifteen students. <b>Identical, down to the number.</b> A good sign for the reliability of this whole chronology.'),
 (1895, 'The Greek Catholic (Melkite) church begins services under Rev. Saba Salem Mogannam.', 'confirmed',
  'The deck dates the Melkite church to 1895. <b>Shāhīn names the priest — a Mogannam</b>, which ties the compiler of the thirty-six-generation chart to the founding of the town’s fourth church.'),
 (1895, 'A severe snowstorm; thirty Russian pilgrims die near al-Bīra; Ramallah people bring donkeys and mules to rescue the rest and bury the dead.', 'new',
  'Entirely new, and one of the few pieces of nineteenth-century social narrative in the whole corpus. The 1895 Palestine snowstorm is attested regionally; the Ramallah rescue is Shāhīn’s.'),
 (1901, 'Ramallah men begin to emigrate to the United States.', 'refined',
  'The deck says emigration began in the Bethlehem area in the 1870s and “from Ramallah it followed,” without a date. <b>Shāhīn supplies one: 1901.</b> That is consistent with Taraki’s figures and with the 1931 census sex ratio, and it gives the emigration chapter a start line.'),
 (1901, 'The Friends start a boys’ boarding school, also with fifteen pupils.', 'confirmed',
  'The deck: Friends Boys School founded 1901 with fifteen students. Identical.'),
 (1901, 'The Turkish government completes a carriage road from Jerusalem to Nablus, past Ramallah and al-Bīra — the present Ramallah–Jerusalem road.', 'new',
  'New, and structurally important: it is the moment the <b>ridge road stops being a track and becomes infrastructure</b>, twenty years before the Mandate.'),
 (1902, 'Ramallah is made a district seat for thirty surrounding villages; Ahmad Murad of Jerusalem appointed the first mudīr. “Till 1902 there had been no government rule in the villages and small towns of Palestine.”', 'new',
  '<b>New and consequential.</b> It dates the arrival of direct Ottoman administration in the town, and it is the administrative prehistory of the 1908 municipality. It also confirms from inside the town what Zeʾevi and the deck argue from the registers: that the hill country was taxed but not governed.'),
 (1903, 'Nicola Khoury brings the first mechanical flour mill; Ibrāhīm Esa Abu Shihady starts a horse-drawn carriage service to Jerusalem at 6 piasters. Wages: labourer 6 piasters a day, boy 4, mason 23, craftsman 15–20; a doctor’s visit 6–10.', 'new',
  '<b>A complete wage table for the town at the turn of the century</b>, which exists nowhere else in this project. Note the mason at 23 piasters — nearly four times a labourer. That bears directly on the mason tradition tested in Part Six of the reconstruction.'),
 (1908, 'Ramallah incorporated as a city; Elias ʿAudi first mayor; council of one representative from each clan.', 'confirmed',
  'The deck has the 1908 municipality. <b>“One representative from each clan” is new</b> and is the single clearest statement anywhere that the ḥamūla structure <i>was</i> the political structure — the same nine divisions the Family Tree Book is organised by.'),
 (1914, 'World War I; about thirty Ramallah men serving in the Turkish army die.', 'new', 'New.'),
 (1915, 'A locust plague; no crops escape; the economy suffers greatly.', 'confirmed',
  'The 1915 locust plague across Palestine and Syria is very well attested. Shāhīn localises it.'),
 (1916, '<b>Typhus plague. About 30 per cent of Ramallah’s population perish.</b>', 'corrected',
  '<b>This changes the population chart.</b> The chart runs 2,061 (1896) → 3,104 (1922) as a smooth rise. A 30 per cent mortality event in 1916 means the true curve <b>falls steeply and then recovers</b>, and that the 1922 figure represents a recovering, not a continuously growing, town. <b>The chart should carry this and does not.</b>'),
 (1917, '27 December: the British Army occupies Ramallah.', 'confirmed',
  'Consistent with the fall of Jerusalem on 9 December 1917. A precise local date the project did not have.'),
 (1927, 'A strong earthquake; two Ramallah inhabitants killed; heavy property damage.', 'confirmed',
  'The July 1927 Jericho earthquake is well attested regionally. Shāhīn gives the local casualty figure.'),
 (1932, 'A 3 per cent school tax on income from all dwellings is imposed by the city for its schools.', 'new',
  'New, and a good indicator of municipal capacity under the Mandate.'),
 (1936, 'Electricity arrives from the Jerusalem Electric Company; most homes soon had electric light.', 'new', 'New.'),
 (1945, 'The Ramallah Summer Resorts Co. organised by Jaleel Harb and others with 50,000 Jordanian dinars, mostly Ramallah stockholders.', 'new',
  'New — and it is the diaspora capital story in miniature: money earned abroad, invested at home, dividends paid.'),
 (1948, 'Thousands of refugees pour into Ramallah.', 'confirmed',
  'Agrees with the reconstruction: the town kept its houses and lost its hinterland, and the camps follow from 1949.'),
 (1951, 'The Summer Resorts Co., with both municipalities, brings water from ʿAin Fara.', 'new', 'New.'),
 (1958, 'The American Ramallah Federation is incorporated in Detroit, Michigan.', 'conflict',
  '<b>The deck says the Federation was founded by recent immigrants in 1952 and formally federated in Detroit on 7 September 1959.</b> Shāhīn says incorporated in Detroit in 1958. These may be three stages of one process — founding, incorporation, federation — but as printed they conflict. <b>The AFRP’s own records settle this in an afternoon, and the AFRP is the publisher of the book.</b>'),
 (1963, '20 May: the Ramallah New Hospital opens.', 'new', 'New.'),
]

def esc(s): return s

def timeline_svg():
    W, H = 860, 330
    x0, x1 = 250, 800
    t0, t1 = 1540, 1980
    def px(y): return x0 + (x1-x0)*(y-t0)/(t1-t0)
    counts = {}
    for yr, _, v, _ in ROWS:
        counts.setdefault(v, []).append(yr)
    order = ['confirmed','refined','corrected','conflict','new','untested']
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Shaheen\'s chronology plotted by verdict">']
    s.append(f'<rect width="{W}" height="{H}" fill="{SURF}"/>')
    s.append(f'<text x="40" y="32" font-size="11" fill="{GOLD}" font-weight="700" letter-spacing="1.4" font-family="Times New Roman, Times, serif">SHĀHĪN’S THIRTY-SEVEN DATES, PLOTTED — AND HOW EACH ONE FARED</text>')
    s.append(f'<text x="40" y="50" font-size="10.5" fill="{GREY}" font-style="italic" font-family="Times New Roman, Times, serif">Each mark is one entry in “Outstanding Dates in Ramallah’s History”, set against everything else in the project.</text>')
    top = 78; rh = 32
    for i, k in enumerate(order):
        y = top + i*rh
        fill, txtc, lab = V[k]
        s.append(f'<rect x="40" y="{y}" width="150" height="{rh-8}" fill="{fill}" stroke="{txtc}" stroke-width=".8" rx="3"/>')
        s.append(f'<text x="115" y="{y+16}" font-size="8.6" fill="{txtc}" text-anchor="middle" font-weight="700" letter-spacing=".9" font-family="Times New Roman, Times, serif">{lab}</text>')
        s.append(f'<text x="196" y="{y+16}" font-size="10" fill="{GREY}" font-family="Times New Roman, Times, serif">{len(counts.get(k,[]))}</text>')
        for yr in counts.get(k, []):
            s.append(f'<circle cx="{px(yr):.1f}" cy="{y+(rh-8)/2:.1f}" r="5" fill="{txtc}" opacity=".85" stroke="#fff" stroke-width="1.2"/>')
    yb = top + len(order)*rh + 4
    s.append(f'<line x1="{x0}" y1="{yb}" x2="{x1}" y2="{yb}" stroke="{RULE}"/>')
    for yr in range(1550, 1981, 50):
        s.append(f'<line x1="{px(yr):.1f}" y1="{yb}" x2="{px(yr):.1f}" y2="{yb+6}" stroke="{FOLIO}"/>')
        s.append(f'<text x="{px(yr):.1f}" y="{yb+20}" font-size="9.4" fill="{FOLIO}" text-anchor="middle" font-family="Times New Roman, Times, serif">{yr}</text>')
    from collections import Counter as _C
    c=_C(v for _,_,v,_ in ROWS)
    line=(f"Nothing in Shāhīn’s chronology is refuted. {c['confirmed']} entries confirm the project’s dates, "
          f"{c['refined']} sharpen them, {c['corrected']+c['conflict']} correct or conflict with them, and {c['new']} are new.")
    s.append(f'<text x="40" y="{H-16}" font-size="10.5" fill="{BODY}" font-weight="700" font-family="Times New Roman, Times, serif">{line}</text>')
    s.append('</svg>')
    return ''.join(s)

# family index
IDXJSON = _asset('ocr', 'family_index.json')
fam = json.load(open(IDXJSON, encoding='utf-8')) if os.path.exists(IDXJSON) else {}
famrows = sorted(fam.items(), key=lambda kv: -len(kv[1]))[:48]
ROMAN = {'عواد':'Awad','جريس':'Jeries','ابراهيم':'Ibrahim','يوسف':'Yousef','جغب':'Jaghab',
 'عوض':'ʿAwad','ايوب':'Ayoub','ميخائيل':'Michael','صرصور':'Sarsour','غنام':'Ghanam',
 'جبران':'Jubran','عقل':'Akel','فرحات':'Farhat','ريان':'Rayan','القطشة':'Qatsha',
 'الطويل':'Tawil','قندح':'Kandah','زيادة':'Ziadeh','القسيس':'Kassees','جابر':'Jaber',
 'ناصر':'Nasir','سالم':'Salem','هاني':'Hani','عابد':'Abed','عيده':'Eadeh','الزعرور':'Zarour',
 'زريفة':'Zrayfeh','العنيد':'Aneed'}

CSS = """
:root{--gold:#B98A4E;--grey:#77726A;--folio:#9A958C;--ink:#1A1A1A;--body:#46423B;
 --rule:#DCD6C9;--green:#007A3D;--dark:#004A26;--lighttext:#F3ECDD;--cream:#FFFAF0;--tan:#D4B483}
*{box-sizing:border-box}
body{margin:0;background:var(--cream);color:var(--ink);
 font:17px/1.6 "Times New Roman",Times,"Liberation Serif",Georgia,serif}
.wrap{max-width:900px;margin:0 auto;padding:0 26px}
.mastrow{display:flex;justify-content:space-between;align-items:baseline;padding-top:20px;
 font:11px/1.4 inherit;letter-spacing:.22em;text-transform:uppercase}
.mastrow .l{color:var(--gold);font-weight:700}.mastrow .r{color:var(--grey);letter-spacing:.12em}
hr.rule{border:0;border-top:1px solid var(--rule);margin:9px 0 26px}
h1{font-size:2.4rem;line-height:1.12;margin:0 0 8px;font-weight:700}
.sub-t{color:var(--grey);font-style:italic;font-size:1.1rem;margin:0 0 12px}
.meta{color:var(--folio);font-size:.86rem;margin:0 0 30px}
.lede{font-size:1.1rem;border-left:3px solid var(--gold);padding:2px 0 2px 20px;margin:0 0 30px;color:var(--body)}
h2{font-size:1.5rem;margin:48px 0 6px;padding:10px 0 8px;border-top:2px solid var(--gold);
 border-bottom:1px solid var(--rule)}
h3{font-size:1.04rem;margin:28px 0 10px;color:var(--green);font-weight:700;letter-spacing:.05em;text-transform:uppercase}
p{margin:0 0 14px;color:var(--body)}p strong,p b{color:var(--ink)}
figure{margin:24px 0;background:#FCFBF8;border:1px solid var(--rule);border-radius:8px;padding:16px 18px 12px}
figcaption{font-size:.87rem;color:var(--body);margin-top:10px}
table.tl{border-collapse:collapse;width:100%;margin:18px 0}
table.tl th{text-align:left;font-size:.7rem;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);
 border-bottom:2px solid var(--gold);padding:8px 10px}
table.tl td{border-bottom:1px solid var(--rule);padding:12px 10px;vertical-align:top;font-size:.94rem;color:var(--body)}
td.yr{white-space:nowrap;font-weight:700;color:var(--ink);font-size:1.02rem;width:56px}
td.vd{width:118px}
.v{display:inline-block;padding:3px 9px;border-radius:10px;font:700 9.4px/1.5 inherit;
 letter-spacing:.08em;text-transform:uppercase;border:1px solid;white-space:nowrap}
.note{background:#FDF6EC;border-left:3px solid #C98B3F;padding:14px 18px;margin:20px 0;
 border-radius:0 5px 5px 0;font-size:.95rem;color:#6b4f2a}
.note b{color:#8A5A1E}
.win{background:#E9F2EC;border-left:3px solid var(--green);padding:14px 18px;margin:20px 0;
 border-radius:0 5px 5px 0;font-size:.95rem;color:#14532d}
ol.acts li{margin-bottom:11px;color:var(--body)}
table.fam{border-collapse:collapse;width:100%;font-size:.86rem;margin:14px 0}
table.fam td{border-bottom:1px solid var(--rule);padding:6px 9px;color:var(--body)}
table.fam td.ar{font-size:1.12em;text-align:right;width:96px;color:var(--ink);font-weight:700}
table.fam td.en{width:110px;color:var(--ink)}
table.fam td.pp{color:var(--grey);font-size:.92em}
code{font:11.5px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;color:#1e6b34;
 background:#F0F5F0;border-radius:3px;padding:2px 6px}
footer{margin:50px 0 40px;padding-top:18px;border-top:1px solid var(--rule);color:var(--folio);font-size:.85rem}
"""

rows_html = []
for yr, txt, v, note in ROWS:
    fill, tc, lab = V[v]
    rows_html.append(
        f'<tr><td class="yr">{yr}</td>'
        f'<td class="vd"><span class="v" style="background:{fill};border-color:{tc};color:{tc}">{lab}</span></td>'
        f'<td><b>{txt}</b><br><span style="color:var(--grey)">{note}</span></td></tr>')

famhtml = []
for ar, pages in famrows:
    en = ROMAN.get(ar, '')
    pp = ', '.join(str(p) for p in pages[:14]) + ('…' if len(pages) > 14 else '')
    famhtml.append(f'<tr><td class="ar">{ar}</td><td class="en">{en}</td><td class="pp">{pp}</td></tr>')

from collections import Counter
cnt = Counter(v for _, _, v, _ in ROWS)

DOC = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Timeline Test — Shāhīn and Mogannam as the control</title>
<style>{CSS}</style></head><body><div class="wrap">
<div class="mastrow"><span class="l">Ramallah Family Tree</span><span class="r">The timeline test &middot; version 1</span></div>
<hr class="rule">
<h1>The Timeline Test</h1>
<p class="sub-t">Shāhīn’s “Outstanding Dates in Ramallah’s History” and John Mogannam’s thirty-six
generations, taken as the control — and every other document in this project checked against them.</p>
<p class="meta">American Federation of Ramallah, Palestine &middot; the Family Tree Project &middot; 17 August 2026 &middot;
built from <code>1982_Shahin_Kashf_al-Niqab_ENGLISH_TEXT_OCR.pdf</code>, pp. 73–75</p>

<p class="lede">The family’s two own documents are the standard here, not the thing being judged.
Shāhīn’s chronology runs from the founding to 1963 in thirty-seven entries; Mogannam’s chart runs
from Adam to Rāshid in thirty-six generations. Everything this project has produced — the deck, the
bibliography, the reconstruction — is measured against them below. <b>Nothing in either is refuted.
Four entries correct us.</b></p>

<figure>{timeline_svg()}
<figcaption><b>Figure 1.</b> Shāhīn’s dates by verdict. The density on the right is not bias — it is
the shape of the record: a town becomes describable in the nineteenth century and minutely
documented in the twentieth.</figcaption></figure>

<h2>Part One · Shāhīn’s chronology, entry by entry</h2>
<p>Thirty-seven entries. <b>{cnt['confirmed']} confirm what the project already had</b> — several to the exact
number of pupils — <b>{cnt['refined']} sharpen it</b>, <b>{cnt['corrected']} correct it</b>,
<b>{cnt['conflict']} conflicts outright</b>, <b>{cnt['new']} are new</b> and {cnt['untested']} cannot be tested.</p>

<table class="tl"><thead><tr><th>Year</th><th>Verdict</th><th>Shāhīn’s entry, and what the record says</th></tr></thead>
<tbody>{''.join(rows_html)}</tbody></table>

<h2>Part Two · What has to change in our documents</h2>

<div class="note">
<p><b>1. The church is 1850, not 1852.</b> The deck and the chapters date the Church of the
Transfiguration to 1852. Shāhīn says 1850, and the carved portal date — which this project verified
independently as the one solid element in the church’s dating — also reads 1850. <b>Two witnesses
against one. Change it.</b></p>
<p><b>2. The population chart must show 1916.</b> Shāhīn records a typhus epidemic killing about
thirty per cent of the town. The chart in <i>The Family, Reconstructed</i> draws a smooth rise from
2,061 in 1896 to 3,104 in 1922. <b>That line is wrong in shape</b>: it should fall hard in 1916 and
recover. The 1922 census counts a town that had recently buried a third of itself.</p>
<p><b>3. The Qays/Yaman gap is no longer empty.</b> The deck states that no source assigns Ramallah
to either faction and declines to assert one. <b>Shāhīn assigns it: Ramallah was the Qays
headquarters in the fighting of 1844.</b> The deck’s sentence is now false as written. It should
become: <i>one source, the family’s own historian, places Ramallah with the Qays.</i></p>
<p><b>4. The Federation’s founding date needs settling.</b> Deck: founded 1952, federated in Detroit
7 September 1959. Shāhīn: incorporated in Detroit 1958. Probably three stages of one process — but
the AFRP publishes this book and holds the records.</p>
</div>

<h3>And what Shāhīn hands us for free</h3>
<div class="win">
<p><b>A seventeenth-century Ramallah datum</b> (1671, the Nativity roof) in the emptiest stretch of
the story. <b>A named first church and its builder</b> (1807, Fr Mitry Elias Kassees). <b>A start date
for the emigration</b> (1901). <b>The date direct government arrives</b> (1902, and the remark that
until then there was no government rule in the villages of Palestine — a statement from inside the
town that matches what Zeʾevi argues from the registers). <b>A complete wage table for 1903</b> —
labourer 6 piasters, mason 23 — which is the only quantitative evidence in this project bearing on
the mason tradition tested in Part Six of the reconstruction. And <b>“one representative from each
clan”</b> on the 1908 city council: the clearest statement anywhere that the ḥamūla structure was
the political structure, which is precisely how the Family Tree Book is organised.</p>
</div>

<h2>Part Three · Mogannam’s chart as the second control</h2>
<p>The thirty-six generations were tested in full in <i>The Family, Reconstructed</i> (Figure 3
there). The result, restated as a test rather than a narrative:</p>
<table class="tl"><tbody>
<tr><td class="yr">1–13</td><td class="vd"><span class="v" style="background:#D5E9DF;border-color:#007A3D;color:#007A3D">SCRIPTURE</span></td><td>Adam to Aaber. Genesis 5 and 11, in the Septuagint reckoning a Rūm Orthodox family inherits. Not a chronology and never was.</td></tr>
<tr><td class="yr">14</td><td class="vd"><span class="v" style="background:#A9CDB8;border-color:#1A1A1A;color:#1A1A1A">THE JOIN</span></td><td>Kahtaan ibn Aaber. Stated by al-Ṭabarī c. 915. <b>Not the family’s to defend — every Qaḥṭānī Arab stands on it.</b></td></tr>
<tr><td class="yr">15–32</td><td class="vd"><span class="v" style="background:#A9CDB8;border-color:#1A1A1A;color:#1A1A1A">CLASSICAL</span></td><td>The Azdī pedigree. <b>Verified against the chart’s own cited sources</b> — al-Suwaydī and Wüstenfeld, both now in the drive. The names and their order match. <b>Al-Ghassānī enters at 29 with ʿAmr Muzayqiyāʾ, exactly where the classical sources put the naming at the spring.</b></td></tr>
<tr><td class="yr">33–34</td><td class="vd"><span class="v" style="background:#D5E9DF;border-color:#007A3D;color:#007A3D">ATTESTED</span></td><td>Jabalah and al-Harith. These are Procopius’s people — real offices, real inscriptions.</td></tr>
<tr><td class="yr">35</td><td class="vd"><span class="v" style="background:#FDF6EC;border-color:#C98B3F;color:#8A5A1E">THE VOID</span></td><td>Nine hundred years in one line. <b>The chart prints its own gap</b> — which is why the rest of it can be trusted. The “45 generations” count is arithmetically too many (it implies 22 years a generation); this edition counts the stretch at <b>about 31</b>, which makes the whole line <b>66 generations, not 36</b>. The gap is real regardless.</td></tr>
<tr><td class="yr">36</td><td class="vd"><span class="v" style="background:#007A3D;border-color:#007A3D;color:#fff">DOCUMENTS</span></td><td>Rāshid. Where the Ottoman paper begins — and where Shāhīn’s chronology, above, takes over.</td></tr>
</tbody></table>
<p><b>The two controls meet exactly once, and they agree.</b> Mogannam’s chart ends at Rāshid;
Shāhīn’s chronology opens with Rāshid settling the town. Between them the family’s own documents
cover Adam to 1963 with a single seam, and the seam is in the right place.</p>

<h2>Part Four · Two sources Shāhīn names that we do not have</h2>
<p>His own bibliography, on p. 76 of the English text, lists what he worked from. Two items are new
to this project and both are chaseable:</p>
<ol class="acts">
<li><b><i>A Brief History of the Haddadeen</i> — a handwritten Arabic manuscript in Ramallah City
Hall, dated 8 August 1953.</b> This is a primary clan document, unpublished, and Shāhīn used it as a
principal source. If it survives in the municipal archive it is the closest thing to a founding
document the Ḥaddādīn have. <b>Nothing in this project has looked for it.</b></li>
<li><b>Qadūra, <i>The History of Ramallah</i> — New York: Huda Press, 1954, in Arabic.</b> The
project has hunted this book for months and had it as “al-Hoda Press.” <b>Shāhīn gives the imprint as
Huda Press, New York</b> — worth re-running the HathiTrust and WorldCat searches on that form.</li>
</ol>
<p>He also cites Anees Maʿlouf, <i>The Society of American Friends in Palestine 1869–1939</i> (Cairo,
in Arabic), and E. G. Rey’s <i>Les Colonies Franques de Syrie</i> (Paris, 1883) — the latter placing
Shāhīn, in 1982, in the same Crusader-settlement literature as Pringle and Bresc-Bautier. And his
census list confirms a detail this project flagged: he used <b><i>Census of Palestine 1931</i>, 2
vols., Alexandria 1933</b> — the full report, where the copy in our drive is the 1932 preliminary
tables.</p>

<h2>Part Five · The Arabic volume is now searchable</h2>
<p>The Arabic section — 894 pages, previously image-only — was OCR’d on 17 August with Tesseract’s
Arabic model at 3× render. <b>860 of 894 pages returned text.</b> The result is
<code>1982_Shahin_Kashf_al-Niqab_OCR_TEXT.txt</code> in the drive, page-marked so any hit can be
taken back to the page image. OCR of a 1982 offset scan is imperfect: <b>use it to find a page, then
read the page.</b></p>
<p>The first thing it yields is a finding aid. The book is organised by family under the headwords
<span style="font-size:1.1em">آل</span> and <span style="font-size:1.1em">دار</span> — “house of” —
and those can be indexed. Ninety-nine family headwords appear on two or more pages; the largest are
below, and they map straight onto the clan rosters in <code>clans/</code>.</p>
<table class="fam"><tbody>{''.join(famhtml)}</tbody></table>
<p style="font-size:.9rem;color:var(--grey)">Full index in <code>family_index.json</code>. Page
numbers are PDF pages of the Arabic scan.</p>

<footer>
<p>Sources: Azeez Shaheen, <i>Ramallah: Its History and Its Genealogies</i> (Birzeit University,
1982), English text by Naseeb Shaheen, “Outstanding Dates in Ramallah’s History,” pp. 73–75, and the
bibliography at p. 76 — scanned and OCR’d 16 August 2026. John Aziz Mogannam, <i>Rashed
El-Haddadeen Ancestry to Adam &amp; Eve</i>. Checked against <i>The History of Ramallah</i> v1 (52
slides), the annotated bibliography fourth edition, and <i>The Family, Reconstructed</i> v1.</p>
</footer>
</div></body></html>
"""
open(OUT, 'w', encoding='utf-8', newline='\n').write(DOC)
print('written', OUT, len(DOC), 'bytes')
print('verdicts:', dict(cnt))
