__author__ = 'sunary'


import itertools
import random
import math
import fractions


class BinaryPredict():

    def __init__(self):
        self.size = 10

        self.way_one = False

        if self.way_one:
            self.keep_size = self.size
        else:
            self.keep_size = reduce(lambda x, y: (x * y)//fractions.gcd(x, y), range(2, self.size + 1))

        self.binary_statistic = [{} for _ in range(self.size)]

        for i in range(self.size):
            bag_binary = self.get_binary(i + 1)
            self.binary_statistic[i]['last'] = 0
            for bin in bag_binary:
                self.binary_statistic[i][bin] = 0

    def process(self):
        self.train()
        self.test()

    def train(self):
        self.keep_binary = ''
        for i in xrange(100000):
            self.add_bin()

    def add_bin(self, bin=None):
        if bin is None:
            bin = str(random.randint(0, 1))

        self.keep_binary += bin
        if self.way_one:
            self.statistic_1()
        else:
            self.statistic_2()

    def statistic_1(self):
        self.keep_binary = self.keep_binary[-self.keep_size:]

        for s in range(self.size):
            if len(self.keep_binary) > s:
                self.binary_statistic[s][self.keep_binary[-s - 1:]] += 1

    def predict_1(self):
        '''
        predict next binary using statistic
        '''
        statistic_case_0 = 0
        statistic_case_1 = 0

        for i in range(self.size):
            prefix_bin = self.get_binary(i)
            for bin in prefix_bin:
                statistic_case_0 += self.binary_statistic[i].get(bin + '0') * math.pow(2, i)
                statistic_case_1 += self.binary_statistic[i].get(bin + '1') * math.pow(2, i)

        return '0' if statistic_case_0 > statistic_case_1 else '1'

    def statistic_2(self):
        for i in range(self.size):
            if len(self.keep_binary) - self.binary_statistic[i]['last'] == i + 1:
                self.binary_statistic[i][self.keep_binary[self.binary_statistic[i]['last']:]] += 1
                self.binary_statistic[i]['last'] += (i + 1)

        if len(self.keep_binary) == self.keep_size:
            self.keep_binary = ''
            for i in range(self.size):
                self.binary_statistic[i]['last'] = 0

    def predict_2(self):
        statistic_case_0 = 0
        statistic_case_1 = 0

        for i in range(self.size):
            if i == 0:
                statistic_case_0 += self.binary_statistic[0].get('0')
                statistic_case_1 += self.binary_statistic[0].get('1')
            else:
                last_bin = self.keep_binary[(self.binary_statistic[i]['last'] + 1):]
                remain_bin = self.get_binary(i - len(last_bin))
                for bin in remain_bin:
                    statistic_case_0 += self.binary_statistic[i].get(last_bin + '0' + bin) * math.pow(2, i)
                    statistic_case_1 += self.binary_statistic[i].get(last_bin + '1' + bin) * math.pow(2, i)

        return '0' if statistic_case_0 > statistic_case_1 else '1'

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

    def test(self):
        total_case = 1000
        right_case = 0
        for _ in xrange(total_case):
            if self.way_one:
                bin_predict = self.predict_1()
            else:
                bin_predict = self.predict_2()
            bin_random = str(random.randint(0, 1))

            if bin_predict == bin_random:
                right_case += 1

            self.add_bin(bin_random)

        print right_case*1.0/total_case


if __name__ == '__main__':
    binary_predict = BinaryPredict()
    binary_predict.process()