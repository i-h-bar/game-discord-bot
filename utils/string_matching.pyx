import numpy as np
cimport numpy as np


def distance(string_1: bytes, string_2: bytes) -> int:
    return c_levenshtein_distance(string_1, string_2)


cdef int c_levenshtein_distance(char *a, char *b):
    cdef int x = len(a) + 1
    cdef int y = len(b) + 1
    cdef int i, j
    cdef int[:, :] d = np.zeros((x, y), dtype=int)
    for i in range(x):
        d[i][0] = i
    for j in range(y):
        d[0][j] = j
    for i in range(1, x):
        for j in range(1, y):
            if a[i-1] == b[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                d[i][j] = min(d[i-1][j], d[i][j-1], d[i-1][j-1]) + 1
    return d[x - 1][y - 1]


def consecutive_sequence_score(string_1: bytes, string_2: bytes) -> int:
    return _consecutive_sequence_score(string_1, string_2)


cdef int _consecutive_sequence_score(char *string_1, char *string_2):
    cdef int i
    cdef int j
    cdef int x = len(string_1) + 1
    cdef int y = len(string_2) + 1
    cdef int[:, :] matrix = np.zeros((x, y), dtype=int)
    cdef int score = 0

    for i in range(1, x):
        for j in range(1, y):
            if string_1[i - 1] == string_2[j - 1]:
                matrix[i][j] = matrix[i - 1][j - 1] + 1
                score += matrix[i][j]

    return score
