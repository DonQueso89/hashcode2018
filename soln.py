import sys
from collections import namedtuple

# latest is the step after the vehicle has arrived
# NOT the step at which the vehicle arrives
class Ride(object):
    def __init__(self, start, end, t_start, t_end, waiting):
        self.start = start
        self.end = end
        self.t_start = t_start
        self.t_end = t_end
        self.waiting = waiting


class Vehicle(object):
    def __init__(self, pos, rides=None):
        """
        :param pos = tuple of (x, y)
        """
        self.rides = rides or []
        self.pos = pos
        self.occupied = False


def get_rides(fname):
    inp = open(fname, 'r')
    R, C, F, N, B, T = map(int, next(inp).split(' '))
    rides = []
    for line in inp:
        a, b, x, y, s, f = map(int, line.split(' '))
        rides.append(Ride((a, b), (x, y), s, f, waiting=True))
    return rides


def main(fname):
    rides = get_rides(fname)


def distance(coord1, coord2):
    """
    :param coord1, tuple of (x, y)
    :param coord2, tuple of (x, y)
    """
    x1, y1 = coord1
    x2, y2 = coord2
    return abs(x1 - x2) + abs(y1 - y2)


if __name__ == '__main__':
    main(sys.argv[1])
