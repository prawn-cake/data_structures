# -*- coding: utf-8 -*-
"""
Elementary implementation

Implementation 1.
* Keep keys in an ordered list as
    keys = [key1, key2, ..., keyN]
    values = [val1, val2, ..., valN]

Where value = values[keys.index(keyN)]
* Search keys with binary search, insert values with rank(k), may take O(N / 2)

Problem: After inserting a new key all the greater keys and values should be
moved to the right


Implementation 2

Binary Search Tree implementation
Problem: dis-balance


Implementation 3
Balanced tree, for example red-black tree


Notes:

- hashCode implementation
  * 31x + y rule


Dynamic resizing:

  - by copying all entries - allocate a new table and copy all values from the
  old one

  - incremental resizing
    * allocate new table, keep old one unchanged
    * check both tables for each lookup
    * insert values only to the new table
    * at each insertion move N values from the old to the new table
    * remove / deallocate old table once migration is completed

  - consistent hashing approach
    * requires monotonic keys

"""


NULL = object()


class AssociativeArray(object):
    def __init__(self):
        self._size = 0

    def put(self, key, value):
        raise NotImplementedError()

    def get(self, key):
        raise NotImplementedError()

    def delete(self, key):
        # Lazy deletion
        deleted = self.put(key, NULL)
        if deleted:
            self._size -= 1

    def contains(self, key):
        return self.get(key) is not None

    def is_empty(self):
        return self.size == 0

    @property
    def size(self):
        return self._size

    def keys(self):
        raise NotImplementedError()


class Node(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value


class SeparateChainHashTable(AssociativeArray):
    """Main idea of a separate-chaining hash table is the following:

    - Hash: map a key to integer between 0 and M - 1
    - Insert: put at front of i-th chain (if not already there)
    - Search: need to search only i-th chain

    Typical choice of M ~ N / 5, where N is a number of keys

    Warnings:
      * M is too small -> long chains
      * M is too large -> too many empty chains

    Hashing chaining is a one of collisions resolution methods
    """

    def __init__(self):
        super().__init__()
        self.m = 97  # number of chains
        self.chains = [[] for _ in range(self.m)]  # array of chains

    def hash(self, key):
        return (hash(key) & 0x7fffffff) % self.m

    def get(self, key):
        i = self.hash(key)
        for node in self.chains[i]:
            if node.key == key:
                return node.value
        return None

    def put(self, key, value):
        i = self.hash(key)

        for node in self.chains[i]:
            if node.key == key:
                node.value = value
                return True  # True indicates that the key was found

        # Put a new node in the beginning of the chain (linked-list)
        self.chains[i].insert(0, Node(key, value))
        if value is not NULL:
            self._size += 1

        # explicitly return None to indicate that the key wasn't found
        return None


class LinearProbingHashTable(AssociativeArray):
    """Linear probing is an another technique to tackle key collisions

    Features:
      - Hash: Map key to integer i between 0 and M - 1
      - Insert: Put a table index i if free; if not try i + 1, i + 2, etc
      - Search: Search table index i; if occupied but not match , try i + 1, ..

    NOTE: Array size M must be greater than number of key-value pairs N
    --> resize an array if it becomes at least a half full

    Warnings:
      * M is too large --> too many empty array entities
      * M is too small --> search time blows up
      * Keep the array half-empty, resize if it's reaches that size

    Optimizations:
      - using another hash function to define the next position may help to
      optimize finding a free slot

    """

    def __init__(self):
        super().__init__()
        self.m = 97
        self._keys = []
        self._values = []

    def delete(self, key):
        """Find and remove key-value pair and then reinsert all of the
        key-value pairs in the same cluster that appear after the deleted pair.

        Alternatively flag the deleted entry so that it is skipped over during
        the search but available for insert (default behavior in python)
        If there are too many flagged entries, create a new hash table and
        rehash all kv pairs

        :param key:
        """
        pass
