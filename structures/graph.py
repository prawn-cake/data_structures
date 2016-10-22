# -*- coding: utf-8 -*-
import collections
import heapq


def find_path(graph, start, end, path=None):
    """

    :param graph: dict
    :param start: str: key
    :param end:   str: key
    :param path:  list
    :return:
    """
    if path is None:
        path = [start]
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

    def __init__(self, value, weight=None):
        self.value = value
        self.weight = weight
        self.is_visited = False
        self._neighbors = []

    def mark_as_visited(self):
        self.is_visited = True

    def link(self, vertex, distance=1):
        self._neighbors.append((vertex, distance))

    def get_neighbors(self, values_list=False):
        if values_list:
            return [(v.value, distance) for v, distance in self._neighbors]
        return self._neighbors

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Use vertex as a context manager, mark it as visited after all

        """
        self.mark_as_visited()

    def __repr__(self):
        return "%s('%s', neighbors=%d)" % (
            self.__class__.__name__, self.value, len(self._neighbors))


def bfs(start_vertex):
    """Breadth-first search implementation"""

    queue = collections.deque()
    start_vertex.mark_as_visited()
    queue.appendleft(start_vertex)

    while len(queue):
        vertex = queue.pop()
        for v in vertex.get_neighbors():
            if not v.is_visited:
                # TODO: calculate distance
                v.mark_as_visited()
                queue.appendleft(v)


class Graph(object):

    """Basic graph implementation"""

    def __init__(self, directed=True):
        self.vertices = {}
        self._directed = directed

    @property
    def is_directed(self):
        return self._directed

    def add_vertex(self, value):
        """Add vertex by value or return already existent

        :param value: any hashable value
        """
        if value in self.vertices:
            return self.vertices[value]

        vertex = Vertex(value=value)
        self.vertices[vertex.value] = vertex
        return vertex

    def add_edge(self, v1, v2, distance=1):
        """Add edge between two vertices with some distance

        :param v1: vertex 1
        :param v2: vertex 2
        :param distance: int: 1 by default
        """
        if distance < 0:
            raise ValueError(
                'Wrong distance value: {}. Must be >= 0'.format(distance))

        v1.link(v2, distance=distance)
        if not self.is_directed:
            v2.link(v1, distance=distance)

    @property
    def size(self):
        return len(self.vertices)

    @staticmethod
    def build_graph(dict_struct, directed=True):
        """Build graph from dictionary

        :param directed: bool: parameter defines is graph directed
        :param dict_struct: dict
        Example:
            graph = {'A': [('B', 1), ('C', 2)],
                     'B': [('C', 3), ('D', 2)],
                     'C': [('D', 1)]}
        Where keys are vertices and values are edges between.
        Each edge can be represented:
            - as tuple - ('value', distance)
            - as string - value with default distance
        """
        g = Graph(directed=directed)
        for value, edges in dict_struct.items():
            new_vertex = g.add_vertex(value)
            if edges:
                for edge in edges:
                    if isinstance(edge, (list, tuple, set)):
                        new_vertex_val, distance = edge
                    elif isinstance(edge, str):
                        new_vertex_val = edge
                        distance = 1
                    else:
                        raise ValueError(
                            "Wrong edge format: {}. Must be str or tuple "
                            "('A', 1)".format(edge))
                    v2 = g.add_vertex(new_vertex_val)
                    g.add_edge(v1=new_vertex, v2=v2, distance=distance)
        return g

    def as_dict(self):
        return {
            k: v.get_neighbors(values_list=True)
            for k, v in self.vertices.items()
        }

    def __contains__(self, item):
        if isinstance(item, Vertex):
            return item.value in self.vertices
        return item in self.vertices

    def __iter__(self):
        return self.vertices.values()

    def __len__(self):
        return self.size

    def __repr__(self):
        return "%s(directed=%s, size=%d)" % (
            self.__class__.__name__, self.is_directed, self.size)


class Path(object):
    """Dijkstra path helper. It stores result of Dijkstra path result dict and
    help to get full vertices path by source and destination values"""

    def __init__(self, path_dict):
        self._path_dict = path_dict
        self._idx = {v.value: v for v in path_dict.keys()}

    def get_path(self, src_value, dst_value):
        """Expand vertices path

        :param src_value: src vertex value
        :param dst_value: dst vertex value
        :return: list of vertices
        """
        vertex = self._path_dict[self._idx[dst_value]]
        path = [vertex]

        # collect path list in backward order
        while vertex.value != src_value:
            vertex = self._path_dict[vertex]
            path.append(vertex)

        # Reverse the path list and append destination vertex
        path = path[::-1]
        path.append(self._idx[dst_value])
        return path

    def __repr__(self):
        return "%s(of=%s)" % (self.__class__.__name__, self._idx.keys())


def dijkstra_search(vertex_1):
    """Dijkstra - Shortest Path Problem for Weighted Graphs

    Main idea is similar like in BFS but priority queue (heap) is used for
    vertices neighbors list

    :param vertex_1: start point
    """

    queue = []
    vertex_1.weight = 0

    # Push distance and vertex
    heapq.heappush(queue, (0, vertex_1))

    path = {vertex_1: None}
    distances = {vertex_1.value: 0}
    weights = {vertex_1: 0}

    while len(queue):
        current_weight, current_v = heapq.heappop(queue)

        with current_v as current_v:
            for neighbor, dst in current_v.get_neighbors():
                if neighbor.is_visited:
                    continue

                if neighbor not in weights:
                    weights[neighbor] = weights[current_v] + dst

                # Save predecessor if not presented
                if neighbor not in path:
                    path[neighbor] = current_v

                # Find a path shorter than previous
                if weights[current_v] + dst < weights[neighbor]:
                    weights[neighbor] = weights[current_v] + dst
                    # Update predecessor
                    path[neighbor] = current_v

                # Update distance
                distances[neighbor.value] = weights[neighbor]
                heapq.heappush(queue, (weights[neighbor], neighbor))

    return distances, Path(path_dict=path)


if __name__ == '__main__':
    graph = {'A': ['B', 'C'],
             'B': ['C', 'D'],
             'C': ['D'],
             'D': ['C'],
             'E': ['F'],
             'F': ['C']}

    assert find_path(graph=graph, start='A', end='D') == ['A', 'B', 'C', 'D']
