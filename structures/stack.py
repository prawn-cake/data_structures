# -*- coding: utf-8 -*-
import sys


class Stack(object):
    def __init__(self):
        self._stack = []

    def pop(self):
        return self._stack.pop()

    def push(self, item):
        return self._stack.append(item)

    def peek(self):
        if self.is_empty():
            return None
        return self._stack[-1]

    def is_empty(self):
        return len(self._stack) == 0


class MaxStack(Stack):
    """Stack with tracking max value"""

    def __init__(self):
        super().__init__()
        self._track = Stack()  # to track max stack

    def push(self, item):
        if item >= self.max():
            self._track.push(item)
        super(MaxStack, self).push(item)

    def pop(self):
        if self.is_empty():
            return None
        item = super(MaxStack, self).pop()
        if item == self._track.peek():
            self._track.pop()
        return item

    def max(self):
        if self.is_empty():
            return -sys.maxsize - 1
        return self._track.peek()


if __name__ == '__main__':
    s = MaxStack()
    for i in [3, 4, 2, 6]:
        s.push(i)

    assert s.max() == 6

    s.pop()
    assert s.max() == 4

    s.pop()
    assert s.max() == 4

    s.pop()
    assert s.max() == 3

    s.pop()
    assert s.max() == -9223372036854775808
