# AFRP-History

## The One Line — The Ramallah Family

**David Saah, PhD · John Mogannam**

The whole history of the Ramallah family as a single unbroken timeline — from Adam
and Eve to today, with the evidence attached at every date. Compiled for the
American Federation of Ramallah, Palestine.

This repository builds the book. It is not a document with a build script bolted
on; the book *is* the program's output, and every figure, map, chart, citation and
correction in it is generated from source at build time.

```bash
python build.py          # → out/AFRP_The_One_Line_v5.html
```

The build is deterministic: the same sources produce byte-identical HTML.

---

## What is in the book

**Sixty-six generations from Adam to Rāshid al-Ḥaddādīn, thirty-six of them named,
thirty with no name at all** — then about eighteen more to this morning. It runs as
one chronological line through fourteen eras of Palestinian history, and the
family's own chain of nine links is threaded through it, era by era, saying at
each point which link we have reached and what evidence there is for it. Often
the honest answer is *none*, and the book says so.

- **32 figures**, all generated: Lambert conformal conic maps drawn from Natural
  Earth, the generational ladder, the register comparison, the evidence chain.
- **154 numbered notes**, renumbered into document order at build time.
- **A test harness**: thirty-six checkable claims from the family's own
  presentation, each with a verdict, so the audit can be re-run by anyone.
- **Corrections printed in the open**, at the same size as the claims they
  replace, with the superseded reading quoted.

---

## Layout

```
build.py              the entry point
src/
  paths.py            where everything lives
  build_v5.py         the book: entries, eras, assembly, CSS
  build_recon.py      the base figure library and GENS (the chart's 36 rows)
  build_figs2.py      the void, the diaspora, the population plates
  build_figs3.py      the chain of nine links, the town plan, the Azd dispersal
  build_figs4.py      the deep past, the branch at Eber, the ladder,
                      the Karak wheel, the register comparison
  build_atlas.py      the cartography — Sheet, fit_box, Sutherland–Hodgman clip
  build_timeline_test.py  the test harness
  build_defters.py    the 1553 and 1562 register names, encoded
assets/               inputs the build reads (the bibliography, the OCR index)
data/                 machine-readable outputs (the register names as CSV)
out/                  the built book
qa/                   the QA suite
docs/                 method, changelog, open questions
```

## The QA suite

```bash
python qa/qa_final.py    # overflow at 1280/900/420, page errors, broken anchors
python qa/qa_ov.py       # text-overlap detection inside every figure
python qa/qa_cover.py    # text painted over by a later opaque shape
```

`qa_ov.py` walks every `<text>` node in all 32 figures, takes its `getBBox()`, and
reports any two that overlap. It should print `[]`.

---

## Method

Four standing rules, set out in full in [docs/METHOD.md](docs/METHOD.md):

1. **The co-authors' own chart is a guide, not a source.** A chart cannot be its
   own evidence, least of all when the people printing it drew it. Every
   correction to it in this book is a self-correction.
2. **Palestinian and Arab scholarship first.** Eastern sources are cited as the
   source; Western editors are cited as the route.
3. **Print uncertainty rather than smooth it.** Where the record corrects the
   family, the correction appears in a marked box at the date where it happens.
4. **Cite everything** — author, work, year, page, DOI or URL.

---

## Sources

The library this book is built on — some ninety PDFs of primary and secondary
sources, the Ottoman register facsimiles, and the OCR of ʿAzīz Shāhīn's
*Kashf al-Niqāb* (1982) — is **not in this repository**. Most of it is not ours to
redistribute. `docs/SOURCES.md` lists what the build expects and where it came
from.

## Contributing

Corrections are the point. If you can show that something here is wrong, open an
issue with the source — author, work, year, page. The book is designed to absorb
that: it prints its own retractions.

Open questions are in [docs/OPEN_QUESTIONS.md](docs/OPEN_QUESTIONS.md). The two
that matter most both need somebody in a Turkish archive.

---

## Licence

The **code** in this repository is MIT — see [LICENSE](LICENSE).

The **book** is the authors'. The sources quoted in its notes — published
scholarship, the Ottoman register facsimiles, the Karak wheel — belong to their
own rights-holders and are cited, not redistributed. See
[docs/SOURCES.md](docs/SOURCES.md).
