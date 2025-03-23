#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Detecting Linux distribution..."
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "Unsupported OS"
    exit 1
fi

echo "Updating system packages..."
if [[ "$OS" == "ubuntu" || "$OS" == "debian" ]]; then
    sudo apt update && sudo apt install -y python3 python3-venv python3-tk
elif [[ "$OS" == "arch" ]]; then
    sudo pacman -Sy --noconfirm python python-virtualenv tk
elif [[ "$OS" == "fedora" ]]; then
    sudo dnf install -y python3 python3-virtualenv python3-tkinter
else
    echo "Unsupported Linux distribution."
    exit 1
fi

echo "Creating virtual environment..."
python3 -m venv myenv
source myenv/bin/activate

echo "Installing required Python packages..."
pip install --upgrade pip
pip install opencv-python opencv-python-headless ultralytics Pillow ttkbootstrap numpy matplotlib torch torchvision torchaudio requests

echo "Installation complete. You can now run the helmet detection software using:"
echo "source myenv/bin/activate && python3 civiceye.py"
