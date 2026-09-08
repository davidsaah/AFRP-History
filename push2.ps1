$ErrorActionPreference = 'Continue'
$env:GIT_TERMINAL_PROMPT = '0'
$root = $PSScriptRoot
$log  = Join-Path $root 'push_log.txt'

function L([string]$m) { $m | Out-File -FilePath $log -Append -Encoding utf8 }
function Run([string]$label, [string[]]$gitArgs) {
    L ''
    L "--- $label : git $($gitArgs -join ' ') ---"
    try {
        $out = & git @gitArgs 2>&1 | Out-String
        L $out.TrimEnd()
        L "exit code: $LASTEXITCODE"
    } catch {
        L "EXCEPTION: $($_.Exception.Message)"
    }
}

"=== AFRP push run $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ===" | Out-File -FilePath $log -Encoding utf8
try { Set-Location -Path $root; L "cwd: $((Get-Location).Path)" } catch { L "SET-LOCATION FAILED: $($_.Exception.Message)" }

L ''
L '--- git --version ---'
try { L ((& git --version 2>&1 | Out-String).TrimEnd()) } catch { L "GIT NOT FOUND: $($_.Exception.Message)" }

Run 'status'   @('status','--porcelain=v1')
Run 'remote'   @('remote','-v')
Run 'user'     @('config','--get','user.name')
Run 'email'    @('config','--get','user.email')
Run 'add'      @('add','-A')
Run 'commit'   @('commit','-F','commit_msg.txt')
Run 'push'     @('push','origin','main')

L ''
L '--- refs after ---'
try { L ("local : " + (Get-Content (Join-Path $root '.git\refs\heads\main') -Raw).Trim()) } catch { L "local : (unreadable)" }
try { L ("remote: " + (Get-Content (Join-Path $root '.git\refs\remotes\origin\main') -Raw).Trim()) } catch { L "remote: (unreadable)" }
L ''
L '=== done ==='
