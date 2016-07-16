__author__ = 'sunary'


from neural_network.model_nn import NeuralNetwork
import copy


class RecurrentNeuralNetwork(NeuralNetwork):

    def __init__(self, layer_nodes=None, using_sigmod=True):
        self.using_sigmod = using_sigmod
        self.recurrent_size = 2

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

        for j in range(len(input)):
            self.layer[0].set_output_layer_first(list(input[j]) + previous_result)

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
            for j in range(len(input)):
                expected_output = []

                if expected_id is not None:
                    if self.using_sigmod:
                        expected_output = [0] * self.layer[-1].num_nut
                    else:
                        expected_output = [-1] * self.layer[-1].num_nut
                    expected_output[expected_id[j]] = 1
                elif unexpected_id is not None:
                    expected_output = [1] * self.layer[-1].num_nut
                    if self.using_sigmod:
                        expected_output[unexpected_id[j]] = 0
                    else:
                        expected_output[unexpected_id[j]] = -1

                self.set_weight(saved_weight[j], saved_bias[j])

                # back_propagation
                delta = self.layer[-1].set_expected_output(expected_output + next_result)
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
    rnn = RecurrentNeuralNetwork([3, 3, 2])
    for _ in range(10):
        print rnn.train([[1, 1, 1], [0, 0, 0]], [1, 0])
        print rnn.train([[1, 1, 0], [0, 0, 1]], [1, 0])
        print rnn.train([[1, 0, 1], [0, 1, 0]], [1, 0])
        print rnn.train([[0, 1, 1], [1, 0, 0]], [1, 0])

    print rnn.train([[1, 1, 1], [0, 0, 0]])