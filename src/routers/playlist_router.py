from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from src.schemas import PlaylistModel
from src.services import PlaylistService
from src.repository import UnitOfWork, InterfaceUnitOfWork


router = APIRouter(
    prefix="/playlist",
    tags=["Playlists CRUD"]
)


@router.post("/")
async def create_new_playlist(
    pl: PlaylistModel,
    uow: Annotated[InterfaceUnitOfWork, Depends(UnitOfWork)]
):
    result = await PlaylistService.add_playlist(uow=uow, pl=pl)
    if result:
        return {"result": result}
    else:
        raise HTTPException(
            status_code=444,
            detail={"failed": "playlist already exists"}
        )


@router.get("/")
async def get_playlists(
    uow: Annotated[InterfaceUnitOfWork, Depends(UnitOfWork)]
):
    return {"result": await PlaylistService.read_playlist(uow=uow)}


@router.get("/{user_id}")
async def get_playlist_by_id(
    pl_id: int,
    uow: Annotated[InterfaceUnitOfWork, Depends(UnitOfWork)]
):
    return {"result": await PlaylistService.read_playlist(uow=uow, pl_id=pl_id)}


@router.patch("/")
async def update_playlist(
    data: dict,
    pl_id: int,
    uow: Annotated[InterfaceUnitOfWork, Depends(UnitOfWork)]
):
    """Update playlist by playlist's ID
    
    :params: `data` - must be dict
    :params: `pl_id` - must be integer and existing
    
    Return `True` or `None`"""

    result = await PlaylistService.update_playlist(
        uow=uow,
        pl_id=pl_id,
        data=data
    )
    if result:
        return {"response": result}


@router.delete("/")
async def delete_playlist_by_id(
    pl_id: int,
    uow: Annotated[InterfaceUnitOfWork, Depends(UnitOfWork)]
):
    """Delete playlist by playlist's ID
    
    :params: `pl_id` - must be integer and existing
    
    Return deleted playlist ID, or `None`"""

    result = await PlaylistService.delete_playlist(uow=uow, pl_id=pl_id)
    if result:
        return {"response": result}
    else:
        raise HTTPException(
            status_code=463,
            detail={"fail": "playlist not found"}
        )