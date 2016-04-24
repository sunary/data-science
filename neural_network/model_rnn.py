__author__ = 'sunary'


from neural_network.model_nn import NeuralNetwork
import copy


class RecurrentNeuralNetwork(NeuralNetwork):

    def __init__(self, layer_nodes=None, using_sigmod=True):
        self.using_sigmod = using_sigmod
        if layer_nodes:
            layer_nodes = [n + 1 for n in layer_nodes]
            layer_nodes[-2] -= 1
            self.random_weight(2.0, layer_nodes)

    def train(self, input, expected_id=None, unexpected_id=None):
        saved_layer = []

        # propagation
        previous_result = 0
        for j in range(len(input)):
            self.layer[0].set_output_layer_first(input[j] + [previous_result])

            temp_layer = []
            for i in range(1, len(self.layer)):
                self.layer[i].propagation(self.layer[i - 1])
                temp_layer.append(copy.deepcopy(self.layer[i].weight))

            saved_layer.append(temp_layer)

            previous_result = self.layer[len(self.layer) - 1].output[-1]

        output = self.layer[len(self.layer) - 1].output[:-1]
        select_id = 0
        max_output = output[0]
        for i in range(1, len(output)):
            if max_output < output[i]:
                max_output = output[i]
                select_id = i

        if (expected_id is not None) or (unexpected_id is not None):
            next_result = 1
            for j in range(len(input)):
                expected_output = []

                if expected_id is not None:
                    if self.using_sigmod:
                        expected_output = [0] * self.layer[len(self.layer) - 1].num_nut
                    else:
                        expected_output = [-1] * self.layer[len(self.layer) - 1].num_nut
                    expected_output[expected_id[j]] = 1
                elif unexpected_id is not None:
                    expected_output = [1] * self.layer[len(self.layer) - 1].num_nut
                    if self.using_sigmod:
                        expected_output[unexpected_id[j]] = 0
                    else:
                        expected_output[unexpected_id[j]] = -1

                # back_propagation
                self.layer[len(self.layer) - 1].set_expected_output(expected_output + [next_result])
                for i in range(len(self.layer) - 2, 0, -1):
                    self.layer[i].back_propagation(self.layer[i - 1], self.layer[i + 1])

                # gradient
                for i in range(1, len(self.layer)):
                    self.layer[i].grad(self.layer[i - 1])

                # cal outout after gradient
                for i in range(1, len(self.layer)):
                    self.layer[i].propagation(self.layer[i - 1])

                next_result = self.layer[1].output[-1]

        return select_id


if __name__ == '__main__':
    rnn = RecurrentNeuralNetwork([2, 3, 2])
    rnn.train([[1, 1], [0, 0]], [1, 0])