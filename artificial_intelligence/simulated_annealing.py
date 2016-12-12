__author__ = 'sunary'


import math
import random


def accept_probability(current_energy, new_energy, temp):
    if new_energy < current_energy:
        return True

    return math.exp((current_energy - new_energy)/temp) > random.random()


def main():
    temp = 10000
    cooling_rate = 0.003

    current_solution = ''
    best_solution = 'best solution'

    while temp > 1:
        if accept_probability():
            current_solution = 'new solution'

        if current_solution > best_solution:
            best_solution = current_solution

        temp *= 1 - cooling_rate


if __name__ == '__main__':
    main()