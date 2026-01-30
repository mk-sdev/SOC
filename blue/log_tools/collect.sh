#!/bin/bash

LOG_SOURCE="/logs/access.log"
OUTPUT="/logs/collected.log"

touch $OUTPUT

echo "[*] Starting log collection from $LOG_SOURCE..."
tail -Fn0 $LOG_SOURCE | while read line; do
    echo "$line" >> $OUTPUT
done
