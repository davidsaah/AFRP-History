# ─────────────────────────────────────────────────────────────────────
#  AFRP-History — stage everything, commit, push to GitHub
#  Double-click RUN_ME_push_to_github.bat, or:
#     powershell -ExecutionPolicy Bypass -File .\push.ps1
# ─────────────────────────────────────────────────────────────────────
$ErrorActionPreference = 'Stop'
$repo = 'C:\Users\David\Projects\AFRP-History'
Set-Location $repo
Write-Host "`n=== repo: $repo ===" -ForegroundColor Cyan

if (-not (Test-Path (Join-Path $repo '.git'))) {
    git init; git branch -M main
    git remote add origin https://github.com/davidsaah/AFRP-History.git
}
if (-not (git config user.name))  { git config user.name  'David Saah' }
if (-not (git config user.email)) { git config user.email 'davidsaah@gmail.com' }
if (-not (git remote get-url origin 2>$null)) {
    git remote add origin https://github.com/davidsaah/AFRP-History.git
}
Write-Host "remote: $(git remote get-url origin)"

Write-Host "`n=== changes about to be committed ===" -ForegroundColor Cyan
git status --short

git add -A

$msg = @"
v5.3 - the two strands, the dam, and the Haram search

THE BOOK  (34 figures, 178 notes, 1,702,555 bytes)

Structure
- Every era now says which strand it is in. The sect() waymarks covered
  nine chapters of fourteen and are now systematic: "What the ground says"
  and "And in our own line" throughout, merging from Era Eleven into "The
  ground and the line, together" - because after 1562 there is one story.
- Era Seven reordered. It ran 324 -> 473 -> 528 -> back to 455 -> 563 ->
  back to 543, and the FIX box inside THE DAM BREAKS pointed forward at
  entries sixty lines earlier. The line strand now runs 455, 473, 528,
  543, 563, with the dateless sovereignty essay last.

New entries
- THE DAM CANNOT HAVE SENT THEM NORTH. Ghassan is attested in the north
  by c. 250 (Inan 75, Abadan 1); the dam first breaches in 455. Both were
  in print and had never been set side by side. Three ways out are tested;
  the third is kept: the dam is not the cause, it is the memory. The
  migration survives, the mechanism does not. Corrects this book's own
  previous correction.
- A MAN WALKED THIS ROAD AND HAD IT CARVED. Riyam 2006-17, published 2016:
  a Sabaean envoy lists the twelve lands he crossed - Asd, Nizar, Tanukh,
  Lihyan, Tadmur, Nabat, Ruman, Lakhm, Ghassan, Ma'add, Tayyi', Khasasat.
  New plate. The Azd are stop one; Ghassan is stop nine.
- WHAT THEY LEFT. Arce on Qasr al-Hallabat: a Roman fort of the limes
  rebuilt as a Ghassanid hall and again as an Umayyad palace, three
  regimes in one set of walls. A gap in a record is not always an absence
  in the world.
- THE TOWNS DO NOT DIE. Walmsley on Pella, Jarash and Amman, 550-750.
- ONE CHRISTIAN, ONE DEBT. Text #922/4, 7 Safar 776 / late July 1374:
  Ni'ma ibn Bishara al-Nasrani buys cotton on credit, 218 dirhams at six
  a week, two witnesses, later struck through. With the whole negative
  Haram search printed.
- THE TERRACES. 167 watchtowers over some 3,000 dunums in al-Tireh and
  'Ain Qinia (al-Houdalieh & Ghadban 2013). New plate. No date, because
  a wall repaired every year has no stratigraphy.

Corrections
- "Men of Jifna in the Haram registers in 1374" was one man, and the
  village is a queried reading - the scribe's Jifna al-Jawz? Demoted to
  evidence about the century, not this district. FIX box.
- Jericho re-attributed to the Palestinian-Italian expedition (MOTA-DACH
  with Rome La Sapienza, Hamdan Taha and Lorenzo Nigro, from 1997). FIX
  box. Kenyon keeps the tower.
- The Amarna letters retold as a labour file through EA 365.
- Philistine arrival now southern-European-related throughout.

THE SEARCH
- The Haram al-Sharif corpus was searched. McGill's microfilm OCR is
  stroke-noise: in 310,000 characters of recognised Arabic from a
  Jerusalem religious archive, al-Quds, al-Haram, al-Sharif and qarya
  occur zero times. The published catalogue was searched instead; the
  ridge villages appear twice in the whole of it.

INFRASTRUCTURE
- Mobile and GitHub Pages: responsive figure scrolling, content-visibility,
  scroll-behavior fix under 760px, atlas path precision cut. First load
  1.42s -> 0.43s. index.html landing page, .nojekyll.
- docs/: CHANGELOG, OPEN_QUESTIONS (Ankara closed on paper - the eighty
  named heads of 1596-97 are printed in al-Furqan vol. 6), SOURCES.
"@

git commit -m $msg

Write-Host "`n=== pushing ===" -ForegroundColor Cyan
if (git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>$null) { git push } else { git push -u origin main }

Write-Host "`nDone. https://github.com/davidsaah/AFRP-History" -ForegroundColor Green
Write-Host "Next: Settings -> Pages -> Deploy from branch -> main -> / (root)."
Write-Host "The site will be https://davidsaah.github.io/AFRP-History/"
Read-Host "`nPress Enter to close"
