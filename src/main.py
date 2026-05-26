import cv2
import os
import time
from ultralytics import YOLO

from alert import trigger_alert

# 🔥 Best accuracy model
model = YOLO("yolov8x.pt")

# 🎥 Video path
stream_url = "../data/sample.webm"

print("Opening:", stream_url)

if not os.path.exists(stream_url):
    print("❌ File not found:", stream_url)
    exit()

cap = cv2.VideoCapture(stream_url)

print("Stream opened:", cap.isOpened())

if not cap.isOpened():
    print("❌ Failed to open video")
    exit()

# 🚨 previous detection state
prev_state = False

# 🐘 total tracked count
total_elephant_count = 0
previous_frame_count = 0

# ⏱️ demo timer
DEMO_DURATION_SECONDS = 60
start_time = time.time()

while True:

    ret, frame = cap.read()

    if not ret:
        print("🔁 Restarting video...")
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # 🔥 higher resolution for partial elephant detection
    frame = cv2.resize(frame, (1920, 1080))

    results = model(frame)

    elephant_detected = False
    elephant_count = 0

    # 🧠 Detection loop
    for r in results:
        for box in r.boxes:

            cls = int(box.cls[0])
            label = model.names[cls]
            conf = float(box.conf[0])

            # 🔥 lower threshold for partial elephants
            if "elephant" in label.lower() and conf > 0.25:

                elephant_detected = True
                elephant_count += 1

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # 🟩 bounding box
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                # 🏷️ label
                cv2.putText(
                    frame,
                    f"Elephant {conf:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 255, 0),
                    2
                )

    # 🐘 update total count
    if elephant_count > previous_frame_count:
        total_elephant_count += (
            elephant_count - previous_frame_count
        )

    previous_frame_count = elephant_count

    # 📊 current count
    cv2.putText(
        frame,
        f"Current Count: {elephant_count}",
        (50, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 0),
        2
    )

    # 📊 total count
    cv2.putText(
        frame,
        f"Total Count: {total_elephant_count}",
        (50, 150),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2
    )

    # 🚨 alert logic
    if elephant_detected and not prev_state:
        trigger_alert(frame, elephant_count)

    prev_state = elephant_detected

    # 🚨 on-screen alert
    if elephant_detected:
        cv2.putText(
            frame,
            "🚨 ALERT: ELEPHANT!",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )

    # ⏱️ timer
    elapsed_time = int(time.time() - start_time)
    remaining_time = DEMO_DURATION_SECONDS - elapsed_time

    cv2.putText(
        frame,
        f"Demo Ends In: {remaining_time}s",
        (50, 200),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 165, 255),
        2
    )

    # ⏹️ stop demo
    if elapsed_time >= DEMO_DURATION_SECONDS:
        print("✅ Demo completed")
        print(
            f"🐘 Total elephants tracked: "
            f"{total_elephant_count}"
        )
        break

    cv2.imshow("EleAgent", frame)

    # ESC key
    if cv2.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()