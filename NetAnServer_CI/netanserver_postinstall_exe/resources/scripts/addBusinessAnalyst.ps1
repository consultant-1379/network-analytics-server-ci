Import-Module C:\netanserver_postinstall_exe\module\Await

Start-AwaitSession
Send-AwaitCommand 'Add-BusinessAnalyst -u BAnalyst01'
Start-Sleep 3
Send-AwaitCommand 'BAnalyst01'
Start-Sleep 3
Send-AwaitCommand 'BAnalyst01'
Start-Sleep 10
Receive-AwaitResponse >> C:\Ericsson\NetAnServer\Logs\userLog.txt
Stop-AwaitSession

$users = Get-Users -all

$ciBusinessUser = $users | Where-Object { $_.USERNAME -eq "BAnalyst01" }

if($ciBusinessUser.GROUP -eq "Business Analyst") {
    return "passed"
} else {
    return "failed"
}