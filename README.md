# **[CivicEye](https://sathwik656.github.io/CivicEye-Website/): Traffic Violation Detection Software**

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

## **Software Setup**

**Open a terminal in the project directory and run the following commands:**
### **Method 1: Using Setup Script**
This is the easiest way to install and run the software.

**Open a terminal in the project directory and run:**
This is the easiest way to install and run the software.

1. **Run the setup script:**
   ```bash
   chmod +x setup.sh  # Make it executable (only needed once)
   ./setup.sh         # Run the installation script
   ```

2. **After installation, use the shortcut script to run the software:**
   ```bash
   ./run.sh
   ```

---

### **Method 2: Manual Installation**
If you prefer to manually install the software, follow these steps:

**Open a terminal in the project directory and run:**
If you prefer to manually install the software, follow these steps:

### **1. User Setup**
Run the following commands to install system dependencies:
```bash
sudo apt update
sudo apt install python3
sudo apt install python3-venv
```

### **2. Set Up a Virtual Environment**
Create and activate a virtual environment:
```bash
python3 -m venv myenv
source myenv/bin/activate
```

### **3. Install Required Python Packages**
Install the necessary Python dependencies:
```bash
pip install opencv-python
pip install opencv-python-headless
pip install ultralytics
pip install Pillow
pip install ttkbootstrap
pip install numpy
pip install matplotlib
pip install torch torchvision torchaudio
pip install requests
```

If using GPU acceleration, install the GPU-compatible PyTorch version:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### **4. Run the Software**
Execute the helmet detection program:
```bash
python3 civiceye.py
```

---

## **Violation Detection Process**
- The software streams the CCTV feed locally and processes video frames using YOLOv8.
- Detected violations are logged, and images with bounding boxes are saved.

## **Data Transmission**
- The software automatically sends violation data (timestamp, violation type, image) to a centralized server through a secure API.

## **Centralized Monitoring**
- Users can log in to the web dashboard to view violation records, download reports, or review images.

---

## **Technical Specifications**
### **Development Requirements**
#### **Programming Language**
- **Python 3.8+**: Ensures compatibility with modern frameworks and libraries.

#### **Libraries**
- **OpenCV:** Handles video streaming, frame extraction, and preprocessing for YOLOv8.
- **PyTorch:** Loads the pre-trained YOLOv8 model and runs inference on video frames.
- **Requests:** Sends violation data (images and metadata) to the centralized server.
- **SQLite:** Stores detected violations locally before sending them to the server.

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

## **Website**
- **URL:** [https://CivicEye.in](https://sathwik656.github.io/CivicEye-Website/)
- **Features:**
  - Software Info
  - System info
  - User Registration and Login
  - View detailed violation logs
  - Filter by violation type, date, or client
  - Download images and reports

---

## **Future Enhancements**
1. Enable multi-language support for broader accessibility.
2. Implement live notification features (e.g., email or SMS alerts).
3. Optimize the YOLO model for Indian road conditions.

---

## **Project Team**
- [**Sathwik**](https://github.com/Sathwik656)
- [**Sakshith**](https://github.com/SHADOW2669)
- [**Deekshith**](https://github.com/Deekshith-O2)
- [**Pratyaksh**](https://github.com/pratyaksh585)

---

## **Support**
For issues or feature requests, please open a ticket in the [GitHub Issues](https://github.com/your-repo/CivicEye/issues) section or contact us at **support@CivicEye.com**.