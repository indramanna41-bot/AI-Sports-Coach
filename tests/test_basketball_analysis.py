from backend.services.basketball_service import (
    analyze_basketball_video
)


VIDEO_PATH = "uploads/basketball_test.mp4"


def test_analyze_basketball():

    result = analyze_basketball_video(
        VIDEO_PATH
    )

    print()
    print("BASKETBALL ANALYSIS")
    print("===================")

    print(
        "Overall Score:",
        result["overall_score"]
    )

    print()
    print("PERFORMANCE SCORES")
    print("------------------")

    components = result[
        "components"
    ]

    print(
        "Ball Interaction:",
        components[
            "ball_interaction"
        ]
    )

    print(
        "Jump Technique:",
        components[
            "jump_technique"
        ]
    )

    print(
        "Arm Coordination:",
        components[
            "arm_coordination"
        ]
    )

    print(
        "Balance:",
        components[
            "balance"
        ]
    )

    print(
        "Movement Consistency:",
        components[
            "movement_consistency"
        ]
    )

    print()
    print("METRICS")
    print("-------")

    print(
        "Jump Events Detected:",
        result["metrics"][
            "jump_events_detected"
        ]
    )

    print()
    print("STRENGTHS")
    print("---------")

    for strength in result[
        "strengths"
    ]:
        print(
            "-",
            strength
        )

    print()
    print("WEAKNESSES")
    print("----------")

    for weakness in result[
        "weaknesses"
    ]:
        print(
            "-",
            weakness
        )

    print()
    print("RECOMMENDATIONS")
    print("---------------")

    for recommendation in result[
        "recommendations"
    ]:
        print(
            "-",
            recommendation
        )

    assert result[
        "success"
    ] is True

    assert result[
        "sport"
    ] == "basketball"

    assert (
        0
        <=
        result["overall_score"]
        <=
        100
    )