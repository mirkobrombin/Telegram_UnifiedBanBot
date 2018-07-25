<div align="center">
  <img src="https://i.imgur.com/zD9Q9sk.png" width="64">
  <h1 align="center">UnifiedBanBot</h1>
  <p align="center">This Telegram bot checks if new chat users are in blacklist and, with a positive result, blocks them.</p>
</div>

<br/>

### Attention, the source does not include updates of the last 4 releases.

<div align="center">
   <a href="https://gitlab.com/brombinmirko/Telegram_UnifiedBanBot/blob/master/LICENSE">
    <img src="https://img.shields.io/badge/License-GPL--3.0-blue.svg">
   </a>
</div>

## Problems/New Features?
Ask for support [here](https://gitlab.com/brombinmirko/Telegram_UnifiedBanBot/issues).

## Requirements
- python
- python-telegram-bot (https://python-telegram-bot.org/)

## Configuration
- Replace **bot_token** with your bot token
- Replace **channel_id** with private or public channel ID, this will be used for bot logs. Remember to add the bot as channel admin
- Replace **blacklist_repo** with your blacklist url (just an empty file)

## How to run
```bash
python bot.py
```