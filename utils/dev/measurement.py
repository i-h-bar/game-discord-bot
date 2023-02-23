import functools
import inspect
import time

from utils.dev.functions import get_function_name


def async_time_it(coroutine):
    coroutine_name = get_function_name(coroutine)
    spec = inspect.getfullargspec(coroutine)
    coro_kwargs = {k: v for k, v in zip(spec.args[-len(spec.defaults):], spec.defaults)}

    @functools.wraps(coroutine)
    async def wrapper(*args, **kwargs):
        nonlocal coroutine_name, coro_kwargs

        kwargs = coro_kwargs | kwargs

        t1 = time.time()
        return_obj = await coroutine(*args, **kwargs)
        total_time = time.time() - t1

        print(
            f"{coroutine_name}"
            f"({', '.join(str(arg) for arg in args) if args else ''}"
            f"{', ' if args and kwargs else ''}"
            f"{', '.join(f'{k}={v}' for k, v in kwargs.items()) if kwargs else ''}) "
            f"took {total_time: .3f}s"
        )

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
