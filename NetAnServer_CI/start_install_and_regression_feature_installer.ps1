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

Import-Module Logger -DisableNameChecking
Import-Module VMRollBack -DisableNameChecking
Import-Module FeatureInstall -DisableNameChecking
Import-Module RunInstall -DisableNameChecking
Import-Module GetMedia -DisableNameChecking
Import-Module CiConfigProvider

#CI Configuration
$configFile = "$($PsScriptRoot)\config\ci-config.xml"
if(-not (Test-Path $configFile)) {
    Write-Warning "the CI Configuration file could not be found: $configFile"
    break
}

$configProvider = CIConfigProvider -configFile $configFile
$VM = $configProvider.getVirtualHost()
$installedPlatformSnapShot = $configProvider.getFullInstallSnapShot()
$BUILD_VERSION = ""
$REMOTE_SERVER = "$VM.athtem.eei.ericsson.se"

# Logger Configuration
$LOGGER_DIR = $PSScriptRoot+"\logs"
if (-not (Test-Path $LOGGER_DIR)) {
    New-Item -path $LOGGER_DIR -type Directory
}
$LOGGER_FILENAME = "automation_CI_featureInstaller.log"
$logger = Get-Logger($LoggerNames.Install)
$logger.setLogDirectory($LOGGER_DIR)
$logger.setLogName($LOGGER_FILENAME)
$logger.logInfo("starting the install and regression script for feature installer", $True) 


### PowerCLI Configuration ###
$CREDENTIALS_XML = $PSScriptRoot+"\credential_store\powercli_credentials.xml"
$VIRTUAL_CENTER = "atvcen1.athtem.eei.ericsson.se"
$snapShot = $installedPlatformSnapShot


## Update the TAF hostname.properties.json with the VM SUT hostname
$tafHostFile = "$($PSScriptRoot)\TAF\ERICTAFNetAnServer_CXP9027134\src\main\resources\taf_properties\host.properties.json"
(Get-Content $tafHostFile).Replace('<hostname>', $VM) | sc $tafHostFile

#####################################################################
#                     Starting Rollforward of VM                    #
#####################################################################
$logger.LogInfo("*******************************************", $True)
$Logger.logInfo("*       Starting Rollforward of VM        *", $True)
$logger.LogInfo("*******************************************", $True)

$isRolledForward = Reset-VM $CREDENTIALS_XML $VIRTUAL_CENTER $VM $snapShot

if (-not $isRolledForward) {
    $logger.logError($MyInvocation, "roll forward to $($snapShot) has failed. Exiting", $True)
    exit
}

$logger.logInfo("roll forward to $($snapShot) completed successfully", $True)
$timeout = 100
$logger.logInfo("Sleeping script for $timeout seconds while waiting for OS to restore", $True)
Start-Sleep -s $timeout


#####################################################################
#                 Get the latest versions of Modules                #
#####################################################################
$logger.LogInfo("*******************************************", $True)
$Logger.logInfo("*    Getting latest versions of Modules   *", $True)
$logger.LogInfo("*******************************************", $True)

### ISO Configuration ###
$MEDIA_DIR = "\Media\netanserver_platform"
$ISO_BUILD_DIRECTORY = $PSScriptRoot+$MEDIA_DIR
$ISO_LOG_DIR = $LOGGER_DIR
#to avoid conflicts in existing media on OS
$INSTALL_LOCATION = "C:\FeatureInstaller-CI\"
$MVN_LOGNAME = "getIso"


$logger.logInfo("Downloading latest Platform ISO", $True)
$isIsoAvailable = Get-Media $ISO_BUILD_DIRECTORY $ISO_LOG_DIR $INSTALL_LOCATION $REMOTE_SERVER $MVN_LOGNAME

if (-not $isIsoAvailable ) {
    $logger.logWarning("Error ISO not Available", $True)
    exit
} else {
    $logger.logInfo("ISO Available at $ISO_BUILD_DIRECTORY", $True)
}

$BUILD_VERSION = Get-ISOBuildVersion $INSTALL_LOCATION $REMOTE_SERVER 

$logger.logInfo("*******************************************", $True)
$logger.logInfo("*        Start Mount of ISO               *", $True)
$logger.logInfo("*******************************************", $True)

$ISOLocation = "C:\FeatureInstaller-CI\"
$drive = Mount-ISO $ISOLocation $REMOTE_SERVER

if ($drive) {
    $logger.logInfo("*******************************************", $True)
    $logger.logInfo("*        Start Decrypt & Deploy           *", $True)
    $logger.logInfo("*******************************************", $True)
    $decryptDeployScript = "NetAnServer.ps1"
    $decryptDeploySuccess = Run-DecryptDeploy $Drive $decryptDeployScript $REMOTE_SERVER 

    if ($decryptDeploySuccess) {
        $logger.logInfo("*******************************************", $True)
        $logger.logInfo("*            Update Modules               *", $True)
        $logger.logInfo("*******************************************", $True)

        #remove all old modules
        Get-Item "\\$($REMOTE_SERVER)\C$\Ericsson\tmp\Scripts\Modules\*" | %{ Remove-Item "\\$($REMOTE_SERVER)\C$\Ericsson\NetAnServer\Modules\$($_.Name)" -Force -Recurse -Confirm:$False }
        Copy-Item -Path "\\$($REMOTE_SERVER)\C$\Ericsson\tmp\Scripts\Modules\*" -Destination "\\$($REMOTE_SERVER)\C$\Ericsson\NetAnServer\Modules" -Recurse -Force
    } else {
        $logger.logWarning("decryption failed")
        return
    }

} else {
    $logger.logError($MyInvocation,"Error Decrypting/Deploying media, Aborting Install ", $True)
    
}

#####################################################################
#                        Transfer Features                          #
#####################################################################
$logger.LogInfo("*******************************************", $True)
$Logger.logInfo("*             Transfer Features           *", $True)
$logger.LogInfo("*******************************************", $True)
#Copy both test feature packages to SUT
$testFeatures = (Get-Item "$($PSScriptRoot)\resources\FeatureInstaller\version-*\version-*.zip")
$FEATURE_PACKAGE_DIR = "\\$($REMOTE_SERVER)\C$\FeatureInstaller-CI\"

New-Item -Path $FEATURE_PACKAGE_DIR -type directory -Force | Out-Null

foreach ($feature in $testFeatures) {
    Copy-Item $($feature.Fullname) "$($FEATURE_PACKAGE_DIR)$($feature.Name)" -Force
}


#####################################################################
#                        Install First Feature                      #
#####################################################################
$logger.LogInfo("*******************************************", $True)
$Logger.logInfo("*          Install First Feature          *", $True)
$logger.LogInfo("*******************************************", $True)
$isInstalled = Install-Feature $($REMOTE_SERVER) "C:\FeatureInstaller-CI\version-one.zip" "1"

if(-not $IsInstalled) {
    $logger.logError($MyInvocation, "error installing version-one.zip", $True)
    return $False
}

#####################################################################
#                        Start TAF Regression                       #
#####################################################################
$logger.LogInfo("*******************************************", $True)
$Logger.logInfo("*                Starting TAF             *", $True)
$logger.LogInfo("*******************************************", $True)
#   Note: TAF carries out the upgrade - please refer to install_feature_two.ps1 
#   in TAF testware resources directory
#
$TAF_DIRECTORY = $PSScriptRoot+"\TAF"
$TAF_LOG_DIR = $LOGGER_DIR

$isTafRun = Start-TAF $TAF_DIRECTORY $TAF_LOG_DIR "clean install -Dsuites=feature-installer.xml"

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
$LOG_DIRECTORY = "C:\Ericsson\NetAnServer\Logs\feature_installation"
$TESTCASES = "FEATURE"
$INSTALL_LOCATION = "C:"
$RESULTS_DIR = $PSScriptRoot + "\results\post-install-logs"

$isPostInstallExe = Start-PostInstallExe $REMOTE_SERVER $LOG_DIRECTORY $INSTALL_LOCATION $RESULTS_DIR "$($TESTCASES)-$($BUILD_VERSION)" $TESTCASES

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

$file = Start-ZipResults -zipTargetDir $RESULTS_DIRECTORY -platformBuildNumber $BUILD_VERSION -includeTAFResults $True -FEATURE_INSTALLER
mv $file "$($file.split('.')[-2])-FEATURE.zip"
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