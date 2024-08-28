
$logger = Get-Logger($LoggerNames.Install)

Function Start-TAF {
    param(
        [string] $tafDir,
        [string] $logsDir,
        [string] $mvnParams
        )

    $currentLocation = Get-Location

    $logger.logInfo("Testing that TAF directory $tafDir exists", $True)  
 
    if (-not (Test-Path $tafDir)) {
        $message = "TAF directory $tafDir does not exist." +
            " Exiting function. Returning False."
        $logger.logError($MyInvocation, $message, $True)
        return $False
    }

    $logger.logInfo("TAF directory $tafDir exists", $True)  
    $logger.logInfo("setting location to $tafDir", $True)
    Set-Location $tafDir

    #test if logdir exitst.
    if (-not (Test-Path $logsDir)) {
        $logger.logWarning("$logsDir does not exist. Creating Directory.", $True)
        New-Item -path $logsDir -type Directory
        $logger.logInfo("$logsDir directory created.", $True)
    }


    # Start MVN Clean install (kicks off tests)
    $timestamp = $(get-date -Format 'yyyyMMdd_HHmmss')
    $mvnOutLog = $logsDir + "\"+ $timestamp +"_mvnStdOut.log"
    $mvnErrLog = $logsDir + "\"+ $timestamp +"_mvnStdErr.log"
   
    $logger.logInfo("Starting mvn $($mvnParams)", $True)
    $logger.logInfo("Maven output sent to $logsDir", $True)
    
    $mvnProcess = Start-Process mvn $mvnParams -RedirectStandardOutput $mvnOutLog -RedirectStandardError $mvnErrLog -PassThru -Wait    

    $logger.logInfo("Resetting location to $currentLocation", $True)
    Set-Location $currentLocation

    if ($mvnProcess.ExitCode -eq 0) {
        $logger.logInfo("Maven cmd complete. Process Exited with exit code: 0. Returning True", $True)
        return $True
    } else {
        $logger.logWarning("Maven cmd exited with non zero exitcode: "+$mvnProcess.ExitCode+". returning False", $True)
        return $False
    }    
}