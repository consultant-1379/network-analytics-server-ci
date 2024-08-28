$home = "C:\\netanserver_postinstall_exe"
cd C:\Ericsson\NetAnServer\Server\10.10.2\tomcat\spotfire-bin\
./config.bat export-config --force -t Ericsson01 > $home\\op.txt
./config.bat set-config-prop -n security.hsts.max-age-seconds -v 31536000 >> $home\\op.txt
./config.bat import-config -c "Enabled HSTS" -t Ericsson01 >> $home\\op.txt
Restart-Service Tss10102 -wa 0

$count = (Select-String -Path "$home\\op.txt" -Pattern "Successfully" -AllMatches).Matches.Count
if ($count -ge 3){
	return 'Successfully enabled HSTS'
}
else{
	return 'Failed to enable HSTS'
}
rm $home\\op.txt
cd $home
