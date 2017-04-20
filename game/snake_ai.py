__author__ = 'sunary'


import Tkinter
import random


# https://github.com/stevennL/Snake

class Map(object):
    '''
    Board tile status:
        -3: food
        -2: wall/obstacle
        -1: border
        0 :empty
        n > 0: path index
    '''
    neighbor_index = ([-1, 0], [0, -1], [0, 1], [1, 0])

    def __init__(self, m, n):
        self.size = (m, n)
        self.board = self.create_board()

    def create_board(self):
        board = [[-1]*(self.size[1] + 2) for _ in range(self.size[0] + 2)]

        for i in range(1, self.size[0] + 1):
            for j in range(1, self.size[1] + 1):
                board[i][j] = 0

        return board

    def path_bfs(self, board, start):
        queue_path = list()
        queue_path.append(start)

        board[start[0]][start[1]] = 1
        while queue_path:
            current = queue_path[0]
            queue_path = queue_path[1:]

            for ni in self.neighbor_index:
                if board[current[0] + ni[0]][current[1] + ni[1]] == 0:
                    queue_path.append((current[0] + ni[0], current[1] + ni[1]))
                    board[current[0] + ni[0]][current[1] + ni[1]] = board[current[0]][current[1]] + 1

    def min_path(self, start, end=None):
        self.path_bfs(self.board, start)

        print self.board

    def max_path(self, start, end):
        invert_board = self.create_board()
        self.path_bfs(invert_board, end)

        for i in range(1, self.size[0] + 1):
            for j in range(1, self.size[1] + 1):
                if self.board[i][j] == -2:
                    invert_board[i][j] = -2

        current = start
        count = 1
        self.board[current[0]][current[1]] = count
        invert_board[current[0]][current[1]] = 0
        while True:
            neighbor_tiles = []
            for ni in self.neighbor_index:
                neighbor_tiles.append(invert_board[current[0] + ni[0]][current[1] + ni[1]])

            max_index_tile = self.max_agrs(neighbor_tiles)
            current = [current[0] + self.neighbor_index[max_index_tile][0],
                       current[1] + self.neighbor_index[max_index_tile][1]]

            count += 1
            self.board[current[0]][current[1]] = count
            invert_board[current[0]][current[1]] = 0

            if current == end:
                break

        print(self.board)

    def max_agrs(self, tiles):
        index_value = 0
        max_value = tiles[index_value]

        for i, t in enumerate(tiles):
            if t > max_value:
                max_value = t
                index_value = i

        return index_value

    def decide_next(self):
        pass


class Snake(object):

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


class SnakeAI(object):

    master = Tkinter.Tk(className='Snake')

    def __init__(self):
        self.size = (20, 20)
        self.width = 25
        self.snake = Snake(self.size)

        self.canvas = Tkinter.Canvas(self.master,
                                     width=self.width * self.size[0],
                                     height=self.width * self.size[1])
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
    map = Map(20, 30)
    map.max_path([1, 1], [19, 25])
