import cv2
import math
import cvzone
import os
from ultralytics import YOLO

# Initialize video capture
video_path = "Media/test_vid2.mp4"
cap = cv2.VideoCapture(video_path)

# Load YOLO model with custom weights
model = YOLO("Weights/best.pt")

# Define class names
classNames = ['With Helmet', 'Without Helmet']

# Directory to store detected images
save_dir = "/home/shadow269/VC_CODE/CivicEye/Detects"
os.makedirs(save_dir, exist_ok=True)

violating_bikes = {}  # Dictionary to track detected bikes

frame_count = 0  # Counter to track frames

while True:
    success, img = cap.read()
    if not success:
        break  # Stop if video ends

    results = model(img, stream=True)
    detected_violations = False  # Flag to track violations in the frame

    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get bounding box coordinates
            conf = math.ceil((box.conf[0] * 100)) / 100  # Confidence score
            cls = int(box.cls[0])  # Class ID

            # Draw bounding box and label
            cvzone.cornerRect(img, (x1, y1, x2 - x1, y2 - y1))
            cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

            # Save full-frame image if "Without Helmet" is detected
            if classNames[cls] == "Without Helmet":
                detected_violations = True

    # Save the full image only once per bike with violation
    if detected_violations:
        img_id = f"violation_{frame_count}.jpg"

        if img_id not in violating_bikes:  # Ensure only one image per bike
            filename = os.path.join(save_dir, img_id)
            cv2.imwrite(filename, img)
            violating_bikes[img_id] = True  # Mark bike as saved
            print(f"Saved violation image: {filename}")

    frame_count += 1  # Increment frame counter

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
