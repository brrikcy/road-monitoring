import torch
import cv2
import os
from ultralytics import YOLO
from datetime import datetime, timedelta
import json

VIDEO_PATH = 'A005_L1S1_Centre_Cam_(21570141)_004.AVI'
MODEL_PATH = 'best.pt'
OUTPUT_FOLDER = 'static/detected_frames4'
OUTPUT_JSON = 'detected.json'
CLASS_NAMES = {
    0: "cracks",
    1: "pothole",
    2: "middle street lines and faded edges",
    3: "roadside garbage piles",
    4: "fallen tree"
}
CONFIDENCE_THRESHOLD = 0.4

detections = []
base_lat, base_lon = 37.7749, -122.4194
lat_step = 0.0001
lon_step = 0.0001
detection_id_counter = 1

try:
    model = YOLO(MODEL_PATH)
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    print(f"Could not open video: {VIDEO_PATH}")
    exit()

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
frame_count = 0
saved_frame_count = 0
start_time = datetime.now()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    if frame_count % 2 != 0:
        continue

    current_lat = base_lat + (lat_step * saved_frame_count)
    current_lon = base_lon + (lon_step * saved_frame_count)
    detection_time = start_time + timedelta(seconds=saved_frame_count * 2)
    results = model.predict(source=frame, conf=CONFIDENCE_THRESHOLD, verbose=False)
    result = results[0]
    boxes = result.boxes

    if boxes is not None and len(boxes) > 0:
        annotated_frame = frame.copy()
        for box in boxes:
            conf = float(box.conf)
            if conf > CONFIDENCE_THRESHOLD:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                class_id = int(box.cls)
                class_name = CLASS_NAMES.get(class_id, f'class_{class_id}')
                label = f"{class_name} {conf:.2f}"
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(annotated_frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)
                image_path = f'{OUTPUT_FOLDER}/frame_{frame_count:04d}.jpg'
                detections.append({
                    "id": detection_id_counter,
                    "class": class_name,
                    "datetime": detection_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "image": image_path,
                    "coordinates": {"lat": round(current_lat, 6), "lng": round(current_lon, 6)},
                    "fixed": False
                })
                detection_id_counter += 1
        output_filename = os.path.join(OUTPUT_FOLDER, f'frame_{frame_count:04d}.jpg')
        cv2.imwrite(output_filename, annotated_frame)
        saved_frame_count += 1

cap.release()
with open(OUTPUT_JSON, 'w') as f:
    json.dump({"detections": detections}, f, indent=4)
print(f"Saved {saved_frame_count} frames to {OUTPUT_FOLDER} and metadata to {OUTPUT_JSON}")
