__author__ = 'sunary'

import math
import os
from random import randint


class LogisticRegression():

    POWER = 3

    def __init__(self):
        self.teaching_speed = 1.0
        self.theta = []
        self.traning_x = []
        self.traning_y = []

    def set_data_traning(self, data):
        for i in range(len(data)):
            self.traning_x.append([])
            self.traning_y.append(data[i][-1])
            for j in range(len(data[i]) - 1):
                self.traning_x[-1].append(data[i][j])

        for i in range(len(self.traning_x[0]) + 1):
            self.theta.append(randint(-5, 5))

    def set_data_traning_polynomial(self, data):
        for i in range(len(data)):
            self.traning_x.append([])
            self.traning_y.append(data[i][-1])
            for j in range(len(data[i]) - 1):
                self.traning_x[-1].append(data[i][j])

        self.theta.append(randint(-5, 5))
        for i1 in range(1, self.POWER):
            for i2 in range(i1 + 1):
                for i3 in range(i2 + 1):
                    self.theta.append(randint(-5, 5))

    def set_theta(self, theta):
        self.theta = theta

    def traning(self):
        for i in range(2000):
            self._cost()
            self._gradient()
            print self.j_theta
            print self.theta

        return self.theta

    def traning_polynomial(self):
        for i in range(2000):
            self._cost_polynomial()
            self._gradient_polynomial()
            print self.j_theta
            print self.theta

        return self.theta

    def test(self):
        case_match = 0
        for i in range(len(self.traning_x)):
            if not (self.get_classify(self.traning_x[i]) ^ self.traning_y[i]):
                case_match += 1

        print case_match*100.0/len(self.traning_x)

    def test_polynomial(self):
        case_match = 0
        for i in range(len(self.traning_x)):
            if not (self.get_classify_polynomial(self.traning_x[i]) ^ self.traning_y[i]):
                case_match += 1

        print case_match*100.0/len(self.traning_x)

    def _cost(self):
        self.j_theta = 0
        for i in range(len(self.traning_x)):
            h = self._sigmoid(self._fx(self.traning_x[i]))
            self.j_theta -= self.traning_y[i]*math.log(h) + (1 - self.traning_y[i])*math.log(1 - h)

        self.j_theta /= len(self.traning_x)

    def _cost_polynomial(self):
        self.j_theta = 0
        for i in range(len(self.traning_x)):
            h = self._sigmoid(self._fx_polynomial(self.traning_x[i]))
            self.j_theta -= self.traning_y[i]*math.log(h) + (1 - self.traning_y[i])*math.log(1 - h)

        for i in range(len(self.theta)):
            self.j_theta += self.teaching_speed/2*self.theta[i]**2

        self.j_theta /= len(self.traning_x)

    def _gradient(self):
        for j in range(len(self.theta)):
            sum_error = 0
            if j == 0:
                for i in range(len(self.traning_x)):
                    sum_error += self._sigmoid(self._fx(self.traning_x[i])) - self.traning_y[i]
            else:
                for i in range(len(self.traning_x)):
                    sum_error += (self._sigmoid(self._fx(self.traning_x[i])) - self.traning_y[i])*self.traning_x[i][j - 1]

            self.theta[j] -= self.teaching_speed*sum_error/len(self.traning_x)

    def _gradient_polynomial(self):
        for j in range(len(self.theta)):
            sum_error = 0

            for i in range(len(self.traning_x)):
                for i1 in range(1, self.POWER):
                    for i2 in range(i1 + 1):
                        for i3 in range(i2 + 1):
                            sum_error += (self._sigmoid(self._fx_polynomial(self.traning_x[i])) - self.traning_y[i])*(self.traning_x[i][0]**(i1 - i2))*(self.traning_x[i][1]**(i2 - i3))*self.traning_x[i][2]**i3
            if j != 0:
                sum_error -= self.teaching_speed*self.theta[j]

            self.theta[j] -= self.teaching_speed*sum_error/len(self.traning_x)

    def get_classify(self, x):
        return self._sigmoid(self._fx(x)) >= 0.5

    def get_classify_polynomial(self, x):
        return self._sigmoid(self._fx_polynomial(x)) >= 0.5

    def _fx(self, x):
        value = self.theta[0]
        for i in range(len(x)):
            value += self.theta[i + 1]*x[i]

        return value

    def _fx_polynomial(self, x):
        value = self.theta[0]
        count_theta = 1
        for i1 in range(1, self.POWER):
            for i2 in range(i1 + 1):
                for i3 in range(i2 + 1):
                    value += self.theta[count_theta]*(x[0]**(i1 - i2))*(x[1]**(i2 - i3))*x[2]**i3

        return value

    def _sigmoid(self, x):
        return 1.0 / (math.exp(-x) + 1.0)

#http://aimotion.blogspot.com/2011/11/machine-learning-with-python-logistic.html
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

    logistic_regression = LogisticRegression()

    logistic_regression.set_data_traning(data_skin)
    # logistic_regression.set_theta([-4.493786325701092, -6.370014854246775, 1.810082583197653, 8.754499417948777])
    # logistic_regression.traning()
    # logistic_regression.test()

    logistic_regression.set_data_traning_polynomial(data_skin)
    logistic_regression.set_theta([-2.420307580849564, 0.2886026874105773, 3.0393755185559446, 2.0393571553313623, 0.039320428882199276, 3.0393755185559446, 5.039412245005106, -1.9607162975669643, -3.960753024016128, 0.039320428882199276, 1.039338792106781, 5.039412245005106, 4.0393938817805255, -4.960771387240709])
    logistic_regression.traning_polynomial()
    logistic_regression.test_polynomial()