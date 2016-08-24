__author__ = 'sunary'


class Boid():

    def __init__(self):
        self.loc = None
        self.vel = None

    def update(self, boids):
        self.loc += self.vel

        neighbour_bolds = self.check_around(boids)
        self.separation(neighbour_bolds)
        self.alignment(neighbour_bolds)
        self.cohesion(neighbour_bolds)

    def check_around(self, boids):
        pass

    def separation(self, neighbour_boids):
        pass

    def alignment(self, neighbour_boids):
        pass

    def cohesion(self, neighbour_boids):
        pass