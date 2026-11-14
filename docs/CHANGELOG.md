# Changelog


## v83 — 14 November 2026: Ramallah from 1914 to today, in the chapters we have

David: "Let's make the more recent history more enriched … the wars … the intifadas, the occupation … up to today … the way you would see it recorded in a Palestinian history museum." He chose option A, "Enrich chapters".

All the new text is in `src/modern.py`. `build_v5.py` changes in two lines.

- **Chapter 10:** adds *Snow, then the earth shakes* (1920, 1927) and *The Second World War* (the Trans-Jordan Frontier Force certificate of Elias Nasrallah Oudeh). There is also a letter from the front of December 1916.
- **Chapter 11:** adds *The town guards itself* (November 1947 – May 1948, from Cadora's chronicle as acting mayor) and *Under the Jordanian crown* (1949–1966). Two more refugee photographs of 1949–50 are added.
- **Chapter 12:** adds *Occupation, and the mayor in Houston* (1967–1982), *The first intifada, and the Authority* (1987–2000), *The second intifada and the siege* (2000–2005) and *The Wall, a capital, and our own people* (2002–2025).
- **Each new entry is built like a museum room:** a short story, then *The record* (a compact panel of dates and documents), at most one testimony for each era, and one or two photographs.
- **Photographs:** 11 Shaheen plates AFRP holds, and three Library of Congress photographs (no known restrictions). The three are the opening of the Palestine Broadcasting Service at Ramallah in 1936, the 1927 earthquake at Nablus, and a Ramallah woman in colour, 1935–46. The other eleven downloaded LoC items and the permission-needed items are listed in `docs/MODERN_IMAGES.md`.
- **Sources:** Palestinian and Arab sources first: Cadora, Shāhīn, Shaheen, al-Farḥān, the municipality, Birzeit University, Taraki, the Institute for Palestine Studies, ARIJ, al-Haq and the PLO Negotiations Affairs Department. United Nations and press reports are cited for dates and counts.

## v82 — 14 November 2026: every figure and map readable on a phone; the old pages in the family edition

No dates or findings change.

**Figures** (`src/build_figs7.py`, put in place by `src/phone_figs.py` after `figure_tidy`): the 23 older 860-unit charts, diagrams, timelines and tables are redrawn in the v80 style, 400 units wide, with nothing under 14 units (11.5 px on a 390 px phone; before, 3 to 6 px). Nothing is retyped: the text is read from the drawings v81 printed, frozen in `data/fig_v81/` by `tools/freeze_v81_figs.py`, and `tools/check_redraw.py` checks that every word of each old drawing is in its redraw. Wide rows become stacked cards, horizontal time axes become vertical, and the drawn pictures (terraces, the dam, the wheel) keep their artwork with numbered keys. `restore_svg` and `post_restore_fixes` still run underneath, unchanged.

**Maps** (`src/phone_maps.py`): each of the 11 maps gets a phone plate beside the full one. Each panel is cut out at phone width with all its artwork; every name is set again at 14 to 15 units with a halo, at its own place; a name that cannot be set without covering another gets a lettered badge at its place and is spelled out under the panel; names on leader lines become lettered badges; the legend is set as rows with their own symbols. Under 760 px the phone plate shows; on wider screens and in print the full plate shows, and tapping a map opens the full plate. `check_redraw.py` checks every word of each full plate is on its phone plate (graticule figures are set where they fit).

**Old pages:**
- Family edition: the twelve source-page scans (the 1186 charter, Shāhīn's founding page, the 1562 endowment register, the 1553–54 Bayt Jālā census, Seetzen, Robinson, Guérin, the 1896 loan agreement, the 1919 *Mirʾāt al-Sharq*, the 1946 notice, the committee's result and the ballot) are back: beside their story where the full book prints them in the story, in the chapter's photo essay where it prints them in the evidence, each with the first sentence of its caption and its source line.
- Main book: every chapter that has old-page scans shows them once (chapters 6 to 10). The repository holds no old-page scan that is not printed except the second copy of the 1186 charter, left out in v80 as a duplicate.

## v81 — 14 November 2026: the family edition, quieter figures, three findings

**Three findings** (approved by David, "All of them"; from the text-mining report of 14 November):
- **The water called Ghassān.** The Yemeni geographer al-Hamdānī (d. 945), *Ṣifat Jazīrat al-ʿArab* (ed. al-Akwaʿ, PDF p. 141), puts "the place of the water that used to be called Ghassān" at the lower end of Wādī Rimaʿ, and his editor says it is still known there. With Ibn al-Kalbī, two independent Arab authorities place the water in the Tihāma of Yemen. Chapter 4 says so in the story and the evidence, and its "What we still don't know" no longer lists the place as unknown.
- **1967.** Ramallah was 59.4 Christians in every hundred of known religion (Israeli census of 1967, introduction p. XII), in place of 57 per cent; the count was taken on 21 September 1967, under curfew. Marked as an Israeli state source, cited for its count.
- **1946.** The notice to Ramallah's voters of 28 March 1946 is signed by ʿĀrif al-ʿĀrif, the historian of Jerusalem, then acting Assistant District Commissioner (ISA P-213/40, PDF p. 81).

**Family edition** (`tools/build_family.py`): `out/Roots_of_Ramallah_Family_6x9.pdf`, 6 × 9 inches. The story half of every chapter, word for word, with no evidence halves, tables, note numbers, evidence labels or correction boxes. It adds a timeline of the whole story, a timeline at the head of each chapter, a photo essay after each chapter (every photograph the full book prints for that era, two to a row), and three family panels: the Saah (sentences of the full book, checked word for word by the build), the five sons, and the emigrants. Chapters start on the next page, with no blank versos.

**Figures:**
- The 23 older charts, diagrams, timelines and tables (`src/figure_tidy.py`, run by `restyle.py`): lines in full capitals are set in small capitals; a heading inside a drawing that repeats the figure's title is dropped; text is enlarged by the largest factor at which nothing collides (5 to 35 per cent on 17 of them), measured by `tools/fit_figure_text.py` into `data/figure_text_scale.json`. Maps are left to the map style.
- Five figures whose drawings print their sources in full no longer repeat them in the caption (6 sovereigns, the scattering, the road the family walked, the Karak wheel, Shāhīn's town plan).
- The 1919 *Mirʾāt al-Sharq* plate now comes before the 1946 election plates (it opens the 1938 entry), so chapter 10's plates run in date order.
- Print: tall phone-first charts are capped so a chart and its caption share one page.

## v80 — 13 November 2026: pictures beside their stories, charts a phone can read

No dates or findings change. The pictures and charts do.

- **Shaheen plates.** 27 new portraits and scenes from the Shaheen collection (`img/shaheen/CATALOGUE.csv`), each placed in the entry it belongs to, with a short caption and its rights line. About 30 plates that sat at chapter heads now sit beside their entries, spread through the text; every placement is checked against the entry's era. The duplicate 1186 charter plate is gone.
- **One numbering.** Every figure, map and plate is numbered by chapter ("Figure 7.3 · Portrait"), front matter as 0.n; the kind (Portrait, Scene, Document, Map, Chart, Diagram) shows on each.
- **New phone-first charts** (`src/build_figs6.py`, 400 units wide, no text under 14 units): the churches and schools, 1776–1925; the households, 1525–1596, with the neighbours in 1596; Karak's Christians counted and named; the Ḥaddādīn and the Ḥalasa; the emigration, 1901–1975; the population, 1838–2021; five sons and eight clans; what the land gave; the camps and their people. The nine-link ladder is redrawn for every chapter.
- **Removed:** "The peoples of this land … overlap", "The whole story on one scale" and "Ramallah among its neighbours, 1596" (now inside the households chart).
- **Maps:** Adhruḥ spelled as the sources spell it; the Dead Sea note added to four maps; the Fig 19 crossing labelled "across the Jordan"; al-Lisān placed on the Karak map.
- **Figure wording:** the figures state what the record shows, with no correction language; Figure 7.6 follows the text (1538–39; early 1600s).
- Print and phone builds both regenerate; the print rules size the ladders to the page.

## v79 — 13 November 2026: two editions from one source, set as a book

No words or facts in the book change. Only the layout does.

**Phone reader** (`src/reader.py`, run at the end of `src/restyle.py`):
- EB Garamond throughout (`assets/fonts/eb-garamond/`, SIL Open Font License), a calmer page with more white, and no coloured badges, rounded cards or heavy bands on phones: labels are small capitals in ochre, panels are set off by a hairline rule.
- Each chapter opens with a different picture from its own era, a large numeral, the dates on their own line and an epigraph from a source quoted in that chapter. Matson stereographs show their left frame. A drop cap starts each story.
- On screens up to 700 px, each chapter's evidence half is folded under "Show the evidence"; links into it open the fold. "What we still don't know" stays open.
- A "Next chapter" link closes each chapter. Figures fit the screen and open full size on a tap; pinch-zoom still works.
- The 15 Library of Congress photographs are now read from `img/loc/` (branch `loc-images`), so they show offline too.

**Printed book** (`tools/build_print.py`, Paged.js 0.4.3 vendored in `tools/vendor/` under its MIT licence):
- `out/Roots_of_Ramallah_6x9.pdf`: 377 pages, 6 × 9 inches. EB Garamond embedded, 10.8 pt on 1.42, justified and hyphenated. A title page and verso, a contents page with page numbers, running heads (book title on the left, chapter on the right) and folios.
- Every chapter opens on a right-hand page of its own: its picture (full bleed for the scans held in `img/`; two-thirds of the page with white around it for the 1024 px Library of Congress scans), the numeral, title, dates, summary and epigraph.
- Dates and evidence labels sit in the outer margin as small ochre notes. Drop caps start each story. The evidence half is a quiet indented section; "What the scholars say" and "What we still don't know" are side panels set off by a hairline. Quotations are set large in italic. Figures and photographs run the full text width with their number, title and caption below; terrain maps are rendered once at print resolution to keep the file small.
- The main book ends with John Mogannam's chart, a short Further reading (fifteen titles taken word for word from the bibliography) and the References. The annotated bibliography and the test harness are printed in `out/Roots_of_Ramallah_Companion_6x9.pdf` (411 pages).
- Every photograph is embedded; one not held in `img/` is left out of print rather than printed as an empty frame. Neither PDF is committed (see `.gitignore`); run `python3 tools/build_print.py`, with `PRINT_CHROMIUM` set to a Chrome binary if Playwright's own is not installed.
- The phone/desktop book grows by 20 KB (3,120,811 to 3,141,123 bytes).

## v78 — 13 November 2026: the book stops talking about its own past editions

David: "Smooth everything." About forty passages in the text, notes and figures that described this book's own earlier mistakes ("earlier editions of this book…", "an earlier draft…", "is withdrawn", "corrected here for the first time", "our earlier versions") now simply state what is true, with every citation kept. Disagreements between named sources are still printed both ways. The six kept correction boxes are unchanged. The preface now says a box marks a long-held family belief the record overturns. The stale Jifnā "six kilometres" fix in `post_restore_fixes.py` is removed.

## v77 — 13 November 2026

### Correction boxes retired (David chose "Keep a few")

The text around every correction box already read the corrected way, so the boxes were only a record of past edits sitting inside the story. Thirty-six were found: thirty-three `FIX()` boxes (seven through the `V69` table) and three hand-written ones. Six are kept, each where a belief the family long held was overturned: leaving Yemen "about 300 AD"; the 1186 charter "pledging Ramallah" (with the 1198 "Ramalei" forgery); Ramallah "founded in 1562" or "about 1550" (two boxes merged into one); Ṣabra as Rāshid's son; the church "built 1852"; the Federation "founded 1952". `FIX()` now returns nothing and `KFIX()` draws the kept boxes. This changelog is the record of what changed.

Removed, with what each had corrected (the text and notes already carry the corrected reading and its sources):
- Jericho credited to its Palestinian–Italian excavators (Taha and Nigro), not only to European and Israeli ones.
- The Maʾrib dam: 620–680 m, sixth century BC, about a thousand years; 1750–1700 BC withdrawn.
- Jabala is historical; the conversion story is the legend.
- The dam's later date does not rescue the dam-to-Syria chain.
- "Whether the Ghassanids were sovereign" is not the question that matters.
- A range of about 27–37 generations, not a fixed count.
- People lived on the hill before the families did (Mamluk village; Muslim households 1538–39).
- Thietmar was hosted at Shawbak by a Frankish widow, not by a bishop at Karak.
- One man of a queried "Jifnā al-Jawz" in 1374, not "men of Jifnā".
- Ghassān named as a living people to about 1300–1400, not only to 890.
- The Chabot "Ghassanide" footnote anecdote withdrawn.
- Shahîd's volumes read; his case does not rest on late Arabic writers alone.
- In the registers from 1553–54, not "from the start".
- al-Ḥudayda existed by 1455 but mattered little before the nineteenth century. Kept as a prose paragraph with its note.
- The settlement begins with the court oath of 1561, not the census of 1562. The note moved into the text.
- Karak's 1596 figure is 103 Christian households; the 143 figure was dropped.
- Sijill 48: 22 June 1565 (Ḥammūdeh 29 June), one entry; the deed was shown and does not survive. The note was added to the text.
- The registers do give names (they are mufaṣṣal).
- Ḥadīd is a lead, not a finding.
- Karak and Shawbak are in Hütteroth and Abdulfattah.
- Musil's "ḫ. el-Ḥaddâd" is a ruin, not a lineage.
- The Karak wheel was misread, not wrong.
- The corridor is remembered in both directions.
- Peake records the Ghassanid claim without judging it.
- The "Warda Books 2025" caption is Munther Haddadin's 2024 book.
- Ramallah was Qaysī in 1844.
- Three shaykhs were put to death in 1834, and 1834 broke the system without ending it.
- Twenty-six men of Jifnā were taken for forced labour, not exiled; one priest followed them.
- The population curve shows the 1916 epidemic as an inference.
- 1938: two fights, a week apart, with each witness's count.
- Kaddoura was mayor from 1943 to 1947.

## v76 — 13 November 2026

### The maps (option B, terrain and water)

All eleven drawn maps now follow one style guide, `docs/MAP_STYLE.md`, implemented in `src/map_style.py` (colours, symbols, type, furniture, terrain) and `src/build_atlas.py` (the `Sheet`, `Flat` and `Lin` projections). Figure 11 is a table and is unchanged.

- **One symbol vocabulary:** green = documented, ochre = remembered, grey = context, open diamond = standing evidence, red ring = Ramallah on every map (an empty ring before 1562). Figure 5's periods use a separate violet ramp, so green and ochre keep their meaning.
- **Ground:** hillshade and muted elevation tints from SRTM/Copernicus (AWS Terrain Tiles) on every regional and district map, each raster under 150 KB and cached in `data/terrain/`. District sheets have 100 m or 200 m contours, with the 800 m line drawn bolder as "the ridge". The old "no hill shading" rule is retired.
- **Water:** one blue family; wadis derived from the elevation model, left unnamed (no sourced names yet). Springs are not drawn yet, for the same reason.
- **Frame and type:** a hairline neatline with graticule ticks on the frame, a scale bar bottom-left, a locator inset on the district sheets, the legend under the map, one source line. No place name is under 11 px on a phone.
- **Redrawn:** figure 17 (the scattering) on a real Arabia with terrain, every arrow drawn as tradition; figure 33 (the town plan) as a framed schematic with a north arrow, "schematic, not to scale", and no scale bar.
- `tools/restore_svg.py` now keeps the eleven maps (their text was checked against v60 first). The book grows by about 1 MB, almost all of it the terrain images.

## v75 — 13 November 2026

### The new literature (David chose "All")

The deep reading of the books shelved on 12 and 13 November (report: `history/deep_research/new_literature_2026-11-13/deep_research_new_literature_2026-11-13.md` in the project files). New paragraphs are in the `ADD75` table in `src/build_v5.py`; corrections are inline, with FIX boxes where the book's wording changes its meaning.

- **New:** al-Maʿlūf 1907, p. 371 n. 1, the earliest outside witness to the Karak and Shawbak origin, the Ḥaddādūn and Sharāqiyyūn halves and the Muslim family at al-Bīra, with no Ghassanid claim; Dissard's Muslim allies and Diāb ibn Qaysūm; the Ḥalasa marriage dated (Oppenheim via Chatelard, Connell) and its lasting marriage ties; Jaussen's 1906 Salt case and the bride-price; the Māʿīn move in stages (1892/94, c. 1901, 1909); Seetzen's Ḥaddādīn tents c. 1806 (via Chatelard) and Jaussen's eight Christian tribes of Karak c. 1905, with a row in the Karak table; Karak's Christian quarter, the Gharābā, the Greek metropolitan and the Arab clergy, Tristram's school; Mādabā sharecroppers from Ramallah and the ʿAzayzāt exodus; Zahran's Mamluk claim, traced to the 1991 clan book; Shahîd on Abū Karib, al-Maṣna, Adhruḥ and Ḥātim's king "from Maʾāb to Zughar" (Karak link labelled inference); Shahîd on Dayr Ghassāna; Analekta III dating the interpreter's flight to 17 December 1809, and the guns taken in April 1821; the Ottoman school report of 1903; van der Leest on Gobat, Girgis (15 March 1863), the 1863–64 petition, Nyland and the 137 boys of 1878; St Andrew's 1855 and 1887/1888 printed both ways; Peake's second road for the Ḥishmeh; the gazetteers on embroidery and remittances; what Haddadin 2024 says, without his unsourced "650".
- **Corrected:** Shahîd's source base (the withdrawn v57 claim is false: Syriac records of 684 and 793, ninth-century Arabic writers, Umayyad verse); Jabala is historical and the conversion is the legend; the 684 timeline line (Kalb's council, not a Ghassanid faction); Greek-silence pages are I.1 534 and 562–64; Ṣadaqa called "inferential" as Shahîd does; Peake 1935 only records the Ghassanid claim; the Biskintā Ḥaddād line is a Lebanese family from the Ḥawrān (al-Maʿlūf p. 179); al-Dabbāgh and Kaddoura are one witness for the Qalāwūn endowment; Dissard's "about 1815" and the gazetteers' seventeenth century give way to the register of 1562; the bibliography's "incompatible with a 300 AD migration" line replaced.

## v73 — 12 November 2026

Scan checks on David's PC: Zarifeh ʿAudeh confirmed, the March 1949 count read, Cadora's 1953 school figures added. Small differences no longer noted (David: "No need to note small differences … for the entire book"): seven notes trimmed (a spelling aside, a roster place name, an edition-numbering caution, two page-number caveats, a pending page check, an OCR reading note). Disagreements that change the story are still printed both ways.

## v72 — 12 November 2026

### More from Cadora (David chose "All 24", 12 November)

23 further paragraphs from Cadora, *Remembering Ramallah*, each marked as his account with scan page markers, appended to `ADD72` in the "v72b" block: the 1889 first class by name, the Holy Sepulchre ceiling, the interpreter of the 1820s, red and white brides with the Mar Saba diary of 1844 ("1500 souls"), Sheikh ʿĪsā Ḥarb, the newcomers' dates, the sheikhs' cloak, the 1807 church's end, weddings, the 1902 mill and 1928 arak works, cemeteries and malaria, the 1910–12 minutes, the 1920s council, the 1924 boundary, the 1920 snow and harvest, the societies, the 1944 hospital committee and "Ramallah Federation", the author's father and wife, professional firsts, Selim Hishmeh with Stanley, the first firms in America and the 1954 roll, and the town in numbers in 1953. Conflicts are printed both ways by name: the 1898/1900 money order, the newcomers' dates, the locusts in 1914/1915, the hospital sums, the fight in 1904/1905, and the church demolished in 1951/1952. Holy Light delegation (candidate 12) skipped: already in the book.

### Round 2: the ready items, Cadora, and the Saah sidebar

David chose "Ready items" on 12 November. New paragraphs, each with its source named, are held in the `ADD72` table in `src/build_v5.py`, keyed by entry title. Numbers are those of the report *Ramallah history gaps round 2*.

- 1938: E14 Assistant Inspector W. E. Birch named (Palestine Police report 1938, s. 17(a); McDowell); E15 the laundress's house; E17 the Ramallah and al-Bīra units and their commanders (the two Ḥannā Khalafs are not merged).
- 1948: E19 Jordan from 18 May (Shalash; Cadora p. 64); E33 the air raids of May and the mayors' visit to the king; E29 to E31 the Lydda march, its dead and its witnesses; E20 the Friends schools take in refugees; E21 the Arab Refugee Congress count, 72,660, March 1949; Cadora's 1953 split (5,000 and 8,500) beside Shāhīn's; Cadora acting mayor from 1 April 1948.
- Cadora also: the 1820 feud in his telling; the municipality established 1 April 1908; the Saah builders of the 1852 church; the clans' crafts; the 1885 lanterns and the 1935 grid; Ḥannā Ibrāhīm al-Saah in Istanbul and Joseph ʿAudeh in 1895 (printed beside Shāhīn's England); the Qaddūra name; Yūsuf Jiryis al-Saah's factory, 1940.
- The Saah builders and Acre: a sidebar in "New families arrive", told as family tradition (Cadora pp. 35, 40, 146), with Buckingham (1821) and the family tree; the al-Qassīs priestly line and Ayoub al-Ṣafadī's silk robes.
- Karak: D4 and D5 and E10 (Peake's Arabic p. 351 on al-Ḥalasa and al-Ṭanāshāt, both views printed; the Ḥaddādīn entry is p. 348).
- Since 1948: D9 and D13 the Federation's founding year in each source's words (AFRP 2024–25 report: "Founded in 1952"; 1958; 1959; the Aramco World 1978 inference); D10 Decree 19 of 2021 and the Christian council head; D15 the 1967 count dated 21 September 1967 for Ramallah–Jericho (occupying power's count).
- Already in the book, so nothing added: D2 (the Latin parish registers of 1857) and E6 (Karak 57 per cent Christian in 1596).

## v71 — 11 November 2026

### Lot 3: large files read on David's PC

- **C60 closed.** The 1961 Jordanian census, Table 2.11: 8,745 Christians among 29,269 people in Ramallah and al-Bīra together (29.9 per cent); no figure for Ramallah alone.
- **C22 closed, book stands.** Ibn al-Kalbī's *Jamhara* (ed. Nājī Ḥasan, p. 615) does put the water between Zabīd and Rimaʿ. The note now gives the page and the Arabic, and says that Yāqūt reports him differently.
- **C28.** The Strehlke note is now from the page itself (p. 18): "qua vaditur" is his correction of the manuscript's "qui vacatur".
- Confirmed with no change needed: C37 (آل الشقرة, بضعة عشر رجلا), C50 (1939 in Shāhīn's Arabic), C53 (4,500 and 9,000 in both editions), the 1946 emigration figure.
- Still open: C14, C47b, the date of the 1967 census, Bertram and Luke after §79.

## v70 — 10 November 2026

### The accepted additions from the deep research (A1 to A40)

Thirty-three new paragraphs, each with its source named, appended to the entry it belongs to. They are held in the `ADD70` table in `src/build_v5.py`, keyed by entry title. Items read only in extract say so in the note.

- Chapters 1 to 5: A1 Khirbet Raddana; A2 Eusebius's two distances; A4 Abraha's repair by month; A5 after al-Mundhir; A6 Ghassān after the conquest, a name without a stated faith.
- Chapters 6 and 7: A7 and A8 the register of 1531–32 and a town with no lord; A9 the Hebron endowment at Karak; A10 the Jordanian reading of 1596 (in the A9 note); A11 "they went back and forth" (David, 10 November); A12 the second Kasābra and Ḥijāz ibn Ḥusayn; A13 the sons of Ḥadīd and Shuqayr, 1604–05; A14 the boundaries of 1565.
- Chapters 8 and 9: A15 the ʿAzzouz incident in full; A16 the local chronicle of the faction wars; A17 Jabal al-Quds; A18 the ḥōsh, the madāfa and Karm ʿAlī; A19 why 1600 to 1800 is blank; A20 the Friends' schools; A21 the town about 1875; A22 the two meanings of qaṣr; A23 the Rafeedie at al-Bīra.
- Chapter 10: A24 to A26 and A33 the revolt (1936, the months around the battle, the names of the dead, the army's word); A27 the missing men were Christian men; A28 what the town lived on; A29 women's societies, paid embroidery and dress; A30 the quarrel behind the 1946 election; A32 the priests' meeting of 30 August 1932; A37 Radio Ramallah after 1948.
- Chapters 11 and 12: A34 al-Jalazūn's first years; A35 the twin towns in 1967; A36 the mayors under occupation; A38 the lions of al-Manāra; A39 the Rāshid al-Ḥaddādīn monument; A40 refugees and the town since.
- Already in the book, so nothing added: A3 (the places of the water) and A31 (the radio opening of 1936).

## v69 — 10 November 2026

### The story check: corrections from the deep research of 10 November

David delegated the rulings ("answer the questions using a Palestinian bias from the literature with proper academic inference when needed"). Rule set: Palestinian and Arab sources decide; where two disagree, both are printed by name; Israeli authors never drive a change and are marked; inference is labelled. Numbers are those of the report *Ramallah history gaps and story check*.

**New correction boxes (8):** C11 the Maʾrib dam (620 to 680 m, sixth century BC, about a thousand years); C27 the hill before the family (first Christians to stay, not first to stay); C29 "in the registers from 1553–54"; C32 the court entry of 22 June 1565 (Ḥammūdeh: 29 June), one entry, deed shown in court; C39 three shaykhs put to death in 1834; C45 and C46 two fights in 1938 and the range of the dead; C58 Kaddoura mayor 1943–47.

**Changed in place, with the source named:** C1, C3, C4, C5, C6a–b, C8, C9, C10, C12 (Israeli-author marks: Finkelstein, Agranat-Tamir, Magen, Roll), C13, C15a–c and e, C16, C17, C19, C20, C21, C23, C24, C25, C26, C30, C33, C34, C35, C36, C37, C38, C40, C41b–c, C42, C43, C44, C47a, C48, C49, C50, C51, C52, C54, C55, C56 (the chronology test now reads 1959), C57a–b, C59, C60.

**Not changed, after checking the book's own notes:** C6c (al-Dabbāgh is the source), C7 (Ghadban 2015 is the source), C15d (already given to Pliny), C18 (Nebes 2004 is the source), C41a and C41d (the notes already cover them). C2 is a wording change only.

**Held for David or for a page still to be read:** C14, C22, C47b.

**C28 (David, 10 November: "Add a note"):** the 1186 line stays, with one note that Strehlke doubted the charter and that Ḥammūdeh and Shaheen accept it.

**After the lot 1 and lot 2 page checks:** C31 now names Abū al-Fidāʾ (“most of its inhabitants are Christians”); C53 stands, since Shāhīn's English p. 29 prints 4,500 and 9,000; C58 is confirmed by the municipality's own list; C59 reads “in the summer of 1967, just after the war” (the census date itself is still unread).

## v67 — 9 November 2026

- **Evidence halves for chapters 9, 11 and 12.** No new text. Three existing entries move from the story to the chapter's evidence half, because each one reads a source rather than tells an event:
  - chapter 9: "The twin town and the Rafeedie family" (the Rafīdiyā tradition, as Ḥammūdeh reports it, and its limits);
  - chapter 11: "Our first history, written in New York" (Kaddoura's 1954 history);
  - chapter 12: "Shāhīn closes the record" (Shāhīn's 1982 history).
- **Build:** the figure restore step now lives in the repo as `tools/restore_svg.py`. It takes the v60 drawings from git commit 9bcad59, matched by figure title, and keeps Figure 27 as drawn. Full build:
  `python build.py && python3 tools/restore_svg.py && python3 src/post_restore_fixes.py out/AFRP_The_One_Line_v5.html && python3 src/restyle.py out/AFRP_The_One_Line_v5.html`.
  Checked: on main it reproduces the published file exactly, apart from the "Last updated" date and random clip-path ids.

## v64.1 — 8 November 2026

### Twelve consistency fixes (approved by David)

1. Khirbet et-Tireh: the chapter 2 note no longer says "until the earthquake of 749"; it points to the withdrawal.
2. Ṭaybeh: 11 km everywhere (the AD 69–70 note said twelve); great-circle from al-Manāra.
3. Jifnā: about 7 km everywhere (was 6.5 km and 6.7 km in two places).
4. ʿAin Samiya: 15.5 km in text and note; the "not independently verified" caveat is resolved with published coordinates.
5. "The ridge and the plateau stay Christian": one man of a queried "Jifnā" in a contract of 1374, not "men of Jifnā" in 1391–92; "continuously Christian" now notes Schick's possible break.
6. "The city, counted to the present": prints 42,122 for 2021 (PCBS), not 43,880 for 2024.
7. Population chart caption: the 1967 dip is no longer called "emigration".
8. 1953: "local count" throughout; the Taraki note records that she calls it "a Jordanian census".
9. "Our contribution": Muslim households since 1538–39.
10. Dissard / court record: "a year earlier" replaced with "in 1561, the year before the census of 1562". "About 1815" still unchecked.
11. Riyam inscription: seven lands, not eight, lie between the Azd and Ghassān.
12. The Federation: the convention count now notes that the roster has no 2020 convention, so the sixty-third falls in 2022.

- **Figure labels:** the "Today" band now reads 42,122 people in 2021, the Jifnā distance in the Roman-road figure is "about seven kilometres", and the Christian-traces timeline shows one man of Jifnā(?) in 1374. The two labels that the SVG restore step brings back are swapped by `src/post_restore_fixes.py`, which runs after the restore and before `restyle.py`.
- **Cross-references:** two leftover "the entry above" now name the entry they mean.
- **Not changed:** the population chart still marks a 2024 projection point, because the restore step brings back the v60 drawing. Its 1967 label already says "counted under curfew".

## v64 — 8 November 2026

### One voice

All 96 entries are rewritten in the voice of `STYLE_GUIDE` (project files):
- plain, warm sentences, with "we" and "our family";
- short titles in sentence case;
- terms explained the first time they appear;
- cross-references that fit the new order.

Each story chapter opens with what was happening and ends with "What we still
don't know".

Nothing else changes. All 272 notes are unchanged, character for character.
All 41 figures, 51 photographs and source pages, the tables and the correction
boxes are kept in their entries. Points the writers thought doubtful were left
alone and listed for David in `history/rewrite_v64_review_notes.md` (project
files).

## v63 — 7 November 2026

### Story first, evidence second (structure only)

David chose option B. All 96 entries are moved and none is reworded.
- **Part One, "The Story of Ramallah":** ten chapters in date order, from the
  land before 1200 BC to the city today.
- **Part Two, "How We Know":** four sections:
  - the Ghassān story, tested;
  - the missing centuries;
  - Karak, the charts and the registers;
  - what is proven.
- **What changed besides the order:**
  - The old "What the ground says" and "And in our own line" signposts are
    dropped.
  - Chapter-head photographs and the "Where our own line stands" strips follow
    their entries. Five strips that repeated "nothing datable" have no chapter
    now.
- **Not done yet.** Some entries still say "the entry above" or "this era"
  about their old neighbours. That is fixed in the rewrite, chapter by chapter,
  following `STYLE_GUIDE` (in the project files).
- **How it works:** `_ORDER` in `src/build_v5.py` lists each chapter's
  entries by the start of their titles. The build stops if any entry is missed
  or matched twice.

## v61.2 — 7 November 2026

### The municipal election of 1946

David added a new source: the election file of the Jerusalem advocates Anton
and Hanna Atalla, Israel State Archives P-213/40 (208 scanned pages). It is on
the shelf as `1946_Ramallah_Municipal_Election_File_Atalla_ISA_P-213-40.pdf`.

- **New entry, 1946, "The town votes".** It covers:
  - the four districts by clan: Dār Jiryis, the Ḥaddāda, Dār Ibrāhīm and
    al-Shaqara;
  - the electoral committee and its timetable;
  - a register drawn from the municipal tax rolls, open to men aged 21 and over;
  - three members returned unopposed, and the Ḥaddāda poll of 15 April 1946;
  - the hearings of November and December 1946.
- **A results table** with the vote for each candidate.
- **Two pages from the source**, under "From the source": the English notice
  of 6 April 1946, and the committee's Arabic account with the result.
- **Voter lists and the family tree.** A paragraph gives the 407 names that
  can be read on the lists by house, and how many of them match the family
  tree; 117 are not in the tree yet. The review list is in the project files
  under `history/sources/1946_election/`.
- **The district 2 ballot paper** (PDF p. 142) is added as a third source page.
- **Not yet done.** The register numbers about 580 voters, but only 407 names
  can be read on the lists. The ruling, the petitioner and exhibit P.5 are not
  in the file.

## v61 — 7 November 2026

### Every figure in the family tree book's look ("Classic")

David chose the Classic option, so all 38 figures and the photographs now
match the Ramallah Family Tree book.
- **Plates.** Each figure sits on white paper between a green double rule
  above and a thin green rule below. The figure number is set in ochre beside
  a green diamond, and the source line is ochre with a thin ochre rule. The
  type is Times throughout.
- **Colours.** `src/restyle.py` runs after the build and after the atlas
  maps are restored. It maps every colour inside the SVGs onto the tree
  book's palette:
  - creams become white;
  - golds and rusts become two ochres, light for shapes and strong for text,
    so they stay distinct;
  - plum and violet become ink greys, because the tree book has no third hue;
  - water blues become a cool stone grey;
  - greens become the tree book's greens.
- **Captions.** The captions that named a colour now name the new one
  ("the ochre ring", "the thin dark band", "dashed dark rings").
- **Photographs.** Each photograph has a thin green frame, a white mat, an
  ochre "Photograph" label, an italic caption and a light warm tone.
- **Seventeen pictures from Shaheen's *Pictorial History of Ramallah, Part II*
  (2005).** David says AFRP holds the rights. Each is credited to the book
  and its page, "reproduced courtesy of the American Federation of Ramallah,
  Palestine". The web copies are in `img/shaheen/`.
  - Chapter 9: the 1186 charter in Latin, with the road *qua vaditur Ramelie*.
  - Chapter 11: the 1553–54 Bayt Jālā register with the thirty-six families.
  - Chapter 12: Shaheen's settlement map, the 1639 "Rammula" map, a Hishmeh
    portrait from the 1870s, a Harb loan agreement of 1896, and a wedding of 1900.
  - Chapter 13:
    - Mayor Elias ʿAudi's family, about 1905;
    - an Ottoman conscript, 1916;
    - a 1930 Shaheen wedding;
    - Manara Square, about 1953;
    - the Arab Women's Union in the 1960s;
    - the Union's meals for refugee children after 1967.

  David confirmed that AFRP holds the rights to every photograph in the book.
  On that basis four more were added: a weaver at his loom, about 1890–1900
  (chapter 12); Ramallah from the south, about 1910; the Friends Meeting House,
  about 1912; and a refugee school in a Ramallah church, 1949 (all chapter 13).
- **Three new figures, drawn in the new look** (`src/build_figs5.py`), for
  eras that had few or none:
  - "Six sovereigns, one people" (539–63 BC);
  - "Who ruled, and who stayed, 636–1517": the dynasties over eleven dated
    Christian traces, with 1186 picked out;
  - "Where the road stopped": a map of the march from Lydda and Ramle and the
    five camps, joined to the towns their people came from.
- **Rāshid's family.** The pencil drawing of the memorial to the first family
  of Ramallah, from the tree book's cover, now opens the book. A photograph of
  the bronze memorial opens chapter 12.
- **One fix.** The atlas plate "The district when Rome wrote it down" and its
  caption still said Ramallah was named nowhere "until 1279". v60 moved the
  first naming to 1186, so both now say 1186.
- **Pages from the sources themselves.** Eight pages and plates now sit inside
  the entries that cite them, under a "From the source" label, each with a
  translation of the lines that matter:
  - ʿAzīz Shāhīn's Arabic account of the founding, *Kashf al-niqāb* (1982),
    p. 10 → "What the family remembers";
  - the 1562 endowment register, Işık's 2015 edition p. 73, with the two
    Ramallah entries boxed (the village, and the 71 Christians) → the 1561–62
    settlement;
  - Robinson at Jifnā, 13 June 1838 → the 1834 revolt;
  - Guérin at Ramallah, 25 May 1870, in French with the Arabic name → the 1850
    church;
  - Seetzen's German of 1806 ("a considerable village, inhabited mostly by
    Greek Christians") → "How the town actually lived";
  - two plates from Grant's *Peasantry of Palestine* (1907): the walled lane
    into the town, and the Friends schools → the Grant entry;
  - the first issue of Boulos Shehadeh's *Mirʾāt al-Sharq*, 17 September 1919
    → "The people this town produced".
- **Period pictures** (downloaded on David's approval, all public domain):
  Strehlke's 1869 printing of the 1186 charter, with *qua vaditur Ramelie*
  boxed, and Vesconte's map of about 1320, both in "The name appears". Also
  the 1881 engraving of the Crusader church at al-Bīra (Magna Mahumeria), the
  1880 survey sheet showing Ramallah and al-Bīra together, and the 1881
  engraving of the al-Bīra khan (the twin-town entry). A 1919 photograph of a
  Ramallah man spinning wool opens chapter 13.

## v60 — 7 November 2026

### Front matter, the family's memory, and the actual data on 1562

**Front matter (draft for the authors).** A dedication, preface and
acknowledgements now open the book, after the title block.

**The oral traditions go in, marked as oral tradition.** There is a new entry,
"What the family remembers". It covers:
- Ṣabra's three brothers (Rāshid to Ramallah, one to Bayt Jālā, one to al-Salṭ);
- the daughter given to Haleesa, from whom the Ḥalasa descend;
- the move to Maʿīn in 1892 and "over 800 souls" by 1953;
- Kaddoura's Ṭanāsh, the purchase from the Ghazāwneh and Karm ʿAlī;
- Khalīl Abū Rayya's account of the 1953 journey to Maʿīn, in Arabic and English.

Sources: N. Shaheen, *Pictorial History II* (2005), chs. 1–3; *Qiṣṣat madīnat Rām
Allāh wa-l-Bīra*, p. 24. Dissard, *Revue Biblique* 1905, pp. 419–421, is added as the
oldest printed telling. His "about 1815" is noted as impossible for Ramallah.

**"Founded 1562" reworded to the actual data.** A FIX box sets out the order of
the records: named 1186, endowed 1279, empty farmland 1525–28, Muslim households from
1538–39, terms agreed in court 1561, counted 1562. The book now calls 1561–62 the
Christian settlement. The key-dates page and the chapter summaries follow. The
households chart showed 37 Christian households for 1562; it is corrected to the
register's 64. The stale 1186 row on the key-dates page, "pledged by a Crusader
king", is corrected to match v58.

**New documents.**
- Robinson 1838 on Bayt Jālā: Christians only, the two-year tradition, 500 taxable
  men, 60 who could read, five shaykhs.
- The 1922 census civil-condition table: Ramallah 170 widowed or divorced women
  against 92 men; 736 married women against 576 married men.

**Photographs.** One or two per chapter, fifteen in all, from the Library of
Congress Matson Collection ("no known restrictions on publication"). They are
linked from loc.gov, not copied into the repository.

**Checked and left out.** "1,500 of 6,000 natives had emigrated" is not in the
English text of Shāhīn (1982).

## v59 — 26 October 2026

### What the Wikipedia article on Ramallah pointed to, checked at the source

**1938: the town's own witness.** Khalil Totah, born in Ramallah in 1886 and head of
the Friends Boys School, kept a diary through the revolt (ed. Thomas M. Ricks,
*Turbulent Times in Palestine*, IPS and PASSIA, 2009). The 1938 entry now carries his
dates: the police station attacked on 5 September, the court and post office closed
on 9 September, the district offices' typewriters taken on 16 September, the battle
with six aircraft on 25 September, and a rebel court sitting in Ramallah in October.
Totah's 25 September and the Quaker letters' 1 October are printed side by side.
Anderson, *JPS* 47:1 (2017), pp. 45–47, is cited for the rebel courts generally.

**Electricity and the radio transmitter.** In the 1922–1944 entry: electricity in
1935 per the Ramallah Municipality (Shāhīn 1982 gives 1936, noted). The Palestine
Broadcasting Service's main transmitter was in Ramallah from March 1936 to 1948
(Stanton, *Jerusalem Quarterly* 86, pp. 101, 109–10).

**The 950 dirhams stay withdrawn, with a lead.** Wikipedia credits the twelve men and
950 dirhams to Rapoport, *Becoming Arab* (2025), p. 105. That page was not seen, and
the same sum is given for ʿAyn ʿArīk on p. 104. The note now records Rapoport's
"twenty-seven documents, all dating from the 1300s" and Müller's list of Ḥaram
documents of 706–708 AH as the place to look.

**Not taken from Wikipedia:** Kelly (2017), p. 130, which could not be seen; the PBS
"1939" date, which is wrong; and "a fourth of 6,000 natives had left by 1956", which
has no source and may be a misreading of "1946".

## v58 — 10 October 2026

### Retitled, and the October research folded in

**The book is now *The Roots of Ramallah: A History of Its People*.** It was
formerly *The One Line*. The output file name and its web address are unchanged.

**A correction to the 1186 entry, made from the charter itself.** Strehlke,
*Tabulae Ordinis Theutonici*, p. 18, no. 20: Guy de Lusignan pledges *unum casellum
nostrum … prope viam regalem, qua vaditur Ramelie*, "one hamlet of ours near the
royal road by which one goes to Ramallah." The pledged village is not named, so
earlier editions were wrong to say "the village of Ramallah becomes the hospital's
property." Ramallah is still first named here. Printed as a FIX box.

**The 1198 "Ramalei" document is withdrawn.** Rey's source is a grant to Marseilles
forged at Acre about 1220 (H. E. Mayer, *Marseilles Levantehandel und ein
akkonensisches Fälscheratelier*, 1972, pp. 1–3), as Shaheen (1992), pp. 19–20,
already reported. In the same FIX box.

**The founding count has a second witness.** The endowment register of the
district, TKGM TTd. 406 (ed. Işık, 2015), delivered in 970/1562–63, lists Ramallah
under the Hebron waqf with "71 persons at 80 akçe": the same 71 Christian entries
as the census. Bayt Jālā's 218 matches too. The edition has no facsimile, so the
word read as *deyr* is flagged as unchecked.

**Karak was already Christian in 1301.** Al-Nuwayrī, *Nihāya* XXXI, 418–419, and
al-Maqrīzī, *Sulūk*, ed. Ziyāda, I/3, 912: Karak's Christians were exempted from
the coloured turbans of 700 AH because "the people of Karak are Christians, and the
Muslims there are few." Added to the Karak 1596 entry, three centuries ahead of the
register.

**The 1850 church is built from the Byzantine church at Khirbet et-Tireh.** Guérin
(*Samarie* II, 1875) and al-Houdalieh (2016). The et-Tireh burials were reinterred
there on 4 August 2015.

**New entry, 1904 · 1908.** The Patriarchate's own 1904 count (Bertram & Luke,
1921, p. 9 n. 1): Ramallah 4,500 Orthodox, Bayt Jālā 4,340, Karak 1,600. The same
report records the Arab laity's struggle with the Greek Brotherhood after 1908.

**New entry, 1938.** The revolt reaches the town: the battle of 1 October 1938,
the British bombing, about eighty killed, from the diary of a Friends school
teacher (McDowell, *Notes from Ramallah, 1939*). The book had nothing on 1936–39.

**Adhruḥ is a Ghassanid place in the sixth century.** Shahîd (2002), II.1,
pp. 61–62, added to the al-Dabbāgh paragraph, as evidence about the region only.

254 notes (was 245). 38 figures, unchanged.

## v5.7 — 7 September 2026

### The open questions, worked through

Fourteen closed. The full state is in `docs/OPEN_QUESTIONS.md`.

**A correction to v5.6, made within a day of printing it.** Robinson & Smith
(1841, III.78–79) was read directly, and the received account of the Jifnā
deportation is wrong — including in this book's own v5.6 entry, and in the general
reference works. Robinson: *"After the rebellion of 1834, twenty-six men were
taken to Egypt and put into the public works, whence they have never returned.
Not long since, one of their two priests went to Egypt to look after them, and
died there."* They were taken for **forced labour**, not exiled; Robinson gives
**no motive and no accusation**; and **one** of the village's two priests followed
them **later**, and died there. The error is a misparse of "one of their two
priests." Printed as a FIX box.

**Why Jifnā was punished** — not a local rising. It lay in the **northern Banī
Ḥārith**, whose shaykh **Ismāʿīl Simḥān was executed by Ibrāhīm Pasha in 1834**.

**Bayt Jālā, 31 May 1834** — soldiers killed **33 Christian men and women** on
suspicion of looting, the day after Ibrāhīm re-entered Jerusalem. Rood, *JQ* 27,
whose own source is the Greek Orthodox monk Spyridon.

**The Bethlehem Muslim-quarter destruction is withdrawn** pending a page.

**The Samḥān nāḥiya question dissolved.** Banī Ḥārith was bipartite — northern
(Simḥān, Rās Karkar) and southern (Kaʿraja, Dayr Ibzīʿ) — and Banī Zayd is a
separate nāḥiya. The circulating table collapses the halves and cites Doumani
p. 35, where no such table exists. **Ramallah sat in Jabal al-Quds**, not as a
seat — so the book's "not a throne village" is now positively sourced.

**The eighth bachelor, found.** Ḥammūdeh reads the 1562 register as 63 households
+ 8 bachelors; the family's transcription reads 64 + 7. **Both total 71 Christian
entries.** The disagreement is one line, read once as a household and once as a
bachelor.

**The Federation has three founding dates because it has three foundings** — the
magazine in 1952, the constituting convention on 7 September 1959, IRS recognition
in August 1963 (EINs 38-6096448 and 38-6096449). The convention count closes on
1959, not 1958.

**Ramallah's Muslim majority, dated properly.** The 1967 census counted **6,966
Christians of 12,134 — 57 per cent.** By 1997, 32 per cent. The crossing falls in
those thirty years and cannot be dated closer: there was no census at all between
them. The 1967 count is an **Israeli state source** and the book now says so on
the page instead of routing it through a tertiary work.

**Khirbet et-Tireh's 749 abandonment is withdrawn** — al-Houdalieh's own
publication says the press "was maintained in continuous use from the Byzantine
through the late Ottoman periods." The press itself is now described: **direct
screw, four press-beds**, a crushing basin 2.1 m across, rooms above for the
owner's share.

**Al-Bīra and Ramallah counted, building by building** — Riwaq's free registry:
**381 historic buildings at Ramallah, 168 at al-Bīra**, and al-Bīra's list is
dominated by the same families Ḥammūdeh names.

**Al-Jalazūn's "inconsistent" population is a category error** — UNRWA's own page
gives 9,450 beside a density computed from 13,000. Registered refugees against
residents.

**The Rafeedie claim is downgraded to an assertion.** Ḥammūdeh's endnote on that
sentence turns out to be an aside about the 1948 refugees, not a citation.

**PCBS 2021 = 42,122** confirmed to the table and locality code; no 2024 figure is
printed, and none was extrapolated.

**Little's *Catalogue* is no longer the blocker** — McGill has put the entire 1978
photographic survey of the Ḥaram corpus on the Internet Archive, open access.

**38 figures · 223 notes.** QA clean.


## v5.6 — 7 September 2026

### A Jesus section, an al-Bīra section, and a full audit

**New: THE ROADS HE USED — and the ridge they run along.** A three-panel plate
(Figure 38) putting every Gospel place at its real coordinates against the hill
Ramallah would be founded on. The two roads from Galilee; the district inside a
day's walk; a numbered key so no label crowds the map. **Markers are graded on
the identification of the place, never on the verse.** With it, three entries:
the roads and Ephraim/eṭ-Ṭaybeh; what this ridge was actually doing in AD 30
(the Gophna toparchy, the terraces, the pilgrim traffic); and what happened to
it in 69–70, when Vespasian garrisoned **Bethel and Ephraim** — the same two
towns — and Titus held Jerusalem's surrendered priests at **Jifnā**.
The al-Bīra and al-Qubeiba pilgrim traditions are printed and graded as
traditions, in violet, dashed.

**New: THE TWIN TOWN — the Rafeedie of al-Bīra.** The Christian family that came
to al-Bīra from Rafīdiyā in the nineteenth century, on Sāmiḥ Ḥammūdeh's
authority — and the fact that **Rafīdiyā tells the same origin story this family
tells**: Ghassanid Christians, flight from al-Karak, a refused marriage. The
book prints the parallel and the objection together: Rafīdiyā already had 85
Christian households in 1596, so the tradition cannot be a literal foundation
account. **The argument offered is that it is a form** — how Palestinian
Christians of these hills remember themselves — and that a form is not a lie.
With Pringle on eight centuries of continuous habitation at al-Bīra, the 1541
court record putting Ramallah and al-Bīra men in business together twenty-one
years before the founding, and two claims the book was offered and refused.

**New: THE PEASANTS' REVOLT of 1834.** Previously a single clause. Now the
event that destroyed the throne-village shaykhs of these hills — including
ʿAbd al-Jābir Barghūthī of Dayr Ghassāna and Ismāʿīl ibn Simḥān of Rās Karkar —
and the one village of this district recorded as taking part: **Jifnā, whose
twenty-six exiles to Egypt were joined voluntarily by two of its priests.**

**New: AND WHERE THEY LIVED — the camps.** The book said Ramallah tripled in
1948 and then never said where the people went. Now: Qaddūra inside the city,
al-Amʿarī, al-Jalazūn, Qalandiyā and Dayr ʿAmmār, with origins, land tenure and
counts — and the demographic question answered in the right order, without the
sectarian frame.

### The framing audit

A full pass over the manuscript for imported framing. Findings acted on:

- The **"Christians and Christianity" volumes** were labelled a Hebrew University
  finding aid. They are the publication series of the **Staff Officer of
  Archaeology for "Judea and Samaria"** — the archaeological arm of the Israeli
  Civil Administration. The caveat now says so.
- **"Judea proper"** removed from the book's own annotation voice.
- The **Amnon Cohen** annotation described Ramallah's Christian majority as
  "demographically displaced by refugee settlement." That contradicted the book's
  own 1948 entry and split this town's Christians from the refugees. Rewritten.
- Custody language corrected: the Mandate files were **taken over in 1948**, not
  "inherited"; the ʿAin Samiya goblet is **held** in the Israel Museum, three
  years into the occupation, **rather than in the governorate it came out of**;
  the Ottoman nüfus registers were transferred to the *Mandate* government.
- Affiliations named where the book had left them as metadata: **Avni** (IAA
  Archaeology Division), the **IAA repositories**, **Judea and Samaria Research
  Studies** (Ariel University, inside a settlement), and the **Mount Gerizim**
  excavation.
- **"the Christian settlers"** — a word this book cannot use loosely — replaced.
- FamilySearch's "Ramallah, Israel" is now named as the cataloguer's geography.

### The fact-check

- **The Ḥaddādīn are no longer said to be "named 1596."** The book proves in a
  full chapter that no occurrence of the name is known before the nineteenth
  century, and the Verdict and Key Dates contradicted it. Fixed.
- **Ghassān in ʿInān 75 and ʿAbadān 1 is in western Arabia, not north-central.**
  Robin, who edited both texts, puts the tribe's centre in that period at
  Yathrib. The dam-collision argument survives in corrected form: the
  inscriptions do not put Ghassān in Syria by 250, they put it **out of Yemen**
  by 250, which is enough.
- **Every distance on every plate is now computed** from the book's stated origin
  and the site's own plotted coordinates, so a label cannot drift from its dot.
  Tell en-Naṣbeh falls from 3 km to **1.8**; eṭ-Ṭaybeh from twelve to **eleven**.
- **The founding arithmetic, from the project's own register transcription:**
  the 1562 register lists **64 Christian households and 7 unmarried men against
  10 Muslim** — not "27 families up from Bayt Jālā."
- Jabal Usays: the writer is **Ruqaym son of Maʿarrif the Awsite**, not Ibrāhīm.
- Jericho 2019–23 is **Nigro and Yasine**; Guy de Lusignan was not yet king in
  March 1186; Mirʾāt al-Sharq has **1,132** issues; the Friends Girls School was
  renamed **1925**; Callaway dug et-Tell **1964–70**; Raddana was dug **1969–74**.
- Mount Gerizim's mid-fifth-century date is **Magen's, and disputed**.
- Beeroth: al-Bīra "most likely comes from Aramaic *bīrāh*, fortress, not the
  Hebrew for wells." Six candidates, none secure.
- Transliterations unified (eṭ-Ṭaybeh; Ḥassan Nawwār; Hassenauer).

### New to the shelf

Doumani, *Rediscovering Palestine* · Taraki, *Enclave Micropolis* · the ARIJ
camp profiles for Qaddūra, al-Amʿarī, al-Jalazūn, Qalandiyā and Dayr ʿAmmār ·
PCBS 2017 · Taha on the Palestinian Department of Antiquities.

**38 figures · 219 notes · 1,844,165 bytes.** QA clean.


## v5.5 — 7 September 2026

### The Bible as a map of this district

At the author's direction: more links between scripture and hard evidence, and
all of them local.

- **New entry, Era Three: THE BIBLE IS A MAP OF THIS DISTRICT — and Palestinian
  villagers are why it can be read.** Nobody found the biblical places by reading
  the Bible. Robinson and Eli Smith found them in 1838 by walking into Palestinian
  villages and asking what people called home, and the answers were the ancient
  names carried in Arabic for three thousand years. *ʿAin Shams is Beth Shemesh.
  ʿĀqir is Ekron. Beitin is Bethel. Seilūn is Shiloh. Mukhmās is Michmash.*
  Closing argument: **a replaced people forgets the names.**
- **New plate: every biblical place within a day's walk**, with the Arabic village
  it survived as, the scripture, the excavation, and a grade for **the
  identification** — not for the scripture. Nine places, the furthest nineteen
  kilometres out.
- **al-Jib / Gibeon.** Pritchard, 1956–59, found **more than sixty jar handles
  inscribed גבען — Gibeon**, in 8th–7th-century Hebrew script. The site says its
  own name, six kilometres from Ramallah. Graded **NAMED ON SITE**.
- **et-Tell / Ai**, printed as gladly as the rest: Hebrew *ha-ʿAi* means **"the
  ruin,"** and the ground agrees — Early Bronze town destroyed c. 2400 BC, empty
  a thousand years, then an Iron I village on the abandoned mound. Dug by
  Marquet-Krause, Callaway and **Hani Nur el-Din of al-Quds University**.
- **al-Bīra / Beeroth** included and openly graded **CONTESTED** — Joshua 9:17,
  Ezra 2:25, Nehemiah 7:29, with the rival candidates acknowledged.

### The scripture thread, run through the other eras

- **Scripture on the Iron Age map** — each site now carries its biblical name and
  one verse: Beitin (Gen 28:10–19), al-Jib (Josh 9–10), Khirbet Seilūn (1 Sam 1–4),
  Tell en-Naṣbeh (1 Sam 10:17–24), et-Tell (Josh 7–8).
- **Jericho** — noted that the same mound carries the Jericho of Joshua 6, near the
  *top* of it, some eight thousand years above the tower this entry is about. The
  book takes no position on the conquest debate and says so.
- **Moab** — the **Mesha Stele and 2 Kings 3 are the same war from opposite
  sides**, naming the same king. Two accounts of one campaign, each the enemy's
  version of the other. The stele also carries the earliest occurrence of the
  divine name outside the Bible.
- **Mount Gerizim** — **John 4:20** added: *"our fathers worshipped in this
  mountain."* The dispute the verse records is the one the archaeology dates.

**37 figures · 187 notes · 1,765,492 bytes.** QA clean.


## v5.4 — 7 September 2026

### Who was on this ridge in 1000 BC — a new entry and two new plates

Answering a reader's question: *were the Israelites here, and were they in
Ramallah?* The second half is easy — **Ramallah did not exist**, and would not
for another two and a half thousand years. The first half is the more
interesting one, and it is now answered from survey data rather than assertion.

- **New entry, Era Three: WHO WAS ON THIS RIDGE — the highlands fill up, and
  nobody arrives.** The central hill country goes from about **25 settlements to
  about 250** between 1200 and 1000 BC, and from a scatter to roughly **45,000
  people** — with no matching emptying-out anywhere a migration could have come
  from.
- **New plate: the highlands fill up.** One dot per settlement, Late Bronze
  against Iron I, with the three things the surveys do *not* find: no destruction
  horizon, no new pottery tradition, no arrival visible anywhere else.
- **New plate: the ridge in the Iron Age.** Every excavated site within a
  morning's walk, at real coordinates, with **Ramallah drawn as an empty ring**.
  **Khirbet Raddana lies inside al-Bīra** — a village of the 12th–11th centuries
  BC on the town's doorstep, dug in the 1960s and since built over.
- **Merneptah, 1208 BC:** the first appearance of the name *Israel* is written
  with the Egyptian determinative for **a people**, not a land — a group living
  in this country, among the people of this country.

The framing is the book's existing thesis extended: Canaanite, Israelite,
Judaean, Christian, Muslim, Palestinian are **names taken by a largely continuous
population**, not peoples replacing one another.

### Withdrawn before publication — the passion entry

An entry on the crucifixion was drafted for Era Six and **removed at the author's
direction before it was ever pushed**. It was proposed and framed by the
assistant, not asked for, and it placed an interpretive correction inside a
passion narrative in a Palestinian Christian family history. That was an
overreach on a matter of reading rather than of fact. The book's existing Gospels
entry is untouched; nothing about the passion has been added, altered or removed
from what the fourth edition carried.

**36 figures · 181 notes · 1,738,007 bytes.**


## v5.3 — 21 August 2026

### The Ḥaram al-Sharīf corpus, searched — and a claim of ours corrected

The 1390s Jerusalem corpus was the one place that might have put a named person
from this ridge inside the 931-year void. It was searched. **Result: nothing of
ours in the published part**, and one of this book's own claims turned out to be
an over-reading.

**The microfilm route is dead for now.** McGill's four rolls are open on
archive.org and the OCR is stroke-noise: in **310,000 characters** of recognised
Arabic from a Jerusalem religious archive, القدس، الحرم، الشريف and قرية occur
**zero times** and محمد occurs **once**. The commonest strings the software
produced are ااا and الا.

**So the published catalogue was searched instead** — Aljoumani, Bhalloo &
Hirschler (2024), which a reader can check. Across the whole of it the villages
of this ridge appear **twice**: a cotton debt of 1374 whose place-name is a
queried reading, and a **1914** letter about the imam of Silwād.

### New entry — ONE CHRISTIAN, ONE DEBT

Era Nine. **7 Ṣafar 776 / late July 1374**: *Niʿma ibn Bishāra al-Naṣrānī*, "the
Christian," buys cotton on credit from the provisioner *Ḥājj ʿUmar ibn Muḥammad
ibn ʿUmar al-ʿAllāf* — 218 dirhams at six dirhams a week, two witnesses, the whole
instrument later struck through, which is how a debt is marked paid. Text #922/4.

The entry prints the negative search in full, so nobody runs it twice.

### A correction, in a FIX box

Earlier editions listed **"men of Jifnā in the Ḥaram registers in 1374"** among
the dated records inside the blank. Two errors: it is **one man, not men**, and
the village is **a queried reading** — the scribe's <span dir="rtl">جفنا الجوز؟</span>,
which the catalogue's index keeps separate from Jifnā north of Ramallah. The
document is kept and demoted: evidence about the century, not about this district.
The claim is corrected in both places it appeared.

### Also

- `OPEN_QUESTIONS.md` §1 (Ankara) **closed on paper**: the eighty named heads of
  1596–97 are printed in al-Furqān volume 6. What remains is buying it.
- New §4b records the Ḥaram search and what would change the result — Little's
  catalogue index (print only) and the CALD database.


## v5.2 — 21 August 2026

### The two strands, made visible

Every era braided two stories — this ridge, and the family's claimed line through
Arabia and Syria — without telling the reader which was which. The `sect()`
waymarks already existed but covered only nine of fourteen chapters. They are now
systematic: **What the ground says** and **And in our own line** in every era, and
from Era Eleven a single merged waymark, *The ground and the line, together*,
because after 1562 there is only one story.

### Era Seven reordered, and a contradiction printed

The chapter ran 324 → 473 → 528 → back to 455 → forward to 563 → back to 543.
Worse, the FIX box inside THE DAM BREAKS ended by pointing at "the next entries,"
which were sixty lines earlier. The line strand now runs **455 → 473 → 528 → 543
→ 563**, with the dateless sovereignty essay last, and Amorkesos moved out of the
land strand where he did not belong.

### New entry — THE DAM CANNOT HAVE SENT THEM NORTH

The book established, from ʿInān 75 and ʿAbadān 1, that Ghassān was a named
people in north-central Arabia by **c. 250**. The dam's first dated breach is
**455**. Both were in print and had never been set side by side. The new entry
does it, tests three ways out, and keeps the third: **the dam is not the cause,
it is the memory** — the dispersal was a drift of centuries, and what the dam
supplied was a date and an image. The migration survives; the mechanism does not.
Printed with a FIX box correcting this book's own previous correction.

### New entry — Riyam 2006-17, twelve lands in the order he crossed them

A third inscription, published 2016 and unknown to earlier editions. A Sabaean
envoy is sent north, comes home, and has the road carved into a dedication to
Taʾlab Riyām: **Asd, Nizār, Tanūkh, Liḥyān, Tadmur, Nabaṭ, Rūmān, Lakhm, Ghassān,
Maʿadd, Ṭayyiʾ, Khaṣaṣat**. New plate. The Azd are stop one; **Ghassān is stop
nine**. The caution is printed too: the list may be a register of lands reached
rather than an ordered march, and the dating is palaeographic.

### New entry — Arce on the limes Arabicus

Qaṣr al-Ḥallābāt: a Roman fort of the *limes* rebuilt as a Ghassanid and monastic
complex and again as an Umayyad palace, three regimes in one set of walls with no
destruction layer. Carries the historiographical point too — the Ghassanid
century fell between classical and Islamic archaeology and nobody dug it. **A gap
in a record is not always an absence in the world.**

### New entry — Walmsley on Pella, Jarash and ʿAmmān

Occupation, markets and church repair running straight through 636. Removes the
objection that the plateau was empty when the tradition puts our people on it —
without pretending it finds anybody of ours.

### Also

- Ghadban (2015) and Aljoumani & Hirschler (2023) are now named files, not just
  citations. The void entry gains **Burhān al-Dīn** — a middling Jerusalem
  scholar of the 1390s whose library survives item by item, a day's walk from
  this ridge and in the exact century our line is silent.


## v5.1 — 21 August 2026

### Ramallah's own people, told through their own scholarship

Three additions, all answering the standing instruction to tell the story through
the people of this place rather than through the people who studied them.

- **A new entry: THE TERRACES.** The staircase hillsides and the corbelled huts
  standing in them, with the count al-Houdalieh and Ghadban made in 2013 — **167
  watchtowers over some 3,000 dunums** in al-Tireh quarter and ʿAin Qinia village
  (*IJAH* 7:5, 509–35). New **Figure: the terraces in section**, with the cutaway
  of a corbelled roof and the three watch seasons of the year. The entry carries
  **no date**, because Ghadban says plainly there is no evidence for when
  Palestinian dry-stone building begins, and a wall that is repaired every year
  has no stratigraphy. It also carries the loss: about **87 per cent** of the
  walls partially collapsed.
- **Jericho re-attributed.** The entry named only Sellin and Watzinger, Garstang,
  Kenyon and Bar-Yosef. Since **1997** the mound has been dug by a joint expedition
  of the **Palestinian Department of Antiquities and Cultural Heritage** and Rome
  «La Sapienza», **Hamdan Taha** and **Lorenzo Nigro** directing, still running
  through the 2019–2023 seasons; their Early Bronze sequence is now the one the
  book follows, and the 2023 UNESCO nomination is named as the Palestinian
  document it is. Printed as a **FIX box**: a correction of attribution, not of
  fact. Kenyon keeps the tower.
- **The Amarna letters rewritten as a labour file.** **EA 365** (Louvre AO 7098)
  quoted in full — Biridiya of Megiddo complaining that he alone furnishes the
  corvée for the fields of Shunama — with the word *massu*, the same *mas* the
  Hebrew Bible uses. The entry says outright that the letter is not about this
  ridge, and quotes it anyway for what it proves about every document in the book:
  *the archive names the mayors; the corvée is everybody else.*

Also: the Philistine arrival is now described as **southern-European-related**
ancestry of unpinned source in the Canaanite entry too, matching the correction
already made in the Iron Age entry.


## v5 — 19 August 2026

### The line recounted at sixty-six

The chart's generation 35 draws 931 years as a single row. At thirty years to a
generation that stretch is **thirty-one** generations, so the line from Adam to
Rāshid is **sixty-six, not thirty-six** — thirty-six of them named, thirty with no
name at all — and about eighteen more to this morning, eighty-four in all. The
ladder in every era strip is drawn on that count and runs the whole way.

Generation **65 is Ṣaqr**, Rāshid's father on the Karak side, drawn in a broken
outline: named by the tradition, named by nobody's clerk. The Mogannam chart's
alternative — Rāshid bin ʿĪsā bin ʿIyād bin Ḍahdūḥa — is printed beside it and
would fill 63–65 instead. Either way the count is sixty-six.

### Two documents that were on our own shelf

- **Ramallah is named in 1186**, not 1279: Guy de Lusignan pledged the village
  against a debt to the German hospital in Jerusalem on 7 March 1186, and Rey
  found *Ramalei* in a manuscript of 1198.
- **1 April 1561** — six men "all of them from the village of Ramallah" swore
  before the qāḍī of Jerusalem to plough this hill and no other until all of it
  was under crop, and the court divided Ramallah in thirds. Three of them are
  Christians this book already tracks through the registers, and one carries the
  road in his own name: Ghunaym bin Sālim **al-Kasbūrī**.

Both from Ḥammūdeh (2014), which this project had been citing for its register
tables and had not read to the end.

### The registers, name by name

John Mogannam's transliterations of Registers 289 and 516 — **109 households and 8
bachelors** — encoded in `src/build_defters.py` and exported to
`data/AFRP_Register_Names_1553_1562.csv`.

**Nineteen of the thirty-six households at Bayt Jālā in 1553 appear again at
Ramallah in 1562 under the same name and the same father.** Not one of the
sixty-three Christian household heads is named Rāshid, and not one is the son of a
Rāshid — which is what it should look like if the movers were his grandchildren.

### The Karak wheel, cited and read properly

Sourced to **Munther Haddadin, دولة الغساسنة؛ أصيلها ورحيلها, Amman: دار ورد
الأردنية, 2024**, plate 84. Two earlier editions reported that no such book
existed and went after the wrong one; that false trail is retracted at full size.
"Warda Books" is دار ورد, the year was one out, and the title was translated
loosely.

Read outward from the hub, the wheel agrees with Ramallah on four points: Ṣabra is
Rāshid's **brother**; the five sons are **Ḥaddād, Ibrāhīm, Jiryis, Shuqayr,
Ḥasan**; the destination is written under his name as رام الله; and his branch
stops there. A previous reading of this book — that the wheel's inner ring held
Rāshid's peers — was this book misreading a chart, and is withdrawn in full.

### Fact-check

Six adversarial passes over the whole book. About fifty corrections, including:
sijill 48 **p. 88** and 29 June 1565; the Ḥaram corpus is the **1390s**;
al-Mundhir arrested **581**; Maʾrib's first dated breach **455**; Jericho **23
km**; Jifnā **seven kilometres due north**; the Sidon Crusader pit held **nine**
men, of whom two were part-European, and the negative result is Lebanese; the
Philistine genome shows **southern-European-related** ancestry, not "Aegean"; the
Shuqba Nubian Levallois association was **rebutted in the same journal in 2022**;
Grant's book is **255 pp.**; the Friends Meetinghouse is **1910**; Miriam Karam
was **fifteen, in 1867**, and stopped **Eli and Sybil** Jones.

Withdrawn for want of a folio: the "twelve fellāḥīn and 950 dirhams" of the Ḥaram
corpus, and the surveyed boundaries, now printed unattributed.

The verdict is de-overstated: **the dynasty this family claims** is named in
contemporary sources; the family's descent from it is not, and the book no longer
implies otherwise.

### The story of Ramallah's people

Miriam Karam now opens the missions century instead of closing it. Dr Philip Asʿad
Maʿlūf — who covered the district alone for twenty-five years, pulled the
twelve-year-old ʿAzīz Shāhīn through typhoid, and died of the typhus he was
treating — gets the headline. Nahda, founded by Ramallah women in 1924, leads.
Khaleel Totah argues Palestine's case for thirty years instead of raising money
for an auditorium. Rabin signed the Lydda order at 13:30 on 12 July 1948. The 1967
count was taken under curfew, and everyone who was abroad lost the right to come
home. Ramallah did not become a capital by accident.

And the family name has a Palestinian and Jordanian literature this book was not
using: **الحدادين is *the blacksmiths***, and Hind Abū al-Shaʿr shows Christian
families of Transjordan specialised in the trade and carry the name still. A trade
name is not a lesser origin than a dynasty. It is a better-documented one.

### Title page

**David Saah, PhD · John Mogannam**, with a credit line for the genealogical
compilation. John's chart stops being an outside source this book audits and
becomes the co-authors' own prior work — which makes the method stricter, not
softer.

## v74 (12 Nov 2026)
- 1706 school grant: Patriarchate documents (Analekta II pp. 307–311, 376–380) quoted; paid yearly, Shāhīn/Cadora say monthly; 1709 school list added.
