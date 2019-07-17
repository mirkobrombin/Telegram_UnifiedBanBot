# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.error import TelegramError, Unauthorized, BadRequest,TimedOut, ChatMigrated, NetworkError
import logging, json, sys, re, MySQLdb, html
from requests import get, post, exceptions
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import config
import strings
import antispam
from handler import log_enabled
from importlib import reload

def get_hash(chat_id):
  if chat_id < 0:
    chat_id=str(chat_id)[1:]
  return "UB"+str(chat_id)

def bot_log(text, bot):
  if log_enabled:
    bot.send_message(config.channel_id, text, parse_mode=ParseMode.HTML)

def log_operation(flag, chat_id, user_id):
  if log_enabled:
    db=MySQLdb.connect(config.database['server'],config.database['user'],config.database['password'],config.database['name'])
    db.autocommit(True)
    cur=db.cursor()
    cur.execute("INSERT INTO ChatOperationsLog (Flag, Chat_ID, User_ID) VALUES ('"+flag+"', (SELECT ID FROM Groups WHERE Chat_ID = "+str(chat_id)+"), "+str(user_id)+")")
    cur.close()
    db.close()

# use this for dashboard stats
def log_blocked_content(flag, chat_id, user_id, status):
  if log_enabled:
    if status:
       status = 1
    db=MySQLdb.connect(config.database['server'],config.database['user'],config.database['password'],config.database['name'])
    db.autocommit(True)
    cur=db.cursor()
    cur.execute("INSERT INTO BlockedContent (Flag, Chat_ID, User_ID, Status) VALUES ('"+flag+"', (SELECT ID FROM Groups WHERE Chat_ID = "+str(chat_id)+"), "+str(user_id)+", "+status+")")
    cur.close()
    db.close()

def build_menu(buttons, n_cols, header_buttons=False, footer_buttons=False):
  menu=[buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
  if header_buttons:
    menu.insert(0, header_buttons)
  if footer_buttons:
    menu.append(footer_buttons)
  return menu

def debug(update):
  if update.message is not None and update.message.text is not None:
    data=""
    chat_name=str(update.message.chat.title) 
    chat_id=str(update.message.chat_id) 
    chat_user=str(update.message.chat.username) 
    author_id=str(update.message.from_user.id) 
    author_user=str(update.message.from_user.name) 
    author_name=str(update.message.from_user.first_name)+" "+str(update.message.from_user.last_name) 
    post_text=str(update.message.text)
    print(strings.DEBUG_UPDATE % (chat_name, chat_id, chat_user, author_id, author_user, author_name, post_text))
