# **[CivicEye] (https://civiceye.my/): Traffic Violation Detection Software (Windows)**

## **Introduction**
CivicEye is an AI-powered software designed to detect and monitor traffic violations using CCTV cameras. Utilizing YOLOv8 for object detection, it identifies helmet violations in real time and processes them locally on the user's machine.

---

## **Key Features**
- **Real-Time Violation Detection**: Detects traffic violations like "No Helmet" using YOLOv8.
- **Local Processing**: Runs directly on the user's machine, ensuring privacy and eliminating cloud dependencies.
- **Automated Image Capture**: Captures images of detected violations and stores them locally.
- **Flexible Video Input**: Supports both pre-recorded videos and real-time webcam feeds.
- **Secure Login System**: Users must authenticate before accessing detection features.
- **Graphical User Interface (GUI)**: Simplified and user-friendly interface for easy interaction.

---

## **Installation Guide**
### **System Requirements**
#### **Client Machine:**
- **OS:** Windows 10 or later
- **Processor:** Intel i3 or higher
- **RAM:** 4GB (8GB recommended)
- **Storage:** 20GB free disk space

### **Setup Instructions**
1. **Download the Latest Release:**
   - Get the Windows installer from the [CivicEye Releases](https://github.com/SHADOW2669/CivicEye/releases).
2. **Run the Setup Script:**
   - Double-click `install.bat` to install dependencies and set up the virtual environment.
3. **Launch the Software:**
   - Use `CivicEye.bat` to start the detection software.

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
   - Bounding boxes and labels are displayed on detected violations.
4. **Data Storage**:
   - Captured images of violations are stored in the `Detects` folder.
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

## **Version 2.0 Release Notes**
- **Added Windows Support**: Fully functional Windows version with `.bat` setup and execution scripts.
- **Graphical User Interface (GUI)**: Improved user experience with a more intuitive interface.
- **Refined Detection System**: Enhanced violation tracking and image storage.
- **Secure Login System**: Mandatory authentication for access control.
- **Local Processing**: Ensures all detection tasks remain on the user's device.

---

## **Future Enhancements (Planned for Future Versions)**
- Add an executable (.exe) file for easier installation on Windows.
- Improve the graphical user interface (GUI) for a better user experience.*
1. Implement centralized reporting to a web server.
2. Expand violation detection to include "Triple Riding" and other infractions.
3. Optimize the YOLO model for region-specific traffic conditions.
4. Add integration for live alerts via email/SMS.
5. Improve UI with additional user-friendly features.

---

## **Support & Contributions**
For issues or feature requests, please contact [SHADOW](https://github.com/SHADOW2669).

