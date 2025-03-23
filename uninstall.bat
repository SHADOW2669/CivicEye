@echo off
setlocal

echo Deactivating virtual environment...
call myenv\Scripts\deactivate 2>nul

echo Removing virtual environment...
rmdir /s /q myenv

echo Uninstalling Python...
winget uninstall -e --id Python.Python.3.12 -h

echo Cleaning up Python installation folder...
rmdir /s /q C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312 2>nul

echo Removing Python from PATH...
setx PATH "%PATH%" 

echo Uninstallation complete.
pause
