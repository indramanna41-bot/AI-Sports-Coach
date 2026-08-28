from backend.vision.pose_analyzer import PoseAnalyzer

from backend.features.running_features import (
    extract_running_features
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

running = extract_running_features(
    pose_result["landmarks"]
)


print()
print("RUNNING FEATURES")
print("================")

for name, value in running.items():
    print(
        name,
        ":",
        value
    )


analyzer.close()