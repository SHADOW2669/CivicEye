@echo off
echo Updating system packages...
winget install -e --id Python.Python.3.12
winget install -e --id python3 python3-venv python3-tk

echo Creating virtual environment...
python -m venv myenv
call myenv\Scripts\activate

echo Installing required Python packages...
pip install --upgrade pip
pip install opencv-python opencv-python-headless ultralytics Pillow ttkbootstrap numpy matplotlib torch torchvision torchaudio requests

echo Installation complete. You can now run the helmet detection software using:
echo call myenv\Scripts\activate ^&^& python civiceye.py
pause
