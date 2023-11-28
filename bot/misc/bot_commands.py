from aiogram import types


bot_commands = (
    ('track', 'load one track from vid'),
    ("playlist", "load YT playlist (unavailable)"),
    ('status', 'user status'),
    ('help', 'help command'),
    ('cut', "cut one vid with timings (unavailable)"),
)


commands_for_bot = []
for cmd in bot_commands:
    commands_for_bot.append(
        types.BotCommand(command=cmd[0], description=cmd[1])
    )