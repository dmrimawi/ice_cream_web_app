echo "Changing the directory to: $1" >> $2/logs_file.log 2>&1
cd $1
echo "Pulling new updates after 240 seconds" >> $2/logs_file.log 2>&1
sleep 240
/usr/bin/git pull --update >> $2/logs_file.log 2>&1
cd $2
exit 0
