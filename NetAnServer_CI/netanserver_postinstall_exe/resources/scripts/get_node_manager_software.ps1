# script return the name of Installed Spotfire Node Manager Software

Get-WmiObject -Class Win32_Product | ForEach-Object{
    if ($_.Name -eq "TIBCO Spotfire Node Manager 7.9") {
        return $_.Name
    }
}

