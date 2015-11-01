# -*- coding: utf-8 -*-
import unittest
from structures.prefix_tree import TrieNode


class PrefixTreeTest(unittest.TestCase):
    def setUp(self):
        self.trie = TrieNode()

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

    def test_find_similar(self):
        trie = TrieNode()
        values = ['amy', 'ann', 'anne', 'emma', 'rob', 'roger']
        for value in values:
            trie.insert(value)

        print(trie.find_similar('amy'))

    def test_delete(self):
        pass
