$ericssonModules = "C:\Ericsson\NetAnServer\Modules"

if ( -not $env:PsModulePath.Contains($ericssonModules)) {
    $env:PSModulePath = $env:PSModulePath + ";$($ericssonModules)"
}


Import-Module ManageAdhocUsers
Import-Module SQLPS

$platformPassword = "Ericsson01"
$CIUSER = "BAnalyst01"

try {
    Add-BusinessAnalyst -u $CIUSER -p $CIUSER -pp $platformPassword 
    Invoke-PromoteUserToGroup -BusinessAuthor -u $CIUSER -pp $platformPassword
} finally {
    Remove-User -u $CIUSER -pp $platformPassword
}