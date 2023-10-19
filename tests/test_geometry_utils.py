from importer import *

from gplates_ws_proxy import geometry_utils


def test_cross_dateline():
    # print(subduction_teeth.test_line_segment_cross_dateline_in_degrees(45, 56, 0))
    # print(subduction_teeth.test_line_segment_cross_dateline_in_degrees(170, -170, 0))
    print(
        geometry_utils.test_line_segment_cross_dateline(
            -3.1185386445524252, 3.1306819004686584, 0
        )
    )
    print(
        geometry_utils.test_line_segment_cross_dateline(
            3.141592653589793, 3.087522261495965, 0
        )  # 3.104774484150127
    )


if __name__ == "__main__":
    test_cross_dateline()
