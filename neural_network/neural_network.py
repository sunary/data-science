__author__ = 'sunary'


from layer_network import LayerNetwork


class NeuralNetwork():

    def __init__(self, layer_nodes, using_sigmod=True):
        self.using_sigmod = using_sigmod
        self.layer = [LayerNetwork(i, self.using_sigmod) for i in layer_nodes]
        self.random_weight()

    def random_weight(self, range_random=2.0):
        for i in range(1, len(self.layer)):
            self.layer[i].random_weight(range_random, self.layer[i - 1].num_nut)

    def set_weight(self, weight):
        for i in range(1, len(self.layer)):
            self.layer[i].set_weight(weight[i - 1])

    def train(self, input, expected_id=None):
        # propagation
        self.layer[0].set_output_layer_first(input)
        for i in range(1, len(self.layer)):
            self.layer[i].propagation(self.layer[i - 1])

        output = self.layer[len(self.layer) - 1].output
        select_id = 0
        max_output = output[0]
        for i in range(1, len(output)):
            if max_output < output[i]:
                max_output = output[i]
                select_id = i

        if expected_id is not None:
            if self.using_sigmod:
                expected_output = [0] * self.layer[len(self.layer) - 1].num_nut
            else:
                expected_output = [-1] * self.layer[len(self.layer) - 1].num_nut
            expected_output[expected_id] = 1

            # back_propagation
            self.layer[len(self.layer) - 1].set_expected_output(expected_output)
            for i in range(len(self.layer) - 2, 0, -1):
                self.layer[i].back_propagation(self.layer[i - 1], self.layer[i + 1])

            # train
            for i in range(1, len(self.layer)):
                self.layer[i].train(self.layer[i - 1])

        return select_id


if __name__ == '__main__':
    xor_nn = NeuralNetwork([2, 4, 2])
    input = [[0, 0],
             [0, 1],
             [1, 0],
             [1, 1]]

    output = [0, 1, 1, 0]
    for i in range(4000):
        xor_nn.train(input[i % 4], output[i % 4])

    for i in range(4):
        print xor_nn.train(input[i])