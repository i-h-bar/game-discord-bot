import itertools


def get_function_name(func):
    index = 0

    for index, (func_letter, wrapper_letter) in enumerate(zip(func.__name__, itertools.cycle("wrapper"))):
        if func_letter != wrapper_letter:
            break

    return func.__name__[index - index % 7:]
