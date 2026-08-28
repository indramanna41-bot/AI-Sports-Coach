from backend.services.athletics_service import (
    analyze_athletics_video
)


VIDEO_PATH = "uploads/athletics_test.mp4"


def test_analyze_athletics():

    result = analyze_athletics_video(
        VIDEO_PATH
    )

    # -----------------------------------------
    # MAIN ANALYSIS
    # -----------------------------------------

    print()
    print("ATHLETICS - SPRINT ANALYSIS")
    print("============================")

    print(
        "Overall Score:",
        result["overall_score"]
    )

    # -----------------------------------------
    # PERFORMANCE SCORES
    # -----------------------------------------

    print()
    print("PERFORMANCE SCORES")
    print("------------------")

    components = result["components"]

    print(
        "Running Technique:",
        components["running_technique"]
    )

    print(
        "Knee Drive:",
        components["knee_drive"]
    )

    print(
        "Stride Quality:",
        components["stride_quality"]
    )

    print(
        "Arm Movement:",
        components["arm_movement"]
    )

    print(
        "Body Posture:",
        components["body_posture"]
    )

    print(
        "Balance:",
        components["balance"]
    )

    print(
        "Movement Consistency:",
        components["movement_consistency"]
    )

    # -----------------------------------------
    # RUNNING METRICS
    # -----------------------------------------

    print()
    print("RUNNING METRICS")
    print("---------------")

    metrics = result["metrics"]

    print(
        "Average Movement Speed:",
        metrics["average_movement_speed"]
    )

    print(
        "Maximum Movement Speed:",
        metrics["maximum_movement_speed"]
    )

    print(
        "Average Stride/Ankle Separation:",
        metrics["average_stride_ankle_separation"]
    )

    print(
        "Maximum Stride/Ankle Separation:",
        metrics["maximum_stride_ankle_separation"]
    )

    print(
        "Average Knee Drive:",
        metrics["average_knee_drive"]
    )

    print(
        "Maximum Knee Drive:",
        metrics["maximum_knee_drive"]
    )

    print(
        "Left/Right Symmetry:",
        metrics["left_right_symmetry"]
    )

    print(
        "Valid Athletics Frames:",
        metrics["valid_athletics_frames"]
    )

    # -----------------------------------------
    # STRENGTHS
    # -----------------------------------------

    print()
    print("STRENGTHS")
    print("---------")

    for strength in result["strengths"]:
        print(
            "-",
            strength
        )

    # -----------------------------------------
    # WEAKNESSES
    # -----------------------------------------

    print()
    print("WEAKNESSES")
    print("----------")

    for weakness in result["weaknesses"]:
        print(
            "-",
            weakness
        )

    # -----------------------------------------
    # RECOMMENDATIONS
    # -----------------------------------------

    print()
    print("RECOMMENDATIONS")
    print("---------------")

    for recommendation in result["recommendations"]:
        print(
            "-",
            recommendation
        )

    # -----------------------------------------
    # WARNING
    # -----------------------------------------

    print()
    print("WARNING")
    print("-------")

    print(
        result["warning"]
    )

    # -----------------------------------------
    # TEST CHECKS
    # -----------------------------------------

    assert result["success"] is True
    assert result["sport"] == "athletics"
    assert 0 <= result["overall_score"] <= 100