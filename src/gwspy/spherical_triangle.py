import math

from . import quaternions, rotation


def get_third_vertex(point_a, point_b, height=0.05):
    """Given two points, get third point of triangle.

    :params point_a: {"lon": lon, "lat": lat} in radian
    :params point_b: {"lon": lon, "lat": lat} in radian
    :params height: in radian

    :returns: {"lon": lon, "lat": lat} in radian
    """

    assert not (
        math.isclose(point_a["lon"], point_b["lon"])
        and math.isclose(point_a["lat"], point_b["lat"])
    )

    PA_xyz = quaternions.lat_lon_to_cart(point_a["lat"], point_a["lon"])
    PB_xyz = quaternions.lat_lon_to_cart(point_b["lat"], point_b["lon"])

    # another method to get middle point
    AB_middle_xyz = (
        (PA_xyz[0] + PB_xyz[0]) / 2,
        (PA_xyz[1] + PB_xyz[1]) / 2,
        (PA_xyz[2] + PB_xyz[2]) / 2,
    )
    AB_middle_xyz = quaternions.normalize(AB_middle_xyz)
    middle_lat, middle_lon = quaternions.cart_to_lat_lon(
        AB_middle_xyz[0], AB_middle_xyz[1], AB_middle_xyz[2]
    )

    """
    # get middle point
    axis, angle = rotation.find_axis_and_angle(
        [PA_lon_lat[1], PA_lon_lat[0]], [PB_lon_lat[1], PB_lon_lat[0]]
    )
    middle_lat, middle_lon = rotation.rotate(
        [PA_lon_lat[1], PA_lon_lat[0]], axis, angle / 2.0
    )
    """

    # get rotation pole
    AB = (PA_xyz[0] - PB_xyz[0], PA_xyz[1] - PB_xyz[1], PA_xyz[2] - PB_xyz[2])
    AB = quaternions.normalize(AB)
    pole_lat, pole_lon = quaternions.cart_to_lat_lon(AB[0], AB[1], AB[2])

    lat, lon = rotation.rotate(
        [middle_lat, middle_lon],
        [pole_lat, pole_lon],
        height,
    )

    return {"lon": lon, "lat": lat}


if __name__ == "__main__":
    a = {"lon": -121.0, "lat": 15.0}
    b = {"lon": -121.0, "lat": -15.0}

    with open("ring.gmt", "w+") as f:
        f.write(f"{a['lon']:.2f} {a['lat']:.2f}\n")
        f.write(f"{b['lon']:.2f} {b['lat']:.2f}\n")
        for angle in range(360):
            third_vertex = get_third_vertex(
                {"lon": math.radians(a["lon"]), "lat": math.radians(a["lat"])},
                {"lon": math.radians(b["lon"]), "lat": math.radians(b["lat"])},
                math.radians(angle),
            )
            f.write(
                f"{math.degrees(third_vertex['lon']):.2f} {math.degrees(third_vertex['lat']):.2f}\n"
            )

    print("done")
