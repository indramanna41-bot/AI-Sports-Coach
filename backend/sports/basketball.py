def clamp(
    value,
    minimum=0.0,
    maximum=100.0
):
    return max(
        minimum,
        min(
            maximum,
            value
        )
    )


def normalize(
    value,
    low,
    high
):
    if high == low:
        return 0.0

    score = (
        (value - low)
        /
        (high - low)
    ) * 100

    return clamp(score)


def analyze_basketball(
    features,
    ball_features=None
):

    if ball_features is None:
        ball_features = {}

    # =====================================================
    # READ POSE FEATURES
    # =====================================================

    maximum_vertical_movement = (
        features.get(
            "maximum_vertical_movement",
            0.0
        )
    )

    average_vertical_movement = (
        features.get(
            "average_vertical_movement",
            0.0
        )
    )

    jump_events = features.get(
        "jump_events_detected",
        0
    )

    arm_difference = features.get(
        "average_arm_difference",
        0.0
    )

    body_center_offset = features.get(
        "average_body_center_offset",
        0.0
    )

    movement_variability = features.get(
        "movement_variability",
        0.0
    )

    valid_frames = features.get(
        "valid_basketball_frames",
        0
    )

    # =====================================================
    # YOLO BALL FEATURES
    # =====================================================

    ball_detection_rate = (
        ball_features.get(
            "ball_detection_rate",
            0.0
        )
    )

    ball_near_player_rate = (
        ball_features.get(
            "ball_near_player_rate",
            0.0
        )
    )

    # =====================================================
    # JUMP TECHNIQUE
    # =====================================================

    vertical_score = normalize(
        maximum_vertical_movement,
        0.01,
        0.12
    )

    average_vertical_score = normalize(
        average_vertical_movement,
        0.005,
        0.07
    )

    if jump_events > 0:
        jump_event_score = 80.0
    else:
        jump_event_score = 30.0

    jump_technique_score = (
        vertical_score * 0.45
        +
        average_vertical_score * 0.25
        +
        jump_event_score * 0.30
    )

    # =====================================================
    # ARM COORDINATION
    # Smaller difference = better symmetry
    # =====================================================

    arm_coordination_score = (
        100
        -
        normalize(
            arm_difference,
            0.01,
            0.18
        )
    )

    # =====================================================
    # BALANCE
    # =====================================================

    balance_score = (
        100
        -
        normalize(
            body_center_offset,
            0.01,
            0.22
        )
    )

    # =====================================================
    # MOVEMENT CONSISTENCY
    # =====================================================

    movement_consistency_score = (
        100
        -
        normalize(
            movement_variability,
            0.005,
            0.10
        )
    )

    # =====================================================
    # BALL INTERACTION
    # YOLO-based prototype score
    # =====================================================

    ball_detection_score = clamp(
        ball_detection_rate
        * 100
    )

    ball_near_player_score = clamp(
        ball_near_player_rate
        * 100
    )

    ball_interaction_score = (
        ball_detection_score
        * 0.40
        +
        ball_near_player_score
        * 0.60
    )

    # =====================================================
    # COMPONENT SCORES
    # =====================================================

    components = {

        "ball_interaction": round(
            ball_interaction_score,
            1
        ),

        "jump_technique": round(
            jump_technique_score,
            1
        ),

        "arm_coordination": round(
            arm_coordination_score,
            1
        ),

        "balance": round(
            balance_score,
            1
        ),

        "movement_consistency": round(
            movement_consistency_score,
            1
        )
    }

    overall_score = round(
        sum(
            components.values()
        )
        /
        len(components),
        1
    )

    # =====================================================
    # STRENGTHS / WEAKNESSES
    # =====================================================

    strengths = []
    weaknesses = []

    for component, score in (
        components.items()
    ):

        readable_name = (
            component.replace(
                "_",
                " "
            )
        )

        if score >= 70:

            strengths.append(
                f"Relatively strong "
                f"{readable_name} "
                f"in this basketball analysis."
            )

        elif score < 50:

            weaknesses.append(
                f"{readable_name.capitalize()} "
                f"was relatively lower "
                f"in this basketball analysis."
            )

    # =====================================================
    # RECOMMENDATIONS
    # =====================================================

    recommendations = []

    if components[
        "ball_interaction"
    ] < 60:

        recommendations.append(
            "Practice controlled ball-handling "
            "and shooting drills."
        )

    if components[
        "jump_technique"
    ] < 60:

        recommendations.append(
            "Practice controlled jump-shot "
            "and vertical jump drills."
        )

    if components[
        "arm_coordination"
    ] < 60:

        recommendations.append(
            "Focus on coordinated arm movement "
            "during shooting and ball control."
        )

    if components[
        "balance"
    ] < 60:

        recommendations.append(
            "Practice balanced shooting stance "
            "and landing control."
        )

    if components[
        "movement_consistency"
    ] < 60:

        recommendations.append(
            "Repeat basketball movement drills "
            "with a consistent movement pattern."
        )

    if not strengths:

        strengths.append(
            "No component crossed the "
            "prototype strength threshold."
        )

    if not weaknesses:

        weaknesses.append(
            "No major weakness was identified "
            "by the prototype rules."
        )

    if not recommendations:

        recommendations.append(
            "Continue structured basketball "
            "practice and upload more videos "
            "for progress comparison."
        )

    # =====================================================
    # ONLY METRIC USER REQUESTED
    # =====================================================

    metrics = {
        "jump_events_detected": (
            jump_events
        )
    }

    return {

        "success": True,

        "sport": "basketball",

        "analysis_mode": (
            "prototype_heuristic"
        ),

        "warning": (
            "Basketball scores are experimental "
            "heuristic estimates derived from "
            "pose and sports-ball detection."
        ),

        "overall_score": (
            overall_score
        ),

        "components": (
            components
        ),

        "metrics": (
            metrics
        ),

        "strengths": (
            strengths
        ),

        "weaknesses": (
            weaknesses
        ),

        "recommendations": (
            recommendations
        ),

        "features": (
            features
        )
    }