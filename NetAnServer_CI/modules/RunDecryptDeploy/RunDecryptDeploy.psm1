Import-Module Logger

$logger = Get-Logger($LoggerNames.Install)
$pstools = (Get-Item $PSScriptRoot ).parent.parent.FullName+"\resources\PSTools"

Function Run-DecryptDeploy{
    param(
        [string] $drive,
        [string] $netAnServerScript, 
        [string] $REMOTE_SERVER,
        [Parameter(Mandatory=$false)][string]$TEST_AD_HOC      
        )

    $session = Start-PSSession $REMOTE_SERVER

    $scriptBlockDecryptDeploy = {          
        param(
            $drive,
            $script
        )
        $rootDrive = $drive+":\"
        $runScript = $rootDrive+$script
        Set-Location "C:\Users\NetAnServer\Desktop\PSTools"
        Start-Process .\PsExec.exe  -ArgumentList "\\localhost -i 0 /accepteula PowerShell -File $runScript -NoExit -wait"  -Wait
    }

    $scriptBlockAdhocDecryptDeploy = {          
        param(
            $drive,
            $script
        )
        $rootDrive = $drive+":\"
        $runScript = $rootDrive+$script
        Set-Location "C:\Users\NetAnServer\Desktop\PSTools"
        Start-Process .\PsExec.exe  -ArgumentList "\\localhost -i 0 /accepteula PowerShell -File $runScript","Ericsson01"  -Wait
    }
    
   
    try {
        #Add PSTools folder to the SUT for. Used to execute the Licence wrapper
        Copy-Item -Path $pstools -Destination \\$REMOTE_SERVER\c$\Users\NetAnServer\Desktop -Recurse -Force
        $logger.logInfo("Starting the execution of the decrypt & deploy script on $($drive):\$($netAnServerScript) ...", $True)
        
        if($TEST_AD_HOC){
            Invoke-Command -Session $session -ScriptBlock  $scriptBlockAdhocDecryptDeploy -ArgumentList $drive,$netAnServerScript -ErrorAction Stop
            $decryptedDeployedCheck = Test-Path -Path \\$REMOTE_SERVER\c$\Ericsson\NetAnServer\StatisticalServices
            Remove-PSSession -Session $session
            return $decryptedDeployedCheck
        }else {
            Invoke-Command -Session $session -ScriptBlock  $scriptBlockDecryptDeploy -ArgumentList $drive,$netAnServerScript -ErrorAction Stop
            $decryptedDeployedCheck = Test-Path -Path \\$REMOTE_SERVER\c$\Ericsson\tmp\Software
            Remove-PSSession -Session $session
            return $decryptedDeployedCheck
        }

 
    } catch {
        $errorMessage = $_.Exception.Message
        $logger.logError($MyInvocation, "Decrypt & deploy Script did not execute successfully: $errorMessage", $True)
        Remove-PSSession -Session $session
        return $False
    }       
            
     Remove-PSSession -Session $session
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