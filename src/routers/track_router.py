from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from src.schemas import TrackModel
from src.services import TrackService
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
