import math
import statistics


def calculate_distance(point_a, point_b):
    """
    Calculate 2D normalized image-space distance.
    """

    dx = point_b["x"] - point_a["x"]
    dy = point_b["y"] - point_a["y"]

    return math.sqrt(
        dx ** 2 + dy ** 2
    )


def calculate_midpoint(point_a, point_b):
    """
    Calculate midpoint between two landmarks.
    """

    return {
        "x": (point_a["x"] + point_b["x"]) / 2,
        "y": (point_a["y"] + point_b["y"]) / 2
    }


def extract_movement_features(
    landmark_frames,
    minimum_visibility=0.7
):
    """
    Extract normalized image-space movement features.

    IMPORTANT:
    These distances and speeds are not meters or m/s.
    They are normalized video-coordinate measurements.
    """

    hip_centers = []

    for frame_data in landmark_frames:

        landmarks = frame_data["landmarks"]

        left_hip = landmarks["left_hip"]
        right_hip = landmarks["right_hip"]

        if (
            left_hip["visibility"] < minimum_visibility
            or right_hip["visibility"] < minimum_visibility
        ):
            continue

        center = calculate_midpoint(
            left_hip,
            right_hip
        )

        hip_centers.append({
            "x": center["x"],
            "y": center["y"],
            "timestamp_ms": frame_data["timestamp_ms"]
        })

    if len(hip_centers) < 2:
        return {
            "movement_distance": 0.0,
            "average_movement_speed": 0.0,
            "maximum_movement_speed": 0.0,
            "movement_speed_variability": None,
            "movement_consistency": None,
            "valid_movement_frames": len(hip_centers)
        }

    distances = []
    speeds = []

    for index in range(1, len(hip_centers)):

        previous = hip_centers[index - 1]
        current = hip_centers[index]

        distance = calculate_distance(
            previous,
            current
        )

        distances.append(distance)

        time_difference_ms = (
            current["timestamp_ms"]
            - previous["timestamp_ms"]
        )

        if time_difference_ms > 0:

            time_difference_seconds = (
                time_difference_ms / 1000
            )

            speed = (
                distance
                / time_difference_seconds
            )

            speeds.append(speed)

    total_distance = sum(distances)

    if speeds:

        average_speed = (
            sum(speeds) / len(speeds)
        )

        maximum_speed = max(speeds)

    else:

        average_speed = 0.0
        maximum_speed = 0.0

    if len(speeds) >= 2:

        speed_variability = statistics.pstdev(
            speeds
        )

        if average_speed > 0:

            coefficient_of_variation = (
                speed_variability
                / average_speed
            )

            movement_consistency = (
                1 / (1 + coefficient_of_variation)
            )

        else:

            movement_consistency = 0.0

    else:

        speed_variability = None
        movement_consistency = None

    return {
        "movement_distance": round(
            total_distance,
            4
        ),

        "average_movement_speed": round(
            average_speed,
            4
        ),

        "maximum_movement_speed": round(
            maximum_speed,
            4
        ),

        "movement_speed_variability": (
            round(speed_variability, 4)
            if speed_variability is not None
            else None
        ),

        "movement_consistency": (
            round(movement_consistency, 4)
            if movement_consistency is not None
            else None
        ),

        "valid_movement_frames": len(
            hip_centers
        )
    }