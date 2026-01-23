#!/bin/bash

if [ -f /.dockerenv ]; then
    # if executed in a container
    TARGET="http://nginx:80"
else
    # when executed on the host
    TARGET="http://localhost:8080"
fi

# list of available endpoints
ENDPOINTS=("/" "/login" "/index.php" "/about" "/contact" "/products")

echo "[*] Starting normal traffic generator..."

while true; do
    # random endpoint
    ENDPOINT=${ENDPOINTS[$RANDOM % ${#ENDPOINTS[@]}]}

    # random IPv4
    OCT1=$((RANDOM % 256))
    OCT2=$((RANDOM % 256))
    OCT3=$((RANDOM % 256))
    OCT4=$((RANDOM % 256))
    SRC_IP="$OCT1.$OCT2.$OCT3.$OCT4"

    # random break period between 0.5 and 3 seconds
    SLEEP_TIME=$(awk -v min=0.5 -v max=3 'BEGIN{srand(); print min+rand()*(max-min)}')

    echo "[*] Sending request to $ENDPOINT from $SRC_IP, sleeping $SLEEP_TIME sec..."

    # sending a request with random IP
    curl -s -H "X-Forwarded-For: $SRC_IP" "$TARGET$ENDPOINT" > /dev/null

    sleep "$SLEEP_TIME"
done
