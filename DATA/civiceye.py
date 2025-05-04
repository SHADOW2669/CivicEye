import requests
import datetime
import cv2
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, font as tkFont
from tkinter import ttk
from ultralytics import YOLO
from PIL import Image, ImageTk
import os
import webbrowser
import json
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import socket # Added for internet connection check
import time # Added for potential delays/retries

# --- Global Variables ---
stop_flag = threading.Event()
video_source = None
frame_position = 0
logged_in = False
user_id = None
detection_thread = None
root = None
status_label = None
app_frame = None
login_frame = None
side_nav_frame = None
side_nav_visible = False
menu_btn = None # Added global reference for menu button

username_entry = None
password_entry = None
login_button = None
register_button = None

github_button = None
contact_button = None

browse_button, webcam_button, cctv_button = None, None, None
start_button, stop_button = None, None
video_label = None

SESSION_FILE = "civiceye_session.json"
current_frame_skip = 30

OFFLINE_EMAIL = "admin@civiceye"
OFFLINE_PASS = "civiceye"
OFFLINE_USER_ID = "offline_admin"

API_BASE_URL = "https://civiceye.my/api"
# Use a reliable host for internet check (Google's public DNS)
INTERNET_CHECK_HOST = "8.8.8.8"
INTERNET_CHECK_PORT = 53
INTERNET_CHECK_TIMEOUT = 3 # Seconds for internet check
SERVER_CHECK_TIMEOUT = 5 # Seconds for server status check
UPLOAD_TIMEOUT = 15 # Seconds for upload request

# --- Font Configuration ---
PRIMARY_FONT_FAMILY = "Poppins"
FALLBACK_FONT_FAMILY = "Helvetica Neue"
FALLBACK_FONT_FAMILY_2 = "Segoe UI"
FALLBACK_FONT_FAMILY_3 = "Helvetica"
FALLBACK_FONT_FAMILY_4 = "Arial"
FALLBACK_FONT_FAMILY_5 = "sans-serif"

def create_font(size, weight="normal", slant="roman", primary=PRIMARY_FONT_FAMILY):
    """Creates a tk.Font object, attempting primary font first, then fallbacks."""
    try:
        font_families = tkFont.families()
        chosen_family = primary if primary in font_families else FALLBACK_FONT_FAMILY
        if chosen_family not in font_families: chosen_family = FALLBACK_FONT_FAMILY_2
        if chosen_family not in font_families: chosen_family = FALLBACK_FONT_FAMILY_3
        if chosen_family not in font_families: chosen_family = FALLBACK_FONT_FAMILY_4
        if chosen_family not in font_families: chosen_family = FALLBACK_FONT_FAMILY_5

        return tkFont.Font(family=chosen_family, size=size, weight=weight, slant=slant)
    except tk.TclError:
        print(f"Warning: Could not create font '{primary}'. Using system default.")
        return tkFont.Font(size=size, weight=weight, slant=slant) # Fallback to system default

# --- Custom Dialogs ---
def show_custom_dialog(title, message, dialog_type="error"):
    """Displays a themed custom dialog box."""
    if not root:
        print(f"Dialog Error: Root window not available for '{title}'")
        return

    dialog = tk.Toplevel(root)
    dialog.title(title)
    dialog.resizable(False, False)
    dialog.grab_set() # Make modal
    dialog.transient(root) # Keep on top of root

    dialog_font = create_font(10)

    # Try to apply theme colors
    try:
        style = tb.Style.get_instance()
        bg_color = style.colors.get('bg')
        fg_color = style.colors.get('fg')
        dialog.config(bg=bg_color)
    except Exception as e:
        print(f"Debug: Could not get theme bg/fg for dialog: {e}")
        bg_color = None
        fg_color = None

    frame = tk.Frame(dialog, padx=20, pady=15)
    if bg_color: frame.config(bg=bg_color)
    frame.pack(expand=True, fill=BOTH)

    # Icon based on type
    try:
        icon_color = style.colors.get('warning') if dialog_type == "warning" else style.colors.get('danger')
    except:
        icon_color = "orange" if dialog_type == "warning" else "red"

    icon_label = tk.Label(frame, text="!" if dialog_type == "warning" else "X", font=create_font(14, weight="bold"), fg=icon_color)
    if bg_color: icon_label.config(bg=bg_color)
    icon_label.pack(side=LEFT, padx=(0, 10))

    # Message label
    msg_label = tk.Label(frame, text=message, font=dialog_font, justify=LEFT, wraplength=300)
    if bg_color: msg_label.config(bg=bg_color)
    if fg_color: msg_label.config(fg=fg_color)
    msg_label.pack(side=LEFT, fill=X, expand=True)

    # OK Button
    button_frame = tk.Frame(dialog, pady=10)
    if bg_color: button_frame.config(bg=bg_color)
    button_frame.pack(fill=X)

    s = ttk.Style()
    s.configure('Dialog.TButton', font=dialog_font)
    ok_button = ttk.Button(button_frame, text="OK", command=dialog.destroy, width=10, style='Dialog.TButton')
    ok_button.pack()
    dialog.bind('<Return>', lambda event=None: ok_button.invoke()) # Bind Enter key

    # Center dialog relative to root window
    root.update_idletasks() # Ensure window dimensions are calculated
    dialog_width = dialog.winfo_reqwidth()
    dialog_height = dialog.winfo_reqheight()
    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    x = root_x + (root_width // 2) - (dialog_width // 2)
    y = root_y + (root_height // 2) - (dialog_height // 2)
    dialog.geometry(f"+{x}+{y}")

    dialog.wait_window() # Wait for dialog to close

def show_custom_error(title, message):
    """Convenience function for error dialog."""
    show_custom_dialog(title, message, dialog_type="error")

def show_custom_warning(title, message):
    """Convenience function for warning dialog."""
    show_custom_dialog(title, message, dialog_type="warning")

# --- Session Management ---
def save_session(uid):
    """Saves the user ID to the session file, skipping offline user."""
    if uid == OFFLINE_USER_ID:
        print("Offline user, session not saved.")
        return
    try:
        with open(SESSION_FILE, 'w') as f:
            json.dump({'user_id': uid}, f)
        print("Session saved.")
    except IOError as e:
        print(f"Error saving session: {e}")

def load_session():
    """Loads user ID from session file if it exists and is valid."""
    global user_id, logged_in
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, 'r') as f:
                session_data = json.load(f)
                loaded_uid = session_data.get('user_id')
                # Ensure loaded ID is not the offline marker
                if loaded_uid and loaded_uid != OFFLINE_USER_ID:
                    user_id = loaded_uid
                    logged_in = True
                    print(f"Session loaded for User ID: {user_id}")
                    return True
                elif loaded_uid == OFFLINE_USER_ID:
                    # If we find an offline marker, delete it on load
                    print("Found offline session marker. Deleting.")
                    delete_session()
                    return False

        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading session file: {e}")
            delete_session() # Delete corrupted or invalid session file
    return False

def delete_session():
    """Deletes the session file."""
    if os.path.exists(SESSION_FILE):
        try:
            os.remove(SESSION_FILE)
            print("Session deleted.")
        except OSError as e:
            print(f"Error deleting session file: {e}")

# --- Connectivity Checks ---
def check_internet_connection(host=INTERNET_CHECK_HOST, port=INTERNET_CHECK_PORT, timeout=INTERNET_CHECK_TIMEOUT):
    """Checks for internet connectivity by trying to connect to a reliable host."""
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        print("Internet connection check: Success")
        return True
    except socket.error as ex:
        print(f"Internet connection check failed: {ex}")
        return False

def check_server_status(url=API_BASE_URL, timeout=SERVER_CHECK_TIMEOUT):
    """Checks if the API server is reachable."""
    try:
        # Use HEAD request to be lighter, fallback to GET if HEAD is not allowed
        response = requests.head(url, timeout=timeout)
        # Consider any 2xx or 3xx status as reachable
        if response.status_code < 400:
             print(f"Server status check: Success (Status: {response.status_code})")
             return True
        else:
             print(f"Server status check: Failed (Status: {response.status_code})")
             return False
    except requests.exceptions.Timeout:
        print("Server status check: Failed (Timeout)")
        return False
    except requests.exceptions.ConnectionError:
        print("Server status check: Failed (Connection Error)")
        return False
    except requests.exceptions.RequestException as e:
        print(f"Server status check: Failed (Request Exception: {e})")
        # Fallback attempt with GET if HEAD failed unexpectedly (e.g., 405 Method Not Allowed)
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code < 400:
                print(f"Server status check (GET fallback): Success (Status: {response.status_code})")
                return True
            else:
                print(f"Server status check (GET fallback): Failed (Status: {response.status_code})")
                return False
        except requests.exceptions.RequestException as e_get:
            print(f"Server status check (GET fallback): Failed (Request Exception: {e_get})")
            return False
    except Exception as e:
        print(f"Server status check: Failed (Unexpected Error: {e})")
        return False

# --- Authentication ---
def login():
    """Handles the user login process, including offline mode and connectivity checks."""
    global logged_in, user_id, app_frame, login_frame

    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not password:
        show_custom_warning("Validation Error", "Email and Password are required.")
        return

    # --- Offline Login ---
    if username == OFFLINE_EMAIL and password == OFFLINE_PASS:
        print("Offline login successful.")
        user_id = OFFLINE_USER_ID
        logged_in = True
        login_frame.pack_forget()
        if app_frame is None:
            app_frame = create_app_frame()
        create_side_nav() # Ensure side nav is created/recreated
        app_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        update_status("Offline login successful. Select a source.")
        update_button_states()
        return # Exit after successful offline login

    # --- Online Login ---
    update_status("Checking connectivity...")
    root.update_idletasks()

    # 1. Check Internet Connection
    if not check_internet_connection():
        show_custom_error("Connection Error", "No internet connection detected.\nPlease check your network settings or use offline mode if available.")
        update_status("Login failed: No internet.")
        return

    # 2. Check Server Status
    if not check_server_status():
        show_custom_error("Server Error", "Could not reach the CivicEye server.\nThe server might be offline or unreachable. Please try again later or use offline mode.")
        update_status("Login failed: Server unreachable.")
        return

    # 3. Attempt Online Login via API
    try:
        update_status("Logging in via server...")
        root.update_idletasks()

        response = requests.post(f"{API_BASE_URL}/login.php", json={
            "email": username,
            "password": password
        }, timeout=10) # Keep API call timeout reasonable
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        result = response.json()

        if result.get("status") == "success" and "user" in result and "id" in result["user"]:
            user_id = result["user"]["id"]
            print(f"Online Login successful. User ID: {user_id}")
            save_session(user_id) # Save session for online users

            login_frame.pack_forget()
            if app_frame is None:
                app_frame = create_app_frame()
            create_side_nav() # Ensure side nav is created/recreated
            app_frame.pack(side=RIGHT, fill=BOTH, expand=True)
            logged_in = True
            update_status("Login successful. Select a source.")
            update_button_states()
            # Re-apply theme in case login changed it (less likely now but good practice)
            current_theme = root.style.theme_use()
            root.style.theme_use(current_theme)

        else:
            # Handle specific API login failures
            show_custom_error("Login Failed", result.get("message", "Invalid credentials or unexpected server response."))
            print(f"Login failed API response: {result}")
            update_status("Login failed. Please check credentials.")
    except requests.exceptions.Timeout:
        show_custom_error("Connection Error", "Login request timed out.\nThe server took too long to respond. Please try again later.")
        update_status("Login failed: API Timeout.")
    except requests.exceptions.RequestException as e:
        show_custom_error("Connection Error", f"Couldn't connect to the login server:\n{e}")
        update_status("Login failed: API Connection error.")
    except Exception as e:
        show_custom_error("Error", f"An unexpected error occurred during login:\n{e}")
        update_status("Login failed: Unexpected error.")
        import traceback
        traceback.print_exc()

def logout():
    """Logs the user out, clears session, and returns to the login screen."""
    global logged_in, user_id, app_frame, login_frame, side_nav_frame, side_nav_visible

    print("Logging out...")
    # Stop detection if running
    if detection_thread and detection_thread.is_alive():
        print("Stopping detection before logout...")
        stop_detection()
        # Optionally wait briefly for the thread to stop
        # detection_thread.join(timeout=0.5)

    # Delete session only if it was an online user
    if user_id != OFFLINE_USER_ID:
        delete_session()

    logged_in = False
    user_id = None

    # Hide side navigation if visible
    if side_nav_visible and side_nav_frame and side_nav_frame.winfo_exists():
        side_nav_frame.pack_forget()
        side_nav_visible = False

    # Hide main application frame
    if app_frame and app_frame.winfo_exists():
        app_frame.pack_forget()

    # Show login frame
    if login_frame:
        # Clear password field for security
        if password_entry and password_entry.winfo_exists():
            password_entry.delete(0, tk.END)
        login_frame.pack(fill=BOTH, expand=TRUE)
    else:
        # Recreate login frame if it was destroyed (shouldn't normally happen)
        login_frame = create_login_frame()
        login_frame.pack(fill=BOTH, expand=TRUE)

    update_status("Logged out. Please log in.")
    update_button_states()

def register():
    """Opens the registration page in the default web browser."""
    print("Register button clicked.")
    open_url("https://civiceye.my/login.php") # Assuming registration is on the login page

def open_url(url):
    """Opens a URL in the default web browser."""
    try:
        webbrowser.open_new(url)
    except Exception as e:
        print(f"Error opening URL {url}: {e}")
        show_custom_error("Error", f"Could not open the link:\n{e}")

# --- UI Theme and Settings ---
def toggle_theme():
    """Toggles between 'darkly' and 'litera' themes."""
    global root
    if root:
        try:
            current_theme = root.style.theme_use()
            new_theme = "litera" if current_theme == "darkly" else "darkly"
            root.style.theme_use(new_theme)
            print(f"Switched to {new_theme} theme")
            update_button_states() # Update buttons which might change style
            # Update side nav style if visible
            if side_nav_frame and side_nav_frame.winfo_exists():
                 style = tb.Style.get_instance()
                 nav_bootstyle = "light" if style.theme.type == 'light' else "dark"
                 side_nav_frame.config(bootstyle=nav_bootstyle)

        except Exception as e:
            print(f"Error switching theme: {e}")

def set_frame_skip(value):
    """Sets the frame skip value for detection performance."""
    global current_frame_skip
    if isinstance(value, int) and value > 0:
        current_frame_skip = value
        print(f"Frame skip set to: {current_frame_skip}")
        update_status(f"Detection Speed set (Process 1 frame every {current_frame_skip})")
    else:
        print(f"Invalid frame skip value: {value}")

# --- File System Utilities ---
def get_script_directory():
    """Gets the directory where the script is running."""
    try:
        # Standard way using __file__
        return os.path.dirname(os.path.abspath(__file__))
    except NameError:
        # Fallback for environments where __file__ is not defined (e.g., interactive)
        print("Warning: __file__ not defined. Using current working directory.")
        return os.getcwd()

# --- Upload Detection (Helper Function) ---
def upload_detection_data(data, image_path):
    """
    Uploads detection data and image to the server in a separate thread.
    Args:
        data (dict): Dictionary containing 'user_id', 'timestamp', 'frame', 'helmet'.
        image_path (str): Path to the locally saved image file.
    """
    if not user_id or user_id == OFFLINE_USER_ID:
        print("Skipping upload: Offline user or user_id not set.")
        return

    upload_url = f"{API_BASE_URL}/save_detect.php"
    print(f"Attempting to upload detection to: {upload_url}")

    try:
        with open(image_path, 'rb') as image_file:
            files = {'image': (os.path.basename(image_path), image_file, 'image/jpeg')}
            response = requests.post(upload_url, data=data, files=files, timeout=UPLOAD_TIMEOUT)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

            try:
                result = response.json()
                if result.get("status") == "success":
                    print(f"✅ Successfully uploaded detection: {os.path.basename(image_path)}")
                    update_status("Detection running... (Violation uploaded)")
                else:
                    print(f"❌ Upload failed (API): {result.get('message', 'Unknown API error')}")
                    update_status(f"Warning: Upload failed - {result.get('message', 'API Error')}")
            except json.JSONDecodeError:
                print(f"❌ Upload failed: Invalid JSON response from server. Status: {response.status_code}, Response: {response.text[:100]}...")
                update_status("Warning: Upload failed - Invalid Server Response")
            except Exception as json_e:
                 print(f"❌ Error processing upload response: {json_e}")
                 update_status("Warning: Upload response error")


    except requests.exceptions.Timeout:
        print("❌ Upload failed: Request timed out.")
        update_status("Warning: Upload timed out")
    except requests.exceptions.ConnectionError:
        print("❌ Upload failed: Could not connect to the server.")
        update_status("Warning: Upload connection error")
    except requests.exceptions.RequestException as e:
        print(f"❌ Upload failed: {e}")
        update_status(f"Warning: Upload failed - {e}")
    except IOError as e:
        print(f"❌ Upload failed: Could not read image file {image_path}. Error: {e}")
        update_status("Warning: Upload failed - File Read Error")
    except Exception as e:
        print(f"❌ An unexpected error occurred during upload: {e}")
        update_status("Warning: Unexpected upload error")
        import traceback
        traceback.print_exc()

# --- Core Detection Logic ---
def run_detection():
    """The main detection loop running in a separate thread."""
    global frame_position, user_id, video_source, stop_flag, video_label, current_frame_skip

    if video_source is None:
        print("No video source specified.")
        update_status("Error: No video source selected.")
        update_button_states()
        return

    if not user_id: # Should not happen if UI logic is correct, but safety check
        print("Error: User ID not set. Cannot run detection.")
        update_status("Error: Not logged in.")
        show_custom_error("Login Error", "User is not logged in. Please restart and log in.")
        update_button_states()
        return

    model = None
    # Load YOLO Model
    try:
        script_dir = get_script_directory()
        weights_path = os.path.join(script_dir, "Weights", "best.pt")
        print(f"Loading model from: {weights_path}")
        update_status("Loading detection model...")
        if not os.path.exists(weights_path):
             raise FileNotFoundError(f"Model file not found at {weights_path}.\nPlease ensure 'Weights/best.pt' exists in the application directory.")
        model = YOLO(weights_path)
        classNames = ['With Helmet', 'Without Helmet'] # Make sure this matches your model
        print("Model loaded successfully.")
    except FileNotFoundError as e:
         show_custom_error("Model Error", f"{e}")
         update_status("Error: Model file not found.")
         update_button_states()
         return
    except ImportError:
         show_custom_error("Dependency Error", "Ultralytics YOLO library not found or import failed.\nPlease install it (`pip install ultralytics`).")
         update_status("Error: YOLO library missing.")
         update_button_states()
         return
    except Exception as e:
        show_custom_error("Model Error", f"Failed to load YOLO model.\nCheck file integrity and dependencies.\nError: {e}")
        update_status("Error: Model load failed.")
        update_button_states()
        import traceback
        traceback.print_exc()
        return

    cap = None
    # Open Video Source
    try:
        print(f"Attempting to open video source: {video_source}")
        update_status(f"Opening video source...") # Keep status concise
        cap = cv2.VideoCapture(video_source)

        # Try alternative backends if default fails
        if not cap.isOpened():
            print("Default backend failed, trying alternatives...")
            backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_V4L2, cv2.CAP_GSTREAMER, cv2.CAP_FFMPEG] # Common backends
            for backend in backends:
                print(f"Trying backend: {backend}")
                cap = cv2.VideoCapture(video_source, backend)
                if cap.isOpened():
                    print(f"Opened successfully with backend: {backend}")
                    break
            # If still not opened after trying backends
            if not cap.isOpened():
                 raise IOError(f"Cannot open video source: {video_source} with any available backend.")

        # Get video properties
        source_fps = cap.get(cv2.CAP_PROP_FPS)
        source_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        source_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"Source Video Details: FPS={source_fps if source_fps > 0 else 'N/A'}, Size={source_width}x{source_height}")

        # Set starting position for video files if needed
        if isinstance(video_source, str) and os.path.exists(video_source): # Check if it's a file path
             if frame_position > 0:
                 success = cap.set(cv2.CAP_PROP_POS_FRAMES, frame_position)
                 if success:
                     print(f"Starting video from frame: {frame_position}")
                 else:
                     print(f"Warning: Could not set starting frame to {frame_position}. Starting from beginning.")
                     frame_position = 0 # Reset if setting failed
        print("Video source opened successfully.")

    except Exception as e:
        show_custom_error("Video Error", f"Failed to open video source: {video_source}\nError: {e}")
        update_status("Error: Video source failed.")
        if cap: cap.release() # Ensure cap is released on error
        update_button_states()
        import traceback
        traceback.print_exc()
        return

    # Prepare Detections Directory
    try:
        script_dir = get_script_directory()
        detects_dir = os.path.join(script_dir, "Detects")
        os.makedirs(detects_dir, exist_ok=True)
        print(f"Detections will be saved locally in: {detects_dir}")
    except Exception as e:
        show_custom_error("Directory Error", f"Could not create 'Detects' directory:\n{e}")
        update_status("Error: Cannot create save directory.")
        update_button_states()
        if cap: cap.release()
        return

    # --- Detection Loop ---
    frame_count = 0
    frame_skip = current_frame_skip # Use the globally set frame skip
    print(f"Using Frame Skip: {frame_skip} (Process 1 out of every {frame_skip} frames)")

    preview_interval = 1 # Update preview every processed frame
    update_status("Detection running...")
    processed_frame_counter = 0
    detection_count = 0 # Count 'Without Helmet' detections in this run
    upload_threads = [] # Keep track of upload threads

    while not stop_flag.is_set():
        try:
            # Read frame
            ret, img = cap.read()
            if not ret:
                print("End of video stream or cannot read frame.")
                update_status("End of video stream.")
                break # Exit loop if no more frames

            current_frame_pos = cap.get(cv2.CAP_PROP_POS_FRAMES) # Get current frame number
            frame_count += 1

            # Frame Skipping Logic
            if frame_count % frame_skip != 0:
                continue # Skip this frame

            processed_frame_counter += 1

            # Resize frame for consistent processing and display
            target_width = 640
            target_height = 480
            try:
                img_resized = cv2.resize(img, (target_width, target_height))
            except cv2.error as resize_error:
                 print(f"Error resizing frame: {resize_error}. Skipping frame.")
                 continue # Skip frame if resize fails

            # Perform YOLO detection
            results = model(img_resized, stream=False, verbose=False, conf=0.5)

            detection_made_in_frame = False # Track if a 'Without Helmet' was found in this frame
            detected_label_text = "" # Store the label text if detection occurs

            # Process detection results
            for r in results:
                for box in r.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = round(box.conf[0].item(), 2)
                    cls_id = int(box.cls[0])

                    if 0 <= cls_id < len(classNames):
                        label_text = classNames[cls_id]
                        label = f'{label_text} {conf:.2f}'
                        color = (0, 255, 0) if label_text == 'With Helmet' else (0, 0, 255)
                        cv2.rectangle(img_resized, (x1, y1), (x2, y2), color, 2)
                        (text_width, text_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                        bg_y1 = y1 - text_height - baseline - 2 if y1 - text_height - baseline - 2 > 0 else y1 + 2
                        bg_y2 = y1 - baseline + 2 if y1 - text_height - baseline - 2 > 0 else y1 + text_height + baseline + 2
                        cv2.rectangle(img_resized, (x1, bg_y1), (x1 + text_width, bg_y2), color, -1)
                        text_y = y1 - baseline - 2 if y1 - text_height - baseline - 2 > 0 else y1 + text_height + 2
                        cv2.putText(img_resized, label, (x1 + 1, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

                        if label_text == "Without Helmet":
                            detection_made_in_frame = True
                            detected_label_text = label_text # Store 'Without Helmet'
                            detection_count += 1
                    else:
                        print(f"Warning: Detected class ID {cls_id} is out of bounds for classNames list.")

            # --- Save and Upload Logic ---
            if detection_made_in_frame:
                save_path = None # Initialize save_path
                try:
                    # 1. Save Locally
                    detection_time_obj = datetime.datetime.now()
                    time_str_file = detection_time_obj.strftime('%Y%m%d_%H%M%S_%f')[:-3] # For filename
                    time_str_api = detection_time_obj.strftime('%Y-%m-%d %H:%M:%S') # For API timestamp
                    filename = f"detection_{time_str_file}_frame_{int(current_frame_pos)}.jpg"
                    save_path = os.path.join(detects_dir, filename)
                    cv2.imwrite(save_path, img_resized) # Save the processed frame with boxes
                    print(f"  Detection saved locally: {filename}")
                    update_status(f"Detection running... ('Without Helmet' saved locally)")

                    # 2. Upload to Server (if online user)
                    if user_id != OFFLINE_USER_ID:
                        # Prepare data for upload
                        upload_data = {
                            'user_id': user_id,
                            'timestamp': time_str_api, # Use formatted string
                            'frame': int(current_frame_pos),
                            'helmet': detected_label_text # Send 'Without Helmet' string
                        }
                        # Start upload in a separate thread to avoid blocking
                        upload_thread = threading.Thread(target=upload_detection_data, args=(upload_data, save_path), daemon=True)
                        upload_threads.append(upload_thread)
                        upload_thread.start()
                    else:
                        print("  Offline user: Skipping server upload.")

                except Exception as save_or_upload_e:
                    print(f"❌ Error during local save or initiating upload: {save_or_upload_e}")
                    update_status(f"Error saving/uploading: {save_or_upload_e}")
                    # Optionally: If local save failed, don't attempt upload
                    # if save_path is None: continue # Or handle differently

            # Update Video Preview Label
            if processed_frame_counter % preview_interval == 0:
                 if video_label and video_label.winfo_exists():
                     try:
                        img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
                        img_pil = Image.fromarray(img_rgb)
                        imgtk = ImageTk.PhotoImage(image=img_pil)
                        video_label.after(0, update_video_label, imgtk)
                     except Exception as e:
                         print(f"Error updating video preview: {e}")
                 else:
                     print("Video label no longer exists, stopping preview updates.")
                     if not stop_flag.is_set(): stop_flag.set()

        except cv2.error as e:
            print(f"OpenCV Error during processing: {e}")
            update_status(f"OpenCV Error: {e}")
            if not stop_flag.is_set(): stop_flag.set()
            break
        except Exception as e:
            print(f"Unexpected error in detection loop: {e}")
            update_status(f"Runtime Error: {e}")
            import traceback
            traceback.print_exc()
            if not stop_flag.is_set(): stop_flag.set()
            break
    # --- End of Detection Loop ---

    print("Detection loop finished or stopped.")
    if cap:
        cap.release()
        print("Video capture released.")

    # Wait briefly for any outstanding upload threads to finish
    print(f"Waiting for {len(upload_threads)} upload thread(s) to complete...")
    active_threads = [t for t in upload_threads if t.is_alive()]
    while active_threads:
         print(f"  {len(active_threads)} uploads still in progress...")
         time.sleep(0.5) # Wait half a second
         # Join threads with a timeout to avoid waiting indefinitely
         for t in active_threads:
             t.join(timeout=0.1) # Short timeout per thread check
         active_threads = [t for t in upload_threads if t.is_alive()]
    print("All upload threads finished or timed out.")


    # Clear the video label after stopping
    if root and root.winfo_exists() and video_label and video_label.winfo_exists():
        video_label.after(0, clear_video_label)

    # Final status update
    final_status = "Detection stopped."
    if detection_count > 0:
        final_status += f" ({detection_count} 'Without Helmet' instance(s) detected)"
    update_status(final_status)
    update_button_states() # Ensure buttons reflect stopped state

# --- GUI Update Callbacks (run on main thread) ---
def update_video_label(imgtk):
    """Updates the video label with a new image (called via root.after)."""
    try:
        if video_label and video_label.winfo_exists():
            video_label.imgtk = imgtk
            video_label.configure(image=imgtk)
    except tk.TclError as e:
        if "invalid command name" not in str(e): print(f"TclError updating video label: {e}")
    except Exception as e: print(f"Error in update_video_label: {e}")

def clear_video_label():
    """Clears the video label (called via root.after)."""
    try:
        if video_label and video_label.winfo_exists():
            video_label.configure(image='')
            video_label.imgtk = None
    except tk.TclError as e:
        if "invalid command name" not in str(e): print(f"TclError clearing video label: {e}")
    except Exception as e: print(f"Error in clear_video_label: {e}")

def update_status(message):
    """Updates the status bar label (called via root.after)."""
    try:
        if status_label and status_label.winfo_exists():
            status_label.after(0, lambda: status_label.config(text=f"Status: {message}"))
    except tk.TclError as e:
        if "invalid command name" not in str(e): print(f"TclError updating status label: {e}")
    except Exception as e: print(f"Error in update_status: {e}")

# --- Source Selection ---
def select_source(source_type):
    """Handles selection of video source (file, webcam, CCTV)."""
    global video_source, frame_position, stop_flag, detection_thread

    # Stop existing detection if running
    if detection_thread and detection_thread.is_alive():
        print("Stopping previous detection to change source...")
        update_status("Stopping previous detection...")
        stop_detection() # Signal the thread to stop
        detection_thread.join(timeout=1.5) # Wait for it
        if detection_thread.is_alive():
            print("Warning: Detection thread did not stop quickly before changing source.")
            show_custom_warning("Warning", "Detection is still stopping. Please wait and try again.")
            update_status("Waiting for detection to stop...")
            return
        detection_thread = None
        print("Previous detection stopped.")

    # Reset state
    stop_flag.clear()
    frame_position = 0
    new_source = None

    try:
        if source_type == "file":
            file_path = filedialog.askopenfilename(
                title="Select Video File",
                filetypes=[("All Files", "*.*")],
                parent=root
            )
            if file_path:
                new_source = file_path
                update_status(f"Selected file: {os.path.basename(file_path)}")
            else:
                update_status("Source selection cancelled.")
        elif source_type == "webcam":
            indices_to_try = [0, 1, 2, -1]
            found_webcam = False
            for index in indices_to_try:
                print(f"Testing webcam index: {index}")
                test_cap = cv2.VideoCapture(index)
                if test_cap.isOpened():
                    new_source = index
                    update_status(f"Selected source: PC Camera (Index {index})")
                    test_cap.release()
                    print(f"Using webcam index: {index}")
                    found_webcam = True
                    break
            if not found_webcam:
                show_custom_warning("Webcam Error", "Could not open any default webcams (tried indices 0, 1, 2, -1).\nEnsure it's connected, drivers installed, and not in use.")
                update_status("Webcam not found or busy.")

        elif source_type == "cctv":
            rtsp_url = simpledialog.askstring("CCTV Source", "Enter RTSP URL (e.g., rtsp://user:pass@ip:port/stream):", parent=root)
            if rtsp_url:
                 rtsp_url = rtsp_url.strip()
                 if rtsp_url.lower().startswith("rtsp://"):
                     new_source = rtsp_url
                     update_status("Selected source: CCTV")
                 else:
                     show_custom_warning("Invalid URL", "Please enter a valid RTSP URL (must start with rtsp://).")
                     update_status("Invalid CCTV URL entered.")
            else:
                update_status("CCTV selection cancelled.")
        else:
            print(f"Error: Invalid source type '{source_type}'")
            update_status("Invalid source type selected.")

        # Update global source only if successful
        if new_source is not None:
             video_source = new_source
        # Don't clear existing source on cancellation/failure of webcam/cctv
        elif source_type != "file":
             pass
        elif source_type == "file" and not new_source:
            pass
        elif source_type == "cctv" and not new_source:
            pass

    except Exception as e:
        show_custom_error("Source Selection Error", f"An error occurred:\n{e}")
        video_source = None
        update_status("Error selecting source.")
        import traceback
        traceback.print_exc()

    update_button_states()

# --- Detection Control ---
def start_detection_thread():
    """Starts the detection process in a new thread."""
    global detection_thread, stop_flag

    if not logged_in:
         show_custom_warning("Login Required", "Please log in before starting detection.")
         return
    if video_source is None:
        show_custom_warning("No Source", "Please select a valid video source first.")
        return
    if detection_thread and detection_thread.is_alive():
        show_custom_warning("Already Running", "Detection is already in progress.")
        return

    stop_flag.clear()
    print("Creating and starting detection thread...")
    detection_thread = threading.Thread(target=run_detection, daemon=True, name="DetectionLoop")
    detection_thread.start()
    update_status("Starting detection...")
    update_button_states()

def stop_detection():
    """Signals the detection thread to stop."""
    global stop_flag, detection_thread
    if detection_thread and detection_thread.is_alive():
        if not stop_flag.is_set():
            print("Stop signal sent to detection thread.")
            stop_flag.set()
            update_status("Stopping detection...")
        else:
            print("Stop signal already sent.")
            update_status("Detection is already stopping...")
    else:
        print("No active detection thread to stop.")
        detection_thread = None
        stop_flag.clear()
        update_status("Detection already stopped.")

    update_button_states()

# --- UI State Management ---
def update_button_states():
    """Updates the enabled/disabled state of UI elements based on application state."""
    def _update():
        if not root or not root.winfo_exists(): return

        try:
            is_running = detection_thread and detection_thread.is_alive()
            source_selected = video_source is not None
            login_active = not logged_in

            # Login Screen Elements
            login_state = NORMAL if login_active else DISABLED
            if login_button and login_button.winfo_exists(): login_button.config(state=login_state)
            if register_button and register_button.winfo_exists(): register_button.config(state=login_state)
            if username_entry and username_entry.winfo_exists(): username_entry.config(state=NORMAL if login_active else DISABLED)
            if password_entry and password_entry.winfo_exists(): password_entry.config(state=NORMAL if login_active else DISABLED)
            if github_button and github_button.winfo_exists(): github_button.config(state=login_state)
            if contact_button and contact_button.winfo_exists(): contact_button.config(state=login_state)

            # Main App Elements
            source_button_state = NORMAL if logged_in and not is_running else DISABLED
            if browse_button and browse_button.winfo_exists(): browse_button.config(state=source_button_state)
            if webcam_button and webcam_button.winfo_exists(): webcam_button.config(state=source_button_state)
            if cctv_button and cctv_button.winfo_exists(): cctv_button.config(state=source_button_state)

            start_button_state = NORMAL if logged_in and source_selected and not is_running else DISABLED
            if start_button and start_button.winfo_exists(): start_button.config(state=start_button_state)

            stop_button_state = NORMAL if is_running else DISABLED
            if stop_button and stop_button.winfo_exists(): stop_button.config(state=stop_button_state)

            # Side Nav Menu Button (using global reference)
            if menu_btn and menu_btn.winfo_exists():
                menu_btn.config(state=NORMAL if logged_in else DISABLED)

        except tk.TclError as e:
             if "invalid command name" not in str(e): print(f"TclError in update_button_states: {e}")
        except Exception as e:
             print(f"Error in update_button_states: {e}")
             import traceback
             traceback.print_exc()

    if root and root.winfo_exists(): root.after(0, _update)

# --- GUI Creation ---
root = tb.Window(themename="darkly")
root.title("CivicEye - Helmet Detection System")
root.minsize(850, 700)
root.geometry("1100x800")

# Define fonts
header_font = create_font(size=18, weight="bold")
login_welcome_font = create_font(size=28, weight="bold")
login_desc_font = create_font(size=11)
login_title_font = create_font(size=20, weight="bold")
login_label_font = create_font(size=10)
login_entry_font = create_font(size=11)
login_tag_font = create_font(size=9)
title_font = create_font(size=16, weight="bold")
status_font = create_font(size=10)
menu_button_font = create_font(size=12)
side_nav_font = create_font(size=10)

def on_closing():
    """Handles window close event, ensuring detection stops."""
    print("Window closing event triggered...")
    if detection_thread and detection_thread.is_alive():
        print("Signalling detection thread to stop...")
        stop_flag.set()
        detection_thread.join(timeout=1.0)
        if detection_thread.is_alive():
            print("Warning: Detection thread still alive after stop signal during exit.")
    if root and root.winfo_exists():
        print("Destroying root window.")
        root.destroy()
    print("Application exit process complete.")

def create_login_frame():
    """Creates the main login screen frame and its widgets."""
    global login_frame, username_entry, password_entry, login_button, register_button
    global github_button, contact_button

    login_frame = tb.Frame(root, padding=(50, 40, 50, 40))
    login_frame.rowconfigure(0, weight=0)
    login_frame.rowconfigure(1, weight=1)
    login_frame.rowconfigure(2, weight=0)
    login_frame.columnconfigure(0, weight=1)

    # Header
    header_frame = tb.Frame(login_frame)
    header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 30))
    header_frame.columnconfigure(0, weight=1)
    try:
        logo_path = os.path.join(get_script_directory(), "logo.png")
        if os.path.exists(logo_path):
            img_pil = Image.open(logo_path)
            img_pil_resized = img_pil.resize((200, 50), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img_pil_resized)
            header_label = tb.Label(header_frame, image=img_tk)
            header_label.image = img_tk
            header_label.grid(row=0, column=0)
        else:
            print(f"Warning: logo.png not found. Displaying text.")
            header_label = tb.Label(header_frame, text="CIVICEYE", font=header_font)
            header_label.grid(row=0, column=0)
    except Exception as e:
        print(f"Error loading logo image: {e}")
        header_label = tb.Label(header_frame, text="CIVICEYE (Logo Error)", font=header_font)
        header_label.grid(row=0, column=0)

    # Content Area
    content_frame = tb.Frame(login_frame)
    content_frame.grid(row=1, column=0, sticky="nsew")
    content_frame.columnconfigure(0, weight=1)
    content_frame.columnconfigure(1, weight=1)
    content_frame.rowconfigure(0, weight=1)

    # Left Side
    left_content = tb.Frame(content_frame, padding=(0, 0, 60, 0))
    left_content.grid(row=0, column=0, sticky="nw", pady=(20,0))
    welcome_label = tb.Label(left_content, text="Welcome to Civic Eye", font=login_welcome_font, anchor="w")
    welcome_label.pack(pady=(0, 15), anchor="w")
    desc_text = "Advanced AI detects traffic violations like helmet usage from\nCCTV feeds in real-time. Local processing ensures privacy."
    desc_label = tb.Label(left_content, text=desc_text, font=login_desc_font, anchor="w", justify="left")
    desc_label.pack(pady=(0, 25), anchor="w")
    tags_frame = tb.Frame(left_content)
    tags_frame.pack(anchor="w")
    tag_texts = ["Real-Time Detection", "Local Privacy", "Evidence Logs"]
    for text in tag_texts:
        tag_frame = tb.Frame(tags_frame, bootstyle="secondary", padding=(8, 4))
        tag_frame.pack(side=LEFT, padx=(0, 10))
        tag_label = tb.Label(tag_frame, text=text, font=login_tag_font, bootstyle="inverse-secondary")
        tag_label.pack()

    # Right Side (Login Form)
    right_content = tb.Frame(content_frame, padding=(60, 0, 0, 0))
    right_content.grid(row=0, column=1, sticky="ne", pady=(20,0))
    login_title_frame = tb.Frame(right_content)
    login_title_frame.pack(anchor="w", fill=X, pady=(0, 5))
    login_title = tb.Label(login_title_frame, text="LOGIN", font=login_title_font)
    login_title.pack(anchor="w")
    login_separator = tb.Separator(right_content)
    login_separator.pack(anchor="w", fill=X, pady=(0, 20))
    email_label = tb.Label(right_content, text="Enter Your Email :", font=login_label_font)
    email_label.pack(anchor="w", pady=(0, 2))
    username_entry = tb.Entry(right_content, font=login_entry_font, width=45)
    username_entry.pack(fill=X, pady=(0, 15), ipady=6)
    password_label = tb.Label(right_content, text="Enter Your Password :", font=login_label_font)
    password_label.pack(anchor="w", pady=(0, 2))
    password_entry = tb.Entry(right_content, font=login_entry_font, width=45, show="*")
    password_entry.pack(fill=X, pady=(0, 25), ipady=6)
    button_frame = tb.Frame(right_content)
    button_frame.pack(fill=X, pady=(10, 0))
    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)
    login_button = tb.Button(button_frame, text="LOGIN", bootstyle="primary", command=login, width=15)
    login_button.grid(row=0, column=0, padx=(0, 5), sticky="ew")
    register_button = tb.Button(button_frame, text="REGISTER", bootstyle="secondary", command=register, width=15)
    register_button.grid(row=0, column=1, padx=(5, 0), sticky="ew")
    password_entry.bind('<Return>', lambda event=None: login_button.invoke())
    username_entry.bind('<Return>', lambda event=None: password_entry.focus_set())

    # Footer
    footer_frame = tb.Frame(login_frame)
    footer_frame.grid(row=2, column=0, sticky="sw", pady=(30, 0))
    github_button = tb.Button(footer_frame, text="GitHub - Source code", bootstyle="link", command=lambda: open_url("https://github.com/SHADOW2669/CivicEye"))
    github_button.pack(side=LEFT, padx=(0, 10))
    contact_button = tb.Button(footer_frame, text="Contact Us", bootstyle="link", command=lambda: open_url("https://civiceye.my/contact-us.php"))
    contact_button.pack(side=LEFT)

    return login_frame

def toggle_side_nav():
    """Shows or hides the side navigation panel."""
    global side_nav_frame, side_nav_visible
    if not side_nav_frame or not side_nav_frame.winfo_exists():
        print("Error: Side nav frame missing. Recreating.")
        create_side_nav()
        if not side_nav_frame: return

    if side_nav_visible:
        side_nav_frame.pack_forget()
        side_nav_visible = False
    else:
        style = tb.Style.get_instance()
        nav_bootstyle = "light" if style.theme.type == 'light' else "dark"
        side_nav_frame.config(bootstyle=nav_bootstyle)
        side_nav_frame.pack(side=LEFT, fill=Y, padx=0, pady=0)
        side_nav_frame.tkraise()
        side_nav_visible = True

def create_side_nav():
    """Creates the side navigation frame and its widgets."""
    global side_nav_frame, side_nav_visible

    if side_nav_frame and side_nav_frame.winfo_exists(): side_nav_frame.destroy()

    style = tb.Style.get_instance()
    nav_bootstyle = "light" if style.theme.type == 'light' else "dark"
    inverse_nav_bootstyle = "inverse-" + nav_bootstyle

    side_nav_frame = tb.Frame(root, width=220, bootstyle=nav_bootstyle)
    side_nav_visible = False

    nav_content_frame = tb.Frame(side_nav_frame, padding=15, bootstyle=nav_bootstyle)
    nav_content_frame.pack(expand=True, fill=BOTH)

    settings_label = tb.Label(nav_content_frame, text="Settings", font=title_font, bootstyle=inverse_nav_bootstyle)
    settings_label.pack(pady=(5, 15), anchor="w")
    theme_btn = tb.Button(nav_content_frame, text="Toggle Theme", command=toggle_theme, bootstyle="outline-secondary")
    theme_btn.pack(fill=X, pady=5)

    speed_label = tb.Label(nav_content_frame, text="Detection Speed", font=title_font, bootstyle=inverse_nav_bootstyle)
    speed_label.pack(pady=(20, 15), anchor="w")
    speed_frame = tb.Frame(nav_content_frame, bootstyle=nav_bootstyle)
    speed_frame.pack(fill=X)
    fast_btn = tb.Button(speed_frame, text="Fast (Skip≈15)", command=lambda: set_frame_skip(15), bootstyle="info")
    fast_btn.pack(fill=X, pady=3)
    balanced_btn = tb.Button(speed_frame, text="Balanced (Skip≈30)", command=lambda: set_frame_skip(30), bootstyle="warning")
    balanced_btn.pack(fill=X, pady=3)
    quality_btn = tb.Button(speed_frame, text="Quality (Skip≈60)", command=lambda: set_frame_skip(60), bootstyle="success")
    quality_btn.pack(fill=X, pady=3)

    spacer = tb.Frame(nav_content_frame, height=1, bootstyle=nav_bootstyle)
    spacer.pack(fill=BOTH, expand=True, pady=10)

    logout_btn = tb.Button(nav_content_frame, text="Logout", command=logout, bootstyle="danger")
    logout_btn.pack(fill=X, pady=5)
    exit_btn = tb.Button(nav_content_frame, text="Exit Application", command=on_closing, bootstyle="secondary")
    exit_btn.pack(fill=X, pady=5)

def create_app_frame():
    """Creates the main application frame shown after login."""
    global app_frame, browse_button, webcam_button, cctv_button
    global start_button, stop_button, video_label, status_label
    global menu_btn # Ensure menu_btn is global here

    local_app_frame = tb.Frame(root, padding=(10, 0, 10, 10))

    # Top Bar
    top_bar = tb.Frame(local_app_frame, padding=(0, 5, 0, 10))
    top_bar.pack(fill=X, side=TOP)
    # Assign to global menu_btn here
    menu_btn = tb.Button(top_bar, text="☰", command=toggle_side_nav, bootstyle="secondary", width=3)
    menu_btn.pack(side=LEFT, padx=(0, 10))
    tb.Label(top_bar, text="Helmet Detection Control Panel", font=title_font).pack(side=LEFT, padx=5)

    # Source Selection
    source_frame = tb.Labelframe(local_app_frame, text="Select Video Source", padding=10, bootstyle="dark")
    source_frame.pack(pady=10, padx=0, fill=X)
    source_frame.columnconfigure(0, weight=1)
    source_frame.columnconfigure(1, weight=1)
    source_frame.columnconfigure(2, weight=1)
    browse_button = tb.Button(source_frame, text="📂 Browse File", bootstyle="primary", command=lambda: select_source("file"))
    browse_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    webcam_button = tb.Button(source_frame, text="📸 Use PC Camera", bootstyle="info", command=lambda: select_source("webcam"))
    webcam_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    cctv_button = tb.Button(source_frame, text="🎥 Connect CCTV", bootstyle="secondary", command=lambda: select_source("cctv"))
    cctv_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

    # Video Display
    video_display_frame = tb.Labelframe(local_app_frame, text="Live Feed / Video Preview", padding=5, bootstyle="dark")
    video_display_frame.pack(pady=10, padx=0, fill=BOTH, expand=TRUE)
    video_label = tb.Label(video_display_frame, anchor=CENTER)
    video_label.pack(fill=BOTH, expand=TRUE, padx=2, pady=2)

    # Detection Controls
    control_frame = tb.Labelframe(local_app_frame, text="Detection Controls", padding=10, bootstyle="dark")
    control_frame.pack(fill=X, padx=0, pady=10)
    control_frame.columnconfigure(0, weight=1)
    control_frame.columnconfigure(1, weight=1)
    start_button = tb.Button(control_frame, text="▶ Start Detection", bootstyle="success", command=start_detection_thread, state=DISABLED)
    start_button.grid(row=0, column=0, padx=(0,5), pady=5, sticky="ew")
    stop_button = tb.Button(control_frame, text="■ Stop Detection", bootstyle="danger", command=stop_detection, state=DISABLED)
    stop_button.grid(row=0, column=1, padx=(5,0), pady=5, sticky="ew")

    # Status Bar
    status_frame = tb.Frame(local_app_frame, padding=(0, 5))
    status_frame.pack(fill=X, side=BOTTOM, pady=(5, 0))
    status_label = tb.Label(status_frame, text="Status: Initializing...", anchor=W, font=status_font)
    status_label.pack(fill=X, padx=5)

    return local_app_frame

# --- Application Initialization ---

if load_session():
    app_frame = create_app_frame()
    create_side_nav()
    if app_frame:
        app_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        update_status("Session loaded. Select a source.")
    else:
        logged_in = False
        delete_session()
        login_frame = create_login_frame()
        login_frame.pack(fill=BOTH, expand=TRUE)
        update_status("Error loading application view. Please log in.")
else:
    login_frame = create_login_frame()
    login_frame.pack(fill=BOTH, expand=TRUE)
    app_frame = None
    update_status("Idle. Please log in.")

update_button_states()
root.protocol("WM_DELETE_WINDOW", on_closing)

# --- Main Loop ---
if __name__ == "__main__":
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("KeyboardInterrupt received. Closing application.")
        on_closing()
    except tk.TclError as e:
         if "application has been destroyed" not in str(e) and "invalid command name" not in str(e):
            print(f"Unhandled Tkinter TclError in main execution: {e}")
            import traceback
            traceback.print_exc()
            try: on_closing()
            except: pass
    except Exception as e:
        print(f"An unexpected error occurred in the main execution block: {e}")
        import traceback
        traceback.print_exc()
        try: on_closing()
        except: pass
    finally:
         print("Application has exited.")