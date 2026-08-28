from backend.vision.pose_analyzer import PoseAnalyzer

from backend.features.athletics_features import (
    extract_athletics_features
)

from backend.sports.athletics import (
    analyze_athletics
)


def analyze_athletics_video(
    video_path,
    target_fps=5
):
    """
    Run the complete Athletics Sprint analysis.

    Pipeline:
    Video
    -> MediaPipe Pose
    -> Athletics Feature Extraction
    -> Heuristic Sprint Scoring
    """

    # --------------------------------------------------
    # 1. POSE ANALYSIS
    # --------------------------------------------------

    pose_analyzer = PoseAnalyzer(
        target_fps=target_fps
    )

    try:
        pose_result = pose_analyzer.analyze_video(
            video_path
        )

    finally:
        pose_analyzer.close()

    # --------------------------------------------------
    # 2. BASIC VALIDATION
    # --------------------------------------------------

    if pose_result["processed_frames"] < 3:
        raise ValueError(
            "The video does not contain enough processed frames."
        )

    if pose_result["pose_detected_frames"] == 0:
        raise ValueError(
            "No usable human pose was detected."
        )

    # --------------------------------------------------
    # 3. ATHLETICS FEATURE EXTRACTION
    # --------------------------------------------------

    features = extract_athletics_features(
        pose_result["landmarks"]
    )

    if features["valid_athletics_frames"] < 3:
        raise ValueError(
            "Not enough valid sprint pose frames were detected."
        )

    # --------------------------------------------------
    # 4. ATHLETICS SCORING
    # --------------------------------------------------

    analysis = analyze_athletics(
        features
    )

    # --------------------------------------------------
    # 5. POSE QUALITY INFORMATION
    # --------------------------------------------------

    analysis["pose_quality"] = {

        "total_video_frames":
            pose_result["total_frames"],

        "processed_frames":
            pose_result["processed_frames"],

        "pose_detected_frames":
            pose_result["pose_detected_frames"],

        "detection_rate":
            pose_result["detection_rate"],

        "original_fps":
            pose_result["original_fps"],

        "analysis_fps":
            pose_result["target_fps"]
    }

    # --------------------------------------------------
    # 6. RETURN FINAL RESULT
    # --------------------------------------------------

    return analysis