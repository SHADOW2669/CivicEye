import cv2
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from ultralytics import YOLO # type: ignore
from PIL import Image, ImageTk
import os
import webbrowser
import ttkbootstrap as tb  # type: ignore

# Global Variables
stop_flag = False
video_source = None
frame_position = 0
logged_in = False

def login():
    global logged_in
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    
    if username == "admin" and password == "1234":
        login_frame.pack_forget()
        app_frame.pack(fill="both", expand=True)
        logged_in = True
    else:
        messagebox.showwarning("Login Failed", "Invalid Username or Password.")

# Function to open URLs
def open_url(url):
    webbrowser.open_new(url)

def run_detection():
    global stop_flag, video_source, frame_position
    stop_flag = False
    
    if not video_source:
        messagebox.showwarning("Warning", "No video source selected.")
        return
    
    model = YOLO("Weights/best.pt")
    classNames = ['With Helmet', 'Without Helmet']
    cap = cv2.VideoCapture(video_source)
    save_dir = "Detects"
    os.makedirs(save_dir, exist_ok=True)
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_position)
    
    while not stop_flag:
        success, img = cap.read()
        if not success:
            break
        
        frame_position = cap.get(cv2.CAP_PROP_POS_FRAMES)
        
        results = model(img, stream=True)
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = round(box.conf[0].item(), 2)
                cls = int(box.cls[0])
                
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(img, f'{classNames[cls]} {conf}', (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                save_path = os.path.join(save_dir, f"frame_{int(frame_position)}.jpg")
                cv2.imwrite(save_path, img)
        
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
        video_label.update()
    
    cap.release()

def start_detection(source=None):
    global stop_flag, video_source
    
    if source:
        video_source = source
    
    if not video_source:
        messagebox.showwarning("Warning", "Please select a video file.")
        return
    
    stop_flag = False
    threading.Thread(target=run_detection, daemon=True).start()

def stop_detection():
    global stop_flag
    stop_flag = True

root = tb.Window(themename="darkly")  
root.title("Helmet Detection System")
root.geometry("700x500")
root.resizable(True, True)

login_frame = tb.Frame(root)
login_frame.pack(fill="both", expand=True)

tb.Label(login_frame, text="🔒 Secure Login", font=("Arial", 18, "bold"), bootstyle="dark").pack(pady=15)

username_entry = tb.Entry(login_frame, bootstyle="primary", font=("Arial", 12))
username_entry.pack(pady=5, padx=20, fill="x")
username_entry.insert(0, "")

password_entry = tb.Entry(login_frame, bootstyle="primary", font=("Arial", 12), show="*")
password_entry.pack(pady=5, padx=20, fill="x")
password_entry.insert(0, "")

tb.Button(login_frame, text="🚀 LOGIN", bootstyle="success", command=login).pack(pady=15, fill="x", padx=20)

button_frame = tb.Frame(login_frame)
button_frame.pack(pady=5, fill="x", padx=20)

tb.Button(button_frame, text="🔑 Forgot Password", bootstyle="link", command=lambda: open_url("https://sathwik656.github.io/CivicEye-Website/")).pack(side="left", padx=5)
tb.Button(button_frame, text="📝 Register", bootstyle="secondary-outline", command=lambda: open_url("https://sathwik656.github.io/CivicEye-Website/")).pack(side="right", padx=5)

social_frame = tb.Frame(login_frame)
social_frame.pack(pady=10, fill="x", padx=20)

tb.Button(social_frame, text="🌐 Website", bootstyle="info", command=lambda: open_url("https://sathwik656.github.io/CivicEye-Website/")).pack(side="left", expand=True, padx=5)
tb.Button(social_frame, text="🐙 GitHub", bootstyle="dark", command=lambda: open_url("https://github.com/SHADOW2669/CivicEye-testing")).pack(side="left", expand=True, padx=5)
tb.Button(social_frame, text="✉ Gmail", bootstyle="danger", command=lambda: open_url("mailto:sakshithshetty69@gmail.com")).pack(side="left", expand=True, padx=5)

app_frame = tb.Frame(root)

tb.Label(app_frame, text="Helmet Detection System", font=("Arial", 16, "bold"), bootstyle="warning").pack(pady=10)

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
    if file_path:
        global frame_position
        frame_position = 0
        start_detection(file_path)

tb.Button(app_frame, text="📂 Browse File", bootstyle="primary", command=browse_file).pack(pady=10)

video_frame = tb.Frame(app_frame, bootstyle="secondary", padding=5)
video_frame.pack(pady=10, fill="both", expand=True)
video_label = tb.Label(video_frame)
video_label.pack()

tb.Button(app_frame, text="▶ Start Detection", bootstyle="success", command=lambda: start_detection(video_source)).pack(pady=10, fill="x", padx=20)
tb.Button(app_frame, text="■ Stop Detection", bootstyle="danger", command=stop_detection).pack(pady=10, fill="x", padx=20)

root.mainloop()
