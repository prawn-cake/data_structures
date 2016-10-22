# -*- coding: utf-8 -*-
import unittest
from structures.graph import Graph, dijkstra_search


class BasicGraphTest(unittest.TestCase):

    def test_create_directed_graph(self):
        # NOTE: graph is directed by default
        g = Graph()
        a_vertex = g.add_vertex('A')
        b_vertex = g.add_vertex('B')
        c_vertex = g.add_vertex('C')
        g.add_edge(a_vertex, b_vertex)
        g.add_edge(b_vertex, c_vertex, distance=2)

        # Convert to dict
        dict_struct = g.as_dict()
        self.assertIsInstance(dict_struct, dict)

        expected = {'A': [('B', 1)], 'C': [], 'B': [('C', 2)]}
        self.assertEqual(dict_struct, expected)

    def test_create_not_directed_graph(self):
        g = Graph(directed=False)
        a_vertex = g.add_vertex('A')
        b_vertex = g.add_vertex('B')
        c_vertex = g.add_vertex('C')

        # Directed graph adds edges for both directions: a <--> b, b <--> c
        g.add_edge(a_vertex, b_vertex)
        g.add_edge(b_vertex, c_vertex, distance=2)

        dict_struct = g.as_dict()
        expected = {'A': [('B', 1)],
                    'C': [('B', 2)],
                    'B': [('A', 1), ('C', 2)]}
        self.assertEqual(dict_struct, expected)

    def test_build_graph_from_dict(self):
        struct = {'A': [('B', 1)], 'C': [], 'B': [('C', 2)]}
        g = Graph.build_graph(struct)
        self.assertIsInstance(g, Graph)
        self.assertEqual(len(g.vertices), 3)
        self.assertEqual(g.as_dict(), struct)

        # Convert graph multiple times, check robustness
        self.assertEqual(Graph.build_graph(g.as_dict()).as_dict(), struct)


class DijkstraSearchTest(unittest.TestCase):

    def test_search(self):
        struct = {'S': [('A', 7), ('B', 3)],
                  'A': [('B', 2), ('C', 2)],
                  'B': [('C', 1)],
                  'D': [('C', 2), ('A', 3)]}
        g = Graph.build_graph(struct, directed=False)
        distances, path = dijkstra_search(g.vertices['S'])

        self.assertEqual(distances['A'], 5)  # S -> B -> A
        self.assertEqual(distances['B'], 3)  # S -> B
        self.assertEqual(distances['C'], 4)  # S -> B -> C
        self.assertEqual(distances['D'], 6)  # S -> B -> C -> D

        p = path.get_path('S', 'D')
        self.assertEqual([v.value for v in p], ['S', 'B', 'C', 'D'])
