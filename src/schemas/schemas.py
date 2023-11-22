import datetime
from pydantic import BaseModel
from typing import Optional


class UserModel(BaseModel):
    id: int
    username: Optional[str] = None
    status: Optional[str] = None
    reg_date: Optional[datetime.datetime] = None


class PlaylistModel(BaseModel):
    id: int
    link: Optional[str] = None
    playlist_name: str
    user_id: int
    reg_date: Optional[datetime.datetime] = None


class TrackModel(BaseModel):
    id: int
    playlist_id: Optional[int]
    track_link: str
    track_tg_id: str
    track_thumbnail: str
    performer: str
    title: str
    reg_date: Optional[datetime.datetime]