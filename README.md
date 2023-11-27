### Telegam YT Music Bot

This is simple Telegram bot that can help you save music from YouTube to Telegram.
You can load single videos and also playlists.

Main commands:
1. /track - load single track from video
2. /playlist - load playlist (unavailable)
3. /cut - cut single video on track by using timecodes (unavailable)

Main stack:
1. Telegram Bot - aiogram 3 + redis
2. FastAPI backend - FastAPI + sqlalchemy + yt_dlp + redis
3. Relative database - PostgreSQL