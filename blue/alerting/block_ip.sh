#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <IP>"
    exit 1
fi

IP=$1
echo "[*] Blocking IP $IP..."
iptables -A INPUT -s $IP -j DROP
echo "[✓] IP $IP blocked."
