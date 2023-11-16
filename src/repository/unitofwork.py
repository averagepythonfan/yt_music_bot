from abc import ABC, abstractmethod
from typing import Type
from src.db import async_session_maker
from .repositories import (
    UserRepository,
    PlaylistRepository,
    TrackRepository
)


class InterfaceUnitOfWork(ABC):
    users: Type[UserRepository]
    tasks: Type[PlaylistRepository]
    task_history: Type[TrackRepository]
    
    @abstractmethod
    async def __init__(self):
        raise NotImplementedError()


    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError()


    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError()


    @abstractmethod
    async def commit(self):
        raise NotImplementedError()


    @abstractmethod
    async def rollback(self):
        raise NotImplementedError()


class UnitOfWork:

    def __init__(self):
        self.session_factory = async_session_maker


    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UserRepository(self.session)
        self.playlists = PlaylistRepository(self.session)
        self.tracks = TrackRepository(self.session)


    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()


    async def commit(self):
        await self.session.commit()


    async def rollback(self):
        await self.session.rollback()
