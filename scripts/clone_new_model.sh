echo "Waiting to have a new model generated"
sleep 240
echo "Changing the directory to: $1"
cd $1
echo "Pulling new updates"
git pull --update
exit 0
