function CIConfigProvider {
    param(
        [Parameter(mandatory=$true)]
        [String] $configFile
    )

    $CIConfigProvider = New-Object PsObject

    if(-not (Test-Path $configFile)) {
        throw "$($configFile) does not exist"
    }

    Add-Member -in $CIConfigProvider NoteProperty '__configFile__' $configFile
    
    
    #Function returns the virtual hostname of CI target VM
    Add-Member -InputObject $CIConfigProvider -MemberType ScriptMethod -Name getVirtualHost -Value {
       [xml]$xmlContent = (Get-Content $($this.__configFile__))
       return $xmlContent.config.'virtual-host'.name
    }

    #Function returns the Base installation requirements snapshot
    Add-Member -InputObject $CIConfigProvider -MemberType ScriptMethod -Name getInitialInstallSnapShot -Value {
       [xml]$xmlContent = (Get-Content $($this.__configFile__))
       return $xmlContent.config.'virtual-host'.'prereq-snapshot'
    }

    #Function returns the Fully installed snapshot
    Add-Member -InputObject $CIConfigProvider -MemberType ScriptMethod -Name getFullInstallSnapShot -Value {
       [xml]$xmlContent = (Get-Content $($this.__configFile__))
       return $xmlContent.config.'virtual-host'.'fullinstall-snapshot'
    }

    #Function returns the snapshot that an upgrade will be run on
    Add-Member -InputObject $CIConfigProvider -MemberType ScriptMethod -Name getUpgradeSnapShot -Value {
       [xml]$xmlContent = (Get-Content $($this.__configFile__))
       return $xmlContent.config.'virtual-host'.'upgrade-snapshot'
    }

    $CIConfigProvider
}