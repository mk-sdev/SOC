#!/bin/sh

echo "START"

./collector/collect.sh &
COLLECT_PID=$!

exec python watcher.py
