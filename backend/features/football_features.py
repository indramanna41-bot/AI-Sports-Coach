import math

from backend.features.angles import (
    calculate_angle,
    summarize_angles
)

from backend.features.movement import (
    extract_movement_features
)

from backend.features.balance import (
    extract_balance_features
)


def calculate_point_distance(point_a, point_b):
    """
    Calculate normalized 2D distance between two points.
    """

    dx = point_b["x"] - point_a["x"]
    dy = point_b["y"] - point_a["y"]

    return math.sqrt(
        dx ** 2 + dy ** 2
    )


def extract_football_features(
    landmark_frames,
    ball_detections,
    minimum_visibility=0.7
):
    """
    Extract Football Phase-1 prototype features.

    Pose-derived features:
    - knee movement
    - ankle movement
    - player movement
    - balance
    - movement consistency

    Ball-derived features:
    - detection rate
    - normalized ball displacement
    - approximate player-to-ball distance

    IMPORTANT:
    These are prototype image-space measurements.
    They are not calibrated real-world speed or distance.
    """

    left_knee_angles = []
    right_knee_angles = []

    left_ankle_positions = []
    right_ankle_positions = []

    for frame_data in landmark_frames:
        landmarks = frame_data["landmarks"]

        if (
            landmarks["left_hip"]["visibility"] >= minimum_visibility
            and landmarks["left_knee"]["visibility"] >= minimum_visibility
            and landmarks["left_ankle"]["visibility"] >= minimum_visibility
        ):
            left_knee_angles.append(
                calculate_angle(
                    landmarks["left_hip"],
                    landmarks["left_knee"],
                    landmarks["left_ankle"]
                )
            )

            left_ankle_positions.append(
                {
                    "x": landmarks["left_ankle"]["x"],
                    "y": landmarks["left_ankle"]["y"]
                }
            )

        if (
            landmarks["right_hip"]["visibility"] >= minimum_visibility
            and landmarks["right_knee"]["visibility"] >= minimum_visibility
            and landmarks["right_ankle"]["visibility"] >= minimum_visibility
        ):
            right_knee_angles.append(
                calculate_angle(
                    landmarks["right_hip"],
                    landmarks["right_knee"],
                    landmarks["right_ankle"]
                )
            )

            right_ankle_positions.append(
                {
                    "x": landmarks["right_ankle"]["x"],
                    "y": landmarks["right_ankle"]["y"]
                }
            )

    movement = extract_movement_features(
        landmark_frames,
        minimum_visibility
    )

    balance = extract_balance_features(
        landmark_frames,
        minimum_visibility
    )

    # --------------------------------------------------
    # Ball features
    # --------------------------------------------------

    valid_ball_centers = []

    total_detection_frames = len(
        ball_detections
    )

    frames_with_ball = 0

    for frame_detection in ball_detections:
        detections = frame_detection.get(
            "detections",
            []
        )

        if not detections:
            continue

        # Use highest confidence ball detection.
        best_detection = max(
            detections,
            key=lambda item: item["confidence"]
        )

        valid_ball_centers.append(
            {
                "x": best_detection["center"]["x"],
                "y": best_detection["center"]["y"],
                "frame": frame_detection["frame"]
            }
        )

        frames_with_ball += 1

    if total_detection_frames > 0:
        ball_detection_rate = (
            frames_with_ball
            / total_detection_frames
        )
    else:
        ball_detection_rate = 0.0

    ball_displacements = []

    for index in range(
        1,
        len(valid_ball_centers)
    ):
        previous = valid_ball_centers[
            index - 1
        ]

        current = valid_ball_centers[
            index
        ]

        distance = calculate_point_distance(
            previous,
            current
        )

        ball_displacements.append(
            distance
        )

    if ball_displacements:
        average_ball_displacement = (
            sum(ball_displacements)
            / len(ball_displacements)
        )

        maximum_ball_displacement = max(
            ball_displacements
        )

    else:
        average_ball_displacement = 0.0
        maximum_ball_displacement = 0.0

    # --------------------------------------------------
    # Approximate player-ball distance
    # --------------------------------------------------

    player_ball_distances = []

    pose_by_frame = {
        frame_data["frame"]: frame_data
        for frame_data in landmark_frames
    }

    for ball_data in valid_ball_centers:
        frame_number = ball_data["frame"]

        pose_frame = pose_by_frame.get(
            frame_number
        )

        if not pose_frame:
            continue

        landmarks = pose_frame["landmarks"]

        left_ankle = landmarks[
            "left_ankle"
        ]

        right_ankle = landmarks[
            "right_ankle"
        ]

        if (
            left_ankle["visibility"]
            < minimum_visibility
            or right_ankle["visibility"]
            < minimum_visibility
        ):
            continue

        left_distance = (
            calculate_point_distance(
                ball_data,
                left_ankle
            )
        )

        right_distance = (
            calculate_point_distance(
                ball_data,
                right_ankle
            )
        )

        player_ball_distances.append(
            min(
                left_distance,
                right_distance
            )
        )

    if player_ball_distances:
        average_player_ball_distance = (
            sum(player_ball_distances)
            / len(player_ball_distances)
        )

        minimum_player_ball_distance = min(
            player_ball_distances
        )
    else:
        average_player_ball_distance = None
        minimum_player_ball_distance = None

    return {
        "left_knee": summarize_angles(
            left_knee_angles
        ),

        "right_knee": summarize_angles(
            right_knee_angles
        ),

        "movement_distance": movement[
            "movement_distance"
        ],

        "average_movement_speed": movement[
            "average_movement_speed"
        ],

        "maximum_movement_speed": movement[
            "maximum_movement_speed"
        ],

        "movement_speed_variability": movement[
            "movement_speed_variability"
        ],

        "movement_consistency": movement[
            "movement_consistency"
        ],

        "average_body_center_offset": balance[
            "average_body_center_offset"
        ],

        "average_shoulder_tilt": balance[
            "average_shoulder_tilt"
        ],

        "average_hip_tilt": balance[
            "average_hip_tilt"
        ],

        "ball_detection_rate": round(
            ball_detection_rate,
            3
        ),

        "average_ball_displacement": round(
            average_ball_displacement,
            4
        ),

        "maximum_ball_displacement": round(
            maximum_ball_displacement,
            4
        ),

        "average_player_ball_distance": (
            round(
                average_player_ball_distance,
                4
            )
            if average_player_ball_distance
            is not None
            else None
        ),

        "minimum_player_ball_distance": (
            round(
                minimum_player_ball_distance,
                4
            )
            if minimum_player_ball_distance
            is not None
            else None
        ),

        "valid_movement_frames": movement[
            "valid_movement_frames"
        ],

        "valid_balance_frames": balance[
            "valid_balance_frames"
        ],

        "ball_frames_tested": (
            total_detection_frames
        ),

        "ball_frames_detected": (
            frames_with_ball
        )
    }