from importer import *


def test_coastlines():
    r = gplates.get_paleo_coastlines(100)
    print(r)

    r = gplates.get_paleo_coastlines(100, format="shapely")
    print(r)
