Import-Module C:\netanserver_postinstall_exe\module\Await

Start-AwaitSession
Send-AwaitCommand 'Update-Password -u Consum01'
Start-Sleep 3
Send-AwaitCommand 'Ericsson02'
Start-Sleep 3
Send-AwaitCommand 'Ericsson02'
Start-Sleep 10
Receive-AwaitResponse >> C:\Ericsson\NetAnServer\Logs\userLog.txt
Stop-AwaitSession