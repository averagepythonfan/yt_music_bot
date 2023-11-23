from src.repository import InterfaceUnitOfWork
from src.schemas import TrackModel
from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError


class TrackService:
    """Class for track interactions."""


    @staticmethod
    async def add_track(uow: InterfaceUnitOfWork,
                        track: TrackModel) -> Optional[int]:
        """Create track"""

        data = track.model_dump(exclude_none=True)
        async with uow:
            pl_id = await uow.tracks.create(data=data)
            await uow.commit()
            return pl_id


    @staticmethod
    async def read_track(uow: InterfaceUnitOfWork,
                         track_id: Optional[int] = None) -> List[TrackModel]:
        """Finds track by ID, might be `None`.
        Return list of one or several tracks"""

        async with uow:
            if track_id:
                data = {"id": track_id}
            else:
                data = {}
            pls = await uow.tracks.read(filter_by=data)
            return pls


    @staticmethod
    async def update_track(uow: InterfaceUnitOfWork,
                           data: dict,
                           track_id: int) -> Optional[bool]:
        """Update playlist data by ID.
        Return `True` if success, otherwise `None`"""

        async with uow:
            res = await uow.tracks.update(id=track_id, data=data)
            if res:
                await uow.commit()
                return True
    

    @staticmethod
    async def delete_track(uow: InterfaceUnitOfWork,
                           track_id: int) -> Optional[int]:
        """Delete track by ID.
        Return its ID, or `None`"""

        data = {"id": track_id}
        async with uow:
            try:
                res = await uow.tracks.delete(data=data)
                await uow.commit()
                return res
            except SQLAlchemyError:
                pass
                # >>> logger
