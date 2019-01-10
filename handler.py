# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.error import TelegramError, Unauthorized, BadRequest,TimedOut, ChatMigrated, NetworkError
import logging, urllib, json, sys, MySQLdb, html, time, threading
import config
import strings
import antispam
import blacklist
import util
import admin

reload(sys)  
sys.setdefaultencoding('utf8')
log_enabled=True

def check_verified_user(bot, update):
  if update.message is not None and update.message.new_chat_members is not None:
    for new in update.message.new_chat_members:
      if new.id in config.admin_id:
        if new.name is None:
          username=str(new.first_name)+" "+str(new.last_name)
        else:
          username=new.name
        bot.send_message(update.message.chat_id, (strings.VERIFIED_USER % username), parse_mode=ParseMode.HTML)

def register_group(bot, update):
  chat_id=update.message.chat_id
  db=MySQLdb.connect(config.database['server'],config.database['user'],config.database['password'],config.database['name'])
  db.autocommit(True)
  cur=db.cursor()
  cur.execute("INSERT INTO Groups (Title, Chat_ID) VALUES ('"+db.escape_string(str(update.message.chat.title))+"', '"+str(chat_id)+"')")
  bot.send_message(config.channel_id, (strings.REPORT_NEW_GROUP % (html.escape(str(update.message.chat.title)), str(chat_id), util.get_hash(int(chat_id)))), parse_mode=ParseMode.HTML)
  cur.close()
  db.close()

def check_registration(bot, update):
  db=MySQLdb.connect(config.database['server'],config.database['user'],config.database['password'],config.database['name'])
  db.autocommit(True)
  cur=db.cursor()
  cur.execute("SELECT ID FROM Groups WHERE Chat_ID='"+str(update.message.chat_id)+"'")
  row=cur.fetchone()
  if cur.rowcount:
    res=True
  else:
    register_group(bot, update)
    res=False
  cur.close()
  db.close()
  return res

@run_async
def check_operations(bot, update):
  starttime=time.time()
  while True:
    print("[Task] Checking..")
    db=MySQLdb.connect(config.database['server'],config.database['user'],config.database['password'],config.database['name'])
    db.autocommit(True)
    cur=db.cursor()
    cur.execute("SELECT * FROM Operations")
    for row in cur.fetchall():
      print(str("[Task] Found ID %s .." % row[0]))
      
      task = row[1]
      chat_id=row[2]
      cur.execute("DELETE FROM Operations WHERE ID = ("+str(row[0])+")")
      
      if task == '!sync':
        admin.sync(bot, update, True, chat_id)
      
      elif task == '!leave':
        admin.leave(bot, update, True, chat_id)
      
      elif task == '!disable':
        admin.disable(bot, update, True, chat_id)
      
      elif task == '!enable':
        admin.disable(bot, update, True, chat_id, True)
        
    cur.close()
    db.close()
    print("[Task] Sleeping..")
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))

def init(bot, update):
  check_operations(bot, update)
  global log_enabled
  if config.debug:
    util.debug(update)
  
  if update.message is not None and update.message.chat.type in ["supergroup", "group"]:
    
    for new in update.message.new_chat_members:
      if new.name == config.bot_username:
        check_registration(bot, update)
    
    db=MySQLdb.connect(config.database['server'],config.database['user'],config.database['password'],config.database['name'])
    db.autocommit(True)
    cur=db.cursor()
    cur.execute("SELECT * FROM Groups WHERE Chat_ID = '"+str(update.message.chat_id)+"'")
    row=cur.fetchone()
    
    check_verified_user(bot, update)
    
    if row[3] == 1:
      if row[4] == 1: #ConfLog
        log_enabled=False
      if row[5] == 1: #ConfSpamWords
        antispam.message_text(bot, update)
      if row[11] == 1: #ConfSpamNonWest
        antispam.text_lang(bot, update)
      if row[6] == 1: #ConfSpamUsername
        antispam.message_entities(bot, update)
        antispam.message_links(bot, update)
      if row[7] == 1: #ConfSpamUser
        antispam.new_user_name(bot, update)
      if row[8] == 1: #ConfScam
        pass
      if row[9] == 1: #ConfBlacklist
        blacklist.check(bot, update)
      if row[10] == 1: #ConfHammer
        antispam.text_lang(bot, update)
    else:
      admin.leave(bot, update, True)
    
    cur.close()
    db.close()
  else:
    admin.leave(bot, update, True)
