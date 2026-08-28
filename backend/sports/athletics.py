def clamp(value, minimum=0.0, maximum=100.0):
    return max(
        minimum,
        min(
            maximum,
            value
        )
    )


def normalize(value, low, high):
    """
    Convert a measured value into a prototype 0-100 scale.

    These ranges are engineering prototype ranges only.
    They are not scientifically validated athletics thresholds.
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


def analyze_athletics(features):
    """
    Prototype sprint-performance analysis.

    The scores are heuristic estimates based on
    pose-derived image-space measurements.

    This is not a scientifically validated
    athletics performance test.
    """

    # --------------------------------------------------
    # GET FEATURES
    # --------------------------------------------------

    average_speed = features.get(
        "average_movement_speed",
        0.0
    )

    maximum_speed = features.get(
        "maximum_movement_speed",
        0.0
    )

    movement_consistency = features.get(
        "movement_consistency",
        0.0
    )

    average_ankle_separation = features.get(
        "average_ankle_separation",
        0.0
    )

    maximum_ankle_separation = features.get(
        "maximum_ankle_separation",
        0.0
    )

    average_knee_drive = features.get(
        "average_knee_drive",
        0.0
    )

    maximum_knee_drive = features.get(
        "maximum_knee_drive",
        0.0
    )

    left_knee_angle = features.get(
        "average_left_knee_angle",
        0.0
    )

    right_knee_angle = features.get(
        "average_right_knee_angle",
        0.0
    )

    left_elbow_angle = features.get(
        "average_left_elbow_angle",
        0.0
    )

    right_elbow_angle = features.get(
        "average_right_elbow_angle",
        0.0
    )

    leg_symmetry_difference = features.get(
        "leg_symmetry_difference",
        0.0
    )

    body_center_offset = features.get(
        "average_body_center_offset",
        0.0
    )

    shoulder_tilt = features.get(
        "average_shoulder_tilt",
        0.0
    )

    hip_tilt = features.get(
        "average_hip_tilt",
        0.0
    )

    valid_frames = features.get(
        "valid_athletics_frames",
        0
    )

    # --------------------------------------------------
    # MOVEMENT CONSISTENCY
    # --------------------------------------------------

    if movement_consistency <= 1.0:
        consistency_score = clamp(
            movement_consistency * 100
        )
    else:
        consistency_score = clamp(
            movement_consistency
        )

    # --------------------------------------------------
    # KNEE DRIVE SCORE
    # --------------------------------------------------

    average_knee_score = normalize(
        average_knee_drive,
        0.01,
        0.12
    )

    maximum_knee_score = normalize(
        maximum_knee_drive,
        0.03,
        0.20
    )

    knee_drive_score = (
        average_knee_score * 0.60
        +
        maximum_knee_score * 0.40
    )

    # --------------------------------------------------
    # STRIDE QUALITY
    # --------------------------------------------------

    average_stride_score = normalize(
        average_ankle_separation,
        0.05,
        0.30
    )

    maximum_stride_score = normalize(
        maximum_ankle_separation,
        0.10,
        0.45
    )

    symmetry_score = (
        100
        - normalize(
            leg_symmetry_difference,
            0,
            35
        )
    )

    stride_quality_score = (
        average_stride_score * 0.40
        +
        maximum_stride_score * 0.35
        +
        symmetry_score * 0.25
    )

    # --------------------------------------------------
    # ARM MOVEMENT
    # --------------------------------------------------

    elbow_difference = abs(
        left_elbow_angle
        - right_elbow_angle
    )

    arm_symmetry_score = (
        100
        - normalize(
            elbow_difference,
            0,
            50
        )
    )

    average_elbow_angle = (
        left_elbow_angle
        + right_elbow_angle
    ) / 2

    elbow_position_score = (
        100
        - normalize(
            abs(
                average_elbow_angle
                - 100
            ),
            0,
            70
        )
    )

    arm_movement_score = (
        arm_symmetry_score * 0.55
        +
        elbow_position_score * 0.45
    )

    # --------------------------------------------------
    # BODY POSTURE
    # --------------------------------------------------

    center_score = (
        100
        - normalize(
            body_center_offset,
            0.03,
            0.30
        )
    )

    shoulder_score = (
        100
        - normalize(
            shoulder_tilt,
            0.0,
            0.08
        )
    )

    hip_score = (
        100
        - normalize(
            hip_tilt,
            0.0,
            0.08
        )
    )

    body_posture_score = (
        center_score * 0.40
        +
        shoulder_score * 0.30
        +
        hip_score * 0.30
    )

    # --------------------------------------------------
    # BALANCE
    # --------------------------------------------------

    balance_score = (
        center_score * 0.50
        +
        symmetry_score * 0.30
        +
        hip_score * 0.20
    )

    # --------------------------------------------------
    # RUNNING TECHNIQUE
    # --------------------------------------------------

    speed_score = (
        normalize(
            average_speed,
            0.05,
            0.50
        ) * 0.60
        +
        normalize(
            maximum_speed,
            0.10,
            1.20
        ) * 0.40
    )

    running_technique_score = (
        knee_drive_score * 0.20
        +
        stride_quality_score * 0.20
        +
        arm_movement_score * 0.15
        +
        body_posture_score * 0.20
        +
        balance_score * 0.10
        +
        speed_score * 0.15
    )

    # --------------------------------------------------
    # COMPONENT SCORES
    # --------------------------------------------------

    components = {
        "running_technique": round(
            running_technique_score,
            1
        ),

        "knee_drive": round(
            knee_drive_score,
            1
        ),

        "stride_quality": round(
            stride_quality_score,
            1
        ),

        "arm_movement": round(
            arm_movement_score,
            1
        ),

        "body_posture": round(
            body_posture_score,
            1
        ),

        "balance": round(
            balance_score,
            1
        ),

        "movement_consistency": round(
            consistency_score,
            1
        )
    }

    # --------------------------------------------------
    # OVERALL SCORE
    # --------------------------------------------------

    overall_score = round(
        sum(
            components.values()
        )
        / len(
            components
        ),
        1
    )

    # --------------------------------------------------
    # STRENGTHS
    # --------------------------------------------------

    strengths = []

    for component, score in components.items():

        if score >= 70:

            readable_name = component.replace(
                "_",
                " "
            )

            strengths.append(
                f"Relatively strong {readable_name} "
                f"in this prototype sprint analysis."
            )

    # --------------------------------------------------
    # WEAKNESSES
    # --------------------------------------------------

    weaknesses = []

    for component, score in components.items():

        if score < 50:

            readable_name = component.replace(
                "_",
                " "
            )

            weaknesses.append(
                f"{readable_name.capitalize()} "
                f"was relatively lower in this sprint analysis."
            )

    # --------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------

    recommendations = []

    if components["running_technique"] < 60:
        recommendations.append(
            "Practice controlled sprint drills focusing on coordinated full-body movement."
        )

    if components["knee_drive"] < 60:
        recommendations.append(
            "Practice high-knee drills and sprint starts to improve knee drive."
        )

    if components["stride_quality"] < 60:
        recommendations.append(
            "Practice stride drills while maintaining controlled and balanced steps."
        )

    if components["arm_movement"] < 60:
        recommendations.append(
            "Focus on coordinated forward-backward arm movement while sprinting."
        )

    if components["body_posture"] < 60:
        recommendations.append(
            "Maintain a stable torso and controlled forward body position during sprinting."
        )

    if components["balance"] < 60:
        recommendations.append(
            "Include single-leg balance and running stability exercises."
        )

    if components["movement_consistency"] < 60:
        recommendations.append(
            "Repeat short sprint drills while trying to maintain a consistent running pattern."
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
            "Continue structured sprint practice and upload more videos for progress comparison."
        )

    # --------------------------------------------------
    # METRICS
    # --------------------------------------------------

    metrics = {
        "average_movement_speed": round(
            average_speed,
            4
        ),

        "maximum_movement_speed": round(
            maximum_speed,
            4
        ),

        "average_stride_ankle_separation": round(
            average_ankle_separation,
            4
        ),

        "maximum_stride_ankle_separation": round(
            maximum_ankle_separation,
            4
        ),

        "average_knee_drive": round(
            average_knee_drive,
            4
        ),

        "maximum_knee_drive": round(
            maximum_knee_drive,
            4
        ),

        "left_right_symmetry": round(
            symmetry_score,
            1
        ),

        "valid_athletics_frames": valid_frames
    }

    # --------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------

    return {
        "success": True,

        "sport": "athletics",

        "analysis_type": "sprint",

        "analysis_mode": (
            "prototype_heuristic"
        ),

        "warning": (
            "Athletics scores are experimental heuristic estimates "
            "derived from pose measurements. Movement speed and stride "
            "measurements are normalized image-space values and are not "
            "real-world meters, meters per second, or km/h."
        ),

        "overall_score": overall_score,

        "components": components,

        "metrics": metrics,

        "strengths": strengths,

        "weaknesses": weaknesses,

        "recommendations": recommendations,

        "features": features
    }