__author__ = 'sunary'


from artificial_intelligence.race_game import RaceGame
from artificial_intelligence.neural_network import NeuralNetwork
import random


class NEAT(RaceGame):

    def __init__(self):
        self.delta_angle = [-0.03, -0.02, -0.01, 0, 0.01, 0.02, 0.03]
        self.nn_nodes = [5, 8, 5, 7]
        self.start()

        RaceGame.__init__(self)

    def start(self):
        self.gen = 1
        self.size = 0
        for i in range(1, len(self.nn_nodes)):
            self.size += self.nn_nodes[i - 1]*self.nn_nodes[i]

        self.len_selection = 20
        range_random = 2.0
        self.chromosome_weight = [[(2*range_random * random.random() - range_random) for _ in range(self.size)]
                                  for _ in range(self.len_selection)]

        self.step_record = [0] * self.len_selection
        self.model_id = 0
        self.model = self.get_model(self.chromosome_weight[self.model_id])

    def get_model(self, weight):
        model = NeuralNetwork(self.nn_nodes)

        nn_weight = []
        for i in range(1, len(self.nn_nodes)):
            layer_weight = []
            for _ in range(self.nn_nodes[i]):
                layer_weight.append(weight[:self.nn_nodes[i - 1]])
                weight = weight[self.nn_nodes[i - 1]:]

            nn_weight.append(layer_weight)
        model.set_weight(nn_weight)

        return model

    def update(self):
        RaceGame.update(self)

        self.step_record[self.model_id] += 1
        if self.is_broken:
            self.model_id += 1
            if self.model_id == len(self.chromosome_weight):
                self.evaluation()
                self.selection()
                self.crossover()
                self.mutation()

                self.step_record = [0] * len(self.chromosome_weight)
                self.model_id = 0

            self.model = self.get_model(self.chromosome_weight[self.model_id])
            self.car.restart()
        else:
            self.car.update(delta_angle=self.get_angle(self.collision_sight + [self.car.angle]))

    def get_angle(self, input):
        id = self.model.train(input)
        return self.delta_angle[id]

    def evaluation(self):
        print 'Gen: %s, max: %s steps' % (self.gen, max(self.step_record))
        self.gen += 1

        fitness = [0] * len(self.chromosome_weight)
        sum_steps = sum(self.step_record)
        for i in range(len(self.chromosome_weight)):
            fitness[i] = float(self.step_record[i])/sum_steps

        self.probability = [0]*len(self.chromosome_weight)

        self.probability[0] = fitness[0]
        for i in range(1, len(fitness)):
            self.probability[i] = self.probability[i - 1] + fitness[i]

    def selection(self):
        object_selected = []
        for _ in range(self.len_selection):
            id = self.id_selection(random.random(), self.probability)
            object_selected.append(self.chromosome_weight[id])

        self.chromosome_weight = object_selected

    def id_selection(self, p, list_probability):
        for i in range(len(list_probability)):
            if p <= list_probability[i]:
                return i
        return len(list_probability) - 1

    def crossover(self):
        object_crossover = []
        for i in range(len(self.chromosome_weight)):
            for j in range(len(self.chromosome_weight)):
                if i != j:
                    len_crossover = random.randint(1, self.size - 1)
                    object_crossover.append(self.chromosome_weight[i][:len_crossover] + self.chromosome_weight[j][len_crossover:])

        self.chromosome_weight += object_crossover

    def mutation(self):
        object_mutation = []
        for _ in range(len(self.chromosome_weight)/5):
            chromosome_mutation = self.chromosome_weight[random.randint(0, len(self.chromosome_weight) - 1)]
            position_mutation = random.randint(0, self.size - 1)
            value_mutation = random.random()/5 + chromosome_mutation[position_mutation]
            chromosome_mutation[position_mutation] = value_mutation

            object_mutation.append(chromosome_mutation)

        self.chromosome_weight += object_mutation


if __name__ == '__main__':
    race_game = NEAT()