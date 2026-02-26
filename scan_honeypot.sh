#!/bin/bash
DATA=$(date +"%Y-%m-%d")
HORA=$(date +"%H%M%S")
ALVO="192.168.0.10"
DIR="resultados/${DATA}"

if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
fi

ARQUIVO="${DIR}/scan_${ALVO//./_}_${HORA}.txt"

echo "SCAN HONEYPOT RNP"
echo "Alvo: $ALVO"
echo "Data: $DATA $HORA"
echo "Diretório: $DIR"
echo "Arquivo: $ARQUIVO"
echo "=============================="

docker run -it --rm --network host rustscan/rustscan:latest -a "$ALVO" -- -sV -sC -T4 2>&1 | tee "$ARQUIVO"

echo ""
echo "SCAN CONCLUIDO"
PORTA_COUNT=$(grep -c "open.*tcp" "$ARQUIVO" 2>/dev/null || echo "0")
echo "Portas abertas: $PORTA_COUNT"
