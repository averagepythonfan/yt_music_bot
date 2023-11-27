import asyncio
import logging
from redis.asyncio.client import Redis
from aiogram import Dispatcher, Bot
from bot.config import TOKEN, REDIS_HOST, REDIS_PASSWORD
from bot.handlers import user, admin
from bot.misc import commands_for_bot
from aiogram.fsm.storage.redis import RedisStorage


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    redis = Redis(host=REDIS_HOST, password=REDIS_PASSWORD)
    storage = RedisStorage(redis=redis)

    dp = Dispatcher(storage=storage)
    bot = Bot(token=TOKEN)

    dp.include_router(router=user)
    dp.include_router(router=admin)
    await bot.set_my_commands(commands=commands_for_bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main=main())