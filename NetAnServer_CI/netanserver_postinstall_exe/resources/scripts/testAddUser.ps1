$ericssonModules = "C:\Ericsson\NetAnServer\Modules"

if ( -not $env:PsModulePath.Contains($ericssonModules)) {
    $env:PSModulePath = $env:PSModulePath + ";$($ericssonModules)"
}


Import-Module SQLPS
Import-Module ManageUsersUtility

$platformPassword = "Ericsson01"
$NewUser = "NewUser04"
$Password = "NewPassword01"
$GroupName = "Consumer"

Add-User $NewUser $Password $GroupName $platformPassword
$getusers = Get-Users -pp $platformPassword

$checkUser = $getusers | Where-Object { $_.USERNAME -eq $NewUser }

try{
    if($checkUser.USERNAME.count -gt 0) {
        return "passed"
    } else {
        return "failed"
}
}Finally{
    $removeuser = Remove-User $NewUser $platformPassword
}
