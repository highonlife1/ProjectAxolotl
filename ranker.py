import cv2
import numpy as np
import joblib
import os

# Load the trained model
model = joblib.load("pvp_rank_model.pkl")

def extract_features(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"❌ Could not open {video_path}")
        return None

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = 0
    bright_flashes = 0
    motion_changes = []

    ret, prev_frame = cap.read()
    if not ret:
        print(f"❌ Could not read first frame.")
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
    avg_motion = np.mean(motion_changes)
    max_motion = np.max(motion_changes)

    return [duration, bright_flashes, avg_motion, max_motion]

def calculate_score(video_path):
    features = extract_features(video_path)
    if features:
        return model.predict([features])[0]  # returns rank like 'lt4', 'ht2', etc.
    return "unranked"

def get_rank(score):
    return score  # already a label like 'lt3', 'ht1'
