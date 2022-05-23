echo "Waiting to have a new model generated" >> $2/logs_file.log 2>&1
sleep 240
echo "Changing the directory to: $1" >> $2/logs_file.log 2>&1
cd $1
echo "Pulling new updates" >> $2/logs_file.log 2>&1
git pull --update >> $2/logs_file.log 2>&1
cd $2
exit 0
