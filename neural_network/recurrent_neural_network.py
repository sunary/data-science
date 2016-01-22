__author__ = 'sunary'


from layer_network import LayerNetwork


class RecurrentNeuralNetwork():

    def __init__(self, layer_nodes, length_layer, use_sigmod=True):
        assert len(layer_nodes) == 3

        self.length_layer = length_layer
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
        saved_hidden_level = []

        for i in range(self.length_layer):
            if i:
                saved_hidden_level.append(self.layer[1].weight)
            else:
                saved_hidden_level.append([0] * len(self.layer[1].weight))

            new_input = input + saved_hidden_level[i]

        if expected_id:
            pass

        return None


if __name__ == '__main__':
    pass