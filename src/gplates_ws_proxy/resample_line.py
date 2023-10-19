import math

from . import rotation


def degree_to_radian(point):
    return [math.radians(point[0]), math.radians(point[1])]


def radian_to_degree(point):
    return [math.degrees(point[0]), math.degrees(point[1])]


def sample_next_point(line, distance, strict=False, accum_length=0):
    """recursive function to sample point one by one
    :param line: a list of (lat, lon) in radians
    :param distance: the distance to the next point
    :param strict: in strict mode, we guarantee the distance. sacrifice the end point if necessary
    :accum_length: parameter to pass down the accumulated length for this recursive function
    :returns: (next point, new line)
        next point (lat,lon) in radians. None, if no more point
        new line -- the line after taking out this point
    """
    if len(list(line)) < 2:
        return None, []

    start_point = line[0]
    second_point = line[1]

    dd = rotation.radian_distance(start_point, second_point)

    if math.isclose(dd + accum_length, distance):
        return second_point, line[1:]
    elif (dd + accum_length) > distance:
        pp = rotation.sample_between_two_points(
            start_point, second_point, [distance - accum_length]
        )[0]
        assert pp
        return pp, [pp] + line[1:]
    else:
        if len(line[1:]) > 1:
            return sample_next_point(
                line[1:], distance, strict=strict, accum_length=dd + accum_length
            )
        else:
            if strict:
                # in strict mode, we guarantee the distance. It means we will sacrifice the end point if necessary
                return None, []
            else:
                return second_point, line[1:]  # reached the last point


def resample_line(line, distance, strict=False):
    """resample a line.
    :param line: a list of (lat, lon) in radians
    :param distance: the distance of the adjacent points
    :param strict: in strict mode, we guarantee the distance. sacrifice the end point if necessary
        in unstrict mode, we always keep the end point
    :returns: the new line
        a list of (lat, lon) in radians. If the input line is shorter than distance, in strict mode, return []
    """
    new_line = [line[0]]

    ll = line

    while True:
        pp, ll = sample_next_point(ll, distance, strict=strict)
        if pp:
            new_line.append(pp)
        else:
            break

    if len(new_line) > 1:
        return new_line
    else:
        return []


if __name__ == "__main__":
    pass
