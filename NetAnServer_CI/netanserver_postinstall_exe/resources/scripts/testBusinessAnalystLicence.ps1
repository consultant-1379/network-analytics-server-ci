# script return the count of licences for Business Analyst
$currentLocation = Get-Location
$configToolLocation = "C:\Ericsson\NetAnServer\Server\7.9\tomcat\bin"
Set-Location $configToolLocation
$datasources = .\config.bat show-licenses -t Ericsson01 -p C:\Ericsson\NetAnServer\Logs\licenses_report_BusinessAnalyst -f true
$countBusinessAnalyst=Get-Content C:\Ericsson\NetAnServer\Logs\licenses_report_BusinessAnalyst|select-string -pattern "Business Analyst" |Measure-Object -line
Set-Location $currentLocation
return "Count:$($countBusinessAnalyst.Lines)"