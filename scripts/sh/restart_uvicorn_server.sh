#!/bin/bash

# Credit to Source: https://levelup.gitconnected.com/how-to-restart-fastapi-server-with-bash-script-f05a5bfcec5c
source /home/project/myenv/bin/activate
cd /home/project/server
PID=$(ps aux | grep 'uvicorn app.main:gender_decoder_api' | grep -v grep | awk {'print $2'} | xargs)
if [ "$PID" != "" ]
then
kill -9 $PID
sleep 2
echo "" > nohup.out
echo "Restarting FastAPI server"
else
echo "No such process. Starting new FastAPI server"
fi
nohup uvicorn myapp:app &