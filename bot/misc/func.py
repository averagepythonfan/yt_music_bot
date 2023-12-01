from typing import Optional
import aiohttp
from .enums import Request


async def back_request(req: Request,
                       url: str = "url",
                       params: dict = dict()) -> Optional[bool]:
    """Makes a request to backend: GET or POST"""

    async with aiohttp.ClientSession() as session:
        if req is Request.get:
            async with session.get(url, params=params) as resp:
                if resp.status == 200:
                    return await resp.json()
        elif req is Request.post:
            async with session.post(url, json=params) as resp:
                if resp.status == 200:
                    return True