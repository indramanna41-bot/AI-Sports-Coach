import cv2
import math

from ultralytics import YOLO

from backend.vision.pose_analyzer import PoseAnalyzer
from backend.features.basketball_features import extract_basketball_features
from backend.sports.basketball import analyze_basketball


def distance(point_a, point_b):
    dx = point_b["x"] - point_a["x"]
    dy = point_b["y"] - point_a["y"]

    return math.sqrt(
        dx ** 2 + dy ** 2
    )


def analyze_basketball_video(
    video_path,
    target_fps=5
):
    # =====================================================
    # 1. MEDIAPIPE POSE ANALYSIS
    # =====================================================

    pose_analyzer = PoseAnalyzer(
        target_fps=target_fps
    )

    try:
        pose_result = pose_analyzer.analyze_video(
            video_path
        )

    finally:
        pose_analyzer.close()

    if pose_result["processed_frames"] < 3:
        raise ValueError(
            "The video does not contain enough processed frames."
        )

    if pose_result["pose_detected_frames"] == 0:
        raise ValueError(
            "No usable human pose was detected."
        )

    basketball_features = extract_basketball_features(
        pose_result["landmarks"]
    )

    if basketball_features[
        "valid_basketball_frames"
    ] < 3:
        raise ValueError(
            "Not enough valid basketball pose frames were detected."
        )

    # =====================================================
    # 2. YOLO SPORTS BALL DETECTION
    # =====================================================

    model = YOLO(
        "yolo11n.pt"
    )

    cap = cv2.VideoCapture(
        video_path
    )

    if not cap.isOpened():
        raise ValueError(
            "Could not open basketball video."
        )

    original_fps = cap.get(
        cv2.CAP_PROP_FPS
    )

    if original_fps <= 0:
        original_fps = 30.0

    frame_step = max(
        int(
            original_fps
            /
            target_fps
        ),
        1
    )

    frame_index = 0

    analyzed_frames = 0
    ball_detected_frames = 0
    ball_near_player_frames = 0

    pose_frames = pose_result[
        "landmarks"
    ]

    pose_index = 0

    try:

        while True:

            success, frame = cap.read()

            if not success:
                break

            if frame_index % frame_step != 0:
                frame_index += 1
                continue

            analyzed_frames += 1

            # =================================================
            # YOLO DETECTION
            #
            # Lower confidence + higher image size helps detect
            # smaller basketballs in the video.
            # =================================================

            results = model.predict(
                frame,
                verbose=False,
                conf=0.15,
                imgsz=960
            )

            ball_centers = []

            for result in results:

                if result.boxes is None:
                    continue

                for box in result.boxes:

                    class_id = int(
                        box.cls[0]
                    )

                    class_name = model.names[
                        class_id
                    ]

                    # COCO YOLO class name
                    if class_name != "sports ball":
                        continue

                    coordinates = (
                        box.xyxy[0]
                        .cpu()
                        .numpy()
                    )

                    x1, y1, x2, y2 = (
                        coordinates
                    )

                    frame_height, frame_width = (
                        frame.shape[:2]
                    )

                    ball_center = {

                        "x": (
                            (x1 + x2)
                            /
                            2
                        )
                        /
                        frame_width,

                        "y": (
                            (y1 + y2)
                            /
                            2
                        )
                        /
                        frame_height
                    }

                    ball_centers.append(
                        ball_center
                    )

            # =================================================
            # BALL INTERACTION
            # =================================================

            if ball_centers:

                ball_detected_frames += 1

                if pose_index < len(
                    pose_frames
                ):

                    pose_frame = pose_frames[
                        pose_index
                    ]

                    landmarks = pose_frame[
                        "landmarks"
                    ]

                    # Important upper-body points for shooting
                    player_points = [

                        landmarks[
                            "left_wrist"
                        ],

                        landmarks[
                            "right_wrist"
                        ],

                        landmarks[
                            "left_elbow"
                        ],

                        landmarks[
                            "right_elbow"
                        ],

                        landmarks[
                            "left_shoulder"
                        ],

                        landmarks[
                            "right_shoulder"
                        ]
                    ]

                    ball_near_player = False

                    for ball_center in ball_centers:

                        for player_point in player_points:

                            ball_distance = distance(
                                ball_center,
                                player_point
                            )

                            # Slightly larger interaction area
                            # because ball detection boxes can
                            # vary between frames.
                            if ball_distance < 0.30:

                                ball_near_player = True
                                break

                        if ball_near_player:
                            break

                    if ball_near_player:

                        ball_near_player_frames += 1

            pose_index += 1
            frame_index += 1

    finally:

        cap.release()

    # =====================================================
    # 3. YOLO BALL FEATURES
    # =====================================================

    if analyzed_frames > 0:

        ball_detection_rate = (
            ball_detected_frames
            /
            analyzed_frames
        )

        ball_near_player_rate = (
            ball_near_player_frames
            /
            analyzed_frames
        )

    else:

        ball_detection_rate = 0.0

        ball_near_player_rate = 0.0

    ball_features = {

        "ball_detection_rate": (
            ball_detection_rate
        ),

        "ball_near_player_rate": (
            ball_near_player_rate
        )
    }

    # =====================================================
    # 4. FINAL BASKETBALL ANALYSIS
    # =====================================================

    analysis = analyze_basketball(

        features=basketball_features,

        ball_features=ball_features
    )

    # =====================================================
    # 5. POSE QUALITY INFORMATION
    # =====================================================

    analysis["pose_quality"] = {

        "total_video_frames": pose_result[
            "total_frames"
        ],

        "processed_frames": pose_result[
            "processed_frames"
        ],

        "pose_detected_frames": pose_result[
            "pose_detected_frames"
        ],

        "detection_rate": pose_result[
            "detection_rate"
        ],

        "original_fps": pose_result[
            "original_fps"
        ],

        "analysis_fps": pose_result[
            "target_fps"
        ]
    }

    return analysis