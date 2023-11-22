from src.repository import InterfaceUnitOfWork
from src.schemas import UserModel
from typing import Optional


class UsersService:

    @staticmethod
    async def add_user(uow: InterfaceUnitOfWork, user: UserModel) -> int:
        """Create a new user, default status: guest
        If success, return a user id"""

        data = user.model_dump(exclude_none=True)
        async with uow:
            user_id = await uow.users.create(data=data)
            await uow.commit()
            return user_id


    @staticmethod
    async def read_user(uow: InterfaceUnitOfWork, user_id: Optional[int] = None):
        async with uow:
            if user_id:
                data = {"id": user_id}
            else:
                data = {}
            user = await uow.users.read(filter_by=data)
            return user


    @staticmethod
    async def update_status(uow: InterfaceUnitOfWork, status: str, id: int):
        data = {"status": status}
        async with uow:
            res = await uow.users.update(id=id, data=data)
            await uow.commit()
            return res


    @staticmethod
    async def delete_user(uow: InterfaceUnitOfWork, user: UserModel):
        data = user.model_dump(exclude_none=True)
        async with uow:
            res = await uow.users.delete(data=data)
            await uow.commit()
            return res
