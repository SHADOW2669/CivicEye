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
   - Configure the CCTV feed by entering the RTSP URL in the provided `config.json` file.
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