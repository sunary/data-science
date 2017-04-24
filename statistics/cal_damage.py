__author__ = 'sunary'


import random


def damage(true_damage, critical_hit):
    if random.randrange(1, 101) < critical_hit:
        return true_damage + true_damage * critical_hit/100
    else:
        return true_damage


def sub_armor(total_damage, armor):
    if armor >= 0:
        return total_damage * 100.0/(100 + armor)
    else:
        return total_damage * (2 - 100.0/(100 - armor))


if __name__ == '__main__':
    print damage(100, 30)
    print sub_armor(100, 25)
    print sub_armor(100, -20)