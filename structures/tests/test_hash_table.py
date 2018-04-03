from structures.hash_table import LinearProbingHashTable


def test_linear_probing_ht():
    t = LinearProbingHashTable()
    t.put('z', 1)
    t.put('b', 2)
    t.put('c', 3)

    assert t.size == 3
    assert t.get('b') == 2

    assert t.delete('b')
    assert t.get('b') is None
    assert t.size == 2
    for i in range(5000):
        t.put(i, i)
