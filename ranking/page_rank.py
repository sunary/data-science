__author__ = 'sunary'


import math


class PageRank():

    def __init__(self):
        self.d = 0.85
        self.epsilon = 10**-3

    def input(self, vertex, edge):
        self.vertex_score = [1.0]*vertex
        self.num_connection = [0]*vertex
        self.matrix_connection = [[False]*vertex for _ in range(vertex)]

        for e in edge:
            self.num_connection[e[0]] += 1
            self.num_connection[e[1]] += 1
            self.matrix_connection[e[0]][e[1]] = True
            self.matrix_connection[e[1]][e[0]] = True

    def process(self):
        while True:
            new_vertex_score = [0]* len(self.vertex_score)
            for i in range(len(self.vertex_score)):
                sum_outbound = 0
                for j in range(len(self.vertex_score)):
                    if self.matrix_connection[i][j]:
                        sum_outbound += self.vertex_score[j]/self.num_connection[j]
                new_vertex_score[i] = (1 - self.d) + self.d*sum_outbound

            max_epsilon = 0.0
            for i in range(len(self.vertex_score)):
                max_epsilon = max(max_epsilon, math.fabs(self.vertex_score[i] - new_vertex_score[i]))
                self.vertex_score[i] = new_vertex_score[i]
            if max_epsilon < self.epsilon:
                return self.vertex_score


if __name__ == '__main__':
    pagerank = PageRank()
    pagerank.input(8, [[0,1], [0,3], [1,2], [1,3], [1,4], [2,4], [2,5], [3,7], [4,5], [4,6], [5,7]])
    print pagerank.process()