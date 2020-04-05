'''particle module'''

class particle(object):
    '''particle object'''
    def __init__(self, prev, nex, vector, bearing, threshold, direction):
        self.prev = prev
        self.nex = nex
        self.vector = vector
        self.bearing = bearing
        self.threshold = threshold
        self.direction = direction
        self.death = False
        self.birth = False
