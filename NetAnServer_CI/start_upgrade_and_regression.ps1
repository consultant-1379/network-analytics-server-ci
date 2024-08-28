# adds the required libs for PowerCli cmdlets. 
# Has to be put here. Causes errors in module
Add-PSsnapin VMware.VimAutomation.Core
Add-PsSnapin KTools.PowerShell.SFTP

#configure module path if needed
$ciModules = $PSScriptRoot+"\modules"
if (-not $env:PSModulePath.Contains($ciModules)) {
    $env:PSModulePath = $env:PSModulePath + ";" + $ciModules
}

Import-Module Logger
Import-Module CiConfigProvider
Import-Module VMRollBack
Import-Module GetMedia
Import-Module RunInstall -DisableNameChecking
Import-Module RemoteScriptExecutor

######################################################
#                   CI Configuration                 #
######################################################
$configFile = "$($PsScriptRoot)\config\ci-config.xml"
if(-not (Test-Path $configFile)) {
    Write-Warning "the CI Configuration file could not be found: $configFile"
    break
}

$configProvider = CIConfigProvider -configFile $configFile
$VM = $configProvider.getVirtualHost()
$installedPlatformSnapShot = $configProvider.getUpgradeSnapShot()
$BUILD_VERSION = ""
$REMOTE_SERVER = "$VM.athtem.eei.ericsson.se"

######################################################
#                 Logger Configuration               #
######################################################
$LOGGER_DIR = $PSScriptRoot+"\logs"
if (-not (Test-Path $LOGGER_DIR)) {
    New-Item -path $LOGGER_DIR -type Directory
}
$LOGGER_FILENAME = "automation_CI.log"
$logger = Get-Logger($LoggerNames.Install)
$logger.setLogDirectory($LOGGER_DIR)
$logger.setLogName($LOGGER_FILENAME)
$logger.logInfo("starting the upgrade and regression script", $True)



######################################################
#                     Set VM Snapshot                #
######################################################
$CREDENTIALS_XML = $PSScriptRoot+"\credential_store\powercli_credentials.xml"
$VIRTUAL_CENTER = "atvcen1.athtem.eei.ericsson.se"
$snapShot = $installedPlatformSnapShot

$logger.LogInfo("*******************************************", $True)
$Logger.logInfo("*          Setting VM Snapshot            *", $True)
$logger.LogInfo("*******************************************", $True)

 $isRolledBack = Reset-VM $CREDENTIALS_XML $VIRTUAL_CENTER $VM $snapShot

if (-not $isRolledBack) {
    $logger.logError($MyInvocation, "snapshot setting has failed. Exiting", $True)
    exit
}

$logger.logInfo("snapshot setting completed successfully", $True)

$timeout = 100
$logger.logInfo("Sleeping script for $timeout seconds while waiting for OS to restore", $True)
Start-Sleep -s $timeout


#####################################################################
#                   Get-Latest Version of ISO Media                 #
#####################################################################
$logger.LogInfo("*******************************************", $True)
$Logger.logInfo("*    Downloading latest version of ISO    *", $True)
$logger.LogInfo("*******************************************", $True)

### ISO Configuration ###
$MEDIA_DIR = "\Media\netanserver_platform"
$ISO_BUILD_DIRECTORY = $PSScriptRoot+$MEDIA_DIR
$ISO_LOG_DIR = $LOGGER_DIR
#to avoid conflicts in existing media on OS
$INSTALL_LOCATION = "C:\Upgrade-CI\"
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



#####################################################################
#                     Find Current Platfrom Version                 #
#####################################################################

$ScriptBlock = {
    $env:PSModulePath = $env:PSModulePath + ";C:\Ericsson\NetAnServer\Modules"

    Import-Module PlatformVersionController -DisableNameChecking
    $platformVersion =  (Get-PlatformVersions | Where-Object -FilterScript { $_.'PRODUCT-ID'.trim() -eq 'CNA4032940'})    
    return $platformVersion.BUILD
}

try {
    $session = New-PSSession $REMOTE_SERVER
    $platformBuild = Invoke-Command -Session $session -ScriptBlock $ScriptBlock
    Write-Host $platformBuild
} catch {
    $logger.logError("Error attempting to get current platform version, $($_.Exception.Message)")
} finally {
    Remove-PSSession -Session $session -ErrorAction SilentlyContinue
}


#####################################################################
#                Transfer the Exe Post install package              #
#####################################################################

$REMOTE_LOCATION = "\\$($REMOTE_SERVER)\C$\"
$isTransferred = Start-TransferExePackage -location $REMOTE_LOCATION

if(-not $isTransferred) {
    $logger.logWarning("Error Transferring exe package", $True)
    break
}

#####################################################################
#                Update Test cases with platform versions           #
#####################################################################
$postinstallExeTestCases = "$($REMOTE_LOCATION)netanserver_postinstall_exe\testcases\upgrade-testcases\"

(Get-ChildItem $postInstallExeTestCases/*) | %{ 
    (Get-Content $_).Replace('<OLD_PLATFORM>', $platformBuild.trim()) | sc $_
    (Get-Content $_).Replace('<NEW_PLATFORM>', $BUILD_VERSION) | sc $_
}


#####################################################################
#                           Mount ISO Media                         #
#####################################################################

$logger.logInfo("*******************************************", $True)
$logger.logInfo("*           Start Mount of ISO            *", $True)
$logger.logInfo("*******************************************", $True)

$ISOLocation = $INSTALL_LOCATION
$drive = Mount-ISO $ISOLocation $REMOTE_SERVER

if (-not $drive) {
    $logger.logWarning("Error mounting ISO")
    break
}
if ($drive) {
    $logger.logInfo("*******************************************", $True)
    $logger.logInfo("*        Start Decrypt & Deploy           *", $True)
    $logger.logInfo("*******************************************", $True)
    $decryptDeployScript = "NetAnServer.ps1"
    $decryptDeploySuccess = Run-DecryptDeploy $drive $decryptDeployScript $REMOTE_SERVER 

     if(-not $decryptDeploySuccess){
        $logger.logError($MyInvocation, "The decrypt and deploy was not completed successfully", $True)
        exit        
    }else{
        $logger.logInfo("The decrypt and deploy was completed successfully", $True)
        $logger.logInfo("*******************************************", $True)
        $logger.logInfo("*        Start Upgrade                    *", $True)
        $logger.logInfo("*******************************************", $True)

        $REMOTE_SCRIPT_LOCATION = "C:/Ericsson/tmp/Scripts/Install/NetAnServer_upgrade.ps1"
        $isRun = Start-Script $REMOTE_SERVER $REMOTE_SCRIPT_LOCATION "" 

        if(-not $isRun){
            $logger.logError($MyInvocation, "The Upgrade was not completed successfully", $True)        
        }else{
            $logger.logInfo("The Upgrade was completed successfully", $True)
        }
    }

}



#####################################################################
#                        Start LOG/CLI Regression                   #
#####################################################################
$logger.LogInfo("*******************************************", $True)
$Logger.logInfo("*        Start LOG/CLI Regression         *", $True)
$logger.LogInfo("*******************************************", $True)

### EXE Configuration ###
$LOG_DIRECTORY = "C:\Ericsson\NetAnServer\Logs\"
$INSTALL_LOCATION = "C:"
$RESULTS_DIR = $PSScriptRoot + "\results\post-install-logs"
$TESTCASES = "UPGRADE"

$isPostInstallExe = Start-PostInstallExe $REMOTE_SERVER $LOG_DIRECTORY $INSTALL_LOCATION $RESULTS_DIR "$($TESTCASES)-$($BUILD_VERSION)" $TESTCASES -NO_DEPLOY

if (-not $isPostInstallExe ) {
    $logger.logWarning("Error executing Python Post install Upgrade Regression Tests", $True)
    return $isPostInstallExe
}



#####################################################################
#                        Zip results                                #
#####################################################################
$logger.LogInfo("*******************************************", $True)
$Logger.logInfo("*        Starting Zip of results             *", $True)
$logger.LogInfo("*******************************************", $True)
$RESULTS_DIRECTORY = "$($PSScriptRoot)\results"

$file = Start-ZipResults -zipTargetDir $RESULTS_DIRECTORY -platformBuildNumber $BUILD_VERSION -includeTAFResults $False -UPGRADE
mv $file "$($file.split('.')[-2])-UPGRADE.zip"

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