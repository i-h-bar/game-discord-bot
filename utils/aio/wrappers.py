import asyncio
import functools
import inspect
from typing import Coroutine, Any, Callable, Awaitable


def asyncify(func) -> Callable[..., Coroutine[Any, Any, Awaitable[Any]]]:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        loop = asyncio.get_running_loop()

        return await loop.run_in_executor(None, functools.partial(func, *args, **kwargs))

    return wrapper


def preserve_sig(wrapped):
    sig = inspect.signature(wrapped)

    def wrapper(func):
        func = functools.wraps(wrapped)(func)
        func.__signature__ = sig

        return func

    return wrapper

