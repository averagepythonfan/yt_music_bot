from re import I
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from src.schemas import UserModel
from src.services import UsersService
from src.repository import UnitOfWork, InterfaceUnitOfWork


router = APIRouter(
    prefix="/user",
    tags=["User CRUD"]
)


@router.post("/")
async def create_new_user(
    user: UserModel,
    uow: Annotated[InterfaceUnitOfWork, Depends(UnitOfWork)]
):
    result = await UsersService.add_user(uow=uow, user=user)
    if result:
        return {"result": result}
    else:
        raise HTTPException(
            status_code=444,
            detail={"failed": "user already exists"}
        )


@router.get("/")
async def get_users(
    uow: Annotated[InterfaceUnitOfWork, Depends(UnitOfWork)]
):
    return {"result": await UsersService.read_user(uow=uow)}


@router.get("/{user_id}")
async def get_user_by_id(
    user_id: int,
    uow: Annotated[InterfaceUnitOfWork, Depends(UnitOfWork)]
):
    return {"result": await UsersService.read_user(uow=uow, user_id=user_id)}


@router.patch("/")
async def update_status(
    status: str,
    user_id: int,
    uow: Annotated[InterfaceUnitOfWork, Depends(UnitOfWork)]
):
    """Update status by user's ID
    
    :params: `status` - must be str: 'guest' or 'admin'
    :params: `user_id` - must be integer and existing
    
    Return `True` or `None`"""

    result = await UsersService.update_status(uow=uow, id=user_id, status=status)
    if result:
        return {"response": result}


@router.delete("/")
async def delete_user_by_id(
    user_id: int,
    uow: Annotated[InterfaceUnitOfWork, Depends(UnitOfWork)]
):
    """Delete user by user's ID
    
    :params: `user_id` - must be integer and existing
    
    Return deleted user ID, or `None`"""

    result = await UsersService.delete_user(uow=uow, user_id=user_id)
    if result:
        return {"response": result}
    else:
        raise HTTPException(
            status_code=463,
            detail={"fail": "user not found"}
        )