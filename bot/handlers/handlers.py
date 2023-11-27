from aiogram import Router
from aiogram import F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from bot.services import UserBotService, PlaylistBotService, TrackBotService
from bot.misc import help_message
from bot.schemas import UserModel, PlaylistModel


user = Router()


@user.message(Command(commands=["start", "help"]))
async def help_command(message: Message) -> None:
    """Help command for user"""

    user_instance = UserModel(
        id=message.from_user.id,
        username=message.from_user.username,
        status="guest"
    )

    if await UserBotService.create_user(user=user_instance):
        playlist_instance = PlaylistModel(
            playlist_name="other",
            user_id=message.from_user.id
        )

        await PlaylistBotService.create_playlist(
            pl=playlist_instance
        )

    await message.answer(help_message, parse_mode="HTML")


@user.message(Command(commands=["track"]))
async def load_track(message: Message, command: CommandObject) -> None:
    '''Load track from link'''

    args = command.args
    if args:
        if args.startswith("https://www.youtu"):
            await message.reply("Here we go! Please, wait")
            if await TrackBotService.upload_track(
                url=args,
                user_id=message.from_user.id
            ):
                pass
            else:
                await message.answer("Oops, something went wrong...")
        else:
            await message.reply(
                text="""Invalid link.
                Should start like <i>https://www.youtube.com/watch?v=</i>
                or <i>https://youtu.be/</i>""",
                parse_mode="HTML"
            )
    else:
        await message.reply("No arguments")


@user.message(Command(commands=["status"]))
async def user_status(message: Message) -> None:
    '''Send user status'''
    answer: UserModel = await UserBotService.read_user(user_id=message.from_user.id)
    if answer:
        await message.reply(f"<b>USER ID</b>: <i>{answer.id}</i>\nSTATUS: {answer.status}",
                            parse_mode="HTML")

