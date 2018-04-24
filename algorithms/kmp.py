__author__ = 'sunary'


class KMPAlgorithm(object):

    def __init__(self):
        pass

    def search(self, word_sought=None, searched=None, table=None):
        table = table or self.create_table(word_sought)

        m = 0
        l = len(word_sought)
        while m + l < len(searched):
            for i in range(l):
                if word_sought[i] != searched[m + i]:
                    m += (i - table[i])
                    break
                elif i == l - 1:
                    return True

        return False

    def create_table(self, text):
        table = [-1, 0] + [0] * len(text[:-2])
        pos = 2
        cnd = 0
        while pos < len(text):
            if text[pos - 1] == text[cnd]:
                table[pos] = cnd + 1
                cnd += 1
                pos += 1
            elif cnd > 0:
                cnd = table[cnd]
            else:
                table[pos] = 0
                pos += 1

        return table


if __name__ == '__main__':
    import datetime

    kmp = KMPAlgorithm()
    word_sought = 'abcdabc'
    s1 = 'abcdabdccacbdaadabcdadc464564dfhfh34534dfgd34534dfdfg4534dhdh45435rhth4634hg34534hgh34345dghfgh345345dhdg34534534545345'
    s2 = '34rete3453hdfgh34534dhdfh4534hfgh345abcdabdccacbdaadabcdabcabdadacbac34t34dfhdf456345fhfgh46345hdfghf4356345fhfgh3463dd'
    s3 = 'abcdabdccacbdaadabcdadc' * 200

    start = datetime.datetime.now()
    for i in xrange(10000):
        kmp.search(word_sought, s1)
        kmp.search(word_sought, s2)
        kmp.search(word_sought, s3)

    print (datetime.datetime.now() - start)

    table = kmp.create_table(word_sought)
    start = datetime.datetime.now()
    for i in xrange(10000):
        kmp.search(word_sought, s1, table)
        kmp.search(word_sought, s2, table)
        kmp.search(word_sought, s3, table)

    print (datetime.datetime.now() - start)

    start = datetime.datetime.now()
    for i in xrange(10000):
        word_sought in s1
        word_sought in s2
        word_sought in s3

    print(datetime.datetime.now() - start)