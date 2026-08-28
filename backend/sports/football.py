def clamp(value, minimum=0.0, maximum=100.0):
    return max(minimum, min(maximum, value))


def normalize(value, low, high):
    """
    Convert a measured value to a prototype 0-100 scale.

    These ranges are engineering prototype ranges only.
    They are NOT scientifically validated football thresholds.
    """

    if value is None:
        return 0.0

    if high == low:
        return 0.0

    score = (
        (value - low)
        / (high - low)
        * 100
    )

    return clamp(score)


def analyze_football(
    features,
    running_features=None,
    ball_control_features=None,
    kicking_features=None,
    kick_events=None,
    **kwargs
):
    """
    Prototype football performance analysis.

    AI/computer vision extracts measurable features.
    Transparent heuristic rules convert those features
    into prototype performance scores.

    These scores are not scientifically validated
    talent predictions.
    """

    if running_features is None:
        running_features = {}

    if ball_control_features is None:
        ball_control_features = {}

    if kicking_features is None:
        kicking_features = {}

    # --------------------------------------------------
    # BASIC FEATURES
    # --------------------------------------------------

    average_speed = features.get(
        "average_movement_speed",
        0
    )

    maximum_speed = features.get(
        "maximum_movement_speed",
        0
    )

    movement_consistency = features.get(
        "movement_consistency",
        0
    )

    body_center_offset = features.get(
        "average_body_center_offset",
        0
    )

    shoulder_tilt = features.get(
        "average_shoulder_tilt",
        0
    )

    hip_tilt = features.get(
        "average_hip_tilt",
        0
    )

    left_knee = features.get(
        "left_knee",
        {}
    )

    right_knee = features.get(
        "right_knee",
        {}
    )

    ball_detection_rate = features.get(
        "ball_detection_rate",
        0
    )

    minimum_player_ball_distance = features.get(
        "minimum_player_ball_distance"
    )

    average_ball_displacement = features.get(
        "average_ball_displacement",
        0
    )

    # --------------------------------------------------
    # MOVEMENT SCORE
    # --------------------------------------------------

    movement_score = (
        normalize(
            average_speed,
            0.05,
            0.50
        ) * 0.65
        +
        normalize(
            maximum_speed,
            0.10,
            1.20
        ) * 0.35
    )

    # --------------------------------------------------
    # LOWER BODY TECHNIQUE
    # --------------------------------------------------

    lower_body_score = (
        normalize(
            left_knee.get("range"),
            20,
            120
        ) * 0.35
        +
        normalize(
            right_knee.get("range"),
            20,
            120
        ) * 0.35
        +
        clamp(
            movement_consistency * 100
        ) * 0.30
    )

    # --------------------------------------------------
    # BALANCE
    # --------------------------------------------------

    offset_score = 100 - normalize(
        body_center_offset,
        0.05,
        0.35
    )

    shoulder_score = 100 - normalize(
        shoulder_tilt,
        0.0,
        0.08
    )

    hip_score = 100 - normalize(
        hip_tilt,
        0.0,
        0.08
    )

    balance_score = (
        offset_score * 0.40
        +
        shoulder_score * 0.30
        +
        hip_score * 0.30
    )

    # --------------------------------------------------
    # BALL INTERACTION
    # --------------------------------------------------

    detection_score = clamp(
        ball_detection_rate * 100
    )

    if minimum_player_ball_distance is not None:
        proximity_score = (
            100
            - normalize(
                minimum_player_ball_distance,
                0.02,
                0.50
            )
        )
    else:
        proximity_score = 0.0

    ball_motion_score = normalize(
        average_ball_displacement,
        0.01,
        0.25
    )

    ball_interaction_score = (
        detection_score * 0.40
        +
        proximity_score * 0.35
        +
        ball_motion_score * 0.25
    )

    if ball_detection_rate < 0.30:
        ball_interaction_score *= 0.60

    # --------------------------------------------------
    # CONSISTENCY
    # --------------------------------------------------

    consistency_score = clamp(
        movement_consistency * 100
    )

    # --------------------------------------------------
    # RUNNING ABILITY
    # --------------------------------------------------

    running_average_speed = running_features.get(
        "average_running_speed",
        0
    )

    running_maximum_speed = running_features.get(
        "maximum_running_speed",
        0
    )

    running_variability = running_features.get(
        "running_speed_variability",
        0
    )

    running_speed_score = normalize(
        running_average_speed,
        0.05,
        0.50
    )

    running_max_score = normalize(
        running_maximum_speed,
        0.10,
        1.20
    )

    running_consistency_score = (
        100
        - normalize(
            running_variability,
            0.0,
            0.50
        )
    )

    running_ability_score = (
        running_speed_score * 0.45
        +
        running_max_score * 0.30
        +
        running_consistency_score * 0.25
    )

    # --------------------------------------------------
    # BALL CONTROL
    # --------------------------------------------------

    close_control_ratio = ball_control_features.get(
        "close_control_ratio",
        0
    )

    average_ball_foot_distance = ball_control_features.get(
        "average_ball_foot_distance"
    )

    minimum_ball_foot_distance = ball_control_features.get(
        "minimum_ball_foot_distance"
    )

    close_control_score = clamp(
        close_control_ratio * 100
    )

    if average_ball_foot_distance is not None:
        average_distance_score = (
            100
            - normalize(
                average_ball_foot_distance,
                0.05,
                0.50
            )
        )
    else:
        average_distance_score = 0.0

    if minimum_ball_foot_distance is not None:
        minimum_distance_score = (
            100
            - normalize(
                minimum_ball_foot_distance,
                0.02,
                0.30
            )
        )
    else:
        minimum_distance_score = 0.0

    ball_control_score = (
        close_control_score * 0.50
        +
        average_distance_score * 0.30
        +
        minimum_distance_score * 0.20
    )

    # --------------------------------------------------
    # KICKING POSTURE
    # --------------------------------------------------

    kicking_left_knee = kicking_features.get(
        "average_left_knee_angle",
        0
    )

    kicking_right_knee = kicking_features.get(
        "average_right_knee_angle",
        0
    )

    kicking_shoulder_tilt = kicking_features.get(
        "average_shoulder_tilt",
        0
    )

    kicking_hip_tilt = kicking_features.get(
        "average_hip_tilt",
        0
    )

    ankle_height_difference = kicking_features.get(
        "maximum_ankle_height_difference",
        0
    )

    knee_difference = abs(
        kicking_left_knee
        - kicking_right_knee
    )

    knee_symmetry_score = (
        100
        - normalize(
            knee_difference,
            0,
            50
        )
    )

    kicking_balance_score = (
        (
            100
            - normalize(
                kicking_shoulder_tilt,
                0,
                0.10
            )
        )
        +
        (
            100
            - normalize(
                kicking_hip_tilt,
                0,
                0.10
            )
        )
    ) / 2

    leg_action_score = normalize(
        ankle_height_difference,
        0.02,
        0.20
    )

    kicking_posture_score = (
        knee_symmetry_score * 0.35
        +
        kicking_balance_score * 0.40
        +
        leg_action_score * 0.25
    )

    # --------------------------------------------------
    # COMPONENT SCORES
    # --------------------------------------------------

    components = {
        "movement": round(
            movement_score,
            1
        ),

        "lower_body_technique": round(
            lower_body_score,
            1
        ),

        "balance": round(
            balance_score,
            1
        ),

        "ball_interaction": round(
            ball_interaction_score,
            1
        ),

        "consistency": round(
            consistency_score,
            1
        ),

        "running_ability": round(
            running_ability_score,
            1
        ),

        "ball_control": round(
            ball_control_score,
            1
        ),

        "kicking_posture": round(
            kicking_posture_score,
            1
        )
    }

    overall_score = round(
        sum(components.values())
        / len(components),
        1
    )

    # --------------------------------------------------
    # STRENGTHS / WEAKNESSES
    # --------------------------------------------------

    strengths = []
    weaknesses = []

    for component, score in components.items():

        readable_name = component.replace(
            "_",
            " "
        )

        if score >= 70:
            strengths.append(
                f"Relatively strong {readable_name} "
                f"in this prototype analysis."
            )

        elif score < 50:
            weaknesses.append(
                f"{readable_name.capitalize()} "
                f"was relatively lower in this analysis."
            )

    # --------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------

    recommendations = []

    if components["movement"] < 60:
        recommendations.append(
            "Practice short acceleration and change-of-direction drills."
        )

    if components["lower_body_technique"] < 60:
        recommendations.append(
            "Practice controlled lower-body movement, stance changes, and kicking preparation."
        )

    if components["balance"] < 60:
        recommendations.append(
            "Include stability, landing, and single-leg control exercises."
        )

    if components["ball_interaction"] < 60:
        recommendations.append(
            "Practice repeated ball-contact and close-control drills."
        )

    if components["consistency"] < 60:
        recommendations.append(
            "Focus on maintaining consistent movement patterns during repeated drills."
        )

    if components["running_ability"] < 60:
        recommendations.append(
            "Practice acceleration, sprint mechanics, and controlled running drills."
        )

    if components["ball_control"] < 60:
        recommendations.append(
            "Practice close dribbling and keeping the ball closer to both feet."
        )

    if components["kicking_posture"] < 60:
        recommendations.append(
            "Practice controlled kicking posture with stable hips, shoulders, and supporting leg."
        )

    if not strengths:
        strengths.append(
            "No component crossed the prototype strength threshold."
        )

    if not weaknesses:
        weaknesses.append(
            "No major weakness was identified by the prototype rules."
        )

    if not recommendations:
        recommendations.append(
            "Continue structured football practice and collect more videos for progress comparison."
        )

    # --------------------------------------------------
    # KICK EVENTS
    # --------------------------------------------------

    kick_events_detected = 0

    if isinstance(kick_events, int):
        kick_events_detected = kick_events

    elif isinstance(kick_events, list):
        kick_events_detected = len(
            kick_events
        )

    elif isinstance(kick_events, dict):
        kick_events_detected = kick_events.get(
            "kick_events_detected",
            kick_events.get(
                "count",
                0
            )
        )

    # --------------------------------------------------
    # RESULT
    # --------------------------------------------------

    return {
        "success": True,

        "sport": "football",

        "analysis_mode": (
            "prototype_heuristic"
        ),

        "warning": (
            "Scores are experimental heuristic estimates "
            "based on pose and pretrained sports-ball detection. "
            "They are not validated talent predictions, and "
            "movement is measured in image space rather than "
            "real-world speed."
        ),

        "overall_score": overall_score,

        "components": components,

        "kick_events_detected": (
            kick_events_detected
        ),

        "strengths": strengths,

        "weaknesses": weaknesses,

        "recommendations": recommendations,

        "features": features,

        "running_features": (
            running_features
        ),

        "ball_control_features": (
            ball_control_features
        ),

        "kicking_features": (
            kicking_features
        )
    }