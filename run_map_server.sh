#!/bin/sh

PYTHON=python3

script=$(tempfile)

$PYTHON AuthServer.py --Ice.Config=authserver.conf>script  & 

PID=$!
echo $(cat script)
sleep 5


$PYTHON Server.py --Ice.Config=server.conf  "$(cat script)"


rm script
kill -9 $PID