=comment
><><><><><><><><><><><><
Used to monitor file system load on servers
Should be ran from co-ordinator
Switches (precede with dash, group into one if passing from shell script)
	q : print email text to console rather than send emails
	c : send an email to confirm any checks succeeded, even if there are no problems
	t : set networkCommandTimeout to 1 second (rather than defined value)
	s : check services
	l : check disk usage - local & NAS
	m : check dmesg output
	w : run check for any (system-Wide) services which have entered maintenance mode, if checking services
	a : execute additional scripts
	h : help
	d : check the most recent value for Datetime_ID
	e : check if any licenses have expired on the server
Usage: perl checkServers.pl -qctslmwhS
><><><><><><><><><><><><
=cut

use strict;
use parsingFuncs;
use ServiceEntry;
use Cwd;

##########################
#Config fields - the values for these are imported from the config file. Look there for a description.
our $rootFileSystemLoadTolerance;
our $NASLoadTolerance;
our $ZFSLoadTolerance;
our $mailServer;
our $coordServer;
our $deploymentName;
our $networkCommandTimeout;
our $loadingConstant;

#Ignore list - will not try to ssh into any servers on this list.
#Used for testing, can be left empty for deployment
our @serverIgnoreList = ();

#Servers to check which aren't defined in service_names
#Used for testing, can be left empty for deployment
our @additionalServersToCheck = ();
##########################

my $sendEmails = 1;
my $checkSvcs = 0;
my $checkLoad = 0;
my $checkMessagesVar = 0;
my $checkMaintenanceSvcs = 0;
my $executeAdditionalScriptsVar = 0;
my $useQuickTimeout = 0;
my $checkDatetimeVal = 0;
my $checkLicensesVal =0;
#These strings are used to store results of checks. When emails are sent, these are 
#checked; a non-empty string indicates a message needs to be sent
my $serverLoadMailString = ""; #Results of root load check
my $servicesMailString = ""; #Results of services check
my $errMailString = ""; #Holds any error messages generated
my $messagesOutput = ""; # Results of dmesg checks
my $checkDatetimeOutput=""; #Results of DataLoading checks
my $checkLicensesOutput="";#Results of license check
my $additionalScriptsOutput = ""; #Output from execution of additional scripts
my $sendOkMail = 0;
my $mailServiceDetected = 0;
my $currentDir = "";
my $mailString = ""; #String containing mail recipients, formatted for email output
my $servicesObjArrPtr;

&main();

#########################################
#	Functions
#########################################
sub main
{
	$currentDir = getcwd();
	
	#Import config fields from config file
	&readConfigFile;
	
	#Load parameters passed to this script
	&initParams;
	
	#Dataloading check is performed by finding the max datetime value found in a table using a user defined SQL command
	if($checkDatetimeVal)
	{
		&checkDatetime($loadingConstant);
	}
	
	#Checks if any of the licenses found on the server are expired on expiring in <30 days
	if($checkLicensesVal)
	{
		&checkLicenses;
	}
	#Read the mail list
	$mailString = &getMailListString;
	&say("Starting checks");
	#Check that the mail service is accessible
	&checkMailService;
	
	#Messages are checked on the co-ord here as execution may terminate before the normal message 
	#check is ran, e.g. if NAS is down
	if($checkMessagesVar)
	{
		&checkMessages($coordServer, 1);
	}
	#Get list of servers on this deployment
	&getServiceNamesFile;

	#Load the service settings file
	if($checkSvcs)
	{
		$servicesObjArrPtr = &readServiceSettings;
	}
	&checkServers;
	if($executeAdditionalScriptsVar)
	{
		&executeAdditionalScripts;
	}

	&sendAllEmails;
	&say("Checks finished");
}

=comment
Finds the number of days between two supplied dates and returns the result.
Args:
	0 - Shortened name of Month of first date ie. "Jan","Feb","Jul" etc.
	1 - Day of month for first date ie. 1,2,30 etc.
	2 - Year of first date ie. 2017,2015 etc.
	3 - Shortened name of Month of second date ie. "Mar","Apr","May" etc.
	4 - Day of month for first date ie. 1,2,30 etc.
	5 - Year of first date ie. 2017,2015 etc.	
=cut
sub dayDifference{

	my $a; #counter used in for loop
	my @date1; #Array to hold first date supplied
	my @date2; #Array to hold second date supplied
	
	$date1[0]=$_[0];
	$date1[1]=$_[1];
	$date1[2]=$_[2];
	
	$date2[0]=$_[3];
	$date2[1]=$_[4];
	$date2[2]=$_[5];
	my @Months = ("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sept","Oct","Nov","Dec"); #Array that holds all the names of the months
	my %MonthOrder=("Jan",1,"Feb",2,"Mar",3,"Apr",4,"May",5,"Jun",6,"Jul",7,"Aug",8,"Sept",9,"Oct",10,"Nov",11,"Dec",12);# Hash that holds the name of each month with their corresponding order number 
	my %MonthDays=("Jan",31,"Feb",28,"Mar",31,"Apr",30,"May",31,"Jun",30,"Jul",31,"Aug",31,"Sept",30,"Oct",31,"Nov",30,"Dec",31);# Hash that holds the name of each month and the corresponding number of days found in each

	my $monthIndex;# holds the value of the month index for date2
	my $nextMonth;
	my $daysSum; #Holds the value of days in the months between each of the dates. ie. doesnt include the days found in the first or last month 
	my $dayConstant;#Varible that holds the number of days between the dates
	my $endMonth; # Hold the index of the last month ie. month of date2
	
	#Logic to find days inbetween the dates
	
	#checks if the dates supplied are equal and if so gives $dayConstant a value of 0 .ie theres no days between the dates
	if($date1[0] eq $date2[0] && $date1[1] eq $date2[1] && $date1[2] eq $date2[2] ){
		$dayConstant=0;
	#Checks if the years of date1 and date2 are not equal
	}elsif ($date1[2] ne $date2[2]){
		$monthIndex=@MonthOrder{$date2[0]};
		#finds the days in the months from date2 to the end of the year
		for($a =$monthIndex-1;$a<=12;$a = $a + 1){
			$nextMonth=$Months[$a];
			#Check to see if the date2's year is a leap year
			if( 0 == $date2[2] % 4 && $nextMonth eq "Feb" && (0 != $date2[2] % 100 or 0 == $date2[2] % 400)  ){
				$daysSum=$daysSum+@MonthDays{$nextMonth}+1;
			}
			else{
				$daysSum=$daysSum+@MonthDays{$nextMonth};
			}
		}
		#If date1's year is bigger than date2's the amount of days is negative (used for the license checks only)
		if($date1[2] > $date2[2]){
			$dayConstant=+$daysSum-$date2[1];
		}
		else{
			$dayConstant=-$daysSum-$date2[1];
		}

		$daysSum=0;
		$monthIndex=@MonthOrder{$date1[0]};
		#finds the days from the start of the year to the month of date1
		for($a =$monthIndex-2;$a>=0;$a = $a - 1){
			$nextMonth=$Months[$a];
			if( 0 == $date1[2] % 4 && $nextMonth eq "Feb" && (0 != $date1[2] % 100 or 0 == $date1[2] % 400)  ){
				$daysSum=$daysSum+@MonthDays{$nextMonth}+1;
			}
			else{
				$daysSum=$daysSum+@MonthDays{$nextMonth};
			}
		}
		#Finds the difference in days adding the new $daysSum and $date1[1] to $dayConstant(The first $daysSum calculated)
		$dayConstant=$dayConstant +$daysSum+$date1[1];
	#Checks if the years of date1 and date2 are equal
	}elsif($date1[2] eq $date2[2]){
		$monthIndex=@MonthOrder{$date2[0]};
		$endMonth=@MonthOrder{$date1[0]};
		#finds the days in the months between date1 and date2
		for($a =$monthIndex-1;$a<$endMonth-1;$a = $a + 1){
			$nextMonth=$Months[$a];
			if( 0 == $date2[2] % 4 && $nextMonth eq "Feb" && (0 != $date2[2] % 100 or 0 == $date2[2] % 400)  ){
				$daysSum=$daysSum+@MonthDays{$nextMonth}+1;
			}
			else{
				$daysSum=$daysSum+@MonthDays{$nextMonth};
			}
		}
		#calculates the differnce in days by subtracting the amount of days between the start of the month and the day given in date2 and adding the days from the start of the month to the day given in day1 
		$dayConstant=$daysSum-$date2[1]+$date1[1];
	
	}
	return $dayConstant;
}
=comment
Checks if any of the services on the server licenses have expired or expiring in less than 30 days and alerts the users if there are any expiring/expired licenses
=cut
sub checkLicenses
{
	#runs the command to fetch the license information. 
	#An example output of this command is:
	#	Feature name     : CXC4011832
	#	Feature identity : FAJ 121 4592
	#	Description      : Ericsson WCG PM Tech Pack
	#	Start date       : Nov 15, 2016 12:00:00 AM
	#	Expiration date  : May 16, 2017 11:59:59 PM
	my $str = qx(licmgr -getlicinfo);
	#Creates an  array of values from spliting the above command on blacklines
	my @str1 = split(/\n{2,}/, $str);
	my $str1Len= scalar @str1; #Finds number of elements in str1 ie. how many feature there is
	my $x; #counter
	my @featureLine; #used to split the line where the name of the feature is found
	my @expirationLine; #used to split the line where the expiration date of the feature is found
	my @expirationDateArr;# used to extract the month,day of month and year from the expiration date line
	my @localDateTime;# Holds the month, day of month and year for current time
	my $featureName; # Holds the name of the feature in each iteration of the for loop
	my $expirationDate;# Holds the expiration date for the feature in each iteration of the for loop
	my $datestring= localtime(); #finds the current time
	my $dayConstant;#Holds the amount of days between the current date and the expiration date of the feature
	my @dateArray = split /\s+/, $datestring;#splits the local time string on whitespaces
	$localDateTime[0]=$dateArray[1];#current month
	$localDateTime[1]=$dateArray[2];#current day of the month
	$localDateTime[2]=$dateArray[4];#current year
	my $localTime =join ' ', @localDateTime;# string that holds the month,day of month and year of the local time
	#iterates through the array of diffent features found in the array str1
	for($x=0;$x<$str1Len;$x=$x+1){
		my @lines = split /\n/, $str1[$x];#splits the feature information on newline
		foreach my $line (@lines){
			#checks if the first column in the line is "Feature" ie. Finds the line that holds the features name. 
			#Then finds the features name by spliting the line on the char ":" and set $featureName equal.
			if(&getColumnData($line, 1) eq "Feature" && &getColumnData($line, 2) eq "name"){
			
				@featureLine= split /:/, $line;
				$featureName=$featureLine[1];
			}
			#checks if the first column in the line is "Expiration" ie. Finds the line that holds the features name.
			#then adds the month,day of month and year to an array and finds the amount of days between the expiration date and the local time found above
			if(&getColumnData($line, 1) eq "Expiration"){
				@expirationLine= split /:/, $line;
				$expirationDate=$expirationLine[1];
				$expirationDateArr[0]=&getColumnData($expirationDate, 1);
				$expirationDateArr[1]=&getColumnData($expirationDate, 2);
				$expirationDateArr[2]=&getColumnData($expirationDate, 3);
				$expirationDateArr[1]=~ s/,$//;
				$expirationDate=join ' ', @expirationDateArr;
				$dayConstant=&dayDifference(@expirationDateArr,@localDateTime);
				#If the difference of the two dates is greater than 30 days adds a line to the output string $checkLicensesOutput depending on the size of difference
				if($dayConstant <= 30){
					if($dayConstant <= 0){
						$checkLicensesOutput.="\nEXPIRED-> Feature Name: $featureName\tExpiration Date: $expirationDate\tCurrent Date: $localTime\tDays Before Expiration: $dayConstant";
					}
					else{
						$checkLicensesOutput.="\nEXPIRING->Feature Name: $featureName\tExpiration Date: $expirationDate\tCurrent Date: $localTime\tDays Before Expiration: $dayConstant";
					}
				}
			}
		}		
		
	}
}
sub checkDatetime
{
	my $datetimeLine;#holds the line that conatains the max datetime value when an SQL command is executed
	my @SQLTime;
	my $SQLTotalTime;
	my $localTotalTime;
	my $timeDif;
	my @lines;
	my $AMPM;
	my $time;
	my $string;#Holds the line that conatains the Date returned from the SQL execution
	my @localDateTime;
	my @SQLDateTime;
	my @monthArray;
	my $dayConstant;
	open my $fh, "../SQLCmds" or die "Could not open config!";#opens file containing the SQLs and the time constants
	my @fileContents = <$fh>;#reads the files
	close $fh;
	#parses through the files contents line by line
	for(my $i = 0; $i < @fileContents; $i++)
	{
		if(substr($fileContents[$i], 0, 1) ne "#"){

			my @param = split /,/, $fileContents[$i];#splits the line on the comma
			my $sql=$param[0];#holds the sql command for that line
			my $timeConstant=$param[1];#holds the time constant for that SQL command	
			
			my $datestring= localtime();#finds the current time
			my @dateArray = split /\s+/, $datestring;# splits the current date time on whitespaces
			my $timeLocal=$dateArray[3];#Holds the time in the format ******************************************************
			my @timeLocalArray= split /[:]/,$timeLocal;#splits the time by the char ":" ie. separates hour,minute and seconds
			


			$localDateTime[0]=$dateArray[1];#Holds the current month
			$localDateTime[1]=$dateArray[2];#Holds the current day of the month
			$localDateTime[2]=$dateArray[4];#holds the  current year
			$localDateTime[3]=$timeLocalArray[0];#holds the current hour of the day
			$localDateTime[4]=$timeLocalArray[1];#holds the current minute of the current hour
			
			my $str = qx(bash eavibom.bash "$sql");#executes the SQL and returns the max datetime value found
			@lines = split /\n+/,$str;#splits the returned string to find the line with the result 
			$string=$lines[0];
			$string=&trim($string);#trims the whitespace from the start and end of the line
			#$string =~ s/^\s+//; *********************************************
			#$string =~ s/\s+$//;**************************************
			@SQLDateTime = split /\s+/, $string; #seperates the date time on whitespaces
			$time=$SQLDateTime[3];
			@SQLTime = split /[:,\s.]+/, $time;#splits the SQLs time by some delimiters
			$AMPM=$SQLTime[3];#holds either the value of "AM" or "PM"
			$AMPM =~ s/0+//;
			#if $AMPM is equal to "PM" adds 12 to the value of hours ie. converts the time to 24hr format
			if($AMPM eq "PM"){
				$SQLTime[0] =$SQLTime[0]+12;
			}
			
			$SQLDateTime[3]=$SQLTime[0];#holds the hour value returned by the SQL
			$SQLDateTime[4]=$SQLTime[1];#holds the minute value returned by the SQL
			
			$dayConstant=&dayDifference($SQLDateTime[0],$SQLDateTime[1],$SQLDateTime[2],$localDateTime[0],$localDateTime[1],$localDateTime[2]); #finds the number of days between the current datetime and the datetime found from executing the SQL
			#the times for each datetime are converted into total hours from the start of the day
			$SQLTotalTime=$SQLDateTime[3] + $SQLDateTime[4]/60;
			$localTotalTime= $dayConstant*24+$localDateTime[3]+$localDateTime[4]/60;
			$timeDif=$localTotalTime-$SQLTotalTime;#Difference in hours found between the two dates
			
			#if the gap in time is greater than the time constant given send an error report
			if ($timeDif > $timeConstant){
				$checkDatetimeOutput.="------------------------------------------------------------------------------\n  Fail!\n  SQL: $sql\n  Local Time: @localDateTime\n  SQL Database Time: @SQLDateTime\n  Max Time Gap: $timeConstant hours\n  Current Time Gap: $timeDif hours\n------------------------------------------------------------------------------\n";
			}
		}
	
	}
	
	
}
sub initParams
{
	if(@ARGV < 1)
	{
		die "No arguments supplied, use -h for help";
	}
	#Parse arguments
	for(my $i = 0; $i <@ARGV; $i++)
	{
		my $str = $ARGV[$i];
		if(substr($str, 0, 1) eq "-")
		{
			my $arg = "";
			for(my $e = 1; $e < length($str); $e++)
			{
				$arg = substr($str, $e, 1);
				if($arg eq "q")
				{
					$sendEmails = 0;
				}
				elsif($arg eq "t")
				{
					$useQuickTimeout = 1;
				}
				elsif($arg eq "c")
				{
					$sendOkMail = 1;
				}
				elsif($arg eq "s")
				{
					$checkSvcs = 1;
				}
				elsif($arg eq "l")
				{
					$checkLoad = 1;
				}
				elsif($arg eq "m")
				{
					$checkMessagesVar = 1;
				}
				elsif($arg eq "w")
				{
					$checkMaintenanceSvcs = 1;
				}
				elsif($arg eq "a")
				{
					$executeAdditionalScriptsVar = 1;
				}
				elsif($arg eq "d")
				{
					$checkDatetimeVal = 1;
				}
				elsif($arg eq "e")
				{
					$checkLicensesVal = 1;
				}

				elsif($arg eq "h")
				{
					my $text = <<STR;
><><><><><><><><><><><><
Used to monitor file system load & services on servers
Should be ran from co-ordinator
Switches (precede with dash, group into one if passing from shell script)
	q : print email text to console rather than send emails
	c : send an email to confirm any checks succeeded, even if there are no problems
	t : set networkCommandTimeout to 1 second (rather than defined value)
	s : check services
	l : check disk usage - local & NAS
	m : check dmesg output
	w : run check for any (system-Wide) services which have entered maintenance mode, if checking services
	a : execute additional scripts
	h : help
	d : check the most recent value for Datetime_ID
	e : check if any licenses have expired on the server
Usage: perl checkServers.pl -qctslmwhS
><><><><><><><><><><><><
STR
					&say($text);
					exit 0;
				}
				else
				{
					die "Invalid switch \"$arg\", use -h for help";
					
				}
			}
		}
		else
		{
			die "Invalid switch \"$str\", use -h for help";
		}
	}
	if($checkMessagesVar == 0 && $checkLoad == 0 && $checkSvcs == 0 && $executeAdditionalScriptsVar == 0 && $checkDatetimeVal == 0 && $checkLicensesVal == 0) 
	{
		die "No checks specified, use -h for help";
	}
}

=comment
	Kills the program and sends an error email
	Args:
		0 - Error text - this will be sent in the email
=cut
sub terminate
{
	my $errTxt = "An error has caused the email alerts script to terminate:\n\n";
	$errTxt.=$_[0];
	&say($errTxt);
	$errMailString.=$errTxt;
	&sendAllEmails;
	die "Terminate called, killing script";
}

=comment
Adds the provided text to the error report, which is mailed at program completion.
If this is called before the mail service is validated, output will be directed to stdout.
Does not interrupt execution
=cut
sub reportError
{
	my $errTxt.=$_[0].="\n\n";
	&say($errTxt);
	$errMailString.=$errTxt;
}

=comment
Tests if a server is up by logging into it and echoing back a message
When this is called the mail service should have been validated
Returns:
	1 if server can be reached, else 0
=cut
sub probeServer
{
	say "Probing server $_[0]";
	#Silence stderr here to hide the banner message ; will also silence any
	#other errors. If connection fails, echo will also fail. The drawback here
	#is the specific error cannot be reported
	#my $result = qx(ssh dcuser\@$_[0] 2>/dev/null echo success );
	my $result = &executeWithTimeout("ssh dcuser\@$_[0] 2>/dev/null 'echo success'");
	if (not defined $result or (defined $result and $result eq ""))
	{
		&reportError("SSH connection to $_[0] from $coordServer failed; please check this server. It may be inaccessible, or the host keys may need to be re-confirmed.");
		return 0;
	}
	&say("Server $_[0] is online");
	return 1;
}

#Attempts to retrieve the service_names file from NAS
#If this fails, it can be assumed NAS is down
sub getServiceNamesFile
{
	#Copy the service names to this directory
	#If eq blank str, operation succeeded.
	&say("Copying service names file");
	my $removeResult = qx(rm service_names);
	if($removeResult ne "")
	{
		&terminate("Command \"rm service_names\" failed in email_alerts directory; could not remove local service_names file, disk checks cannot continue until this is fixed!\n\n$removeResult");
	}
	&say("Old service names file deleted");
	my $copyResult = &executeWithTimeout("cp /eniq/sw/conf/service_names . ");
	#If the cp failed due to file not existing (rather than NAS down) this is where it should be caught
	#if $copyResult not defined : cp command timed out
	#if $copyResult defined and not an empty string : cp failed due to OS error, e.g not found, permissions, etc.
	if(not defined $copyResult or (defined $copyResult and $copyResult ne ""))
	{
		&terminate("Could not copy service_names file:\n\n$copyResult\n\nNAS may be offline, disk checks cannot continue until this is fixed!\n\n");
	}
	#Sanity check
	my $grepResult = qx(ls -a | grep service_names);
	if($grepResult eq "")
	{
		&terminate("File service_names could not be found locally - the file failed to copy. NAS may be offline, disk checks cannot continue until this is fixed!\n\n");
	}
	&say("File copied");
}

=comment
Checks latest messages. This works by first appending to the file all of
the dmesg output from today. The contents are then parsed - duplicated entries are 
ignored; any values that are only present in the file once are considered new
and are mailed. 
The file is then re-wrote, with any values with old timestamps (ie not today or yesterday) deleted

Args:
	0 - server to check. dmesg will be ran on this server, but it's output will be stored locally
	1 - bool, run check locally, i.e. ignore $_[0]
=cut
sub checkMessages
{
	&say("\tChecking dmesg on $_[0]");
	#Write the latest results to the messages file
	#Command needs to be broken up as much as possible for qx to run it properly
	#Start by building date stamps
	my $today = &trim(qx(date +"%e"));
	my $thisMonth = &trim(qx(date +"%b"));
	my $yesterday = int($today) - 1;
	#Pad the string correctly
	my $yesterdayStamp = $yesterday < 10 ? $thisMonth."  ".$yesterday : $thisMonth." ".$yesterday;
	my $todayStamp = int($today) < 10 ? $thisMonth."  ".$today : $thisMonth." ".$today;
	
	#This should be wrapped in quotes so grep handles it properly
	my $systemYear = "\"".qx(date +"%Z %Y");
	$systemYear = &trim($systemYear);
	$systemYear.="\"";
	
	#Append all messages to the relevant messages file
	if(defined($_[1]) && $_[1])
	{
		qx(dmesg | egrep "$yesterdayStamp|$todayStamp" | grep -v $systemYear >> messages_$_[0]);
	}
	else
	{
		qx(ssh dcuser\@$_[0] 2>/dev/null 'dmesg | egrep "$yesterdayStamp|$todayStamp" | grep -v $systemYear' >> messages_$_[0]);
	}
	
	#Read the messages file
	my $fh;
	open $fh, "messages_$_[0]" or undef($fh);
	if(not defined $fh)
	{
		&reportError("Could not open messages file messages_$_[0].");
		return;
	}
	my @contentsArray = <$fh>;
	close $fh;
	my @uniqueValsArray;
	
	#Filter duplicate values out; any values that are not duplicated are new and should be mailed
	messagesLabelB:
	for(my $e = 0; $e < @contentsArray; $e++)
	{
		my $duplicateCount = 0;
		for(my $ee = 0; $ee < @contentsArray; $ee++)
		{
			if($contentsArray[$e] eq $contentsArray[$ee])
			{
				$duplicateCount++;
				if($duplicateCount > 1)
				{
					next messagesLabelB;
				}
			}
		}
		#Check that the datestamp for this message is from today or yesterday
		if(substr($contentsArray[$e], 0, 6) eq $todayStamp || substr($contentsArray[$e], 0, 6) eq $yesterdayStamp )
		{
			push @uniqueValsArray, $contentsArray[$e];
		}
	}
	
	#Overwrite the messages file
	if(defined($_[1]) && $_[1])
	{
		qx(dmesg | egrep "$yesterdayStamp|$todayStamp" | grep -v $systemYear > messages_$_[0]);
	}
	else
	{
		qx(ssh dcuser\@$_[0] 2>/dev/null 'dmesg | egrep "$yesterdayStamp|$todayStamp" | grep -v $systemYear' > messages_$_[0]);
	}
	
	#Mail any unique messages
	my $msgStr = "";
	if(@uniqueValsArray > 0)
	{
		$msgStr.="The following server messages have been generated on $_[0] since this check was ran last:\n\n------------------------\n\n"
	}
	for(my $i = 0; $i < @uniqueValsArray; $i++)
	{
		$msgStr.=$uniqueValsArray[$i]."\n";
	}
	if($msgStr ne "")
	{
		$msgStr.="\n\n------------------------\n\n";
		&say("\t\tFinished checking messages file. Messages to report, sending mail");
		$messagesOutput.=$msgStr;
	}
	else
	{
		&say("\t\tFinished checking messages file. No messages to report, not sending mail");
	}
	
	&say("\tFinished dmesg check on $_[0]");
}

=comment
Checks if the mail service is installed and running on the specified mail server
=cut
sub checkMailService
{
	&say("Checking mail service");
	#Check if the server is reachable
	if(!&probeServer($mailServer))
	{
		die "Mail server is not reachable!";
	}
	my $result = qx(ssh dcuser\@$mailServer 2>/dev/null 'svcs -a | grep smtp:sendmail');
	if($result eq "")
	{
		die "No mail service installed on $mailServer";
	}
	#$result should look like this:
	#online         Jul_11   svc:/network/smtp:sendmail
	if(&countColumnsInLine($result) >= 1 && &getColumnData($result, 1) ne "online")
	{
		die "SMTP service is not online on $mailServer! Aborting";
	}
	&say("Mail service running on $mailServer");
	$mailServiceDetected = 1;
}

=comment
Reads the service names file and get unique names
Returns:
	Array containing unique server names
=cut
sub readServiceNames
{
	#Read the file
	open my $fh, "service_names" or &terminate("Error reading service names file!");
	my @fileContents = <$fh>;
	#Grep through the file data for valid server names
	@fileContents = grep {
   							 $_ !~ /^\s*$/ && substr($_, 0, 1) ne "#" && 
   							 &countColumnsInLine($_) >= 5 &&
   							 substr(&getColumnData($_, 5), 0, 2) eq "at"
   	} @fileContents;
	
	my $i = 0;
	my @serverNamesArray;
	
	#Loop through lines of file and pull unique values into @serverNamesArray
	loopLabel:
	while($i < @fileContents)
	{
		#line will look something like this:
		#10.45.193.38::atrcxb1399::dwhdb
		my $serverName = &getColumnData($fileContents[$i], 5); 
		#Check that the entry hasn't already been added
		for(my $e = 0; $e <= @serverNamesArray-1; $e++)
		{
			if($serverNamesArray[$e] eq $serverName)
			{
				$i++;
				next loopLabel;
			}
		}
		#Value is unique, safe to add
		push @serverNamesArray, $serverName;
	    $i++;
	}
	#Add any additionally defined servers
	push @serverNamesArray, @additionalServersToCheck;

	return @serverNamesArray;
}
=comment
Checks through all the servers and sends emails if neccessary
=cut
sub checkServers
{
	my @serverNames = &readServiceNames;
	&say("Starting server check");
	OuterLabel:
	for(my $i = 0; $i < @serverNames; $i++)
	{
		for(my $e = 0; $e < @serverIgnoreList; $e++)
		{
			if($serverNames[$i] eq $serverIgnoreList[$e])
			{
				&say("Ignoring $serverNames[$i]..");
				next OuterLabel;
			}
		}
		#Make sure the server is reachable
		if(&probeServer($serverNames[$i]))
		{
			&say("Checking $serverNames[$i]..");
			if($checkSvcs)
			{	
				&checkServerServices($serverNames[$i]);
			}
			if($checkLoad)
			{
				&checkRootLoad($serverNames[$i]);
				&checkZFSLoad($serverNames[$i]);
			}
			if($checkMessagesVar)
			{
				#messages on the co-ord were already checked above, see comment at top of file
				if($serverNames[$i] ne $coordServer)
				{
					&checkMessages($serverNames[$i]);
				}
			}
			&say("..Finished checking $serverNames[$i]");
		}
	}
	#NAS only needs to be checked once
	if($checkLoad)
	{
		&checkNASLoad;
	}
	&say("Finished server check");
}

=comment
Checks all services as defined in services_config, as well as a system wide maintenance check
	Params:
			0 - name of the server (eg atrcxb1399)
=cut
sub checkServerServices
{
	my $serverName = $_[0];
	#Find relevant services for this server
	my @servicesObjArr = @$servicesObjArrPtr;
	my $serverFound = 0;
	#Vars storing result of grep queries
	my $onlineServicesQueryResult = "";
	my $disabledServicesQueryResult = "";
	my $offlineServicesQueryResult = "";
	my $legacyrunServicesQueryResult = "";
	
	my $message = "";
	my $sendMail = 0;
	#Loop through array until the current server is found
	for(my $i = 0; $i < @servicesObjArr; $i++)
	{
		my $currentObj = $servicesObjArr[$i];
		if($currentObj->getServerName() eq $serverName)
		{
			my $servicesGrepQuery;
			$serverFound = 1;
			#Online services
			my $servicesArrayPtr = $currentObj->getOnlineServicesPtr();
			if(defined($servicesArrayPtr))
			{
				#Build the grep command from all of the services
				$servicesGrepQuery = $currentObj->getGrepString("online");
				&say("\tOnline services query: ".$servicesGrepQuery);
				#Now that the query has been built, run it
				$onlineServicesQueryResult = qx(ssh dcuser\@$serverName 2>/dev/null ' $servicesGrepQuery ');
				#If data was returned, mail it
				if ($onlineServicesQueryResult ne "")
				{
					$message.="The following services are not online on $serverName:\n\n$onlineServicesQueryResult\n\n";
					$sendMail = 1;
				}
			}
			#Disabled services
			$servicesArrayPtr = $currentObj->getDisabledServicesPtr();
			if(defined($servicesArrayPtr))
			{
				$servicesGrepQuery = $currentObj->getGrepString("disabled");
				say("\tDisabled services query: ".$servicesGrepQuery);
				$disabledServicesQueryResult = qx(ssh dcuser\@$serverName 2>/dev/null ' $servicesGrepQuery ');
				if ($disabledServicesQueryResult ne "")
				{
					$message.="The following services are not disabled on $serverName:\n\n$disabledServicesQueryResult\n\n";
					$sendMail = 1;
				}
			}
			#Offline services
			$servicesArrayPtr = $currentObj->getOfflineServicesPtr();
			if(defined($servicesArrayPtr))
			{
				$servicesGrepQuery = $currentObj->getGrepString("offline");
				&say("\tOffline services query: ".$servicesGrepQuery);
				$offlineServicesQueryResult = qx(ssh dcuser\@$serverName 2>/dev/null ' $servicesGrepQuery ');
				if ($offlineServicesQueryResult ne "")
				{
					$message.="The following services are not offline on $serverName:\n\n$offlineServicesQueryResult\n\n";
					$sendMail = 1;
				}
			}
			#Legacy run
			$servicesArrayPtr = $currentObj->getLegacyRunServicesPtr();
			if(defined($servicesArrayPtr))
			{
				$servicesGrepQuery = $currentObj->getGrepString("legacy");
				&say("\tlegacy_run services query: ".$servicesGrepQuery);
				$legacyrunServicesQueryResult = qx(ssh dcuser\@$serverName 2>/dev/null ' $servicesGrepQuery ');
				if ($legacyrunServicesQueryResult ne "")
				{
					$message.="The following services are not in legacy_run on $serverName:\n\n$legacyrunServicesQueryResult\n\n";
					$sendMail = 1;
				}
			}
		}
	}
	#If the server hasn't been found, report an error
	if(!$serverFound)
	{
		&reportError("Error checking services:\n\nServer $serverName has no entry in services_config - check that the entry is formatted correctly.");
		return;
	}
	#Run a system wide check for services in maintenance
	my $systemwideServiceResults = "";
	if($checkMaintenanceSvcs)
	{
		$systemwideServiceResults = qx(ssh dcuser\@$serverName 2>/dev/null 'svcs -a | grep maintenance');	
		if ($systemwideServiceResults ne "")
		{
			$message.="The following system wide services are in maintenance on $serverName:\n\n$systemwideServiceResults\n\n";
			$sendMail = 1;
		}
	}

	#Check that ddc and roll-snap are online
	my $miscServices = qx(svcs -a | egrep -i 'svc:/ericsson/eric_monitor/ddc:|svc:/eniq/roll-snap:' | egrep -v online);
	if ($miscServices ne "")
	{
		$message.="The following services are not online on $serverName (this check was only ran for ddc and roll-snap):\n\n$miscServices\n\n";
		$sendMail = 1;
	}
	
	#If all of these strings are empty, all services are in the required states
	if($systemwideServiceResults eq "" and $onlineServicesQueryResult eq "" and $miscServices eq ""
		 and $disabledServicesQueryResult eq "" and $offlineServicesQueryResult eq "" and $legacyrunServicesQueryResult eq "")
	{
		#All good, no email needed
		&say ("\tAll services on $serverName ok");
		return;
	}

	if($sendMail)
	{
		$message.="----------------------------\n\n";
		&say ("\tServices on $serverName not ok, sending mail");
		$servicesMailString.="Check Services on $serverName!\n\n$message";
	}
}

=comment
Checks the root file system load (capacity column) and sends an email if necessary
	Params:
			0 - name of the server (eg atrcxb1399)
=cut
sub checkRootLoad
{
	my $serverName = $_[0];
	my $fileSystemLoadStr = &executeWithTimeout("ssh dcuser\@$serverName 2>/dev/null 'df -hl /dev/md/dsk/'");
	if(not defined $fileSystemLoadStr)
	{
		&reportError("Error checking root load:\n\ndf -h command failed to respond after $networkCommandTimeout seconds on $serverName when checking root load. If this behaviour continues it should be investigated.");
		&say("\tRoot load could not be checked on $serverName, sending mail");
		return;
	}
	#Pull the load percentage from the string
	#Should be getting input in a string something like this:
	#	Filesystem             size   used  avail capacity  Mounted on
	#	/dev/md/dsk/d70         12G   7.2G   4.5G    62%    /
	my $fileSystemLoadValue = &getColumnData($fileSystemLoadStr, 11, 1);
	my $lengthParam = length($fileSystemLoadValue);
	#Sanity check
	if(substr($fileSystemLoadValue, $lengthParam - 1, 1) eq "%")
	{
		if(int(substr($fileSystemLoadValue, 0, $lengthParam)) >= $rootFileSystemLoadTolerance)
		{
			&say ("\tRoot load on $serverName not ok, sending mail");
			#Send email
			$serverLoadMailString.="Root file system load on $serverName is $fileSystemLoadValue!\n\n";
			return;
		}
		else
		{
			&say ("\tRoot load on $serverName ok ($fileSystemLoadValue)");
		}
	}
	else
	{
		&reportError("Error parsing root load results:\n\nPercentage load value not found in substring:\n$fileSystemLoadValue\nof:\n$fileSystemLoadStr\nLength of sub:\n$lengthParam\n");
	}
}

=comment
Checks the load on all NAS mounts (capacity column) and sends an email if necessary
This check is ran from the local machine (i.e. the co-ordinator)
=cut
sub checkNASLoad
{
	my $NASDataStr = &executeWithTimeout("df -h | grep nas");
	if(not defined($NASDataStr))
	{
		&reportError("Error checking NAS:\n\ndf -h command failed to respond after $networkCommandTimeout seconds on $coordServer when checking NAS load. If this behaviour continues it should be investigated.");
		&say("\tNAS load could not be checked from $coordServer, sending mail");
		return;
	}
	
	#Dereference the returned array pointer
	my @NASData = @{&splitToArray($NASDataStr)};
	for(my $i = 0; $i < @NASData; $i++)
	{
		#Line of NAS output (ie element of array) will look like this:
		#nas1:/vx/events1-admin   2.0G   164M   1.8G     9%    /eniq/admin

		my $NASLoad = &getColumnData($NASData[$i], 5, 1); #The load on the current mount
		if(substr($NASLoad, length($NASLoad) -1 , 1) eq "%")
		{
			#Name of NAS mount
			my $NASString = &getColumnData($NASData[$i], 1, 1);
			if(int(substr($NASLoad, 0, length($NASLoad - 1))) >= $NASLoadTolerance)
			{
				&say ("\tNAS load on $NASString at $coordServer not ok, sending mail");
				$serverLoadMailString.="Load on $NASString is $NASLoad (checked from $coordServer)!\n\n";
				#say "Email: Check NAS load on $coordServer!, Load on $NASString is $NASLoad!"
			}
			else
			{
				&say ("\tNAS load on $NASString at $coordServer ok ($NASLoad)");
			}
		}
		else
		{
			&reportError("Error parsing NAS results:\n\nPercentage load value not found in sub string:\n$NASLoad\nof:\n$NASData[$i]\n");
		}
	}	
}

=comment
Checks the ZFS mount loads on the specified server and sends an email if needed
Params:
	0 - name of server to check
=cut
sub checkZFSLoad
{
	my $serverName = $_[0];
	#my $ZFSDataStr = &executeWithTimeout("ssh dcuser\@$serverName 2>/dev/null 'df -hl | egrep \"^eniq_sp_1 |^eniq_ui_pool |^eniq_mz_pool |^eniq_iqr_pool |^eniq_coordinator_pool \"'");
	my $ZFSDataStr = &executeWithTimeout("ssh dcuser\@$serverName 2>/dev/null 'df -hl | grep \"eniq\"'");
	if(not defined($ZFSDataStr))
	{
		&reportError("Error checking ZFS:\n\ndf -h command failed to respond after $networkCommandTimeout seconds on $serverName when checking ZFS load. If this behaviour continues it should be investigated.");
		&say("\tZFS load could not be checked on $serverName, sending mail");
		return;
	}
	
	#Dereference the returned array pointer
	my @ZFSData = @{&splitToArray($ZFSDataStr)};
	for(my $i = 0; $i < @ZFSData; $i++)
	{
		#Line of ZFS output (ie element of array) will look like this:
		#eniq_coordinator_pool/dwh_main    16G   208M    13G     2%    /eniq/database/dwh_main
		my $ZFSLoad = &getColumnData($ZFSData[$i], 5, 1);
		#Sanity check
		if(substr($ZFSLoad, length($ZFSLoad - 1), 1) eq "%")
		{
			my $ZFSString = &getColumnData($ZFSData[$i], 1, 1);
			if(int(substr($ZFSLoad, 0, length($ZFSLoad - 1))) >= $ZFSLoadTolerance)
			{
				&say ("\tZFS load on $ZFSString at $serverName not ok, sending mail");
				$serverLoadMailString.="Load on $ZFSString at $serverName is $ZFSLoad!\n\n";
			}
			else
			{
				&say ("\tZFS load on $ZFSString at $serverName ok ($ZFSLoad)");
			}
		}
	}	
}

=comment
Sends emails or writes to console
=cut
sub sendAllEmails
{
	my $allOkString;
	#If any of the mail strings have any data in them, add mail footers
	if($serverLoadMailString ne "")
	{
		$serverLoadMailString.="----------------------------\n\n".
		"Root system tolerance: $rootFileSystemLoadTolerance\%".
		"\n\nNAS tolerance: $NASLoadTolerance\%".
		"\n\nZFS tolerance: $ZFSLoadTolerance\%".
		"\n\n----------------------------".
		"\n\nA log file has been generated at $currentDir/cronResult.txt".
		"\n\nThis message was sent to:\n\n\t$mailString";
	}
	if($messagesOutput ne "")
	{
		$messagesOutput.="A log file has been generated at $currentDir/cronResult.txt".
		"\n\nThis message was sent to:\n\n\t$mailString";
	}
	if($servicesMailString ne "")
	{
		$servicesMailString.="A log file has been generated at $currentDir/cronResult.txt".
		"\n\nThis message was sent to:\n\n\t$mailString";
	}
	if($errMailString ne "")
	{
		$errMailString.="A log file has been generated at $currentDir/cronResult.txt".
		"\n\nThis message was sent to:\n\n\t$mailString";
	}
	if($additionalScriptsOutput ne "")
	{
		$additionalScriptsOutput.="A log file has been generated at $currentDir/cronResult.txt".
		"\n\nThis message was sent to:\n\n\t$mailString";
	}
	if($checkDatetimeOutput ne "")
	{
		$checkDatetimeOutput.="\nA log file has been generated at $currentDir/cronResult.txt".
		"\n\nThis message was sent to:\n\n\t$mailString";
	
	}
	if($checkLicensesOutput ne "")
	{
		$checkLicensesOutput.="\n\nA log file has been generated at $currentDir/cronResult.txt".
		"\n\nThis message was sent to:\n\n\t$mailString";
	
	}

	
	#If all strings are empty, checks came back ok. Send confirmation mail if appropriate
	if($servicesMailString eq "" && $serverLoadMailString eq "" && $errMailString eq "" && $messagesOutput eq "" && $additionalScriptsOutput eq "" && $checkDatetimeOutput eq "" && $checkLicensesOutput eq "")
	{
		if(!$sendOkMail)
		{
			#No errors to report, no confirmation requested; cant exit here.
			&say("No mail sent");
			return;
		}
		&say("All ok, sending mail");
		$allOkString.="All services, loads and checks are ok. This mail was sent to confirm that the email system is up.\n\nA log file has been generated at $currentDir/cronResult.txt".
		"\n\nThis message was sent to:\n\n\t$mailString";
	}
	#Running in quiet mode - email text should go to console only.
	if(!$sendEmails)
	{
		&say("EMAIL: \n><><><><><><><><><><><\n------------\n$deploymentName: Check server load\n------------\n\n$serverLoadMailString\n><><><><><><><><><><><\n");
		&say("EMAIL: \n><><><><><><><><><><><\n------------\n$deploymentName: Check services\n------------\n\n$servicesMailString\n><><><><><><><><><><><\n");
		&say("EMAIL: \n><><><><><><><><><><><\n------------\n$deploymentName: Mail script error\n------------\n\n$errMailString\n><><><><><><><><><><><\n");
		&say("EMAIL: \n><><><><><><><><><><><\n------------\n$deploymentName: Server messages\n------------\n\n$messagesOutput\n><><><><><><><><><><><\n");
		&say("EMAIL: \n><><><><><><><><><><><\n------------\n$deploymentName: Mail system OK\n------------\n\n$allOkString\n><><><><><><><><><><><\n");
		&say("EMAIL: \n><><><><><><><><><><><\n------------\n$deploymentName: Additional Script Output\n------------\n\n$additionalScriptsOutput\n><><><><><><><><><><><\n");
		&say("EMAIL: \n><><><><><><><><><><><\n------------\n$deploymentName: Check dataloading\n------------\n\n$checkDatetimeOutput\n><><><><><><><><><><><\n");
		&say("EMAIL: \n><><><><><><><><><><><\n------------\n$deploymentName: Check licenses\n------------\n\n$checkLicensesOutput\n><><><><><><><><><><><\n");

	}
	#Only send if a mail service has been detected - needed as &terminate is called when 
	#a mail server is not located
	elsif ($mailServiceDetected)
	{
		#Send mail to everyone on the list
		my @mailList = &readMailList;
		for(my $i = 0; $i < @mailList; $i++)
		{
			if($serverLoadMailString ne "")
			{
				qx(ssh dcuser\@$mailServer 2>/dev/null 'echo \"$serverLoadMailString\" | mailx -s \"$deploymentName: Check server load\" $mailList[$i]');
			}
			if($servicesMailString ne "")
			{
				qx(ssh dcuser\@$mailServer 2>/dev/null 'echo \"$servicesMailString\" | mailx -s \"$deploymentName: Check services\" $mailList[$i]');
			}
			if($errMailString ne "")
			{
				qx(ssh dcuser\@$mailServer 2>/dev/null 'echo \"$errMailString\" | mailx -s \"$deploymentName: Mail script error\" $mailList[$i]');
			}
			if($allOkString ne "")
			{
				qx(ssh dcuser\@$mailServer 2>/dev/null 'echo \"$allOkString\" | mailx -s \"$deploymentName: Mail system OK\" $mailList[$i]');
			}
			if($messagesOutput ne "")
			{
				qx(ssh dcuser\@$mailServer 2>/dev/null 'echo \"$messagesOutput\" | mailx -s \"$deploymentName: Deployment messages\" $mailList[$i]');
			}
			if($additionalScriptsOutput ne "")
			{
				qx(ssh dcuser\@$mailServer 2>/dev/null 'echo \"$additionalScriptsOutput\" | mailx -s \"$deploymentName: Additional script output\" $mailList[$i]');
			}
			if($checkDatetimeOutput ne "")
			{

				qx(ssh dcuser\@$mailServer 2>/dev/null 'echo \"$checkDatetimeOutput\" | mailx -s \"$deploymentName: Check dataloading\" $mailList[$i]');
			}
			if($checkLicensesOutput ne "")
			{

				qx(ssh dcuser\@$mailServer 2>/dev/null 'echo \"$checkLicensesOutput\" | mailx -s \"$deploymentName: Check licenses\" $mailList[$i]');
			}

		}
		&say("Mail sent to:\n\t$mailString");
	}
}

=comment
Reads the mail list
	Returns:
		Array containing email addresses 
=cut
sub readMailList
{
	open my $fh, "../mailList.txt" or die "Could not open mailList.txt!";
	my @fileContents = <$fh>;
	close $fh;
	my @returnArray;
	for(my $i = 0; $i < @fileContents; $i++)
	{
		if(substr($fileContents[$i], 0, 1) ne "#" and $fileContents[$i] !~ /^\s*$/)
		{
			push @returnArray, $fileContents[$i];
		}
	}
	return @returnArray;
}

=comment
Reads the mailing list and returns it, formatted for emails
=cut
sub getMailListString
{
	my @mailList = &readMailList;
	my $returnStr;
	for(my $i = 0; $i < @mailList; $i++)
	{
		$returnStr = $returnStr.$mailList[$i]."\n\t";
	}
	return $returnStr;
}

=comment
	Reads services_config file.
	Returns:
		Pointer to array of ServiceEntry objects
=cut
sub readServiceSettings
{
	&say("Reading service settings");
	open my $fh, "../services_config" or &terminate("Could not open services_config file!\n\n");
	my @fileContents = <$fh>;
	close $fh;
	my @serviceSettingsObjs;
	
	#Loop for every line in the file
	for(my $i = 0; $i < @fileContents; $i++)
	{
		my @serversOnCurentLine = ();
		#ignore comment lines, make sure there's valid data on this line (i.e. starts with "server")
		$fileContents[$i] = &trim($fileContents[$i]);
		if(substr($fileContents[$i], 0, 1) ne "#" && substr($fileContents[$i], 0, 7) eq "server:")
		{
			#See comment in parsingFuncs::getColumnData() src for explanation of this logic; basically
			#break the line into an array, with each element being a server entry
			#Sample line:
			#	server:atrcxb2424, server:atrcxb2904,server:atrcxb2908
			@serversOnCurentLine = split(/&&&&&+/, join("&&&&&", split (/ +|,/, $fileContents[$i])));
			#Remove the server: prefix from entries, as well as any trailing ws (newlines)
			@serversOnCurentLine = grep { $_ = substr($_, 7) ; $_ =~ s/\s+$// ; 1  } @serversOnCurentLine;
		}
		if(@serversOnCurentLine > 0)
		{
			#Create new ServiceEntry object
			my $serviceEntryObj = new ServiceEntry(undef, undef, undef, undef, undef, undef); 
			while(1)
			{
				$i++;
				#Bounds check
				if($i == @fileContents)
				{
					last;
				}
				my $currentLine = &trim($fileContents[$i]);
				#Ignore this line if it's a comment or blank
				if(substr($currentLine, 0, 1) eq "#" || $currentLine =~ /^\s*$/)
				{
					next;
				}
				#In this case it's the start of a new server entry; exit this loop
				elsif(substr($currentLine, 0, 7) eq "server:")
				{
					#Decrement $i here so it's not skipped in the outer for loop
					$i--;
					last;
				}
				#There should be two columns in this line
				if(&countColumnsInLine($currentLine, 1) != 2)
				{
					&reportError("$currentLine in services_config file is incorrectly formatted.");
				}
				else
				{
					#Read the services defined on this line, add them to the object
					#Line will look something like:
					#online svc:/eniq/esm
					my $statusStr = &getColumnData($currentLine, 1, 1);
					if($statusStr eq "online")
					{
						$serviceEntryObj->addOnlineService(&getColumnData($currentLine, 2, 1));
					}
					elsif($statusStr eq "offline")
					{
						$serviceEntryObj->addOfflineService(&getColumnData($currentLine, 2, 1));
					}
					elsif($statusStr eq "disabled")
					{
						$serviceEntryObj->addDisabledService(&getColumnData($currentLine, 2, 1));
					}
					elsif($statusStr eq "legacy_run")
					{
						$serviceEntryObj->addLegancyRunService(&getColumnData($currentLine, 2, 1));
					}
					else
					{
						#Report error, bad formatting
						&reportError("$statusStr at $fileContents[$i] in services_config file is not a valid service status.");
					}
				}
			}
			#For each server on the current line, create a new object in the serviceSettingsObjs array
			for(my $e = 0; $e < @serversOnCurentLine; $e++)
			{
				my $name = $serversOnCurentLine[$e];
				my $onlineServicesPtr = $serviceEntryObj->getOnlineServicesPtr();
				my $offlineServicesPtr = $serviceEntryObj->getOfflineServicesPtr();
				my $disabledServicesPtr = $serviceEntryObj->getDisabledServicesPtr();
				my $legacyRunServicesPtr = $serviceEntryObj->getLegacyRunServicesPtr();
				#A new object needs to be created here so we don't end up with an array of duplicate objects/references
				push @serviceSettingsObjs, new ServiceEntry($name, $onlineServicesPtr, $offlineServicesPtr,
															$disabledServicesPtr, $legacyRunServicesPtr);
			}
		}
	}
	return \@serviceSettingsObjs;
}

=comment
Execute the given command. The process will be given X amount of seconds to complete,
where X is the value of $networkCommandTimeout. After this period of time the script 
kill_proc.pl will attempt to kill the process.
This is useful when running commands such as df -hk; if NAS went down that command could 
hang indefinitely, causing the script to block.
 
Args:
	0 - String, command to execute
	1 - Integer, optional argument. If specified, use this value as the command timeout
Returns:
	Undef if the command failed (timed out), otherwise any return data from the command
=cut
sub executeWithTimeout
{
	my $timeout = $networkCommandTimeout;
	#If the -t option was specified
	if($useQuickTimeout)
	{
		$timeout = 1;
	}
	elsif(defined($_[1]))
	{
		$timeout = $_[1];
	}
	#Note: when passing $_[0] to kill_proc, arguments should not be wrapped in quotes. 
	#	The following command:
	#		df -hk
	#
	#	is equivalent to (given a networkCommandTimeout value of 6):
	#
	#	$ df -hk & PID=$! ; ( sleep 6 ; perl kill_proc.pl PID df -hk ) &
	#	
	#	Note on $!:
	#		$!	Expands to the process ID of the most recently executed background (asynchronous) command.
	#	See kill_proc.pl for a continuation of this documentation
	my $cmd = "$_[0] & PID=\$! ; ( sleep $timeout ; perl kill_proc.pl \$PID $_[0] ) & ";
	my $commandOutput = qx( $_[0] & PID=\$! ; ( sleep $timeout ; perl kill_proc.pl \$PID $_[0] ) & );
	#Effectively swallowing the error message here, but there's only one scenario where it can arise
	if(substr($commandOutput, 0, 7) eq "Killing")
	{
		return undef;
	}
	return $commandOutput;
}

=comment
Reads the config file and sets the config values
=cut
sub readConfigFile
{
	open my $fh, "../config" or die "Could not open config!";
	my @fileContents = <$fh>;
	close $fh;
	my %configValues;
	for(my $i = 0; $i < @fileContents; $i++)
	{
		#Ignore comments and blank lines
		if(substr($fileContents[$i], 0, 1) ne "#" and $fileContents[$i] !~ /^\s*$/)
		{
			#See comment in parsingFuncs::getColumnData() src for explanation of this logic
			#The line will look something like this:
			#coordServer = atrcxb1399
			#The returned array will look something like this:
			#(coordServer, atrcxb1399)
			my @currentLine = split(/&&&&&+/, join("&&&&&", split (/ +|=/, $fileContents[$i])));
			$configValues{$currentLine[0]} = &trim($currentLine[1]);
		}
	}
	$rootFileSystemLoadTolerance = $configValues{"rootFileSystemLoadTolerance"};
	$NASLoadTolerance = $configValues{"NASLoadTolerance"};
	$ZFSLoadTolerance = $configValues{"ZFSLoadTolerance"};
	$mailServer = $configValues{"mailServer"};
	$coordServer = $configValues{"coordServer"};
	$deploymentName = $configValues{"deploymentName"};
	$networkCommandTimeout = $configValues{"networkCommandTimeout"};
	$loadingConstant = $configValues{"loadingConstant"};
	
}

=comment
Executes all scripts in  the additional_scripts directory. Each script must define it's own
execution timeout
=cut
sub executeAdditionalScripts
{
	&say("Executing additional scripts");
	my $contents = `ls ../additional_scripts`;
	#If there's no files in the directory
	if ($contents eq "")
	{
		return undef;
	}
	
	#Loop for everything in the directory
	foreach my $item (split(/\n/, $contents))
	{
		#If the current item is a shell script
		if(substr($item, -3) eq ".sh")
		{
			open my $fh, "../additional_scripts/$item";
			if (not defined($fh))
			{
				&reportError("Script file remote_scripts/$item could not be opened.");
				next;
			}
			#The first line will contain a shebang, the second a comment including the timeout command
			#e.g. of line 2:
			#TIMEOUT=30
			my (undef, $timeoutLine) = <$fh>;
			#if there is no timeout specified, report the error
			if($timeoutLine !~ /^#TIMEOUT=\d*$/)
			{
				&reportError("Script file remote_scripts/$item is not formatted correctly; expecting TIMEOUT definition on line 2. Aborting execution of this script");
				next;
			}
			#Get the timeout value from the comment
			my (undef, $commandTimeout) = split(/=/, $timeoutLine);
			#Will be followed by \n, need to remove this
			$commandTimeout = &trim($commandTimeout);
			$additionalScriptsOutput.="Output from script $item:\n\n-------------------\n";
			&say("\tExecuting $item");
			my $scriptOutput = &executeWithTimeout("../additional_scripts/$item 2>&1", $commandTimeout);
			#If not defined, then the command timed out
			if(not defined($scriptOutput))
			{
				$additionalScriptsOutput.="Script execution timed out, process was killed!\n\n-------------------\n";
				next;
			}
			$additionalScriptsOutput.=$scriptOutput;
			$additionalScriptsOutput.="\n\n-------------------\n";
		}
	}	
	&say("..All additional scripts executed");
}