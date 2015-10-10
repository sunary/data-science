__author__ = 'sunary'


import random
import math


class Vertex():

    def __init__(self):
        self.visited = False
        self.id = 0
        self.pos = [0, 0]
        self.disp = [0, 0]

    def set_pos(self, pos):
        self.pos = pos

    def set_disp(self, disp):
        self.disp = disp

    def pos_norm(self):
        return self.pos[0]**2 + self.pos[1]**2

    def disp_norm(self):
        return self.disp[0]**2 + self.disp[1]**2


class Graph():

    def __init__(self, vertex):
        self.num_vertex = vertex
        self.vertex = [Vertex() for _ in range(vertex)]

    def set_edge(self, edge):
        self.num_edge = len(edge)
        self.edge = edge


#Fruchterman and Reingold algorithm
class ForceDirected():
    WIDTH = 400
    HEIGHT = 400

    def __init__(self):
        self.t = self.WIDTH*0.05

    def input(self, vertex, edge):
        self.graph = Graph(vertex)
        self.graph.set_edge(edge)
        self.k = math.sqrt(self.WIDTH*self.WIDTH*1.0 / self.graph.num_vertex)

        for i in range(self.graph.num_vertex):
            self.graph.vertex[i].set_pos([self.WIDTH/3*(random.random() - 0.5), self.HEIGHT/3*(random.random() - 0.5)])

    def process(self):
        num_loops = 40
        for i in range(num_loops):
            # calculate repulsive forces
            for v1 in range(self.graph.num_vertex):
                self.graph.vertex[v1].set_disp([0, 0])

                for v2 in range(self.graph.num_vertex):
                    if v1 != v2:
                        temp_vertex = Vertex()
                        temp_vertex.set_pos([self.graph.vertex[v1].pos[0] - self.graph.vertex[v2].pos[0], self.graph.vertex[v1].pos[1] - self.graph.vertex[v2].pos[1]])
                        norm = temp_vertex.pos_norm()
                        norm = 1 if norm == 0 else norm

                        self.graph.vertex[v1].disp[0] += temp_vertex.pos[0]*self._fr(norm)/norm
                        self.graph.vertex[v1].disp[1] += temp_vertex.pos[1]*self._fr(norm)/norm

			# calculate attractive forces
            for v in range(self.graph.num_vertex):
                self.graph.vertex[v].visited = False

            for e in range(self.graph.num_edge):
                if not self.graph.vertex[self.graph.edge[e][1]].visited:
                    temp_vertex = Vertex()
                    temp_vertex.set_pos([self.graph.vertex[self.graph.edge[e][0]].pos[0] - self.graph.vertex[self.graph.edge[e][1]].pos[0], self.graph.vertex[self.graph.edge[e][0]].pos[1] - self.graph.vertex[self.graph.edge[e][1]].pos[1]])

                    norm = temp_vertex.pos_norm()
                    norm = 1 if norm == 0 else norm

                    self.graph.vertex[self.graph.edge[e][0]].disp[0] -= temp_vertex.pos[0]*self._fa(norm)/norm
                    self.graph.vertex[self.graph.edge[e][0]].disp[1] -= temp_vertex.pos[1]*self._fa(norm)/norm

                    self.graph.vertex[self.graph.edge[e][1]].disp[0] -= temp_vertex.pos[0]
                    self.graph.vertex[self.graph.edge[e][1]].disp[1] -= temp_vertex.pos[1]

                self.graph.vertex[self.graph.edge[e][0]].visited = True

			# arrange positions to fit the canvas
            for v in range(self.graph.num_vertex):
                norm = self.graph.vertex[v].disp_norm()
                norm = 1 if norm == 0 else norm

                self.graph.vertex[v].pos[0] += (self.graph.vertex[v].disp[0]/norm) *min(math.fabs(self.graph.vertex[v].disp[0]), self.t)
                self.graph.vertex[v].pos[1] += (self.graph.vertex[v].disp[1]/norm) *min(math.fabs(self.graph.vertex[v].disp[1]), self.t)

                self.graph.vertex[v].pos[0] = min(self.WIDTH/2, max(-self.WIDTH/2, self.graph.vertex[v].pos[0]))
                self.graph.vertex[v].pos[1] = min(self.HEIGHT/2, max(-self.HEIGHT/2, self.graph.vertex[v].pos[1]))

            self.t = self.t*(num_loops- i)/num_loops;

        return [[vertex.pos[0] + self.WIDTH/2, vertex.pos[1] + self.HEIGHT/2]  for vertex in self.graph.vertex]

    def _fr(self, x):
        return self.k**2/x

    def _fa(self, x):
        return x**2/self.k


if __name__ == '__main__':
    force_directed = ForceDirected()
    force_directed.input(8, [[0,1], [0,3], [1,2], [1,3], [1,4], [2,4], [2,5], [3,7], [4,5], [4,6], [5,7]])
    print force_directed.process()