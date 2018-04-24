__author__ = 'sunary'


def find(array, a, b):
    pa = -1
    pb = -1
    min_distance = len(array)

    for i in range(len(array)):
        if a == array[i]:
            min_distance = min(min_distance, i - pb) if pb >= 0 else min_distance
            pa = i
        elif b == array[i]:
            min_distance = min(min_distance, i - pa) if pa >= 0 else min_distance
            pb = i

    return -1 if (min_distance == len(array)) else min_distance


print(find(["cat", "dog", "bird", "fish", "cat", "duck", "chicken", "dog"], "dog", "duck"))
print(find(["cat", "dog", "bird", "fish", "cat", "duck", "chicken", "dog"], "cat", "frog"))
