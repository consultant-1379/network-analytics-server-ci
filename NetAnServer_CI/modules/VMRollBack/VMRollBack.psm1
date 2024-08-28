
Import-Module Logger


$logger = Get-Logger($LoggerNames.Install)


Function Reset-VM {
    param(
        [string] $xmlFile,
        [string] $virtualCentre,
        [string] $virtualMachine,
        [string] $snapShotName
        )

    $logger.logInfo("Creating user credentials from file $xmlFile")
    $credentials = Get-VICredentialStoreItem -Host $virtualCentre -File $xmlFile
        
    ###
    ### Connect to Virtual Centre
    ###
    try {   
        $logger.logInfo("Attempting to connect to Virtual Centre $virtualCentre", $True)
        Connect-VIServer $virtualCentre -User $credentials.User -Password $credentials.Password -ErrorAction Stop -WarningAction SilentlyContinue
        $logger.logInfo("Successfully connected to Virtual Centre $virtualCentre", $True)
    } catch {
        $errorMessage = $_.Exception.Message
        $logger.logError($MyInvocation, "Could not connect to Virtual Centre $virtualCentre. `n $errorMessage", $True)
        return $False
    }

    ###
    ### Get the VM
    ###
    try {
        $logger.logInfo("Checking if VM $virtualMachine exists in VC $virtualCentre", $True)
        $targetVM = Get-VM $virtualMachine -ErrorAction Stop
        $logger.logInfo("VM $virtualMachine found in $virtualCentre", $True)
    } catch {
        $errorMessage = $_.Exception.Message
        $logger.logError($MyInvocation, "Could not find VM $virtualCentre in Virtual Centre $virtualCentre. `n $errorMessage", $True)
        disconnectFromVirtualCentre
        return $False
    }

    ###
    ### Find SnapShot
    ###
    try {
        $logger.logInfo("Attempting to find snapshot $snapShotName", $True)
        $restoreSnapshot = Get-Snapshot $snapShotName -VM $targetVM -ErrorAction Stop
        $logger.logInfo("Snapshot $snapShotName found", $True)
    } catch {
        $errorMessage = $_.Exception.Message
        $logger.logError($MyInvocation, "Could not find snapshot $snapShotName for VM $targetVM. `n $errorMessage", $True)
        disconnectFromVirtualCentre
        return $False
    }
    
    ###
    ### Start Rollback
    ###
    try {
        $logger.logInfo("Attempting to roll back $targetVM to snapshot $snapShotName", $True)
        Set-VM -VM $targetVM -Snapshot $restoreSnapshot -Confirm:$False -ErrorAction Stop
        $logger.logInfo("Roll back $targetVM to snapshot $snapShotName completed", $True)
    } catch {
        $errorMessage = $_.Exception.Message
        $logger.logError($MyInvocation, "Roll back to snapshot $snapShotName for VM $targetVM failed. `n $errorMessage", $True)
        disconnectFromVirtualCentre
        return $False
    }

    disconnectFromVirtualCentre
    $logger.logInfo("Exiting VM Rollback. Returning $True", $True)
    return $True
}

Function disconnectFromVirtualCentre {
    $logger.logInfo("Disconnecting from Virtual Centre $virtualCentre", $True)
    Disconnect-VIServer $virtualCentre -Confirm:$False
    $logger.logInfo("Disconnected successfully from Virtual Centre $virtualCentre", $True)
}


Export-ModuleMember -Function "Reset-VM"