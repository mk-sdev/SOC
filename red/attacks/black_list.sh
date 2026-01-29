#!/bin/bash

echo "[*] Simulating sending request from a black-listed IP..."

IP=$1

if [[ -z "$IP" ]]; then
    IP="1.2.3.4"
fi

curl -s -H "X-Forwarded-For: $IP" $TARGET/login > /dev/null

echo "[*] Finished"