from re import I
from typing import Annotated
from fastapi import APIRouter, Depends
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
    return {"result": await UsersService.add_user(uow=uow, user=user)}


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
    return {"result": await UsersService.update_status(uow=uow, id=user_id, status=status)}


@router.delete("/")
async def delete_user_by_id(
    user: UserModel,
    uow: Annotated[InterfaceUnitOfWork, Depends(UnitOfWork)]
):
    return {"result": await UsersService.delete_user(uow=uow, user=user)}