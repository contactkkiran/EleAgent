import os
import time
import threading
import cv2


# 🔊 play sound
def play_sound():

    os.system(
        "afplay /System/Library/Sounds/Submarine.aiff"
    )


# 🚨 alert function
def trigger_alert(frame, elephant_count):

    print(
        f"🚨 ALERT: "
        f"{elephant_count} Elephant(s) detected!"
    )

    # 🔊 sound
    threading.Thread(
        target=play_sound
    ).start()

    # 📸 save image
    filename = f"elephant_{int(time.time())}.jpg"

    cv2.imwrite(filename, frame)

    print(f"📸 Snapshot saved: {filename}")