#!/bin/bash
set -e

echo "START"

./log_tools/collect.sh & python3 ./watcher.py &

# wait for every background process
wait