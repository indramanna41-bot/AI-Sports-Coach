from backend.vision.pose_analyzer import PoseAnalyzer
from backend.features.angles import calculate_angle, summarize_angles


VIDEO_PATH = (
    "uploads/FREESTYLE 😱🔥 FOOTBALL SKILLS ⚽️⭐️ BEACH FOOTBALL "
    "valerikostovofficial - v7skills (1080p, h264, youtube).mp4"
)

MIN_VISIBILITY = 0.70


def landmarks_are_visible(*landmarks):
    """
    Return True only when all supplied landmarks
    have sufficient MediaPipe visibility.
    """
    return all(
        landmark["visibility"] >= MIN_VISIBILITY
        for landmark in landmarks
    )


analyzer = PoseAnalyzer()

result = analyzer.analyze_video(VIDEO_PATH)

left_elbow_angles = []
right_elbow_angles = []
left_knee_angles = []
right_knee_angles = []

skipped_measurements = 0


for frame_data in result["landmarks"]:

    landmarks = frame_data["landmarks"]

    # LEFT ELBOW
    if landmarks_are_visible(
        landmarks["left_shoulder"],
        landmarks["left_elbow"],
        landmarks["left_wrist"]
    ):
        left_elbow_angles.append(
            calculate_angle(
                landmarks["left_shoulder"],
                landmarks["left_elbow"],
                landmarks["left_wrist"]
            )
        )
    else:
        skipped_measurements += 1

    # RIGHT ELBOW
    if landmarks_are_visible(
        landmarks["right_shoulder"],
        landmarks["right_elbow"],
        landmarks["right_wrist"]
    ):
        right_elbow_angles.append(
            calculate_angle(
                landmarks["right_shoulder"],
                landmarks["right_elbow"],
                landmarks["right_wrist"]
            )
        )
    else:
        skipped_measurements += 1

    # LEFT KNEE
    if landmarks_are_visible(
        landmarks["left_hip"],
        landmarks["left_knee"],
        landmarks["left_ankle"]
    ):
        left_knee_angles.append(
            calculate_angle(
                landmarks["left_hip"],
                landmarks["left_knee"],
                landmarks["left_ankle"]
            )
        )
    else:
        skipped_measurements += 1

    # RIGHT KNEE
    if landmarks_are_visible(
        landmarks["right_hip"],
        landmarks["right_knee"],
        landmarks["right_ankle"]
    ):
        right_knee_angles.append(
            calculate_angle(
                landmarks["right_hip"],
                landmarks["right_knee"],
                landmarks["right_ankle"]
            )
        )
    else:
        skipped_measurements += 1


print("\nFILTERED ANGLE SUMMARY")
print("======================")

print("Pose detected frames:", result["pose_detected_frames"])
print("Detection rate:", result["detection_rate"])
print("Minimum visibility:", MIN_VISIBILITY)

print()

print(
    "Left elbow:",
    summarize_angles(left_elbow_angles)
)

print(
    "Right elbow:",
    summarize_angles(right_elbow_angles)
)

print(
    "Left knee:",
    summarize_angles(left_knee_angles)
)

print(
    "Right knee:",
    summarize_angles(right_knee_angles)
)

print()

print("Valid left elbow measurements:", len(left_elbow_angles))
print("Valid right elbow measurements:", len(right_elbow_angles))
print("Valid left knee measurements:", len(left_knee_angles))
print("Valid right knee measurements:", len(right_knee_angles))

print("Skipped low-visibility measurements:", skipped_measurements)


analyzer.close()