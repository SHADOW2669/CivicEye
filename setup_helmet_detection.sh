#!/bin/bash

# Create and activate virtual environment
python3 -m venv myenv
source myenv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install cvzone ultralytics

# Run the script
python3 helmet_detection_video.py
