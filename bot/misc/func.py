import aiohttp
from .enums import Request


async def back_request(req: Request, url: str = "url", **kwargs):
    async with aiohttp.ClientSession() as session:
        if req is Request.get:
            async with session.get(url, params=kwargs) as resp:
                assert resp.status == 200
                return await resp.json()
        elif req is Request.post:
            async with session.post(url, data=kwargs) as resp:
                assert resp.status == 200
                return await resp.json()