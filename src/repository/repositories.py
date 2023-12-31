from abc import ABC, abstractmethod
from typing import List
from sqlalchemy import delete, insert, update, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import Users, Playlists, Tracks


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
        self.session: AsyncSession = session

    async def create(self, data: dict) -> int:
        """Create a model's instance like user, playlist and track.
        Returns an instance ID"""

        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def read(self, filter_by: dict = None) -> list:
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        f = res.scalars()
        units = f.all()
        return [el.to_dict() for el in units]
    
    async def update(self, id: int, data: dict) -> int:
        stmt = update(self.model).values(**data).filter_by(id=id).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def delete(self, data: dict) -> int:
        stmt = delete(self.model).filter_by(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()


class UserRepository(SQLAlchemyRepository):
    model = Users


class PlaylistRepository(SQLAlchemyRepository):
    model = Playlists


class TrackRepository(SQLAlchemyRepository):
    model = Tracks
