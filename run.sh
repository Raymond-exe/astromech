#!/bin/bash

cd "$(dirname "$0")"

echo "[run.sh] Checking for updates from remote repo..."
git fetch --all
git reset --hard origin/master

echo "[run.sh] Starting flask server..."
sudo python3 src/main.py
