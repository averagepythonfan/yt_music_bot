from typing import Optional
import aiohttp
from src.config import TOKEN
from enum import Enum
from aiohttp import FormData


async def pic_content(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return resp


async def tg_post_request(formdata: FormData) -> Optional[dict]:
    """Makes a POST request to Telegram server.
    Return a dict data, otherwise return `None`."""

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                f"https://api.telegram.org/bot{TOKEN}/sendAudio",
                data=formdata
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
        except aiohttp.ClientError as e:
            pass



class YtInstance(Enum):
    video = "video"
    playlist = "playlist"
