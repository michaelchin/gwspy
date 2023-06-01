import requests
import shapely
from shapely.geometry import shape

from . import _auth as a
from ._auth import auth


@auth
def get_paleo_coastlines(age, model="MULLER2022", format="geojson"):
    """Get paleo-coastlines

    :param age: the input paleo age
    :param model: the name of rotation model
    :param format: the return data format, such as geojson, shapely
    :returns: paleo-coastlines
    :rtype: geojson

    """
    headers = {
        "Accept": "application/json",
    }
    params = {"time": age, "model": model}

    ret = requests.get(
        a.server_url + "/reconstruct/coastlines/",
        params=params,
        verify=True,
        headers=headers,
        proxies={"http": a.proxy},
    )
    json_data = ret.json()
    if ret.status_code in [200, 201]:
        if format == "shapely":
            geoms = [
                shape(feature["geometry"]).buffer(0)
                for feature in json_data["features"]
            ]
            return geoms
        else:
            return json_data
    else:
        raise Exception("Failed to get paleo-coastlines.")
