import logging
from typing import Annotated, List
from celery.result import AsyncResult
from fastapi import APIRouter, Depends, HTTPException
from src.schemas import TrackModel, SingleVid
from src.services import TrackService, YouTubeService, PlaylistService
from src.repository import UnitOfWork, InterfaceUnitOfWork
from src.tasks.tasks import yt_task
from src.services.misc import podcast_lenght


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/track",
    tags=["Track CRUD"]
)


@router.post("/")
async def create_new_track(
    track: TrackModel,
    uow: Annotated[InterfaceUnitOfWork, Depends(UnitOfWork)]
):
    """Create track by its own data"""

    result = await TrackService.add_track(uow=uow, track=track)
    if result:
        return {"result": result}
    else:
        raise HTTPException(
            status_code=444,
            detail={"failed": "track already exists"}
        )


@router.get("/")
async def get_tracks(
    uow: Annotated[InterfaceUnitOfWork, Depends(UnitOfWork)]
):
    """Return a List of available tracks"""

    return {"result": await TrackService.read_track(uow=uow)}


@router.get("/{user_id}")
async def get_playlist_by_id(
    track_id: int,
    uow: Annotated[InterfaceUnitOfWork, Depends(UnitOfWork)]
):
    """Return a list of one track's data"""

    return {"result": await TrackService.read_track(uow=uow, track_id=track_id)}


@router.patch("/")
async def update_track(
    data: dict,
    track_id: int,
    uow: Annotated[InterfaceUnitOfWork, Depends(UnitOfWork)]
):
    """Update playlist by playlist's ID
    
    :params: `data` - must be dict
    :params: `track_id` - must be integer and existing
    
    Return `True` or `None`"""

    result = await TrackService.update_track(
        uow=uow,
        track_id=track_id,
        data=data
    )
    if result:

        return {"response": result}


@router.delete("/")
async def delete_track_by_id(
    track_id: int,
    uow: Annotated[InterfaceUnitOfWork, Depends(UnitOfWork)]
):
    """Delete playlist by playlist's ID
    
    :params: `pl_id` - must be integer and existing
    
    Return deleted playlist ID, or `None`"""

    result = await TrackService.delete_track(uow=uow, track_id=track_id)
    if result:
        return {"response": result}
    else:
        raise HTTPException(
            status_code=463,
            detail={"fail": "track not found"}
        )


@router.post("/upload")
async def upload_track(
    vid: SingleVid,
    uow: Annotated[InterfaceUnitOfWork, Depends(UnitOfWork)],
    podcast: bool = False,
):
    """Requires a single video scheme: url and user ID.
    
    Return a track_id that depends on message id from tg response."""

    podcast_opt = {
        'format': 'mp3/bestaudio/best',
        'match_filter': podcast_lenght,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
    }

    yt_opt = podcast_opt if podcast else None

    resp: AsyncResult = yt_task.delay(vid.url, vid.user_id, yt_opt)
    resp = resp.get()

    # logger.info(f"Response from celery: {resp}")

    if isinstance(resp, dict):
        plst_lst: List[dict] = await PlaylistService.read_playlist(
            uow=uow,
            data={"user_id": vid.user_id, "playlist_name": "other"}
        )

        plst = plst_lst[0]
        playlist_id = plst.get("id")

        try:
            tn = resp['result']['audio']['thumbnail']['file_id']
        except KeyError:
            tn = None

        track = TrackModel(
            id=resp["result"]["message_id"],
            playlist_id=playlist_id,
            track_link=vid.url,
            track_tg_id=resp['result']['audio']['file_id'],
            track_thumbnail=tn,
            performer=resp['result']['audio']['performer'],
            title=resp['result']['audio']['title']
        )

        track_response = await TrackService.add_track(uow=uow, track=track)

        logger.info(f"track added: {track_response}")

        return {"result": track_response}

    elif isinstance(resp, str):
        logger.info(f"failed to add track: {resp}")
        return {"status": "failed",
                "message": f"{resp}"}



@router.get("/check/{url}")
async def check_title(
    url: str
):
    """Check video title"""

    yt = YouTubeService(url=url)
    return await yt.check_track_data()