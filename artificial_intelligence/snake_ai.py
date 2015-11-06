__author__ = 'sunary'


import Tkinter
import random


class Snake():

    def __init__(self, size):
        self.size = size
        self.board = [[0]*self.size[1] for _ in range(self.size[0])]

        self.tile = []

    def len(self):
        return len(self.tile)

    def head(self):
        return self.tile[0]

    def tail(self):
        return self.tile[self.len() - 1]

    def move(self, dir):
        self.tile = [dir] + self.tile[:-1]
        self.order()

    def eat(self, food):
        self.tile = [food] + self.tile
        self.order()

    def order(self):
        self.board = [[0]*self.size[1] for _ in range(self.size[0])]
        for i in range(self.len()):
            self.board[self.tile[i][0]][self.tile[i][1]] = i + 1

    def random_food(self):
        food = (random.randint(0, self.size[0]), random.randint(0, self.size[1]))
        self.board[food[0]][food[1]] = -1
        return food

    def path_to(self, dir):
        path = []

        return path

class SnakeAI():

    master = Tkinter.Tk(className='Snake')

    def __init__(self):
        self.size = (20, 20)
        self.width = 25
        self.snake = Snake(self.size)

        self.canvas = Tkinter.Canvas(self.master, width=self.width * self.size[0], height=self.width * self.size[1])
        self.canvas.pack()

        self.master.after(0, self.draw)
        self.master.mainloop()

    def draw(self):
        self.canvas.delete(Tkinter.ALL)

        self.update()
        self.master.after(20, self.draw)

    def update(self):
        pass


if __name__ == '__main__':
    snake_ai = SnakeAI()
