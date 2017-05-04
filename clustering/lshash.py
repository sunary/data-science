__author__ = 'sunary'


import random


class LSHash(object):
    '''
    uniform_planes = np.array(item_value).reshape((self.num_hashtables, self.hash_size, self.input_dim)).tolist()
    <=>
    item_value = np.array(uniform_planes).flatten()
    '''
    def __init__(self, hash_size, input_dim, num_hashtables=1):
        self.hash_size = hash_size
        self.input_dim = input_dim
        self.num_hashtables = num_hashtables

        self.uniform_planes = [self._generate_uniform_planes() for _ in range(self.num_hashtables)]
        self.storage = [{} for _ in range(self.num_hashtables)]

    def _generate_uniform_planes(self):
        return [[4*(random.random() - 0.5) for _ in range(self.input_dim)]
                    for _ in range(self.hash_size)]

    def _hash(self, planes, input_point):
        '''
        return hash key by input_point
        xxx with x = {0,1}
        '''
        projections = [0] * self.hash_size
        for i in range(self.hash_size):
            for j in range(self.input_dim):
                projections[i] += planes[i][j] * input_point[j]

        return ''.join(['1' if i > 0 else '0' for i in projections])

    def index(self, input_point):
        for i in range(self.num_hashtables):
            key_hashed = self._hash(self.uniform_planes[i], input_point)
            if self.storage[i].get(key_hashed) is None:
                self.storage[i][key_hashed] = set()

            self.storage[i][key_hashed].add(input_point)

    def get_candidates(self, input_point):
        '''
        get candidates same hashed key
        '''
        candidates = set()
        for i in range(self.num_hashtables):
            key_hashed = self._hash(self.uniform_planes[i], input_point)
            this_table = self.storage[i].get(key_hashed)
            if this_table:
                candidates |= this_table

        return candidates


if __name__ == '__main__':
    lshash = LSHash(6, 8, 2)
    lshash.index((1, 2, 3, 4, 5, 6, 7, 8))
    lshash.index((2, 3, 4, 5, 6, 7, 8, 9))
    lshash.index((10, 12, 99, 1, 5, 31, 2, 3))
    print lshash.get_candidates((1, 2, 3, 4, 5, 6, 7, 7))