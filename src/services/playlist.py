from src.repository import InterfaceUnitOfWork
from src.schemas import PlaylistModel
from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError


class PlaylistService:
    """Class for playlist interactions."""


    @staticmethod
    async def add_playlist(uow: InterfaceUnitOfWork,
                           pl: PlaylistModel) -> Optional[int]:
        """Create playlist.
        
        Return a playlist ID if success"""

        data = pl.model_dump(exclude_none=True)
        async with uow:
            pl_id = await uow.playlists.create(data=data)
            await uow.commit()
            return pl_id


    @staticmethod
    async def read_playlist(uow: InterfaceUnitOfWork,
                            data: Optional[dict] = {}) -> List[PlaylistModel]:
        """Finds playlist by ID, might be `None`.
        Return list of one or several playlists"""

        async with uow:
            pls = await uow.playlists.read(filter_by=data)
            return pls


    @staticmethod
    async def update_playlist(uow: InterfaceUnitOfWork,
                              data: dict,
                              pl_id: int) -> Optional[bool]:
        """Update playlist data by ID.
        Return `True` if success, otherwise `None`"""

        async with uow:
            res = await uow.playlists.update(id=pl_id, data=data)
            if res:
                await uow.commit()
                return True
    

    @staticmethod
    async def delete_playlist(uow: InterfaceUnitOfWork,
                              pl_id: int) -> Optional[int]:
        """Delete playlist by ID.
        Return its ID, or `None`"""

        data = {"id": pl_id}
        async with uow:
            try:
                res = await uow.playlists.delete(data=data)
                await uow.commit()
                return res
            except SQLAlchemyError:
                pass
                # >>> logger
