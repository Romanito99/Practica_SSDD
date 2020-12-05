#!/bin/sh

PYTHON=python3


#tmpfile=script

script= $PYTHON AuthServer.py --Ice.Config=authserver.conf  & 
echo $script
PID=$!
sleep 5


$PYTHON Server.py --Ice.Config=server.conf  "$script"
sleep 5


kill -9 $PID