import math


def calculate_midpoint(point_a, point_b):
    return {
        "x": (point_a["x"] + point_b["x"]) / 2,
        "y": (point_a["y"] + point_b["y"]) / 2
    }


def calculate_distance(point_a, point_b):
    dx = point_b["x"] - point_a["x"]
    dy = point_b["y"] - point_a["y"]

    return math.sqrt(
        dx ** 2 + dy ** 2
    )


def extract_balance_features(
    landmark_frames,
    minimum_visibility=0.7
):
    """
    Prototype balance-related measurements.

    These are heuristic geometric features,
    not clinically or scientifically validated
    balance scores.
    """

    body_center_offsets = []
    shoulder_tilts = []
    hip_tilts = []

    valid_frames = 0

    for frame_data in landmark_frames:
        landmarks = frame_data["landmarks"]

        required = [
            landmarks["left_shoulder"],
            landmarks["right_shoulder"],
            landmarks["left_hip"],
            landmarks["right_hip"],
            landmarks["left_ankle"],
            landmarks["right_ankle"]
        ]

        if any(
            landmark["visibility"] < minimum_visibility
            for landmark in required
        ):
            continue

        valid_frames += 1

        shoulder_center = calculate_midpoint(
            landmarks["left_shoulder"],
            landmarks["right_shoulder"]
        )

        hip_center = calculate_midpoint(
            landmarks["left_hip"],
            landmarks["right_hip"]
        )

        ankle_center = calculate_midpoint(
            landmarks["left_ankle"],
            landmarks["right_ankle"]
        )

        body_center_offset = calculate_distance(
            hip_center,
            ankle_center
        )

        body_center_offsets.append(
            body_center_offset
        )

        shoulder_tilt = abs(
            landmarks["left_shoulder"]["y"]
            - landmarks["right_shoulder"]["y"]
        )

        hip_tilt = abs(
            landmarks["left_hip"]["y"]
            - landmarks["right_hip"]["y"]
        )

        shoulder_tilts.append(
            shoulder_tilt
        )

        hip_tilts.append(
            hip_tilt
        )

    if valid_frames == 0:
        return {
            "average_body_center_offset": None,
            "average_shoulder_tilt": None,
            "average_hip_tilt": None,
            "valid_balance_frames": 0
        }

    return {
        "average_body_center_offset": round(
            sum(body_center_offsets)
            / len(body_center_offsets),
            4
        ),
        "average_shoulder_tilt": round(
            sum(shoulder_tilts)
            / len(shoulder_tilts),
            4
        ),
        "average_hip_tilt": round(
            sum(hip_tilts)
            / len(hip_tilts),
            4
        ),
        "valid_balance_frames": valid_frames
    }