echo "Pushing the new data to git repo" >> $2/logs_file.log 2>&1
echo "Changing direcotory to $1" >> $2/logs_file.log 2>&1
cd $1
echo "Creating the commit" >> $2/logs_file.log 2>&1
/usr/bin/git commit -a -m "WebServer: Updating the data file" >> $2/logs_file.log 2>&1
echo "pushing commit to origin master" >> $2/logs_file.log 2>&1
/usr/bin/git push origin master >> $2/logs_file.log 2>&1
echo "return to dir: $2" >> $2/logs_file.log 2>&1
cd $2
echo "starting the learning process" >> $2/logs_file.log 2>&1
curl --max-time 3 $3 >> $2/logs_file.log 2>&1
exit 0
