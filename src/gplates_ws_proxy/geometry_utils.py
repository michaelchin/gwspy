import math

from .rotation import cross


def test_line_segment_cross_dateline_in_degrees(
    point_a_lon, point_b_lon, central_meridian
):
    """same as test_line_segment_cross_dateline except all arguments are in degrees"""
    return test_line_segment_cross_dateline(
        math.radians(point_a_lon),
        math.radians(point_b_lon),
        math.radians(central_meridian),
    )


def test_line_segment_cross_dateline(point_a_lon, point_b_lon, central_meridian):
    """Return True if the line segment cross dateline, otherwise False.
    All parameters are in radians.
    """
    dateline_lon = central_meridian + math.pi

    a_to_dateline = abs(point_a_lon - dateline_lon) % (math.pi * 2)
    b_to_dateline = abs(point_b_lon - dateline_lon) % (math.pi * 2)
    a_to_b = abs(point_a_lon - point_b_lon) % (math.pi * 2)

    assert not math.isclose(
        a_to_b, math.pi
    )  # two points are 180 degree apart along longitude axis. cannot decide if cross dateline

    if a_to_dateline > math.pi:
        a_to_dateline = 2 * math.pi - a_to_dateline
    if b_to_dateline > math.pi:
        b_to_dateline = 2 * math.pi - b_to_dateline
    if a_to_b > math.pi:
        a_to_b = 2 * math.pi - a_to_b

    # print(a_to_dateline, b_to_dateline, a_to_b)

    if math.isclose(a_to_dateline, 0.0) or math.isclose(b_to_dateline, 0.0):
        # print(point_a_lon, point_b_lon)
        if abs(point_a_lon - point_b_lon) < math.pi:
            return False
        else:
            return True

    if math.isclose(a_to_dateline + b_to_dateline, a_to_b):
        return True

    if a_to_dateline + b_to_dateline > a_to_b:
        return False
    else:
        return True


def lat_lon_to_xyz(lat, lon):
    """all in radians"""
    x = math.cos(lat) * math.cos(lon)
    y = math.cos(lat) * math.sin(lon)
    z = math.sin(lat)
    return x, y, z


def xyz_to_lat_lon(x, y, z):
    """in radians"""
    lat = math.asin(z) * 180.0 / math.pi
    lon = math.atan2(y, x) * 180.0 / math.pi
    return lat, lon


def find_two_great_circles_intersections(point_a, point_b, point_c, point_d):
    """return the two intersection points"""
    # to gradians
    pa_lat_rad = math.radians(point_a["lat"])
    pa_lon_rad = math.radians(point_a["lon"])
    pb_lat_rad = math.radians(point_b["lat"])
    pb_lon_rad = math.radians(point_b["lon"])

    # to gradians
    pc_lat_rad = math.radians(point_c["lat"])
    pc_lon_rad = math.radians(point_c["lon"])
    pd_lat_rad = math.radians(point_d["lat"])
    pd_lon_rad = math.radians(point_d["lon"])

    # get xyz coordinates
    xa, ya, za = lat_lon_to_xyz(pa_lat_rad, pa_lon_rad)
    xb, yb, zb = lat_lon_to_xyz(pb_lat_rad, pb_lon_rad)
    xc, yc, zc = lat_lon_to_xyz(pc_lat_rad, pc_lon_rad)
    xd, yd, zd = lat_lon_to_xyz(pd_lat_rad, pd_lon_rad)

    # Get normal to planes containing great circles
    N1 = cross([xa, ya, za], [xb, yb, zb])
    N2 = cross([xc, yc, zc], [xd, yd, zd])

    # Find line of intersection between two planes
    L = cross(N1, N2)

    # Find two intersection points
    X1 = [x / math.sqrt(L[0] ** 2 + L[1] ** 2 + L[2] ** 2) for x in L]
    X2 = [-x for x in X1]
    lat1, lon1 = xyz_to_lat_lon(X1[0], X1[1], X1[2])
    lat2, lon2 = xyz_to_lat_lon(X2[0], X2[1], X2[2])

    return {"lat": lat1, "lon": lon1}, {"lat": lat2, "lon": lon2}
