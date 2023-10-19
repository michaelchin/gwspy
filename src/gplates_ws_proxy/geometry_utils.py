import math


def test_line_segment_cross_dateline_in_degrees(
    point_a_lon, point_b_lon, central_meridian
):
    """same as test_line_segment_cross_dateline except all arguments are in degrees"""
    return test_line_segment_cross_dateline(
        math.radians(point_a_lon),
        math.radians(point_b_lon),
        math.radians(central_meridian),
    )


def test_line_segment_cross_dateline(point_a_lon, point_b_lon, central_meridian):
    """Return True if the line segment cross dateline, otherwise False.
    All parameters are in radians.
    """
    half_pi = math.pi / 2
    dateline_lon = central_meridian + math.pi

    a_to_dateline = abs(point_a_lon - dateline_lon) % (math.pi * 2)
    b_to_dateline = abs(point_b_lon - dateline_lon) % (math.pi * 2)
    a_to_b = abs(point_a_lon - point_b_lon) % (math.pi * 2)

    assert not math.isclose(
        a_to_b, math.pi
    )  # two points are 180 degree apart along longitude axis. cannot decide if cross dateline

    if a_to_dateline > math.pi:
        a_to_dateline = 2 * math.pi - a_to_dateline
    if b_to_dateline > math.pi:
        b_to_dateline = 2 * math.pi - b_to_dateline
    if a_to_b > math.pi:
        a_to_b = 2 * math.pi - a_to_b

    # print(a_to_dateline, b_to_dateline, a_to_b)

    if math.isclose(a_to_dateline, 0.0) or math.isclose(b_to_dateline, 0.0):
        # print(point_a_lon, point_b_lon)
        if abs(point_a_lon - point_b_lon) < math.pi:
            return False
        else:
            return True

    if math.isclose(a_to_dateline + b_to_dateline, a_to_b):
        return True

    if a_to_dateline + b_to_dateline > a_to_b:
        return False
    else:
        return True
