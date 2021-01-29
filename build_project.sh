#!/bin/sh
mkdir -p /tmp/db/SSDD-CONEJOBRAOJOS
cp icegauntlet.ice /tmp/db/SSDD-CONEJOBRAOJOS
cp AuthServer.py /tmp/db/SSDD-CONEJOBRAOJOS
cp Server.py /tmp/db/SSDD-CONEJOBRAOJOS
mkdir -p /tmp/db/registry
mkdir -p /tmp/db/node1
mkdir -p /tmp/db/node2
icepatch2calc /tmp/db/SSDD-CONEJOBRAOJOS
icegridnode --Ice.Config=node1.config & icegridnode --Ice.Config=node2.config


