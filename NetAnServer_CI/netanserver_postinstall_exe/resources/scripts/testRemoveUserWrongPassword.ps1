$ericssonModules = "C:\Ericsson\NetAnServer\Modules"

if ( -not $env:PsModulePath.Contains($ericssonModules)) {
    $env:PSModulePath = $env:PSModulePath + ";$($ericssonModules)"
}

Import-Module SQLPS
Import-Module ManageUsersUtility

$platformPassword = "WrongPassword"
$NewUser = "NewUser05"
$Password = "NewPassword01"
$GroupName = "Consumer"

Remove-User $NewUser $platformPassword