import httpx
from cache import AsyncTTL
from httpx import Timeout


@AsyncTTL(time_to_live=86400, min_cleanup_interval=3600)
async def async_get(url: str, return_json: bool = True):
    async with httpx.AsyncClient(timeout=Timeout(timeout=10.0)) as client:
        raw_response = await client.get(url)

    if return_json:
        return raw_response.json()
    else:
        return raw_response
