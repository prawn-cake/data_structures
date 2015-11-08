# -*- coding: utf-8 -*-
import unittest
from structures.prefix_tree import TrieNode, PrefixTree


class TrieNodeTest(unittest.TestCase):
    def test_insert(self):
        trie = TrieNode()
        values = ['amy', 'ann', 'emma', 'rob', 'roger']
        for value in values:
            trie.insert(value)
        print(trie)
        print(trie.nodes)
        self.assertEqual(trie.total_words(), 5)
        self.assertEqual(trie.total_prefixes(), 15)

    def test_find(self):
        trie = TrieNode()
        values = ['amy', 'ann', 'emma', 'rob', 'roger']
        for value in values:
            trie.insert(value)

        # True assertions
        for val in values:
            self.assertTrue(trie.find(val), 'Not found: {}'.format(val))

        # False assertions
        for val in ['am', 'an', 'johm', 'max']:
            self.assertFalse(trie.find(val))

    def test_find_with_tolerance(self):
        trie = TrieNode()
        values = ['amy', 'ann', 'anne', 'emma', 'rob', 'roger', 'anna']
        for value in values:
            trie.insert(value)

        # Find non-exact words
        self.assertFalse(trie.find('ani', tolerance=0))
        self.assertTrue(trie.find('ani', tolerance=1))

        # Check dict interface
        self.assertFalse('ani' in trie)
        print(trie.find('ani', tolerance=1))

    def test_delete(self):
        trie = TrieNode()
        values = ['amy', 'ann', 'anne', 'emma', 'rob', 'roger', 'anna']
        for value in values:
            trie.insert(value)

        self.assertTrue(trie.find('ann'))
        self.assertEqual(trie.total_words(), 7)
        trie.delete('ann')
        self.assertFalse(trie.find('ann'))
        self.assertEqual(trie.total_words(), 6)


class PrefixTreeTest(unittest.TestCase):
    def test_lookup(self):
        prefix_tree = PrefixTree()
        values = ['amy', 'ann', 'anne', 'emma', 'rob', 'roger', 'anna']
        for value in values:
            prefix_tree[value] = value

        self.assertIn('amy', prefix_tree)
        result = prefix_tree['ann']
        self.assertTrue(result)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)