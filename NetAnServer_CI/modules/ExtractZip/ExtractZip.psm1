Import-Module Logger

$logger = Get-Logger($LoggerNames.Install)


### Function: Open-ZipFile ###
#
#   Extracts zip file to specified location
# Arguments:
#   $inputZip - the absolute path of zipfile to extract 
#   $outputLocation - the absolute path to extract location directory
#
# Return Values:
#   [boolean]
#
Function Open-ZipFile() {
    param(
        $inputZip,
        $outputLocation
    )

    $logger.logInfo("testing $outputLocation exists", $True)
    if ( -not (Test-Path $outputLocation)) {
        $logger.logInfo("creating output location $outputLocation", $True)
        New-Item $outputLocation -type directory | Out-Null
    }

    $logger.logInfo("unzipping file $inputZip", $True)

    try {
        Add-Type -assembly "system.io.compression.filesystem"
        [io.compression.zipfile]::ExtractToDirectory($inputZip, $outputLocation)
    } catch {
        $logger.logError($MyInvocation, "unzipping of file $($inputZip) failed:  $($_.Exception.Message)", $True)
        return $False
    }

    $logger.logInfo("$inputZip unzipped to $outputLocation", $True)
    return $True
}