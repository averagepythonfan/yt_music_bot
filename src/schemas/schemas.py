from pydantic import BaseModel
from typing import Optional


class UserModel(BaseModel):
    user_id: int
    user_name: Optional[str]
    user_status: Optional[str]


class PlaylistModel(BaseModel):
    playlist_id: int
    user_id: int
    link: str
