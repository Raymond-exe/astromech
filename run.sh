#!/bin/bash

cd "$(dirname "$0")"

echo "[run.sh] Checking for updates from remote repo..."
git fetch --all
git reset --hard origin/master

if [ -p /tmp/servo_ctrl ]; then
    echo "[run.sh] Creating FIFO pipe /tmp/servo_ctrl for servo control..."
    mkfifo /tmp/servo_ctrl
else
    echo "[run.sh] /tmp/servo_ctrl already exists."
fi

echo "[run.sh] Cleaning build directory..."
rm -rf build/*
mkdir -p build

echo "[run.sh] Compiling servo control file..."
cmake --workflow --preset build

if [ -x build/astromech-cpp ]; then
    echo "[run.sh] Succeeded compiling. Running program..."
    ./build/astromech-cpp
else
    echo "[run.sh] Failed to compile servo control C++ file, aborting!"
    exit 1
fi

echo "[run.sh] Starting flask server..."
sudo python3 src/web-app.py
