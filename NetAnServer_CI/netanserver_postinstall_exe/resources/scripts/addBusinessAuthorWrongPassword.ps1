$ericssonModules = "C:\Ericsson\NetAnServer\Modules"

if ( -not $env:PsModulePath.Contains($ericssonModules)) {
    $env:PSModulePath = $env:PSModulePath + ";$($ericssonModules)"
}


Import-Module ManageAdhocUsers
Import-Module SQLPS

$platformPassword = "WrongPassword"
$CIUSER = "BAuthor01"
Add-BusinessAuthor -u $CIUSER -p $CIUSER -pp $platformPassword 