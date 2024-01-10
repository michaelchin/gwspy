import json

from utils import logger

from gplates_ws_proxy import subduction_teeth

lons = [-43.1124, -6.1282, 5.0676, 18.7966, 30.2718, 40.4890, 52.3162]
lats = [11.3974, 6.6426, 10.8345, 9.1520, 6.0869, 9.1520, 6.9207]


def test_subduction_teeth():
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

    assert len(teeth) > 0


if __name__ == "__main__":
    teeth = subduction_teeth.get_subduction_teeth_in_degrees(
        lons,
        lats,
        base_length=1,
        spacing=0.5,
        height=0.5,
        geojson=True,
        polarity=subduction_teeth.Polarity.LEFT,
    )

    NO_GEOMETRY_COLLECTION = True

    print(len(teeth))

    data = {"type": "FeatureCollection"}
    data["features"] = []

    if NO_GEOMETRY_COLLECTION:
        for tooth in teeth:
            feature = {"type": "Feature", "properties": {}}
            feature["geometry"] = tooth
            data["features"].append(feature)
    else:
        feature = {"type": "Feature", "properties": {}}
        feature["geometry"] = {"type": "GeometryCollection", "geometries": teeth}
        data["features"].append(feature)

    line_feature = {"type": "Feature", "properties": {}}
    line_feature["geometry"] = {
        "type": "LineString",
        "coordinates": list(zip(lons, lats)),
    }

    data["features"].append(line_feature)

    with open("triangles.json", "w") as outfile:
        json.dump(data, outfile, indent=4)

    print("Done. Teeth have been saved to triangles.json.")
