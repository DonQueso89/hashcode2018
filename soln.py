import random
import sys
import pendulum
import numpy as np
from collections import namedtuple


# latest is the step after the vehicle has arrived
# NOT the step at which the vehicle arrives
Ride = namedtuple('Ride', ['start', 'end', 't_start', 't_end', 'ind'])


class Vehicle(object):
    def __init__(self, pos, rides=None):
        """
        :param pos = tuple of (x, y)
        """
        self.rides = rides or []
        self.pos = pos
        self.current_ride = None

    def __str__(self):
        s = str(len(self.rides))
        for r in self.rides:
            s += ' %d' % r.ind
        s += '\n'
        return s

    def assign(self, ride):
        self.current_ride = ride
        self.rides.append(ride)

    def unassign(self):
        self.current_ride = None

    @property
    def r(self):
        return self.current_ride


def get_rides(fp):
    rides = []
    ind = 0
    for line in fp:
        a, b, x, y, s, f = map(int, line.split(' '))
        rides.append(Ride(np.array([a, b]), np.array([x, y]), s, f, ind))
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
        vehicle = Vehicle(np.array([0, 0]))
        rides = optimal_path(vehicle, rides, T)
        vehicles.append(vehicle)

    rides = sorted(rides, key=lambda x: x.t_start, reverse=True)
    output(vehicles, fname)


def closest_ride(vehicle, rides):
    closest = random.choice(rides)
    for r in rides:
        if distance(r.start, vehicle.pos) < distance(closest.start, vehicle.pos):
            closest = r
   
    return closest


def optimal_path(vehicle, rides, T):
    t = 0
    attempt = 0
    while t < T and len(rides) > 0:
        closest = closest_ride(vehicle, rides)
        if attempt == 1:
            closest = random.choice(rides)
            attempt = 0
        dist_to_start = distance(vehicle.pos, closest.start)
        dist_ride = distance(closest.start, closest.end)
        if (T - t) < (dist_to_start + dist_ride):
            break
        # Can the vehicle still do the ride?
        if dist_to_start + t < closest.t_end - dist_ride:
            vehicle.assign(closest)
            t += dist_to_start
            t += dist_ride
            vehicle.pos = closest.end
            rides = [r for r in rides if r.ind != closest.ind]
            continue
        attempt += 1
    return rides


def output(vehicles, fname):
    with open('%soutput%s' % (fname, pendulum.now().isoformat()), 'a') as outp:
        for v in vehicles:
            outp.write(str(v))


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
