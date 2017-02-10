# -*- coding: utf-8 -*-


class BinaryHeap(object):

    def __init__(self, values=None):
        self._storage = values or []

    @property
    def storage(self):
        return self._storage

    def insert(self, k):
        raise NotImplementedError()

    @classmethod
    def heapify(cls, values):
        heap = cls()
        for k in values:
            heap.insert(k)
        return heap

    def remove(self, k):
        raise NotImplementedError()

    def extract_min(self):
        raise NotImplementedError()

    def swap(self, i, j):
        swap = self.storage[i]
        self.storage[i] = self.storage[j]
        self.storage[j] = swap
        return self.storage[i], self.storage[j]

    def get_parent(self, i):
        """Formula: parent_id = (i - 1) / 2 and rounded to lower bound

        :param i:
        :return:
        """
        if i == 0:
            return 0, self.storage[0]
        parent_id = int(round((i - 1) / 2))
        return parent_id, self.storage[parent_id]

    @property
    def size(self):
        return len(self.storage)

    def height_of(self, i):
        """Get height of node i. It equals count of hops from i to root

        :param i:
        """
        height = 0
        while i != 0:
            i = self.get_parent(i)[0]
            height += 1
        return height


class MinHeap(BinaryHeap):

    def insert(self, k):
        """Insert new element into the heap

        :param k: element

        Find empty element
        """
        idx = self.size
        self.storage.append(k)
        self._sift_up(idx)

    def _sift_up(self, i):
        if i == 0:
            return None
        value = self.storage[i]
        parent_id, parent_val = self.get_parent(i)

        if parent_val > value:
            self.swap(parent_id, i)
            self._sift_up(parent_id)

    def _sift_down(self, i):
        val = self.storage[i]
        left_id, left_value = self.left_child(i)
        right_id, right_value = self.right_child(i)

        if left_value is None and right_value is None:
            return None

        if val > min(filter(None, [left_value, right_value])):
            if left_value and right_value:
                if left_value < right_value:
                    self.swap(i, left_id)
                    self._sift_down(left_id)
                else:
                    self.swap(i, right_id)
                    self._sift_down(right_id)
            elif left_value and right_value is None:
                self.swap(i, left_id)
                self._sift_down(left_id)
            elif right_value and left_value is None:
                self.swap(i, right_id)
                self._sift_down(right_id)

    def remove(self, k):
        pass

    def extract_min(self):
        if self.size == 0:
            return None
        elif self.size == 1:
            return self.storage.pop()
        _min = self.storage[0]
        self.storage[0] = self.storage.pop()
        self._sift_down(0)
        return _min

    def extract_all(self):
        return [self.extract_min() for _ in range(self.size)]

    def left_child(self, i):
        left_idx = 2 * i + 1
        if left_idx < self.size:
            return left_idx, self.storage[left_idx]
        return left_idx, None

    def right_child(self, i):
        right_idx = 2 * i + 2
        if right_idx < self.size:
            return right_idx, self.storage[right_idx]
        return right_idx, None

    def validate(self):
        """Helper method to validate correctness of heap structure

        :return: bool
        """
        for i in range(self.size):
            parent_id, parent_val = self.get_parent(i)
            if parent_val > self.storage[i]:
                return False
        return True

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.storage)
