__author__ = 'sunary'


list_number = [1, 2, 2, 4, 8, 12, 34, 2, 67, 23, 38, 25, 17, 15, 91, 28]
M = 117


def dynamic_programming():
    if all_sum(list_number, checker=M) is True:
        return 'Yes'
    else:
        return 'No'


def meet_in_the_middle():
    list1 = list_number[:len(list_number)/2]
    all_sum1 = all_sum(list1, checker=M)
    if all_sum1 is True:
        return 'Yes'

    list2 = list_number[len(list_number)/2:]
    all_sum2 = all_sum(list2, checker=M)
    if all_sum2 is True:
        return 'Yes'

    # all_sum1 = list(all_sum1); all_sum1.sort()
    # all_sum2 = list(all_sum2); all_sum2.sort()

    for n1 in all_sum1:
        for n2 in all_sum2:
            if (n1 + n2) == M:
                return 'Yes'
            elif (n1 + n2) > M:
                break

    return 'No'


def all_sum(list_num, checker):
    result_to = set()

    for i in range(len(list_num)):
        set_num = set()

        for x in result_to:
            if add_to_set(set_num, x + list_num[i], checker):
                return True

        result_to.add(list_num[i])
        result_to.update(set_num)

    return result_to


def add_to_set(set_num, num, checker):
    if num == M:
        return True
    elif num < M:
        set_num.add(num)

    return False


if __name__ == '__main__':
    print dynamic_programming()
    print meet_in_the_middle()