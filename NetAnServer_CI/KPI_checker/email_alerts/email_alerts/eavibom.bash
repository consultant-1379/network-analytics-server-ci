#!/usr/bin/bash
#Bash file that executes the SQL commands passed to it.
#-U=Username, -P=Password, -S=Servername -b=Disables the display of the table headers output. $1=The first variable passed to the file ie. The SQL command
iqisql -Udc -Pdc -Sdwhdb -w200 -b <<EOF
$1
go
EOF