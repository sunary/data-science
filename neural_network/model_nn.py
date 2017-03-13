__author__ = 'sunary'


from neural_network.layer_nn import LayerNetwork
from array import array


class NeuralNetwork(object):

    def __init__(self, layer_nodes=None, using_sigmod=True):
        self.using_sigmod = using_sigmod
        if layer_nodes:
            self.random_weight(2.0, layer_nodes)

    def create_layers(self, layer_nodes=None):
        if layer_nodes:
            self.layer = [LayerNetwork(i, self.using_sigmod) for i in layer_nodes]

    def random_weight(self, range_random=2.0, layer_nodes=None):
        self.create_layers(layer_nodes)
        for i in range(1, len(self.layer)):
            self.layer[i].random_weight(range_random, self.layer[i - 1].num_nut)

    def set_weight(self, weight, bias=None, layer_nodes=None):
        self.create_layers(layer_nodes)
        for i in range(1, len(self.layer)):
            set_bias = bias[i - 1] if bias else None
            self.layer[i].set_weight(weight[i - 1], set_bias)

    def train(self, input, expected_id=None, unexpected_id=None):
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

        if (expected_id is None) and (unexpected_id is None):
            return select_id
        else:
            expected_output = []

            if expected_id is not None:
                if self.using_sigmod:
                    expected_output = [0] * self.layer[len(self.layer) - 1].num_nut
                else:
                    expected_output = [-1] * self.layer[len(self.layer) - 1].num_nut
                expected_output[expected_id] = 1
            elif unexpected_id is not None:
                expected_output = [1] * self.layer[len(self.layer) - 1].num_nut
                if self.using_sigmod:
                    expected_output[unexpected_id] = 0
                else:
                    expected_output[unexpected_id] = -1

            # back_propagation
            cost = 0
            delta = self.layer[len(self.layer) - 1].set_expected_output(expected_output)
            cost += sum([d**2 for d in delta])

            for i in range(1, len(self.layer) - 1)[::-1]:
                delta = self.layer[i].back_propagation(self.layer[i - 1], self.layer[i + 1])
                cost += sum([d**2 for d in delta])

            # gradient
            for i in range(1, len(self.layer)):
                self.layer[i].grad(self.layer[i - 1])

            return cost

    def save(self, filename='model.dat'):
        float_array = array('d', [])

        float_array.append(len(self.layer))
        for layer in self.layer:
            float_array.append(layer.num_nut)

        for layer in self.layer[1:]:
            for i in range(len(layer.weight)):
                for j in range(len(layer.weight[0])):
                    float_array.append(layer.weight[i][j])

            for i in range(layer.num_nut):
                float_array.append(layer.bias[i])

        fo = open(filename, 'wb')
        float_array.tofile(fo)
        fo.close()

    def load(self, filename='model.dat'):
        fo = open(filename, 'rb')
        float_array = array('d')
        float_array.fromstring(fo.read())
        fo.close()

        num_layer = int(float_array[0])
        nn_weight = []
        bias = []

        layer_nodes = float_array[1:num_layer + 1]
        layer_nodes = [int(x) for x in layer_nodes]
        float_array = float_array[num_layer + 1:]

        for i in range(1, len(layer_nodes)):
            layer_weight = []
            for _ in range(layer_nodes[i]):
                layer_weight.append(float_array[:layer_nodes[i - 1]])
                float_array = float_array[layer_nodes[i - 1]:]

            nn_weight.append(layer_weight)

            bias.append(float_array[:layer_nodes[i]])
            float_array = float_array[layer_nodes[i]:]

        self.set_weight(nn_weight, bias, layer_nodes)


if __name__ == '__main__':
    xor_nn = NeuralNetwork([2, 4, 2])
    input = [[0, 0],
             [0, 1],
             [1, 0],
             [1, 1]]

    output = [0, 1, 1, 0]
    for i in range(4000):
        print xor_nn.train(input[i % 4], output[i % 4])

    for i in range(4):
        print xor_nn.train(input[i])

    xor_nn.save()

    xor_nn = NeuralNetwork()
    xor_nn.load()
    for i in range(4):
        print xor_nn.train(input[i])