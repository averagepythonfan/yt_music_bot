from pydantic import BaseModel
from typing import Optional


class UserModel(BaseModel):
    user_id: int
    user_name: Optional[str]
    user_status: Optional[str]


class PlaylistModel(BaseModel):
    playlist_id: Optional[int]
    link: Optional[str]
    playlist_name: str
    user_id: int
