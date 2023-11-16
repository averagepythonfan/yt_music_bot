from pydantic import BaseModel


class UserModel(BaseModel):
    user_id: int
    user_name: str | None
    user_status: str | None


class PlaylistModel(BaseModel):
    playlist_id: int
    user_id: int
    link: str
