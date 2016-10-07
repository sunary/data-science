__author__ = 'sunary'


import math


def elo_ratio(rank_1, rank_2):
    sc_1 = 1.0/(1 + math.pow(10, (rank_2 - rank_1)/400.0))
    sc_2 = 1.0/(1 + math.pow(10, (rank_1 - rank_2)/400.0))

    return sc_1, sc_2


def game_elo(rank_1, rank_2, p1_win, k):
    sc_1, sc_2 = elo_ratio(rank_1, rank_2)

    if p1_win:
        rank_1 += k * (1 - sc_1)
        rank_2 += k * (0 - sc_2)
    else:
        rank_1 += k * (0 - sc_1)
        rank_2 += k * (1 - sc_2)

    return rank_1, rank_2


if __name__ == '__main__':
    rank_1 = 1000
    rank_2 = 2300
    k = 24

    print game_elo(rank_1, rank_2, True, k)
    print game_elo(rank_1, rank_2, False, k)