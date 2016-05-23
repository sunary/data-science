__author__ = 'sunary'


import random


def damage(true_damage, critical_hit):
    if random.randrange(1, 101) < critical_hit:
        return true_damage + true_damage * critical_hit/100
    else:
        return true_damage


def sub_amor(total_damage, amor):
    if amor >= 0:
        return total_damage * 100.0/(100 + amor)
    else:
        return total_damage * (2 - 100.0/(100 - amor))


if __name__ == '__main__':
    print damage(100, 30)
    print sub_amor(100, 25)
    print sub_amor(100, -20)