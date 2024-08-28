$ericssonModules = "C:\Ericsson\NetAnServer\Modules"

if ( -not $env:PsModulePath.Contains($ericssonModules)) {
    $env:PSModulePath = $env:PSModulePath + ";$($ericssonModules)"
}

Import-Module SQLPS
Import-Module ManageUsersUtility

$platformPassword = "Ericsson01"
$NewUser = "NewUser06"
$Password = "NewPassword01"
$GroupName = "Consumer"

Add-User $NewUser $Password $GroupName $platformPassword
$getusers = Get-Users -pp $platformPassword

$checkUser = $getusers | Where-Object { $_.USERNAME -eq $NewUser }

$updatePassword=Update-Password -u $NewUser -p "NewPassword02" -pp $platformPassword

try{
    If ($checkUser.USERNAME.count -gt 0 -And $updatePassword -ne $False) {
        return "passed"
    } Else {
        return "failed"
    }
} Finally {
    $removeuser = Remove-User $NewUser $platformPassword
}
