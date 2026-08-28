import cv2

from backend.vision.object_detector import ObjectDetector


VIDEO_PATH = "uploads/FREESTYLE 😱🔥 FOOTBALL SKILLS ⚽️⭐️ BEACH FOOTBALL valerikostovofficial - v7skills (1080p, h264, youtube).mp4"


detector = ObjectDetector()

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    raise ValueError("Could not open football video")

frame_number = 0
tested_frames = 0
detected_frames = 0

# Test approximately every 15th frame.
while True:
    success, frame = cap.read()

    if not success:
        break

    frame_number += 1

    if frame_number % 15 != 0:
        continue

    tested_frames += 1

    detections = detector.detect_sports_ball(frame)

    if detections:
        detected_frames += 1

        print(
            f"Frame {frame_number}: "
            f"{len(detections)} ball detection(s)"
        )

        for detection in detections:
            print(detection)


cap.release()

print()
print("BALL DETECTION TEST")
print("===================")
print("Frames tested:", tested_frames)
print("Frames with ball:", detected_frames)

if tested_frames > 0:
    detection_rate = detected_frames / tested_frames
else:
    detection_rate = 0

print(
    "Ball detection rate:",
    round(detection_rate, 3)
)