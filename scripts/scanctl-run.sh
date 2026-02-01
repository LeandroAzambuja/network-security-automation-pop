#!/bin/bash

BASE="/home/pop-hdb/automacao_honeypot"
LOG="/var/log/scanctl.log"

cd $BASE || exit 1

./scanctl run -t 192.168.0.10 -s completo -d 30 >> $LOG 2>&1

