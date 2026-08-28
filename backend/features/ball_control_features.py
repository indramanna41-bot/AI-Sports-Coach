import math


def point_distance(point_a, point_b):
    dx = point_b["x"] - point_a["x"]
    dy = point_b["y"] - point_a["y"]

    return math.sqrt(
        dx ** 2 + dy ** 2
    )


def extract_ball_control_features(
    landmark_frames,
    ball_detection_frames,
    minimum_visibility=0.7
):
    """
    Prototype football ball-control measurements.

    Measures how often the detected ball stays close
    to either ankle/foot.

    IMPORTANT:
    This does not yet prove dribbling quality.
    It measures player-ball proximity and continuity.
    """

    pose_by_frame = {
        frame_data["frame"]: frame_data
        for frame_data in landmark_frames
    }

    control_distances = []
    close_control_frames = 0
    matched_frames = 0

    for ball_frame in ball_detection_frames:
        detections = ball_frame.get(
            "detections",
            []
        )

        if not detections:
            continue

        frame_number = ball_frame[
            "frame"
        ]

        pose_frame = pose_by_frame.get(
            frame_number
        )

        if pose_frame is None:
            continue

        landmarks = pose_frame[
            "landmarks"
        ]

        left_ankle = landmarks[
            "left_ankle"
        ]

        right_ankle = landmarks[
            "right_ankle"
        ]

        if (
            left_ankle["visibility"] < minimum_visibility
            or right_ankle["visibility"] < minimum_visibility
        ):
            continue

        best_ball = max(
            detections,
            key=lambda item: item["confidence"]
        )

        ball_center = best_ball[
            "center"
        ]

        left_distance = point_distance(
            ball_center,
            left_ankle
        )

        right_distance = point_distance(
            ball_center,
            right_ankle
        )

        nearest_distance = min(
            left_distance,
            right_distance
        )

        control_distances.append(
            nearest_distance
        )

        matched_frames += 1

        # Prototype proximity threshold only.
        if nearest_distance <= 0.15:
            close_control_frames += 1

    if matched_frames > 0:
        close_control_ratio = (
            close_control_frames
            / matched_frames
        )

        average_control_distance = (
            sum(control_distances)
            / len(control_distances)
        )

        minimum_control_distance = min(
            control_distances
        )
    else:
        close_control_ratio = 0.0
        average_control_distance = None
        minimum_control_distance = None

    return {
        "matched_ball_pose_frames": matched_frames,

        "close_control_frames": (
            close_control_frames
        ),

        "close_control_ratio": round(
            close_control_ratio,
            3
        ),

        "average_ball_foot_distance": (
            round(
                average_control_distance,
                4
            )
            if average_control_distance
            is not None
            else None
        ),

        "minimum_ball_foot_distance": (
            round(
                minimum_control_distance,
                4
            )
            if minimum_control_distance
            is not None
            else None
        )
    }