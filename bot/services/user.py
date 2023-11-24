from typing import Optional
from bot.misc import Request, back_request
from dataclasses import dataclass
from bot.config import BACKEND
from bot.schemas import UserModel


@dataclass
class User:
    user_id: int
    status: str


class UserBotService:
    """User service for intercations
    
    CRUD-like"""


    @staticmethod
    async def create_user(user: UserModel) -> Optional[bool]:
        """Create user by Telegram ID, return True or None.        
        Default user status is GUEST"""

        return await back_request(
            req=Request("post"),
            url=f"http://{BACKEND}:9090/user/",
            params=user.model_dump(exclude_none=True)
        )
    

    @staticmethod
    async def read_user(user_id: int) -> Optional[UserModel]:
        """Accept a Telegram user ID,
        return a pydantic UserModel or `None`"""

        user = await back_request(
            req=Request("get"),
            url=f"http://{BACKEND}:9090/user/{user_id}"
        )
        if user:
            return UserModel.model_validate(user["result"][0])


    @staticmethod
    async def update_user(user_id: int, params: dict) -> Optional[UserModel]:
        """Enter user ID and update data,
        return User object or None"""

        return await back_request(
            req=Request("get"),
            user_id=user_id,
            params=params
        )
    
    @staticmethod
    async def delete_user(user_id: int) -> Optional[bool]:
        """Delete user by ID, return True or None"""

        return await back_request(
            req=Request("post"),
            user_id=user_id
        )