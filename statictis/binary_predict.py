__author__ = 'sunary'


import itertools
import random


class BinaryPredict():

    def __init__(self):
        self.size = 7
        self.binary_statistic = [{} for _ in range(self.size)]

        for i in range(self.size):
            bag_binary = self.get_binary(i + 1)
            for bin in bag_binary:
                self.binary_statistic[i][bin] = 0

    def process(self):
        self.train()
        self.test()

    def train(self):
        self.keep_binary = ''
        for i in xrange(1000000):
            self.add_bin()

    def add_bin(self, bin=None):
        if bin is None:
            bin = str(random.randint(0, 1))

        self.keep_binary += bin
        self.keep_binary = self.keep_binary[-self.size:]

        for s in range(self.size):
            if len(self.keep_binary) > s:
                self.binary_statistic[s][self.keep_binary[-s - 1:]] += 1

    def get_binary(self, len):
        '''
        Cartesian product binary has lengh len
        Examples:
            >>> get_binary(2):
            ['00', '01', '10', '11']
        '''
        bag_binary = []
        for p in itertools.product('01', repeat = len):
            bag_binary.append(''.join(x for x in p))

        return bag_binary

    def predict(self):
        '''
        predict next binary using statistic
        '''
        statistic_case_0 = 0
        statistic_case_1 = 0

        for i in range(self.size):
            prefix_bin = self.get_binary(i)
            for bin in prefix_bin:
                statistic_case_0 += self.binary_statistic[i].get(bin + '0')
                statistic_case_1 += self.binary_statistic[i].get(bin + '1')

        return '0' if statistic_case_0 > statistic_case_1 else '1'

    def test(self):
        total_case = 1000
        right_case = 0
        for _ in xrange(total_case):
            bin_predict = self.predict()
            bin_random = str(random.randint(0, 1))

            if bin_predict == bin_random:
                right_case += 1

            self.add_bin(bin_random)

        print right_case*1.0/total_case


if __name__ == '__main__':
    binary_predict = BinaryPredict()
    binary_predict.process()