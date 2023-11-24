from bot.misc import back_request, Request
from bot.config import BACKEND


class TrackBotService:


    @staticmethod
    async def upload_track(url, user_id):
        return await back_request(
            req=Request("post"),
            url=f"http://{BACKEND}:9090/track/upload",
            params={
                "user_id": user_id,
                "url": url,
            }
        )