#!/usr/bin/env python
'''
  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

# -*- coding: utf-8 -*-  
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.error import TelegramError, Unauthorized, BadRequest,TimedOut, ChatMigrated, NetworkError
import logging, urllib, json

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Config
bot_token = "000000000:0000000000000000000000000000000000"
channel_id = -1000000000000 # private channel for reports
blacklist_repo = "http://localhost/unifiedban_blacklist.json"
admin_id = [
  10000000
]

# Strings
UNIFIEDBANREPORT_PREFIX = "<b>unifiedban/report:</b> "
SYNCING_BLACKLIST = "<i>[Sto sincronizzando la chat con la Blacklist..]</i>"
SYNC_COMPLETE = "<b>[Chat sincronizzata con la Blacklist!]</b>"
BAN_REPORT = UNIFIEDBANREPORT_PREFIX+"Utente %s con ID %s presente nella Blacklist, rimosso dalla chat %s."
SYNC_REPORT = UNIFIEDBANREPORT_PREFIX+"Chat %s sincronizzata con la Blacklist, aggiunti %s user_id"

def error(bot, update, error):
    logger.warning('unifiedban/log: Update "%s" --- ha causato un errore --- "%s"', update, error)
    
def sync_with_blacklist(bot, update):
  if update.message.from_user.id in admin_id:
    bot.send_message(update.message.chat_id, SYNCING_BLACKLIST, parse_mode=ParseMode.HTML)
    response=urllib.urlopen(blacklist_repo)
    data=json.loads(response.read())
    counter=0
    for user in data:
      try:
        print("Blocking "+str(user))
        bot.kick_chat_member(update.message.chat_id, user)
        print("Success!")
        counter+=1
      except TelegramError:
        print("Fail!")
    bot.send_message(update.message.chat_id, SYNC_COMPLETE, parse_mode=ParseMode.HTML)
    bot.send_message(channel_id, (SYNC_REPORT % (str(update.message.chat.title), counter)), parse_mode=ParseMode.HTML)
    bot.delete_message(update.message.chat_id, update.message.message_id)

def check_blacklist(bot, update):
  response=urllib.urlopen(blacklist_repo)
  data=json.loads(response.read())
  try:
    for new in update.message.new_chat_members:
      if new.id in data:
        bot.send_message(channel_id, (BAN_REPORT % (str(new.username), str(new.id), str(update.message.chat.title))), parse_mode=ParseMode.HTML)
        bot.kick_chat_member(update.message.chat_id, new.id)
  except AttributeError:
    pass

def main():
    updater=Updater(bot_token)
    dp = updater.dispatcher
    dp.add_error_handler(error)
    dp.add_handler(CommandHandler("sync", sync_with_blacklist))
    dp.add_handler(MessageHandler(None, check_blacklist))
    updater.start_polling()
    updater.idle()

if __name__=='__main__':
    main()
