# 🚇 MetroPredict

**Real-time Metro Station Crowd Monitoring & Prediction using Computer Vision**

MetroPredict is a Flask-based web application that uses YOLOv8 object detection to analyze live video feeds from metro stations, count passengers in real time, and predict crowd levels and wait times — helping commuters make smarter travel decisions.

---

## ✨ Features

- **Real-time crowd detection** via YOLOv8 (person detection on live/recorded video feeds)
- **Crowd level classification** — Low, Medium, or High — per station
- **Estimated wait time** based on crowd density
- **Auto-refreshing dashboard** every 30 seconds
- **REST API** for stations and crowd-level data
- **Responsive frontend** built with vanilla HTML/CSS/JS

---

## 🖥️ Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Backend    | Python, Flask                     |
| CV / ML    | OpenCV, Ultralytics YOLOv8        |
| Frontend   | HTML5, CSS3, Vanilla JavaScript   |
| Data Store | JSON flat files                   |

---

## 📁 Project Structure

```
metropredict/
├── backend/
│   ├── app.py              # Flask app, API routes, YOLO inference
│   └── models/
│       └── yolov8n.pt      # YOLOv8 nano model weights
├── data/
│   ├── metro_stations.json # Station definitions
│   ├── crowd_data.json     # Latest crowd data (auto-generated)
│   └── videos/             # Per-station video feeds (e.g. aluva.mp4)
├── frontend/
│   └── index.html          # Dashboard UI
└── main.py                 # Entry point
```

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.8+
- pip

### 1. Clone the repository

```bash
git clone https://github.com/your-username/metropredict.git
cd metropredict
```

### 2. Install dependencies

```bash
pip install flask opencv-python ultralytics
```

### 3. Add the YOLOv8 model

Download the YOLOv8 nano weights and place them at:

```
backend/models/yolov8n.pt
```

You can download it from the [Ultralytics releases](https://github.com/ultralytics/assets/releases) or let Ultralytics auto-download on first run by modifying the model path.

### 4. Add video feeds

Place `.mp4` video files for each station inside `data/videos/`. File names must match the station `id` values defined in `metro_stations.json`:

```
data/videos/aluva.mp4
data/videos/edappally.mp4
data/videos/mg_road.mp4
data/videos/kalamassery.mp4
data/videos/lissie.mp4
```

> If a video file is missing, that station will default to a crowd count of 0 and level "low".

### 5. Run the application

```bash
python main.py
```

The app will start on `http://0.0.0.0:5000`.

---

## 🔌 API Endpoints

### `GET /api/stations`
Returns all configured metro stations.

```json
[
  { "id": "aluva", "name": "Aluva" },
  { "id": "edappally", "name": "Edappally" },
  ...
]
```

### `GET /api/crowd-levels`
Processes the latest video frame for each station and returns crowd data.

```json
[
  {
    "station": "Aluva",
    "crowd_level": "medium",
    "count": 5,
    "wait_time": "5-10 minutes",
    "timestamp": "2025-03-23 14:32:10"
  },
  ...
]
```

---

## 📊 Crowd Level Logic

| People Detected | Crowd Level | Estimated Wait |
|-----------------|-------------|----------------|
| 0 – 3           | 🟢 Low      | 2–5 minutes    |
| 4 – 7           | 🟡 Medium   | 5–10 minutes   |
| 8+              | 🔴 High     | 10–15 minutes  |

---

## 🚉 Default Stations

The following Kochi Metro stations are pre-configured:

- Aluva
- Edappally
- MG Road
- Kalamassery
- Lissie

To add or modify stations, edit `data/metro_stations.json` and add a corresponding video file to `data/videos/`.

---

## 🙋 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

