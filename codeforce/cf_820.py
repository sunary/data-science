__author__ = 'sunary'


def polygon(n, a):
    a_vertex = (n - 2)*180/n

    a_elem = a_vertex/(n - 2)

    d = 2
    d_a = a_elem
    while a > d_a:
        d_a += a_elem
        d += 1

    print a, (2*d_a - a_elem)/2
    if a > (2*d_a - a_elem)/2:
        return '{} {} {}'.format(1, d, 2)
    else:
        return '{} {} {}'.format(2, d, 1)

s = raw_input().split(' ')
print polygon(int(s[0]), int(s[1]))