"""Learning Dynamic Programing."""
from itertools import product
from typing import (
    List,
    NamedTuple,
)

INPUT_ARRAYS = [
    [-7, 3, 4, -2, -3, 1, -3],
]
INPUT_ARRAYS.extend([list(pp) for pp in product([-10, -1, 0, 1, 10], repeat=3)])


class MinSubArray(NamedTuple):
    start_index: int
    end_index: int
    sum: int


def min_sum(array: List) -> MinSubArray:
    """
    Calculates the minimum sum of a continuous sub-array of array.
    Returns a named tuple with attributes sum, with the actual minimum
    sum; start_index, with the starting index for the sub-array; and end_index,
    with the ending index for the sub-array.

    NAIVE APPROACH?
    :param array:
    :return:
    """
    if len(array) == 0:
        return MinSubArray(0, 1, 0)
    if len(array) == 1:
        return MinSubArray(0, 1, array[0])
    mini_sum = float("inf")
    c_sum = float("inf")
    min_st_idx = 0
    min_en_idx = 0
    c_st_idx = 0
    for c_en_idx, number in enumerate(array):
        if number < c_sum:
            c_sum = number
            c_st_idx = c_en_idx
        elif number >= c_sum:
            c_sum += number
        if c_sum < mini_sum:
            mini_sum = c_sum
            min_st_idx = c_st_idx
            min_en_idx = c_en_idx
    return MinSubArray(min_st_idx, min_en_idx + 1, mini_sum)


# if __name__ == "__main__":
#     for array in INPUT_ARRAYS:
#         min_sum_array = min_sum(array)
#         st = min_sum_array.start_index
#         en = min_sum_array.end_index
#         print(array, "=>", array[st:en], "soma", min_sum_array.sum)


def dp_min_sum(array: List[int], min_sum_so_far=None, current_sum=None)->int:
    """
    Calculates the minimum sum of a continuous sub-array of array.
    Returns a named tuple with attributes sum, with the actual minimum
    sum; start_index, with the starting index for the sub-array; and end_index,
    with the ending index for the sub-array.

    DYNAMIC PROGRAMING APPROACH?
    :param array:
    :param min_sum_so_far:
    :param current_sum:
    :return:
    """
    if not array:
        return min_sum_so_far
    element = array[0]
    if min_sum_so_far is None:
        min_sum_so_far = float("inf")
    if current_sum is None:
        current_sum = float("inf")
    if element < min_sum_so_far:
        min_sum_so_far = element
    elif (element >= min_sum_so_far) and (element < current_sum):
        current_sum = element
    elif (element >= min_sum_so_far) and (element >= current_sum):
        current_sum += element
    return dp_min_sum(
        array=array[1:], min_sum_so_far=min_sum_so_far, current_sum=current_sum
    )


if __name__ == "__main__":
    for array in INPUT_ARRAYS:
        min_sum_array = dp_min_sum(array)
        st = min_sum_array.start_index
        en = min_sum_array.end_index
        print(array, "=>", array[st:en], "soma", min_sum_array.sum)
