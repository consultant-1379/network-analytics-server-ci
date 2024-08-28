## launches the adhoc bundle deployment script

Function Start-Script() {
    param(
        [string] $remoteServer,
        [string] $scriptname,
        [string] $scriptArgs
    )

    $invokeScriptSB = {
        param(
            [string]$script,
            [string]$arguments
        )
        $DRIVE = (Get-ChildItem Env:SystemDrive).value
        $installParams = @{}
        $installParams.Add('installDir', ($DRIVE) + "\Ericsson\NetAnServer")
        $installParams.Add('PSModuleDir', $installParams.installDir + "\Modules") 
        
        if(-not $env:PSModulePath.Contains($installParams.PSModuleDir)){
            $PSPath = $env:PSModulePath + ";"+$installParams.PSModuleDir
            [Environment]::SetEnvironmentVariable("PSModulePath", $PSPath, "Machine")
            $env:PSModulePath = $PSPath
        }

        powershell $script $arguments
    }

    try {
        $session = Start-PSSession $remoteServer
        Invoke-Command -Session $session -ScriptBlock $invokeScriptSB -ArgumentList $scriptname, $scriptArgs -ErrorAction Stop
        return @($True, "Remote Command $scriptname Remote Server $remoteServer executed")
   
    } catch {
        return @($False, "Error executing script $scriptname")
   
    } finally {
        if($session) {
            Remove-PSSession -Session $session
        }
    }

}
