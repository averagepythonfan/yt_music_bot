from bot.misc import Request, back_request
from bot.schemas import PlaylistModel
from bot.config import BACKEND
from typing import Optional


class PlaylistBotService:


    @staticmethod
    async def create_playlist(pl: PlaylistModel):
        return await back_request(
            req=Request('post'),
            url=f"http://{BACKEND}:9090/playlist/",
            params=pl.model_dump(exclude_none=True)
        )