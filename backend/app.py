from flask import Flask, jsonify, render_template
from datetime import datetime
import json
import os
import cv2
from ultralytics import YOLO

# Set up Flask app
app = Flask(__name__, static_folder="../frontend", template_folder="../frontend")

# Base directories
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # "C:\Users\mazin\Downloads\metropredict\backend"
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))  # "C:\Users\mazin\Downloads\metropredict"

# Define paths
DATA_DIR = os.path.join(ROOT_DIR, "data")
MODEL_PATH = os.path.join(BASE_DIR, "models", "yolov8n.pt")
STATIONS_FILE = os.path.join(DATA_DIR, "metro_stations.json")
DATA_FILE = os.path.join(DATA_DIR, "crowd_data.json")
VIDEO_DIR = os.path.join(DATA_DIR, "videos")

# Load YOLO model
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Error: Model file not found at {MODEL_PATH}")
model = YOLO(MODEL_PATH)

def ensure_data_files_exist():
    """Ensure required data files exist before running the app."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(VIDEO_DIR, exist_ok=True)

    # Initialize station data if missing
    if not os.path.exists(STATIONS_FILE):
        stations = [
            {"id": "aluva", "name": "Aluva"},
            {"id": "edappally", "name": "Edappally"},
            {"id": "mg_road", "name": "MG Road"},
            {"id": "kalamassery", "name": "Kalamassery"},
            {"id": "lissie", "name": "Lissie"}
        ]
        with open(STATIONS_FILE, 'w') as f:
            json.dump(stations, f, indent=4)

    # Initialize crowd data if missing
    if not os.path.exists(DATA_FILE):
        crowd_data = [
            {"station": station["name"], "crowd_level": "low", "count": 0, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            for station in get_stations()
        ]
        with open(DATA_FILE, 'w') as f:
            json.dump(crowd_data, f, indent=4)

def get_stations():
    """Load station data from JSON file."""
    with open(STATIONS_FILE, 'r') as f:
        return json.load(f)

def get_crowd_data():
    """Load current crowd data from JSON file."""
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_crowd_data(data):
    """Save crowd data to JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def process_video_frame(video_path):
    """Process a video frame to detect people and determine crowd level."""
    if not os.path.exists(video_path):
        print(f"Warning: Video file {video_path} not found.")
        return {"count": 0, "crowd_level": "low"}

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Unable to open video {video_path}")
        return {"count": 0, "crowd_level": "low"}

    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        print(f"Error: Unable to read frames from {video_path}")
        return {"count": 0, "crowd_level": "low"}

    results = model(frame)

    # Count people (Class ID 0 in COCO dataset is "person")
    person_count = sum(1 for box in results[0].boxes.data.tolist() if int(box[5]) == 0)

    # Classify crowd level
    if person_count <= 3:
        crowd_level = "low"
    elif person_count <= 7:
        crowd_level = "medium"
    else:
        crowd_level = "high"

    return {"count": person_count, "crowd_level": crowd_level}

def estimate_wait_time(crowd_level):
    """Estimate wait time based on crowd level."""
    return {
        "low": "2-5 minutes",
        "medium": "5-10 minutes",
        "high": "10-15 minutes"
    }.get(crowd_level, "Unknown")

def update_crowd_data():
    """Update crowd data by processing video feeds."""
    stations = get_stations()
    crowd_data = []

    for station in stations:
        video_path = os.path.join(VIDEO_DIR, f"{station['id']}.mp4")
        result = process_video_frame(video_path)

        crowd_data.append({
            "station": station["name"],
            "crowd_level": result["crowd_level"],
            "count": result["count"],
            "wait_time": estimate_wait_time(result["crowd_level"]),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    save_crowd_data(crowd_data)
    return crowd_data

# Routes
@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')

@app.route('/api/stations')
def api_stations():
    """API endpoint to get all station information."""
    return jsonify(get_stations())

@app.route('/api/crowd-levels')
def api_crowd_levels():
    """API endpoint to get current crowd levels."""
    crowd_data = update_crowd_data()
    return jsonify(crowd_data)

# Initialize data files on startup
ensure_data_files_exist()

if __name__ == "__main__":
    app.run(debug=True)
