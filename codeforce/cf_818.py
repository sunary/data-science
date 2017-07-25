__author__ = 'sunary'


def olympia(N, k):
    d = N/2/(k + 1)
    c = k*d
    print '{} {} {}'.format(d, c, N - d -c)


def permutation(n, a):
    index = [0] * (n + 1)

    set_value = set()
    for i in range(1, len(a)):
        temp = (a[i] - a[i-1]) if (a[i] > a[i-1]) else (a[i] - a[i-1] + n)
        if index[a[i - 1]] == 0 or index[a[i-1]] == temp:
            index[a[i-1]] = (a[i] - a[i-1]) if (a[i] > a[i-1]) else (a[i] - a[i-1] + n)
            set_value.add(index[a[i-1]])
        else:
            return -1

    for i in range(1, n + 1):
        if index[i] == 0:
            for j in range(1, n + 1):
                if j not in set_value:
                    index[i] = 0
                    set_value.add(j)
                    break

    if len(set(index[1:])) < n:
        return -1

    return ' '.join([str(x) for x in index[1:]])


n = int(raw_input().split(' ')[0])
a = [int(x) for x in raw_input().split(' ')]
print permutation(n, a)






