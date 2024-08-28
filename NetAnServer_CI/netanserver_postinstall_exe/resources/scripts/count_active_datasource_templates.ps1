# script return the number of enabled datasource templates

$currentLocation = Get-Location
$configToolLocation = "C:\Ericsson\NetAnServer\Server\10.10.1\tomcat\bin"
Set-Location $configToolLocation
$datasources = .\config.bat list-ds-template | findstr true 
$activeDatasources = $datasources | measure
Set-Location $currentLocation
return "Count:$($activeDatasources.Count)"