from typing import Optional
from bot.misc import Request, back_request
from dataclasses import dataclass


@dataclass
class User:
    user_id: int
    status: str


class UserService:
    """User service for intercations
    
    CRUD-like"""


    @staticmethod
    async def create_user(user_id: int) -> Optional[bool]:
        """Create user by Telegram ID, return True or None.        
        Default user status is GUEST"""

        return await back_request(
            req=Request("post"),
            user_id=user_id,
            status="guest"
        )
    

    @staticmethod
    async def read_user(user_id: int) -> Optional[User]:
        """Enters a Telegram user ID,
        return a JSON with user data or None"""

        return await back_request(
            req=Request("get"),
            user_id=user_id
        )
    

    @staticmethod
    async def update_user(user_id: int, **kwargs) -> Optional[User]:
        """Enter user ID and update data,
        return User object or None"""

        return await back_request(
            req=Request("get"),
            user_id=user_id,
            **kwargs
        )
    
    @staticmethod
    async def delete_user(user_id: int) -> Optional[bool]:
        """Delete user by ID, return True or None"""

        return await back_request(
            req=Request("post"),
            user_id=user_id
        )