# -*- coding: utf-8 -*-
import unittest
from structures.bk_tree import BKNode, levenshtein_distance


class BKNodeTestCase(unittest.TestCase):
    def test_base(self):
        root = BKNode('hat')
        BKNode.insert(root, 'hate')
        BKNode.insert(root, 'trac')
        BKNode.insert(root, 'roar')
        BKNode.insert(root, 'power')
        BKNode.insert(root, 'row')

        # print(root.in_order_traversal(root))

        # self.assertEqual(root.count, 6)  # FIXME
        self.assertEqual(root.search('grow'), [])

        nodes = root.search('row', tolerance=1)
        self.assertIsInstance(nodes, list)
        for node in nodes:
            self.assertIsInstance(node, BKNode)
        self.assertEqual(nodes[0].word, 'row')

        result = root.search('row', tolerance=2, result_set=[])
        self.assertEqual(len(result), 2)  # roar and row


class LevenshteinDistanceTestCase(unittest.TestCase):
    def test_on_empty_strings(self):
        self.assertEqual(levenshtein_distance('', ''), 0)
        self.assertEqual(levenshtein_distance('a', ''), 1)
        self.assertEqual(levenshtein_distance('', 'a'), 1)
        self.assertEqual(levenshtein_distance('abc', ''), 3)

    def test_on_equal_strings(self):
        self.assertEqual(levenshtein_distance('abc', 'abc'), 0)

    def test_on_inserts(self):
        self.assertEqual(levenshtein_distance('abc', 'ac'), 1)
        self.assertEqual(levenshtein_distance('xabxcdxxefxgx', 'abcdefg'), 6)

    def test_on_many_operations(self):
        self.assertEqual(
            levenshtein_distance('java was neat', 'scala is great'), 7)
        self.assertEqual(levenshtein_distance('tape', 'hat'), 3)
