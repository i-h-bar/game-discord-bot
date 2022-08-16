from utils import string_matching
from utils.aio.wrappers import asyncify


def initialise(string: str):
    return "".join([word[0] for word in string.split(" ")])


@asyncify
def async_sequence_score(item_1, item_2):
    return item_2, string_matching.consecutive_sequence_score(item_1, item_2)
