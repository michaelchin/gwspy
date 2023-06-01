import requests
import shapely
from shapely.geometry import shape

from . import _auth as a
from ._auth import auth


@auth
def get_paleo_coastlines(
    age,
    model="MULLER2022",
    format="geojson",
    facecolor="lime",
    edgecolor="none",
    alpha=0.5,
    extent=(-20, 20, -20, 20),
    anchor_plate_id=0,
):
    """Get paleo-coastlines

    :param age: the input paleo age
    :param model: the name of rotation model
    :param format: the return data format, such as geojson, shapely, png
    :param facecolor: face color -- only for png format
    :param edgecolor: edge color -- only for png format
    "param alpha": alpha -- only for png format
    :param extent: (left, right, bottom, top) -- only for png format
    :param anchor_plate_id: anchor plate id

    :returns: paleo-coastlines
    :rtype: geojson

    """

    params = {"time": age, "model": model, "anchor_plate_id": anchor_plate_id}
    if format == "png":
        params["fmt"] = "png"
        params["facecolor"] = facecolor
        params["edgecolor"] = edgecolor
        params["alpha"] = alpha
        params["extent"] = f"{extent[0]},{extent[1]},{extent[2]},{extent[3]}"
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
