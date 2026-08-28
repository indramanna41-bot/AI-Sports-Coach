from backend.vision.pose_analyzer import PoseAnalyzer
from backend.features.kicking_features import (
    extract_kicking_features
)


VIDEO_PATH = (
    "uploads/FREESTYLE 😱🔥 FOOTBALL SKILLS ⚽️⭐️ BEACH FOOTBALL "
    "valerikostovofficial - v7skills (1080p, h264, youtube).mp4"
)


analyzer = PoseAnalyzer(
    target_fps=5
)

pose_result = analyzer.analyze_video(
    VIDEO_PATH
)

kicking = extract_kicking_features(
    pose_result["landmarks"]
)


print()
print("KICKING POSTURE FEATURES")
print("========================")

for name, value in kicking.items():
    print(
        name,
        ":",
        value
    )


analyzer.close()