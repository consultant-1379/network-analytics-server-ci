Import-Module Logger

$logger = Get-Logger($LoggerNames.Install)

Function Start-PostInstallExe {
    param (
        [string] $remoteServer,
        [string] $remoteLogFiles,
        [string] $remotePackageInstallLocation,
        [string] $resultsDir, 
        [string] $buildVersion,
        [string] $test_type,
        [switch] $NO_DEPLOY
    )

    $TESTS_COMPLETED = "Tests Completed"

    $logger.logInfo("Starting Post Installation Sanity Tests exe", $True)
    
    $installLocation = $remotePackageInstallLocation.Replace(":", "$")
    $remoteInstallLocation = "\\$remoteServer\$installLocation"
    $remoteExeDir = "$remoteInstallLocation\netanserver_postinstall_exe"
    $remoteResultsDir = "$remoteInstallLocation\netanserver_postinstall_exe\results"
   
    if(-not $NO_DEPLOY) {
        $logger.logInfo("Testing if Remote exe dir exists $remoteExeDir", $True)    
        if ( Test-Path $remoteExeDir ) {
            $logger.logInfo("Removing remote exe dir $remoteExeDir", $True)
            Remove-Item $remoteExeDir -Recurse -Confirm:$False
            $logger.logInfo("Remote exe dir $remoteExeDir removed", $True)
        }
    #copy package to remote location
    
        $isTransferred = Start-TransferExePackage -location $remoteInstallLocation

        if(-not $isTransferred) {
            return $isTransferred
        }
    }

    #setup session and execute tests
    try {        
        $logger.logInfo("Establishing session to $remoteServer", $True)
        $session = New-PSSession $remoteServer -ErrorAction Stop
        $logger.logInfo("Session established", $True)
    } catch {
        $errorMessage = $Error[0].Stacktrace
        $logger.logError($MyInvocation, "Error establising session to $remoteServer `n $errorMessage ", $True)
        return $False
    }

    $formattedInstallLocation = $remoteExeDir.Replace("\\$remoteServer\", "").Replace("$", ":")
    $exeLocation = "$formattedInstallLocation\dist"

    # get the test cases to run based on $test_type switch
    $testCasesDir = Get-TestCaseDirectory $test_type
    $testCasesLocation = "$formattedInstallLocation\$testCasesDir"



    try {
        $logger.logInfo("Setting Session directory to path  $exeLocation", $True)
        $logger.logInfo("Executing testcases located at $testCasesLocation", $True)
        
        $results = Invoke-Command -Session $session -ScriptBlock { 
               
                $execLoc = $args[0].Item('exeLoc')
                $testsLocation = $args[0].Item('testsLoc')
                $logsLocation = $args[0].Item('logLoc')

                Set-Location $execLoc
                 .\testrunner.exe -td $testsLocation -l $logsLocation -r
                 
            } -ArgumentList @{"exeLoc"="$exeLocation"; "testsLoc"="$testCasesLocation"; "logLoc"="$remoteLogFiles"}  -ErrorAction Stop 
      
        $logger.logInfo("TestCases Executed `n $results", $True)
        Close-Session $session

    } catch {
        $errorMessage = $_.Exception.Message
        $logger.logError($MyInvocation, "Error executing remote commands setLocation: $exeLocation " +
            "testcases: $testCasesLocation logfiles: $remoteLogFiles `n $session `n $errorMessage `n $results ", $True)
        Close-Session $session
        return $False
    }

    
    if ($results.Contains($TESTS_COMPLETED)) {
        $logger.logInfo("Testcases in exe post installation tests completed successfully", $True)         
    } else {
        $logger.logWarning("Error in execution exe post installation tests", $True)
    }
    
    
    #rename results with build version + copy html file from remote dir to local results dir
    try {        
        Get-ChildItem $remoteResultsDir -Filter "*.html" | ForEach-Object {            
            $newName = $_.BaseName + "_" + $buildVersion
            $logger.logInfo("Renaming results from $_.BaseName to $newName", $True) 
            $remoteDir =  $_.Directory
            Move-Item $_.FullName "$remoteDir\$newName.html"
            $logger.logInfo("Renaming complete", $True) 
        } 

        $logger.logInfo("Transferring results from $remoteResultsDir to $resultsDir", $True) 
        Copy-Item -Path $remoteResultsDir\* -Include "*.html" "$resultsDir" -ErrorAction Stop
        $logger.logInfo("Results transferred from $remoteResultsDir to $resultsDir", $True)
    } catch {
         $errorMessage = $_.Exception.Message
         $logger.logError($MyInvocation, "Error transferring results from $remoteResultsDir to $resultsDir `n $errorMessage", $True)
         return $False
    }

    return $True
}


Function Close-Session {
    param (
        $sess
        )

    try {
        $logger.logInfo("Closing PSSession $sess", $True)
        Remove-PSSession -Session $sess -ErrorAction Stop
        $logger.logInfo("PSSession closed", $True)
    } catch {
        $errorMessage = $_.Exception.Message
        $logger.logWarning("Exception in closing PSSession `n $errorMessage", $True)
    }

}


Function Get-TestCaseDirectory {
    param (
        [string] $testTypeSwitch
    )

    switch ($testTypeSwitch) {
        ADHOC {
            $logger.logInfo("return adhoc-testcases" , $True)
            return "testcases\adhoc-testcases"
        }

        PLATFORM {
            $logger.logInfo("return platform-testcases" , $True)
            return "testcases\platform-testcases"
        }


        FEATURE {
            $logger.logInfo("return feature-installer-testcases" , $True)
            return "testcases\feature-installer-testcases"
        }

        UPGRADE {
            $logger.logInfo("return upgrade-testcases", $True)
            return "testcases\upgrade-testcases"
        }
    }
}

Function Start-TransferExePackage {
    param(
        [string] $location
    )

    try {        
        $logger.logInfo("Copying exe package to $location", $True)
        Copy-Item ./netanserver_postinstall_exe -destination $location -Force -Recurse -ErrorAction  Stop
        $logger.logInfo("Package copied to $location", $True)
        return $true
    } catch {
        $errorMessage = $_.Exception.Message
        $logger.logError($MyInvocation, "Error copying netanserver_postinstall_exe to $location" +
            " `n $errorMessage", $True)
        return $False
    }
}

Export-ModuleMember -Function "Start-TransferExePackage"
Export-ModuleMember -Function "Start-PostInstallExe"
