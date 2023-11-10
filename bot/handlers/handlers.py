from aiogram import Router
from aiogram import F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from bot.services import UserService
from bot.misc import help_message


user = Router()


@user.message(Command(commands=["start", "help"]))
async def help_command(message: Message) -> None:
    """Help command for user"""

    await message.answer(help_message, parse_mode="HTML")


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
async def user_status(message: Message) -> None:
    '''Send user status'''
    answer = await UserService.read_user(user_id=message.from_user.id)# Implement User.service
    await message.reply(answer)