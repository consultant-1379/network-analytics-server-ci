#!/usr/local/bin/perl
use strict;
my $localHour;
my $localMinute;
my @months;
my @days;
my $str;
my $string;
my $SQLDateTime;
my @SQLTime;
my $SQLTotalTime;
my $localTotalTime;
my $timeDif;
my @lines;
my @SQLDateTime;
my $AMPM;
my $totalTime;
my $time;
my @timeSQL;



@months = qw( Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec );
@days = qw(Sun Mon Tue Wed Thu Fri Sat Sun);
(my $sec,my $min,my $hour, my $mday,my $mon,my $year,my $wday,my $yday,my $isdst) = localtime();
$localHour=$hour;
$localMinute=$min;

$str = "max(dc_e_volte_kpi_raw.DATETIME_ID)\n-----------------------------------\n       Dec  12 2016  9:30:00.000000AM\n\n(1 row affected)";
@lines = split /\n+/,$str;
$string=$lines[2];
$string =~ s/^\s+//;
$string =~ s/\s+$//;
@SQLDateTime = split /\s+/, $string;
$time=$SQLDateTime[3];
@SQLTime = split /[:,\s.]+/, $time;

$AMPM=$timeSQL[3];
$AMPM =~ s/0+//;
if($AMPM eq "PM"){
$SQLTime[0] =$SQLTime[0] +12;
}
$SQLTotalTime=$SQLTime[0]*60 + $SQLTime[1];
$localTotalTime=$localHour*60+$localMinute;
print"$localTotalTime\n";
print"$SQLTotalTime\n";
$timeDif=$localTotalTime-$SQLTotalTime;

