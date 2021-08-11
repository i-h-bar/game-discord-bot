import collections


def initialise(string: str):
    return "".join([word[0] for word in string.split(" ")])


def quick_gestalt(str_1: str, str_2: str) -> float:
    return (2 * sum((collections.Counter(str_1) & collections.Counter(str_2)).values()))/(len(str_1) + len(str_2))