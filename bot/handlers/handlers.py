from aiogram import Router
from aiogram import F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message


user = Router()


@user.message(Command(commands=["track"]))
async def load_track(message: Message, command: CommandObject) -> None:
    '''Load track from link'''

    args = command.args
    if args:
        if args.startswith("https://www.youtube.com/watch?v="):
            pass # Implement sevice
        else:
            await message.reply("Invalid link")
    else:
        await message.reply("No arguments")


@user.message(Command(commands=["status"]))
async def user_status(message: Message):
    '''Send user status'''
    answer = "User status"# Implement User.service
    await message.reply(answer)