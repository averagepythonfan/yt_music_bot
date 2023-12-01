from typing import Optional
import aiohttp
import logging
from .enums import Request

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("backend.request")


async def back_request(req: Request,
                       url: str = "url",
                       params: dict = dict()) -> Optional[dict]:
    """Makes a request to backend: GET or POST"""

    async with aiohttp.ClientSession() as session:
        if req is Request.get:
            async with session.get(url, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    logger.info(f"data: {data}")
                    return data
        elif req is Request.post:
            async with session.post(url, json=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    logger.info(f"data: {data}")
                    return data