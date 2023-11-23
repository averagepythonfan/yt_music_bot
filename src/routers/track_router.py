from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from src.schemas import TrackModel
from src.services import TrackService, YouTubeService, PlaylistService
from src.repository import UnitOfWork, InterfaceUnitOfWork


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
    user_id: int,
    url: str,
    uow: Annotated[InterfaceUnitOfWork, Depends(UnitOfWork)]
):
    vid = YouTubeService(url=url)
    await vid.from_yt_to_tg(user_id=user_id)
    if vid.is_sended:
        plst_lst: List[dict] = await PlaylistService.read_playlist(
            uow=uow,
            data={"user_id": user_id, "playlist_name": "other"}
        )

        plst = plst_lst[0]

        playlist_id = plst.get("id")

        track = TrackModel(
            id=vid.response_data["result"]["message_id"],
            playlist_id=playlist_id,
            track_link=url,
            track_tg_id=vid.response_data['result']['audio']['file_id'],
            track_thumbnail=vid.response_data['result']['audio']['thumbnail']['file_id'],
            performer=vid.response_data['result']['audio']['performer'],
            title=vid.response_data['result']['audio']['title']
        )

        return {"result": await TrackService.add_track(uow=uow, track=track)}