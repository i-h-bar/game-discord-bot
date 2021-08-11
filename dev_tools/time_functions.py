import functools
import time

from dev_tools.functions import get_function_name


def async_time_it(coroutine):
    coroutine_name = get_function_name(coroutine)

    @functools.wraps(coroutine)
    async def wrapper(*args, **kwargs):
        nonlocal coroutine_name

        t1 = time.time()
        return_obj = await coroutine(*args, **kwargs)
        total_time = time.time() - t1

        print(f"{coroutine_name} took {total_time: .3f}s")

        return return_obj

    return wrapper


def time_it(func):
    func_name = get_function_name(func)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal func_name

        t1 = time.time()
        return_obj = func(*args, **kwargs)
        total_time = time.time() - t1

        print(f"{func_name} took {total_time: .3f}s")

        return return_obj

    return wrapper
