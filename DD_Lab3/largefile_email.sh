#!/bin/sh

filename='bigfiles'
find  ~/Documents -type f -size +1M > $filename
count=`cat bigfiles | wc -l`

if [ $? -ne 0 ]
then
  date >> $filename
  mail -s "Large log files found on server" skarthik4231@gmail.com < $filename
fi