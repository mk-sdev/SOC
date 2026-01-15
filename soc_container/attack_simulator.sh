#!/bin/bash
TARGET="http://localhost:8080"

echo "[*] Generating normal traffic..."
for i in {1..20}; do
    curl -s $TARGET/ > /dev/null
done

echo "[*] Simulating brute force..."
for i in {1..20}; do
    curl -s $TARGET/login > /dev/null
done

echo "[*] Simulating SQL Injection..."
for i in {1..5}; do
    curl -s "$TARGET/index.php?id=1%27%20OR%20%271%27=%271" > /dev/null
done

echo "[*] Simulating LFI..."
for i in {1..5}; do
    curl -s "$TARGET/index.php?page=../../../../etc/passwd" > /dev/null
done

echo "[*] Simulating scan..."
for i in {1..100}; do
    curl -s $TARGET/test$i > /dev/null
done

echo "[✓] Attack simulation complete."
