import requests

from . import _auth as a
from ._auth import auth


@auth
def get_paleo_labels(time: float, model: str = "MULLER2022"):
    """get a list of paleo-labels

    :returns: a dict object, {"names": names, "lons": lons, "lats": lats}
    """

    url = f"{a.server_url}/earth/get_labels?time={time}&model={model}"
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception(f"Failed to get paleo-labels {r.status_code}! -- {url}")
    labels = r.json()
    names = []
    lons = []
    lats = []
    for label in labels:
        names.append(label[0])
        lats.append(label[1])
        lons.append(label[2])
    return {"names": names, "lons": lons, "lats": lats}


@auth
def get_paleo_cities(time: float, model: str = "MULLER2022"):
    """get a list of paleo-cities

    :returns: a dict object, {"names": names, "lons": lons, "lats": lats}
    """

    url = f"{a.server_url}/earth/get_cities?time={time}&model={model}"
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception(f"Failed to get paleo-cities {r.status_code}! -- {url}")

    return r.json()
