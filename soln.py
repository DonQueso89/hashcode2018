import random
import sys
import pendulum
from collections import namedtuple


# latest is the step after the vehicle has arrived
# NOT the step at which the vehicle arrives
class Ride(object):
    def __init__(self, start, end, t_start, t_end, waiting, ind):
        self.start = start
        self.end = end
        self.t_start = t_start
        self.t_end = t_end
        self.waiting = waiting
        self.ind = ind


class Vehicle(object):
    def __init__(self, pos, rides=None):
        """
        :param pos = tuple of (x, y)
        """
        self.rides = rides or []
        self.pos = pos
        self.occupied = False

    def __str__(self):
        s = str(len(self.rides))
        for r in self.rides:
            s += ' %d' % r.ind
        s += '\n'
        return s

    def assign(self, ride):
        self.rides.append(ride)


def get_rides(fp):
    rides = []
    ind = 0
    for line in fp:
        a, b, x, y, s, f = map(int, line.split(' '))
        rides.append(Ride((a, b), (x, y), s, f, True, ind))
        ind += 1
    return rides


def main(fname):
    fp = open(fname, 'r')
    R, C, F, N, B, T = map(int, next(fp).split(' '))
    # init rides
    rides = get_rides(fp)
    # init vehicles
    vehicles = []
    for i in range(F):
        vehicles.append(Vehicle((0, 0)))

    for ride in rides:
        random.choice(vehicles).assign(ride)

    output(vehicles, fname)


def output(vehicles, fname):
    with open('%soutput%s' % (fname, pendulum.now().isoformat()), 'a') as outp:
        for v in vehicles:
            outp.write(str(v))


def score(vehicles):
   pass


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
