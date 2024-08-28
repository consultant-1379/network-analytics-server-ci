$ericssonModules = "C:\Ericsson\NetAnServer\Modules"

if ( -not $env:PsModulePath.Contains($ericssonModules)) {
    $env:PSModulePath = $env:PSModulePath + ";$($ericssonModules)"
}


Import-Module SQLPS
Import-Module ManageUsersUtility

$platformPassword = "WrongPassword"
$CIUSER = "Consum01"
Add-ConsumerUser -u $CIUSER -p "$($CIUSER)" -pp $platformPassword 

