__author__ = 'sunary'


class Node(object):

    def __init__(self, char, value=0):
        self.char = char
        self.value = value
        self.child = []

    def get_char(self):
        return self.char

    def add(self, child_node):
        position = len(self.child)
        if position == 0 or self.child[position - 1].get_char() != child_node.get_char():
            self.child.append(child_node)
            position += 1

        return position - 1

    def insert(self, child_node):
        position = len(self.child)
        if position == 0:
            self.child.append(child_node)
            position += 1
        else:
            position = self.find_child_char(child_node.get_char())
            if self.child[position].get_char() != child_node.get_char():
                self.child[position + 1:position + 1] = [child_node]
                position += 1

        return position - 1

    def find_child_char(self, char):
        if not self.child:
            return 0

        left_position = 0
        right_position = len(self.child) - 1

        mid_position = (left_position + right_position)/2
        mid_value = self.child[mid_position].char
        while left_position <= right_position:
            if char < mid_value:
                right_position = mid_position - 1
            else:
                left_position = mid_position + 1

            mid_position = (left_position + right_position)/2
            mid_value = self.child[mid_position].char

        return left_position - 1

    def exist_child_char(self, char):
        return char == self.child[self.find_child_char(char)]

    def get_child(self, char):
        if not self.child:
            return None

        position = self.find_child_char(char)
        if char == self.child[position].get_char:
            return self.child[position]
        return None

    def show_child(self):
        str_child = ''
        for child in self.child:
            str_child += str(child.get_char()) + ', '
        return str_child


class SearchTrie(object):

    def __init__(self):
        self.root_node = Node('root')

    def sort_add_to_trie(self, list_word):
        self.add_to_trie(sorted(list_word))

    def add_to_trie(self, list_word):
        for word in list_word:
            # self.add_to_trie_node(word, 0, self.root_node)
            self.add_to_trie_node2(word)

    def add_to_trie_node(self, word, i, node):
        if i >= len(word):
            return

        child_node = Node(word[i], 1 if i == len(word) - 1 else 0)
        position = node.add(child_node)

        self.add_to_trie_node(word, i + 1, node.child[position])

    def add_to_trie_node2(self, word):
        father_node = self.root_node
        len_word = len(word)
        for i in range(len_word):
            child_node = Node(word[i], 1 if i == len_word - 1 else 0)
            position = father_node.add(child_node)
            father_node = father_node.child[position]

    def find(self, word):
        father_node = self.root_node
        len_word = len(word)
        for i in range(len_word):
            position = father_node.find_child_char(word[i])
            if word[i] == father_node.child[position].char:
                father_node = father_node.child[position]
                if i == len_word - 1:
                    return father_node.value == 1
            else:
                return False

        return False

    def read_file_trie(self, trie_file):
        with open(trie_file, 'r') as fo:
            self.text_trie = fo.read()

        self.text_trie = self.text_trie.split(';')
        self.root_node = Node('root')
        self.read_trie(self.root_node)

    def read_trie(self, child_node):
        text_node = self.text_trie[0].split(',')
        del self.text_trie[0]
        child_node.char = text_node[0]
        child_node.value = int(text_node[1])
        if text_node[2] != '-':
            for i in range(int(text_node[2])):
                child_node.child.append(Node(''))
                self.read_trie(child_node.child[i])

    def write_file_trie(self, trie_file):
        self.text_trie = ''
        self.write_file(self.root_node)

        with open(trie_file, 'w') as fo:
            fo.write(self.text_trie)

    def write_file(self, child_node):
        self.text_trie += child_node.char + ',' + str(child_node.value) + ',' + (str(len(child_node.child)) if child_node.child else '-') + ';'
        if child_node:
            for child in child_node.child:
                self.write_file(child)


if __name__ == '__main__':
    search_trie = SearchTrie()
    search_trie.sort_add_to_trie(['32', '12', '213434', '22', '231', '324', '34', '4', '44', '512', '122'])
    # search_trie.read_file_trie('text_processing/trie.txt')
    print(search_trie.root_node.show_child())
    print(search_trie.find('12'))
    print(search_trie.find('3124'))
    print(search_trie.find('22'))
    print(search_trie.find('232'))
    print(search_trie.find('4'))
    # search_trie.write_file_trie('text_processing/trie.txt')