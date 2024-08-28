$user = 'netanserver'
$password = 'Ericsson01'
$table = 'NETWORK_ANALYTICS_FEATURE'
$database = 'netAnServer_repdb'
$server = 'localhost'
$first_column = 'a'
$insertSQL = "INSERT INTO $table 
                    ([FEATURE-NAME], [PRODUCT-ID], [RELEASE], [RSTATE], [BUILD], [LIBRARY-PATH], [STATUS])
                VALUES 
                    ('$($first_column)', 'b', 'c', 'd', 'e', 'f', 'g')"

$removeSQL = "DELETE FROM $table where [FEATURE-NAME] = '$($first_column)'"
$selectSQL = "SELECT * FROM $table"
$test_result = "failed"

Function exec-cmd() {
    param(
        [string] $query
    )
    $result = Invoke-SqlCMD -ServerInstance $server -Database $database -Username $user -Password $password -Query $query
    return $result
}


$result = exec-cmd $selectSQL

if ($result -ne $null) {
    return "$test_result - should not have data in repdb database"
}

exec-cmd -query $insertSQL
$result = exec-cmd -query $selectSQL

$isEqual = $result[0].CompareTo('a')

if ($isEqual -eq 1) {
    $test_result = "passed"
}

exec-cmd -query $removeSQL

return $test_result
