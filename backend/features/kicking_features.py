from backend.features.angles import calculate_angle


def extract_kicking_features(
    landmark_frames,
    minimum_visibility=0.7
):
    """
    Extract prototype kicking-posture measurements
    from MediaPipe pose landmarks.

    These measurements do not yet prove whether
    a shot or pass was successful.
    """

    kicking_samples = []

    for frame_data in landmark_frames:
        landmarks = frame_data["landmarks"]

        required_names = [
            "left_shoulder",
            "right_shoulder",
            "left_hip",
            "right_hip",
            "left_knee",
            "right_knee",
            "left_ankle",
            "right_ankle"
        ]

        valid = True

        for name in required_names:
            if (
                landmarks[name]["visibility"]
                < minimum_visibility
            ):
                valid = False
                break

        if not valid:
            continue

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

        shoulder_tilt = abs(
            landmarks["left_shoulder"]["y"]
            - landmarks["right_shoulder"]["y"]
        )

        hip_tilt = abs(
            landmarks["left_hip"]["y"]
            - landmarks["right_hip"]["y"]
        )

        left_ankle_height = (
            landmarks["left_ankle"]["y"]
        )

        right_ankle_height = (
            landmarks["right_ankle"]["y"]
        )

        ankle_height_difference = abs(
            left_ankle_height
            - right_ankle_height
        )

        kicking_samples.append({
            "frame": frame_data["frame"],
            "timestamp_ms": frame_data["timestamp_ms"],
            "left_knee_angle": left_knee_angle,
            "right_knee_angle": right_knee_angle,
            "shoulder_tilt": shoulder_tilt,
            "hip_tilt": hip_tilt,
            "ankle_height_difference": (
                ankle_height_difference
            )
        })

    if not kicking_samples:
        return {
            "average_left_knee_angle": None,
            "average_right_knee_angle": None,
            "average_shoulder_tilt": None,
            "average_hip_tilt": None,
            "maximum_ankle_height_difference": None,
            "valid_kicking_frames": 0
        }

    left_angles = [
        sample["left_knee_angle"]
        for sample in kicking_samples
        if sample["left_knee_angle"] is not None
    ]

    right_angles = [
        sample["right_knee_angle"]
        for sample in kicking_samples
        if sample["right_knee_angle"] is not None
    ]

    shoulder_tilts = [
        sample["shoulder_tilt"]
        for sample in kicking_samples
    ]

    hip_tilts = [
        sample["hip_tilt"]
        for sample in kicking_samples
    ]

    ankle_differences = [
        sample["ankle_height_difference"]
        for sample in kicking_samples
    ]

    return {
        "average_left_knee_angle": (
            round(
                sum(left_angles) / len(left_angles),
                2
            )
            if left_angles
            else None
        ),

        "average_right_knee_angle": (
            round(
                sum(right_angles) / len(right_angles),
                2
            )
            if right_angles
            else None
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

        "maximum_ankle_height_difference": round(
            max(ankle_differences),
            4
        ),

        "valid_kicking_frames": len(
            kicking_samples
        )
    }