__author__ = 'sunary'


import Tkinter
import math
import random


CANVAS_SIZE = (700, 500)


class Boid():

    def __init__(self):
        self.loc = None
        self.angle = None
        self.triangle = [[0, 0] for _ in range(3)]

    def set(self, loc, angle):
        self.loc = loc
        self.angle = angle

        self.update_triangle()

    def draw(self, canvas):
        canvas.create_polygon(self.triangle[0][0], self.triangle[0][1],
                              self.triangle[1][0], self.triangle[1][1],
                              self.triangle[2][0], self.triangle[2][1], fill='red')

    def update(self, boids):
        self.loc = [self.loc[0] + 2 * math.cos(self.angle), self.loc[1] - 2 * math.sin(self.angle)]

        self.loc[0] = CANVAS_SIZE[0] + self.loc[0] if self.loc[0] < 0 else self.loc[0]
        self.loc[1] = CANVAS_SIZE[1] + self.loc[1] if self.loc[1] < 0 else self.loc[1]

        self.loc[0] = self.loc[0] - CANVAS_SIZE[0] if self.loc[0] > CANVAS_SIZE[0] else self.loc[0]
        self.loc[1] = self.loc[1] - CANVAS_SIZE[1] if self.loc[1] > CANVAS_SIZE[1] else self.loc[1]

        neighbour_bolds = self.check_around(boids)
        if len(neighbour_bolds):
            temp_angle = self.cohesion(neighbour_bolds)
            self.separation(neighbour_bolds, temp_angle)
            self.alignment(neighbour_bolds)


        self.update_triangle()

    def update_triangle(self):
        self.triangle[0] = [self.loc[0] + 10 * math.cos(self.angle), self.loc[1] - 10 * math.sin(self.angle)]
        self.triangle[1] = [self.loc[0] + 8 * math.cos(self.angle + math.pi * 5/6), self.loc[1] - 8 * math.sin(self.angle + math.pi * 5/6)]
        self.triangle[2] = [self.loc[0] + 8 * math.cos(self.angle + math.pi * 7/6), self.loc[1] - 8 * math.sin(self.angle + math.pi * 7/6)]

    def check_around(self, boids, r=20):
        neighbour_bolds = []
        for b in boids:
            if (self.loc[0] - b.loc[0])**2 + (self.loc[1] - b.loc[1])**2 < r **2:
                neighbour_bolds.append(b)

        return neighbour_bolds

    def cohesion(self, neighbour_boids):
        middle = [sum([b.loc[0] for b in neighbour_boids])/len(neighbour_boids),
                  sum([b.loc[1] for b in neighbour_boids])/len(neighbour_boids)]

        return math.atan2(middle[1] - self.loc[1], middle[0] - self.loc[0])

    def separation(self, neighbour_boids, temp_angle):
        for i in range(7, 1):
            has_collision = False
            for b in neighbour_boids:
                if (self.loc[0] + math.cos(temp_angle)* 5 * i/8 - b.loc[0])**2 + (self.loc[1] - math.cos(temp_angle)* 5 * i/8 - b.loc[1])**2 < 10 **2:
                    has_collision = True
                    break
            if not has_collision:
                self.loc = [self.loc[0] + math.cos(temp_angle)* 5 * i/8, self.loc[0] - math.sin(temp_angle)* 5 * i/8]
                return

    def alignment(self, neighbour_boids):
        self.angle = sum([b.angle for b in neighbour_boids] + [self.angle])/(len(neighbour_boids) + 1)



class Flocking():

    master = Tkinter.Tk(className='Race game')

    def __init__(self):
        self.boids = [Boid() for _ in range(24)]

        for i in range(1, 7):
            for j in range(1, 5):
                self.boids[(i - 1)* 4 + (j - 1)].set(loc=[i*100, j*100], angle=math.pi *random.randrange(10)/10)

        self.canvas = Tkinter.Canvas(self.master, width=CANVAS_SIZE[0], height=CANVAS_SIZE[1])
        self.canvas.pack()

        self.master.after(0, self.draw)
        self.master.mainloop()

    def draw(self):
        self.canvas.delete(Tkinter.ALL)

        for i in range(len(self.boids)):
            self.boids[i].draw(self.canvas)

        self.update()
        self.master.after(20, self.draw)

    def update(self):
        for i in range(len(self.boids)):
            self.boids[i].update(self.boids[:i] + self.boids[i + 1:])


if __name__ == '__main__':
    flocking = Flocking()