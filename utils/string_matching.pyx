import numpy as np
cimport numpy as np

np.import_array()



def distance(string_1: str, string_2: str) -> int:
    return _distance(string_1, string_2)


cdef int _distance(str string_1, str string_2):
    cdef int x
    cdef int y

    cdef object[:, :] matrix = np.zeros((len(string_1) + 1, len(string_2) + 1), dtype=object)

    for x in range(matrix.shape[0]):
        matrix[x, 0] = x

    for y in range(matrix.shape[1]):
        matrix[0, y] = y

    for x in range(1, matrix.shape[0]):
        for y in range(1, matrix.shape[1]):
            if string_1[x - 1] == string_2[y - 1]:
                matrix[x, y] = matrix[x - 1, y - 1]
            else:
                matrix[x, y] = min(matrix[x - 1, y - 1], matrix[x - 1, y], matrix[x, y - 1]) + 1

    return matrix[-1, -1]


def longest_sequence(string_1: str, string_2: str) -> int:
    return _longest_sequence(string_1, string_2)


cdef int _longest_sequence(str string_1, str string_2):
    cdef int x
    cdef int y
    cdef object[:, :] matrix = np.zeros((len(string_1) + 1, len(string_2) + 1), dtype=object)

    for x in range(1, matrix.shape[0]):
        for y in range(1, matrix.shape[1]):
            if string_1[x - 1] == string_2[y - 1]:
                matrix[x, y] = matrix[x - 1, y - 1] + 1

    return np.sum(matrix)