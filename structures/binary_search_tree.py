# -*- coding: utf-8 -*-
"""Binary search tree implementation"""

from collections import deque


class Node(object):

    """Implementation of binary search tree """

    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value
        self.count = 1

    @classmethod
    def insert(cls, node, value):
        if node is None:
            return Node(value)
        if value == node.value:
            node.value = value
            print('Value `{}` is contained in the tree'.format(value))
        elif value > node.value:
            node.right = Node.insert(node.right, value)
        elif value < node.value:
            node.left = Node.insert(node.left, value)

        node.count = 1 + cls.size_of(node.left) + \
            cls.size_of(node.right)
        return node

    def search(self, value):
        if value == self.value:
            return self
        elif value < self.value:
            if self.left:
                return self.left.search(value)
            else:
                return None
        else:
            if self.right:
                return self.right.search(value)
            else:
                return None

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
            Node.in_order_traversal(node.left, order)
        order.append(node.value)
        if node.right:
            Node.in_order_traversal(node.right, order)
        return order

    @classmethod
    def pre_order_traversal(cls, node, order=None):
        if order is None:
            order = []

        order.append(node.value)
        if node.left:
            Node.pre_order_traversal(node.left, order)
        if node.right:
            Node.pre_order_traversal(node.right, order)

        return order

    @classmethod
    def level_order_traversal(cls, node, queue=None, order=None):
        """Level order traversal is implemented with queue
        Steps:
            1. Add node value to order list and go ahead
            2. Put next node to the queue (left AND/OR right if exists)
            3. Declare while loop and repeat first two steps until queue length
            will be equal 0

        """
        if order is None:
            order = []
        if queue is None:
            queue = deque()

        order.append(node.value)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

        while len(queue) != 0:
            Node.level_order_traversal(
                queue.popleft(), queue=queue, order=order)

        return order

    @classmethod
    def get_tree(cls, values):
        """Build tree from list of values

        :param values: list
        :return: Node: tree
        """
        root = Node.insert(None, values[0])
        for value in values[1:]:
            Node.insert(root, value)
        return root

    @classmethod
    def size_of(cls, node):
        if node is None:
            return 0
        return node.count

    @classmethod
    def height(cls, node):
        if node is None:
            return 0
        return 1 + max(cls.height(node.left), cls.height(node.right))

    @classmethod
    def rank(cls, value, node):
        """How many values less than value

        :param value:
        :param node:
        """
        if node is None:
            return 0

        if node.value > value:
            return Node.rank(value, node.left)
        elif node.value < value:
            return 1 + cls.size_of(node.left) +\
                Node.rank(value, node.right)
        elif node.value == value:
            return cls.size_of(node.left)

    @classmethod
    def delete(cls, value, node):
        if node is None:
            return None
        # find the node
        if value > node.value:
            node.right = cls.delete(value, node.right)
        elif value < node.value:
            node.left = cls.delete(value, node.left)
        else:
            # node is found
            if node.right is None:  # no right child
                return node.left
            if node.left is None:   # no left child
                return node.right

            tmp = node
            node = cls.get_min(tmp.right)
            node.right = cls.delete_min(tmp.right)
            node.left = tmp.left
        node.count = 1 + cls.size_of(node.left) + cls.size_of(node.right)
        return node

    @classmethod
    def delete_min(cls, node):
        if node.left is None:
            return node.right
        node.left = Node.delete_min(node.left)
        node.count = 1 + cls.size_of(node.left) + cls.size_of(node.right)
        return node

    def __unicode__(self):
        return "{}(value={}; nodes={})".format(
            self.__class__.__name__,
            self.value,
            self.count)

    def __repr__(self):
        return "{}(value={}; nodes={})".format(
            self.__class__.__name__,
            self.value,
            self.count)
