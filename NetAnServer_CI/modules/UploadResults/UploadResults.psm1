Import-Module Logger

$logger = Get-Logger($LoggerNames.Install)
function Start-Sftp {
    param(
        [string] $ip,
        [string] $user,
        [string] $remotePath,
        [string] $localFilePath
    )

        $logger.logInfo("Starting sftp to Radiator in following directory $remotePath", $True)

    try {
        $logger.logInfo("Attempting to sftp from $localFilePath", $True)
        $key = "C:\users\NetanServer\.ssh\id_rsa"
        $sftp = Open-SFTPServerWithPublicKey -serverAddress $ip -userName $user $key

        Get-ChildItem $localFilePath -Filter "*.zip" | ForEach-Object {
            if ($sftp.Connected) {
                $sftp.Put($_.FullName, $remotePath)
                 $logger.logInfo("sftp done on $ip", $True)
            } else {
                $logger.logError("$ip could not be connected", $True)
            }
        }
    } catch {
            $logger.logError($MyInvocation, "sftp did not execute successfully $_.Exception.Message", $True)

        }
}