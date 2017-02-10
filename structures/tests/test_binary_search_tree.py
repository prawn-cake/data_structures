# -*- coding: utf-8 -*-
import unittest
from structures.binary_search_tree import Node


class BinarySearchTreeTest(unittest.TestCase):

    def do_basic_checks(self, root):
        self.assertEqual(root.max_val, 7)
        self.assertEqual(root.min_val, 1)
        self.assertEqual(root.count, 7)
        self.assertIsInstance(root.search(5), Node)
        self.assertIsNone(root.search(8))
        # check rank
        self.assertEqual(Node.rank(7, root), 6)  # 6 nodes less than 7
        self.assertEqual(Node.rank(1, root), 0)
        self.assertEqual(Node.level_order_traversal(root),
                         [4, 1, 7, 2, 5, 3, 6])

    def test_tree(self):
        root = Node.insert(None, 4)
        Node.insert(root, 1)
        Node.insert(root, 2)
        Node.insert(root, 7)
        Node.insert(root, 5)
        Node.insert(root, 4)  # already exist
        Node.insert(root, 6)
        Node.insert(root, 3)

        order = Node.in_order_traversal(root)
        self.assertEqual([node.value for node in order], [1, 2, 3, 4, 5, 6, 7])
        self.do_basic_checks(root=root)

        # Build tree from the list
        tree = Node.get_tree(Node.pre_order_traversal(root))
        self.do_basic_checks(root=tree)

    def test_tree_insert_delete(self):
        tree = Node.get_tree([4, 1, 7, 2, 5, 3, 6])
        Node.insert(tree, 8)
        Node.insert(tree, 9)
        Node.delete(7, tree)
        self.assertEqual(Node.level_order_traversal(tree),
                         [4, 1, 8, 2, 5, 9, 3, 6])
        values = [5, 3, 7, 9]
        tree = Node.get_tree(values)
        self.assertEqual(Node.level_order_traversal(tree), [5, 3, 7, 9])
        self.assertEqual(tree.count, 4)
        self.assertEqual(Node.height(tree), 3)
