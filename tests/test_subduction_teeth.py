import json

from importer import *

from gplates_ws_proxy import subduction_teeth


def test_subduction_teeth():
    lons = [-43.1124, -6.1282, 5.0676, 18.7966, 30.2718, 40.4890, 52.3162]
    lats = [11.3974, 6.6426, 10.8345, 9.1520, 6.0869, 9.1520, 6.9207]

    """
    teeth = subduction_teeth.get_subduction_teeth(
        [math.radians(lon) for lon in lons],
        [math.radians(lat) for lat in lats],
        geojson=True,
        return_degrees=True,
    )
    """
    teeth = subduction_teeth.get_subduction_teeth_in_degrees(
        lons, lats, base_length=1, spacing=0.5, height=0.5, geojson=True
    )
    data = {"type": "FeatureCollection"}
    data["features"] = []
    feature = {"type": "Feature", "properties": {}}
    feature["geometry"] = {"type": "GeometryCollection", "geometries": teeth}

    line_feature = {"type": "Feature", "properties": {}}
    line_feature["geometry"] = {"type": "LineString", "coordinates": zip(lons, lats)}

    data["features"].append(feature)

    with open("triangles.json", "w") as outfile:
        json.dump(data, outfile, indent=4)


if __name__ == "__main__":
    test_subduction_teeth()
