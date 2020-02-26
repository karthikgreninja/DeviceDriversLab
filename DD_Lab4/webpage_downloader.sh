#!/bin/sh

# the url to retrieve
URL=https://www.pokemon.com/us/

# write header information to the log file
start_date=`date`
echo "START-------------------------------------------------" >> output.txt
echo "" >> output.txt

# retrieve the web page using curl. time the process with the time command.
time (curl --connect-timeout 100 $URL) >> output.txt

# write additional footer information to the log file
echo "" >> output.txt
end_date=`date`
echo "STARTTIME: $start_date" >> output.txt
echo "END TIME:  $end_date" >> output.txt
echo "" >> output.txt