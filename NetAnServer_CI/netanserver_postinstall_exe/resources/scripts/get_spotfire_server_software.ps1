# script return the name of Installed Spotfire Server Software

Get-WmiObject -Class Win32_Product | ForEach-Object{
    if ($_.Name -like "TIBCO Spotfire Server 10.10*") {
        return $_.Name
    }
}

