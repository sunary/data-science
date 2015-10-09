__author__ = 'sunary'

import os

class Kmean():

    def __init__(self):
        pass

    def input(self, data, num_cluster):
        self.num_cluster = num_cluster
        self.dimension = len(data[0])

        self.data = data
        self.group = [gp % self.num_cluster for gp in range(len(data))]
        self.previous_group = [0]*len(self.group)

        self.center = []

    def cluster(self):
        while self._has_change():
            # cal center
            count_element_in_group = [0]*len(self.group)
            self.center = [[0]*self.dimension for _ in range(self.num_cluster)]
            for i in range(len(self.data)):
                count_element_in_group[self.group[i]] += 1
                for j in range(self.dimension):
                    self.center[self.group[i]][j] += self.data[i][j]

            for i in range(self.num_cluster):
                for j in range(self.dimension):
                    self.center[i][j] /= count_element_in_group[i]*1.0

            # determine group by distance
            for i in range(len(self.data)):
                distance = [0]*self.num_cluster
                for j in range(self.num_cluster):
                    for k in range(self.dimension):
                        distance[j] += (self.data[i][k] - self.center[j][k])**2

                min_distance = distance[0]
                self.group[i] = 0
                for j in range(1, self.num_cluster):
                    if distance[j] < min_distance:
                        min_distance = distance[j]
                        self.group[i] = j

            return self.group

    def _has_change(self):
        different_group = False
        for i in range(len(self.group)):
            if self.group[i] != self.previous_group[i]:
                different_group = True
                break
        if different_group:
            for i in range(len(self.group)):
                self.previous_group[i] = self.group[i]

        return different_group

if __name__ == '__main__':
    current_dir = os.path.dirname(__file__)

    fo = open(current_dir + '/../resources/skin.txt')
    data_skin = fo.read()
    data_skin = data_skin.split('\n')
    for i in range(len(data_skin)):
        data_skin[i] = data_skin[i].split('\t')
        for j in range(len(data_skin[i]) - 1):
            data_skin[i][j] = int(data_skin[i][j])/255.0
        data_skin[i][3] = 0 if (data_skin[i][3] == '2') else 1


    kmean = Kmean()
    kmean.input(data_skin, 5)
    print kmean.cluster()