$ericssonModules = "C:\Ericsson\NetAnServer\Modules"

if ( -not $env:PsModulePath.Contains($ericssonModules)) {
    $env:PSModulePath = $env:PSModulePath + ";$($ericssonModules)"
}


Import-Module SQLPS
Import-Module ManageUsersUtility

$platformPassword = "Ericsson01"
$CIUSER = "CIUser03"
Add-ConsumerUser -u $CIUSER -p $CIUSER -pp $platformPassword | Out-Null
$users = Get-Users -pp $platformPassword

$ciConsumerUser = $users | Where-Object { $_.USERNAME -eq $CIUSER }

if($ciConsumerUser.GROUP -eq "Consumer") {
    Remove-User -u $CIUSER -pp $platformPassword
    return "passed"
} else {
    Remove-User -u $CIUSER -pp $plaformPassword
    return "failed"
}