param(
  [string] $oldPlatform,
  [string] $newPlatform
)

$ericssonModules = "C:\Ericsson\NetAnServer\Modules"

if ( -not $env:PsModulePath.Contains($ericssonModules)) {
    $env:PSModulePath = $env:PSModulePath + ";$($ericssonModules)"
}

Import-Module PlatformVersionController -DisableNameChecking

$platformVersion = (Get-PlatformVersions -FULL_HISTORY | Where-Object -FilterScript { $_.'PRODUCT-ID'.trim() -eq 'CNA4032940' })

$oldVersion = $platformVersion | Where-Object -FilterScript {$_.BUILD.trim() -eq $oldPlatform }
$isRemoved = $oldVersion.STATUS.trim() -eq 'REMOVED'

$newVersion = $platformVersion | Where-Object -FilterScript {$_.BUILD.trim() -eq $newPlatform }
$isActive = $newVersion.STATUS.trim() -eq 'ACTIVE'

if($isActive -and $isRemoved) {
    return "PASSED"
} else {
    return "FAILED"
}