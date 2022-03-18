"""Learning Dynamic Programing."""
# Standard Library
from typing import (
    Dict,
    List,
)

INPUT_ARRAY = [-7, 3, 4, -2, -3, 1, -3]


def sum_slice(array: List[int], start: int, end: int, cache: Dict) -> int:
    """
    Sums a semi-open slice [start,end) of the given array of ints, checking the cache for hits.
    cache is not working properly yet.
    :param array:
    :param start:
    :param end:
    :param cache:
    :return:
    """
    sl = slice(start, end, None)
    kk = str(sl)
    if kk in cache:
        # print(f"found sum for {sl} in cache, returning it. sum is {cache[kk]}")
        return cache[kk]
    cache[kk] = sum(array[sl])
    # string_array = (str(array[sl]) + " " * 30)[:30]
    # print(f"calculating sum for {sl} in array {string_array}...sum is {cache[kk]}")
    return cache[kk]


# if __name__ == "__main__":
#     cache = {str(slice(0, 1)): -7}
#     print(sum_slice(INPUT_ARRAY, 0, 1, cache))
#     print(sum_slice(INPUT_ARRAY, 0, 1, {}))
#     del cache


def min_sum(array: List) -> int:
    """
    Calculates the minimum sum of a continuous sub-array of array.
    returns the namedtuple with attributes value, with the actual minimum sum; start,
    with the starting index for the sub-array; and end, with the ending index for the
    sub-array.
    :param array:
    :return:
    """
    cache = {}
    result_sum = array[0]
    ll = len(array)
    for ss in range(ll):
        for ee in range(ss, ll + 1):
            result_sum = min(result_sum, sum_slice(array, ss, ee, cache))
    return result_sum


# if __name__ == "__main__":
#     result = min_sum(INPUT_ARRAY)
#     print(result)
