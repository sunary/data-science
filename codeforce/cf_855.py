__author__ = 'sunary'


def diary(names):
    name_set = set()
    output = []

    for n in names:
        if n in name_set:
            output.append('YES')
        else:
            name_set.add(n)
            output.append('NO')

    return '\n'.join(output)


def maxim(a, p, q, r):
    min_index = 0
    max_index = 0

    min_a = 1e9
    max_a = -1e9
    for i in range(len(a)):
        if a[i] > max_a:
            max_a = a[i]
            max_index = i
        if a[i] < min_a:
            min_a = a[i]
            min_index = i

    if max_index > min_index:
        return small_p(a[min_index:max_index])
    else:
        return max(small_p(a[:max_index], p, q, r), small_p(a[min_index:], p, q, r))


def small_p(a, p, q, r):
    pass


n = int(raw_input())
_names = [raw_input() for _ in range(n)]
print diary(_names)