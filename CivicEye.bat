@echo off
echo Activating virtual environment...
call myenv\Scripts\activate

echo Running the helmet detection program...
python civiceye.py

pause
