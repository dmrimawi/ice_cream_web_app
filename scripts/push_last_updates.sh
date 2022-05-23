echo "Pushing the new data to git repo"
echo "Changing direcotory to $1"
cd $1
echo "Creating the commit"
git commit -a -m "WebServer: Updating the data file"
echo "pushing commit to origin master"
git push origin master
echo "return to dir: $2"
cd $2
exit 0
