#!/bin/bash

TARGET=${TARGET:-http://localhost:8080}

echo "[*] Simulating nmap scan..."
nmap -sS -p- $TARGET
echo "[*] Finished simulating nmap scan"