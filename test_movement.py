from backend.vision.pose_analyzer import PoseAnalyzer
from backend.features.movement import extract_movement_features


VIDEO_PATH = (
    "uploads/Badminton Trick Shots And Smash #badminton "
    "#badmintontrickshot #trickshots - Aapo Puhakka "
    "Badminton (1080p, h264, youtube).mp4"
)


analyzer = PoseAnalyzer()

result = analyzer.analyze_video(
    VIDEO_PATH
)

movement = extract_movement_features(
    result["landmarks"]
)


print("\nBADMINTON MOVEMENT ANALYSIS")
print("===========================")

print(
    "Movement distance:",
    movement["movement_distance"]
)

print(
    "Average movement speed:",
    movement["average_movement_speed"]
)

print(
    "Maximum movement speed:",
    movement["maximum_movement_speed"]
)

print(
    "Speed variability:",
    movement["movement_speed_variability"]
)

print(
    "Movement consistency:",
    movement["movement_consistency"]
)

print(
    "Valid movement frames:",
    movement["valid_movement_frames"]
)


analyzer.close()