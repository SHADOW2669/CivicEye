# **CivicEye: Linux Version 1.1**

## **Key Features**
- **Real-Time Violation Detection**: Detects traffic violations such as "No Helmet" using YOLOv8 from video files.
- **Local Processing**: Runs directly on the user's machine, ensuring privacy and reducing server costs.
- **Automated Image Capture**: Captures images of violations and stores them in a local directory.
- **Media File Input Only**: Users must provide a pre-recorded video file for detection (Version 1.1).

---

## **Installation Guide**
### **System Requirements**
- **OS:** Linux (Version 1.1 is Linux-only)
- **Processor:** Intel i3 or higher
- **RAM:** 4GB (8GB recommended)
- **Storage:** 20GB free disk space
- **Python:** 3.8+

### **Setup Instructions**
1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/your-repo/CivicEye.git](https://github.com/your-repo/CivicEye.git)
    # Replace with your actual repository URL
    ```
2.  **Navigate to the Project Directory:**
    ```bash
    cd CivicEye
    ```
3.  **Run the Setup Script:**
    * This script will set up the Python virtual environment and install dependencies.
    ```bash
    chmod +x setup_civiceye.sh
    ./setup_civiceye.sh
    ```
4.  **Run the Software:**
    * Use the `run.sh` script to start the application.
    ```bash
    chmod +x run.sh
    ./run.sh
    ```

---

## **Software Workflow**
1.  **User Setup**:
    - User provides a pre-recorded video file path when prompted or via configuration.
2.  **Violation Detection**:
    - YOLOv8 processes video frames from the file and detects violations such as "Without Helmet".
    - Bounding boxes and labels are drawn on detected violations.
3.  **Data Storage**:
    - Captured images of violations are stored in the `Detects` folder within the project directory.
    - The software ensures that each violation is saved only once per frame to avoid duplicates.
4.  **Real-Time Monitoring**:
    - A window displays the video feed with detection overlays.
    - Users can typically exit the application by pressing 'q'.

---

## **Technical Overview**
### **Programming Language:**
- **Python 3.8+**: Used for the core application logic, AI processing, and automation.

### **Core Libraries:**
1.  **OpenCV**: Handles video file reading, frame processing, image manipulation (drawing boxes), and saving captured violation images.
2.  **YOLOv8 (Ultralytics)**: Provides the pre-trained object detection model used to identify helmet violations in video frames.
3.  **cvzone**: A utility library often used alongside OpenCV for simplifying tasks like drawing stylized bounding boxes or displaying information on frames.

---

## **Version 1.1 Release Notes**
- **Dedicated Setup Script (`setup_civiceye.sh`)**: Streamlines the installation of dependencies and virtual environment creation.
- **Dedicated Run Script (`run.sh`)**: Provides a simple command to execute the application within its environment.
- **Media File Input Only**: This version focuses exclusively on processing pre-recorded video files. Live camera feed support is not included in V1.1.
- **Refined Detection Workflow**: Improvements made to how violations are tracked and how corresponding images are captured and stored.
- **Local Processing**: Reinforces that all detection and data handling occur on the user's local machine.