# **CivicEye: Traffic Violation Detection Software**

## **Introduction**
CivicEye is an innovative software designed to detect and monitor traffic violations using home-based CCTV cameras. It empowers users to identify common traffic rule violations, such as riding without helmets in real-time. The software integrates seamlessly with user-provided CCTV systems, processes violations locally, and sends critical data and evidence to a centralized database. Users can access detailed violation logs and reports via a dedicated website.

---

## **Objectives**
1. **Traffic Violation Detection:** Leverage AI-powered object detection (YOLOv8) to identify violations like "no helmet," "triple riding," and more.
2. **Automated Data Reporting:** Send violation data (images, timestamps, types) from the client’s system to a centralized database.
3. **Centralized Monitoring:** Allow users to view and manage detected violations via a web dashboard.
4. **Privacy and Efficiency:** Enable local processing on the client’s machine, ensuring data privacy and reducing server costs.
5. **Scalability:** Create a robust, user-friendly software that can be downloaded and run across different devices.

---

## **Key Features**
- **Real-Time Violation Detection:** Automatically detect and record traffic violations using the YOLOv8 object detection model.
- **Local Processing:** Run the detection software locally on the client’s machine, minimizing data transmission.
- **Automated Reporting:** Send violation evidence (photos and metadata) to a centralized database for storage and review.
- **Web Dashboard:** Provide a user-friendly website for viewing, searching, and filtering violations.
- **Customizable Configuration:** Users can easily configure the CCTV feed (RTSP URL) and software settings.

---

## **Software Workflow**
1. **User Setup:**
   - Download the software from the official GitHub repository.
   - Configure the CCTV feed by entering the RTSP URL in the provided `config.json` file. [Ongoing Implementation]
   - Install system dependencies:
     ```bash
     sudo apt update
     sudo apt install python3
     sudo apt install python3-venv
     ```
   - Set up a virtual environment:
     ```bash
     python3 -m venv myenv
     source myenv/bin/activate  # For Linux/macOS
     ```
   - Install required Python packages:
     ```bash
     pip install cvzone
     pip install ultralytics
     ```
   - Run the software:
     ```bash
     python3 helmet_detection_video.py
     ```

2. **Violation Detection:**
   - The software streams the CCTV feed locally and processes video frames using YOLOv3.
   - Detected violations are logged, and images with bounding boxes are saved.

3. **Data Transmission:**
   - The software automatically sends violation data (timestamp, violation type, image) to a centralized server through a secure API.

4. **Centralized Monitoring:**
   - Users can log in to the web dashboard to view violation records, download reports, or review images.

---

## **Technical Specifications** [May be revised as the project advances]
### **Development Requirements**
#### **Programming Language**
- **Python 3.8+**: Python is a versatile programming language with robust libraries for machine learning, computer vision, and web development. Version 3.8+ ensures compatibility with modern frameworks and libraries.

#### **Libraries**
1. **OpenCV**:
   - OpenCV is an open-source library used for real-time computer vision tasks.
   - In this project, it facilitates video streaming from CCTV cameras, frame extraction, and pre-processing for YOLOv3 input.
   - Example Usage:
     - Streaming a CCTV feed via RTSP.
     - Resizing frames for model input.
     - Displaying video feeds with bounding boxes.
     ```python
     import cv2
     cap = cv2.VideoCapture("rtsp://username:password@camera_ip:port")
     ret, frame = cap.read()
     cv2.imshow("Frame", frame)
     ```

2. **PyTorch**:
   - PyTorch is a machine learning framework used to implement and run YOLOv3.
   - It is used to load the pre-trained YOLOv3 model, process frames, and perform object detection.
   - Example Usage:
     - Loading YOLOv3 weights and configurations.
     - Running inference on video frames to detect objects.
     ```python
     import torch
     model = torch.hub.load('ultralytics/yolov5', 'yolov3')
     results = model(frame)
     ```

3. **Requests**:
   - Requests is a Python library for making HTTP requests.
   - It is used to send violation data (images and metadata) to the centralized server via REST APIs.
   - Example Usage:
     - Sending a POST request with violation details and images.
     ```python
     import requests
     data = {"violation_type": "No Helmet", "timestamp": "2025-02-15T10:30:00Z"}
     response = requests.post("https://your-server.com/api/violations", json=data)
     ```

4. **SQLite**:
   - SQLite is a lightweight, file-based database used for local storage of violation data.
   - It allows the software to temporarily store detected violations and metadata locally before sending them to the server.
   - Example Usage:
     - Creating a database to store violation logs.
     - Querying data for local analysis or debugging.
     ```python
     import sqlite3
     conn = sqlite3.connect("violations.db")
     cursor = conn.cursor()
     cursor.execute("CREATE TABLE IF NOT EXISTS Violations (id INTEGER PRIMARY KEY, timestamp TEXT, violation_type TEXT)")
     ```

### **Hardware Requirements**
#### For Clients:
- **Processor:** Intel i3 or higher
- **RAM:** 4GB (8GB recommended)
- **GPU:** Optional (YOLOv3-tiny can run on CPU)
- **Storage:** 20GB free disk space

#### For Centralized Server:
- **Processor:** 16-core CPU (e.g., Intel Xeon)
- **RAM:** 32GB
- **GPU:** NVIDIA Tesla T4 or equivalent
- **Storage:** 1TB SSD for video and metadata storage

---

Here’s your updated **Setup Instructions**:

---

## **Setup Instructions**  
1. Clone the repository:  
   ```bash
   git clone https://github.com/your-repo/CivicEye.git
   ```
2. Navigate to the project directory:  
   ```bash
   cd CivicEye
   ```
3. Install system dependencies:  
   ```bash
   sudo apt update
   sudo apt install python3
   sudo apt install python3-venv
   ```
4. Set up a virtual environment:  
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate  # For Linux/macOS
   ```
5. Install required Python packages:  
   ```bash
   pip install cvzone
   pip install ultralytics
   ```
6. Update the `config.json` file with your CCTV RTSP URL and other preferences.  [Ongoing Implementation]

7. Start the detection software:  
   ```bash
   python3 helmet_detection_video.py
   ```

---

## **Website**
1. **URL:** [https://CivicEye.in](https://sathwik656.github.io/CivicEye-Website/)
2. **Features:**
   - Software Info
   - System info
   - User Registration and Login
   - View detailed violation logs.
   - Filter by violation type, date, or client.
   - Download images and reports.

---

## **Future Enhancements**
1. Enable multi-language support for broader accessibility.
2. Implement live notification features (e.g., email or SMS alerts).
3. Optimize the YOLO model for Indian road conditions.

---

Project by:
* Sathwik
* Sakshith
* Deekshith
* Pratyaksh
---
## **Support**
For issues or feature requests, please open a ticket in the [GitHub Issues](https://github.com/your-repo/CivicEye/issues) section or contact us at support@CivicEye.com.