
$logger = Get-Logger($LoggerNames.Install)

function Get-Media {
    param(
        [string] $mediaBuildDir,      
        [string] $logsDir,       
        [string] $remoteDownloadLocation,   
        [string] $REMOTE_SERVER, 
        [string] $mvnLogFileName
        )

    $currentLocation = Get-Location

    $logger.logInfo("Testing that media directory $mediaBuildDir exists", $True)  
 
    if (-not (Test-Path $mediaBuildDir)) {
        $message = "Media directory $mediaBuildDir does not exist." +
            " Exiting function. Returning False."
        $logger.logError($MyInvocation, $message, $True)
        return $False
    }

    $logger.logInfo("Media directory $mediaBuildDir exists", $True)  
    $logger.logInfo("Setting location to $mediaBuildDir", $True)
    Set-Location $mediaBuildDir


    # Start MVN Clean install (Download ISO)
    $timestamp = $(get-date -Format 'yyyyMMdd_HHmmss')
    $mvnOutLog = $logsDir + "\"+ $timestamp +"_$($mvnLogFileName)_mvnStdOut.log"
    $mvnErrLog = $logsDir + "\"+ $timestamp +"_$($mvnLogFileName)_mvnStdErr.log"
    $mvnSuccess = $False
   
    $remoteLocation = $remoteDownloadLocation.Replace(":", "$")
    $mvnOutputDirectory = "\\$REMOTE_SERVER\$remoteLocation"
    $mvnArgs = "clean install -DoutputDirectory=$mvnOutputDirectory"

    $logger.logInfo("Starting mvn with args $mvnArgs", $True)
    $logger.logInfo("Maven output sent to $logsDir", $True)
    
    $mvnProcess = Start-Process mvn $mvnArgs -RedirectStandardOutput $mvnOutLog -RedirectStandardError $mvnErrLog -PassThru -Wait    
    $logger.logInfo("mvn $mvnArgs COMPLETE", $True) 

    $logger.logInfo("Resetting location to $currentLocation", $True)
    Set-Location $currentLocation

    if ($mvnProcess.ExitCode -eq 0) {
        $logger.logInfo("Maven install completed successfully. Process Exited with exit code: 0. Returning True", $True)
        $mvnSuccess = $True
    } else {
        $logger.logWarning("Maven did not install successfully. Exitcode returned: "+$mvnProcess.ExitCode+". returning False", $True)
        $mvnSuccess = $False
    }
    
    return $mvnSuccess   
   
}

Function Get-ISOBuildVersion {
    param(
        [string] $remoteIsoLocation,
        [string] $remoteHost
    )

    $remoteFilePath = "\\$remoteHost\"+$remoteIsoLocation.Replace(":", "$")+"\*.iso"
    $logger.logInfo("looking up rstate from iso on remote path: $remoteFilePath", $True)

    if (Test-Path($remoteFilePath)) {
        $isoName = Get-Item $remoteFilePath 
        $buildVersion = $isoName.BaseName.Split("-")[-1]
        $logger.logInfo("Build Version: $buildVersion", $True)
        return $buildVersion
    } 

    $logger.logError($MyInvocation, "$remotePath not found", $True) 
    return $null
}


Function Get-AdhocBuildVersion {
    param(
        [string] $remoteAdhocBundleLocation,
        [string] $remoteHost,
        [string] $artifactName
    )

    $remoteFilePath = "\\$remoteHost\"+$remoteAdhocBundleLocation.Replace(":", "$")+"\$($artifactName)*.zip"
    $logger.logInfo("looking up rstate from adhoc zip on remote path: $remoteFilePath", $True)

    if (Test-Path($remoteFilePath)) {
        $adhocBundleName = Get-Item $remoteFilePath 
        $buildVersion = $adhocBundleName.BaseName.Split("-")[-1]
        $logger.logInfo("Build Version: $buildVersion", $True)
        return $buildVersion
    } 

    $logger.logError($MyInvocation, "$remotePath not found", $True) 
    return $null
}
