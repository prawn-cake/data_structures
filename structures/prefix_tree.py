# -*- coding: utf-8 -*-
"""Prefix tree / Digital tree / Radix tree / Trie implementation
See definition: https://en.wikipedia.org/wiki/Trie
"""
import collections


class PrefixTree(collections.MutableMapping):
    """Prefix tree. In fact this is just a trie node holder"""

    def __init__(self):
        self.tree = TrieNode()

    def __contains__(self, value):
        return bool(list(self.tree.lookup(value=value, fuzzy=False)))

    def __setitem__(self, _, value):
        """Set tree value

        :param _:
        :param value:
        """
        self.tree.insert(value=value)

    def __getitem__(self, value):
        return self.tree.lookup(value=value)

    def __delitem__(self, key):
        return self.tree.remove(value=key)

    def __iter__(self):
        return iter(self.tree)

    def __len__(self):
        return self.tree.total_tags()


class TrieNode(collections.Iterable):
    """Main tree node class"""

    def __init__(self, tag='', parent=None):
        self.tag = tag
        self.value = None
        self.words = 0
        self.tags_num = 0
        self.nodes = {}
        self.parent = parent

    def _get_or_create_node(self, value, create=True):
        """Get or create trie node.
        Reusable in the lookup, insert and delete methods

        :param value: str
        :return: TrieNode
        """
        node = self
        idx = 1
        while idx <= len(value):
            tag = value[:idx]
            # Create new node with tag if doesn't exist
            if tag not in node.nodes:
                if create:
                    node.nodes[tag] = TrieNode(tag=tag, parent=node)
                    node.tags_num += 1
                else:
                    # Return None if node is not found
                    return None
            node = node.nodes[tag]

            # Increment index and continue traversing
            idx += 1
        return node

    def insert(self, value):
        """Inserting value to a tree

        :param value: str: value to insert
        """
        if not isinstance(value, str):
            raise ValueError("Wrong value to insert '%r', must be str" % value)

        # Get or create node
        node = self._get_or_create_node(value=value)
        if node.value is None:
            node.value = value
            node.parent.words += 1

    def remove(self, value):
        """Remove value from the tree
        Find the node and remove the value or the node itself if no children

        :param value: str:
        :rtype : int: -1, 0 or 1, where
         -1 - nothing to delete
         0  - whole node has been removed
         1  - only node value has been removed
        """

        node = self._get_or_create_node(value=value, create=False)
        if node is None or node.value is None:
            # Nothing to delete, no such value in the tree
            return -1

        # If there are children, just reset the value
        parent = node.parent
        parent.words -= 1
        if node.nodes:
            node.value = None
            return 1
        else:
            # Remove link from parent and remove the node object itself
            parent.tags_num -= 1
            del parent.nodes[node.tag]
            del node
            return 0

    def lookup(self, value, fuzzy=True):
        """Values lookup method.

        :param fuzzy: bool: continue search and return values from child nodes
        :param value: str: string value
        :return:
        """

        node = self
        idx = 1
        while idx <= len(value):
            tag = value[:idx]
            # Create new node with tag if doesn't exist
            if tag not in node.nodes:
                node.nodes[tag] = TrieNode(tag=tag)
                node.tags_num += 1
            node = node.nodes[tag]

            # Increment index and continue searching
            idx += 1

        # Handle if this is a final value and check if anything further
        if fuzzy:
            for val in node.get_values():
                yield val
        else:
            if node.value:
                yield node.value

    def total_words(self, prefix=None):
        """Get total words in general and particularly

        :param prefix: if prefix is set filter sum by branch
        :return: int
        """

        if prefix:
            node = self._get_or_create_node(create=False, value=prefix)
        else:
            node = self
        cnt = node.words

        # Traverse tree and gather all counters
        for node in self.traverse_tree():
            cnt += node.words

        return cnt

    def total_tags(self, tag=None):
        """Get total tags

        :param tag:
        :return:
        """
        if tag:
            node = self._get_or_create_node(create=False, value=tag)
        else:
            node = self
        cnt = node.words

        # Traverse tree and gather all counters
        for node in self.traverse_tree():
            cnt += node.tags_num

        return cnt

    def traverse_tree(self):
        """Traverse nodes and get end values with depth search
        """
        nodes = [self]
        while nodes:
            node = nodes.pop()
            yield node

            if node.nodes:
                nodes.extend(node.nodes.values())

    def get_values(self):
        """Handy helper around traverse to get tree values
        :rtype : str: node value
        """
        for node in self.traverse_tree():
            if node.value:
                yield node.value

    def __repr__(self):
        return "%s(tag='%s', words=%d, tags_num=%d)" % (
            self.__class__.__name__, self.tag, self.words, self.tags_num)

    def __iter__(self):
        return iter(self.nodes)
