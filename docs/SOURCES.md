# Sources

The library this book is built on is **not in this repository**. Most of it is not
ours to redistribute — published scholarship, archival scans, and a family history
still in copyright.

## What the build actually reads

| path | what it is | required? |
|---|---|---|
| `assets/AFRP_Ramallah_Bibliography_v4.html` | the annotated bibliography, built separately, imported as Appendix A | **yes** |
| `assets/ocr/family_index.json` | index of names in the OCR of Shāhīn (1982) | optional — the build degrades gracefully |
| Natural Earth 10m/50m shapefiles | coastlines, rivers, lakes for the atlas | fetched by `cartopy` on first run |

Everything else — the ninety-odd PDFs cited in the notes — is referenced by
filename in the text (rendered as `code`) so a reader with the library can find
the file, and is never opened by the build.

## The principal texts

- **ʿAzīz Shāhīn**, كشف النقاب عن تاريخ رام الله والأنساب (1982), 894 pp. — OCR'd
  in full for this project; the English edition read complete.
- **John Mogannam**, *The Ramallah Family Tree Book* — the chart of thirty-six
  named generations, and the English transliterations of the Ottoman registers of
  1553 and 1562 (ch. 4, charts 1–4).
- **Sameeh Hammoudeh**, "New Light on Ramallah's Origins in the Ottoman Period,"
  *Jerusalem Quarterly* 59 (2014), 37–52.
- **Yūsuf Jiryis Qaddūra**, تاريخ رام الله (al-Hudā Press, New York, 1954).
- **Khalīl Abū Rayya**, رام الله قديماً وحديثاً (1980).
- **Muṣṭafā Murād al-Dabbāgh**, القبائل العربية وسلائلها في بلادنا فلسطين (1979).
- **Munther Haddadin**, دولة الغساسنة؛ أصيلها ورحيلها (Amman: دار ورد الأردنية,
  2024), ISBN 978-9923-76-975-1 — the source of the Karak wheel, plate 84.
- **Hütteroth & Abdulfattah**, *Historical Geography of Palestine, Transjordan and
  Southern Syria in the Late 16th Century* (1977).
- **Elihu Grant**, *The Peasantry of Palestine* (Boston: Pilgrim Press, 1907).

## Palestinian scholarship the book cites as the source

Not a complete list — these are the works the book leans on where a foreign
account of the same ground exists and was passed over for them.

- **Salah Hussein al-Houdalieh** (al-Quds University) — the excavation of Khirbet
  et-Tireh, two kilometres from the town centre: *Archaeological Discovery* 4:1
  (2016), 48–67; *JEMAHS* 2:3 (2014), 188–208; the oil press in *Jerusalem
  Quarterly* 62 (2015), 84–97.
- **Al-Houdalieh & Shadi S. Ghadban** (Birzeit), "Agricultural Watchtowers in
  Al-Tireh Quarter and ʿAin Qinia Village, Ramallah, Palestine," *International
  Journal of Architectural Heritage* **7:5 (2013), 509–535**, DOI
  10.1080/15583058.2011.654049 — the survey that counted **167 towers over some
  3,000 dunums**.
- **Shadi Ghadban**, "Palestinian Dry Stone Structures — An Endogenous Expression
  of Cultural Landscape," *Journal "Sustainable Development, Culture, Traditions"*
  1b (2015), 34–46; and "The Architecture of the Palestinian Dry-Stone Hut —
  Al-mantarah," *JCCS-A* 6 (2012), 16–25.
- **Hamdan Taha** (Department of Antiquities and Cultural Heritage, Ministry of
  Tourism and Antiquities) with **Lorenzo Nigro** (Rome «La Sapienza») and, in the
  first seasons, **Nicolò Marchetti** — the Italian–Palestinian Expedition to Tell
  es-Sultan, from 1997 to the 2019–2023 seasons. Also Taha's own account of the
  site in *This Week in Palestine*.
- **Nur Masalha**, **Hamdan Taha at ʿAbūd**, and the Ottoman register
  transliterations of **John Mogannam**, are cited throughout.

## Rights

The text of the book is the authors'. The register facsimiles, the published
scholarship quoted in the notes, and the Karak wheel are their own rights-holders'
and are cited, not reproduced, except where quotation is fair.

The repository carries an **MIT licence**, which covers the code — the builders,
the cartography, the QA suite. It does not and cannot cover the sources quoted in
the notes, and it is not a grant of rights over the book's text.
