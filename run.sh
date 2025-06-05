#!/bin/bash

cd "$(dirname "$0")"

echo "[run.sh] Checking for updates from remote repo..."
git fetch --all
git reset --hard origin/master

echo "[run.sh] Cleaning build directory..."
rm -rf build/*
mkdir -p build

if [ -p /tmp/servo_ctrl ]; then
    echo "[run.sh] Creating FIFO pipe /tmp/servo_ctrl for servo control..."
    mkfifo /tmp/servo_ctrl
else
    echo "[run.sh] /tmp/servo_ctrl already exists."
fi

# echo "[run.sh] Compiling main file..."
# g++ src/main.cpp -o build/main

# if [ $? -eq 0 ]; then
#     echo "[run.sh] Succeeded compiling. Running program..."
#     ./build/main
# else
#     echo "[run.sh] Failed to compile, check for errors!"
#     echo "End of line."
#     exit 1
# fi

echo "[run.sh] Starting flask server..."
sudo python3 src/web-app.py
