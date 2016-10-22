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

    def __init__(self, value, distance=0, key_function=None):
        self.nodes = {}

        if key_function is None:
            key_function = lambda val: val

        self.key = key_function(value)
        self.value = value

        self.distance = distance  # levenshtein distance
        self.count = 1
        self.key_function = key_function

    def insert(self, value):
        # calculate new distance for every child node

        insert_key = self.key_function(value)

        distance = levenshtein_distance(self.key, insert_key)
        if distance in self.nodes:
            self.nodes[distance].insert(value)
        else:
            self.nodes[distance] = BKTree(value,
                                          distance=distance,
                                          key_function=self.key_function)
        # FIXME
        self.count = 1 + self.size_of(self) \
            + sum([self.size_of(n) for n in self.nodes.values()])

    def search(self, key, distance=0, result_set=None):
        if result_set is None:
            result_set = []

        cur_distance = levenshtein_distance(key, self.key)

        if cur_distance <= distance:
            result_set.append(self)

        for d, node in self.nodes.items():
            if cur_distance - distance <= d <= cur_distance + distance:
                node.search(key, distance, result_set)

        return [node.value for node in result_set]

    @property
    def max_val(self):
        last_node = self
        while last_node.right:
            last_node = last_node.right
        return last_node.value

    @property
    def min_val(self):
        last_node = self
        while last_node.left:
            last_node = last_node.left
        return last_node.value

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
        order.append(node.value)
        if node.right:
            BKTree.in_order_traversal(node.right, order)
        return order

    @classmethod
    def size_of(cls, node):
        return len(node.nodes)

    @classmethod
    def height(cls, node):
        if node is None:
            return 0
        return 1 + max(cls.height(node.left), cls.height(node.right))

    @staticmethod
    def create(values, key_function=None):
        """Factory method to create a tree

        :param values: list of values
        :return: BKTree instance
        """
        root = BKTree(value=values.pop(), key_function=key_function)
        for val in values:
            root.insert(val)
        return root
