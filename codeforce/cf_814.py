__author__ = 'sunary'


# http://codeforces.com/contest/814/


def sequence(a, b):
    if not is_increasing(a):
        return 'Yes'

    b = sorted(b, key=lambda x: -x)
    k = 0
    for i in range(len(a)):
        if a[i] == 0:
            a[i] = b[k]
            k += 1

    if not is_increasing(a):
        return 'Yes'
    else:
        return 'No'


def is_increasing(m):
    for i in range(len(m) - 1):
        if m[i] != 0 and m[i + 1] != 0 and m[i] >= m[i + 1]:
            return False

    return True


def rever(a, b):
    w = set([i + 1 for i in range(len(a))])
    for i in range(len(a)):
        if a[i] == b[i]:
            w.remove(a[i])

    while w:
        for i in range(len(a)):
            if a[i] != b[i]:
                if a[i] in w:
                    b[i] = a[i]
                    w.remove(a[i])
                elif b[i] in w:
                    a[i] = b[i]
                    w.remove(b[i])
                else:
                    if len(w) == 1:
                        a[i] = b[i] = w.pop()

    return ' '.join([str(x) for x in a])


def cir(s, q, c):
    max = 0
    e = 0
    for i in range(q):
        if s[i] == c:
            e += 1

    for i in range(len(s) - q):
        if s[i] == c:
            e -= 1
        if s[i + q] == c:
            e += 1
        if e > max:
            max = e

    return max + q

raw_input()
a = [int(x) for x in raw_input().split(' ')]
b = [int(x) for x in raw_input().split(' ')]
print rever(a, b)
