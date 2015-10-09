__author__ = 'sunary'


class MinhashSignatures():

    def __init__(self, input_dim, hfunc_para):
        self.input_dim = input_dim
        self.hfunc_para = hfunc_para

    def _hash_function(self, para1, para2, x):
        return (para1*x + para2) % self.input_dim

    def hash(self, input_point):
        hashed = [self.input_dim] * len(self.hfunc_para)
        for i in range(len(self.hfunc_para)):
            for j, point in enumerate(input_point):
                if point:
                    hashed[i] = min (hashed[i], self._hash_function(self.hfunc_para[i][0], self.hfunc_para[i][1], j))

        return hashed


if __name__ == '__main__':
    minhash_signatures = MinhashSignatures(5, [(1, 1), (3, 1)])
    print minhash_signatures.hash([1, 0, 0, 1, 0])
    print minhash_signatures.hash([0, 0, 1, 0, 0])
    print minhash_signatures.hash([0, 1, 0, 1, 1])
    print minhash_signatures.hash([1, 0, 1, 1, 0])