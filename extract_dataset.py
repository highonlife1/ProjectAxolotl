import os
import cv2
import numpy as np
import pandas as pd

def extract_features(video_path):
    print(f"Extracting features from: {video_path}")
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"❌ Cannot open video file: {video_path}")
        return None

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = 0
    bright_flashes = 0
    motion_changes = []

    ret, prev_frame = cap.read()
    if not ret:
        print(f"❌ Could not read first frame of: {video_path}")
        return None

    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1

        brightness = np.mean(frame)
        if brightness > 220:
            bright_flashes += 1

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(prev_gray, gray)
        motion_score = np.sum(diff)
        motion_changes.append(motion_score)
        prev_gray = gray

    cap.release()

    duration = frame_count / fps if fps else 0
    return {
        "duration": duration,
        "bright_flashes": bright_flashes,
        "avg_motion": np.mean(motion_changes),
        "max_motion": np.max(motion_changes)
    }

def main():
    folder = "clips"
    if not os.path.exists(folder):
        print(f"❌ ERROR: 'clips' folder not found in {os.getcwd()}")
        input("Press Enter to close...")
        return

    files = [f for f in os.listdir(folder) if f.endswith(".mp4")]
    if not files:
        print("⚠️ No .mp4 files found in clips/")
        input("Press Enter to close...")
        return

    data = []
    for f in files:
        path = os.path.join(folder, f)
        features = extract_features(path)
        if features:
            label_guess = f.split("_")[0]
            label = input(f"Label for {f}? (default = {label_guess}): ").strip().lower() or label_guess
            features["label"] = label
            data.append(features)

    if data:
        df = pd.DataFrame(data)
        df.to_csv("features.csv", index=False)
        print("✅ Saved to features.csv")
    else:
        print("❌ No usable data extracted")

    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
