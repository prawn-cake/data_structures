# -*- coding: utf-8 -*-
import unittest
from structures.graph import find_path


class GraphTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_find_path(self):
        graph = {'A': ['B', 'C'],
                 'B': ['C', 'D'],
                 'C': ['D'],
                 'D': ['C'],
                 'E': ['F'],
                 'F': ['C']}

        self.assertEqual(find_path(graph, 'A', 'D'), ['A', 'B', 'C', 'D'])
