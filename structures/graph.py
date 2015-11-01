# -*- coding: utf-8 -*-
"""Basic graph implementation"""


def find_path(graph, start, end, path=None):
    if path is None:
        path = [start]
    else:
        path.append(start)

    if start == end:
        return path

    if start not in graph:
        return None

    for vertex in graph[start]:
        if vertex not in path:
            return find_path(graph, vertex, end, path)

    return None


class Vertex(object):
    def __init__(self, id, weight=0):
        self.id = id
        self.weight = weight
        self.is_visited = False
        self.vertexes = []

    def mark_as_visited(self):
        self.is_visited = True


class Graph(object):

    """Basic graph implementation"""

    def __init__(self):
        self.vertices = {}

    def add_vertex(self, key):
        vertex = Vertex(id=key)
        self.vertices[vertex.id] = vertex

    @property
    def size(self):
        return len(self.vertices)

    def __contains__(self, item):
        if isinstance(item, Vertex):
            return item.id in self.vertices
        return item in self.vertices

    def __iter__(self):
        return self.vertices.values()


# NOTE: BFS implementation is in the coursera project
