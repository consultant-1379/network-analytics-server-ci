$ericssonModules = "C:\Ericsson\NetAnServer\Modules"

if ( -not $env:PsModulePath.Contains($ericssonModules)) {
    $env:PSModulePath = $env:PSModulePath + ";$($ericssonModules)"
}


Import-Module ManageAdhocUsers
Import-Module SQLPS

$platformPassword = "Ericsson01"
$CIUSER = "BAuthor01"
Add-BusinessAuthor -u $CIUSER -p $CIUSER -pp $platformPassword 
Invoke-PromoteUserToGroup -BusinessAnalyst -u $CIUSER -pp $platformPassword


$users = Get-Users -pp $platformPassword
$ciBusinessUser = $users | Where-Object { $_.USERNAME -eq $CIUSER }

$result = "failed"

try {
    $ciBusinessUser | % { if($_.GROUP -eq "Business Author") { $result = "passed" }}
    return $result
} finally {
    Remove-User -u $CIUSER -pp $platformPassword
}