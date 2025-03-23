# **CivicEye: Traffic Violation Detection Software**

## **Introduction**
CivicEye is an AI-powered software that enables users to detect and monitor traffic violations using home-based CCTV cameras. By leveraging advanced object detection techniques, it identifies violations such as riding without helmets in real-time and processes them locally on the user's machine.

---

## **Key Features**
- **Real-Time Violation Detection**: Detects traffic violations such as "No Helmet" using YOLOv8.
- **Local Processing**: Runs directly on the user's machine, ensuring privacy and reducing server costs.
- **Automated Image Capture**: Captures images of violations and stores them in a local directory.
- **Configurable Video Input**: Users can provide a video file path or use a live camera feed.

---

## **Installation Guide**
### **System Requirements**
#### **Client Machine:**
- **OS:** Linux (Version 1 is Linux-only)
- **Processor:** Intel i3 or higher
- **RAM:** 4GB (8GB recommended)
- **Storage:** 20GB free disk space

### **Setup Instructions**
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-repo/CivicEye.git
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
   python3 helmet_detection_video.py
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

## **Website**
- **URL:** [CivicEye Website](https://sathwik656.github.io/CivicEye-Website/)
- **Features:**
  - Displays basic information about the software.
  - Provides installation and usage instructions.

---

## **Future Enhancements (Planned for Future Versions)**
1. Implement centralized reporting to a web server.
2. Expand violation detection to include "Triple Riding" and other infractions.
3. Optimize the YOLO model for region-specific traffic conditions.
4. Add integration for live alerts via email/SMS.

---

## **Support & Contributions**
For issues or feature requests, please open a ticket in the [GitHub Issues](https://github.com/shadow2669).


