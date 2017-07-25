__author__ = 'sunary'


def gcd(a, b):
    return factor(a) if a < b else factor(b)


def factor(a):
    f = 1
    for i in range(2, a + 1):
        f *= i

    return f


def crossword(s, t):
    min_sub = 999999999
    min_replace = []

    for i in range(len(t) - len(s) + 1):
        count_sub = 0
        index_replace = []
        for j in range(len(s)):
            if t[i + j] != s[j]:
                count_sub += 1
                index_replace.append(j + 1)

        if count_sub < min_sub:
            min_sub = count_sub
            min_replace = index_replace[:]

    return '{}\n{}'.format(min_sub, ' '.join([str(i) for i in min_replace]))

raw_input()
s = raw_input()
t = raw_input()
print crossword(s, t)

