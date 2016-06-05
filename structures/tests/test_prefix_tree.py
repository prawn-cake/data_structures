# -*- coding: utf-8 -*-
import unittest
import inspect
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
        self.assertEqual(trie.total_tags(), 15)

        # Test insert same value and check total counters
        trie.insert('amy')
        self.assertEqual(trie.total_words(), 5)
        self.assertEqual(trie.total_tags(), 15)

    def test_lookup(self):
        trie = TrieNode()
        values = ['amy', 'ann', 'emma', 'rob', 'roger']
        for value in values:
            trie.insert(value)

        # True assertions
        for val in values:
            self.assertTrue(trie.lookup(val), 'Not found: {}'.format(val))

        # Test fuzzy
        self.assertEqual(sorted(list(trie.lookup('a'))),
                         sorted(['amy', 'ann']))

        # False assertions with disabled fuzzy option
        for val in ['am', 'an', 'johm', 'max']:
            self.assertFalse(list(trie.lookup(val, fuzzy=False)))

        # Test empty search
        self.assertEqual(list(trie.lookup('non-existed')), [])

    def test_delete(self):
        trie = TrieNode()
        values = ['amy', 'ann', 'anne', 'emma', 'rob', 'roger', 'anna']
        for value in values:
            trie.insert(value)

        total_words = trie.total_words()
        total_tags = trie.total_tags()
        self.assertEqual(total_words, 7)

        # Test delete end value
        self.assertEqual(trie.remove('amy'), 0)
        self.assertEqual(trie.total_words(), 6)
        self.assertEqual(trie.total_tags(), total_tags - 1)

        # Check that nothing to delete
        self.assertEqual(trie.remove('amy'), -1)
        self.assertEqual(trie.total_words(), 6)
        self.assertEqual(trie.total_tags(), total_tags - 1)

        # Test delete the value but keep the node (and number of tags)
        self.assertEqual(trie.remove('ann'), 1)
        self.assertEqual(trie.total_words(), 5)
        self.assertEqual(trie.total_tags(), total_tags - 1)


class PrefixTreeTest(unittest.TestCase):
    def test_lookup(self):
        prefix_tree = PrefixTree()
        values = ['amy', 'ann', 'anne', 'emma', 'rob', 'roger', 'anna']
        for value in values:
            prefix_tree[value] = value

        self.assertIn('amy', prefix_tree)
        result = prefix_tree['ann']
        self.assertTrue(result)
        self.assertTrue(inspect.isgenerator(result))
        # expect 'ann', 'anne' and 'anna'
        self.assertEqual(len(list(result)), 3)