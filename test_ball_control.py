import cv2

from backend.vision.pose_analyzer import PoseAnalyzer
from backend.vision.object_detector import ObjectDetector
from backend.features.ball_control_features import (
    extract_ball_control_features
)


VIDEO_PATH = (
    "uploads/FREESTYLE 😱🔥 FOOTBALL SKILLS ⚽️⭐️ BEACH FOOTBALL "
    "valerikostovofficial - v7skills (1080p, h264, youtube).mp4"
)


TARGET_FPS = 5


pose_analyzer = PoseAnalyzer(
    target_fps=TARGET_FPS
)

pose_result = pose_analyzer.analyze_video(
    VIDEO_PATH
)

pose_analyzer.close()


detector = ObjectDetector()

cap = cv2.VideoCapture(
    VIDEO_PATH
)

original_fps = cap.get(
    cv2.CAP_PROP_FPS
)

frame_interval = max(
    1,
    round(
        original_fps
        / TARGET_FPS
    )
)

frame_number = 0

ball_frames = []


while True:
    success, frame = cap.read()

    if not success:
        break

    frame_number += 1

    if (
        frame_number
        % frame_interval
        != 0
    ):
        continue

    detections = detector.detect_sports_ball(
        frame
    )

    ball_frames.append({
        "frame": frame_number,
        "detections": detections
    })


cap.release()


ball_control = extract_ball_control_features(
    pose_result["landmarks"],
    ball_frames
)


print()
print("BALL CONTROL FEATURES")
print("=====================")

for name, value in ball_control.items():
    print(
        name,
        ":",
        value
    )