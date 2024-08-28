Import-Module Logger
Import-Module Await

$logger = Get-Logger($LoggerNames.Install)

function Install-Feature() {
    param(
        [string] $remoteServer,
        [string] $remoteFeature,
        [string] $datasource
    )

    try {
            Start-AwaitSession
            $logger.logInfo("Attempting to establish remote session", $True) 
            $logger.logInfo("Enter-PSSession -ComputerName '$remoteServer'", $True) 
            Send-AwaitCommand "Enter-PSSession -ComputerName '$remoteServer'"
            start-sleep 2
            $logger.logInfo("Install-Feature $($remoteFeature)", $True) 
            Send-AwaitCommand "Install-Feature $($remoteFeature)"
            start-Sleep 10
            $logger.logInfo("using datasource $datasource", $True) 
            Send-AwaitCommand "$datasource"
            start-sleep 10
            Send-AwaitCommand "y"
            start-sleep 30
    } catch {
        $errorMessage = $_.Exception.Message
        $logger.logError($MyInvocation, "Installation of feature did not execute successfully: $errorMessage", $True)
        return $false
    } finally {
        Stop-AwaitSession
    }       
  return $true
} 