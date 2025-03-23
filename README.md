# **CivicEye: Traffic Violation Detection Software**

## **Introduction**
CivicEye is an AI-powered software that enables users to detect and monitor traffic violations using home-based CCTV cameras. By leveraging advanced object detection techniques, it identifies violations such as riding without helmets in real-time and processes them locally on the user's machine.

---

## **Key Features**
- **Real-Time Violation Detection**: Detects traffic violations such as "No Helmet" using YOLOv8.
- **Local Processing**: Runs directly on the user's machine, ensuring privacy and reducing server costs.
- **Automated Image Capture**: Captures images of violations and stores them in a local directory.
- **Flexible Video Input**: Users can either provide a pre-recorded video file or use the default webcam for real-time detection.
- **Secure Login System**: Requires authentication before accessing the detection system.

---

## **Installation Guide**
### **System Requirements**
#### **Client Machine:**
- **OS:** Linux (debian Linux-only)
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
3. **Run the Setup Script:**
   ```bash
   chmod +x setup_civiceye.sh
   ./setup_civiceye.sh
   ```
4. **Run the Software:**
   ```bash
   chmod +x run.sh
   ./run.sh
   ```

---

## **Software Workflow**
1. **User Login**:
   - Default credentials:
     - **Username:** admin
     - **Password:** 1234
   - Users must authenticate before accessing detection features.
2. **User Setup**:
   - Users can provide a pre-recorded video file or press Enter to use the default webcam.
3. **Violation Detection**:
   - YOLOv8 processes video frames and detects violations such as "Without Helmet".
   - Bounding boxes and labels are drawn on detected violations.
4. **Data Storage**:
   - Captured images of violations are stored in the `Detects` folder.
   - The software ensures that each violation is saved only once per frame.
5. **Real-Time Monitoring**:
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
4. **Pillow**: Converts images for display in the GUI.
5. **ttkbootstrap**: Provides enhanced UI styling and elements.

---

## **Website**
- **URL:** [CivicEye Website](https://civiceye.my/)
- **Features:**
  - Displays basic information about the software.
  - Provides installation and usage instructions.

---

## **Version 1.2 Release Notes**
- **Updated Setup Script**: Now supports multiple Linux distributions (Ubuntu, Debian, Arch, Fedora).
- **Refined Run Script**: A dedicated `run.sh` file for easy execution.
- **Improved Detection Workflow**: Enhancements in violation tracking and image storage.
- **Flexible Video Input**: Users can either provide a video file or use the default webcam.
- **Secure Login System**: Users must authenticate before accessing detection features.
- **Local Processing**: All detection and processing occur on the client machine.
- **Basic Website**: Provides installation and usage information.

---

## **Future Enhancements (Planned for Future Versions)**
1. Implement centralized reporting to a web server.
2. Expand violation detection to include "Triple Riding" and other infractions.
3. Optimize the YOLO model for region-specific traffic conditions.
4. Add integration for live alerts via email/SMS.
5. Improve UI with additional user-friendly features.

---

## **Support & Contributions**
For issues or feature requests, please contact [SHADOW](https://github.com/SHADOW2669).

