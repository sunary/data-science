__author__ = 'sunary'


from neural_network.model_nn import NeuralNetwork
from neural_network.race_game import RaceGame


class CarGenetic(RaceGame):

    def __init__(self):
        self.delta_angle = [-0.035, -0.03, -0.025, -0.02, -0.015, -0.01, -0.005, 0,
                            0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035]
        self.len_delta = len(self.delta_angle)
        self.nn_nodes = [5, 8, 5, self.len_delta]

        self.start()

        RaceGame.__init__(self)

    def start(self):
        self.model = NeuralNetwork(self.nn_nodes)
        self.step = 0
        self.max_step = 0
        self.training_group = []
        self.best_traning = []

    def update(self):
        RaceGame.update(self)

        if self.is_broken:
            self.training_car()
            self.car.restart()
            self.training_group = []
            self.step = 0
        else:
            input = self.collision_sight + [self.car.angle]
            id_output = self.model.train(input)
            self.training_group.append((input, id_output))
            self.step += 1

            self.car.update(delta_angle=self.delta_angle[id_output])

    def training_car(self):
        num_last_step = 5
        if self.step > self.max_step:
            self.max_step = self.step
            self.best_traning = self.training_group[:-num_last_step]

            for train_data in self.best_traning:
                self.model.train(train_data[0], expected_id=train_data[1])

        for train_data in self.training_group[-num_last_step:]:
            self.model.train(train_data[0], unexpected_id=train_data[1])


if __name__ == '__main__':
    race_game = CarGenetic()