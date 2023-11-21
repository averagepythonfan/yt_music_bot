import datetime
from typing import Optional, List
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import DATE, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "bot_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(5), default='guest')
    reg_date: Mapped[datetime.datetime] = mapped_column(DATE, default=datetime.datetime.today())

    playlists: Mapped[List["Playlists"]] = relationship()


class Playlists(Base):
    __tablename__ = 'playlists'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    link: Mapped[Optional[str]]
    playlist_name: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("bot_users.id"), nullable=False)
    reg_date: Mapped[datetime.datetime] = mapped_column(DATE, default=datetime.datetime.today())

    playlists: Mapped[List["Tracks"]] = relationship()

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
