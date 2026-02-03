# 🚧 Road Infrastructure AI Monitoring System (YOLOv11n)

An end-to-end computer vision and web solution designed to automate road inspections. This project utilizes the cutting-edge YOLOv11n (Nano) model for high-speed object detection and a Flask dashboard for infrastructure management and repair tracking.

---

## 🏗 System Architecture

The project consists of two primary components:

### 🔍 Inference Engine (main.py)

Processes raw video footage, detects road defects using YOLOv11n, and logs data with simulated GPS coordinates.

### 🌐 Management Dashboard (app.py)

A web interface that reads the detection logs, allowing users to visualize, track, and manage repairs.

---

## 🛠 Features

* **YOLOv11n Integration** — Leverages the latest YOLO architecture for optimized real-time detection on edge devices.
* **Automated Geotagging** — Simulates a GPS trail for every detected issue, facilitating map-based planning.
* **Damage Classification** — Specifically trained to identify:

  * Cracks & Potholes
  * Faded street lines and edges
  * Roadside garbage piles
  * Fallen trees
* **Repair Workflow** — Track **Fixed** vs **Pending** status of infrastructure issues via a centralized dashboard.
* **Evidence Logging** — Saves annotated `.jpg` frames for every detection as visual proof.

---

## 📁 Project Structure

```
.
├── main.py                 # The AI Inference engine (YOLOv11n)
├── app.py                  # The Flask Web Application (Dashboard)
├── best.pt                 # YOLOv11n model weights
├── detected.json           # Shared data storage (JSON Database)
├── requirements.txt        # Project dependencies
├── static/
│   └── detected_frames4/   # Visual evidence (annotated frames)
└── templates/              # Dashboard UI components
    ├── dashboard.html
    ├── view.html
    └── map.html
```

---

## 🚀 Getting Started

### 1️⃣ Prerequisites

* Python **3.8 – 3.11**
* Hardware: A GPU is recommended for faster processing, but YOLOv11n is optimized to run efficiently on CPUs as well.

---

### 2️⃣ Installation

Install the required packages using the provided `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Running the Pipeline

#### ▶ Step 1 — Run Detection

Process your video file to populate the database. This script will read the video, detect issues, and save them to `detected.json`.

```bash
python main.py
```

#### ▶ Step 2 — Launch Dashboard

Start the Flask server to view and manage the results:

```bash
python app.py
```

View the application at:

```
http://127.0.0.1:5000
```

---

## 📊 Data Management

The system uses a shared `detected.json` file to communicate between the AI script and the Web app.

### Data Structure Example

```json
{
    "detections": [
        {
            "id": 1,
            "class": "pothole",
            "datetime": "2023-10-27 10:30:00",
            "image": "static/detected_frames4/frame_0010.jpg",
            "coordinates": {"lat": 37.7749, "lng": -122.4194},
            "fixed": false
        }
    ]
}
```

**Note:** If you encounter `TypeError: list indices must be integers...` in `app.py`, it means `detected.json` is missing the `"detections"` wrapper. Ensure `main.py` has run successfully or manually initialize the file with:

```json
{"detections": []}
```

---

## ⚙️ Configuration

You can adjust the following parameters in `main.py`:

* **CONFIDENCE_THRESHOLD** — Currently set to `0.4` to balance precision and recall.
* **frame_count % 2 != 0** — Set to skip every other frame to increase processing speed.
* **base_lat / base_lon** — Change these coordinates to match the starting point of your specific road survey.

---

## 📝 License

This project is intended for road maintenance monitoring and urban planning research.
