$ericssonModules = "C:\Ericsson\NetAnServer\Modules"

if ( -not $env:PsModulePath.Contains($ericssonModules)) {
    $env:PSModulePath = $env:PSModulePath + ";$($ericssonModules)"
}


Import-Module ManageAdhocUsers
Import-Module SQLPS

$platformPassword = "WrongPassword"
$CIUSER = "BAnalyst01"
Add-BusinessAnalyst -u $CIUSER -p "$($CIUSER)" -pp $platformPassword 