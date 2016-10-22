# -*- coding: utf-8 -*-
"""BK-Tree is a data structure used for spell checking based on the
Levenshtein Distance between two words"""


def levenshtein_distance(s, t):
    """Levenshtein distance is a string metric for measuring the difference
    between two sequences

    :param s: string
    :param t: string
    :return: int: distance between two strings
    """
    if s == t:
        return 0
    elif len(s) == 0:
        return len(t)
    elif len(t) == 0:
        return len(s)

    n, m = len(s), len(t)
    if n < m:
        return levenshtein_distance(t, s)

    current_row = range(n + 1)

    for i in range(1, m + 1):  # row iterator
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):  # column iterator
            add, delete = previous_row[j] + 1, current_row[j - 1] + 1
            subst_cost = (s[j - 1] != t[i - 1])
            change = previous_row[j - 1] + subst_cost
            current_row[j] = min(add, delete, change)

    return current_row[n]


class BKTree(object):
    """
    BK-tree implementation.
    A metric tree suggested by Walter Austin Burkhard and Robert M. Keller
    """

    def __init__(self, word, distance=0):
        self.nodes = {}
        self.word = str(word)
        self.distance = distance  # levenshtein distance
        self.count = 1

    @classmethod
    def insert(cls, node, word):
        # calculate new distance for every child node

        if node is None:
            return BKTree(word)

        distance = levenshtein_distance(node.word, word)
        if distance in node.nodes:
            BKTree.insert(node.nodes[distance], word)
        else:
            node.nodes[distance] = BKTree(word, distance=distance)

        # FIXME
        node.count = 1 + cls.size_of(node) \
            + sum([cls.size_of(n) for n in node.nodes.values()])
        return node

    def search(self, word, distance=0, result_set=None):
        if result_set is None:
            result_set = []

        cur_distance = levenshtein_distance(word, self.word)

        if cur_distance <= distance:
            result_set.append(self)

        for d, node in self.nodes.items():
            if cur_distance - distance <= d <= cur_distance + distance:
                node.search(word, distance, result_set)

        return result_set

    @property
    def max_val(self):
        last_node = self
        while last_node.right:
            last_node = last_node.right
        return last_node.word

    @property
    def min_val(self):
        last_node = self
        while last_node.left:
            last_node = last_node.left
        return last_node.word

    @classmethod
    def get_min(cls, node):
        while node.left:
            node = node.left
        return node

    @classmethod
    def in_order_traversal(cls, node, order=None):
        if order is None:
            order = []

        if node.left:
            BKTree.in_order_traversal(node.left, order)
        order.append(node.word)
        if node.right:
            BKTree.in_order_traversal(node.right, order)
        return order

    @classmethod
    def get_tree(cls, values):
        """Build tree from list of values

        :param values:
        :return:
        """
        root = BKTree.insert(None, values[0])
        for value in values[1:]:
            BKTree.insert(root, value)
        return root

    @classmethod
    def size_of(cls, node):
        return len(node.nodes)

    @classmethod
    def height(cls, node):
        if node is None:
            return 0
        return 1 + max(cls.height(node.left), cls.height(node.right))

    def __unicode__(self):
        return self.__repr__()

    def __repr__(self):
        return "{}(word={}; distance:{}; nodes={})".format(
            self.__class__.__name__,
            self.word,
            self.distance,
            self.count)

    @staticmethod
    def create(values):
        """Factory method to create a tree

        :param values: list of values
        :return: BKTree instance
        """
        root = BKTree(values.pop())
        for val in values:
            BKTree.insert(root, val)
        return root
