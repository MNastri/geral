"""Learning Dynamic Programing."""
from typing import (
    List,
    NamedTuple,
)

INPUT_ARRAYS = [[-7, 3, 4, -2, -3, 1, -3]]


class MinSubArray(NamedTuple):
    index_start: int
    index_end: int
    sub_array_sum: int


def min_sum(array: List) -> MinSubArray:
    """
    Calculates the minimum sum of a continuous sub-array of array.
    Returns a named tuple with attributes sub_array_sum, with the actual minimum
    sum; index_start, with the starting index for the sub-array; and index_end,
    with the ending index for the sub-array.
    :param array:
    :return:
    """
    print(array)
    if len(array) == 0:
        return MinSubArray(0, 0, 0)
    if len(array) == 1:
        return MinSubArray(0, 0, array[0])
    mini_sum = float("inf")
    c_sum = float("inf")
    min_st_idx = 0
    min_en_idx = 0
    c_st_idx = 0
    print("minimo global é", mini_sum)
    print("minimo atual é", c_sum)

    for current_end_index, number in enumerate(array):
        print()
        print("verifica", number)
        c_sum += number
        print("minimo atual é", c_sum)
        if number < c_sum:
            print(number, "é menor que minimo atual")
            c_sum = number
            c_st_idx = current_end_index
        if c_sum < mini_sum:
            print("minimo atual é menor que minimo global")
            mini_sum = c_sum
            min_st_idx = c_st_idx
            min_en_idx = current_end_index
        print("minimo global é", mini_sum)
    return MinSubArray(min_st_idx, min_en_idx, mini_sum)


if __name__ == "__main__":
    soma = min_sum(INPUT_ARRAYS)
    for array in INPUT_ARRAYS:
        print(array, "=>", soma)
