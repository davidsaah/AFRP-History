$ErrorActionPreference = 'Stop'
Set-Location -Path $PSScriptRoot
$msg = @'
v5.7 — the open questions worked through; fourteen closed

Corrects v5.6 within a day. Robinson & Smith (1841, III.78-79) read directly:
the received account of the Jifna deportation is wrong, including in this book.
Twenty-six men were taken to Egypt and PUT INTO THE PUBLIC WORKS, not exiled;
Robinson gives no motive; and ONE of the village's two priests followed them
later and died there. The error is a misparse of "one of their two priests."

Also: Jifna lay in the northern Bani Harith, whose shaykh Isma'il Simhan was
executed in 1834 — which is why the village was punished. Bayt Jala, 31 May
1834, 33 Christian men and women killed on suspicion of looting. The Bethlehem
Muslim-quarter destruction withdrawn pending a page.

The Samhan nahiya question dissolved: Bani Harith was bipartite, and the
circulating table cites a Doumani page that carries no such table. Ramallah sat
in Jabal al-Quds, not as a seat.

The eighth bachelor found: Hammudeh reads 63 households + 8 bachelors, the
family transcription 64 + 7, both totalling 71 Christian entries.

The Federation has three founding dates because it has three foundings: the
magazine 1952, the constituting convention 7 Sept 1959, IRS recognition Aug 1963.

Ramallah's Muslim majority dated: 6,966 Christians of 12,134 in 1967 (57%), 32%
by 1997, no census in between. Flagged as an Israeli state source on the page.

Khirbet et-Tireh's 749 abandonment withdrawn — al-Houdalieh says continuous use
Byzantine to late Ottoman. The oil press added: direct screw, four beds.

Riwaq's registry: 381 historic buildings at Ramallah, 168 at al-Bira.

38 figures, 223 notes. QA clean.
'@
git add -A
git commit -m $msg
git push origin main
Write-Host ""
Write-Host "Pushed. Local and remote refs:" -ForegroundColor Green
Get-Content .git\refs\heads\main
Get-Content .git\refs\remotes\origin\main
Read-Host "Press Enter to close"
