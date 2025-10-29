# **CivicEye – Ubuntu (Docker Edition)**

## **Features**

* **Real-Time Helmet Detection:** Detects individuals as *With Helmet* (green bounding box) or *Without Helmet* (red bounding box) using a YOLOv8 model.
* **Multiple Video Sources:** Supports:

  * Local video files (`.mp4`, `.avi`, etc.)
  * Connected webcams
  * RTSP streams (CCTV or IP cameras)
* **Frame Saving (‘Without Helmet’ detections):**

  * **Online Mode:** Saves detection info and frames to the CivicEye cloud (`civiceye.my`) using your credentials.
  * **Offline Mode:** Saves detection frames locally under `Detects/` inside the container or mounted volume.
* **Adjustable Detection Speed:** Choose between ‘Fast’, ‘Balanced’, and ‘Quality’ to manage performance vs. accuracy.

  * `Fast (Skip=15)` → Higher speed, more CPU.
  * `Balanced (Skip=30)` → Default balance.
  * `Quality (Skip=60)` → Fewer frames, lowest CPU.
* **User Authentication:**

  * **Online Mode:** Uses your `civiceye.my` login.
  * **Offline Mode:** Uses fixed local credentials (`admin@civiceye` / `civiceye`).
* **Session Persistence:** Online sessions remain active until logout.
* **Modern GUI:** Built using Tkinter and `ttkbootstrap` (supports Light/Dark themes).
* **Containerized Setup:** Runs fully inside Docker for isolation and easy deployment.

---

## **System Requirements**

| Component      | Requirement                                             |
| -------------- | ------------------------------------------------------- |
| OS             | Ubuntu 22.04+ or other Linux with X11 display           |
| CPU            | Intel i3 or higher                                      |
| RAM            | 4GB minimum (8GB recommended)                           |
| Storage        | ~5GB free space                                         |
| Docker         | Latest version installed (`sudo apt install docker.io`) |
| GPU (optional) | NVIDIA GPU with CUDA if YOLO GPU acceleration is needed |
| Internet       | Required for setup and Online Mode                      |

---

## **Installation (Docker Setup)**

### **1. Clone or Download the Project**

```bash
git clone https://github.com/<your-org>/CivicEye.git
cd CivicEye
```

Ensure the directory contains:

* `Dockerfile`
* `requirements.txt`
* `DATA/` folder with `civiceye.py`

---

### **2. Build the Docker Image**

```bash
sudo docker build -t civiceye .
```
This might take a while , so grab a coffee

---

### **3. Run the Container**

#### **Run With GUI (local display)**

If you are running on a Linux desktop:

```bash
xhost +local:root
sudo docker run -it --rm \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    civiceye
```

---

### **4. (Optional) GPU Support**

If you have an NVIDIA GPU:

* Install the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
* Then run:

```bash
sudo docker run -it --rm \
    --gpus all \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    civiceye
```

---

## **Usage Guide**

### **Login**

1. Launch CivicEye (container starts GUI).
2. Choose:

   * **Online Mode:** Use your `civiceye.my` credentials.
   * **Offline Mode:**

     ```
     Email: admin@civiceye
     Password: civiceye
     ```
3. The app checks for internet connectivity before online login.

---

### **Main Interface**

* **Menu Button (☰):** Opens side navigation.
* **Theme Toggle:** Switch between light (‘litera’) and dark (‘darkly’).
* **Detection Speed:** Choose from Fast, Balanced, Quality.
* **Video Source:**

  * *Browse File*: Select local video file.
  * *Use PC Camera*: Open default webcam.
  * *Connect CCTV*: Enter RTSP URL.
* **Control Buttons:**

  * *Start Detection*: Begin YOLO processing.
  * *Stop Detection*: Halt detection.
* **Video Preview:** Displays bounding boxes:

  * Green = With Helmet
  * Red = Without Helmet
* **Status Bar:** Shows current state messages.

---

### **Detection Outputs**

* **Online Mode:** Saves detection data to the CivicEye server.
* **Offline Mode:** Saves JPEG images under:

  ```
  Detects/detection_YYYYMMDD_HHMMSS_ms_frame_XXX.jpg
  ```

  inside `/app/Detects/` (or your mounted volume).

---

## **Technical Overview**

| Component                | Description                                                       |
| ------------------------ | ----------------------------------------------------------------- |
| **Language**             | Python 3.10+                                                      |
| **Core Libraries**       | Ultralytics YOLO, OpenCV, Tkinter, ttkbootstrap, Pillow, Requests |
| **GUI Framework**        | Tkinter + ttkbootstrap                                            |
| **Containerization**     | Ubuntu 22.04 base, Python 3.10, Docker-managed                    |
| **Optional GPU Support** | CUDA runtime (via `nvidia/cuda` base image)                       |

---

## **Uninstallation**

To remove the Docker image:

```bash
sudo docker rmi civiceye
```

To remove all unused containers and images:

```bash
sudo docker system prune -a
```

---

