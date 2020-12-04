#!/bin/sh

PYTHON=python3

auth_proxy=$(tempfile)


$PYTHON AuthServer.py --Ice.Config=authserver.conf>auth_proxy & 
PID=$!
sleep 5
echo "authproxy: $(cat auth_proxy)"

$PYTHON Server.py --Ice.Config=server.conf "$(cat auth_proxy)" 
sleep 5

rm auth_proxy
kill -9 $PID