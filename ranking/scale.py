__author__ = 'sunary'


import math


class Scale():

    def __init__(self):
        pass

    @staticmethod
    def standard_competition_ranking(sequence):
        '''
        Examples:
            >>> Scale.standard_competition_ranking([1, 2, 2, 4])
            [1, 2, 2, 4]
        '''
        order = Scale.get_order(sequence)
        sequence = sorted(sequence)
        index = [1]*len(sequence)

        len_same_ranking = 1
        for i in range(1, len(sequence)):
            if sequence[i] == sequence[i - 1]:
                index[i] = index[i - 1]
                len_same_ranking += 1
            else:
                index[i] = index[i - 1] + len_same_ranking
                len_same_ranking = 1

        ranking = [1]*len(sequence)
        for i in range(len(sequence)):
            ranking[i] = index[order[i] - 1]

        return ranking

    @staticmethod
    def modified_competition_ranking(sequence):
        '''
        Examples:
            >>> Scale.modified_competition_ranking([1, 2, 2, 4])
            [1, 3, 3, 4]
        '''
        order = Scale.get_order(sequence)
        sequence = sorted(sequence)
        index = [1]*len(sequence)

        len_same_ranking = 1
        first_value = True
        for i in range(1, len(sequence)):
            if sequence[i] == sequence[i - 1]:
                index[i] = index[i - 1]
                len_same_ranking += 1
                if i == len(sequence) - 1:
                    value_same_ranking = index[i] + len_same_ranking - 1
                    for j in range(i - len_same_ranking + 1, i + 1):
                        index[j] = value_same_ranking
            else:
                index[i] = index[i - 1] + len_same_ranking
                if first_value:
                    value_same_ranking = 1
                    first_value = False
                else:
                    value_same_ranking = index[i] - 1
                for j in range(i - len_same_ranking, i):
                    index[j] = value_same_ranking

                if i == len(sequence) - 1:
                    index[i] = len(sequence)
                else:
                    len_same_ranking = 1

        ranking = [1]*len(sequence)
        for i in range(len(sequence)):
            ranking[i] = index[order[i] - 1]

        return ranking

    @staticmethod
    def dense_ranking(sequence):
        '''
        Examples:
            >>> Scale.dense_ranking([1, 2, 2, 4])
            [1, 2, 2, 3]
        '''
        order = Scale.get_order(sequence)
        sequence = sorted(sequence)
        index = [1]*len(sequence)

        for i in range(1, len(sequence)):
            if sequence[i] == sequence[i - 1]:
                index[i] = index[i - 1]
            else:
                index[i] = index[i - 1] + 1

        ranking = [1]*len(sequence)
        for i in range(len(sequence)):
            ranking[i] = index[order[i] - 1]

        return ranking

    @staticmethod
    def ordinal_ranking(sequence):
        '''
        Examples:
            >>> Scale.ordinal_ranking([1, 2, 2, 4])
            [1, 2, 3, 4]
        '''
        ranking = Scale.get_order(sequence)
        return ranking

    @staticmethod
    def fractional_ranking(sequence):
        '''
        Examples:
            >>> Scale.fractional_ranking([1, 2, 2, 4])
            [1.0, 2.5, 2.5, 4.0]
        '''
        order = Scale.get_order(sequence)
        sequence = sorted(sequence)
        index = order[::]

        len_same_ranking = 1
        for i in range(1, len(sequence)):
            if sequence[i] == sequence[i - 1]:
                len_same_ranking += 1
                if i == len(sequence) - 1:
                    value_same_ranking = sum([x + 1 for x in range(i - len_same_ranking + 1, i + 1)])*1.0/len_same_ranking
                    for j in range(i - len_same_ranking + 1, i + 1):
                        index[j] = value_same_ranking
            else:
                value_same_ranking = sum([x + 1 for x in range(i - len_same_ranking, i)])*1.0/len_same_ranking
                for j in range(i - len_same_ranking, i):
                    index[j] = value_same_ranking

                if i == len(sequence) - 1:
                    index[i] = len(sequence)*1.0
                else:
                    len_same_ranking = 1

        ranking = [1]*len(sequence)
        for i in range(len(sequence)):
            ranking[i] = index[order[i] - 1]

        return ranking

    @staticmethod
    def get_order(sequence):
        '''
        Examples:
            >>> Scale.get_order([5, 3, 7, 2])
            [3, 2, 4, 1]
        '''
        order = [0]*len(sequence)
        mark_ordered = [False]*len(sequence)
        sorted_sequence = sorted(sequence)

        for i in range(len(sequence)):
            for j in range(len(sorted_sequence)):
                if not mark_ordered[j] and sequence[i] == sorted_sequence[j]:
                    order[i] = j + 1
                    mark_ordered[j] = True
                    break
        return order

    @staticmethod
    def percentile(sequence):
        max_sequence = max(sequence)
        return [x*100.0/max_sequence for x in sequence]

    @staticmethod
    def minmax(sequence):
        min_sequence = sequence[0]
        max_sequence = sequence[0]
        for x in sequence[1:]:
            if min_sequence > x:
                min_sequence = x
            elif max_sequence < x:
                max_sequence = x
        return min_sequence, max_sequence

    @staticmethod
    def scale_data(data, data_range=(-12, 15), feature_range=(0, 100)):
        '''
        Scaling a data point to feature_range using data_range
    
        Args:
            data (float): a data point to be scaled
            data_range (tuple): the tuple of (min, max) range represents the data value range
            feature_range (tuple): the tuple of (min, max) range to scale the column to
    
        Returns:
            scaled data
        '''
        if data >= 1.0:
            data = math.log10(data) - data_range[0]
        elif -1 <= data < 1.0:
            data = -data_range[0]
        else:
            data = -math.log10(math.fabs(data)) - data_range[0]
    
        scaled_data = feature_range[0] + data * (feature_range[1] - feature_range[0]) / (data_range[1] - data_range[0])
    
        if scaled_data < feature_range[0]:
            return feature_range[0]
        elif scaled_data > feature_range[1]:
            return feature_range[1]
        else:
            return scaled_data


if __name__ == '__main__':
    import doctest
    doctest.testmod()