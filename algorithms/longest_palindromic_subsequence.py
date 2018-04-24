__author__ = 'sunary'


def subsequence(array):
    n = len(array)
    index_array = [[0] * len(array) for _ in range(n)]

    for i in range(n):
        index_array[i][i] = 1

    for sl in range(2, n + 1):
        for i in range(n - sl + 1):
            j = sl + i - 1
            if array[i] == array[j] and sl == 2:
                index_array[i][j] = 2
            elif array[i] == array[j]:
                index_array[i][j] = index_array[i + 1][j - 1] + 2
            else:
                index_array[i][j] = max(index_array[i][j - 1], index_array[i + 1][j])

    return index_array[0][-1]


if __name__ == '__main__':
    print(subsequence('BBABCBCAB'))