import cv2
import math
import cvzone
import os
from ultralytics import YOLO

media_input = input("Enter video file path or press Enter to use the default camera: ").strip()
if media_input == "":
    cap = cv2.VideoCapture(0)
else:
    cap = cv2.VideoCapture(media_input)

model = YOLO("Weights/best.pt")

classNames = ['With Helmet', 'Without Helmet']

save_dir = "Detects"
os.makedirs(save_dir, exist_ok=True)

violating_bikes = {}
frame_count = 0

while True:
    success, img = cap.read()
    if not success:
        break

    results = model(img, stream=True)
    detected_violations = False

    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = math.ceil((box.conf[0] * 100)) / 100
            cls = int(box.cls[0])

            cvzone.cornerRect(img, (x1, y1, x2 - x1, y2 - y1))
            cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

            if classNames[cls] == "Without Helmet":
                detected_violations = True

    if detected_violations:
        img_id = f"violation_{frame_count}.jpg"
        if img_id not in violating_bikes:
            filename = os.path.join(save_dir, img_id)
            cv2.imwrite(filename, img)
            violating_bikes[img_id] = True
            print(f"Saved violation image: {filename}")

    frame_count += 1

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
