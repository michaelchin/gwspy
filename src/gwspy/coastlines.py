import requests
from shapely.geometry import shape

from . import _auth as a
from ._auth import auth


@auth
def get_paleo_coastlines(
    time: float,
    model="MULLER2022",
    format="geojson",
    facecolor="lime",
    edgecolor="none",
    alpha: float = 0.5,
    extent=(-180, 180, -90, 90),
    wrap: bool = True,
    central_meridian: float = 0.0,
    anchor_plate_id: int = 0,
    min_area: float = None,
):
    """Get paleo-coastlines

    By default, the polygons are wrapped along (180/-180). If you would like to wrap them
    at other locations, be careful that some plotting packages might not work well with them.

    :param time: the input paleo age
    :param model: the name of rotation model
    :param format: the return data format, such as geojson, shapely, png
    :param facecolor: face color -- only for png format
    :param edgecolor: edge color -- only for png format
    :param alpha: alpha -- only for png format
    :param extent: (left, right, bottom, top) -- only for png format
    :param anchor_plate_id: anchor plate id
    :param central_meridian: central meridian
    :param wrap: flag to indicate if wrap the polygons along dateline
    :param min_area: only returns polygons with a larger area

    :returns: paleo-coastlines
    :rtype: geojson

    """

    params = {
        "time": time,
        "model": model,
        "anchor_plate_id": anchor_plate_id,
        "wrap": wrap,
        "central_meridian": central_meridian,
    }

    if min_area is not None:
        params["min_area"] = min_area

    if extent is not None:
        params["extent"] = f"{extent[0]},{extent[1]},{extent[2]},{extent[3]}"

    if format == "png":
        params["fmt"] = "png"
        params["facecolor"] = facecolor
        params["edgecolor"] = edgecolor
        params["alpha"] = alpha
        headers = {
            "Accept": "image/png",
        }
    else:
        headers = {
            "Accept": "application/json",
        }

    ret = requests.get(
        a.server_url + "/reconstruct/coastlines/",
        params=params,
        verify=True,
        headers=headers,
        proxies={"http": a.proxy},
    )

    if ret.status_code in [200, 201]:
        if format == "shapely":
            json_data = ret.json()
            geoms = [
                shape(feature["geometry"]).buffer(0)
                for feature in json_data["features"]
            ]
            return geoms
        elif format == "png":
            return ret.content
        else:
            json_data = ret.json()
            return json_data
    else:
        raise Exception("Failed to get paleo-coastlines.")
