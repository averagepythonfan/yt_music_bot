import copy
import os
from io import BytesIO
from fastapi.concurrency import contextmanager_in_threadpool
from yt_dlp import YoutubeDL
from .misc import (tg_post_request,
                   YtInstance,
                   pic_content)
from .track_service import TrackService
from src.schemas import TrackModel
from PIL import Image
from aiohttp import ClientResponse, ClientSession, ClientError


class YouTubeService:

    default_config = {
        'format': 'mp3/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
    }

    def __init__(self,
                 url: str,
                 yt_opt: dict = None,
                 instanse: YtInstance = YtInstance("video")) -> None:
        assert isinstance(instanse, YtInstance), "YtInstance must be video or playlist"
        self.url = url
        self.config = self.default_config if yt_opt is None else yt_opt
        with YoutubeDL({}) as ydl:
            info = ydl.extract_info(self.url, download=False)
            title = copy.deepcopy(info['title'])
            self.performer, self.song_name = (el.strip() for el in title.split("-"))
            self.thumb_link = copy.deepcopy(info["thumbnail"])
            del info
        self.config["outtmpl"] = f"{self.performer} - {self.song_name}"
        self.path_music = f"{os.getcwd()}/{self.performer} - {self.song_name}.mp3"
        self.is_sended = False
    

    @property
    def info(self) -> dict:
        return {
            "url": self.url,
            "config": self.config,
            "performer": self.performer,
            "song name": self.song_name,
            "thumbnail link": self.thumb_link,
            "path mp3": self.path_music,
        }
    

    def _extract_audio(self):
        with YoutubeDL(self.config) as ydl:
            error_code = ydl.download(self.url)
    

    async def fetch_pic(self) -> ClientResponse:
        async with ClientSession() as session:
            async with session.get(self.thumb_link) as resp:
                if resp.status == 200:
                    return await resp.read()
                else:
                    raise ClientError("Failed to fetch pic")


    async def _extract_thumbnail(self):
        pic = await self.fetch_pic()
        img = Image.open(BytesIO(pic))
        width, height = img.size

        sq = min([width, height])
        
        left = (width - sq)/2
        top = (height - sq)/2
        right = (width + sq)/2
        bottom = (height + sq)/2
        
        img = img.crop((left, top, right, bottom))
        img = img.resize(size=(320, 320))
        self.path_thumbnail = f"{os.getcwd()}/thumbnail.png"
        img.save(fp=self.path_thumbnail)


    def _clear_data(self):
        os.remove(self.path_music)
        os.remove(self.path_thumbnail)
    

    async def _send_to_user(self, user_id: int) -> ClientResponse:
        payload = {
            'chat_id': user_id,
            'performer': self.performer,
            "title": self.song_name,
            'parse_mode': 'HTML',
        }
        
        return await tg_post_request(
            pic=self.path_thumbnail,
            track=self.path_music,
            payload=payload
        )


    async def from_yt_to_tg(self, user_id: int):
        # print(f"[interface] start extract audio for {user_id}")
        self._extract_audio()
        # print("[interface] audio extracted")
        await self._extract_thumbnail()
        # print("[interface] thumbnail extracted")
        tg_response = await self._send_to_user(user_id=user_id)
        if tg_response.status == 200:
            # print("[interface] send audio to user")
            self._clear_data()
            # print("[interface] clear data")
            self.is_sended = True
        self.response_data = await tg_response.json()