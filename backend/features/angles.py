import math
import statistics


def calculate_angle(point_a, point_b, point_c):
    """
    Calculate angle ABC in degrees.
    point_b is the joint where the angle is measured.
    """

    ax = point_a["x"]
    ay = point_a["y"]

    bx = point_b["x"]
    by = point_b["y"]

    cx = point_c["x"]
    cy = point_c["y"]

    vector_ba = (
        ax - bx,
        ay - by
    )

    vector_bc = (
        cx - bx,
        cy - by
    )

    dot_product = (
        vector_ba[0] * vector_bc[0]
        + vector_ba[1] * vector_bc[1]
    )

    magnitude_ba = math.sqrt(
        vector_ba[0] ** 2
        + vector_ba[1] ** 2
    )

    magnitude_bc = math.sqrt(
        vector_bc[0] ** 2
        + vector_bc[1] ** 2
    )

    if magnitude_ba == 0 or magnitude_bc == 0:
        return None

    cosine_angle = dot_product / (
        magnitude_ba * magnitude_bc
    )

    cosine_angle = max(
        -1.0,
        min(1.0, cosine_angle)
    )

    angle_radians = math.acos(
        cosine_angle
    )

    angle_degrees = math.degrees(
        angle_radians
    )

    return round(angle_degrees, 2)


def remove_outliers(angle_values, threshold=3.5):
    """
    Remove statistical outliers using Median Absolute Deviation.

    This is not a sports-performance threshold.
    It is only used to reduce obvious pose-estimation spikes.
    """

    valid_angles = [
        angle
        for angle in angle_values
        if angle is not None
    ]

    if len(valid_angles) < 5:
        return valid_angles

    median_value = statistics.median(
        valid_angles
    )

    deviations = [
        abs(angle - median_value)
        for angle in valid_angles
    ]

    median_deviation = statistics.median(
        deviations
    )

    if median_deviation == 0:
        return valid_angles

    filtered_angles = []

    for angle in valid_angles:

        modified_z_score = (
            0.6745
            * abs(angle - median_value)
            / median_deviation
        )

        if modified_z_score <= threshold:
            filtered_angles.append(angle)

    return filtered_angles


def summarize_angles(angle_values):
    """
    Calculate basic statistics after removing
    obvious statistical outliers.
    """

    filtered_angles = remove_outliers(
        angle_values
    )

    if not filtered_angles:
        return {
            "average": None,
            "minimum": None,
            "maximum": None,
            "range": None,
            "samples": 0
        }

    average_angle = (
        sum(filtered_angles)
        / len(filtered_angles)
    )

    minimum_angle = min(
        filtered_angles
    )

    maximum_angle = max(
        filtered_angles
    )

    angle_range = (
        maximum_angle
        - minimum_angle
    )

    return {
        "average": round(
            average_angle,
            2
        ),
        "minimum": round(
            minimum_angle,
            2
        ),
        "maximum": round(
            maximum_angle,
            2
        ),
        "range": round(
            angle_range,
            2
        ),
        "samples": len(
            filtered_angles
        )
    }