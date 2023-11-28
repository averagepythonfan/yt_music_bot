from aiogram import Router, F
from bot.filters import AdminFilter
from aiogram.types import Message, Audio, PhotoSize
from aiogram.methods import SendAudio
from aiogram.filters import Command, CommandObject
from bot.services import TrackBotService


admin = Router()


# failed
@admin.message(AdminFilter(), F.photo)
async def change_pic(message: Message):
    if msg := message.reply_to_message:
        audio = isinstance(msg.audio, Audio)
        pic = isinstance(message.photo[1], PhotoSize)
        if audio and pic:
            result: SendAudio = await message.answer_audio(
                audio=msg.audio.file_id,
                performer=msg.audio.performer,
                title=msg.audio.title,
                thumbnail=message.photo[1].file_id
            )
            # print(result)
        else:
            await message.reply("Please select audio, and reply a pucture")
    else:
        await message.reply("There is not reply message. Please select")


@admin.message(AdminFilter(), Command(commands=["change"]))
async def chencge_status(message: Message, command: CommandObject):
    if command.args:
        await message.reply("User interface change user's status")
        await message.reply("Success")
    else:
        await message.reply("There is not args")


@admin.message(AdminFilter(), Command(commands=["check"]))
async def check_title(message: Message, command: CommandObject):
    if args := command.args:
        data = await TrackBotService.check_title(url=args)
        await message.answer_photo(
            photo=data["pic"],
            caption=f"Title: {data['title']}\nChannel: {data['chennel']}"
        )