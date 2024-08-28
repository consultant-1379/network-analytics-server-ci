Import-Module C:\netanserver_postinstall_exe\module\Await

Start-AwaitSession
Send-AwaitCommand 'Add-BusinessAuthor -u BAuthor01'
Start-Sleep 3
Send-AwaitCommand 'BAuthor01'
Start-Sleep 3
Send-AwaitCommand 'BAuthor01'
Start-Sleep 10
Receive-AwaitResponse >> C:\Ericsson\NetAnServer\Logs\userLog.txt
Stop-AwaitSession

$users = Get-Users -all

$ciBusinessUser = $users | Where-Object { $_.USERNAME -eq "BAuthor01" }

if($ciBusinessUser.GROUP -eq "Business Author") {
    return "passed"
} else {
    return "failed"
}