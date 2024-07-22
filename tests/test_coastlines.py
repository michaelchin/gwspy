from utils import logger

import gwspy


def test_coastlines():
    r = gwspy.get_paleo_coastlines(100)
    print(r)

    r = gwspy.get_paleo_coastlines(100, format="shapely")
    print(r)
