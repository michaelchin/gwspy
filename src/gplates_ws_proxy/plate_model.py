import json

import requests
import shapely
from shapely.geometry import shape

from . import _auth as a
from ._auth import auth
from .coastlines import get_paleo_coastlines
from .paleoearth import get_paleo_labels
from .reconstruction import get_paleo_coordinates, reconstruct_points
from .topology import Topology, get_subduction_zones


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

    def get_paleo_labels(self):
        """get a list of paleo-labels

        :returns: a dict object, {"names": names, "lons": lons, "lats": lats}
        """
        return get_paleo_labels()

    def get_subduction_zones(self, time):
        """"""
        return get_subduction_zones(self.name, time)

    def get_topology(self, time):
        """"""
        return Topology(self.name, time)

    def get_coastlines(
        self,
        time: float,
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
        """"""
        return get_paleo_coastlines(
            time=time,
            model=self.name,
            format=format,
            facecolor=facecolor,
            edgecolor=edgecolor,
            alpha=alpha,
            extent=extent,
            wrap=wrap,
            central_meridian=central_meridian,
            anchor_plate_id=anchor_plate_id,
            min_area=min_area,
        )


def reconstruct_shapely_points(
    model: PlateModel, points: list[shapely.Point], time: float, pids: list[int] = []
) -> list[shapely.Point]:
    """reconstruct a list of shapely points to {time}Ma"""
    return reconstruct_points(points, time, model=model.name, pids=pids)
