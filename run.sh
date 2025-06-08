#!/bin/bash

cd "$(dirname "$0")"

echo "[run.sh] Checking for updates from remote repo..."
git fetch --all
git reset --hard origin/master

echo "[run.sh] Starting audio stream"
(
    while true; do
        ffmpeg -f alsa -i hw:2,0 -ac 1 -f mp3 -content_type audio/mpeg -listen 1 http://localhost:8000
        echo "Client disconnected, restarting stream in 1s..."
        sleep 1
    done
) &

echo "[run.sh] Starting flask server..."
sudo python3 src/main.py
