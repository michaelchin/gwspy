import requests
from shapely.geometry import LineString, shape

from . import _auth as a
from ._auth import auth
from .utils import geojson_to_shapely


class Topology:
    def __init__(self, model_name, time):
        self.plate_polygons = None
        self.plate_polygons_lines = None
        self.plate_boundaries = None
        self.model_name = model_name
        self.time = time

    def get_plate_polygons(self, return_format="geojson", as_lines=False):
        if not as_lines:
            if self.plate_polygons is None:
                self.plate_polygons = get_topological_plate_polygons(
                    self.model_name, self.time
                )
            if return_format.lower() == "geojson":
                return self.plate_polygons
            else:
                return geojson_to_shapely(self.plate_polygons)
        else:
            if self.plate_polygons_lines is None:
                self.plate_polygons_lines = get_topological_plate_polygons(
                    self.model_name, self.time, as_lines=True
                )
            if return_format.lower() == "geojson":
                return self.plate_polygons_lines
            else:
                return geojson_to_shapely(self.plate_polygons_lines)

    def get_plate_boundaries(self, return_format="geojson"):
        if self.plate_boundaries is None:
            self.plate_boundaries = get_topological_plate_boundaries(
                self.model_name, self.time
            )
        if return_format.lower() == "geojson":
            return self.plate_boundaries
        else:
            return geojson_to_shapely(self.plate_boundaries)

    def get_plate_polygon_names(self):
        names = []
        if self.plate_polygons is None:
            self.plate_polygons = get_topological_plate_polygons(
                self.model_name, self.time
            )
        for feature in self.plate_polygons["features"]:
            if "name" in feature["properties"] and feature["properties"]["name"]:
                names.append(feature["properties"]["name"])
        return list(set(names))

    def get_plate_boundary_types(self):
        types = []
        if self.plate_boundaries is None:
            self.plate_boundaries = get_topological_plate_boundaries(
                self.model_name, self.time
            )
        for feature in self.plate_boundaries["features"]:
            if "type" in feature["properties"]:
                types.append(feature["properties"]["type"])
        return list(set(types))

    def get_features(self, name, return_format="geojson"):
        ret = {"type": "FeatureCollection", "features": []}

        if self.plate_boundaries is None:
            self.plate_boundaries = get_topological_plate_boundaries(
                self.model_name, self.time
            )
        for feature in self.plate_boundaries["features"]:
            if (
                "type" in feature["properties"]
                and feature["properties"]["type"] == name
            ):
                ret["features"].append(feature)

        if return_format.lower() == "geojson":
            return ret
        else:
            return geojson_to_shapely(ret)


@auth
def get_topological_plate_boundaries(model, time):
    """return topological plate boundaries

    :params model: model name
    :params time: reconstruction time

    :returns: geojson
    """
    headers = {
        "Accept": "application/json",
    }

    params = {"time": time, "model": model}

    ret = requests.get(
        a.server_url + "/topology/plate_boundaries/",
        params=params,
        verify=True,
        headers=headers,
        proxies={"http": a.proxy},
    )

    if ret.status_code in [200, 201]:
        return ret.json()


@auth
def get_topological_plate_polygons(model, time, as_lines=False):
    """return topological plate polygons

    :params model: model name
    :params time: reconstruction time

    :returns: geojson
    """
    headers = {
        "Accept": "application/json",
    }

    params = {"time": time, "model": model}
    if as_lines:
        params["as_lines"] = True

    ret = requests.get(
        a.server_url + "/topology/plate_polygons/",
        params=params,
        verify=True,
        headers=headers,
        proxies={"http": a.proxy},
    )

    if ret.status_code in [200, 201]:
        return ret.json()


@auth
def get_subduction_zones(model, time):
    """return subduction zones as geojson object"""
    r = requests.get(
        f"{a.server_url}/topology/get_subduction_zones?time={time}&model={model}"
    )
    if r.status_code != 200:
        raise Exception("Failed to get subduction zones.")
    return r.json()
