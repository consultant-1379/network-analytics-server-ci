# Call addConsumerUser.ps1 Script here
.("C:\netanserver_postinstall_exe\resources\scripts\addConsumerUser.ps1")
Write-Host "Consumer Added"

# Call updateConsumerPassword.ps1 Script here
.("C:\netanserver_postinstall_exe\resources\scripts\updateConsumerPassword.ps1")
Write-Host "Consumer Password Updated"

# Call addBusinessAuthor.ps1 Script here
.("C:\netanserver_postinstall_exe\resources\scripts\addBusinessAuthor.ps1")
Write-Host "Business Author Added"

# Call addBusinessAnalyst.ps1 Script here
.("C:\netanserver_postinstall_exe\resources\scripts\addBusinessAnalyst.ps1")
Write-Host "Business Analyst Added"

# Call removeConsumerUser.ps1 Script here
.("C:\netanserver_postinstall_exe\resources\scripts\promoteUserToGroup.ps1")
Write-Host "User Promoted"

# Call removeConsumerUser.ps1 Script here
.("C:\netanserver_postinstall_exe\resources\scripts\removeConsumerUser.ps1")
Write-Host "User Removed"