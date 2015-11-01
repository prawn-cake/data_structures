# -*- coding: utf-8 -*-
"""Prefix tree / Digital tree / Radix tree / Trie implementation
See definition: https://en.wikipedia.org/wiki/Trie
"""


class TrieNode(object):
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
        pass

    def find(self, value):
        if not value:
            if self.is_end:
                return True

            # Probably typo in the word
            return False

        tag = value[0]
        if tag in self.nodes:
            node = self.nodes[tag]
            return node.find(value[1:])

        return False

    def find_similar(self, key, tolerance=1):
        node = self
        for tag in key:
            if tag not in self.nodes:
                return None
            else:
                node = self.nodes[tag]
        return node.tag

    def total_words(self, key=None):
        """Get total words in general and particularly

        :param key: if key is set filter sum by branch
        :return: int
        """
        if key:
            tag = key[0]
            if tag in self.nodes:
                node = self.nodes[tag]
                return self.words + node.words(key=key[1:])
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

    def __contains__(self, item):
        pass

    def __setitem__(self, key, value):
        pass

    def __getitem__(self, item):
        pass

    def __repr__(self):
        return "%s(tag='%s', words=%d)" % (
            self.__class__.__name__, self.tag, self.words)


if __name__ == '__main__':
    pass
