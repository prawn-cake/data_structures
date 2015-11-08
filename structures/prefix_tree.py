# -*- coding: utf-8 -*-
"""Prefix tree / Digital tree / Radix tree / Trie implementation
See definition: https://en.wikipedia.org/wiki/Trie
"""
import random
import collections

SEPARATOR = '\n'


class PrefixTree(collections.MutableMapping):
    """Prefix tree. In fact this is just a trie node holder"""

    def __init__(self, tolerance=0):
        self.tree = TrieNode()
        self.tolerance = tolerance

    def __contains__(self, item):
        return self.tree.find(value=item, tolerance=self.tolerance)

    def __setitem__(self, _, value):
        """Set tree value

        :param _:
        :param value:
        """
        self.tree.insert(value=value)

    def __getitem__(self, item):
        nodes = self.tree.find(
            value=item, tolerance=self.tolerance, lookup_list=[])
        result_list = []

        if len(nodes):
            word = None
            stack = []
            for node in nodes:
                char = node.tag
                if char != SEPARATOR:
                    stack.append(char)
                else:
                    if word is None:
                        word = ''.join(stack)
                        result_list.append(word)
                        stack = []
                    else:
                        result_list.append(''.join([word, ''.join(stack)]))

        return result_list

    def __delitem__(self, key):
        return self.tree.delete(key)

    def __iter__(self):
        return iter(self.tree)

    def __len__(self):
        pass


class TrieNode(collections.Iterable):
    """Main tree node class"""

    def __init__(self, tag=''):
        self.tag = tag
        self.words = 0
        self.prefixes = 0
        self.nodes = {}

    def insert(self, value):
        if not value:
            # end of insert, last character of word
            self.words += 1
        else:
            tag = value[0]
            if tag not in self.nodes:
                self.nodes[tag] = TrieNode(tag=tag)
                self.prefixes += 1
            node = self.nodes[tag]
            node.insert(value[1:])

    def delete(self, value):
        """Delete operation

        :rtype : object
        """
        if not value:
            if self.is_end and not self.words:
                return True
            else:
                self.words -= 1
                return False

        tag = value[0]
        if tag in self.nodes:
            node = self.nodes[tag]
            can_delete = node.delete(value=value[1:])
            if can_delete:
                del self.nodes[tag]
                self.prefixes -= 1

    def get_random_node(self):
        random_key = random.choice(list(self.nodes.keys()))
        return self.nodes[random_key]

    def find(self, value, tolerance=0, lookup_list=None):
        """Find method.
        Some tricks are here:
          - basic search just return true or false
          - 'tolerant' search enable to do non-exact search

        :param value: str: string value
        :param tolerance: int: degree of tolerance
        :param lookup_list: list: enable to do words lookup
        :return:
        """
        # FIXME: perhaps tolerance is wrong feature for this data structure
        if not value:
            if self.is_end:
                # Separate words with line-break
                if lookup_list:
                    lookup_list.append(TrieNode(tag=SEPARATOR))

                # if it's the end of word but tolerance > 0, continue search
                if tolerance > 0 and self.nodes:
                    tolerance -= 1
                    node = self.get_random_node()
                    if lookup_list:
                        lookup_list.append(node)
                    node.find(value='',
                              tolerance=tolerance,
                              lookup_list=lookup_list)
                return lookup_list or True

            # Probably typo in the word
            return False

        tag = value[0]
        if tag in self.nodes:
            node = self.nodes[tag]

            if lookup_list is not None:
                lookup_list.append(node)

            return node.find(value=value[1:],
                             tolerance=tolerance,
                             lookup_list=lookup_list)
        else:
            if tolerance > 0:
                tolerance -= 1

                # We are tolerant and do continue searching in some random node
                node = self.get_random_node()

                if lookup_list is not None:
                    lookup_list.append(node)
                return node.find(value=value[1:],
                                 tolerance=tolerance,
                                 lookup_list=lookup_list)
        return False

    def total_words(self, prefix=None):
        """Get total words in general and particularly

        :param prefix: if prefix is set filter sum by branch
        :return: int
        """
        if prefix:
            tag = prefix[0]
            if tag in self.nodes:
                node = self.nodes[tag]
                return self.words + node.words(key=prefix[1:])
            else:
                return 0
        else:
            return self.words + sum([
                node.total_words() for node in self.nodes.values()])

    def total_prefixes(self, key=None):
        if key:
            tag = key[0]
            if tag in self.nodes:
                node = self.nodes[tag]
                return self.prefixes + node.total_prefixes(key=key[1:])
            else:
                return 0
        else:
            return self.prefixes + sum([
                node.total_prefixes() for node in self.nodes.values()])

    @property
    def is_end(self):
        """Indicate that current node is the end of the word

        :rtype : bool
        """
        return bool(self.words)

    def __repr__(self):
        return "%s(tag='%s', words=%d, prefixes=%d)" % (
            self.__class__.__name__, self.tag, self.words, self.prefixes)

    def __iter__(self):
        return iter(self.nodes)
