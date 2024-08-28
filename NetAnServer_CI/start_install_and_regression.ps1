#
# See Readme.txt for details of script
#
# adds the required libs for PowerCli cmdlets. 
# Has to be put here. Causes errors in module
Add-PSsnapin VMware.VimAutomation.Core
Add-PsSnapin KTools.PowerShell.SFTP

#configure module path if needed
$ciModules = $PSScriptRoot+"\modules"
if (-not $env:PSModulePath.Contains($ciModules)) {
    $env:PSModulePath = $env:PSModulePath + ";" + $ciModules
}

#import modules
Import-Module Logger
Import-Module VMRollBack
Import-Module TAFRunner
Import-Module GetMedia
Import-Module PostInstallExeRunner
Import-Module ZipResults
Import-Module UploadResults
Import-Module RunInstall
Import-Module -DisableNameChecking RunDecryptDeploy
Import-Module ExtractZip
Import-Module RemoteScriptExecutor
Import-Module CiConfigProvider


# CI Configuration
$configFile = "$($PsScriptRoot)\config\ci-config.xml"
if(-not (Test-Path $configFile)) {
    Write-Warning "the CI Configuration file could not be found: $configFile"
    break
}

$configProvider = CIConfigProvider -configFile $configFile
$VM = $configProvider.getVirtualHost()
$vmSnapshot = $configProvider.getInitialInstallSnapShot()
$BUILD_VERSION = ""
$REMOTE_SERVER = "$VM.athtem.eei.ericsson.se"

# Logger Configuration
$LOGGER_DIR = $PSScriptRoot+"\logs"
if (-not (Test-Path $LOGGER_DIR)) {
    New-Item -path $LOGGER_DIR -type Directory
}
$LOGGER_FILENAME = "automation_CI.log"
$logger = Get-Logger($LoggerNames.Install)
$logger.setLogDirectory($LOGGER_DIR)
$logger.setLogName($LOGGER_FILENAME)
$logger.logInfo("starting the install and regression script", $True) 

## Update the TAF hostname.properties.json with the VM SUT hostname
$tafHostFile = "$($PSScriptRoot)\TAF\ERICTAFNetAnServer_CXP9027134\src\main\resources\taf_properties\host.properties.json"
(Get-Content $tafHostFile).Replace('<hostname>', $VM) | sc $tafHostFile

#####################################################################
#                            VM Rollback                            #
#####################################################################

### PowerCLI Configuration ###
$CREDENTIALS_XML = $PSScriptRoot+"\credential_store\powercli_credentials.xml"
$VIRTUAL_CENTER = "atvcen1.athtem.eei.ericsson.se"
$snapShot = $vmSnapshot

$logger.LogInfo("*******************************************", $True)
$Logger.logInfo("*        Starting Rollback of VM          *", $True)
$logger.LogInfo("*******************************************", $True)

 $isRolledBack = Reset-VM $CREDENTIALS_XML $VIRTUAL_CENTER $VM $snapShot

if (-not $isRolledBack) {
    $logger.logError($MyInvocation, "roll back has failed. Exiting", $True)
    exit
}

$logger.logInfo("roll back completed successfully", $True)

$timeout = 100
$logger.logInfo("Sleeping script for $timeout seconds while waiting for OS to restore", $True)
Start-Sleep -s $timeout
#####################################################################
#                           Download ISO                            #
#####################################################################

### ISO Configuration ###
$MEDIA_DIR = "\Media\netanserver_platform"
$ISO_BUILD_DIRECTORY = $PSScriptRoot+$MEDIA_DIR
$ISO_LOG_DIR = $LOGGER_DIR
$INSTALL_LOCATION = "C:\"
$MVN_LOGNAME = "getIso"

$logger.logInfo("*******************************************", $True)
$Logger.logInfo("*         Getting ISO                     *", $True)
$logger.logInfo("*******************************************", $True)

$isIsoAvailable = Get-Media $ISO_BUILD_DIRECTORY $ISO_LOG_DIR $INSTALL_LOCATION $REMOTE_SERVER $MVN_LOGNAME

if (-not $isIsoAvailable ) {
    $logger.logWarning("Error ISO not Available", $True)
    exit
} else {
    $logger.logInfo("ISO Available at $ISO_BUILD_DIRECTORY", $True)
}

$BUILD_VERSION = Get-ISOBuildVersion $INSTALL_LOCATION $REMOTE_SERVER 


#####################################################################
#                       Run Install                                 #
#####################################################################


$logger.logInfo("*******************************************", $True)
$logger.logInfo("*        Start Mount of ISO               *", $True)
$logger.logInfo("*******************************************", $True)

$ISOLocation = "C:\" 
$Drive = Mount-ISO $ISOLocation $REMOTE_SERVER

if ($Drive) {
    $logger.logInfo("*******************************************", $True)
    $logger.logInfo("*        Start Decrypt & Deploy           *", $True)
    $logger.logInfo("*******************************************", $True)
    $decryptDeployScript = "NetAnServer.ps1"
    $decryptDeploySuccess = Run-DecryptDeploy $Drive $decryptDeployScript $REMOTE_SERVER 

     if(-not $decryptDeploySuccess){
        $logger.logError($MyInvocation, "The decrypt and deploy was not completed successfully", $True)
        exit        
    }else{
        $logger.logInfo("The decrypt and deploy was completed successfully", $True)
        $logger.logInfo("*******************************************", $True)
        $logger.logInfo("*        Start Install                    *", $True)
        $logger.logInfo("*******************************************", $True)

        $InstallSuccess = Run-Install $REMOTE_SERVER 

        if(-not $InstallSuccess){
            $logger.logError($MyInvocation, "The install was not completed successfully", $True)        
        }else{
            $logger.logInfo("The install was completed successfully", $True)
        }
    }

} else {
    $logger.logError($MyInvocation,"Error Decrypting/Deploying media, Aborting Install ", $True)
    
}

#####################################################################
#                        Start TAF Regression                       #
#####################################################################

### TAF Configuration ###
$TAF_DIRECTORY = $PSScriptRoot+"\TAF"
$TAF_LOG_DIR = $LOGGER_DIR

$logger.LogInfo("*******************************************", $True)
$Logger.logInfo("*        Starting TAF Regression          *", $True)
$logger.LogInfo("*******************************************", $True)


$isTafRun = Start-TAF $TAF_DIRECTORY $TAF_LOG_DIR "clean install -Dsuites=adminui-suite.xml"

if (-not $isTafRun ) {
    $logger.logWarning("Error executing TAF Regression Tests", $True)
}

$logger.logInfo("Taf regression tests complete", $True)


#####################################################################
#                        Start LOG/CLI Regression                   #
#####################################################################
$logger.LogInfo("*******************************************", $True)
$Logger.logInfo("*        Start LOG/CLI Regression         *", $True)
$logger.LogInfo("*******************************************", $True)

### EXE Configuration ###
$LOG_DIRECTORY = "C:\Ericsson\NetAnServer\Logs"
$INSTALL_LOCATION = "C:"
$RESULTS_DIR = $PSScriptRoot + "\results\post-install-logs"
$TESTCASES = "PLATFORM"

$isPostInstallExe = Start-PostInstallExe $REMOTE_SERVER $LOG_DIRECTORY $INSTALL_LOCATION $RESULTS_DIR "$($TESTCASES)-$($BUILD_VERSION)" $TESTCASES

if (-not $isPostInstallExe ) {
    $logger.logWarning("Error executing Python Post install Regression Tests", $True)
}

$logger.logInfo("Python Post install Regression Tests complete", $True)


#####################################################################
#                        Download Adhoc Bundle                      #
#####################################################################
#
#   This will require a pom file in the root directory called:
#            /NetAnServer_CI/Media/adhoc_bundle
#

#!!!!! CHANGE PARAMETERS ONCE KNOWN !!!!!!!
$ADHOC_ARTIFACT_ID = "Ericsson-network-analytics-server-ad-hoc-enabler-package" # the artifact ID of the adhoc bundle 
$INSTALL_LOCATION = "C:\" # location on remote SUT

$logger.logInfo("*******************************************", $True)
$Logger.logInfo("*        Downloading Adhoc Bundle         *", $True)
$logger.logInfo("*******************************************", $True)

$MEDIA_DIR = "\Media\adhoc_bundle" 
$ADHOC_BUILD_DIRECTORY = $PSScriptRoot+$MEDIA_DIR #location of adhoc bundle POM

$ADHOC_LOG_DIR = $LOGGER_DIR #destination for mvn logs
$MVN_LOGNAME = "getAdhoc" #mvn logname e.g. <date-time>_getAdhoc_strErr.log 

$isBundleAvailable = Get-Media $ADHOC_BUILD_DIRECTORY $ADHOC_LOG_DIR $INSTALL_LOCATION $REMOTE_SERVER $MVN_LOGNAME

if (-not $isBundleAvailable ) {
    $logger.logWarning("Error Adhoc Bundle Media not Available", $True)
    exit
} else {
    $logger.logInfo("Adhoc Bundle Media Available at $ADHOC_BUILD_DIRECTORY", $True)
}

$ADHOC_BUILD_VERSION = Get-AdhocBuildVersion $INSTALL_LOCATION $REMOTE_SERVER $ADHOC_ARTIFACT_ID


#####################################################################
#                          Unzip Adhoc Bundle                       #
#####################################################################

#!!!!! CHANGE PARAMETER ONCE KNOWN !!!!!!!
$ADHOC_EXTRACT_LOCATION = "C:\Ericsson\tmp\adhoc" #  the remote location to extract zip file to

$logger.logInfo("*******************************************", $True)
$Logger.logInfo("*         Unzipping Adhoc Bundle          *", $True)
$logger.logInfo("*******************************************", $True)

$remoteSourceZipLocation = $INSTALL_LOCATION -replace ":", "$"
$adhocBundleZip = (Get-Item "\\$($REMOTE_SERVER)\$($remoteSourceZipLocation)\*" -Filter "*$($ADHOC_ARTIFACT_ID)*zip").Fullname


$extractlocation = $ADHOC_EXTRACT_LOCATION -replace ":", "$"
$remoteZipExtractLocation = "\\$($REMOTE_SERVER)\$($extractlocation)\"

$isZipExtracted = Open-ZipFile $adhocBundleZip $remoteZipExtractLocation

if (-not $isZipExtracted) {
    $logger.logError($MyInvocation, "Error extracting adhoc bundle zip file", $True)
    exit
}


#####################################################################
#                     Execute Adhoc Bundle Deployment               #
#####################################################################


$Drive = "C"
$adhocBundleScript = "Ericsson\tmp\adhoc\AdHocEnablerExtractInstall.ps1"
$TEST_AD_HOC = $true

$logger.logInfo("*******************************************", $True)
$Logger.logInfo("*     Executing Adhoc Bundle Deployment   *", $True)
$logger.logInfo("*******************************************", $True)

$result = Run-DecryptDeploy $Drive $adhocBundleScript $REMOTE_SERVER $TEST_AD_HOC

if($result){
    $logger.logInfo("The Adhoc Bundle Deployment was completed successfully", $True)
}else {
    $logger.logError($MyInvocation, "The Adhoc Bundle Deployment Failed", $True)
}


#####################################################################
#                        Start Python exe testcases                 #
#####################################################################

$LOG_DIRECTORY = "C:\Ericsson\NetAnServer\Logs\AdhocEnabler"
$TESTCASES = "ADHOC"

$logger.LogInfo("*******************************************", $True)
$Logger.logInfo("*        Start Python exe testcases       *", $True)
$logger.LogInfo("*******************************************", $True)

### EXE Configuration ###

$INSTALL_LOCATION = "C:"
$RESULTS_DIR = $PSScriptRoot + "\results\post-install-logs"

$isPostInstallExe = Start-PostInstallExe $REMOTE_SERVER $LOG_DIRECTORY $INSTALL_LOCATION $RESULTS_DIR "$($TESTCASES)-$($ADHOC_BUILD_VERSION)" $TESTCASES

if (-not $isPostInstallExe ) {
    $logger.logWarning("Error executing Python Post install Regression Tests", $True)
}

$logger.logInfo("Python Post install Regression Tests complete", $True)


#####################################################################
#                        Zip results                                #
#####################################################################
$logger.LogInfo("*******************************************", $True)
$Logger.logInfo("*        Starting Zip of results             *", $True)
$logger.LogInfo("*******************************************", $True)
$RESULTS_DIRECTORY = "$($PSScriptRoot)\results"

$file = Start-ZipResults -zipTargetDir $RESULTS_DIRECTORY -platformBuildNumber $BUILD_VERSION -adhocBuildVersion $ADHOC_BUILD_VERSION -includeTAFResults $True

mv $file "$($file.split('.')[-2])-PLATFORM-ADHOC.zip"


#####################################################################
#                        FTP results to Radiator                   #
#####################################################################
$logger.LogInfo("*******************************************", $True)
$Logger.logInfo("*        FTP results to radiator         *", $True)
$logger.LogInfo("*******************************************", $True)


$CI_HUB_IP="150.132.151.70"
$CI_USER="eniqdmt"
$CI_DIR_LOCATION="/tmp"
Start-Sftp $CI_HUB_IP $CI_USER $CI_DIR_LOCATION $RESULTS_DIRECTORY