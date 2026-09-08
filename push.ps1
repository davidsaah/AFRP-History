# AFRP-History — push to GitHub
#
# NOTE: ErrorActionPreference is deliberately 'Continue', NOT 'Stop'.
# git writes ordinary progress and CRLF warnings to stderr, and under 'Stop'
# PowerShell treats native stderr as a terminating error and kills the script
# before it reaches `git commit`. That is what silently broke this file before
# 8 September 2026 — it looked like it ran, and committed nothing.
$ErrorActionPreference = 'Continue'
$env:GIT_TERMINAL_PROMPT = '0'
Set-Location -Path $PSScriptRoot

# The commit message lives in commit_msg.txt so nothing has to survive
# PowerShell here-string quoting. Edit that file, not this one.
if (-not (Test-Path 'commit_msg.txt')) {
    Write-Host "commit_msg.txt is missing — write the commit message there first." -ForegroundColor Red
    Read-Host "Press Enter to close"; exit 1
}

git add -A
git commit -F commit_msg.txt
git push origin main

Write-Host ""
Write-Host "Local and remote refs — these must match:" -ForegroundColor Green
Get-Content .git\refs\heads\main
Get-Content .git\refs\remotes\origin\main
Write-Host ""
Write-Host "Do NOT verify by loading the GitHub web page; it has served stale data on this repo." -ForegroundColor Yellow
Read-Host "Press Enter to close"
