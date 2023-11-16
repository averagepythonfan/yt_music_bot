from src.repository import InterfaceUnitOfWork
from src.schemas import UserModel


class UsersService:

    @staticmethod
    async def add_user(uow: InterfaceUnitOfWork, user: UserModel) -> int:
        """Create a new user, default status: guest
        If success, return a user id"""

        data = user.model_dump()
        async with uow:
            user_id = await uow.users.create(data=data)
            await uow.commit()
            return user_id


    @staticmethod
    async def read_user(uow: InterfaceUnitOfWork, user_id: int):
        data = {"id": user_id}
        async with uow:
            user = await uow.users.read(data)
            return user

    @staticmethod
    async def update_status(uow: InterfaceUnitOfWork, user: UserModel, id: int):
        data = user.model_dump()
        async with uow:
            res = await uow.users.update(id=id, data=data)
            await uow.commit()
            return res

    @staticmethod
    async def delete_user(uow: InterfaceUnitOfWork, user: UserModel):
        data = user.model_dump()
        async with uow:
            res = await uow.users.delete(data=data)
            await uow.commit()
            return res