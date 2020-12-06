#!/bin/sh

PYTHON=python3
SERVER_CONFIG=server.conf


sleep 5

$PYTHON Server.py --Ice.Config=$SERVER_CONFIG  "$1" 


