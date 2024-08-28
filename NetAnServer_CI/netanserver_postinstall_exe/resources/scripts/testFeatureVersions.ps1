$ericssonModules = "C:\Ericsson\NetAnServer\Modules"

if ( -not $env:PsModulePath.Contains($ericssonModules)) {
    $env:PSModulePath = $env:PSModulePath + ";$($ericssonModules)"
}

Import-Module RepDBUtilities
$allFeatures = Get-Features -Full_History

#The updated version
$versionOneFeature = $allFeatures | %{ if($_.Build.trim() -eq "R1A01") { return $_.STATUS }}
$versionTwoFeature = $allFeatures | %{ if($_.Build.trim() -eq "R1A02") { return $_.STATUS }}

if(($versionOneFeature.trim() -eq "REMOVED") -and ($versionTwoFeature.trim() -eq "INSTALLED")) {
    return "passed"
} else {
    return "failed"
}