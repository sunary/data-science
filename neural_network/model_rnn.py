__author__ = 'sunary'


from neural_network.model_nn import NeuralNetwork


class RecurrentNeuralNetwork():

    def __init__(self, layer_nodes=None, len_sequence=None):
        self.len_sequence = len_sequence

        self.recurrent_size = 2

        if layer_nodes:
            layer_nodes[0] += self.recurrent_size
            layer_nodes[-1] += self.recurrent_size

        self.nn = [NeuralNetwork(layer_nodes=layer_nodes) for _ in range(self.len_sequence)]

    def train(self, input, expected_id=None, unexpected_id=None):
        previous_result = [0] * self.recurrent_size
        select_id = []

        remember_variable = [previous_result]

        # propagation
        for j in range(self.len_sequence):
            input_layer = [inp[j] for inp in input]
            self.nn[j].layer[0].set_output_layer_first(input_layer + previous_result)

            for i in range(1, len(self.nn[j].layer)):
                self.nn[j].layer[i].propagation(self.nn[j].layer[i - 1])

            previous_result = self.nn[j].layer[-1].output[-self.recurrent_size:]
            previous_result = [1, 0] if previous_result[0] > previous_result[1] else [0, 1]
            remember_variable.append(previous_result)

            output = self.nn[j].layer[-1].output[:-self.recurrent_size]
            select_id.append(0 if output[0] > output[1] else 1)

        if (expected_id is None) and (unexpected_id is None):
            return select_id
        else:
            next_result = [1] * self.recurrent_size
            cost = 0

            expected_output = []
            if expected_id is not None:
                for j in range(self.len_sequence):
                    expected_output.append([0] * (self.nn[j].layer[-1].num_nut - self.recurrent_size))
                    expected_output[-1][expected_id[j]] = 1
            elif unexpected_id is not None:
                for j in range(self.len_sequence):
                    expected_output.append([1] * (self.nn[j].layer[-1].num_nut - self.recurrent_size))
                    expected_output[-1][unexpected_id[j]] = 0

            # back_propagation
            for j in range(self.len_sequence)[::-1]:
                delta = self.nn[j].layer[-1].set_expected_output(expected_output[j] + next_result)
                cost += sum([d**2 for d in delta])

                for i in range(1, len(self.nn[j].layer) - 1)[::-1]:
                    delta = self.nn[j].layer[i].back_propagation(self.nn[j].layer[i - 1], self.nn[j].layer[i + 1])
                    cost += sum([d**2 for d in delta])

                # gradient
                for i in range(1, len(self.nn[j].layer)):
                    self.nn[j].layer[i].grad(self.nn[j].layer[i - 1])

                next_result = remember_variable[j - 1]

            return cost


if __name__ == '__main__':
    pass
