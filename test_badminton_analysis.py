from backend.vision.pose_analyzer import PoseAnalyzer

from backend.features.badminton_features import (
    extract_badminton_features
)

from backend.sports.badminton import (
    analyze_badminton
)


VIDEO_PATH = (
    "uploads/Badminton Trick Shots And Smash #badminton "
    "#badmintontrickshot #trickshots - Aapo Puhakka "
    "Badminton (1080p, h264, youtube).mp4"
)


analyzer = PoseAnalyzer()

pose_result = analyzer.analyze_video(
    VIDEO_PATH
)

features = extract_badminton_features(
    pose_result["landmarks"]
)

analysis = analyze_badminton(
    features
)


print("\nBADMINTON PROTOTYPE ANALYSIS")
print("============================")

print(
    "Analysis mode:",
    analysis["analysis_mode"]
)

print(
    "Overall score:",
    analysis["overall_score"]
)

print("\nCOMPONENT SCORES")
print("----------------")

for name, score in analysis["components"].items():
    print(
        name,
        ":",
        score
    )


print("\nSTRENGTHS")
print("---------")

for item in analysis["strengths"]:
    print(
        "-",
        item
    )


print("\nWEAKNESSES")
print("----------")

for item in analysis["weaknesses"]:
    print(
        "-",
        item
    )


print("\nRECOMMENDATIONS")
print("---------------")

for item in analysis["recommendations"]:
    print(
        "-",
        item
    )


print("\nWARNING")
print("-------")

print(
    analysis["warning"]
)


analyzer.close()