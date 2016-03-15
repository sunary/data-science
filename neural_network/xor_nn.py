__author__ = 'sunary'


from layer_network import LayerNetwork


class XorNeuralNetwork():
    '''
    xor function using neural network
    '''

    input = [[0, 0],
             [0, 1],
             [1, 0],
             [1, 1]]

    output = [0, 1, 1, 0]

    def __init__(self):
        self.layer_1st = LayerNetwork(2)
        self.layer_2nd = LayerNetwork(5)
        self.layer_3rd = LayerNetwork(5)
        self.layer_last = LayerNetwork(2)

        self.layer_2nd.random_weight(2, self.layer_1st.num_nut)
        self.layer_3rd.random_weight(2, self.layer_2nd.num_nut)
        self.layer_last.random_weight(2, self.layer_3rd.num_nut)

    def train(self, round):
        for _ in range(round):
            case_match = 0
            for i in range(len(self.input)):
                # propagation
                self.layer_1st.set_output_layer_first(self.input[i])
                self.layer_2nd.propagation(self.layer_1st)
                self.layer_3rd.propagation(self.layer_2nd)
                self.layer_last.propagation(self.layer_3rd)

                #check rate
                if self.layer_last.node_expected() == self.output[i]:
                    case_match += 1

                # back_propagation
                expected_output = [0]* self.layer_last.num_nut
                expected_output[self.output[i]] = 1
                self.layer_last.set_expected_output(expected_output)
                self.layer_3rd.back_propagation(self.layer_2nd, self.layer_last)
                self.layer_2nd.back_propagation(self.layer_1st, self.layer_3rd)

                # train
                self.layer_2nd.train(self.layer_1st)
                self.layer_3rd.train(self.layer_2nd)
                self.layer_last.train(self.layer_3rd)

            # print case_match*100.0/len(self.input)

    def test(self):
        for i in range(len(self.input)):
            self.layer_1st.set_output_layer_first(self.input[i])
            self.layer_2nd.propagation(self.layer_1st)
            self.layer_3rd.propagation(self.layer_2nd)
            self.layer_last.propagation(self.layer_3rd)
            print 0 if (self.layer_last.output[0] > self.layer_last.output[1]) else 1


if __name__ == '__main__':
    xor = XorNeuralNetwork()
    xor.train(4000)
    xor.test()