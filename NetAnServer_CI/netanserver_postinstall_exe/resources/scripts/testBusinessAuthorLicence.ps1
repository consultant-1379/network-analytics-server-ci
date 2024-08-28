# script return the count of licences for Business Author
$currentLocation = Get-Location
$configToolLocation = "C:\Ericsson\NetAnServer\Server\7.9\tomcat\bin"
Set-Location $configToolLocation
$datasources = .\config.bat show-licenses -t Ericsson01 -p C:\Ericsson\NetAnServer\Logs\licenses_report_BusinessAuthor -f true
$countBusinessAuthor=Get-Content C:\Ericsson\NetAnServer\Logs\licenses_report_BusinessAuthor|select-string -pattern "Business Author" |Measure-Object -line
Set-Location $currentLocation
return "Count:$($countBusinessAuthor.Lines)"