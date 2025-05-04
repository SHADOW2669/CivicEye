# CivicEye - Windows

## Features

* **Real-Time Helmet Detection:** Identifies individuals as 'With Helmet' (green bounding box) and 'Without Helmet' (red bounding box) using a YOLOv8 model.
* **Multiple Video Sources:** Supports:
    * Local video files (`.mp4`, `.avi`, etc.)
    * Connected PC Webcams
    * RTSP streams from CCTV cameras
* **Frame Saving (for 'Without Helmet' detections):**
    * **Online Mode:** Saves detection details (timestamp, frame number) and potentially frames to a database associated with your `civiceye.my` account. Frame filenames follow `detection_YYYYMMDD_HHMMSS_ms_frame_XXX.jpg`. Requires login via `civiceye.my` credentials.
    * **Offline Mode:** Saves detection frames locally in the `Detects/` folder within the application directory using the same filename format. Uses predefined local credentials.
* **Adjustable Detection Speed:** Choose between 'Fast', 'Balanced', and 'Quality' modes via the side menu. This adjusts frame skipping to balance performance (CPU usage) and detection accuracy based on your hardware.
    * *Fast (Skip=15):* Processes more frames, higher CPU usage, potentially quicker detection.
    * *Balanced (Skip=30):* A standard mix of performance and resource usage (Default).
    * *Quality (Skip=60):* Processes fewer frames, lower CPU usage, might miss very brief events.
* **User Authentication:**
    * **Online Mode:** Login using your registered `civiceye.my` credentials. Requires an active internet connection for login validation.
    * **Offline Mode:** Use predefined credentials (`admin@civiceye` / `civiceye`) for local use without internet or server access.
* **Session Persistence:** Remembers your *online* login session for convenience (cleared on logout). Offline mode does not use persistent sessions.
* **GUI Interface:** Provides a user-friendly graphical interface built with Tkinter and ttkbootstrap themes (Light/Dark toggle).
* **Automated Setup:** Includes a setup script (`setup_civiceye.bat`) for handling dependencies and environment creation.
* **Easy Launch:** Creates a simple launcher script (`run_civiceye.bat`) for starting the application.

---

## **Installation Guide For Windows**

### **System Requirements**
* **OS:** Windows 10 or later (64-bit recommended)
* **Processor:** Intel i3 or higher recommended
* **RAM:** 4GB (8GB recommended for smoother performance)
* **Storage:** Approx. 5GB free disk space (for Python packages, virtual environment, and saved detections)
* **Python:** 3.8+ **must be installed** and **added to the system PATH**.
    * Download from [python.org](https://www.python.org/downloads/windows/).
    * **Crucial:** During installation, ensure the checkbox "Add Python [version] to PATH" or "Add python.exe to PATH" is selected.
* **Internet:** Required during the initial setup (`setup_civiceye.bat`) to download Python packages. Optional for Offline Mode afterwards. Required for Online Mode login/operation.

### **Setup Instructions**
The setup process uses a batch script (`setup_civiceye.bat`) to automate the installation of Python packages within a dedicated virtual environment.

1.  **Download Project Files:** Obtain the CivicEye project files (e.g., download and extract a ZIP archive), ensuring you have `setup_civiceye.bat`, `requirements.txt`, and the `DATA` folder (containing `civiceye.py` and `icon.ico`).
2.  **Navigate to the Directory:** Open File Explorer and go to the folder where you extracted the project files.
3.  **Run the Setup Script:**
    * **Double-click** the `setup_civiceye.bat` file.
    * A command prompt window will open.
    * The script will check if you have Python 3.8+ installed and added to your PATH.
    * It will create a Python virtual environment named `myenv` within the project directory.
    * It will install all required Python libraries listed in `requirements.txt` into the `myenv` virtual environment. This step might take several minutes depending on your internet speed.
    * It will create a convenient launcher script named `run_civiceye.bat` in the project directory.
    * It will create a Desktop shortcut named `CivicEye.lnk` in the same folder (using `icon.ico` if available).
    * **Important:** At the end, it will ask if you want to delete the setup script (`setup_civiceye.bat`) and `requirements.txt`. Type `Y` or `N` and press Enter. It's generally safe to delete them after setup is complete, but keeping `requirements.txt` can be useful.
    * The command prompt window will close after you press a key.

---

## **Running the Application (Windows)**

After the setup is complete:

1.  **Navigate** to the project directory in File Explorer.
2.  Find the file named **`run_civiceye.bat`**.
3.  **Double-click `run_civiceye.bat`** to start the application.
    * The first time, a command prompt might flash briefly while the virtual environment activates, then the main application window should appear.

*(Alternatively, you can use the `CivicEye.lnk` shortcut created by the setup script in the project folder).*

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
    * **Menu Button (☰):** Click the hamburger icon (☰) in the top-left corner to open/close the side navigation panel.
    * **Side Navigation:**
        * `Toggle Theme`: Switches between the light ('litera') and dark ('darkly') UI themes.
        * `Detection Speed`: Choose `Fast (Skip=15)`, `Balanced (Skip=30)`, or `Quality (Skip=60)`.
        * `Logout`: Logs out the current user (stops detection if running and clears any saved online session data). Returns to the login screen.
        * `Exit Application`: Safely closes the CivicEye program.
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

## **Windows Version**
* **GUI Implementation:** Introduced a graphical user interface using Tkinter and ttkbootstrap.
* **Online/Offline Modes:** Added distinct operating modes with user authentication (online via `civiceye.my`, offline with fixed credentials).
* **Multiple Video Sources:** Expanded input options to include local files, PC webcams, and RTSP streams via the GUI.
* **Adjustable Detection Speed:** Implemented 'Fast', 'Balanced', and 'Quality' settings to manage performance vs. accuracy trade-offs.
* **Online Session Persistence:** Added functionality to remember online login sessions.
* **Local Saving:** Implemented local saving of 'Without Helmet' detection frames to the `Detects/` folder. Online database saving might be separate.
* **Windows Setup Script (`setup_civiceye.bat`):** Created a batch script to automate dependency installation within a virtual environment (`myenv`) and create a launcher script (`run_civiceye.bat`) and shortcut (`CivicEye.lnk`).
* **Windows Uninstaller (`uninstall_civiceye.bat`):** Provided a script to remove installed components.
* **Theming:** Added light ('litera') and dark ('darkly') theme options accessible from the GUI.
* **Side Navigation:** Implemented a side panel for settings and actions instead of a traditional menu bar.
