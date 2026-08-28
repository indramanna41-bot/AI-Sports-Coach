import math
import statistics


def point_distance(point_a, point_b):
    dx = point_b["x"] - point_a["x"]
    dy = point_b["y"] - point_a["y"]

    return math.sqrt(
        dx ** 2 + dy ** 2
    )


def extract_running_features(
    landmark_frames,
    minimum_visibility=0.7
):
    """
    Extract prototype running-related measurements.

    These are normalized image-space features.
    They are not real-world meters, cadence, or speed.
    """

    hip_positions = []
    ankle_separations = []
    knee_heights = []

    valid_frames = 0

    for frame_data in landmark_frames:
        landmarks = frame_data["landmarks"]

        required = [
            landmarks["left_hip"],
            landmarks["right_hip"],
            landmarks["left_knee"],
            landmarks["right_knee"],
            landmarks["left_ankle"],
            landmarks["right_ankle"]
        ]

        if any(
            landmark["visibility"] < minimum_visibility
            for landmark in required
        ):
            continue

        valid_frames += 1

        hip_center = {
            "x": (
                landmarks["left_hip"]["x"]
                + landmarks["right_hip"]["x"]
            ) / 2,

            "y": (
                landmarks["left_hip"]["y"]
                + landmarks["right_hip"]["y"]
            ) / 2
        }

        hip_positions.append({
            "x": hip_center["x"],
            "y": hip_center["y"],
            "timestamp_ms": frame_data["timestamp_ms"]
        })

        ankle_distance = point_distance(
            landmarks["left_ankle"],
            landmarks["right_ankle"]
        )

        ankle_separations.append(
            ankle_distance
        )

        knee_height_difference = abs(
            landmarks["left_knee"]["y"]
            - landmarks["right_knee"]["y"]
        )

        knee_heights.append(
            knee_height_difference
        )

    # ----------------------------------
    # Hip movement speed
    # ----------------------------------

    hip_speeds = []

    for index in range(
        1,
        len(hip_positions)
    ):
        previous = hip_positions[index - 1]
        current = hip_positions[index]

        distance = point_distance(
            previous,
            current
        )

        time_ms = (
            current["timestamp_ms"]
            - previous["timestamp_ms"]
        )

        if time_ms > 0:
            seconds = time_ms / 1000

            hip_speeds.append(
                distance / seconds
            )

    if hip_speeds:
        average_running_speed = (
            sum(hip_speeds)
            / len(hip_speeds)
        )

        maximum_running_speed = max(
            hip_speeds
        )

        speed_variability = (
            statistics.pstdev(hip_speeds)
            if len(hip_speeds) >= 2
            else 0
        )
    else:
        average_running_speed = 0
        maximum_running_speed = 0
        speed_variability = 0

    # ----------------------------------
    # Leg movement
    # ----------------------------------

    if ankle_separations:
        average_ankle_separation = (
            sum(ankle_separations)
            / len(ankle_separations)
        )

        maximum_ankle_separation = max(
            ankle_separations
        )
    else:
        average_ankle_separation = 0
        maximum_ankle_separation = 0

    if knee_heights:
        average_knee_lift_difference = (
            sum(knee_heights)
            / len(knee_heights)
        )

        maximum_knee_lift_difference = max(
            knee_heights
        )
    else:
        average_knee_lift_difference = 0
        maximum_knee_lift_difference = 0

    return {
        "average_running_speed": round(
            average_running_speed,
            4
        ),

        "maximum_running_speed": round(
            maximum_running_speed,
            4
        ),

        "running_speed_variability": round(
            speed_variability,
            4
        ),

        "average_ankle_separation": round(
            average_ankle_separation,
            4
        ),

        "maximum_ankle_separation": round(
            maximum_ankle_separation,
            4
        ),

        "average_knee_lift_difference": round(
            average_knee_lift_difference,
            4
        ),

        "maximum_knee_lift_difference": round(
            maximum_knee_lift_difference,
            4
        ),

        "valid_running_frames": valid_frames
    }