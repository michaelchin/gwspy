import requests

from . import _auth as a
from ._auth import auth


@auth
def get_subduction_zones(model, time):
    """return subduction zones as geojson object"""
    r = requests.get(
        f"{a.server_url}/topology/get_subduction_zones?time={time}&model={model}"
    )
    if r.status_code != 200:
        raise Exception("Failed to get subduction zones.")
    return r.json()
