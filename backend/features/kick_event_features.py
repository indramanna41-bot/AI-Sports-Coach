import math


def point_distance(point_a, point_b):
    dx = point_b["x"] - point_a["x"]
    dy = point_b["y"] - point_a["y"]

    return math.sqrt(
        dx ** 2 + dy ** 2
    )


def extract_kick_events(
    landmark_frames,
    ball_detection_frames,
    minimum_visibility=0.7,
    contact_distance_threshold=0.12,
    ball_motion_threshold=0.05
):
    """
    Detect prototype football kick events.

    A likely kick event is identified when:
    1. The ball is close to either ankle.
    2. The ball then shows noticeable image-space movement.

    IMPORTANT:
    This is heuristic event detection.
    It is not yet a trained kick-classification model.
    """

    pose_by_frame = {
        frame_data["frame"]: frame_data
        for frame_data in landmark_frames
    }

    ball_centers = []

    for frame_data in ball_detection_frames:
        detections = frame_data.get(
            "detections",
            []
        )

        if not detections:
            continue

        best_detection = max(
            detections,
            key=lambda item: item["confidence"]
        )

        ball_centers.append({
            "frame": frame_data["frame"],
            "center": best_detection["center"],
            "confidence": best_detection["confidence"]
        })

    kick_events = []

    for index in range(
        len(ball_centers) - 1
    ):
        current_ball = ball_centers[index]
        next_ball = ball_centers[index + 1]

        frame_number = current_ball[
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
            left_ankle["visibility"]
            < minimum_visibility
            or right_ankle["visibility"]
            < minimum_visibility
        ):
            continue

        ball_center = current_ball[
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

        nearest_foot_distance = min(
            left_distance,
            right_distance
        )

        ball_displacement = point_distance(
            current_ball["center"],
            next_ball["center"]
        )

        if (
            nearest_foot_distance
            <= contact_distance_threshold
            and ball_displacement
            >= ball_motion_threshold
        ):
            kicking_foot = (
                "left"
                if left_distance < right_distance
                else "right"
            )

            kick_events.append({
                "frame": frame_number,
                "kicking_foot": kicking_foot,
                "ball_foot_distance": round(
                    nearest_foot_distance,
                    4
                ),
                "ball_displacement_after_contact": round(
                    ball_displacement,
                    4
                ),
                "ball_confidence": current_ball[
                    "confidence"
                ]
            })

    return {
        "kick_events_detected": len(
            kick_events
        ),

        "kick_events": kick_events,

        "contact_distance_threshold": (
            contact_distance_threshold
        ),

        "ball_motion_threshold": (
            ball_motion_threshold
        )
    }