Import-Module C:\netanserver_postinstall_exe\module\Await

Start-AwaitSession
Send-AwaitCommand 'Add-ConsumerUser -u Consum01'
Start-Sleep 3
Send-AwaitCommand 'Ericsson01'
Start-Sleep 3
Send-AwaitCommand 'Ericsson01'
Start-Sleep 10
Receive-AwaitResponse > C:\Ericsson\NetAnServer\Logs\userLog.txt
Stop-AwaitSession

$users = Get-Users

$ciConsumerUser = $users | Where-Object { $_.USERNAME -eq 'Consum01' }

if($ciConsumerUser.GROUP -eq "Consumer") {
    return "passed"   
} else {
    return "failed"
}