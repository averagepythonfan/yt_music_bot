### Telegam YT Music Bot

This is simple Telegram bot that can help you save music from YouTube to Telegram.
You can load single videos and also playlists.

Main commands:
1. /track - load single track from video
2. /playlist - load playlist (unavailable)
3. /cut - cut single video on track by using timecodes (unavailable)

Main stack:
1. Telegram Bot - aiogram 3 + redis
2. Backend - FastAPI + sqlalchemy + yt_dlp + celery
3. Relative database - PostgreSQL


## To run your own instance:
Pre-requirements: git, docker, docker compose, python 3.10, poetry, make

# Requirements:
- Firstly you need to clone repository:
```
~$: git clone https://github.com/averagepythonfan/yt_music_bot.git
```

- Then install poetry dev group, it install ansible on your computer:
```
~$: poetry install --only=dev
```

- Rename "inventory-example.ini" to "inventory.ini",
do it to "ansible-example.cfg" exactly the same.

- Edit "invetory.ini" and "ansible.cfg" with your own options.

- Then run command, that run ansible playbook script:
```
~$: ansible-playbook playbooks/dev.yml --tags="up"
```
OR
```
~$: ansible-playbook playbooks/prod.yml --tags="up"
```
