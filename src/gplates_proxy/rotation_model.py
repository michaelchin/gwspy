import requests, json, time, random

from . import _auth as a
from ._auth import auth


@auth
def list_rotation_models():
    """return a list which contains all the available rotation models"""
    ret = requests.get(
        a.server_url + "/info/model_names",
        verify=True,
        proxies={"http": a.proxy},
    )
    return json.loads(str(ret.text))


@auth
def get_model_details(model_name):
    """Given a rotation model name, return the details about the model"""
    params = {"model": model_name}
    ret = requests.get(
        a.server_url + f"/info/get_model_details",
        params=params,
        verify=True,
        proxies={"http": a.proxy},
    )
    print(ret.text)
    return json.loads(str(ret.text))
