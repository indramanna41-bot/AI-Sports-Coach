from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


VIDEO_PATH = (
    "uploads/FREESTYLE 😱🔥 FOOTBALL SKILLS ⚽️⭐️ BEACH FOOTBALL "
    "valerikostovofficial - v7skills (1080p, h264, youtube).mp4"
)


def test_analyze_football():

    with open(VIDEO_PATH, "rb") as video_file:

        response = client.post(
            "/api/analyze/football",
            data={
                "user_id": "test_user_1"
            },
            files={
                "file": (
                    "football_test.mp4",
                    video_file,
                    "video/mp4"
                )
            }
        )

    print()
    print("STATUS CODE:")
    print(response.status_code)

    print()
    print("SERVER RESPONSE:")
    print(response.text)

    assert response.status_code == 200

    result = response.json()

    print()
    print("FOOTBALL ANALYSIS")
    print("=================")

    print(
        "Overall Score:",
        result["overall_score"]
    )

    print()
    print("COMPONENT SCORES")
    print("----------------")

    components = result["components"]

    print(
        "Movement:",
        components["movement"]
    )

    print(
        "Lower Body Technique:",
        components["lower_body_technique"]
    )

    print(
        "Balance:",
        components["balance"]
    )

    print(
        "Ball Interaction:",
        components["ball_interaction"]
    )

    print(
        "Consistency:",
        components["consistency"]
    )

    if "running_ability" in components:
        print(
            "Running Ability:",
            components["running_ability"]
        )

    if "ball_control" in components:
        print(
            "Ball Control:",
            components["ball_control"]
        )

    if "kicking_posture" in components:
        print(
            "Kicking Posture:",
            components["kicking_posture"]
        )

    if "kick_events_detected" in result:

        print()
        print("KICKING ACTIVITY")
        print("----------------")

        print(
            "Kick Events Detected:",
            result["kick_events_detected"]
        )

    print()
    print("STRENGTHS")
    print("---------")

    for strength in result["strengths"]:
        print(
            "-",
            strength
        )

    print()
    print("WEAKNESSES")
    print("----------")

    for weakness in result["weaknesses"]:
        print(
            "-",
            weakness
        )

    print()
    print("RECOMMENDATIONS")
    print("---------------")

    for recommendation in result["recommendations"]:
        print(
            "-",
            recommendation
        )

    if "warning" in result:

        print()
        print("WARNING")
        print("-------")

        print(
            result["warning"]
        )