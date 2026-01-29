#!/bin/bash

set -eu

source /app/attacks/_generate_ip.sh

echo "[*] Simulating brute force..."

IP=$(generate_ip "${1:-}") # if $1 doesn't exist, use empty string

for i in {1..20}; do
    curl -s -H "X-Forwarded-For: $IP" $TARGET/login > /dev/null
done

echo "[*] Finished simulating brute force"