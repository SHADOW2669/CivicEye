@echo off
setlocal enabledelayedexpansion

:: CivicEye Uninstaller Script for Windows
:: Removes the virtual environment, launcher shortcut, DATA folder, Readme.md,
:: session file, Detects folder (optional), and itself.

:: --- Configuration ---
set VENV_NAME=myenv
set LAUNCHER_SCRIPT=run_civiceye.bat
set SHORTCUT_NAME=CivicEye.lnk
set DETECTS_FOLDER=Detects
set SESSION_FILE=civiceye_session.json
set DATA_FOLDER=DATA
set README_FILE=Readme.md

:: --- Get Script Directory ---
set SCRIPT_DIR=%~dp0
:: Remove trailing backslash if present
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

:: --- Path Definitions ---
set VENV_DIR=%SCRIPT_DIR%\%VENV_NAME%
set LAUNCHER_SCRIPT_PATH=%SCRIPT_DIR%\%LAUNCHER_SCRIPT%
set SHORTCUT_PATH=%SCRIPT_DIR%\%SHORTCUT_NAME%
set DESKTOP_SHORTCUT_PATH=%USERPROFILE%\Desktop\%SHORTCUT_NAME%
set DETECTS_PATH=%SCRIPT_DIR%\%DETECTS_FOLDER%
set SESSION_PATH=%SCRIPT_DIR%\%SESSION_FILE%
set DATA_PATH=%SCRIPT_DIR%\%DATA_FOLDER%
set README_PATH=%SCRIPT_DIR%\%README_FILE%

:: --- Jump to main logic ---
goto :main_logic

:: --- Helper Function for Printing ---
:print_header
echo.
echo === %~1 ===
goto :eof

:print_info
echo [INFO] %~1
goto :eof

:print_warn
echo [WARN] %~1
goto :eof

:print_error
echo [ERROR] %~1
goto :eof

:: --- Main Logic ---
:main_logic

call :print_header "CivicEye Uninstaller (Full Cleanup)"
echo.
call :print_warn "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
call :print_warn "!!                    EXTREME CAUTION!                      !!"
call :print_warn "!! This script will PERMANENTLY DELETE the following:       !!"
echo   - Virtual environment folder: %VENV_DIR%
echo   - DATA folder (including .py script, icon): %DATA_PATH%
echo   - Launcher script (if exists): %LAUNCHER_SCRIPT_PATH%
echo   - Shortcut in this folder:  %SHORTCUT_PATH%
echo   - Shortcut on Desktop (if exists): %DESKTOP_SHORTCUT_PATH%
echo   - Saved session file (if exists): %SESSION_PATH%
echo   - Readme file:                %README_PATH%
call :print_warn "!! It can also remove the '%DETECTS_FOLDER%' folder.            !!"
call :print_warn "!! THIS ACTION CANNOT BE UNDONE.                            !!"
call :print_warn "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
echo.

:confirm_uninstall
set CONFIRM=
set /p CONFIRM="Are you absolutely sure you want to permanently delete these files? (Y/N): "
if /I not "%CONFIRM%"=="Y" (
    if /I not "%CONFIRM%"=="N" (
        call :print_warn "Please answer Y or N."
        goto :confirm_uninstall
    )
    call :print_info "Uninstallation cancelled."
    goto :end
)

:: --- Deletion Process ---

call :print_header "Starting Removal Process"

:: Delete Virtual Environment
if exist "%VENV_DIR%\" (
    call :print_info "Removing virtual environment folder: %VENV_NAME%..."
    rmdir /S /Q "%VENV_DIR%"
    if errorlevel 1 (
        call :print_error "Failed to remove %VENV_DIR%. It might be in use or permissions issue."
    ) else (
        call :print_ok "%VENV_NAME% removed."
    )
) else (
    call :print_warn "Virtual environment folder '%VENV_NAME%' not found."
)

:: Delete DATA Folder
if exist "%DATA_PATH%\" (
    call :print_info "Removing DATA folder..."
    rmdir /S /Q "%DATA_PATH%"
    if errorlevel 1 (
        call :print_error "Failed to remove %DATA_PATH%. Check permissions or if files are open."
    ) else (
        call :print_ok "%DATA_FOLDER% removed."
    )
) else (
    call :print_warn "'%DATA_FOLDER%' folder not found."
)

:: Delete Launcher Script (run_civiceye.bat)
if exist "%LAUNCHER_SCRIPT_PATH%" (
    call :print_info "Removing launcher script: %LAUNCHER_SCRIPT%..."
    del /F /Q "%LAUNCHER_SCRIPT_PATH%" > nul
    call :print_ok "%LAUNCHER_SCRIPT% removed."
) else (
    call :print_warn "Launcher script '%LAUNCHER_SCRIPT%' not found."
)

:: Delete Local Shortcut (.lnk)
if exist "%SHORTCUT_PATH%" (
    call :print_info "Removing shortcut: %SHORTCUT_NAME%..."
    del /F /Q "%SHORTCUT_PATH%" > nul
    call :print_ok "%SHORTCUT_NAME% removed from script folder."
) else (
    call :print_warn "Shortcut '%SHORTCUT_NAME%' not found in script folder."
)

:: Delete Desktop Shortcut (.lnk)
if exist "%DESKTOP_SHORTCUT_PATH%" (
    call :print_info "Removing Desktop shortcut..."
    del /F /Q "%DESKTOP_SHORTCUT_PATH%" > nul
    call :print_ok "Desktop shortcut removed."
) else (
    call :print_warn "Desktop shortcut '%SHORTCUT_NAME%' not found."
)

:: Delete Session File
if exist "%SESSION_PATH%" (
    call :print_info "Removing session file..."
    del /F /Q "%SESSION_PATH%" > nul
    call :print_ok "Session file removed."
) else (
    call :print_warn "Session file '%SESSION_FILE%' not found."
)

:: Delete Readme File
if exist "%README_PATH%" (
    call :print_info "Removing Readme file..."
    del /F /Q "%README_PATH%" > nul
    call :print_ok "%README_FILE% removed."
) else (
    call :print_warn "'%README_FILE%' not found."
)


:: Ask about Detects folder
if exist "%DETECTS_PATH%\" (
    echo.
    call :print_warn "The '%DETECTS_FOLDER%' folder contains saved detection images."
    :confirm_detects
    set DEL_DETECTS=
    set /p DEL_DETECTS="Do you want to delete the '%DETECTS_FOLDER%' folder as well? (Y/N): "
    if /I "%DEL_DETECTS%"=="Y" (
        call :print_info "Removing %DETECTS_FOLDER% folder..."
        rmdir /S /Q "%DETECTS_PATH%"
        if errorlevel 1 (
             call :print_error "Failed to remove %DETECTS_PATH%. Check permissions or if files are open."
             pause
        ) else (
            call :print_ok "%DETECTS_FOLDER% removed."
        )
    ) else if /I not "%DEL_DETECTS%"=="N" (
        call :print_warn "Please answer Y or N."
        goto :confirm_detects
    ) else (
        call :print_info "Skipping deletion of %DETECTS_FOLDER% folder."
    )
) else (
    call :print_info "'%DETECTS_FOLDER%' folder not found."
)

echo.
call :print_ok "Main uninstallation steps finished."
echo.

:: Self-deletion
call :print_info "Attempting to remove the uninstaller script itself..."
:: Use timeout for delay before self-deletion attempt
timeout /t 3 /nobreak > nul
start "" /B cmd /c del /F /Q "%~f0" ^& exit /b

:end
endlocal
:: The final pause might not be reached if self-deletion works immediately
echo Press any key to exit the uninstaller window (if it hasn't closed).
pause > nul
exit /b 0