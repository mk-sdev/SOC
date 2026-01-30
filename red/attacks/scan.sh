#!/bin/bash

if [ -f /.dockerenv ]; then
    TARGET="nginx"
else 
    TARGET="localhost"
fi

echo "[*] Simulating nmap scan..."
# enforcing http
nmap -p 80 --script=http-title --source-port 53 -sT $TARGET

echo "[*] Finished simulating nmap scan"