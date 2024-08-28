Import-Module Logger
Import-Module Await


$logger = Get-Logger($LoggerNames.Install)

Function Mount-ISO{
       param(
        [string] $ISOLocation,
        [string] $REMOTE_SERVER
       
        )
    $remoteDestination = "\\$REMOTE_SERVER"+"\"+$ISOLocation.Replace(":", "$")
    $logger.logInfo("Starting mount of ISO in following directory $remoteDestination", $True)  
    $logger.logInfo("Testing that  $remoteDestination exists", $True)  
    
    if(-not (Test-Path($remoteDestination))){
        $logger.logError($MyInvocation, "Cannot Locate  $remoteDestination", $True)
        return $False
    }
    
    $logger.logInfo("$remoteDestination exists", $True)      
    $ISOImage = get-childitem  $remoteDestination | where {$_.extension -eq ".iso"}
        
    if(-not $ISOImage){
        $logger.logError($MyInvocation, "No ISO exists at $remoteDestination", $True)
        return $False  
    }
        
    $logger.logInfo("Found ISO: $ISOImage", $True) 
              
    $session = Start-PSSession $REMOTE_SERVER
               
    $ScriptBlockMount = {     
             $path = $args[0]      
             $before = (Get-Volume).DriveLetter
             $mountResult = Mount-DiskImage -ImagePath $path -StorageType ISO -Passthru
             $after = (Get-Volume).DriveLetter
             $Drive = Compare $before $after -Passthru
             return $Drive                 
        }
                 
    try {
        $logger.logInfo("Attempting to Mount ISO from $ISOLocation$ISOImage", $True) 
        $drive = Invoke-Command -Session $session -ScriptBlock $ScriptBlockMount -ArgumentList "$ISOLocation$ISOImage" -ErrorAction Stop
        $logger.logInfo("ISO Mounted on:  $Drive drive ", $True)
    }catch{
        $errorMessage = $_.Exception.Message
        $logger.logError($MyInvocation," Error mounting ISO:  $errorMessage ", $True)
        Remove-PSSession -Session $session
        return $False
    }

    Remove-PSSession -Session $session
    return $Drive  
}


Function Run-Install{
    param(
        [string] $REMOTE_SERVER       
        )

    try{
        Start-AwaitSession
        
        $ADMIN_USER_NAME = "NetAnServer02"
        $ADMIN_PASSWORD = "Ericsson02"
        $CORRECT_PASSWORD = "Ericsson01"
        $CERT_PASSWORD = "Abcde01!"
        $INSTALL_SCRIPT = ".\tmp\Scripts\Install\NetAnServer_install.ps1"
        $logger.logInfo("Attempting to establish remote session", $True) 
        Send-AwaitCommand "Enter-PSSession -ComputerName '$REMOTE_SERVER'"
        start-sleep 2
        Send-AwaitCommand "cd C:\Ericsson\"
        start-Sleep 3
        $logger.logInfo("Starting the Install of NetAnServer .", $True) 
        Send-AwaitCommand "$INSTALL_SCRIPT"
        start-sleep 5
        Send-AwaitCommand "$CORRECT_PASSWORD"
        Send-AwaitCommand "$CORRECT_PASSWORD"
        start-sleep 2
        Send-AwaitCommand "$ADMIN_USER_NAME"
        Send-AwaitCommand "$ADMIN_PASSWORD"
        start-sleep 2
        Send-AwaitCommand "$CERT_PASSWORD"
        start-sleep 2
        Send-AwaitCommand y
        start-Sleep 2
        $output = (Receive-AwaitResponse)
        $logger.logInfo("Installation in progress...sleeping for 900 seconds...", $True)
        start-sleep 900
        Send-AwaitCommand 'Exit'
       

    } catch {
        $errorMessage = $_.Exception.Message
        $logger.logError($MyInvocation, "Install Script did not execute successfully: $errorMessage", $True)
        return $false
    }

   finally{
        Stop-AwaitSession
    }
       
  return $true
}

Function Start-PSSession {
     param(           
          [string] $REMOTE_SERVER       
           )

     try { 
          $logger.logInfo("Attempting to establish remote session", $True) 
          $session = New-PSSession $REMOTE_SERVER -ErrorAction Stop
          $logger.logInfo("Remote session established $session ", $True)
          return $session
    } catch {
          $errorMessage = $_.Exception.Message
          $logger.logError($MyInvocation,"Error establishing Remote Session:  $errorMessage ", $True)
          return $null
    }

}