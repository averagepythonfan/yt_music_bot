from aiogram import types


bot_commands = (
    ('track', 'load one track from vid'),
    ("playlist", "load YT playlist"),
    ('status', 'user status'),
    ('cut', "cut one vid with timings"),
)


commands_for_bot = []
for cmd in bot_commands:
    commands_for_bot.append(
        types.BotCommand(command=cmd[0], description=cmd[1])
    )