# -*- coding: utf-8 -*-
"""Minimum spanning tree using Kruskal’s Algorithm"""

from structures.disjoint_set import DSet


if __name__ == '__main__':
    # Format: (node P, node Q, distance)
    # https://he-s3.s3.amazonaws.com/media/uploads/6322896.jpg
    g = [
        ('A', 'B', 1),
        ('A', 'C', 7),

        ('B', 'C', 5),
        ('B', 'D', 4),
        ('B', 'E', 3),

        ('C', 'E', 6),
        ('D', 'E', 2),
    ]

    dset = DSet(['A', 'B', 'C', 'D', 'E'])
    mst = []
    for p, q, distance in sorted(g, key=lambda item: item[2]):
        print('--> %s' % ([p, q, distance]))
        if dset.connected(p, q):
            print('Cycle detected')
            continue
        dset.union(p, q)
        mst.append((p, q, distance))

    assert mst == [('A', 'B', 1), ('D', 'E', 2), ('B', 'E', 3), ('B', 'C', 5)]
