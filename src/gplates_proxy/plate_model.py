import json

import requests

from . import _auth as a
from ._auth import auth
from .reconstruction import reconstruct_shapely_points


class PlateModel:
    def __init__(self, name):
        self.name = name

    @auth
    @staticmethod
    def list():
        """return a list which contains all the available rotation models"""
        ret = requests.get(
            a.server_url + "/model/list",
            verify=True,
            proxies={"http": a.proxy},
        )
        return json.loads(str(ret.text))

    @auth
    def get_cfg(self):
        """Given a rotation model name, return the details about the model"""
        params = {"model": self.name}

        ret = requests.get(
            a.server_url + f"/model/show",
            params=params,
            verify=True,
            proxies={"http": a.proxy},
        )

        return json.loads(str(ret.text))

    def reconstruct(self, points, time: float, pids=[]):
        """reconstruct a list of shapely points to {time}Ma"""
        return reconstruct_shapely_points(points, time, model=self.name, pids=pids)
