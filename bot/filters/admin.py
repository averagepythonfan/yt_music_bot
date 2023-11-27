from typing import Any
from aiogram.filters import BaseFilter
from aiogram.types import Message
from bot.config import ADMIN


class AdminFilter(BaseFilter):
    """Check if message from admin"""

    def __init__(self) -> None:
        self.admin_id = int(ADMIN)


    async def __call__(self, message: Message) -> Any:
        return message.from_user.id == self.admin_id
