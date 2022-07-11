import asyncio
import functools
from typing import Coroutine, Any, Callable, Awaitable


def asyncify(func) -> Callable[..., Coroutine[Any, Any, Awaitable[Any]]]:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        loop = asyncio.get_running_loop()

        return await loop.run_in_executor(None, functools.partial(func, *args, **kwargs))

    return wrapper
