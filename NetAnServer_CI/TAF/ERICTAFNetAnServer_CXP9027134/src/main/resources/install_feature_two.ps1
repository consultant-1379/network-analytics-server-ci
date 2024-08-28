param(
    [string] $server,
    [string] $feature,
    [string] $datasource
)

$currentLocation = $PSScriptRoot
$requiredModules = "$((Get-Item $currentLocation).Parent.Parent.Parent.Parent.Parent.Fullname)\modules"

if (-not $env:PsModulePath.Contains($requiredModules)) {
    $env:PsModulePath = $env:PsModulePath + ";$($requiredModules)"
}

Import-Module FeatureInstall
Install-Feature $server $feature $datasource
