#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Updating system packages..."
sudo apt update
sudo apt install -y python3 python3-venv

echo "Creating virtual environment..."
python3 -m venv myenv
source myenv/bin/activate

echo "Installing required Python packages..."
pip install --upgrade pip
pip install opencv-python opencv-python-headless ultralytics Pillow ttkbootstrap numpy matplotlib torch torchvision torchaudio requests

echo "Installation complete. You can now run the helmet detection software using:"
echo "source myenv/bin/activate && python3 civiceye.py"