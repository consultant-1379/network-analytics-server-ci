Import-Module Logger

$logger = Get-Logger($LoggerNames.Install)

function Start-ZipResults {
    param(
        [string] $zipTargetDir,
        [string] $platformBuildVersion,
        [string] $adhocBuildVersion,
        [bool] $includeTAFResults,
        [switch] $FEATURE_INSTALLER,
        [switch] $UPGRADE
    )
    $global:zipPackage = ""
    $global:date = Get-Date -format "yyyyMMddHHmmss"
    $global:logger = Get-Logger($LoggerNames.Install)
    $global:zipName = "NetAnServerCIResults"
    $global:ciRootDir = (Get-Item $PSScriptRoot).parent.parent.FullName
    $global:sourceFolder = $zipTargetDir+"\"+$zipName+$date
    $global:zipFinalName = $sourceFolder+".zip"
    $global:postInstallLogsDir = $ciRootDir+"\results\post-install-logs"
    $global:postInstallTAFDir = $ciRootDir+"\results\post-install-taf"
    $global:tafResultsDir = $ciRootDir+"\TAF\test-pom-NetAnServer\target\Jcat_LOGS\*"
    $global:installLogTempDir = $postInstallLogsDir+"\post-install-logs"

    if (Test-Path($sourceFolder)) {
        $logger.logInfo("Source folder exists, creating new.", $True)  
        Remove-Item $sourceFolder
    }

    #Remove previous results zip folder
    Get-ChildItem -Path $zipTargetDir -Recurse | Remove-Item -Include "*.zip" -Recurse -Force

    New-Item -ItemType directory -Path $sourceFolder | Out-Null

    $logger.logInfo("Begining Zip of Post Install Log and Taf results", $True)  

    #Adding Post-Install-Logs    
    if ($FEATURE_INSTALLER) {
        Add-PostInstallLogs -FEATURE_INSTALLER
    } else {
        Add-PostInstallLogs
    }

    #Adding Post-Install-TAF
    if ($includeTAFResults) {
        Add-PostInstallTAF 
    }

    #Remove .gitignore files
    Get-ChildItem -Path $sourceFolder -Recurse | Remove-Item -Include "*.gitignore" -Recurse -Force

    #Add folder to Zip 
    Zip-Files $zipFinalName $sourceFolder

    #Delete temporary folders
    Remove-Item -Recurse -Force $installLogTempDir
    Remove-Item -Recurse -Force $sourceFolder
    
    if ($includeTAFResults) {
        #Clean post-install-taf directory
        Get-ChildItem -Path $postInstallTAFDir -Recurse | Remove-Item -Exclude "*.gitignore" -Recurse -Force
    }

    return $zipFinalName
}

function Add-PostInstallLogs {
    param(
        [switch] $FEATURE_INSTALLER
    )

    $logger.logInfo("Adding Post Install Logs results", $True) 
    #create temp post-install-logs dir
    $cssDir = "\css"
    $jsDir = "\js"

    if (-not (Test-Path $installLogTempDir)) {
        New-Item -ItemType directory -Path $installLogTempDir | Out-Null
    }
   
    #Copy CSS folder
    Copy-Item -Path $postInstallLogsDir$cssDir -Destination $installLogTempDir$cssDir -Recurse -Force

    #Copy JS folder
    Copy-Item -Path $postInstallLogsDir$jsDir -Destination $installLogTempDir$jsDir -Recurse -Force

    #Copy Latest HTML file
    #This will only copy the latest file for the current build. If no file is present will not copy.
    $latestPlatformHtmlFile = Get-ChildItem $postinstallLogsDir | Sort-Object LastWriteTime -Descending | Where-Object { $_.Name.Contains($platformBuildVersion) -and $_.Name.Contains("PLATFORM") } | select -First 1
    $latestAdhocHtmlFile = Get-ChildItem $postinstallLogsDir | Sort-Object LastWriteTime -Descending | Where-Object { $_.Name.Contains($adhocBuildVersion) -and $_.Name.Contains("ADHOC") } | select -First 1
    $latestFeatureHtmlFile = Get-ChildItem $postinstallLogsDir | Sort-Object LastWriteTime -Descending | Where-Object { $_.Name.Contains($platformBuildVersion) -and $_.Name.Contains("FEATURE") } | select -First 1
    $latestUpgradeHtmlFile = Get-ChildItem $postinstallLogsDir | Sort-Object LastWriteTime -Descending | Where-Object { $_.Name.Contains($platformBuildVersion) -and $_.Name.Contains("UPGRADE") } | select -First 1
    
    if($FEATURE_INSTALLER) {
        if ($latestFeatureHtmlFile) {
            Copy-Item -Path $postInstallLogsDir"\"$latestFeatureHtmlFile -Destination $installLogTempDir -Recurse -Force
        }
    } elseif($UPGRADE) {
        if($latestUpgradeHtmlFile) {
            Copy-Item -Path $postInstallLogsDir"\"$latestUpgradeHtmlFile -Destination $installLogTempDir -Recurse -Force
        }

        if($latestPlatformHtmlFile) {
            Copy-Item -Path $postInstallLogsDir"\"$latestPlatformHtmlFile -Destination $installLogTempDir -Recurse -Force
        }

    } else {
        if ($latestPlatformHtmlFile) {
            Copy-Item -Path $postInstallLogsDir"\"$latestPlatformHtmlFile -Destination $installLogTempDir -Recurse -Force
        }

        if ($latestAdhocHtmlFile) {
            Copy-Item -Path $postInstallLogsDir"\"$latestAdhocHtmlFile -Destination $installLogTempDir -Recurse -Force
        }
    }    

    Copy-Item -Path $installLogTempDir -Destination $sourceFolder -Recurse -Force
}

function Add-PostInstallTAF {

    $logger.logInfo("Adding TAF results", $True) 
    #Copy Taf results to temp directory
    Copy-Item -Path $tafResultsDir -Destination $postInstallTAFDir  -Recurse -Force 
    Copy-Item -Path $postInstallTAFDir -Destination $sourceFolder -Recurse -Force


}

function Zip-Files {
    param( 
        [string] $sourceFolder,
        [string] $sourcedir 
    ) 
    $logger.logInfo("Creating zip from source folder", $True) 
    Add-Type -Assembly System.IO.Compression.FileSystem
    $compressionLevel = [System.IO.Compression.CompressionLevel]::Optimal
    [System.IO.Compression.ZipFile]::CreateFromDirectory($sourcedir, $sourceFolder, $compressionLevel, $false)
}

Export-ModuleMember "Start-ZipResults"