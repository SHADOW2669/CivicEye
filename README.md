# **CivicEye: Linux Version 1.0**

## **Key Features**
- **Real-Time Violation Detection**: Detects traffic violations such as "No Helmet" using YOLOv8.
- **Local Processing**: Runs directly on the user's machine, ensuring privacy and reducing server costs.
- **Automated Image Capture**: Captures images of violations and stores them in a local directory.
- **Configurable Video Input**: Users can provide a video file path or use a live camera feed.

## **Installation Guide**
- ### **System Requirements**
  - **OS:** Linux (Version 1 is Linux-only)
  - **Processor:** Intel i3 or higher
  - **RAM:** 4GB (8GB recommended)
  - **Storage:** 20GB free disk space

- ### **Setup Instructions**
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/SHADOW2669/CivicEye.git
   ```
2. **Navigate to the Project Directory:**
   ```bash
   cd CivicEye
   ```
3. **Install Dependencies:**
   ```bash
   sudo apt update
   sudo apt install python3 python3-venv
   ```
4. **Set Up a Virtual Environment:**
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate  # Linux/macOS
   ```
5. **Install Required Python Packages:**
   ```bash
   pip install cvzone ultralytics opencv-python
   ```
6. **Run the Detection Software:**
   ```bash
   python3 civiceye.py
   ```

---

## **Software Workflow**
1. **User Setup**:
   - User provides a video file path or opts for a live camera feed.
2. **Violation Detection**:
   - YOLOv8 processes video frames and detects violations such as "Without Helmet".
   - Bounding boxes and labels are drawn on detected violations.
3. **Data Storage**:
   - Captured images of violations are stored in the `Detects` folder.
   - The software ensures that each violation is saved only once per frame.
4. **Real-Time Monitoring**:
   - Video feed is displayed with detection overlays.
   - Users can exit the application by pressing 'q'.

---

## **Technical Overview**
### **Programming Language:**
- **Python 3.8+**: Used for AI-based image processing and automation.

### **Core Libraries:**
1. **OpenCV**: Handles video stream processing, frame capture, and image saving.
2. **YOLOv8 (Ultralytics)**: Performs real-time object detection for helmet violations.
3. **cvzone**: Used for drawing bounding boxes and labels on detected objects.
4. **Math & OS**: Handles confidence score calculations and file operations.

---