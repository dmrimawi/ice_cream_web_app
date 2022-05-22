echo "Pushing the new data to git repo"
echo "Changing direcotory to $1"
cd $1
machine_info=$(uname -a)
git commit -a -m "WebServer: Updating the data file" -m "${machine_info}"
git push origin master
exit 0
