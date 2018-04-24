__author__ = 'sunary'


def subsequence(array):
    lis = [array[0]]

    for i in range(1, len(array)):
        if array[i] > lis[-1]:
            lis.append(array[i])
        else:
            for j in range(0, len(lis)):
                if lis[j] > array[i]:
                    lis[j] = array[i]
                    break

    return lis


def subsequence_dp(array):
    pass


if __name__ == '__main__':
    print(subsequence([2, 6, 3, 4, 1, 2, 9, 5, 8]))