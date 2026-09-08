$ErrorActionPreference = 'Continue'
$env:GIT_TERMINAL_PROMPT = '0'
$root = $PSScriptRoot
$log  = Join-Path $root 'push_log.txt'
Set-Location -Path $root

function L([string]$m) { $m | Out-File -FilePath $log -Append -Encoding utf8 }
function Run([string]$label, [string[]]$a) {
    L ''; L "--- $label : git $($a -join ' ') ---"
    try { L ((& git @a 2>&1 | Out-String).TrimEnd()); L "exit code: $LASTEXITCODE" }
    catch { L "EXCEPTION: $($_.Exception.Message)" }
}

"=== AFRP cleanup push $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ===" | Out-File -FilePath $log -Encoding utf8
Run 'untrack log' @('rm','--cached','-q','--ignore-unmatch','push_log.txt')
Run 'add'         @('add','-A')
Run 'status'      @('status','--porcelain=v1')
Run 'commit'      @('commit','-F','commit_msg.txt')
Run 'push'        @('push','origin','main')
L ''; L '--- refs after ---'
try { L ("local : " + (Get-Content (Join-Path $root '.git\refs\heads\main') -Raw).Trim()) } catch { L 'local : (unreadable)' }
try { L ("remote: " + (Get-Content (Join-Path $root '.git\refs\remotes\origin\main') -Raw).Trim()) } catch { L 'remote: (unreadable)' }
L ''; L '=== done ==='
