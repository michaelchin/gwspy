from shapely.geometry import MultiPolygon, Polygon, shape


def geojson_to_shapely(json_data):
    ret = []
    for feature in json_data["features"]:
        s = shape(feature["geometry"])
        if isinstance(s, Polygon) or isinstance(s, MultiPolygon):
            ret.append(s.buffer(0))
        else:
            ret.append(s)

    return ret
