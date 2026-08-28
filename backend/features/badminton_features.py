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


def extract_badminton_features(
    landmark_frames,
    minimum_visibility=0.7
):
    """
    Build a structured feature dictionary for the
    badminton prototype.

    These are measured video-derived features.
    They are not validated talent predictions.
    """

    left_elbow_angles = []
    right_elbow_angles = []
    left_knee_angles = []
    right_knee_angles = []

    for frame_data in landmark_frames:
        landmarks = frame_data["landmarks"]

        if (
            landmarks["left_shoulder"]["visibility"] >= minimum_visibility
            and landmarks["left_elbow"]["visibility"] >= minimum_visibility
            and landmarks["left_wrist"]["visibility"] >= minimum_visibility
        ):
            left_elbow_angles.append(
                calculate_angle(
                    landmarks["left_shoulder"],
                    landmarks["left_elbow"],
                    landmarks["left_wrist"]
                )
            )

        if (
            landmarks["right_shoulder"]["visibility"] >= minimum_visibility
            and landmarks["right_elbow"]["visibility"] >= minimum_visibility
            and landmarks["right_wrist"]["visibility"] >= minimum_visibility
        ):
            right_elbow_angles.append(
                calculate_angle(
                    landmarks["right_shoulder"],
                    landmarks["right_elbow"],
                    landmarks["right_wrist"]
                )
            )

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

    movement = extract_movement_features(
        landmark_frames,
        minimum_visibility
    )

    balance = extract_balance_features(
        landmark_frames,
        minimum_visibility
    )

    return {
        "left_elbow": summarize_angles(
            left_elbow_angles
        ),

        "right_elbow": summarize_angles(
            right_elbow_angles
        ),

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

        "valid_movement_frames": movement[
            "valid_movement_frames"
        ],

        "valid_balance_frames": balance[
            "valid_balance_frames"
        ]
    }