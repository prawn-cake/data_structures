# -*- coding: utf-8 -*-
import unittest
from structures.bk_tree import BKTree, levenshtein_distance


class BKTreeTestCase(unittest.TestCase):

    def test_base(self):
        values = ['hat', 'hate', 'trac', 'roar', 'power', 'row']
        tree = BKTree.create(values)

        # self.assertEqual(tree.count, 6)  # FIXME
        self.assertEqual(tree.search('grow'), [])

        nodes = tree.search('row', distance=1)
        self.assertIsInstance(nodes, list)
        for node in nodes:
            self.assertIsInstance(node, BKTree)
        self.assertEqual(nodes[0].word, 'row')

        result = tree.search('row', distance=2, result_set=[])
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
