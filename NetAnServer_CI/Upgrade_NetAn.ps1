Import-Module C:\netanserver_postinstall_exe\module\Await

try{
	$serv = $args[0]
	
	Start-AwaitSession

	$ADMIN_USER_NAME = "Administrator"
	$ADMIN_PASSWORD = "Ericsson01"
	$CORRECT_PASSWORD = "Ericsson01"
	$CERT_PASSWORD = "Ericsson01"
	$INSTALL_SCRIPT = "C:\Ericsson\tmp\Scripts\Install\NetAnServer_upgrade.ps1"
	Send-AwaitCommand "$INSTALL_SCRIPT"
	start-sleep 2
	Send-AwaitCommand "$serv"
	start-sleep 5
	Send-AwaitCommand "$ADMIN_USER_NAME"
	start-sleep 5
	Send-AwaitCommand "$ADMIN_PASSWORD"
	start-sleep 5
	Send-AwaitCommand "$ADMIN_PASSWORD"
	start-sleep 2
	Send-AwaitCommand "$CORRECT_PASSWORD"
	Send-AwaitCommand "$CORRECT_PASSWORD"
	start-sleep 2
	Send-AwaitCommand "$CERT_PASSWORD"
	Send-AwaitCommand "$CERT_PASSWORD"
	start-sleep 2
	Send-AwaitCommand y
	start-Sleep 2
	start-sleep 900
	Receive-AwaitResponse
	Send-AwaitCommand 'Exit'
} catch {
        $errorMessage = $_.Exception.Message
		write-host $errorMessage
}finally{
        Stop-AwaitSession
}
