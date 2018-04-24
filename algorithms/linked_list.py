__author__ = 'sunary'


class Node(object):
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next = next_node

    def __str__(self):
        s = []
        while self:
            s.append(str(self.data))
            self = self.next

        return ' '.join(s)

    def __eq__(self, other):
        if self is None and other is None:
            return True
        if self and other and self.data == other.data:
            return self.next == other.next

        return False

    def add(self, next_node=None):
        head = self
        while head.next:
            head = head.next

        head.next = next_node

    def len(self):
        counter = 0
        while self:
            counter += 1
            self = self.next

        return counter


def reverse(a):
    current = a
    previous = None
    while current:
        next = current.next
        current.next = previous
        previous = current
        current = next

    return previous


def merge(a, b):
    m = None
    while True:
        if a and (not b or (a.data < b.data)):
            temp = Node(a.data, None)
            a = a.next
        else:
            temp = Node(b.data, None)
            b = b.next

        if m is None:
            m = temp
            head = m
        else:
            head.next = temp
            head = head.next

        if not (a or b):
            break

    return m


def remove_duplicate(a):
    current = a
    while current:
        next = current.next
        while next and current.data == next.data:
            current.next = next.next
            next = current.next

        current = current.next

    return a


def cycle_detect(a):
    head1 = a
    head2 = a.next

    while head2:
        if head1.data == head2.data:
            return 1
        head1 = head1.next
        if head2.next:
            head2 = head2.next.next
        else:
            head2 = None

    return 0


def find_merge_node(a, b):
    len_a = a.len()
    len_b = b.len()
    if len_a > len_b:
        for _ in range(len_a - len_b):
            a = a.next
    else:
        for _ in range(len_b - len_a):
            b = b.next

    while a != b:
        a = a.next
        b = b.next
    return a.data


def sorted_insert(a, i):
    previous = a
    head = previous.next

    while head.data < i:
        head = head.next
        previous = previous.next

    previous.next = Node(i, head)

    return a


def insert_tail(a, i):
    if not a:
        return Node(i, None)

    head = a
    while head:
        if head.next:
            head = head.next
        else:
            head.next = Node(i, None)
            break

    return a


def insert_head(a, i):
    head = a
    a = Node(i, head)
    return a


def insert_nth(a, i, n):
    head = a

    if n == 0:
        a = Node(i, head)
    else:
        for _ in range(n - 1):
            head = head.next

        head.next = Node(i, head.next)
    return a


def delete_node(a, n):
    head = a

    if n == 0:
        a = head.next
    else:
        for _ in range(n - 1):
            head = head.next

        head.next = head.next.next
    return a


def merge_and_reverse(a, b):
    m = None
    while a or b:
        if a and (not b or (a.data < b.data)):
            head = Node(a.data, m)
            a = a.next
        else:
            head = Node(b.data, m)
            b = b.next

        m = head

    return m


if __name__ == '__main__':
    a = Node(1, Node(3, Node(5, None)))
    b = Node(2, Node(4, Node(6, None)))
    c = Node(1, Node(2, Node(2, Node(4, Node(6, None)))))
    d = Node(1, Node(2, Node(2, Node(3, Node(3, Node(4, None))))))
    e = Node(1, Node(1, Node(1, Node(1, Node(1, None)))))
    # b1 = Node(5, a)
    # b2 = Node(5, Node(3, Node(2, a)))
    # print merge(a, b)
    # print remove_duplicate(d)
    # print find_merge_node(b1, b2)
    # print insert_tail(a, 4)
    # print insert_head(a, 4)
    # print insert_nth(a, 4, 1)
    # print delete_node(a, 2)
    print(merge_and_reverse(a, b))