#!/bin/bash

# Update package list
sudo apt update

# Install required system packages
sudo apt install -y python3.12-venv

# Create and activate virtual environment
python3 -m venv myenv
source myenv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install cvzone ultralytics opencv-python

# Run the detection script
python3 civiceye.py
