import requests

from . import _auth as a
from ._auth import auth


@auth
def get_paleo_labels(time: float, model: str = "MULLER2022"):
    """get a list of paleo-labels

    :returns: a dict object, {"names": names, "lons": lons, "lats": lats}
    """

    r = requests.get(f"{a.server_url}/earth/get_labels?time={time}&model={model}")
    if r.status_code != 200:
        raise Exception("Failed to get paleo-labels!")
    labels = r.json()
    names = []
    lons = []
    lats = []
    for label in labels:
        names.append(label[0])
        lats.append(label[1])
        lons.append(label[2])
    return {"names": names, "lons": lons, "lats": lats}
