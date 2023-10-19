import math
from enum import Enum

from . import rotation
from .geometry_utils import test_line_segment_cross_dateline
from .resample_line import sample_next_point
from .spherical_triangle import get_third_vertex


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

    assert point_a != point_b  # the two points cannot be the same

    axis, angle = rotation.find_axis_and_angle(
        (point_a["lat"], point_a["lon"]),
        (point_b["lat"], point_b["lon"]),
    )

    if not base_length:
        lat = point_b["lat"]
        lon = point_b["lon"]
    else:
        lat, lon = rotation.rotate((point_a["lat"], point_a["lon"]), axis, base_length)
    _height = height
    if polarity == Polarity.RIGHT:
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
    base_length: float = 0.03,
    spacing: float = 0.01,
    height: float = 0.03,
    polarity: Polarity = Polarity.UNKNOWN,
    geojson: bool = False,
    return_degrees: bool = True,
    central_meridian: float = None,
):
    """return a list of triangle polygons for given polyline

    :params lons: a list of lons (in radian)
    :params lats: a list of lats (in radian)
    :params base_length: base length of triangle (in radian)
    :params spacing: space between triangles (in radian)
    :params height: triangle height (in radian)
    :params polarity: the polarity of this subduction zone (left or right)
    :params geojson: if set True, return data in geojson format
    :params return_degrees: if set True, return coordinates in degrees
    :params central_meridian: if set, omit triangles cross dateline (in radian)

    :returns: [[{'lon':lon, 'lat':lat}, {'lon':lon, 'lat':lat}, {'lon':lon, 'lat':lat}],...]
        or {
                "type": "GeometryCollection",
                "geometries":
                [
                    {
                        "type": "Polygon",
                        "coordinates":
                        [
                            [
                                [100.0, 0.0], [101.0, 0.0], [101.0, 1.0],
                            ]
                        ]
                    },
                    {
                        "type": "Polygon",
                        "coordinates":
                        [
                            [
                                [110.0, 10.0], [10.0, 10.0], [101.0, 10.0],
                            ]
                        ]
                    },
                    ...
                ]
            }
    """
    assert len(lons) == len(lats)
    assert len(lons) > 1
    if (
        max(lons) > math.pi
        or min(lons) < -math.pi
        or max(lats) > math.pi
        or min(lats) < -math.pi
    ):
        raise Exception("The coordinates need to be in radians.")

    if geojson:
        return_degrees = True

    first_vertex = {"lon": lons[0], "lat": lats[0]}

    pp, ll = sample_next_point(list(zip(lats, lons)), base_length, strict=True)
    triangles = []
    while pp:
        second_vertex = {"lon": pp[1], "lat": pp[0]}
        triangles.append(
            get_triangle(
                first_vertex,
                second_vertex,
                None,  # base_length
                height,
                polarity,
            )
        )
        if polarity == Polarity.UNKNOWN:
            triangles.append(
                get_triangle(
                    first_vertex,
                    second_vertex,
                    None,  # base_length
                    height,
                    Polarity.LEFT,
                )
            )
            triangles.append(
                get_triangle(
                    first_vertex,
                    second_vertex,
                    None,  # base_length
                    height,
                    Polarity.RIGHT,
                )
            )

        pp, ll = sample_next_point(ll, spacing, strict=True)
        if not pp:
            break
        first_vertex = {"lon": pp[1], "lat": pp[0]}
        pp, ll = sample_next_point(ll, base_length, strict=True)

    _triangles = []
    if central_meridian is not None:
        for triangle in triangles:
            if (
                test_line_segment_cross_dateline(
                    triangle[0]["lon"], triangle[1]["lon"], central_meridian
                )
                or test_line_segment_cross_dateline(
                    triangle[1]["lon"], triangle[2]["lon"], central_meridian
                )
                or test_line_segment_cross_dateline(
                    triangle[0]["lon"], triangle[2]["lon"], central_meridian
                )
            ):
                continue
            else:
                _triangles.append(triangle)
        triangles = _triangles

    if geojson:
        polygons = []
        for triangle in triangles:
            polygon = {"type": "Polygon"}
            if return_degrees:
                polygon["coordinates"] = [
                    [
                        [
                            math.degrees(triangle[0]["lon"]),
                            math.degrees(triangle[0]["lat"]),
                        ],
                        [
                            math.degrees(triangle[1]["lon"]),
                            math.degrees(triangle[1]["lat"]),
                        ],
                        [
                            math.degrees(triangle[2]["lon"]),
                            math.degrees(triangle[2]["lat"]),
                        ],
                        [
                            math.degrees(triangle[0]["lon"]),
                            math.degrees(triangle[0]["lat"]),
                        ],
                    ]
                ]
            else:
                polygon["coordinates"] = [
                    [
                        [triangle[0]["lon"], triangle[0]["lat"]],
                        [triangle[1]["lon"], triangle[1]["lat"]],
                        [triangle[2]["lon"], triangle[2]["lat"]],
                        [triangle[0]["lon"], triangle[0]["lat"]],
                    ]
                ]
            polygons.append(polygon)
        return polygons

    if return_degrees:
        triangles_in_degrees = []
        for triangle in triangles:
            triangle_in_degrees = [
                {
                    "lon": math.degrees(triangle[0]["lon"]),
                    "lat": math.degrees(triangle[0]["lat"]),
                },
                {
                    "lon": math.degrees(triangle[1]["lon"]),
                    "lat": math.degrees(triangle[1]["lat"]),
                },
                {
                    "lon": math.degrees(triangle[2]["lon"]),
                    "lat": math.degrees(triangle[2]["lat"]),
                },
            ]
            triangles_in_degrees.append(triangle_in_degrees)
        return triangles_in_degrees
    else:
        return triangles


def get_subduction_teeth_in_degrees(
    lons: list[float],
    lats: list[float],
    base_length: float = 1,
    spacing: float = 0.5,
    height: float = 1,
    polarity: Polarity = Polarity.UNKNOWN,
    geojson: bool = False,
    central_meridian: float = None,
):
    """same as get_subduction_teeth, just everything is in degrees"""
    if central_meridian is not None:
        central_meridian = math.radians(central_meridian)
    return get_subduction_teeth(
        [math.radians(lon) for lon in lons],
        [math.radians(lat) for lat in lats],
        base_length=math.radians(base_length),
        spacing=math.radians(spacing),
        height=math.radians(height),
        polarity=polarity,
        geojson=geojson,
        return_degrees=True,
        central_meridian=central_meridian,
    )
