# -*- coding: utf-8 -*-


class DSet(object):
    """Disjoint set using union quick find implementation"""

    def __init__(self, data, getter=lambda p: p):
        self._map = {getter(item): i for i, item in enumerate(data)}
        self._index = list(range(len(data)))
        self._getter = getter

    def union(self, p, q):
        """Union of two elements

        """
        p_idx = self._map[self._getter(p)]
        q_idx = self._map[self._getter(q)]

        # Update all previous elements to the new root
        tmp_value = self._index[p_idx]
        for i in range(len(self._index)):
            if self._index[i] == tmp_value:
                self._index[i] = self._index[q_idx]

    def connected(self, p, q):
        p_val, q_val = map(self._getter, [p, q])
        return self._index[self._map[p_val]] == self._index[self._map[q_val]]


if __name__ == '__main__':
    dset = DSet(['A', 'B', 'C', 'D', 'E'])
    dset.union('A', 'B')
    dset.union('B', 'E')
    dset.union('E', 'D')

    assert dset.connected('A', 'E') is True
    assert dset.connected('D', 'C') is False
