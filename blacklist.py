# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.error import TelegramError, Unauthorized, BadRequest,TimedOut, ChatMigrated, NetworkError
import logging, json, sys, MySQLdb
import config
import strings
import antispam
import util
from importlib import reload
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2


def check_in_blacklist(uid):
  db=MySQLdb.connect(config.database['server'],config.database['user'],config.database['password'],config.database['name'])
  db.autocommit(True)
  cur=db.cursor()
  cur.execute("SELECT User_ID FROM Blacklist WHERE User_ID="+str(uid)+" AND Whitelist = 0")
  row=cur.fetchone()
  if cur.rowcount:
    res=True
  else:
    res=False
  cur.close()
  db.close()
  return res

def check(bot, update):
  blacklist=False
  
  try:
    for new in update.message.new_chat_members:
      if check_in_blacklist(new.id):
        user=new
        blacklist=True
  except AttributeError:
    pass
  
  if check_in_blacklist(update.message.from_user.id):
    user=update.message.from_user
    blacklist=True
  
  if blacklist:
    if user.name is not None:
      user_name=user.name
    else:
      user_name=str(user.first_name)+" "+str(user.last_name)
    chat_id=update.message.chat_id
    util.bot_log(strings.BAN_REPORT % (str(user_name), str(user.id), str(update.message.chat.title), util.get_hash(int(chat_id))), bot)
    bot.kick_chat_member(update.message.chat_id, user.id)
    bot.delete_message(update.message.chat_id, update.message.message_id)
