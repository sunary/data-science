__author__ = 'sunary'


import math
import random


def accept_probability(current_energy, new_energy, temp):
    if new_energy < current_energy:
        return True

    return math.exp((current_energy - new_energy)/temp) > random.random()

# while t_new > stopping temp:
#      for number of runs at each temp:
#           x_new, y_new = random neighboring value of x_old, y_old
#           calculate the cost c_new of this neighboring solution
#           if   c_new – c_old >= 0:
#                This is a better solution, so move to it
#           else:
#                Calculate the probability of moving to the new worse solution
#                Probability moving  =  𝑒^((𝑐_𝑛𝑒𝑤  − 𝑐_𝑜𝑙𝑑)/𝑡_𝑛𝑒𝑤 )
#    t_new = t_new * cooling_rate

def main():
    temp = 10000
    cooling_rate = 0.003

    current_solution = 'init solution'
    best_solution = 'best solution'

    while temp > 1:
        if current_solution > best_solution:
            best_solution = current_solution
        elif accept_probability(current_energy, new_energy, temp):
            current_solution = 'new worse solution'

        temp *= (1 - cooling_rate)


if __name__ == '__main__':
    main()
