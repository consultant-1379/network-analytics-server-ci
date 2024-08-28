# script return the count of licences for Consumer
$currentLocation = Get-Location
$configToolLocation = "C:\Ericsson\NetAnServer\Server\7.9\tomcat\bin"
Set-Location $configToolLocation
$datasources = .\config.bat show-licenses -t Ericsson01 -p C:\Ericsson\NetAnServer\Logs\licenses_report_consumer -f true
$countconsumer=Get-Content C:\Ericsson\NetAnServer\Logs\licenses_report_consumer|select-string -pattern '"Consumer";"Consumer"' |Measure-Object -line
Set-Location $currentLocation
return "Count:$($countconsumer.Lines)"