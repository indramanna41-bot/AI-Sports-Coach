import math

from backend.features.angles import calculate_angle
from backend.features.movement import extract_movement_features
from backend.features.balance import extract_balance_features


def point_distance(point_a, point_b):
    """
    Calculate normalized image-space distance
    between two pose landmarks.
    """

    dx = point_b["x"] - point_a["x"]
    dy = point_b["y"] - point_a["y"]

    return math.sqrt(
        dx ** 2 + dy ** 2
    )


def extract_athletics_features(
    landmark_frames,
    minimum_visibility=0.7
):
    """
    Extract prototype sprint-related features
    from MediaPipe pose landmarks.

    These measurements are image-space measurements
    and are not real-world meters or km/h.
    """

    left_knee_angles = []
    right_knee_angles = []

    left_elbow_angles = []
    right_elbow_angles = []

    ankle_separations = []
    knee_drive_values = []

    valid_frames = 0

    # --------------------------------------------------
    # PROCESS EACH POSE FRAME
    # --------------------------------------------------

    for frame_data in landmark_frames:

        landmarks = frame_data["landmarks"]

        required_landmarks = [
            "left_shoulder",
            "right_shoulder",
            "left_elbow",
            "right_elbow",
            "left_wrist",
            "right_wrist",
            "left_hip",
            "right_hip",
            "left_knee",
            "right_knee",
            "left_ankle",
            "right_ankle"
        ]

        # Skip frame if important body landmarks
        # are not clearly visible.
        if any(
            landmarks[name]["visibility"]
            < minimum_visibility
            for name in required_landmarks
        ):
            continue

        valid_frames += 1

        # --------------------------------------------------
        # KNEE ANGLES
        # --------------------------------------------------

        left_knee_angle = calculate_angle(
            landmarks["left_hip"],
            landmarks["left_knee"],
            landmarks["left_ankle"]
        )

        right_knee_angle = calculate_angle(
            landmarks["right_hip"],
            landmarks["right_knee"],
            landmarks["right_ankle"]
        )

        left_knee_angles.append(
            left_knee_angle
        )

        right_knee_angles.append(
            right_knee_angle
        )

        # --------------------------------------------------
        # ARM / ELBOW ANGLES
        # --------------------------------------------------

        left_elbow_angle = calculate_angle(
            landmarks["left_shoulder"],
            landmarks["left_elbow"],
            landmarks["left_wrist"]
        )

        right_elbow_angle = calculate_angle(
            landmarks["right_shoulder"],
            landmarks["right_elbow"],
            landmarks["right_wrist"]
        )

        left_elbow_angles.append(
            left_elbow_angle
        )

        right_elbow_angles.append(
            right_elbow_angle
        )

        # --------------------------------------------------
        # STRIDE / ANKLE SEPARATION
        # --------------------------------------------------

        ankle_separation = point_distance(
            landmarks["left_ankle"],
            landmarks["right_ankle"]
        )

        ankle_separations.append(
            ankle_separation
        )

        # --------------------------------------------------
        # KNEE DRIVE
        # --------------------------------------------------

        knee_drive = abs(
            landmarks["left_knee"]["y"]
            - landmarks["right_knee"]["y"]
        )

        knee_drive_values.append(
            knee_drive
        )

    # --------------------------------------------------
    # EXISTING MOVEMENT FEATURES
    # --------------------------------------------------

    movement_features = (
        extract_movement_features(
            landmark_frames,
            minimum_visibility
        )
    )

    # --------------------------------------------------
    # EXISTING BALANCE FEATURES
    # --------------------------------------------------

    balance_features = (
        extract_balance_features(
            landmark_frames,
            minimum_visibility
        )
    )

    # --------------------------------------------------
    # HELPER
    # --------------------------------------------------

    def average(values):

        if not values:
            return 0.0

        return sum(values) / len(values)

    # --------------------------------------------------
    # LEG SYMMETRY
    # --------------------------------------------------

    average_left_knee = average(
        left_knee_angles
    )

    average_right_knee = average(
        right_knee_angles
    )

    leg_symmetry_difference = abs(
        average_left_knee
        - average_right_knee
    )

    # --------------------------------------------------
    # RETURN FEATURES
    # --------------------------------------------------

    return {

        "average_left_knee_angle": round(
            average_left_knee,
            2
        ),

        "average_right_knee_angle": round(
            average_right_knee,
            2
        ),

        "leg_symmetry_difference": round(
            leg_symmetry_difference,
            2
        ),

        "average_left_elbow_angle": round(
            average(
                left_elbow_angles
            ),
            2
        ),

        "average_right_elbow_angle": round(
            average(
                right_elbow_angles
            ),
            2
        ),

        "average_ankle_separation": round(
            average(
                ankle_separations
            ),
            4
        ),

        "maximum_ankle_separation": round(
            max(
                ankle_separations
            )
            if ankle_separations
            else 0.0,
            4
        ),

        "average_knee_drive": round(
            average(
                knee_drive_values
            ),
            4
        ),

        "maximum_knee_drive": round(
            max(
                knee_drive_values
            )
            if knee_drive_values
            else 0.0,
            4
        ),

        "average_movement_speed":
            movement_features.get(
                "average_movement_speed",
                0.0
            ),

        "maximum_movement_speed":
            movement_features.get(
                "maximum_movement_speed",
                0.0
            ),

        "movement_speed_variability":
            movement_features.get(
                "movement_speed_variability",
                0.0
            ),

        "movement_consistency":
            movement_features.get(
                "movement_consistency",
                0.0
            ),

        "average_body_center_offset":
            balance_features.get(
                "average_body_center_offset",
                0.0
            ),

        "average_shoulder_tilt":
            balance_features.get(
                "average_shoulder_tilt",
                0.0
            ),

        "average_hip_tilt":
            balance_features.get(
                "average_hip_tilt",
                0.0
            ),

        "valid_athletics_frames":
            valid_frames
    }