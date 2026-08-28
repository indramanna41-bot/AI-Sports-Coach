from backend.vision.pose_analyzer import PoseAnalyzer

from backend.features.badminton_features import (
    extract_badminton_features
)

VIDEO_PATH = "uploads/Badminton Trick Shots And Smash #badminton #badmintontrickshot #trickshots - Aapo Puhakka Badminton (1080p, h264, youtube).mp4"


analyzer = PoseAnalyzer()

result = analyzer.analyze_video(
    VIDEO_PATH
)

features = extract_badminton_features(
    result["landmarks"]
)


print("\nBADMINTON FEATURE EXTRACTION")
print("============================")

for key, value in features.items():
    print(key, ":", value)


analyzer.close()