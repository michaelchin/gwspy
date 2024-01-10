from utils import logger

import gplates_ws_proxy


def test_coastlines():
    r = gplates_ws_proxy.get_paleo_coastlines(100)
    print(r)

    r = gplates_ws_proxy.get_paleo_coastlines(100, format="shapely")
    print(r)
