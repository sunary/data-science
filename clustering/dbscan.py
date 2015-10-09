__author__ = 'sunary'


class DBscan():

    def __init__(self):
        pass

    def input(self, data, min_pts, num_group = None, min_element = None):
        self.min_pts = min_pts**2

        self.dimension = len(data[0])
        self.data = data

        self.num_group = num_group
        self.min_element = min_element

        self.group = [-1]*len(self.data)

    def cluster(self):
        next_group = 0
        for i in range(len(self.data)):
            if self.group[i] < 0:
                self.group[i] = next_group
                next_group += 1
                for u in range(i + 1, len(self.data)):
                    if self.group[u] == -1 and self._euler_distance(self.data[i], self.data[u]) <= self.min_pts:
                        self.group[u] = self.group[i]

        #sort elements in groups
        num_elements = [0]*next_group
        for i in range(len(self.group)):
            num_elements[self.group[i]] += 1

        index_sorted = [i for i in range(next_group)]
        for i in range(len(num_elements)):
            for j in range(i + 1, len(num_elements)):
                if num_elements[i] < num_elements[j]:
                    temp = num_elements[i]
                    num_elements[i] = num_elements[j]
                    num_elements[j] = temp
                    temp = index_sorted[i]
                    index_sorted[i] = index_sorted[j]
                    index_sorted[j] = temp

        if self.min_element:
            self.num_group = 0
            while self.num_group < len(num_elements) and num_elements[self.num_group] > self.min_element:
                self.num_group += 1

        final_group = [-1]*len(self.group)
        for i in range(len(self.data)):
            for j in range(self.num_group):
                if self.group[i] == index_sorted[j]:
                    final_group[i] = j
                    break
        return final_group

    def _euler_distance(self, data1, data2):
        distance = 0
        for i in range(self.dimension):
            distance += (data1[i] - data2[i])**2

        return distance

if __name__ == '__main__':
    dbscan = DBscan()
    dbscan.input([[12, 123],
                    [32, 1],
                    [3, 32],
                    [6, 120],
                    [20, 89],
                    [50, 32],
                    [19, 23],
                    [20, 23],
                    [81, 45],
                    [45, 90],
                    [9, 34],
                    [90, 123],
                    [78, 36],
                    [17, 9],
                    [34, 21],
                    [100, 64],
                    [69, 78],
                    [60, 12],
                    [32, 54],
                    [75, 23],
                    [43, 100],
                    [82, 19]], 30, num_group= 5)
    print dbscan.cluster()