__author__ = 'sunary'


import random


class GeneticAlgorithm():

    '''
    Solve: a + b + c + d = 100
    with a, b, c, d >= 0
    '''

    def __init__(self):
        self.size = 4

    def start(self):
        self.len_selection = 10
        self.chromosome = [[random.randint(0, 100) for _ in range(self.size)] for _ in range(self.len_selection)]

    def process(self):
        self.start()

        while True:
            is_answer = self.evaluation()
            if is_answer:
                return is_answer
            self.selection()
            self.crossover()
            self.mutation()

    def f(self, para):
        return abs(sum(para) - 100)

    def evaluation(self):
        '''
        evaluate chromosomes
        '''
        fitness = [0]*len(self.chromosome)

        for i in range(len(self.chromosome)):
            fitness[i] = self.f(self.chromosome[i])
            if fitness[i] == 0:
                return self.chromosome[i]
            fitness[i] = 1.0/fitness[i]

        sum_fitness = sum(fitness)
        self.probability = [0]*len(self.chromosome)

        self.probability[0] = fitness[0]/sum_fitness
        for i in range(1, len(fitness)):
            self.probability[i] = self.probability[i - 1] + fitness[i]/sum_fitness

        return False

    def selection(self):
        '''
        select best chromosomes by evaluation
        '''
        object_selected = []
        for _ in range(self.len_selection):
            id = self.id_selection(random.random(), self.probability)
            object_selected.append(self.chromosome[id])

        self.chromosome = object_selected

    def id_selection(self, p, list_probability):
        for i in range(len(list_probability)):
            if p <= list_probability[i]:
                return i
        return len(list_probability) - 1

    def crossover(self):
        '''
        crossover each other by random position [0:size-1]
        '''
        object_crossover = []
        for i in range(len(self.chromosome)):
            for j in range(len(self.chromosome)):
                if i != j:
                    len_crossover = random.randint(1, self.size - 1)
                    object_crossover.append(self.chromosome[i][:len_crossover] + self.chromosome[j][len_crossover:])

        self.chromosome += object_crossover

    def mutation(self):
        object_mutation = []
        for _ in range(random.randint(0, len(self.chromosome))):
            chromosome_mutation = self.chromosome[random.randint(0, len(self.chromosome) - 1)]
            position_mutation = random.randint(0, self.size - 1)
            value_mutation = (random.randint(0, 4) - 2) + chromosome_mutation[position_mutation]
            value_mutation = 0 if value_mutation <= 0 else value_mutation
            chromosome_mutation[position_mutation] = value_mutation

            object_mutation.append(chromosome_mutation)

        self.chromosome += object_mutation


if __name__ == '__main__':
    genetic_algorithm = GeneticAlgorithm()
    print genetic_algorithm.process()