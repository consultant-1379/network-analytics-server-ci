$here = Split-Path -Parent $MyInvocation.MyCommand.Path

Describe "Scenarios" {

    Start-AwaitSession

    try
    {
        It "Does Something" {
            Send-AwaitCommand 'C:\network-analytics-server\src\main\scripts\Install\NetAnServer_installV2.ps1'
            Send-AwaitCommand 'Ericsson01'
            $output = Wait-AwaitResponse 
            
            #Send-AwaitCommand '"`n"*50'
            #Send-AwaitCommand '"AAA"*2'
            #$output = Wait-AwaitResponse AAAAAA
            #$output -match 'AAAAAA' | Should be $true

            #Send-AwaitCommand 'cls'
            #$null = Wait-AwaitResponse "PS"

            #Send-AwaitCommand '"BBB"*2'
            #$output = Wait-AwaitResponse BBBBBB
            #$output -match 'BBBBBB' | Should be $true


                   }
    }
    finally
    {
        Stop-AwaitSession
    }
}