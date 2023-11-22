import datetime
from typing import Optional, List
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import DATE, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from schemas import UserModel, PlaylistModel, TrackModel


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "bot_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(5), default='guest')
    reg_date: Mapped[datetime.datetime] = mapped_column(DATE, default=datetime.datetime.today())

    playlists: Mapped[List["Playlists"]] = relationship()

    def to_dict(self) -> dict:
        unit = UserModel(
            id=self.id,
            username=self.username,
            status=self.status,
            reg_date=self.reg_date
        )
        return unit.model_dump(exclude_none=True)


class Playlists(Base):
    __tablename__ = 'playlists'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    link: Mapped[Optional[str]]
    playlist_name: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("bot_users.id"), nullable=False)
    reg_date: Mapped[datetime.datetime] = mapped_column(DATE, default=datetime.datetime.today())

    playlists: Mapped[List["Tracks"]] = relationship()

    def to_dict(self) -> dict:
        unit = PlaylistModel(
            id=self.id,
            link=self.link,
            playlist_name=self.playlist_name,
            user_id=self.user_id,
            reg_date=self.reg_date
        )
        return unit.model_dump(exclude_none=True)

class Tracks(Base):
    __tablename__ = 'tracks'

    id: Mapped[int] = mapped_column(primary_key=True)
    playlist_id: Mapped[int] = mapped_column(ForeignKey("playlists.id"))
    track_link: Mapped[str] = mapped_column(unique=False)
    track_tg_id: Mapped[str] = mapped_column(unique=False)
    track_thumbnail: Mapped[str] = mapped_column(unique=False)
    performer: Mapped[str] = mapped_column(unique=False)
    title: Mapped[str] = mapped_column(unique=False)
    reg_date: Mapped[datetime.datetime] = mapped_column(DATE, default=datetime.datetime.today())

    def to_dict(self) -> dict:
        unit = TrackModel(
            id=self.id,
            playlist_id=self.playlist_id,
            track_link=self.track_link,
            track_tg_id=self.track_tg_id,
            track_thumbnail=self.track_thumbnail,
            performer=self.performer,
            title=self.title,
            reg_date=self.reg_date
        )
        return unit.model_dump(exclude_none=True)
