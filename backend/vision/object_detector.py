from ultralytics import YOLO


class ObjectDetector:
    """
    Reusable YOLO object detector.

    For Football Phase 1 we use a pretrained YOLO model
    and look for the COCO class: "sports ball".

    This is not a custom football detector.
    """

    def __init__(
        self,
        model_name="yolo11n.pt",
        confidence_threshold=0.25
    ):
        self.model_name = model_name
        self.confidence_threshold = confidence_threshold

        self.model = YOLO(
            model_name
        )

    def detect_sports_ball(
        self,
        frame
    ):
        """
        Detect sports balls in one video frame.

        Returns a list of detections.

        Each detection contains:
        - confidence
        - bounding box
        - normalized center point
        """

        results = self.model.predict(
            source=frame,
            conf=self.confidence_threshold,
            verbose=False
        )

        detections = []

        if not results:
            return detections

        result = results[0]

        if result.boxes is None:
            return detections

        frame_height = frame.shape[0]
        frame_width = frame.shape[1]

        names = result.names

        for box in result.boxes:
            class_id = int(
                box.cls[0].item()
            )

            class_name = names[
                class_id
            ]

            if class_name != "sports ball":
                continue

            confidence = float(
                box.conf[0].item()
            )

            x1, y1, x2, y2 = (
                box.xyxy[0]
                .cpu()
                .tolist()
            )

            center_x = (
                (x1 + x2) / 2
            )

            center_y = (
                (y1 + y2) / 2
            )

            normalized_center_x = (
                center_x / frame_width
            )

            normalized_center_y = (
                center_y / frame_height
            )

            detections.append({
                "class_name": "sports ball",

                "confidence": round(
                    confidence,
                    4
                ),

                "bbox": {
                    "x1": round(
                        float(x1),
                        2
                    ),
                    "y1": round(
                        float(y1),
                        2
                    ),
                    "x2": round(
                        float(x2),
                        2
                    ),
                    "y2": round(
                        float(y2),
                        2
                    )
                },

                "center": {
                    "x": round(
                        normalized_center_x,
                        5
                    ),
                    "y": round(
                        normalized_center_y,
                        5
                    )
                }
            })

        return detections