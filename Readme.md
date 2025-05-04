# **CivicEye: Linux Version 1.2**

## **Features**

* **Real-Time Helmet Detection:** Identifies individuals as 'With Helmet' (green bounding box) and 'Without Helmet' (red bounding box) using a YOLOv8 model.
* **Multiple Video Sources:** Supports:
    * Local video files (`.mp4`, `.avi`, etc.)
    * Connected PC Webcams
    * RTSP streams from CCTV cameras
* **Frame Saving (for 'Without Helmet' detections):**
    * **Online Mode:** Saves detection details (timestamp, frame number) and potentially frames to a database associated with your `civiceye.my` account. Frame filenames follow `detection_YYYYMMDD_HHMMSS_ms_frame_XXX.jpg`. Requires login via `civiceye.my` credentials.
    * **Offline Mode:** Saves detection frames locally in the `Detects/` folder within the application directory using the same filename format. Uses predefined local credentials.
* **Adjustable Detection Speed:** Choose between 'Fast', 'Balanced', and 'Quality' modes via the side menu. This adjusts frame skipping to balance performance (CPU usage) and detection accuracy based on your hardware.
    * *Fast:* Processes more frames, higher CPU usage, potentially quicker detection.
    * *Balanced:* A standard mix of performance and resource usage.
    * *Quality:* Processes fewer frames, lower CPU usage, might miss very brief events.
* **User Authentication:**
    * **Online Mode:** Login using your registered `civiceye.my` credentials. Requires an active internet connection for login validation.
    * **Offline Mode:** Use predefined credentials (`admin@civiceye` / `civiceye`) for local use without internet or server access.
* **Session Persistence:** Remembers your *online* login session for convenience (cleared on logout). Offline mode does not use persistent sessions.
* **GUI Interface:** Provides a user-friendly graphical interface built with Tkinter and ttkbootstrap themes (Light/Dark toggle).
* **Automated Setup:** Includes a setup script (`setup_civiceye.sh`) for handling dependencies, environment creation, and desktop integration.
* **Desktop Integration:** Creates a `.desktop` launcher for easy access from the application menu and desktop.

---

## **Installation Guide**

### **System Requirements**
* **OS:** Linux (Debian/Ubuntu, Arch, Fedora derivatives recommended; setup script targets these)
* **Processor:** Intel i3 or higher recommended
* **RAM:** 4GB (8GB recommended for smoother performance)
* **Storage:** 25GB free disk space (allows for dependencies, virtual environment, and saved detections)
* **Python:** 3.8+ (The setup script installs `python3-venv` and `python3-pip`)
* **Internet:** Required for initial setup (downloading packages) and for Online Mode login/operation. Optional for Offline Mode after setup.

### **Setup Instructions**
The setup process uses a script (`setup_civiceye.sh`) to automate the installation of system dependencies and Python packages within a dedicated virtual environment.

1.  **Download Project Files:** Obtain the CivicEye project files (e.g., download or clone the repository), ensuring you have `setup_civiceye.sh` and `requirements.txt`.
2.  **Open a Terminal:** Navigate to the directory where you downloaded/cloned the project files (e.g., `cd /path/to/Your_CivicEye_Directory/`).
3.  **Make Setup Script Executable:**
    ```bash
    chmod +x setup_civiceye.sh
    ```
4.  **Run the Setup Script:**
    ```bash
    ./setup_civiceye.sh
    ```
    * The script will attempt to detect your Linux distribution (Debian/Ubuntu, Arch, Fedora).
    * It will prompt for your `sudo` password to install necessary system packages (like `python3-tk`, `python3-pip`, `python3-venv`, etc.).
    * It creates a Python virtual environment named `myenv` within the project directory.
    * It installs all required Python libraries listed in `requirements.txt` into the `myenv` virtual environment.
    * It creates a convenient launcher script named `civiceye.sh` in the project directory.
    * It creates a desktop launcher file (`civiceye.desktop`), attempts to place it in `~/.local/share/applications/` (for the application menu), and copies it to your `~/Desktop` folder.
    * **Important:** Upon successful completion, the script will **delete itself (`setup_civiceye.sh`) and the `requirements.txt` file** to prevent accidental re-runs and keep the directory clean.

---

## **Running the Application**

After the setup is complete, you can run CivicEye using one of the following methods:

1.  **Application Menu / Desktop Icon:**
    * Look for "**CivicEye**" in your system's application menu. (You might need to log out and log back in for it to appear after the first setup).
    * Alternatively, navigate to your Desktop folder and find the `civiceye.desktop` file. Double-click the launcher icon.
    * **First time only:** Your system might ask for permission to run the launcher. If so:
        * Right-click the icon -> Properties -> Permissions -> Check "Allow executing file as program" (or similar wording).
        * Alternatively, you might see a prompt asking to "Trust and Launch". Choose this option.

2.  **Terminal (Manual Launch):**
    * Navigate to the project directory:
        ```bash
        cd /CivicEye/
        ```
    * Activate the virtual environment:
        ```bash
        source myenv/bin/activate
        ```
    * Run the main Python script:
        ```bash
        cd DATA/
        python civiceye.py
        ```
    * When finished, deactivate the environment:
        ```bash
        deactivate
        ```


---

## **Usage Guide**

1.  **Login Screen:**
    * When you start CivicEye, the login screen appears.
    * **Online Mode:** Enter your registered email and password for the `civiceye.my` service. Click "LOGIN". An internet connection check is performed first.
    * **Register:** Clicking "REGISTER" opens the CivicEye registration page (`civiceye.my`) in your default web browser (requires internet).
    * **Offline Mode:** Use the following credentials and click "LOGIN":
        * Email: `admin@civiceye`
        * Password: `civiceye`
        (This mode operates entirely locally, requires no internet post-setup, and does not save online session data).

2.  **Main Application Window:**
    * **Select Video Source:** Use the buttons provided:
        * `Browse File`: Opens a file dialog to select a local video file.
        * `Use PC Camera`: Attempts to access the default system webcam.
        * `Connect CCTV`: Prompts for an RTSP stream URL (e.g., `rtsp://user:pass@ip_address:port/stream`).
    * **Control Detection:**
        * `Start Detection` (Green Button): Begins processing the selected video source. The video preview will display in the central area.
        * `Stop Detection` (Red Button): Halts the current detection process.
    * **Video Preview:** Shows the video feed. Detected objects are highlighted with bounding boxes:
        * Green Box: 'With Helmet'
        * Red Box: 'Without Helmet' (Frames with these detections are saved based on the mode).
    * **Status Bar:** Displays messages about the application's current state (e.g., "Processing video...", "Detection stopped.", "Connecting to camera...") at the bottom.
    * **Side Navigation Menu (☰):** Click the hamburger icon (☰) in the top-left corner to open/close the side panel.
        * `Toggle Theme`: Switches between the light ('litera') and dark ('darkly') UI themes.
        * `Detection Speed`: Choose `Fast`, `Balanced`, or `Quality`.
        * `Logout`: Logs out the current user (stops detection if running and clears any saved online session data). Returns to the login screen.
        * `Exit Application`: Safely closes the CivicEye program.

3.  **Viewing Detections:**
    * **Online Mode:** Detections ('Without Helmet') are recorded in a database linked to your account. Accessing these records might require specific features within the application or external tools depending on the database implementation. Frame filenames follow the pattern `detection_YYYYMMDD_HHMMSS_ms_frame_XXX.jpg`.
    * **Offline Mode:** Frames ('Without Helmet') are saved as JPEG images directly into the `Detects/` folder located within the main application directory (`Your_CivicEye_Directory/Detects/`). You can browse this folder using your system's file manager. Filenames follow the same pattern: `detection_YYYYMMDD_HHMMSS_ms_frame_XXX.jpg`.

---

## **Technical Overview**

### **Programming Language:**
* **Python 3.8+**: Core application logic, AI integration, and GUI.

### **Core Libraries:**
1.  **OpenCV (cv2)**: Handles video stream reading (files, cameras, RTSP), frame processing, image manipulation, and saving captured violation images.
2.  **YOLOv8 (Ultralytics)**: Provides the real-time object detection model for identifying helmet usage.
3.  **Tkinter & ttkbootstrap**: Used to create the graphical user interface (GUI), providing widgets and modern themes (light/dark).
4.  **Pillow (PIL)**: Used for image operations, especially within the GUI context.
5.  **Requests**: Used for online authentication and potential communication with the `civiceye.my` backend (in Online Mode).
6.  **(Potential Database Library)**: Depending on the implementation for Online Mode storage (e.g., `sqlite3` for a local DB, or others like `psycopg2` for PostgreSQL if interacting with a remote server).

---

## **Version 1.2 Release Notes**
* **GUI Implementation:** Introduced a graphical user interface using Tkinter and ttkbootstrap, replacing command-line operation.
* **Online/Offline Modes:** Added distinct operating modes with user authentication (online via `civiceye.my`, offline with fixed credentials).
* **Multiple Video Sources:** Expanded input options to include local files, PC webcams, and RTSP streams via the GUI.
* **Adjustable Detection Speed:** Implemented 'Fast', 'Balanced', and 'Quality' settings to manage performance vs. accuracy trade-offs.
* **Online Session Persistence:** Added functionality to remember online login sessions.
* **Database Integration (Online Mode):** Framework for saving detection data to a database when operating online.
* **Enhanced Setup Script:** Improved `setup_civiceye.sh` to handle GUI dependencies (`requirements.txt`) and integrate with the desktop environment (`civiceye.desktop`).
* **Self-Cleaning Setup:** The setup script now removes itself and `requirements.txt` after successful execution.
* **Theming:** Added light ('litera') and dark ('darkly') theme options accessible from the GUI.
