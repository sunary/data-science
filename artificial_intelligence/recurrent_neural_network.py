__author__ = 'sunary'


from layer_network import LayerNetwork


class RecurrentNeuralNetwork():

    def __init__(self, layer_nodes, use_sigmod=True):
        self.use_sigmod = use_sigmod
        self.layer = [LayerNetwork(i, self.use_sigmod) for i in layer_nodes]
        self.prev_hiddent_layer = LayerNetwork(layer_nodes[1], self.use_sigmod)
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
        max_output = -1
        for i in range(len(output)):
            if max_output < output[i]:
                max_output = output[i]
                select_id = i

        if expected_id:
            if self.use_sigmod:
                expected_output = [0] * self.layer[len(self.layer) - 1].num_nut
            else:
                expected_output = [-1] * self.layer[len(self.layer) - 1].num_nut
            expected_output[expected_id] = 1

            # back_propagation
            self.layer[len(self.layer) - 1].set_expected_output(expected_output)
            for i in range(len(self.layer) - 2, 0, -1):
                self.layer[i].back_propagation(self.layer[i - 1], self.layer[i + 1])

            #train
            for i in range(1, len(self.layer)):
                self.layer[i].train(self.layer[i - 1])

        return select_id


if __name__ == '__main__':
    pass