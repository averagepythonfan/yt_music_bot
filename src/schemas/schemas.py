import datetime
from pydantic import BaseModel
from typing import Optional


class UserModel(BaseModel):
    id: int
    username: Optional[str] = None
    status: Optional[str] = None
    reg_date: Optional[datetime.datetime] = None


class PlaylistModel(BaseModel):
    id: Optional[int] = None
    link: Optional[str] = None
    playlist_name: str
    user_id: int
    reg_date: Optional[datetime.datetime] = None


class TrackModel(BaseModel):
    id: Optional[int] = None
    playlist_id: int
    track_link: str
    track_tg_id: str
    track_thumbnail: Optional[str] = None
    performer: str
    title: str
    reg_date: Optional[datetime.datetime] = None


class SingleVid(BaseModel):
    user_id: int
    url: str