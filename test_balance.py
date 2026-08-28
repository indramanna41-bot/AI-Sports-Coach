from backend.vision.pose_analyzer import PoseAnalyzer
from backend.features.balance import extract_balance_features


VIDEO_PATH = (
    "uploads/FREESTYLE 😱🔥 FOOTBALL SKILLS ⚽️⭐️ BEACH FOOTBALL "
    "valerikostovofficial - v7skills (1080p, h264, youtube).mp4"
)


analyzer = PoseAnalyzer()

result = analyzer.analyze_video(
    VIDEO_PATH
)

balance_features = extract_balance_features(
    result["landmarks"]
)


print("\nBALANCE ANALYSIS")
print("================")

print(
    "Average body-center offset:",
    balance_features["average_body_center_offset"]
)

print(
    "Average shoulder tilt:",
    balance_features["average_shoulder_tilt"]
)

print(
    "Average hip tilt:",
    balance_features["average_hip_tilt"]
)

print(
    "Valid balance frames:",
    balance_features["valid_balance_frames"]
)


analyzer.close()