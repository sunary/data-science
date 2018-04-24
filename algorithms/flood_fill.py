__author__ = 'sunary'


index = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]

def run(n, a):
    counter = 1
    for i in range(n):
        for j in range(n):
            if a[i][j] == '1':
                counter += 1
                set_point = set()
                set_point.add((i, j))
                while set_point:
                    i2, j2 = set_point.pop()
                    for id in index:
                        if check_bound(n, i2 + id[0], j2 + id[1]) and a[i2 + id[0]][j2 + id[1]] == '1':
                            set_point.add((i2 + id[0], j2 + id[1]))
                            a[i2 + id[0]][j2 + id[1]] = counter

    return counter - 1


def check_bound(n, x, y):
    return x >= 0 and x < n and y >= 0 and y < n


N = int(raw_input())
S = [raw_input().split(' ') for _ in range(N)]

print(run(N, S))
