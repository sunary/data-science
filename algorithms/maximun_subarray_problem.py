__author__ = 'sunary'


def kadane(array):
    max_ending_here = 0
    max_so_far = 0

    for elem in array:
        max_ending_here = max_ending_here + elem
        max_ending_here = max(max_ending_here, 0)
        max_so_far = max(max_so_far, max_ending_here)

    return max_so_far


if __name__ == '__main__':
    print(kadane([-2, 1, -3, 4, -1, 2, 1, -5, 4]))