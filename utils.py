"""
This file contains functions which are useful for any kind of data
manipulation but don't fit too well into any specific file.
"""

def unroll_list(in_list):
    """
    This function takes in a list of lists and
    unrolls them into a single list.

    Example:
    [[0, 0], [0, 1], [0, 2]] -> [0, 0, 0, 1, 0, 2]
    """

    return [j for i in in_list for j in i]


def unzip_list(in_list):
    """
    This function converts a list of tuples into a
    tuple of lists.

    Example:
    [(0, 0), (0, 1), (0, 2)] -> ([0, 0, 0], [0, 1, 2])
    """

    return list(zip(*in_list))
