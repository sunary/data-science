__author__ = 'sunary'


import math
import random
import copy


class LayerNetwork():
    '''
    layer of neural network
    '''
    shim = 1.0
    teaching_speed = 0.1

    def __init__(self, num_nut_layer, using_sigmod=True):
        self.using_sigmod = using_sigmod
        self.num_nut = num_nut_layer

        self.bias = [1.0] * self.num_nut
        self.output = [0] * self.num_nut
        self.delta = [0] * self.num_nut
        self.weight = [[] for _ in range(self.num_nut)]

    # only first layer need output
    def set_output_layer_first(self, input_model):
        self.output = input_model[:]

    def set_teaching_speed(self, speed):
        self.teaching_speed = speed

    def set_weight(self, input_weight, bias=None):
        self.weight = copy.deepcopy(input_weight)
        if bias:
            self.bias = bias[:]

    def random_weight(self, range_random, num_nut_previous_layer):
        random_weight = [[] for _ in range(self.num_nut)]
        for i in range(self.num_nut):
            random_weight[i] = [0]* num_nut_previous_layer
            for j in range(num_nut_previous_layer):
                random_weight[i][j] = 2*range_random*random.random() - range_random

        self.set_weight(random_weight)

    def propagation(self, previous_layer):
        for i in range(self.num_nut):
            temp = 0
            for j in range(previous_layer.num_nut):
                temp += self.weight[i][j]*previous_layer.output[j]
            self.output[i] = self.f_active(temp + self.bias[i])

    def back_propagation(self, previous_layer, next_layer):
        self.delta = [0]*self.num_nut
        for i in range(self.num_nut):
            temp = 0
            for j in range(previous_layer.num_nut):
                temp += self.weight[i][j]*previous_layer.output[j]
            for j in range(next_layer.num_nut):
                self.delta[i] += next_layer.weight[j][i]*next_layer.delta[j]

            self.delta[i] *= self.f_derivation(temp + self.bias[i])

        return self.delta

    def grad(self, previous_layer):
        for i in range(self.num_nut):
            for j in range(previous_layer.num_nut):
                self.weight[i][j] += self.teaching_speed*self.delta[i]*previous_layer.output[j]
            self.bias[i] += self.teaching_speed * self.delta[i] * self.bias[i]

    def set_expected_output(self, output_expected):
        for i in range(len(self.delta)):
            self.delta[i] = output_expected[i] - self.output[i]

        return self.delta

    def node_expected(self):
        max_value = 0
        id_node = 0
        for i in range(len(self.output)):
            if self.output[i] > max_value:
                max_value = self.output[i]
                id_node = i
        return id_node

    def f_active(self, x):
        if self.using_sigmod:
            # range [0, 1]
            return 1.0 / (math.exp(-x * self.shim) + 1.0)
        else:
            # range [-1, 1]
            return 1.0 - 2 / (math.exp(2*x * self.shim) + 1)

    def f_derivation(self, x):
        if self.using_sigmod:
            f_activation = self.f_active(x)
            return self.shim * f_activation*(1.0 - f_activation)
        else:
            f_activation = self.f_active(x)
            return self.shim * (1.0 - f_activation **2)