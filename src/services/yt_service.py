import copy
import os
from io import BytesIO
from typing import Optional
from yt_dlp import YoutubeDL
from .misc import (tg_post_request,
                   YtInstance,
                   longer_then_12_min)
from PIL import Image
from aiohttp import (ClientResponse,
                     ClientSession,
                     ClientError,
                     FormData)


class YouTubeService:
    """Service for working with yt-dlp, files
    and TelegramBot API."""


    default_config = {
        'format': 'mp3/bestaudio/best',
        'match_filter': longer_then_12_min,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
    }

    def __init__(self,
                 url: str,
                 yt_opt: dict = None,
                 instanse: YtInstance = YtInstance("video")) -> None:
        """Init YouTubeService instance.
        
        :param: `url` - must be `str`, a URL link of video.
            Might be earn from share and looks like:
            >>> url = "https://youtu.be/jyI2PqPsOFs?si=rz2eWeRuHX-iufcb"
            Simple link from address bar is also valid:
            >>> url = "https://www.youtube.com/watch?v=irfj8pQwhno"

        :param: `yt_opt` - a dict with yt-dlp config.
            If yt_opt is `None` then initialize default config from class attribute.

        :param: `instanse` - YtInstance object, might be
            YtInstance("video") or YtInstance("playlist"),
            otherwise raise Assertion Error."""

        assert isinstance(instanse, YtInstance), "YtInstance must be video or playlist"

        self.url = url
        self.config = self.default_config if yt_opt is None else yt_opt
        with YoutubeDL({}) as ydl:
            # download video metadata
            info = ydl.extract_info(self.url, download=False)
            self.video_title: str = copy.deepcopy(info['title'])
            self.channel_name: str = copy.deepcopy(info["channel"])
            self.thumb_link: str = copy.deepcopy(info["thumbnail"])
            del info
        self.config["outtmpl"] = f"{self.video_title}"
        self.path_music = f"{os.getcwd()}/{self.video_title}.mp3"
        self.is_sended = False
        if len(self.video_title.split(" - ", maxsplit=2)) == 2:
            self.performer, self.song_name = (
                el.strip() for el in self.video_title.split(" - ", maxsplit=2)
            )
        else:
            self.performer, self.song_name = self.channel_name, self.video_title
    

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
    

    async def check_track_data(self) -> dict:
        """Return a video data"""
        return {
            "title": self.video_title,
            "channel": self.channel_name,
            "thumbnail": self.thumb_link
        }


    def _extract_audio(self):
        """Download video and convert it to audio
        according to config.
        
        May throw yt-dlp exceptions"""

        with YoutubeDL(self.config) as ydl:
            self.error_code = ydl.download(self.url)
    

    async def fetch_pic(self) -> Optional[bytes]:
        """Download pic from vid's metadata.
        Using aiohttp's ClientSession.
        
        Return:
            `bytes` - if request was successfull.
            `None` - otherwise."""

        async with ClientSession() as session:
            async with session.get(self.thumb_link) as resp:
                if resp.status == 200:
                    return await resp.read()
                else:
                    raise ClientError("Failed to fetch pic")


    async def _extract_thumbnail(self) -> None:
        """Fetch pic from URL, crop it and resize it.
        Returns `None`"""

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
        """Delete audio and thumbnail files."""
        os.remove(self.path_music)
        os.remove(self.path_thumbnail)
    

    async def _send_to_user(self, user_id: int) -> Optional[ClientResponse]:
        """Send audio to user by user_id using TGBot API.
        :params: `user_id` - must be int
        
        Return response from telegram server or `None`."""

        data = FormData()

        data.add_field(name="chat_id", value=str(user_id))
        data.add_field(name="performer", value=self.performer)
        data.add_field(name="title", value=self.song_name)
        data.add_field(name="parse_mode", value="HTML")

        audio = open(self.path_music, "rb")

        data.add_field(
            name="audio",
            value=audio,
            filename=self.path_music,
            content_type="multipart/form-data"
        )

        thumbnail = open(self.path_thumbnail, "rb")

        data.add_field(
            name="thumbnail",
            value=thumbnail,
            filename=self.path_thumbnail,
            content_type="multipart/form-data"
        )

        response_data = await tg_post_request(
            formdata=data
        )

        audio.close()
        thumbnail.close()

        return response_data

    async def from_yt_to_tg(self, user_id: int):
        """Makes a full pipeline of YouTube-to-Telegram transitions."""
        self._extract_audio()
        await self._extract_thumbnail()
        self.response_data = await self._send_to_user(user_id=user_id)
        # if self.response_data:
        #     self.is_sended = True
        self._clear_data()
        return self.response_data