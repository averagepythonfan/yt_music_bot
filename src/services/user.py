from src.repository import InterfaceUnitOfWork
from src.schemas import UserModel
from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError


class UsersService:
    """Class for user interactions based on CRUD.
    It integrates in user's endpoinds.
    Every static method accept an UoW interface,
    that manage ORM's repository,
    usually this is SQLAlchemy repositiry."""


    @staticmethod
    async def add_user(uow: InterfaceUnitOfWork,
                       user: UserModel) -> Optional[int | bool]:
        """Create a new user, default status: guest.
        Accepts a UoW interface and user's pydantic model.
        If success, return a user id, otherwise return `None`,
        else user already exist return `False`."""

        data = user.model_dump(exclude_none=True)
        async with uow:
            try:
                exist = uow.users.read(filter_by={"id": user.id})
                if exist:
                    return False
                user_id = await uow.users.create(data=data)
                await uow.commit()
                return user_id
            except SQLAlchemyError as e:
                await uow.rollback()
                # >>> logger alert


    @staticmethod
    async def read_user(uow: InterfaceUnitOfWork,
                        user_id: Optional[int] = None) -> List[UserModel]:
        """Finds user by ID, might be `None`.
        Return list of one or several user"""

        async with uow:
            if user_id:
                data = {"id": user_id}
            else:
                data = {}
            user = await uow.users.read(filter_by=data)
            return user


    @staticmethod
    async def update_status(uow: InterfaceUnitOfWork,
                            status: str,
                            id: int) -> Optional[bool]:
        """Update user's status by ID.
        Return `True` if success, otherwise `None`"""

        data = {"status": status}
        async with uow:
            res = await uow.users.update(id=id, data=data)
            if res:
                await uow.commit()
                return True


    @staticmethod
    async def delete_user(uow: InterfaceUnitOfWork,
                          user_id: int) -> Optional[int]:
        """Delete user by ID.
        Return its ID, or `None`"""

        data = {"id": user_id}
        async with uow:
            try:
                res = await uow.users.delete(data=data)
                await uow.commit()
                return res
            except SQLAlchemyError:
                pass
                # >>> logger