import numpy as np
cimport numpy as np

def levenshtein_distance(string_1: str, string_2: str) -> int:
    return c_levenshtein_distance(string_1.encode(), string_2.encode())

def index_of_potentials(item_to_find: str, items: list[bytes]) -> list[int]:
    return list(c_index_of_potentials(item_to_find.encode(), items))


def index_below_threshold(item_to_find: bytes, items: list[bytes], threshold: int = 7) -> memoryview:
    return c_index_below_threshold(item_to_find, items, threshold)

cdef int[:] c_index_below_threshold(char *item_to_find, list items, int threshold):
    cdef int i
    return np.array([i for i in range(len(items)) if c_levenshtein_distance(item_to_find, items[i]) < threshold], dtype=int)

cdef long long[:] c_index_of_potentials(char *item_to_find, list items):
    cdef int i
    cdef int[:] levs = np.zeros(len(items), dtype=int)


    for i in range(len(items)):
        levs[i] = c_levenshtein_distance(item_to_find, items[i])

    return np.argpartition(levs, 10)[:10]

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


def consecutive_sequence_score(string_1: str, string_2: str) -> int:
    return _consecutive_sequence_score(string_1.encode(), string_2.encode())


cdef int _consecutive_sequence_score(char *string_1, char *string_2):
    cdef int x
    cdef int y
    cdef int[:, :] matrix = np.zeros((len(string_1) + 1, len(string_2) + 1), dtype=int)

    for x in range(1, matrix.shape[0]):
        for y in range(1, matrix.shape[1]):
            if string_1[x - 1] == string_2[y - 1]:
                matrix[x, y] = matrix[x - 1, y - 1] + 1

    return np.sum(matrix) / len(string_2)
