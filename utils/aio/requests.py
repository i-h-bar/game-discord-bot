import httpx
from cache import AsyncTTL
from httpx import Timeout, Response

client = httpx.AsyncClient(timeout=Timeout(timeout=10.0))


@AsyncTTL(time_to_live=86400)
async def async_get(url: str) -> Response:
    return await client.get(url)
