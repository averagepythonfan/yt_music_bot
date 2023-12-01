from asyncio import run
from celery import Celery
from src.config import REDIS_HOST, REDIS_PASSWORD
from src.services import YouTubeService
from src.services import VideoTooLong


celery = Celery("celery")


celery.conf.broker_url = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:6379"
celery.conf.result_backend = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:6379"


async def yt_service_run(url: str, user_id: int):
    yt = YouTubeService(url=url)
    try:
        return await yt.from_yt_to_tg(user_id=user_id)
    except VideoTooLong as e:
        return f"{e}"


@celery.task(name="yt_task")
def yt_task(url: str, user_id: int):
    return run(yt_service_run(url=url, user_id=user_id))
