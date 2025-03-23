import cv2  # OpenCV for image processing
import math  # Math module for calculations
import cvzone  # Cvzone for easy OpenCV functionalities
import os  # OS module for file operations
from ultralytics import YOLO  # YOLO model for object detection

# Ask user for media input
media_input = input("Enter video file path or press Enter to use the default camera: ").strip()
if media_input == "":
    cap = cv2.VideoCapture(0)  # Use default camera
else:
    cap = cv2.VideoCapture(media_input)  # Use provided video file

# Load YOLO model with custom weights
model = YOLO("Weights/best.pt")  # Load trained YOLO model

# Define class names
classNames = ['With Helmet', 'Without Helmet']  # Labels for detected objects

# Directory to store detected images
save_dir = "Detects"
os.makedirs(save_dir, exist_ok=True)  # Create directory if it doesn't exist

violating_bikes = {}  # Dictionary to track detected bikes with violations
frame_count = 0  # Counter to track frames processed

while True:
    success, img = cap.read()  # Read a frame from the video or camera
    if not success:
        break  # Stop processing if video ends or camera fails

    results = model(img, stream=True)  # Perform object detection on the frame
    detected_violations = False  # Flag to track violations in the frame

    for r in results:
        boxes = r.boxes  # Extract bounding boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get bounding box coordinates
            conf = math.ceil((box.conf[0] * 100)) / 100  # Confidence score rounded to two decimal places
            cls = int(box.cls[0])  # Class ID of detected object

            # Draw bounding box and label on the image
            cvzone.cornerRect(img, (x1, y1, x2 - x1, y2 - y1))  # Draw rectangle
            cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

            # Check if detected object is "Without Helmet"
            if classNames[cls] == "Without Helmet":
                detected_violations = True  # Set flag to True if violation detected

    # Save the full image only once per detected violation
    if detected_violations:
        img_id = f"violation_{frame_count}.jpg"
        if img_id not in violating_bikes:  # Ensure image is saved only once per violation
            filename = os.path.join(save_dir, img_id)
            cv2.imwrite(filename, img)  # Save image of violation
            violating_bikes[img_id] = True  # Mark this frame as saved
            print(f"Saved violation image: {filename}")

    frame_count += 1  # Increment frame counter

    cv2.imshow("Image", img)  # Display the frame
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit if 'q' key is pressed
        break

cap.release()  # Release video capture resource
cv2.destroyAllWindows()  # Close all OpenCV windows
