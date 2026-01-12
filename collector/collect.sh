#!/bin/bash

# Ścieżki w kontenerze soc
LOG_SOURCE="./logs/access.log"
OUTPUT="./logs/collected.log"

# Tworzymy plik jeśli nie istnieje
touch $OUTPUT

echo "[*] Starting log collection from $LOG_SOURCE..."
tail -Fn0 $LOG_SOURCE | while read line; do
    echo "$line" >> $OUTPUT
done
