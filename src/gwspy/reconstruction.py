import json

import requests
from shapely import Point

from . import _auth as a
from ._auth import auth


@auth
def get_paleo_coordinates(
    lats,
    lons,
    age,
    model="SETON2012",
    pids=[],
):
    """convenient function to get paleo-coordinates at {age}"""

    if len(lats) != len(lons):
        raise Exception("the length of lats and lons must be the same.")

    pids_len = len(pids)
    if pids_len > 0:
        if pids_len != 1 and pids_len != len(lons):
            raise Exception(
                "the length of pids must be 0, 1 or the length of lons/lats."
            )

    data = {"time": age, "return_null_points": ""}

    # construct the request string for points
    lats_str = ""
    lons_str = ""
    for lat in lats:
        lats_str += f"{lat:3.2f},"
    for lon in lons:
        lons_str += f"{lon:3.2f},"

    data["lats"] = lats_str[:-1]
    data["lons"] = lons_str[:-1]

    # construct the request string for plates ids
    if pids_len == 1:
        data["pid"] = f"{int(pids[0])}"
    elif pids_len == len(lons):
        pids_str = ""
        for pid_ in pids:
            pids_str += f"{int(pid_)},"
        data["pids"] = pids_str[:-1]

    data["model"] = model

    ret = requests.post(
        a.server_url + "/reconstruct/reconstruct_points/",
        data=data,
        verify=True,
        proxies={"http": a.proxy},
    )
    # print(ret.text)

    data = json.loads(str(ret.text))
    # print(data)
    lats_r = []
    lons_r = []
    for c in data["coordinates"]:
        if not c:
            lats_r.append(float("NAN"))
            lons_r.append(float("NAN"))
        else:
            lats_r.append(c[1])
            lons_r.append(c[0])

    return {"lats": lats_r, "lons": lons_r}


@auth
def reconstruct_points(
    points: list[Point],
    age,
    model="SETON2012",
    pids=[],
):
    """get paleo-coordinates for a list of shapely points, return new shapely points"""
    lats = [p.y for p in points]
    lons = [p.x for p in points]

    data = get_paleo_coordinates(lats, lons, age, model, pids)

    return [Point(x, y) for x, y in zip(data["lons"], data["lats"])]
