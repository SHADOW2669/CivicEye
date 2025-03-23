import cv2
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from ultralytics import YOLO  # Object detection model
from PIL import Image, ImageTk  # For displaying video frames in Tkinter
import os
import webbrowser
import ttkbootstrap as tb  # Themed Tkinter for UI styling

# Global Variables
stop_flag = False  # Flag to control video processing loop
video_source = None  # Path to the selected video file
frame_position = 0  # Stores the last processed frame position
logged_in = False  # User login status

# Login Function
def login():
    """Handles user authentication."""
    global logged_in
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    
    if username == "admin" and password == "1234":
        # Hide login frame and show application frame
        login_frame.pack_forget()
        app_frame.pack(fill="both", expand=True)
        logged_in = True
    else:
        messagebox.showwarning("Login Failed", "Invalid Username or Password.")

# Function to open URLs in the default web browser
def open_url(url):
    webbrowser.open_new(url)

# Function to run YOLOv8 detection
def run_detection():
    """Runs the helmet detection using YOLOv8 on the selected video file."""
    global stop_flag, video_source, frame_position
    stop_flag = False  # Ensure the loop runs
    
    if not video_source:
        messagebox.showwarning("Warning", "No video source selected.")
        return

    # Load the YOLO model
    model = YOLO("Weights/best.pt")
    classNames = ['With Helmet', 'Without Helmet']
    
    # Open the video file
    cap = cv2.VideoCapture(video_source)
    
    # Create a directory to save detected frames if it doesn't exist
    save_dir = "Detects"
    os.makedirs(save_dir, exist_ok=True)

    # Set video to the last frame position (if restarted)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_position)
    
    while not stop_flag:
        success, img = cap.read()
        if not success:
            break  # Exit if video ends
        
        frame_position = cap.get(cv2.CAP_PROP_POS_FRAMES)  # Update frame position
        
        # Perform object detection
        results = model(img, stream=True)
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get bounding box coordinates
                conf = round(box.conf[0].item(), 2)  # Get confidence score
                cls = int(box.cls[0])  # Get class ID

                # Draw bounding box and label on the frame
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(img, f'{classNames[cls]} {conf}', (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Save detected frame with bounding box
                save_path = os.path.join(save_dir, f"frame_{int(frame_position)}.jpg")
                cv2.imwrite(save_path, img)
        
        # Convert frame for Tkinter display
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
        video_label.update()
    
    cap.release()  # Release video resource

# Function to start detection in a separate thread
def start_detection(source=None):
    """Starts helmet detection in a separate thread to keep UI responsive."""
    global stop_flag, video_source
    
    if source:
        video_source = source  # Set video source
    
    if not video_source:
        messagebox.showwarning("Warning", "Please select a video file.")
        return
    
    stop_flag = False  # Reset stop flag
    threading.Thread(target=run_detection, daemon=True).start()  # Run detection in a thread

# Function to stop detection
def stop_detection():
    """Stops the detection loop."""
    global stop_flag
    stop_flag = True

# Initialize Tkinter window
root = tb.Window(themename="darkly")  # Uses a dark theme for UI
root.title("Helmet Detection System")
root.geometry("700x500")
root.resizable(True, True)

# Login Frame UI
login_frame = tb.Frame(root)
login_frame.pack(fill="both", expand=True)

tb.Label(login_frame, text="🔒 Secure Login", font=("Arial", 18, "bold"), bootstyle="dark").pack(pady=15)

# Username Entry
username_entry = tb.Entry(login_frame, bootstyle="primary", font=("Arial", 12))
username_entry.pack(pady=5, padx=20, fill="x")

# Password Entry
password_entry = tb.Entry(login_frame, bootstyle="primary", font=("Arial", 12), show="*")
password_entry.pack(pady=5, padx=20, fill="x")

# Login Button
tb.Button(login_frame, text="🚀 LOGIN", bootstyle="success", command=login).pack(pady=15, fill="x", padx=20)

# Forgot Password & Register Buttons
button_frame = tb.Frame(login_frame)
button_frame.pack(pady=5, fill="x", padx=20)
tb.Button(button_frame, text="🔑 Forgot Password", bootstyle="link", command=lambda: open_url("https://sathwik656.github.io/CivicEye-Website/")).pack(side="left", padx=5)
tb.Button(button_frame, text="📝 Register", bootstyle="secondary-outline", command=lambda: open_url("https://sathwik656.github.io/CivicEye-Website/")).pack(side="right", padx=5)

# Social Media Buttons
social_frame = tb.Frame(login_frame)
social_frame.pack(pady=10, fill="x", padx=20)
tb.Button(social_frame, text="🌐 Website", bootstyle="info", command=lambda: open_url("https://sathwik656.github.io/CivicEye-Website/")).pack(side="left", expand=True, padx=5)
tb.Button(social_frame, text="🐙 GitHub", bootstyle="dark", command=lambda: open_url("https://github.com/SHADOW2669/CivicEye-testing")).pack(side="left", expand=True, padx=5)
tb.Button(social_frame, text="✉ Gmail", bootstyle="danger", command=lambda: open_url("mailto:sakshithshetty69@gmail.com")).pack(side="left", expand=True, padx=5)

# Main Application Frame (hidden until login)
app_frame = tb.Frame(root)

tb.Label(app_frame, text="Helmet Detection System", font=("Arial", 16, "bold"), bootstyle="warning").pack(pady=10)

# Function to browse and select video file
def browse_file():
    """Opens a file dialog to select a video file."""
    file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
    if file_path:
        global frame_position
        frame_position = 0  # Reset frame position
        start_detection(file_path)

# File Selection Button
tb.Button(app_frame, text="📂 Browse File", bootstyle="primary", command=browse_file).pack(pady=10)

# Video Display Frame
video_frame = tb.Frame(app_frame, bootstyle="secondary", padding=5)
video_frame.pack(pady=10, fill="both", expand=True)
video_label = tb.Label(video_frame)
video_label.pack()

# Start & Stop Buttons
tb.Button(app_frame, text="▶ Start Detection", bootstyle="success", command=lambda: start_detection(video_source)).pack(pady=10, fill="x", padx=20)
tb.Button(app_frame, text="■ Stop Detection", bootstyle="danger", command=stop_detection).pack(pady=10, fill="x", padx=20)

# Run the Tkinter main loop
root.mainloop()
