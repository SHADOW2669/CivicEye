@echo off
setlocal enabledelayedexpansion

:: CivicEye Setup Script for Windows
:: Installs dependencies, sets up a virtual environment, and creates a shortcut in the script folder.
:: Automatically cleans up setup files upon successful completion.

:: --- Configuration ---
set VENV_NAME=myenv
set REQUIREMENTS_FILE=requirements.txt
set PYTHON_SCRIPT_REL_PATH=DATA\civiceye.py
set SHORTCUT_NAME=CivicEye.lnk
set APP_ICON_NAME=icon.ico
set MIN_PYTHON_MAJOR=3
set MIN_PYTHON_MINOR=8

:: --- Get Script Directory ---
set SCRIPT_DIR=%~dp0
:: Remove trailing backslash if present
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

:: --- Path Definitions ---
set VENV_DIR=%SCRIPT_DIR%\%VENV_NAME%
set REQUIREMENTS_PATH=%SCRIPT_DIR%\%REQUIREMENTS_FILE%
set PYTHON_SCRIPT_PATH=%SCRIPT_DIR%\%PYTHON_SCRIPT_REL_PATH%
set VENV_PYTHON=%VENV_DIR%\Scripts\python.exe
set VENV_PYTHONW=%VENV_DIR%\Scripts\pythonw.exe
set VENV_ACTIVATE=%VENV_DIR%\Scripts\activate.bat
set APP_ICON_PATH=%SCRIPT_DIR%\DATA\%APP_ICON_NAME%
set SHORTCUT_PATH=%SCRIPT_DIR%\%SHORTCUT_NAME%
set VBS_TEMP_FILE=%TEMP%\create_shortcut_%RANDOM%.vbs

:: --- Argument Parsing ---
if /I "%1"=="-h" goto :usage
if /I "%1"=="--help" goto :usage

goto :main_logic

:: --- Helper Function for Printing ---
:print_header
echo.
echo ^>^>^> %1
goto :eof

:print_info
echo [INFO] %1
goto :eof

:print_ok
echo [OK]   %1
goto :eof

:print_warn
echo [WARN] %1
goto :eof

:print_error
echo [ERROR] %1
goto :eof

:: --- Usage/Help Function ---
:usage
echo Usage: %~nx0
echo Sets up the environment and creates a shortcut for the CivicEye application in the current folder.
echo.
echo This script requires Python %MIN_PYTHON_MAJOR%.%MIN_PYTHON_MINOR%+ to be installed and available in the system PATH.
echo Ensure 'Add Python to PATH' was selected during Python installation.
echo.
pause
goto :eof


:: --- Core Functions ---

:check_system_deps
    call :print_info "Checking for system dependencies..."
    set PYTHON_CMD=
    set PYTHON_VER_OK=0

    :: Check for python command
    python --version > nul 2>&1
    if not errorlevel 1 (
        set PYTHON_CMD=python
    ) else (
        :: Check for py launcher
        py -%MIN_PYTHON_MAJOR% --version > nul 2>&1
        if not errorlevel 1 (
            set PYTHON_CMD=py -%MIN_PYTHON_MAJOR%
        )
    )

    if "%PYTHON_CMD%"=="" (
        call :print_error "Python %MIN_PYTHON_MAJOR%.%MIN_PYTHON_MINOR%+ not found in PATH."
        call :print_error "Please install Python from python.org and select 'Add Python to PATH'."
        exit /b 1
    )
    call :print_ok "Found Python command: '%PYTHON_CMD%'"

    :: Check Python Version
    call :print_info "Checking Python version (requires >= %MIN_PYTHON_MAJOR%.%MIN_PYTHON_MINOR%)..."
    for /f "tokens=2 delims= " %%v in ('%PYTHON_CMD% --version 2^>^&1') do set "PY_VER=%%v"
    :: Check if version string was captured
    if "!PY_VER!"=="" (
        call :print_warn "Could not determine Python version from '%PYTHON_CMD% --version'."
        call :print_warn "Assuming version is OK, but errors may occur later."
        set PYTHON_VER_OK=1
    ) else (
        for /f "tokens=1,2 delims=." %%a in ("!PY_VER!") do (
            set /a MAJOR=%%a
            set /a MINOR=%%b
        )
        if !MAJOR! LSS %MIN_PYTHON_MAJOR% (
            call :print_error "Python %MIN_PYTHON_MAJOR%.x or higher is required (found Major: !MAJOR!)."
            exit /b 1
        )
        if !MAJOR! EQU %MIN_PYTHON_MAJOR% if !MINOR! LSS %MIN_PYTHON_MINOR% (
            call :print_error "Python %MIN_PYTHON_MAJOR%.%MIN_PYTHON_MINOR% or newer is required (found: !PY_VER!)."
            exit /b 1
        )
        call :print_ok "Python version !PY_VER! is sufficient."
        set PYTHON_VER_OK=1
    )

    call :print_info "Checking for pip module..."
    %PYTHON_CMD% -m pip --version > nul 2>&1
    if errorlevel 1 (
        call :print_error "'pip' module not found for %PYTHON_CMD%."
        call :print_error "Please ensure pip is installed with Python."
        exit /b 1
    )
    call :print_ok "'pip' module found."

     call :print_info "Checking for venv module..."
     :: Use import check which is more reliable than -h across versions
    %PYTHON_CMD% -c "import venv" > nul 2>&1
     if errorlevel 1 (
        call :print_error "'venv' module not found for %PYTHON_CMD%."
        call :print_error "Please ensure venv is installed with Python."
        exit /b 1
     )
    call :print_ok "'venv' module found."

    call :print_ok "System dependencies check passed."
    exit /b 0
:eof

:setup_venv
    call :print_header "Setting up Python Virtual Environment (%VENV_NAME%)"
    if not exist "%VENV_DIR%" (
        call :print_info "Creating virtual environment..."
        %PYTHON_CMD% -m venv "%VENV_DIR%"
        if errorlevel 1 (
            call :print_error "Failed to create virtual environment."
            exit /b 1
        )
    ) else (
        call :print_info "Virtual environment already exists."
    )

    call :print_info "Activating virtual environment for package installation..."
    call "%VENV_ACTIVATE%"

    call :print_info "Upgrading pip..."
    python -m pip install --upgrade pip
    if errorlevel 1 (
        call :print_error "Failed to upgrade pip."
        call deactivate > nul 2>&1
        exit /b 1
    )

    if not exist "%REQUIREMENTS_PATH%" (
        call :print_error "'%REQUIREMENTS_FILE%' not found in '%SCRIPT_DIR%'."
        call deactivate > nul 2>&1
        exit /b 1
    )

    call :print_info "Installing Python packages from %REQUIREMENTS_FILE%..."
    call :print_warn "This may take a while depending on your internet connection..."
    pip install -r "%REQUIREMENTS_PATH%"
    if errorlevel 1 (
        call :print_error "Failed to install Python packages."
        call :print_warn "Check network connection/proxy settings and '%REQUIREMENTS_FILE%'."
        call deactivate > nul 2>&1
        exit /b 1
    )

    call :print_info "Deactivating environment after setup..."
    call deactivate > nul 2>&1
    call :print_ok "Virtual environment setup complete."
    exit /b 0
:eof

:create_local_shortcut
    call :print_header "Creating Shortcut in Script Folder (%SHORTCUT_NAME%)"

    :: Determine which python executable to use for launching GUI (prefer pythonw.exe)
    set VENV_LAUNCH_PYTHON=%VENV_PYTHON%
    if exist "%VENV_PYTHONW%" (
        call :print_info "Using pythonw.exe for shortcut (no console)."
        set VENV_LAUNCH_PYTHON=%VENV_PYTHONW%
     ) else (
        call :print_warn "pythonw.exe not found in venv. Shortcut might show console briefly."
     )

    :: Check if required files exist before creating shortcut
    if not exist "%VENV_LAUNCH_PYTHON%" (
        call :print_error "Python executable not found at '%VENV_LAUNCH_PYTHON%'. Cannot create shortcut."
        exit /b 1
    )
     if not exist "%PYTHON_SCRIPT_PATH%" (
        call :print_error "Main Python script '%PYTHON_SCRIPT_REL_PATH%' not found at '%PYTHON_SCRIPT_PATH%'. Cannot create shortcut."
        exit /b 1
    )

    :: Prepare paths WITHOUT outer quotes for easier VBS formatting
    set TARGET_EXE_RAW=%VENV_LAUNCH_PYTHON%
    set TARGET_ARGS_RAW=%PYTHON_SCRIPT_PATH%
    set WORKING_DIR_RAW=%SCRIPT_DIR%
    set ICON_LOCATION_RAW=%APP_ICON_PATH%
    set SHORTCUT_FULL_PATH_RAW=%SHORTCUT_PATH%

    :: Check if icon file exists
    if not exist "%ICON_LOCATION_RAW%" (
        call :print_warn "Icon file '%APP_ICON_NAME%' not found at %ICON_LOCATION_RAW%. Shortcut will use default icon."
        set ICON_LOCATION_RAW=
    )

    :: Create temporary VBScript file
    >"%VBS_TEMP_FILE%" echo Set oWS = WScript.CreateObject("WScript.Shell")
    >>"%VBS_TEMP_FILE%" echo sLinkFile = "%SHORTCUT_FULL_PATH_RAW%"
    >>"%VBS_TEMP_FILE%" echo Set oLink = oWS.CreateShortcut(sLinkFile)
    >>"%VBS_TEMP_FILE%" echo oLink.TargetPath = "%TARGET_EXE_RAW%"
    >>"%VBS_TEMP_FILE%" echo oLink.Arguments = """%TARGET_ARGS_RAW%"""
    >>"%VBS_TEMP_FILE%" echo oLink.WorkingDirectory = "%WORKING_DIR_RAW%"
    if defined ICON_LOCATION_RAW if not "%ICON_LOCATION_RAW%"=="" (
        >>"%VBS_TEMP_FILE%" echo oLink.IconLocation = "%ICON_LOCATION_RAW%, 0"
    )
    >>"%VBS_TEMP_FILE%" echo oLink.WindowStyle = 1 ' 1 = Normal window
    >>"%VBS_TEMP_FILE%" echo oLink.Description = "Launch CivicEye Application"
    >>"%VBS_TEMP_FILE%" echo oLink.Save

    call :print_info "Running VBScript to create shortcut..."
    cscript //Nologo "%VBS_TEMP_FILE%"
    if errorlevel 1 (
        call :print_error "Failed to create shortcut using VBScript."
        call :print_info "VBScript content was:"
        type "%VBS_TEMP_FILE%"
        del "%VBS_TEMP_FILE%" > nul 2>&1
        exit /b 1
    )

    del "%VBS_TEMP_FILE%" > nul 2>&1
    call :print_ok "Shortcut created at %SHORTCUT_PATH%"
    exit /b 0
:eof


:cleanup_setup_files
    call :print_header "Cleaning Up Setup Files"
    :: *** REMOVED USER PROMPT - Cleanup is now automatic ***
    if exist "%REQUIREMENTS_PATH%" (
        call :print_info "Deleting %REQUIREMENTS_FILE%..."
        del /F /Q "%REQUIREMENTS_PATH%" > nul
        if errorlevel 1 (
           call :print_warn "Could not delete %REQUIREMENTS_FILE%."
        )
    )
    call :print_info "Deleting setup script: %~nx0"
    :: Use timeout for delay before self-deletion
    timeout /t 2 /nobreak > nul
    del /F /Q "%~f0" > nul
    if errorlevel 1 (
       call :print_warn "Could not delete setup script %~nx0."
    )
    exit /b 0
:eof


:: --- Main Execution Logic ---
:main_logic

call :print_header "Starting CivicEye Setup"
call :print_info "Script directory: %SCRIPT_DIR%"
call :print_warn "Ensure this script is run in a directory with standard ASCII characters."

:: Check system dependencies first
call :check_system_deps
if errorlevel 1 (
    call :print_error "Prerequisites missing. Please check messages above."
    pause
    exit /b 1
)

:: Setup the virtual environment and install Python packages
call :setup_venv
if errorlevel 1 (
    call :print_error "Virtual environment setup failed."
    pause
    exit /b 1
)

:: Create the shortcut in the script folder
call :create_local_shortcut
if errorlevel 1 (
    call :print_error "Failed to create shortcut."
    pause
    exit /b 1
)

:: --- Final Completion Message ---
echo.
echo ==================================================
echo  Setup Complete!
echo ==================================================
echo  You can now run the application by double-clicking
echo  the '%SHORTCUT_NAME%' icon in this directory.
echo ==================================================
echo.

:: Clean up setup files (this script and requirements.txt) - Now runs automatically
call :cleanup_setup_files

endlocal
echo Setup finished. Press any key to exit.
pause > nul
exit /b 0