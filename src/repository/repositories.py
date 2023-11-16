from abc import ABC, abstractmethod
from sqlalchemy import delete, insert, update, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import UserScheme, PlaylistSheme, TrackSheme


class AbstractRepository(ABC):
    """Abstract repository"""
    
    @abstractmethod
    async def create():
        raise NotImplementedError
    
    @abstractmethod
    async def read():
        raise NotImplementedError

    @abstractmethod
    async def update():
        raise NotImplementedError

    @abstractmethod
    async def delete():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: dict):
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def read(self, filter_by: dict):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        return res.scalars()
    
    async def update(self, id: int, data: dict) -> int:
        stmt = update(self.model).values(**data).filter_by(id=id).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def delete(self, data: dict):
        stmt = delete(self.model).filter_by(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()


class UserRepository(SQLAlchemyRepository):
    model = UserScheme


class PlaylistRepository(SQLAlchemyRepository):
    model = PlaylistSheme


class TrackRepository(SQLAlchemyRepository):
    model = TrackSheme
