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
        self.last_id = -1
        self.training_group = []

    def update(self):
        RaceGame.update(self)

        if self.is_broken:
            self.training_car()
            self.car.restart()
            self.last_id = -1
            self.training_group = []
        else:
            input = self.collision_sight + [self.car.angle]
            id_output = self.model.train(input)
            if (id_output <= self.len_delta/2 and self.last_id <= self.len_delta/2) or \
                    (id_output >= self.len_delta/2 and self.last_id >= self.len_delta/2):
                self.training_group.append((input, id_output))
            else:
                self.training_group = [(input, id_output)]
                self.last_id = id_output

            self.car.update(delta_angle=self.delta_angle[id_output])

    def training_car(self):
        for train_data in self.training_group:
            new_id = train_data[1]
            if self.car_collision_id < 2 and new_id < self.len_delta - 1:
                new_id += 1
            elif self.car_collision_id >= 2 and new_id > 0:
                new_id -= 1

            self.model.train(train_data[0], new_id)


if __name__ == '__main__':
    race_game = CarGenetic()