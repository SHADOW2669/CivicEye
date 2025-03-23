@echo off
setlocal

echo Updating system packages...
winget install -e --id Python.Python.3.12 -h --accept-package-agreements --accept-source-agreements

echo Checking if Python is installed...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python not found! Adding Python to PATH...
    setx PATH "%PATH%;C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312"
)

echo Checking pip...
python -m ensurepip --default-pip
python -m pip install --upgrade pip

echo Creating virtual environment...
python -m venv myenv
call myenv\Scripts\activate

echo Installing required Python packages...
pip install --upgrade pip
pip install opencv-python opencv-python-headless ultralytics Pillow ttkbootstrap numpy matplotlib torch torchvision torchaudio requests

echo Installation complete. You can now run the software using:
echo call myenv\Scripts\activate && python civiceye.py
pause