def clamp(value, minimum=0.0, maximum=100.0):
    return max(minimum, min(maximum, value))


def normalize(value, low, high):
    """
    Convert a measured value to a temporary 0-100 prototype scale.

    These ranges are engineering prototype ranges only.
    They are NOT scientifically validated badminton thresholds.
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


def analyze_badminton(features):
    """
    Prototype badminton analysis.

    IMPORTANT:
    This does not determine natural talent.

    The scores are heuristic estimates based on
    video-derived measurements.
    """

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
        "average_body_center_offset"
    )

    shoulder_tilt = features.get(
        "average_shoulder_tilt"
    )

    hip_tilt = features.get(
        "average_hip_tilt"
    )

    left_knee = features.get(
        "left_knee",
        {}
    )

    right_knee = features.get(
        "right_knee",
        {}
    )

    left_elbow = features.get(
        "left_elbow",
        {}
    )

    right_elbow = features.get(
        "right_elbow",
        {}
    )

    # --------------------------------------------------
    # MOVEMENT
    #
    # Uses time-normalized speed features instead of
    # raw total movement distance so frame sampling
    # affects the result less.
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
    # FOOTWORK
    #
    # Uses knee movement range + consistency.
    # Avoids raw movement distance.
    # --------------------------------------------------

    footwork_score = (
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
    # UPPER BODY
    # --------------------------------------------------

    upper_body_score = (
        normalize(
            left_elbow.get("range"),
            20,
            150
        ) * 0.50
        +
        normalize(
            right_elbow.get("range"),
            20,
            150
        ) * 0.50
    )

    # --------------------------------------------------
    # CONSISTENCY
    # --------------------------------------------------

    consistency_score = clamp(
        movement_consistency * 100
    )

    components = {
        "footwork": round(
            footwork_score,
            1
        ),

        "movement": round(
            movement_score,
            1
        ),

        "balance": round(
            balance_score,
            1
        ),

        "upper_body_technique": round(
            upper_body_score,
            1
        ),

        "consistency": round(
            consistency_score,
            1
        )
    }

    overall_score = round(
        sum(components.values())
        / len(components),
        1
    )

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

    recommendations = []

    if components["footwork"] < 60:
        recommendations.append(
            "Practice controlled lateral footwork and recovery steps."
        )

    if components["movement"] < 60:
        recommendations.append(
            "Practice short movement drills with controlled direction changes."
        )

    if components["balance"] < 60:
        recommendations.append(
            "Include stability and controlled landing exercises."
        )

    if components["upper_body_technique"] < 60:
        recommendations.append(
            "Practice controlled shadow swings while maintaining consistent shoulder and elbow movement."
        )

    if components["consistency"] < 60:
        recommendations.append(
            "Use repeated controlled drills and focus on maintaining similar movement patterns."
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
            "Continue structured practice and collect more videos for comparison."
        )

    return {
        "success": True,

        "sport": "badminton",

        "analysis_mode": "prototype_heuristic",

        "warning": (
            "Scores are experimental heuristic estimates based on "
            "video-derived measurements. They are not validated "
            "talent predictions."
        ),

        "overall_score": overall_score,

        "components": components,

        "strengths": strengths,

        "weaknesses": weaknesses,

        "recommendations": recommendations,

        "features": features
    }