#!/bin/sh

PYTHON=python3
SERVER_CONFIG=server.conf

$PYTHON Server.py --Ice.Config=$SERVER_CONFIG  "$1">PRX | tail -1 PRX
