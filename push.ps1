# ─────────────────────────────────────────────────────────────────────
#  AFRP-History — stage everything, commit, push to GitHub
#  Run:  right-click → Run with PowerShell
#     or:  powershell -ExecutionPolicy Bypass -File .\push.ps1
# ─────────────────────────────────────────────────────────────────────
$ErrorActionPreference = 'Stop'
$repo = 'C:\Users\David\Projects\AFRP-History'

Set-Location $repo
Write-Host "`n=== repo: $repo ===" -ForegroundColor Cyan

# 0. sanity
if (-not (Test-Path (Join-Path $repo '.git'))) {
    Write-Host "No .git here. Initialising and wiring the remote..." -ForegroundColor Yellow
    git init
    git branch -M main
    git remote add origin https://github.com/davidsaah/AFRP-History.git
}

# 1. who is committing
if (-not (git config user.name))  { git config user.name  'David Saah' }
if (-not (git config user.email)) { git config user.email 'davidsaah@gmail.com' }

# 2. make sure the remote is right
$remote = (git remote get-url origin 2>$null)
if (-not $remote) { git remote add origin https://github.com/davidsaah/AFRP-History.git }
Write-Host "remote: $(git remote get-url origin)"

# 3. what is about to go in
Write-Host "`n=== changes ===" -ForegroundColor Cyan
git status --short

# 4. stage and commit
git add -A

$msg = @"
v5.1 - Ramallah's own people, and the mobile/Pages build

The book
- New entry: THE TERRACES. The dry-stone staircase hillsides and the corbelled
  huts standing in them, with al-Houdalieh & Ghadban's 2013 count: 167
  watchtowers over some 3,000 dunums in al-Tireh quarter and 'Ain Qinia
  village (IJAH 7:5, 509-535). New plate: the hillside in section, a cutaway
  of the corbelled roof, and the three watch seasons. The entry carries no
  date - there is no evidence for when Palestinian dry-stone building begins,
  and a wall repaired every year has no stratigraphy.
- Jericho re-attributed. Since 1997 Tell es-Sultan has been dug by the
  Palestinian Department of Antiquities and Cultural Heritage with Rome
  La Sapienza, Hamdan Taha and Lorenzo Nigro directing, through the 2019-2023
  seasons. Their Early Bronze sequence is now the one the book follows and
  the 2023 UNESCO nomination is named as the Palestinian document it is.
  Printed as a FIX box: a correction of attribution, not of fact.
- The Amarna letters rewritten as a labour file. EA 365 (Louvre AO 7098)
  quoted in full - Biridiya of Megiddo furnishing the corvee for Shunama -
  with massu, the same mas the Hebrew Bible uses.
- Philistine arrival described as southern-European-related throughout.

Earlier, uncommitted
- Era Six entry: WERE THE GHASSANIDS SOVEREIGN - and why it is being asked.
- The 1948 al-Khuri monograph read: it calls the Ghassanid descent zaam in
  its first sentence and prints where its own chain breaks. Verdict box
  rewritten around it. The modern claimant is named nowhere in the book.
- Mobile and GitHub Pages: responsive figure scrolling, content-visibility,
  scroll-behavior fix under 760px; atlas path precision cut; index.html
  landing page; .nojekyll. First load 1.42s -> 0.43s.
- New literature reviewed: 35 files manifested, renamed, and 20 claim-related
  items separated out. None fills a line.
- docs/: CHANGELOG, OPEN_QUESTIONS and SOURCES brought up to date.
"@

git commit -m $msg

# 5. push
Write-Host "`n=== pushing ===" -ForegroundColor Cyan
$hasUpstream = (git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>$null)
if ($hasUpstream) { git push } else { git push -u origin main }

Write-Host "`nDone. https://github.com/davidsaah/AFRP-History" -ForegroundColor Green
Write-Host "If a browser or device-code prompt appears, that is GitHub asking you to sign in - approve it and the push finishes."
Write-Host "`nNext: Settings -> Pages -> Deploy from branch -> main -> / (root)."
Write-Host "The site will be https://davidsaah.github.io/AFRP-History/"
Read-Host "`nPress Enter to close"
