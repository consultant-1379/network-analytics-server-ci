Import-Module C:\netanserver_postinstall_exe\module\Await

Start-AwaitSession
Send-AwaitCommand 'Invoke-PromoteUserToGroup -u Consum01 -BusinessAuthor'
Start-Sleep 6
Receive-AwaitResponse >> C:\Ericsson\NetAnServer\Logs\userLog.txt
Stop-AwaitSession

$users = Get-Users -all

$ciBusinessUser = $users | Where-Object { $_.USERNAME -eq "Consum01" }

if($ciBusinessUser.GROUP -eq "Business Author") {
    return "passed"
} else {
    return "failed"
}