__author__ = 'sunary'


import itertools
import math


set_upper = 'ABCDEF'
set_lower = 'abcdef'
set_digit = '012345'

set_all = set_upper + set_lower + set_digit

set_password = set()


def gen():
    for u in set_upper:
        for l in set_lower:
            for d in set_digit:
                for a in set_all:
                    s = [u, l, d, a]
                    for p in itertools.permutations(s, 4):
                        set_password.add(''.join(p))

    assert len(set_password) == math.pow(6, 6)


if __name__ == '__main__':
    gen()