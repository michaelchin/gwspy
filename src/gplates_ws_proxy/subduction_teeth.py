from enum import Enum

import rotation
from resample_line import sample_next_point
from spherical_triangle import get_third_vertex


class Polarity(Enum):
    UNKNOWN = 0
    RIGHT = 1
    LEFT = 2


def get_triangle(point_a, point_b, base_length, height, polarity):
    """return a triangle

    :params point_a:  {"lon": lon, "lat": lat} in radian
    :params point_b:  {"lon": lon, "lat": lat} in radian
    :params base_length: triangle base length
    :params polarity: subduction polarity
    """
    axis, angle = rotation.find_axis_and_angle(
        (point_a["lat"], point_a["lon"]),
        (point_b["lat"], point_b["lon"]),
    )
    lat, lon = rotation.rotate((point_a["lat"], point_a["lon"]), axis, base_length)
    _height = height
    if polarity == Polarity.LEFT:
        _height = -height
    point_c = get_third_vertex(
        point_a,
        {"lon": lon, "lat": lat},
        _height,
    )
    return [
        point_a,
        {"lon": lon, "lat": lat},
        point_c,
    ]


def get_subduction_teeth(
    lons: list[float],
    lats: list[float],
    base_length: float = 0.05,
    spacing: float = 0.05,
    height: float = 0.05,
    polarity: Polarity = Polarity.UNKNOWN,
):
    """return a list of triangle polygons for given polyline

    :params lons: a list of lons
    :params lats: a list of lats
    :params base_length: base length of triangle (in radian)
    :params spacing: space between triangles (in radian)
    :params height: triangle height (in radian)
    :params polarity: the polarity of this subduction zone (left or right)
    """
    assert len(lons) == len(lats)
    assert len(lons) > 1

    # the first triangle, always have at least one triangle for a line
    triangles = [
        get_triangle(
            {"lon": lons[0], "lat": lats[0]},
            {"lon": lons[1], "lat": lats[1]},
            base_length,
            height,
            polarity,
        )
    ]

    pp, ll = sample_next_point(
        list(zip(lats, lons)), base_length + spacing, strict=True
    )

    while pp:
        triangles.append(
            get_triangle(
                {"lon": pp[1], "lat": pp[0]},
                {"lon": ll[1][1], "lat": ll[1][0]},
                base_length,
                height,
                polarity,
            )
        )
        pp, ll = sample_next_point(ll, base_length + spacing, strict=True)
    return triangles


if __name__ == "__main__":
    lons = [-43.1124, -6.1282, 5.0676, 18.7966, 30.2718, 40.4890, 52.3162]
    lats = [11.3974, 6.6426, 10.8345, 9.1520, 6.0869, 9.1520, 6.9207]

    print(get_subduction_teeth(lons, lats))
