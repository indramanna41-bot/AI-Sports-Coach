import math


def distance(point_a, point_b):
    dx = point_b["x"] - point_a["x"]
    dy = point_b["y"] - point_a["y"]

    return math.sqrt(
        dx ** 2 + dy ** 2
    )


def average(values):
    if not values:
        return 0.0

    return sum(values) / len(values)


def extract_basketball_features(
    landmark_frames,
    minimum_visibility=0.35
):
    """
    Basketball pose feature extraction.

    Final outputs will support:
    - Jump Technique
    - Arm Coordination
    - Balance
    - Movement Consistency
    - Jump Events Detected

    Ball Interaction is handled separately using YOLO.
    """

    body_heights = []
    body_movements = []
    arm_differences = []
    body_center_offsets = []

    valid_frames = 0
    previous_body_center = None

    for frame_data in landmark_frames:

        landmarks = frame_data["landmarks"]

        # -------------------------------------------------
        # CORE LANDMARKS
        # These are required for the frame to be usable.
        # -------------------------------------------------

        core_landmarks = [
            "left_shoulder",
            "right_shoulder",
            "left_hip",
            "right_hip"
        ]

        core_visible = all(
            landmarks[name]["visibility"]
            >= minimum_visibility
            for name in core_landmarks
        )

        if not core_visible:
            continue

        valid_frames += 1

        # =================================================
        # BODY CENTER
        # =================================================

        hip_center_x = (
            landmarks["left_hip"]["x"]
            +
            landmarks["right_hip"]["x"]
        ) / 2

        hip_center_y = (
            landmarks["left_hip"]["y"]
            +
            landmarks["right_hip"]["y"]
        ) / 2

        shoulder_center_x = (
            landmarks["left_shoulder"]["x"]
            +
            landmarks["right_shoulder"]["x"]
        ) / 2

        body_heights.append(
            hip_center_y
        )

        # =================================================
        # MOVEMENT
        # =================================================

        current_body_center = {
            "x": hip_center_x,
            "y": hip_center_y
        }

        if previous_body_center is not None:

            movement = distance(
                previous_body_center,
                current_body_center
            )

            body_movements.append(
                movement
            )

        previous_body_center = (
            current_body_center
        )

        # =================================================
        # BALANCE
        # =================================================

        body_center_offset = abs(
            shoulder_center_x
            -
            hip_center_x
        )

        body_center_offsets.append(
            body_center_offset
        )

        # =================================================
        # ARM COORDINATION
        # Only calculate when arm landmarks are visible.
        # =================================================

        arm_landmarks = [
            "left_elbow",
            "right_elbow",
            "left_wrist",
            "right_wrist"
        ]

        arms_visible = all(
            landmarks[name]["visibility"]
            >= minimum_visibility
            for name in arm_landmarks
        )

        if arms_visible:

            left_arm_length = (
                distance(
                    landmarks["left_shoulder"],
                    landmarks["left_elbow"]
                )
                +
                distance(
                    landmarks["left_elbow"],
                    landmarks["left_wrist"]
                )
            )

            right_arm_length = (
                distance(
                    landmarks["right_shoulder"],
                    landmarks["right_elbow"]
                )
                +
                distance(
                    landmarks["right_elbow"],
                    landmarks["right_wrist"]
                )
            )

            arm_difference = abs(
                left_arm_length
                -
                right_arm_length
            )

            arm_differences.append(
                arm_difference
            )

    # =====================================================
    # JUMP DETECTION
    # =====================================================

    jump_events = 0
    vertical_movements = []

    if len(body_heights) >= 3:

        baseline_height = average(
            body_heights
        )

        jump_threshold = 0.025
        in_jump = False

        for body_y in body_heights:

            vertical_rise = (
                baseline_height
                -
                body_y
            )

            vertical_movements.append(
                max(
                    vertical_rise,
                    0.0
                )
            )

            if (
                vertical_rise
                >= jump_threshold
                and not in_jump
            ):
                jump_events += 1
                in_jump = True

            elif (
                vertical_rise
                <
                jump_threshold * 0.40
            ):
                in_jump = False

    # =====================================================
    # MOVEMENT CONSISTENCY
    # =====================================================

    average_movement = average(
        body_movements
    )

    if body_movements:

        movement_variability = average(
            [
                abs(
                    movement
                    -
                    average_movement
                )
                for movement
                in body_movements
            ]
        )

    else:

        movement_variability = 0.0

    # =====================================================
    # RETURN FEATURES
    # =====================================================

    return {

        "maximum_vertical_movement": round(
            max(vertical_movements)
            if vertical_movements
            else 0.0,
            4
        ),

        "average_vertical_movement": round(
            average(
                vertical_movements
            ),
            4
        ),

        "jump_events_detected": (
            jump_events
        ),

        "average_arm_difference": round(
            average(
                arm_differences
            ),
            4
        ),

        "average_body_center_offset": round(
            average(
                body_center_offsets
            ),
            4
        ),

        "average_body_movement": round(
            average_movement,
            4
        ),

        "movement_variability": round(
            movement_variability,
            4
        ),

        "valid_basketball_frames": (
            valid_frames
        )
    }