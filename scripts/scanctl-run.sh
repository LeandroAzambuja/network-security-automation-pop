#!/bin/bash

if [ -z "$DEFECTDOJO_API_TOKEN" ]; then
  echo "DEFECTDOJO_API_TOKEN não definido."
  exit 1
fi

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$BASE_DIR" || exit 1

./scanctl run -t 192.168.0.10 -s completo -d 1 >> logs/cron_exec.log 2>&1
