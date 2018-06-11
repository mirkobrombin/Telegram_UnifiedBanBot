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
import logging, urllib, json

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Config
bot_token = "000000000:0000000000000000000000000000000000"
channel_id = -1000000000000 # private channel for reports
blacklist_repo = "http://localhost/unifiedban_blacklist.json"

def error(bot, update, error):
    logger.warning('unifiedban/log: Update "%s" caused error "%s"', update, error)

def check_blacklist(bot, update):
  response=urllib.urlopen(blacklist_repo)
  data=json.loads(response.read())
  try:
    for new in update.message.new_chat_members:
      if new.id in data:
        bot.send_message(channel_id, "<b>unifiedban/report:</b> User "+str(new.username)+" with ID "+str(new.id)+" in BlackList, blocked from chat "+str(update.message.chat.title), parse_mode=ParseMode.HTML)
        bot.kick_chat_member(update.message.chat_id, new.id)
  except AttributeError:
    pass
    
def main():
    updater=Updater(bot_token)
    dp = updater.dispatcher
    dp.add_error_handler(error)
    dp.add_handler(MessageHandler(None, check_blacklist))
    updater.start_polling()
    updater.idle()

if __name__=='__main__':
    main()

