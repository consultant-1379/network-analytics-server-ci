use strict;
use parsingFuncs;
use ServiceEntry;
use Cwd;

my $sendEmails = 1;
my $mailServiceDetected = 0;
my $currentDir = "";
my $mailString = ""; #String containing mail recipients, formatted for email output
my ($zipname, $mailListPath) = @ARGV




&main();
sub main
{
	$currentDir = getcwd();
	#Read the mail list
	$mailString = &getMailListString;
	&say("Starting checks");
	#Check that the mail service is accessible
	&checkMailService;
	&sendAllEmails;
	&say("Checks finished");
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
Reads the mail list
	Returns:
		Array containing email addresses 
=cut
sub readMailList
{
	open my $fh, $mailListPath or die "Could not open mailList.txt!";
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
	Pulls data from a line of text at specified column. Delimits using dashes, dots (periods)
	colons and whitespace, by default.
Args:
	0 - String, Line of text to read data from
	1 - Number, column index - this is 0 padded, so use 1 for the first column
	2 - Number, Delimit using WS only. Leave blank or undef for standard delimit
Returns:
	Data at column specified
=cut
sub getColumnData
{
	my $lineData = $_[0];
	my $columnToPullDataFrom = $_[1];
	$lineData = &trim($lineData);
	#Older implementation of this subroutine was not zero-indexed, adjust here to keep things working.
	$columnToPullDataFrom--;
	my @dataArray;
	my $columnCount = 0;
	#Standard delimit
	if(not defined($_[2]))
	{
		#Split on spaces, dots or dashes
		#A single split will fail here given the following string:
		#	"Usage: grep -hblcnsviw pattern file . . .\n"
		#This will give a length of 6 (instead of 5), because of the dash before the
		#grep switches. The workaround is to join the string back with a pattern not 
		#likely to be seen, then splitting again on this pattern with the + option
		@dataArray = split(/&&&&&+/, join("&&&&&", split (/ +|\.|\-|:/, $lineData)));
		$columnCount = @dataArray;
		if($columnToPullDataFrom >= $columnCount)
		{
			die "Attempt to access column $columnToPullDataFrom is invalid, line only has $columnCount columns! Line:\n".$lineData."\nendl";
		}
		else
		{
			return $dataArray[$columnToPullDataFrom];
		}
	}
	#WS only delimit
	else
	{
		@dataArray = split (/ +/, $lineData);
		$columnCount = @dataArray;
		if($columnToPullDataFrom >= $columnCount)
		{
			die "Attempt to access column $columnToPullDataFrom is invalid, line only has $columnCount columns! Line:\n".$lineData."\nendl";
		}
		else
		{
			return $dataArray[$columnToPullDataFrom];
		}
	}
	die "Error in getColumnData, should not be here! Debug textParser.pm";
}
=comment
	Counts the number of columns in a line - delimits using dashes, dots (periods)
	colons and whitespace by default
Args:
		0 - String, Line of text to read from
		1 - Bool, delimit using ws only
Returns:
		int, real number of columns
=cut
sub countColumnsInLine
{	
	my $lineData = $_[0];
	my $columnCount = 0;
	$lineData = &trim($lineData);
	if(not defined($_[1]))
	{
		#Split on spaces, dots or dashes
		#A single split will fail here given the following string:
		#	"Usage: grep -hblcnsviw pattern file . . .\n"
		#This will give a length of 6 (instead of 5), because of the dash before the
		#grep switches. The workaround is to join the string back with a pattern not 
		#likely to be seen, then splitting again on this pattern with the + option
		$columnCount = split(/&&&&&+/, join("&&&&&", split (/ +|\.|\-|:/, $lineData)));
		return $columnCount;
	}
	$columnCount = split (/ +/, $lineData);
	return $columnCount;
}

sub terminate
{
	my $errTxt = "An error has caused the email alerts script to terminate:\n\n";
	$errTxt.=$_[0];
	&say($errTxt);
	$errMailString.=$errTxt;
	&sendAllEmails;
	die "Terminate called, killing script";
}






sub say
{
	if(not defined($_[1]))
	{
		print $_[0]."\n";
	}
}


sub sendAllEmails
{
	#Only send if a mail service has been detected - needed as &terminate is called when 
	#a mail server is not located
	if ($mailServiceDetected)
	{
		#Send mail to everyone on the list
		my @mailList = &readMailList;
		for(my $i = 0; $i < @mailList; $i++){
			qx(ssh dcuser\@$mailServer 2>/dev/null 'echo \"Attached are the results of the most recent run of the script\" | mailx -s \"Jython script Results\" -a zipName.zip $mailList[$i]');
		}
		&say("Mail sent to:\n\t$mailString");
	}
}
