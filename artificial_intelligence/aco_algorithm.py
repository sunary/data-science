__author__ = 'sunary'


import random


class Ant():

    def __init__(self):
        self.cost = 0
        self.trace = [0]

    def start_travel(self):
        self.cost = 0
        self.trace = [0]

    def add_vertex(self, _vertex, _cost):
        self.trace.append(_vertex)
        self.cost += _cost

    def get_position(self):
        return self.trace[-1]

    def get_cost(self):
        return self.cost

    def get_path(self):
        path = []
        for i in range(len(self.trace) - 1):
            path.append((self.trace[i], self.trace[i + 1]))

        return path


class ACOAlgorithm():

    '''
    Ant colony optimization algorithms to find shortest path
    '''

    def __init__(self):
        self.evaporation_rate = 0.8
        self.threshhold = 0.5
        self.remain_path = 0

    def set_graph(self, graph):
        self.size = len(graph)

        self.num_ant = 20*self.size ** 2
        self.ant = [Ant() for _ in range(self.num_ant)]


        self.distance = graph
        self.pheromones = [[1.0]* self.size for _ in range(self.size)]

        max_distance = 0
        for i in range(len(self.distance)):
            for j in range(len(self.distance[0])):
                if self.distance[i][j] > max_distance:
                    max_distance = self.distance[i][j]

        for i in range(len(self.distance)):
            for j in range(len(self.distance[0])):
                if self.distance[i][j] > 0:
                    self.distance[i][j] /= max_distance*1.0
                else:
                    self.pheromones[i][j] = -1.0

    def process(self):
        while True:
            self._start_travel()
            self._find_edge()
            if self._finish_travel():
                break

        for i in range(self.num_ant):
            if len(self.ant[i].trace) == self.size:
                print 'trace %s' % (self.ant[i].trace)
                break

    def _start_travel(self):
        for i in range(self.num_ant):
            self.ant[i].start_travel()

    def _find_edge(self):
        while not self._have_ant_completed():
            for i in range(len(self.ant)):
                available_edge = 0
                for e in range(self.size):
                    if e not in self.ant[i].trace and self.pheromones[self.ant[i].get_position()][e] > 0:
                        available_edge +=  (2.0 - self.distance[self.ant[i].get_position()][e])*self.pheromones[self.ant[i].get_position()][e]

                last_e = -1
                prob_edge = 0
                prob_random = random.uniform(0.0, 1.0)
                for e in range(self.size):
                    if e not in self.ant[i].trace and self.pheromones[self.ant[i].get_position()][e] > 0:
                        prob_edge += (2.0 - self.distance[self.ant[i].get_position()][e])*self.pheromones[self.ant[i].get_position()][e]/available_edge
                        last_e = e
                        if prob_edge >= prob_random:
                            break
                if last_e >= 0:
                    self.ant[i].add_vertex(last_e, self.distance[self.ant[i].get_position()][last_e])
                else:
                    self.ant[i].start_travel()

    def _finish_travel(self):
        #find short path
        avg_cost = 0
        ant_completed = 0
        for i in range(len(self.ant)):
            if len(self.ant[i].trace) == self.size:
                avg_cost += self.ant[i].get_cost()
                ant_completed += 1
        avg_cost /= ant_completed

        #update pheromones
        for i in range(len(self.pheromones)):
            for j in range(len(self.pheromones[0])):
                if self.pheromones[i][j] > 0:
                    self.pheromones[i][j] *= (1 - self.evaporation_rate)

        for i in range(len(self.ant)):
            if self.ant[i].get_cost() < avg_cost:
                update_pheromones = self.ant[i].get_path()
                for x,y in update_pheromones:
                    self.pheromones[x][y]  += avg_cost/self.ant[i].get_cost()

        #remove path has small pheromones
        if self.remain_path > 2*(self.size - 1):
            for i in range(len(self.pheromones)):
                for j in range(len(self.pheromones[0])):
                    if self.pheromones[i][j] <= self.threshhold:
                        self.pheromones[i][j] = -1.0
        else:
            min_pheromones = 999999.99
            for i in range(len(self.pheromones)):
                for j in range(len(self.pheromones[0])):
                    if self.pheromones[i][j] > 0 and self.pheromones[i][j] < min_pheromones:
                        min_pheromones = self.pheromones[i][j]

            for i in range(len(self.pheromones)):
                for j in range(len(self.pheromones[0])):
                    if self.pheromones[i][j] <= min_pheromones:
                        self.pheromones[i][j] = -1.0

        #check exist only one path
        self.remain_path = 0
        for i in range(len(self.pheromones)):
            for j in range(len(self.pheromones[0])):
                if self.pheromones[i][j] > 0:
                    self.remain_path += 1

        return self.remain_path < self.size

    def _have_ant_completed(self):
        for i in range(len(self.ant)):
            if len(self.ant[i].trace) == self.size:
                return True
        return False


if __name__ == '__main__':
    aco = ACOAlgorithm()
    graph = [[-1, 5, 7, 9, 2],
             [5, -1, 12, 8, 6],
             [7, 12, -1, 13, 21],
             [9, 8, 13, -1, 9],
             [2, 6, 21, 9, -1]]
    aco.set_graph(graph)
    aco.process()