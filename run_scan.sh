#!/bin/bash

export DEFECTDOJO_API_TOKEN=0dff240192d73235779d2ca72c39496faf75809e

cd /home/pop-hdb/automacao_honeypot

./scanctl run -t 192.168.0.10 -s completo -d 1 >> logs/cron_exec.log 2>&1
