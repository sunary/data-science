__author__ = 'sunary'


from neural_network.model_nn import NeuralNetwork
import copy


class RecurrentNeuralNetwork(NeuralNetwork):

    def __init__(self, layer_nodes=None):
        self.using_sigmod = True

        self.recurrent_size = 2

        if layer_nodes:
            layer_nodes[0] += self.recurrent_size
            layer_nodes[-1] += self.recurrent_size
            self.random_weight(2.0, layer_nodes)

    def set_sequence(self, len_sequence):
        self.len_sequence = len_sequence

        self.saved_weight = [None] * self.len_sequence
        self.saved_bias = [None] * self.len_sequence

        for j in range(self.len_sequence):
            temp_weight = []
            temp_bias = []
            for i in range(1, len(self.layer)):
                temp_weight.append(copy.deepcopy(self.layer[i].weight))
                temp_bias.append(copy.deepcopy(self.layer[i].bias))

            self.saved_weight[j] = temp_weight
            self.saved_bias[j] = temp_bias

    def train(self, input, expected_id=None, unexpected_id=None):
        previous_result = [0] * self.recurrent_size
        select_id = []

        remember_variable = [previous_result]

        # propagation
        for j in range(self.len_sequence):
            self.set_weight(self.saved_weight[j], self.saved_bias[j])

            input_layer = [inp[j] for inp in input]
            self.layer[0].set_output_layer_first(input_layer + previous_result)

            temp_weight = []
            temp_bias = []
            for i in range(1, len(self.layer)):
                self.layer[i].propagation(self.layer[i - 1])
                temp_weight.append(copy.deepcopy(self.layer[i].weight))
                temp_bias.append(copy.deepcopy(self.layer[i].bias))

            self.saved_weight[j] = temp_weight
            self.saved_bias[j] = temp_bias

            previous_result = self.layer[-1].output[-self.recurrent_size:]
            previous_result = [0, 1] if previous_result[1] > previous_result[0] else [1, 0]
            remember_variable.append(previous_result)

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
                for j in range(self.len_sequence):
                    expected_output.append([0] * (self.layer[-1].num_nut - self.recurrent_size))
                    expected_output[-1][expected_id[j]] = 1
            elif unexpected_id is not None:
                for j in range(self.len_sequence):
                    expected_output.append([1] * (self.layer[-1].num_nut - self.recurrent_size))
                    expected_output[-1][unexpected_id[j]] = 0

            # back_propagation
            for j in range(self.len_sequence)[::-1]:
                self.set_weight(self.saved_weight[j], self.saved_bias[j])

                delta = self.layer[-1].set_expected_output(expected_output[j] + next_result)
                cost += sum([d**2 for d in delta])

                for i in range(1, len(self.layer) - 1)[::-1]:
                    delta = self.layer[i].back_propagation(self.layer[i - 1], self.layer[i + 1])
                    cost += sum([d**2 for d in delta])

                # gradient
                for i in range(1, len(self.layer)):
                    self.layer[i].grad(self.layer[i - 1])

                # cal output after gradient
                for i in range(1, len(self.layer)):
                    self.layer[i].propagation(self.layer[i - 1])

                next_result = remember_variable[j]

                temp_weight = []
                temp_bias = []
                for i in range(1, len(self.layer)):
                    temp_weight.append(copy.deepcopy(self.layer[i].weight))
                    temp_bias.append(copy.deepcopy(self.layer[i].bias))

                self.saved_weight[j] = temp_weight
                self.saved_bias[j] = temp_bias

            return cost


if __name__ == '__main__':
    pass