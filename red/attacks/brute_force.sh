#!/bin/bash

TARGET=${TARGET:-http://localhost:8080}

echo "[*] Simulating brute force..."

for i in {1..20}; do
    curl -s -H "X-Forwarded-For: 66.66.66.66" $TARGET/login > /dev/null
done

echo "[*] Finished simulating brute force"