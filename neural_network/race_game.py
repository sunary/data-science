__author__ = 'sunary'


import Tkinter
import math


class Wall():

    def __init__(self, rect):
        self.rect = rect

    def draw(self, canvas):
        canvas.create_rectangle(*self.rect, fill='black')

    def check_in(self, point):
        return (point[0] >= self.rect[0] and point[0] <= self.rect[2]) and (point[1] >= self.rect[1] and point[1] <= self.rect[3])

    def check_collision(self, line):
        four_edges = (((self.rect[0], self.rect[1]), (self.rect[2], self.rect[1])),
                        ((self.rect[2], self.rect[1]), (self.rect[2], self.rect[3])),
                        ((self.rect[2], self.rect[3]), (self.rect[0], self.rect[3])),
                        ((self.rect[0], self.rect[3]), (self.rect[0], self.rect[1])))

        intersect = []
        for edge in four_edges:
            intersect.append(self.intersect(edge, line))

        return intersect

    def intersect(self, line1, line2):
        '''
        intersect 2 lines
        '''
        point = None
        s1_x = float(line1[1][0] - line1[0][0])
        s1_y = float(line1[1][1] - line1[0][1])

        s2_x = float(line2[1][0] - line2[0][0])
        s2_y = float(line2[1][1] - line2[0][1])

        try:
            s = (-s1_y * (line1[0][0] - line2[0][0]) + s1_x * (line1[0][1] - line2[0][1])) / (-s2_x * s1_y + s1_x * s2_y)
            t = ( s2_x * (line1[0][1] - line2[0][1]) - s2_y * (line1[0][0] - line2[0][0])) / (-s2_x * s1_y + s1_x * s2_y)
        except:
            return point

        if (s >= 0 and s <= 1) and (t >= 0 and t <= 1):
            point = ((line1[0][0] + (t * s1_x)), (line1[0][1] + (t * s1_y)))

        return point


class Car():

    def __init__(self, start, width, height):
        self.start = start
        self.width = width
        self.height = height

        self.r_sight = 2*width

        self.v = self.width*1.0/30

        self.relative_vertexts = [[self.width/2, -self.height/2],
                                [-self.width/2, -self.height/2],
                                [-self.width/2, self.height/2],
                                [self.width/2, self.height/2]]

        self.relative_sights = [[0, -self.r_sight],
                                [math.sqrt(2)*self.r_sight/2, -math.sqrt(2)*self.r_sight/2],
                                [self.r_sight, 0],
                                [math.sqrt(2)*self.r_sight/2, math.sqrt(2)*self.r_sight/2],
                                [0, self.r_sight]]

        self.restart()

    def restart(self):
        self.mid = self.start
        self.angle = math.pi

        self.vertexs = [[0, 0] for _ in range(4)]
        self.sights = [[0, 0] for _ in range(5)]

        self.cal_vertext()

    def draw(self, canvas):
        canvas.create_polygon(self.vertexs[0][0], self.vertexs[0][1], self.vertexs[1][0], self.vertexs[1][1],
                              self.vertexs[2][0], self.vertexs[2][1], self.vertexs[3][0], self.vertexs[3][1], fill='blue')

        canvas.create_oval(self.mid[0] - self.r_sight, self.mid[1] - self.r_sight, self.mid[0] + self.r_sight, self.mid[1] + self.r_sight, outline='red')
        for i in range(len(self.sights)):
            canvas.create_line(self.mid[0], self.mid[1], self.sights[i][0], self.sights[i][1], fill='red')

    def update(self, delta_angle=0):
        self.angle += delta_angle

        vx = self.v * math.cos(self.angle)
        vy = self.v * math.sin(self.angle)
        self.mid = [self.mid[0] + vx, self.mid[1] + vy]

        self.cal_vertext()

    def cal_vertext(self):
        for i in range(len(self.vertexs)):
            x = self.relative_vertexts[i][0]
            y = self.relative_vertexts[i][1]
            new_x = x*math.cos(self.angle) - y*math.sin(self.angle)
            new_y = y*math.cos(self.angle) + x*math.sin(self.angle)

            self.vertexs[i][0] = self.mid[0] + new_x
            self.vertexs[i][1] = self.mid[1] + new_y

        for i in range(len(self.sights)):
            x = self.relative_sights[i][0]
            y = self.relative_sights[i][1]
            new_x = x*math.cos(self.angle) - y*math.sin(self.angle)
            new_y = y*math.cos(self.angle) + x*math.sin(self.angle)

            self.sights[i][0] = self.mid[0] + new_x
            self.sights[i][1] = self.mid[1] + new_y


class RaceGame():
    master = Tkinter.Tk(className='Race game')

    def __init__(self):
        self.car = Car((225, 275), 45, 25)
        wall_position = [(0, 0, 450, 50),
                         (0, 300, 450, 350),
                         (0, 0, 50, 350),
                         (400, 0, 450, 350),
                         (100, 100, 150, 250),
                         (300, 100, 350, 250),
                         (200, 50, 250, 150),
                         (100, 200, 350, 250)]
        self.walls = [Wall(rect) for rect in wall_position]

        self.canvas = Tkinter.Canvas(self.master, width=450, height=350)
        self.canvas.pack()

        self.master.after(0, self.draw)
        self.master.mainloop()

    def draw(self):
        self.canvas.delete(Tkinter.ALL)
        for wall in self.walls:
            wall.draw(self.canvas)

        self.car.draw(self.canvas)

        self.update()
        self.master.after(20, self.draw)

    def update(self):
        self.is_broken = False
        for point in self.car.vertexs:
            for wall in self.walls:
                if wall.check_in(point):
                    self.is_broken = True
                    break

        self.collision_sight = [1]*len(self.car.sights)
        if not self.is_broken:
            for i in range(len(self.car.sights)):
                for wall in self.walls:
                    points_collision = wall.check_collision((self.car.mid, self.car.sights[i]))
                    for point in points_collision:
                        if point:
                            self.collision_sight[i] = min(self.collision_sight[i],
                                                          math.sqrt(((self.car.mid[0] - point[0])**2) + (self.car.mid[1] - point[1])**2)/self.car.r_sight)


if __name__ == '__main__':
    race_car = RaceGame()