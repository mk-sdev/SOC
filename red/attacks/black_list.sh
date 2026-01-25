#!/bin/bash

TARGET=${TARGET:-http://localhost:8080}

echo "[*] Simulating sending request from a black-listed IP..."

curl -s -H "X-Forwarded-For: 12.34.56.78" $TARGET/login > /dev/null

echo "[*] Finished"