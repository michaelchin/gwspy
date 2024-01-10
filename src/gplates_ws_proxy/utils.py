from shapely.geometry import MultiPolygon, Polygon, shape

from . import _auth as a
from ._auth import auth


def geojson_to_shapely(json_data):
    ret = []
    for feature in json_data["features"]:
        s = shape(feature["geometry"])
        if isinstance(s, Polygon) or isinstance(s, MultiPolygon):
            ret.append(s.buffer(0))
        else:
            ret.append(s)

    return ret


@auth
def get_cfg():
    return {
        "username": a.username,
        "passwd": a.passwd,
        "server_url": a.server_url,
        "proxy": a.proxy,
    }
