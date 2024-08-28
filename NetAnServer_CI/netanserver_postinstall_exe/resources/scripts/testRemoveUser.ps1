$ericssonModules = "C:\Ericsson\NetAnServer\Modules"

if ( -not $env:PsModulePath.Contains($ericssonModules)) {
    $env:PSModulePath = $env:PSModulePath + ";$($ericssonModules)"
}

Import-Module SQLPS
Import-Module ManageUsersUtility

$platformPassword = "Ericsson01"
$NewUser = "NewUser05"
$Password = "NewPassword01"
$GroupName = "Consumer"

Add-User $NewUser $Password $GroupName $platformPassword
$getusers = Get-Users -pp $platformPassword

$checkUser = $getusers | Where-Object { $_.USERNAME -eq $NewUser }

if($checkUser.USERNAME.count -eq 0) {
     return "failed"
} 

Remove-User $NewUser $platformPassword
$allusers = Get-Users -pp $platformPassword

$checkUser = $allUsers | Where-Object { $_.USERNAME -eq $NewUser }

if($checkUser.USERNAME.count -eq 0) {
     return "passed"
}  else {
    return "failed"
}