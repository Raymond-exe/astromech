#!/bin/bash

cd "$(dirname "$0")"

echo "[run.sh] Checking for updates from remote repo..."
git fetch --all
git reset --hard origin/master

echo "[run.sh] Cleaning ./out/ directory..."
rm -rf out/*
mkdir -p out

echo "[run.sh] Compiling main file..."
g++ src/main.cpp -o out/main

if [ $? -eq 0 ]; then
    echo "[run.sh] Succeeded compiling. Running program..."
    ./out/main
else
    echo "[run.sh] Failed to compile, check for errors!"
    echo "End of line."
    exit 1
fi
