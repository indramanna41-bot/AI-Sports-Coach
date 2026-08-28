from backend.features.angles import calculate_angle
from backend.vision.pose_analyzer import PoseAnalyzer


video_path = "uploads/FREESTYLE 😱🔥 FOOTBALL SKILLS ⚽️⭐️ BEACH FOOTBALL valerikostovofficial - v7skills (1080p, h264, youtube).mp4"


analyzer = PoseAnalyzer()

result = analyzer.analyze_video(video_path)


if not result["landmarks"]:
    print("No landmarks detected.")
    analyzer.close()
    raise SystemExit


first_frame = result["landmarks"][0]

landmarks = first_frame["landmarks"]


left_elbow_angle = calculate_angle(
    landmarks["left_shoulder"],
    landmarks["left_elbow"],
    landmarks["left_wrist"]
)


right_elbow_angle = calculate_angle(
    landmarks["right_shoulder"],
    landmarks["right_elbow"],
    landmarks["right_wrist"]
)


left_knee_angle = calculate_angle(
    landmarks["left_hip"],
    landmarks["left_knee"],
    landmarks["left_ankle"]
)


right_knee_angle = calculate_angle(
    landmarks["right_hip"],
    landmarks["right_knee"],
    landmarks["right_ankle"]
)


print("\nJOINT ANGLE TEST")
print("================")

print(
    "Left elbow angle:",
    left_elbow_angle
)

print(
    "Right elbow angle:",
    right_elbow_angle
)

print(
    "Left knee angle:",
    left_knee_angle
)

print(
    "Right knee angle:",
    right_knee_angle
)


analyzer.close()