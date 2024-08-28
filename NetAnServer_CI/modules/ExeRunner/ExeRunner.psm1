
#Generic function for executing exes

Function Start-EXE() {
    param(
        [string] $exeLocation,
        [string] $arguments
    )

    $processTimeout = 40000 #40 seconds
    
    try {
        $p = Start-Process -FilePath $exeLocation -ArgumentList $arguments -Verb RunAs -Passthru -ErrorAction Stop 
    } catch {
        @($False, "Error executing process $($exeLocation) $($arguments)")
    }

    if(-not $p.WaitForExit($processTimeout)) {
        @($False, "Process has timed out $($exeLocation)")
    }

    if ($p.ExitCode -eq 0) {
        return @($True, "Process $exeLocation has exited successfully")
    } else {
        return @($False, "Process $exeLocation has exited with exitcode $($p.ExitCode)")
    }
}