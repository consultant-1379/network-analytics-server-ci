param(
  [string] $requestType
)

$scriptUnderTest = "C:\Ericsson\NetAnServer\Scripts\backup_restore\backup_restore\service_stop_start.ps1"

if($requestType -eq "stop" ) {

    &$scriptUnderTest stop

    if($? -eq $true) {
        return "PASSED"
    } else {
        return "FAILED"
    }

} elseif ($requestType -eq "start") {

    &$scriptUnderTest start

    if($? -eq $true) {
        return "PASSED"
    } else {
        return "FAILED"
    }
} 