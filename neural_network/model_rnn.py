__author__ = 'sunary'


from neural_network.model_nn import NeuralNetwork
import copy


class RecurrentNeuralNetwork(NeuralNetwork):

    def __init__(self, layer_nodes=None, using_sigmod=True):
        self.using_sigmod = using_sigmod
        self.recurrent_size = 1

        if layer_nodes:
            layer_nodes[0] += self.recurrent_size
            layer_nodes[-1] += self.recurrent_size
            self.random_weight(2.0, layer_nodes)

    def train(self, input, expected_id=None, unexpected_id=None):
        saved_weight = []
        saved_bias = []

        # propagation
        previous_result = [0] * self.recurrent_size
        select_id = []

        for j in range(len(input[0])):
            input_layer = [inp[j] for inp in input]
            self.layer[0].set_output_layer_first(input_layer + previous_result)

            temp_weight = []
            temp_bias = []
            for i in range(1, len(self.layer)):
                self.layer[i].propagation(self.layer[i - 1])
                temp_weight.append(copy.deepcopy(self.layer[i].weight))
                temp_bias.append(copy.deepcopy(self.layer[i].bias))

            saved_weight.append(temp_weight)
            saved_bias.append(temp_bias)
            previous_result = self.layer[-1].output[-self.recurrent_size:]

            output = self.layer[-1].output[:-self.recurrent_size]
            max_output = output[0]
            select_id.append(0)

            for i in range(1, len(output)):
                if max_output < output[i]:
                    max_output = output[i]
                    select_id[-1] = i

        if (expected_id is None) and (unexpected_id is None):
            return select_id
        else:
            next_result = [1] * self.recurrent_size
            cost = 0

            expected_output = []
            if expected_id is not None:
                for i in range(len(expected_id)):
                    if self.using_sigmod:
                        expected_output.append([0] * self.layer[-1].num_nut)
                    else:
                        expected_output.append([-1] * self.layer[-1].num_nut)
                    expected_output[-1][expected_id[i]] = 1
            elif unexpected_id is not None:
                for i in range(len(unexpected_id)):
                    expected_output.append([1] * self.layer[-1].num_nut)
                    if self.using_sigmod:
                        expected_output[-1][unexpected_id[i]] = 0
                    else:
                        expected_output[-1][unexpected_id[i]] = -1

            for j in range(len(expected_output) - 1, -1, -1):
                self.set_weight(saved_weight[j], saved_bias[j])

                # back_propagation
                delta = self.layer[-1].set_expected_output(expected_output[len(expected_output) - j - 1] + next_result)
                cost += sum([d**2 for d in delta])

                for i in range(len(self.layer) - 2, 0, -1):
                    delta = self.layer[i].back_propagation(self.layer[i - 1], self.layer[i + 1])
                    cost += sum([d**2 for d in delta])

                # gradient
                for i in range(1, len(self.layer)):
                    self.layer[i].grad(self.layer[i - 1])

                # cal output after gradient
                for i in range(1, len(self.layer)):
                    self.layer[i].propagation(self.layer[i - 1])

                next_result = self.layer[0].output[-self.recurrent_size:]

            return cost


if __name__ == '__main__':
    import numpy as np
    import random

    largest_number = 2 **8
    binary = np.unpackbits(np.array([range(largest_number)], dtype=np.uint8).T, axis=1)

    rnn = RecurrentNeuralNetwork([2, 3, 2])
    for _ in range(10000):
        a = random.randrange(largest_number/2)
        b = random.randrange(largest_number/2)
        c = a + b

        a = binary[a]
        b = binary[b]
        c = binary[c]

        a = [a[len(a) - i - 1] for i in range(len(a))]
        b = [b[len(b) - i - 1] for i in range(len(b))]
        c = [c[len(c) - i - 1] for i in range(len(c))]

    for _ in range(10):
        a = random.randrange(largest_number/2)
        b = random.randrange(largest_number/2)
        c = a + b

        a = binary[a]
        b = binary[b]
        c = binary[c]

        a = [a[len(a) - i - 1] for i in range(len(a))]
        b = [b[len(b) - i - 1] for i in range(len(b))]
        c = [c[len(c) - i - 1] for i in range(len(c))]

        print rnn.train([a, b])
        print c
        print '--'