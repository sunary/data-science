__author__ = 'sunary'


import Tkinter
import time


class Wall():

    def __init__(self, rect):
        self.rect = rect

    def draw(self, canvas):
        canvas.create_rectangle(*self.rect, fill='black')

class Car():

    def __init__(self, start, width, height):
        self.start = start
        self.width = width
        self.height = height

        self.v = self.width/20
        self.restart()

    def restart(self):
        self.mid = self.start
        self.angle = 0
        self.a1 = (self.mid[0] - self.width/2, self.mid[1] - self.height/2)
        self.a2 = (self.mid[0] + self.width/2, self.mid[1] - self.height/2)
        self.a3 = (self.mid[0] + self.width/2, self.mid[1] + self.height/2)
        self.a4 = (self.mid[0] - self.width/2, self.mid[1] + self.height/2)

    def draw(self, canvas):
        canvas.create_polygon(self.a1[0], self.a1[1], self.a2[0], self.a2[1], self.a3[0], self.a3[1], self.a4[0], self.a4[1], fill='blue')

    def update(self):
        pass


class RaceGame():
    root = Tkinter.Tk(className='Race game')

    def __init__(self):
        self.car = Car((225, 275), 45, 25)
        wall_position = [(0, 0, 450, 50),
                         (0, 300, 450, 350),
                         (0, 50, 50, 300),
                         (400, 50, 450, 300),
                         (100, 100, 150, 200),
                         (300, 100, 350, 200),
                         (200, 50, 250, 150),
                         (100, 200, 350, 250)]
        self.walls = [Wall(rect) for rect in wall_position]

        canvas = Tkinter.Canvas(self.root, width=450, height=350)
        canvas.pack()
        self.root.canvas = canvas.canvas = canvas

        while True:
            self.draw(canvas)
            self.root.mainloop()
            self.control()
            self.update()
            time.sleep(0.04)

    def draw(self, canvas):
        canvas.delete(Tkinter.ALL)

        for wall in self.walls:
            wall.draw(canvas)

        self.car.draw(canvas)


    def control(self):
        pass

    def update(self):
        pass


class NEAT():

    def __init__(self):
        self.race_game = RaceGame()

    def process(self):
        pass


if __name__ == '__main__':
    neat = NEAT()
    neat.process()
