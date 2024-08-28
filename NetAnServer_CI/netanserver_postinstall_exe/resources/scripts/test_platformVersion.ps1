$ericssonModules = "C:\Ericsson\NetAnServer\Modules"

if ( -not $env:PsModulePath.Contains($ericssonModules)) {
    $env:PSModulePath = $env:PSModulePath + ";$($ericssonModules)"
}

Import-Module PlatformVersionController -DisableNameChecking
Import-Module SQLPS -DisableNameChecking

$isoFileName = Get-ChildItem C:\ *.iso
$isoBuild = ($isoFileName.toString().split(".")[0]).split("-")[-1]

$plaformDetails = Get-PlatformVersions | Where-Object -FilterScript { $_.'PRODUCT-ID'.trim() -eq 'CNA4032940' }
$cmdletBuild = ($plaformDetails.BUILD).TrimEnd()


if(($isoBuild -ne $cmdletBuild)){
    $isoFileName = Get-ChildItem C:\Upgrade-CI\ *.iso
    $isoBuild = ($isoFileName.toString().split(".")[0]).split("-")[-1]

}

if ($isoBuild -eq $cmdletBuild) {
    return "Passed"
} else {
    return "Failed"
}
