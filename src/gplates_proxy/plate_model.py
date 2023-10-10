import json

import requests
import shapely

from . import _auth as a
from ._auth import auth
from .reconstruction import get_paleo_coordinates, reconstruct_points


class PlateModel:
    def __init__(self, name="MULLER2019"):
        self.name = name

    @auth
    @staticmethod
    def list_models():
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

    def reconstruct(
        self,
        lats: list[float],
        lons: list[float],
        age: float,
        pids: list[int] = [],
    ) -> dict[str, list]:
        """reconstruct a list of lats and lons to age

        :returns: for example, {'lats':[1.1,2.2], 'lons':[2.1,2.3]}
        """
        return get_paleo_coordinates(lats, lons, age, model=self.name, pids=pids)


def reconstruct_shapely_points(
    model: PlateModel, points: list[shapely.Point], time: float, pids: list[int] = []
) -> list[shapely.Point]:
    """reconstruct a list of shapely points to {time}Ma"""
    return reconstruct_points(points, time, model=model.name, pids=pids)
