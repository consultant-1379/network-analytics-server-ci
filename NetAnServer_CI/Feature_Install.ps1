Import-Module C:\netanserver_postinstall_exe\module\Await

try{
	$feature = $args[0]
	
	Start-AwaitSession
	if($feature -like "*pm*"){
		$datasource = "1"
	}else{
		$datasource = "2"
	}
	
	$INSTALL_FEATURE = "Install-Feature -Force $feature"
	Send-AwaitCommand "$INSTALL_FEATURE"
	start-sleep 15
	Send-AwaitCommand "$datasource"
	start-sleep 5
	Send-AwaitCommand y
	start-Sleep 180
	Receive-AwaitResponse
	Send-AwaitCommand 'Exit'
} catch {
        $errorMessage = $_.Exception.Message
		write-host $errorMessage
}finally{
        Stop-AwaitSession
}