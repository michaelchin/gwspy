import math

from utils import *

from gwspy import geometry_utils


def test_cross_dateline():
    assert (
        geometry_utils.test_line_segment_cross_dateline_in_degrees(45, 56, 0) == False
    )
    assert (
        geometry_utils.test_line_segment_cross_dateline_in_degrees(170, -170, 0) == True
    )
    assert (
        geometry_utils.test_line_segment_cross_dateline(
            -3.1185386445524252, 3.1306819004686584, 0
        )
        == True
    )

    assert (
        geometry_utils.test_line_segment_cross_dateline(
            3.141592653589793, 3.087522261495965, 0
        )
        == False
    )
    assert (
        geometry_utils.test_line_segment_cross_dateline(
            -3.141592653589793, 3.087522261495965, 0
        )
        == True
    )


def test_intersection_of_great_circles():
    intersections = geometry_utils.find_two_great_circles_intersections(
        {"lon": 0, "lat": 0},
        {"lon": 0, "lat": 90},
        {"lon": 0, "lat": 0},
        {"lon": 90, "lat": 0},
    )
    assert math.isclose(intersections[0]["lat"], 0)
    assert math.isclose(intersections[0]["lon"], 180)
    assert math.isclose(intersections[1]["lat"], 0)
    assert math.isclose(intersections[1]["lon"], 0)
    print(intersections)
    intersections = geometry_utils.find_two_great_circles_intersections(
        {"lon": -35.8744, "lat": 13.9450},
        {"lon": 20.6730, "lat": 4.6999},
        {"lon": 1.5714, "lat": 28.5002},
        {"lon": -16.5855, "lat": -4.9771},
    )
    print(intersections)
    assert math.isclose(intersections[0]["lat"], -10.804293538655628)
    assert math.isclose(intersections[0]["lon"], 171.3465458795531)
    assert math.isclose(intersections[1]["lat"], 10.804293538655628)
    assert math.isclose(intersections[1]["lon"], -8.653454120446886)


if __name__ == "__main__":
    test_cross_dateline()
    test_intersection_of_great_circles()
