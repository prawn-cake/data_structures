# -*- coding: utf-8 -*-
"""
https://en.wikipedia.org/wiki/Red%E2%80%93black_tree
"""


class Color(object):
    RED = 0
    BLACK = 1


class RBNode(object):
    """Red-black tree node
    
    Tree properties:
      * If a node is red, then both its children are black
      
    """
    def __init__(self, value, color=Color.BLACK):
        self._value = value
        self._color = color
        self._left = None
        self._right = None

    def is_nil(self):
        return self._left is None and self._right is None

    def populate(self):
        self._left = RBNode(None, color=Color.BLACK)
        self._right = RBNode(None, color=Color.BLACK)

    def insert(self, value):
        node = RBNode(value, color=Color.RED)
        node.populate()

        if value > self._value:
            self._right = node
        elif value < self._value:
            self._left = node
        else:
            # if value is the same it's the same node
            pass


if __name__ == '__main__':
    pass
