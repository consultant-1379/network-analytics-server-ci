Import-Module C:\netanserver_postinstall_exe\module\Await

$CIUSER = "Consum01"

$users = Get-Users

$ciConsumerUser = $users | Where-Object { $_.USERNAME -eq $CIUSER }

if($ciConsumerUser.GROUP -eq "Consumer") {
	Start-AwaitSession
    Send-AwaitCommand 'Remove-User -u Consum01'
	Start-Sleep 6
	Receive-AwaitResponse >> C:\Ericsson\NetAnServer\Logs\userLog.txt
	Stop-AwaitSession
    return "passed"
    
} else {
    return "failed"
}