# -*- coding: utf-8 -*-


def get_mid(start, end):
    return start + ((end - start) // 2)


def binary_search(arr, key):
    arr = sorted(arr)
    n = len(arr)
    lo, hi = 0, n - 1  # lower and higher search bounds

    while lo <= hi:
        # [lo, .., hi]  --> [.., lo, .., hi, ..] and to get mid index you need
        # to add lo value to (hi - lo)
        # mid = (hi - lo) + lo // 2
        mid = get_mid(lo, hi)
        if key > arr[mid]:
            lo = mid + 1
        elif key < arr[mid]:
            hi = mid - 1
        else:
            return mid
    return -1


if __name__ == '__main__':
    A = [1, 2, 3, 4, 5]
    assert binary_search(A, 5) == 4
    assert binary_search(A, 2) == 1
    assert binary_search(A, 1) == 0
    assert binary_search(A, 0) == -1
    assert binary_search(A, 6) == -1
