"""Different utilities for bruteforce problem solutions"""


def permutations(arr: list, l: int, r: int):
    """Generate all permutations of an array using backtracking

    Complexity: 2^n

    """
    if l == r:
        print(''.join(arr))

    for i in range(l, r):
        arr[l], arr[i] = arr[i], arr[l]
        permutations(arr, l + 1, r)
        arr[l], arr[i] = arr[i], arr[l]


def perms_graph(curr: list, remains: list):
    for i in range(len(remains)):
        new_remains = remains[:]
        new_cur = curr + [new_remains.pop(i)]
        # last child
        if len(new_remains) == 0:
            print(new_cur)
            return new_cur
        perms_graph(new_cur, new_remains)


def gen_all_subsequences(slovo: str):
    """ Generate all subsequences of a string

    Complexity: 2^n

    :param slovo: initial string
    :return:

    NOTE: to avoid duplicates set can be used to collect subsequences
    """

    def gen_subsequence(slovo: str, start: int, end: int):
        if end > len(slovo):
            return ''
        if start > end:
            return ''

        prefix = slovo[start:end]
        for c in slovo[end:]:
            print(prefix + c)
        gen_subsequence(slovo, start, end + 1)

    for i in range(len(slovo)):
        gen_subsequence(slovo[i:], 0, 1)


if __name__ == '__main__':
    arr = ['A', 'B', 'C']
    permutations(arr, 0, len(arr))

    # permutations(['B', 'C', 'A'])
    # perms_graph([], arr)

    # gen_all_subsequences('abppplee')

