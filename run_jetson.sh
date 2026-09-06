#!/bin/bash

# ROS2 environment
source /opt/ros/humble/setup.bash

# Project directory
PROJECT_DIR="/home/nvidia/yolo_demo"
SCRIPT_PATH="$PROJECT_DIR/src/detect.py"
MODEL_PATH="$PROJECT_DIR/weights/best.pt"

cd "$PROJECT_DIR" || exit 1

# Check detector program
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "Error: detect.py not found"
    exit 1
fi

# Check model
if [ ! -f "$MODEL_PATH" ]; then
    echo "Error: best.pt not found"
    exit 1
fi

# Check camera
if [ ! -e /dev/video0 ]; then
    echo "Error: /dev/video0 not found"
    exit 1
fi

echo "Starting YOLO11 + ROS2 detector..."

exec /usr/bin/python3 "$SCRIPT_PATH"