# EleAgent — Real-Time Elephant Detection & Alert System

EleAgent is an AI-powered wildlife monitoring tool that detects elephants in video streams using YOLOv8, draws bounding boxes around detected animals, tracks counts, and fires instant alerts (sound + snapshot) the moment an elephant enters the frame.

---

## Features

- **Real-time detection** — runs YOLOv8x (high-accuracy model) on each video frame
- **Bounding box overlay** — labels every detected elephant with confidence score
- **Live counters** — current frame count and cumulative total displayed on screen
- **Instant alert** — plays a system sound and saves a timestamped JPEG snapshot on first detection per event
- **Demo mode** — auto-stops after 60 seconds for controlled demonstrations
- **ESC to quit** — manual exit at any time

---

## Project Structure

```
EleAgent/
├── data/
│   └── sample.webm          # Sample wildlife video for testing
├── model/
│   └── yolov8n.pt           # Lightweight YOLOv8 nano model (backup)
├── src/
│   ├── main.py              # Entry point — video loop, detection, overlay
│   ├── alert.py             # Alert logic — sound + snapshot on detection
│   ├── detector.py          # (Detection helpers)
│   └── stream.py            # (Stream utilities)
├── utils/
│   └── logger.py            # Logging utilities
└── requirements.txt
```

---

## Requirements

- Python 3.8+
- macOS (alert sound uses `afplay`; swap for another player on Linux/Windows)

Install dependencies:

```bash
pip install -r requirements.txt
```

**requirements.txt** installs:
- `ultralytics` — YOLOv8 framework
- `opencv-python` — video capture and frame rendering
- `yt-dlp` — download video streams from URLs (optional use)

---

## Usage

```bash
cd src
python main.py
```

The script opens `../data/sample.webm` by default. To use a different video or live stream, update `stream_url` in [src/main.py](src/main.py#L12):

```python
stream_url = "../data/sample.webm"   # local file
# or
stream_url = "rtsp://your-camera-feed"  # live RTSP stream
```

Press **ESC** to exit early. After 60 seconds the demo ends automatically and prints the total elephant count.

---

## How It Works

1. **Video capture** — OpenCV opens the video and reads frames in a loop.
2. **Frame resize** — each frame is upscaled to 1920×1080 to improve detection of partially visible elephants.
3. **YOLOv8 inference** — the frame is passed to `yolov8x.pt`; any detection with class name containing `"elephant"` and confidence above **0.25** is registered.
4. **Overlay** — bounding boxes, labels, live count, and a demo countdown are drawn onto the frame.
5. **Alert** — on the rising edge of detection (elephant not present → present), `trigger_alert()` fires a system sound in a background thread and saves a JPEG snapshot named `elephant_<timestamp>.jpg`.

---

## Alert System

Defined in [src/alert.py](src/alert.py):

| Action | Detail |
|---|---|
| Console log | Prints elephant count to stdout |
| Sound | Plays `Submarine.aiff` via `afplay` (macOS) |
| Snapshot | Saves `elephant_<unix_timestamp>.jpg` in the working directory |

---

## Model

| Model | File | Use case |
|---|---|---|
| YOLOv8x | `src/yolov8x.pt` | High-accuracy inference (default) |
| YOLOv8n | `model/yolov8n.pt` | Lightweight / faster inference |

To switch models, change the path in [src/main.py](src/main.py#L9):

```python
model = YOLO("yolov8x.pt")   # swap to "../model/yolov8n.pt" for speed
```

---

## Potential Extensions

- Push alerts to SMS / email via Twilio or SendGrid
- Support RTSP/HLS live camera feeds
- Log detections to a database or CSV for trend analysis
- Add a web dashboard for remote monitoring
