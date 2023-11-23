from typing import Optional
import aiohttp
from src.config import TOKEN
from enum import Enum


async def pic_content(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return resp


async def tg_post_request(pic: str, track: str, payload: dict) -> Optional[dict]:
    async with aiohttp.ClientSession() as session:
        try:
            audio = open(track, "rb")
            thumbnail = open(pic, "rb")
            async with session.post(
                f"https://api.telegram.org/bot{TOKEN}/sendAudio",
                data={"audio": audio, "thumbnail": thumbnail},
                payload=payload
            ) as resp:
                return resp
        except aiohttp.ClientError as e:
            pass
        finally:
            audio.close()
            thumbnail.close()


class YtInstance(Enum):
    video = "video"
    playlist = "playlist"
