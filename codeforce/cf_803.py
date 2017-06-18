__author__ = 'sunary'


# http://codeforces.com/contest/803


def fill_matrix(n, k):
    m = [[0]*n for _ in range(n)]
    for i in range(n):
        m[i][i] = 1
        k -= 1
        if k == 0:
            return m
        for j in range(i + 1, n):
            if k >= 2:
                m[i][j] = m[j][i] = 1
                k -= 2
            if k == 0:
                return m