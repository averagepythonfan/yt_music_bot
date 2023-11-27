from bot.misc import back_request, Request
from bot.config import BACKEND


class TrackBotService:


    @staticmethod
    async def upload_track(url: str, user_id: int):
        return await back_request(
            req=Request("post"),
            url=f"http://{BACKEND}:9090/track/upload",
            params={
                "user_id": user_id,
                "url": url,
            }
        )


    @staticmethod
    async def check_title(url: str):
        return await back_request(
            req=Request("get"),
            url=f"http://{BACKEND}:9090/track/check/{url}"
        )
