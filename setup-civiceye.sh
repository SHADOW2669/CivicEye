#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# --- Configuration ---
VENV_NAME="myenv"
REQUIREMENTS_FILE="requirements.txt"
PYTHON_SCRIPT_REL_PATH="DATA/civiceye.py" # Relative path from project root
PYTHON_SCRIPT_NAME="civiceye.py"
DESKTOP_LAUNCHER_FILE="civiceye.desktop" # Name for the .desktop launcher
# *** UPDATED APP NAME ***
APP_NAME="CivicEye"
APP_COMMENT="Run the CivicEye Helmet Detection Application"
APP_ICON_NAME="icon.png" # Use icon.png (ensure it exists in DATA dir)
LOG_FILE="setup_civiceye.log"
MIN_PYTHON_MAJOR=3
MIN_PYTHON_MINOR=8 # Require Python 3.8+

# --- Script Flags ---
ENABLE_LOGGING=false

# --- Detect script directory safely ---
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# --- Path Definitions ---
VENV_DIR="$SCRIPT_DIR/$VENV_NAME"
REQUIREMENTS_PATH="$SCRIPT_DIR/$REQUIREMENTS_FILE"
PYTHON_SCRIPT_PATH="$SCRIPT_DIR/$PYTHON_SCRIPT_REL_PATH"
VENV_PYTHON="$VENV_DIR/bin/python" # Use 'python' inside venv
VENV_ACTIVATE="$VENV_DIR/bin/activate"
DESKTOP_LAUNCHER_PATH_LOCAL="$SCRIPT_DIR/$DESKTOP_LAUNCHER_FILE" # Local copy
APP_ICON_PATH="$SCRIPT_DIR/DATA/$APP_ICON_NAME" # Full path to icon inside DATA
# Standard user application directory
USER_APP_DIR="$HOME/.local/share/applications"
DESKTOP_LAUNCHER_PATH_SYSTEM="$USER_APP_DIR/$DESKTOP_LAUNCHER_FILE"

# --- ANSI Color Codes ---
COLOR_RESET='\033[0m'
COLOR_BOLD='\033[1m'
COLOR_BLUE='\033[0;34m'
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[0;33m'
COLOR_RED='\033[0;31m'
COLOR_CYAN='\033[0;36m'

# --- Helper Functions for Printing ---
print_header() { echo -e "\n${COLOR_BOLD}${COLOR_BLUE}>>> $1${COLOR_RESET}"; }
print_info() { echo -e "${COLOR_CYAN}[INFO]${COLOR_RESET} $1"; }
print_ok() { echo -e "${COLOR_GREEN}[OK]${COLOR_RESET}   $1"; }
print_warn() { echo -e "${COLOR_YELLOW}[WARN]${COLOR_RESET} $1"; }
print_error() { echo -e "${COLOR_RED}[ERROR]${COLOR_RESET} $1" >&2; }

# --- Usage/Help Function ---
usage() {
  echo "Usage: $0 [OPTIONS]"
  echo "Sets up the environment and creates a system launcher for the CivicEye application."
  echo ""
  echo "Options:"
  echo "  --log        Log all setup output to $LOG_FILE."
  echo "  -h, --help   Display this help message and exit."
  echo ""
  exit 0
}

# --- Argument Parsing ---
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    --log)
      ENABLE_LOGGING=true
      shift # past argument
      ;;
    -h|--help)
      usage
      ;;
    *) # unknown option
      print_error "Unknown option: $1"
      usage
      ;;
  esac
done

# --- Enable Logging if Requested ---
if [[ "$ENABLE_LOGGING" = true ]]; then
    # Check if tee is available
    if ! command -v tee &> /dev/null; then
        print_warn "'tee' command not found. Logging to file disabled."
        ENABLE_LOGGING=false
    else
        print_info "Logging enabled. Output will also be saved to '$LOG_FILE'"
        # Redirect stdout and stderr to tee, which writes to file and stdout/stderr
        exec > >(tee -a "$LOG_FILE") 2>&1
    fi
fi

# --- Core Functions ---

install_packages() {
    local package_manager="$1"
    shift
    local packages=("$@")
    print_info "Installing system packages using ${COLOR_BOLD}$package_manager${COLOR_RESET}: ${packages[*]}"
    print_warn "This may require sudo privileges."
    sleep 1 # Give user time to see message
    case "$package_manager" in
        apt)    sudo apt update && sudo apt install -y "${packages[@]}" ;;
        pacman) sudo pacman -Sy --noconfirm "${packages[@]}" ;;
        dnf)    sudo dnf install -y "${packages[@]}" ;;
        *)      print_error "Unsupported package manager '$package_manager'"; exit 1 ;;
    esac
}

check_system_deps() {
    print_info "Checking for system dependencies..."
    local missing_dep=0
    local python_cmd="python3" # Default command

    # Check for python3 first
    if ! command -v python3 &> /dev/null; then
        if command -v python &> /dev/null; then
            python_cmd="python"
            print_info "Using 'python' command."
        else
            print_warn "'python3' or 'python' command not found."
            missing_dep=1
        fi
    fi

    # Check Python version if command found
    if [[ $missing_dep -eq 0 ]]; then
        if ! $python_cmd -c "import sys; assert sys.version_info >= ($MIN_PYTHON_MAJOR, $MIN_PYTHON_MINOR)" &> /dev/null; then
            print_warn "Python $MIN_PYTHON_MAJOR.$MIN_PYTHON_MINOR+ is required (found `$($python_cmd --version 2>&1)`)."
            missing_dep=1
        else
             print_ok "Python version >= $MIN_PYTHON_MAJOR.$MIN_PYTHON_MINOR found (`$($python_cmd --version 2>&1)`)."
        fi
    fi

    # Check Tkinter
    if [[ $missing_dep -eq 0 ]]; then
         if ! $python_cmd -c 'import tkinter' &> /dev/null; then
            print_warn "'tkinter' module not available for $python_cmd."
            missing_dep=1
        fi
    fi
    # Check for pip
    if [[ $missing_dep -eq 0 ]]; then
        if ! $python_cmd -m pip --version &> /dev/null; then
             print_warn "'pip' for $python_cmd not found."
             missing_dep=1
        fi
    fi
    # Check for venv
     if [[ $missing_dep -eq 0 ]]; then
         if ! $python_cmd -m venv -h &> /dev/null; then
             print_warn "'venv' module for $python_cmd not found."
             missing_dep=1
        fi
    fi

    if [[ $missing_dep -eq 1 ]]; then
        return 1 # False (indicates dependencies are missing)
    else
        print_ok "Required system dependencies seem available."
        return 0 # True
    fi
}

install_system_deps() {
    print_info "Detecting Linux distribution..."
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        OS="$ID"
        print_info "Detected OS: ${COLOR_BOLD}$OS${COLOR_RESET}"
    else
        print_error "Cannot detect OS. Please install dependencies manually."
        exit 1
    fi

    local packages
    local python_cmd="python3" # Needed for venv creation later
    case "$OS" in
        ubuntu|debian)
            packages=(python3 python3-venv python3-tk python3-pip)
            install_packages apt "${packages[@]}"
            ;;
        arch)
            packages=(python python-virtualenv tk) # pip is usually included
            install_packages pacman "${packages[@]}"
            python_cmd="python" # Use 'python' on Arch
            ;;
        fedora)
            packages=(python3 python3-virtualenv python3-tkinter python3-pip)
            install_packages dnf "${packages[@]}"
            ;;
        *)
            print_error "Unsupported OS '$OS'. Install Python$MIN_PYTHON_MAJOR.$MIN_PYTHON_MINOR+, pip, venv/virtualenv, and Tkinter manually."
            exit 1
            ;;
    esac
    # Return the python command used by the OS
    echo "$python_cmd"
}

setup_venv() {
    # Creates venv and installs python packages
    local python_cmd="$1" # Python command to use (python or python3)
    print_header "Setting up Python Virtual Environment ($VENV_NAME)"
    if [[ ! -d "$VENV_DIR" ]]; then
        print_info "Creating virtual environment using $python_cmd..."
        "$python_cmd" -m venv "$VENV_DIR" || { print_error "Failed to create venv"; exit 1; }
    else
        print_info "Virtual environment already exists."
    fi

    print_info "Activating virtual environment for package installation..."
    source "$VENV_ACTIVATE"
    print_info "Using Python: $($VENV_PYTHON --version)"

    print_info "Upgrading pip..."
    # Use the venv's python to run pip module
    "$VENV_PYTHON" -m pip install --upgrade pip || { print_error "Failed to upgrade pip"; deactivate || true; exit 1; }

    if [[ ! -f "$REQUIREMENTS_PATH" ]]; then
        print_error "'$REQUIREMENTS_FILE' not found in '$SCRIPT_DIR'."
        deactivate || true
        exit 1
    fi

    print_info "Installing Python packages from $REQUIREMENTS_FILE..."
    print_warn "This may take a while depending on your internet connection..."
    "$VENV_PYTHON" -m pip install -r "$REQUIREMENTS_PATH" || {
        print_error "Failed to install Python packages."
        print_warn "Check network connection/proxy settings and '$REQUIREMENTS_FILE'."
        deactivate || true
        exit 1
    }

    deactivate || true
    print_ok "Virtual environment setup complete."
}

create_desktop_launcher() {
    # Creates or updates the .desktop file to run the application
    print_header "Creating Desktop Launcher ($DESKTOP_LAUNCHER_FILE)"

    # Check if icon exists, otherwise use a default
    local icon_line="Icon=application-x-executable" # Generic executable icon
    if [ -f "$APP_ICON_PATH" ]; then
        icon_line="Icon=$APP_ICON_PATH" # Use the full path to the icon
    else
        print_warn "Icon file '$APP_ICON_NAME' not found in '$SCRIPT_DIR/DATA'. Using default icon."
    fi

    # Check if required scripts/files exist before creating launcher
    if [[ ! -f "$VENV_ACTIVATE" ]]; then
        print_error "Virtual environment activation script not found at '$VENV_ACTIVATE'. Cannot create launcher."
        exit 1
    fi
     if [[ ! -x "$VENV_PYTHON" ]]; then
        print_error "Virtual environment Python binary not found or not executable at '$VENV_PYTHON'. Cannot create launcher."
        exit 1
    fi
    if [[ ! -f "$PYTHON_SCRIPT_PATH" ]]; then
        print_error "Main Python script '$PYTHON_SCRIPT_REL_PATH' not found at '$PYTHON_SCRIPT_PATH'. Cannot create launcher."
        exit 1
    fi

    # Construct the Exec command carefully, quoting paths
    # This command activates the venv, sources .env if it exists, then runs python
    local exec_command="bash -c 'cd \"$SCRIPT_DIR\" && source \"$VENV_ACTIVATE\" && [[ -f .env ]] && set -a && source .env && set +a ; \"$VENV_PYTHON\" \"$PYTHON_SCRIPT_PATH\"'"

    # Create the content for the .desktop file
    desktop_content=$(cat << EOF
[Desktop Entry]
Version=1.0
Name=$APP_NAME
Comment=$APP_COMMENT
Exec=$exec_command
Path=$SCRIPT_DIR
$icon_line
Terminal=false
Type=Application
Categories=Application;Utility;
StartupNotify=true
EOF
)

    # Write to local file first (optional backup)
    echo "$desktop_content" > "$DESKTOP_LAUNCHER_PATH_LOCAL"
    chmod +x "$DESKTOP_LAUNCHER_PATH_LOCAL"
    print_ok "Local launcher created/updated at $DESKTOP_LAUNCHER_PATH_LOCAL"

    # Ensure the target directory exists
    mkdir -p "$USER_APP_DIR" || { print_error "Could not create user application directory: $USER_APP_DIR"; exit 1; }

    # Write to system-recognized location
    echo "$desktop_content" > "$DESKTOP_LAUNCHER_PATH_SYSTEM"
    chmod +x "$DESKTOP_LAUNCHER_PATH_SYSTEM" # Ensure it's executable there too
    print_ok "System launcher created/updated at $DESKTOP_LAUNCHER_PATH_SYSTEM"

    # *** ADDED: Copy launcher to Desktop ***
    DESKTOP_DIR="$HOME/Desktop"
    if [[ -d "$DESKTOP_DIR" && -w "$DESKTOP_DIR" ]]; then
        cp "$DESKTOP_LAUNCHER_PATH_LOCAL" "$DESKTOP_DIR/$DESKTOP_LAUNCHER_FILE"
        chmod +x "$DESKTOP_DIR/$DESKTOP_LAUNCHER_FILE"
        print_ok "Launcher copied to Desktop: $DESKTOP_DIR/$DESKTOP_LAUNCHER_FILE"
    else
        print_warn "Desktop directory '$DESKTOP_DIR' not found or not writable. Skipping desktop copy."
    fi
    # *** END ADDED SECTION ***


    # Attempt to update the desktop database (might require user logout/login to see changes)
    if command -v update-desktop-database &> /dev/null; then
        print_info "Updating desktop database..."
        update-desktop-database "$USER_APP_DIR"
    else
        print_warn "'update-desktop-database' command not found. You may need to log out and back in to see the launcher in your menu."
    fi
}


cleanup_setup_files() {
    # Deletes this setup script and the requirements file
    print_header "Cleaning Up Setup Files"
    # Delete requirements file if it exists
    if [[ -f "$REQUIREMENTS_PATH" ]]; then
        print_info "Deleting $REQUIREMENTS_FILE..."
        rm -f -- "$REQUIREMENTS_PATH"
    fi
    # Delete this setup script itself
    print_info "Deleting setup script: $0"
    rm -f -- "$0"
}

# --- Main Execution Logic ---

print_header "Starting CivicEye Setup"
print_info "Script directory: $SCRIPT_DIR"

# Check OS Type
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    print_warn "This setup script is primarily designed for Linux."
    print_warn "MacOS or other OS users may need to install dependencies manually (Python 3.8+, pip, venv, Tkinter)."
    # Decide whether to exit or proceed with caution
    # exit 1 # Option: Exit if not Linux
fi

# Check system dependencies first, install if needed
PYTHON_CMD_USED="python3" # Default
if ! check_system_deps; then
    print_header "Installing System Dependencies"
    PYTHON_CMD_USED=$(install_system_deps) # Get python command used by installer
    print_ok "System dependencies installation attempted."
    # Verify again after installation attempt
    if ! check_system_deps; then
        print_error "System dependencies still missing after installation attempt. Please install manually."
        exit 1
    fi
else
    print_info "System dependencies already met."
fi


# Setup the virtual environment and install Python packages
# Pass the correct python command (python or python3) to setup_venv
setup_venv "$PYTHON_CMD_USED"

# Create the launcher .desktop file that the user will run
create_desktop_launcher

# --- Final Completion Message ---
echo ""
echo -e "${COLOR_BOLD}==================================================${COLOR_RESET}"
echo -e "${COLOR_BOLD}${COLOR_GREEN} ✅ Setup Complete! ${COLOR_RESET}"
echo -e "${COLOR_BOLD}==================================================${COLOR_RESET}"
echo -e " The application launcher '${COLOR_YELLOW}$APP_NAME${COLOR_RESET}' should now be available"
echo -e " in your system's application menu (you might need to log out/in)."
echo -e " A copy has also been placed on your Desktop (if possible)."
echo -e " You may need to right-click the launcher and 'Allow Launching'."
echo -e "${COLOR_BOLD}==================================================${COLOR_RESET}"
echo ""

# Clean up setup files (this script and requirements.txt) - Runs by default
cleanup_setup_files

exit 0
