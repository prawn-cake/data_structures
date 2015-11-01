# -*- coding: utf-8 -*-
import unittest
from structures.binary_heap import MinHeap


class BinaryHeapTestCase(unittest.TestCase):
    def test_swap(self):
        heap = MinHeap([1, 2, 3, 4])
        heap.swap(0, 1)
        self.assertEqual(heap.storage, [2, 1, 3, 4])

    def test_get_parent(self):
        heap = MinHeap([1, 2, 3, 4, 5, 6, 7, 8, 9])

        parent_id, value = heap.get_parent(0)
        self.assertEqual(parent_id, 0)
        self.assertEqual(value, 1)

        parent_id, value = heap.get_parent(9)
        self.assertEqual(parent_id, 4)
        self.assertEqual(value, 5)

        parent_id, value = heap.get_parent(6)
        self.assertEqual(parent_id, 2)
        self.assertEqual(value, 3)

    def test_insert(self):
        heap = MinHeap.heapify([6, 1, 5, 4, 3, 2, 7])
        # print(heap)

        # 1st check: auto
        self.assertTrue(heap.validate())

        # 2nd check: manual
        for i in range(heap.size):
            parent_id, parent_val = heap.get_parent(i)
            # print('id: {} <= {}; val: {} <= {}'.format(
            #     i, parent_id, heap.storage[i], parent_val))
            self.assertLessEqual(parent_val, heap.storage[i])

    def test_height_of(self):
        heap = MinHeap.heapify([6, 1, 5, 4, 3, 2, 7, 8, 9, 0])
        self.assertEqual(heap.height_of(9), 3)
        self.assertEqual(heap.height_of(0), 0)
        self.assertEqual(heap.height_of(6), 2)
        self.assertEqual(heap.height_of(1), 1)
        self.assertEqual(heap.height_of(2), 1)

    def test_extract_min(self):
        heap = MinHeap.heapify([6, 1, 5, 4, 3, 2, 7])
        self.assertTrue(heap.validate())
        size = heap.size
        # print(heap)
        self.assertEqual(heap.extract_min(), 1)
        self.assertEqual(heap.size, size - 1)
        # print(heap)
        self.assertTrue(heap.validate())
        self.assertEqual(heap.extract_all(), [2, 3, 4, 5, 6, 7])
        self.assertEqual(heap.size, 0)