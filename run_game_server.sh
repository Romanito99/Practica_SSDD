#!/bin/sh

PYTHON=python3

AUTH_CONFIG=authserver.conf
SERVER_CONFIG=server.conf


PRX=$(tempfile)
PRX1=$(tempfile)

$PYTHON AuthServer.py --Ice.Config=$AUTH_CONFIG>PRX &

PID=$!

sleep 3

$PYTHON Server.py --Ice.Config=$SERVER_CONFIG  "$(cat PRX)">PRX1 | tail -1 PRX1


kill -KILL $PID
rm $PRX



