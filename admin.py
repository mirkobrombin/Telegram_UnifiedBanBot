# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.error import TelegramError, Unauthorized, BadRequest,TimedOut, ChatMigrated, NetworkError
import logging, urllib, json, sys, re, html, unicodedata, MySQLdb, time
from requests import get, post, exceptions
import config
import strings
import antispam
import util
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
from importlib import reload


def help_message(bot, update):
  if update.message.from_user.id in config.admin_id or bot.get_chat_member(update.message.chat_id, 
                                                                                   update.message.from_user.id).status in ["creator", "administrator"]:
    
    bot.send_message(update.message.chat_id, strings.HELP_MESSAGE, parse_mode=ParseMode.HTML)
    bot.delete_message(update.message.chat_id, update.message.message_id)

def restart(bot, update):
  if update.message.from_user.id in config.super_admin_id:
    bot.send_message(update.message.chat_id, strings.RESTART, parse_mode=ParseMode.HTML)

def safenames(bot, update):
  if update.message.from_user.id in config.admin_id or bot.get_chat_member(update.message.chat_id, 
                                                                                   update.message.from_user.id).status in ["creator", "administrator"]:
    chat_id = update.message.chat_id
    db=MySQLdb.connect(config.database['server'],config.database['user'],config.database['password'],config.database['name'])
    db.autocommit(True)
    cur=db.cursor()
    cur.execute("SELECT * FROM SafeNames WHERE Chat_ID = '"+str(chat_id)+"'")
    sns=""
    for row in cur.fetchall():
      sns=sns+"- @"+str(row[1])+"\n"
    bot.send_message(chat_id, (strings.LIST_SAFENAMES % sns), parse_mode=ParseMode.HTML)
    cur.close()
    db.close()
    util.log_operation('!safenames', chat_id, update.message.from_user.id)

def safe(bot, update, remove=False):
  if update.message.from_user.id in config.admin_id or bot.get_chat_member(update.message.chat_id, 
                                                                                   update.message.from_user.id).status in ["creator", "administrator"]:
    if remove == False:
      word=update.message.text[6:]
    else:
      word=update.message.text[8:]
    if word.startswith("@"):
      if antispam.is_spam(word, False, False, True):
        word=word[1:]
        if " " in word:
          bot.send_message(update.message.chat_id, strings.INVALID_SAFENAME, parse_mode=ParseMode.HTML)
        else:
          db=MySQLdb.connect(config.database['server'],config.database['user'],config.database['password'],config.database['name'])
          db.autocommit(True)
          cur=db.cursor()
          if remove == False:
            cur.execute("INSERT IGNORE INTO SafeNames (Name, Chat_ID) VALUES ('"+str(word)+"', '"+str(update.message.chat_id)+"')")
            u=bot.send_message(update.message.chat_id, (strings.SAFE_NAME_SAVED % (html.escape(str("@"+word)))), parse_mode=ParseMode.HTML)
            util.log_operation('!addsafename:'+str(word), update.message.chat_id, update.message.from_user.id)
          else:
            cur.execute("DELETE FROM SafeNames WHERE Name = '"+str(word)+"' AND Chat_ID = '"+str(update.message.chat_id)+"'")
            u=bot.send_message(update.message.chat_id, (strings.SAFE_NAME_REMOVED % (html.escape(str("@"+word)))), parse_mode=ParseMode.HTML)
            util.log_operation('!removesafename:'+str(word), update.message.chat_id, update.message.from_user.id)
          bot.delete_message(update.message.chat_id, update.message.message_id)
          time.sleep(5)
          bot.delete_message(update.message.chat_id, u.message_id)
          cur.close()
          db.close()
      else:
        bot.send_message(update.message.chat_id, strings.INVALID_SAFENAME, parse_mode=ParseMode.HTML)
    else:
      bot.send_message(update.message.chat_id, strings.INVALID_SAFENAME, parse_mode=ParseMode.HTML)

def unsafe(bot, update):
  safe(bot, update, True)

def ban(bot, update, unban=False):
  if update.message.from_user.id in config.admin_id or bot.get_chat_member(update.message.chat_id, 
                                                                                   update.message.from_user.id).status in ["creator", "administrator"]:
    if update.message.reply_to_message:
      user_id=update.message.reply_to_message.from_user.id
      if update.message.reply_to_message.from_user.name is not None:
        user_name=update.message.reply_to_message.from_user.name
      else:
        user_name=str(update.message.reply_to_message.from_user.first_name)+" "+str(update.message.reply_to_message.from_user.last_name)
      chat_id=update.message.chat_id
      if unban == False:
        if user_id != config.bot_id:
          bot.send_message(config.channel_id, (strings.REPORT_USER_BAN % (str(update.message.from_user.name),  
                                                                                 str(user_name),
                                                                                 str(user_id),
                                                                                 str(update.message.chat.title),
                                                                                 util.get_hash(int(chat_id)))), parse_mode=ParseMode.HTML)
          bot.kick_chat_member(update.message.chat_id, user_id)
          bot.send_message(update.message.chat_id, (strings.USER_BAN % str(user_name)), 
                         parse_mode=ParseMode.HTML)
          util.log_operation('!ban:'+str(user_id), chat_id, update.message.from_user.id)
      else:
        bot.send_message(CONF_.channel_id, (strings.REPORT_USER_UNBAN % (str(update.message.from_user.name), 
                                                                               str(update.message.chat.title), 
                                                                               str(user_name),
                                                                               str(user_id),
                                                                               util.get_hash(int(chat_id)))), parse_mode=ParseMode.HTML)
        bot.unban_chat_member(update.messCONF_age.chat_id, int(user_id))
        bot.send_message(update.message.chat_id, (strings.USER_UNBAN % str(user_name)), 
                         parse_mode=ParseMode.HTML)
        util.log_operation('!unban:'+str(user_id), chat_id, update.message.from_user.id)
  bot.delete_message(update.message.chat_id, update.message.message_id)

def unban(bot, update):
  ban(bot, update, True)

def delete(bot, update):
  if update.message.from_user.id in config.admin_id or bot.get_chat_member(update.message.chat_id, 
                                                                                   update.message.from_user.id).status in ["creator", "administrator"]:
    if update.message.reply_to_message:
      user_id=update.message.reply_to_message.from_user.id
      user_name=update.message.reply_to_message.from_user.name
      text=update.message.reply_to_message.text
      chat_id=update.message.chat_id
      if user_id != config.bot_id:
        bot.send_message(config.channel_id, (strings.REPORT_DELETED_MESSAGE % (str(update.message.from_user.name), 
                                                                        str(update.message.chat.title), 
                                                                        str(text),
                                                                        util.get_hash(int(chat_id)))), parse_mode=ParseMode.HTML)
  bot.delete_message(update.message.chat_id, update.message.reply_to_message.message_id)
  bot.delete_message(update.message.chat_id, update.message.message_id)
  util.log_operation('!rm:'+str(update.message.reply_to_message.message_id), chat_id, update.message.from_user.id)

def add_to_blacklist(bot, update, remove=False):
  if update.message.from_user.id in config.admin_id:
    chat_id=update.message.chat_id
    if update.message.reply_to_message:
      user_id=update.message.reply_to_message.from_user.id
      if int(user_id) in config.admin_id:
        return False
      if update.message.reply_to_message.from_user.name is not None:
        user_name=update.message.reply_to_message.from_user.name
      else:
        user_name=str(update.message.reply_to_message.from_user.first_name)+" "+str(update.message.reply_to_message.from_user.last_name)
      bot.send_message(update.message.chat_id, (strings.USER_BLACKLIST % str(user_name)), 
                       parse_mode=ParseMode.HTML)
    else:
      user_id = update.message.text[7:]
      if int(user_id) in config.admin_id:
        return False
      user_name = user_id
  
  db=MySQLdb.connect(config.database['server'],config.database['user'],config.database['password'],config.database['name'])
  db.autocommit(True)
  cur=db.cursor()
  
  if remove == False:
    try:
      cur.execute("INSERT INTO Blacklist (User_ID, Chat_ID) VALUES ("+str(user_id)+", '"+str(chat_id)+"')")
      try:
        bot.kick_chat_member(update.message.chat_id, user_id)
      except TelegramError:
        pass
      bot.send_message(config.channel_id, (strings.REPORT_NEW_USER_IN_BLACKLIST % (str(update.message.from_user.name), 
                                                                                 str(user_name), 
                                                                                 str(update.message.chat.title),
                                                                                 util.get_hash(int(chat_id)))), parse_mode=ParseMode.HTML)
    except MySQLdb.IntegrityError:
      bot.send_message(update.message.chat_id, (strings.USER_ALREADY_IN_BLACKLIST % str(user_name)))
  else:
    try:
      cur.execute("DELETE FROM Blacklist WHERE User_ID = ("+str(user_id)+")")
      try:
        bot.unban_chat_member(update.message.chat_id, int(user_id))
      except TelegramError:
        pass
      bot.send_message(config.channel_id, (strings.REPORT_REMOVED_FROM_BLACKLIST % (str(update.message.from_user.name), 
                                                                                    str(user_name), 
                                                                                    str(update.message.chat.title),
                                                                                    util.get_hash(int(chat_id)))), parse_mode=ParseMode.HTML)
    except MySQLdb.IntegrityError:
      bot.send_message(update.message.chat_id, (strings.USER_NOT_IN_BLACKLIST % str(user_name)))
  cur.close()
  db.close()
  bot.delete_message(update.message.chat_id, update.message.message_id)

def remove_from_blacklist(bot, update):
  if update.message.from_user.id in config.super_admin_id:
    add_to_blacklist(bot, update, True)

@run_async
def sync_async(bot, update, trigger=False, chat_id=False):
  sync(bot, update, trigger, chat_id)

def sync(bot, update, trigger=False, chat_id=False):
  # Check for admin or trigger
  # if no trigger, get chat_id from update
  if update.message.from_user.id in config.admin_id or trigger:
    if trigger:
      sync_message = strings.DASH_SYNCING_BLACKLIST
    else:
      sync_message = strings.SYNCING_BLACKLIST
      chat_id=update.message.chat_id
      
    # send the operation message to the chat and save update for edit
    u=bot.send_message(chat_id, sync_message, 
                       parse_mode=ParseMode.HTML, 
                       disable_web_page_preview=True)
    
    # delete the request message if no trigger
    if trigger == False:
      try:
        bot.delete_message(chat_id, update.message.message_id)
      except TelegramError:
        pass
      
    # get the blacklist and set a counter to 0
    db=MySQLdb.connect(config.database['server'],config.database['user'],config.database['password'],config.database['name'])
    db.autocommit(True)
    cur=db.cursor()
    cur.execute("SELECT User_ID FROM Blacklist")
    counter=0
    
    # for each blacklist item, try to block or fail, wait 1.5s every 10 operations
    # then increase counter by one
    for row in cur.fetchall():
      counter+=1
      if counter % 10 == 0:
        time.sleep(0)
      try:
        print("Blocking "+str(row[0]))
        bot.kick_chat_member(chat_id, row[0])
        print("Success!")
      except TelegramError:
        print("Fail!")
    cur.close()
    db.close()
    
    # edit the operation message with result
    bot.edit_message_text(text=(strings.SYNC_COMPLETE % str(counter)), 
                          chat_id=u.chat_id, 
                          message_id=u.message_id, 
                          parse_mode=ParseMode.HTML, 
                          disable_web_page_preview=True)
    
    # send a log message to the report channel
    bot.send_message(config.channel_id, (strings.SYNC_REPORT % (str(u.chat.title), counter, util.get_hash(int(chat_id)))), 
                     parse_mode=ParseMode.HTML)

def check_permissions(bot, update):
  if update.message.from_user.id in config.admin_id or bot.get_chat_member(update.message.chat_id, 
                                                                           update.message.from_user.id).status in ["creator", "administrator"]:
    chat_id = update.message.chat_id
    prm=bot.getChatMember(chat_id, config.bot_id)
    if prm.can_delete_messages == False or prm.can_restrict_members == False:
      rs="\n"+strings.BOT_PERMISSIONS_NO
    else:
      rs="\n"+strings.BOT_PERMISSIONS_OK
    bot.send_message(chat_id, (strings.BOT_PERMISSIONS % (str(prm.can_delete_messages), str(prm.can_restrict_members)))+rs, 
                              parse_mode=ParseMode.HTML, 
                              disable_web_page_preview=True)
    util.log_operation('!check', chat_id, update.message.from_user.id)

def leave(bot, update, force=False, chat_id=False):
  if chat_id == False:
    if update.message is None:
      if update.channel_post is not None:
        chat_id=update.channel_post.chat_id
        chat_title=update.channel_post.chat.title
      f=0
    else:
      chat_id=update.message.chat_id
      chat_title=update.message.chat.title
      f=update.message.from_user.id
  else:
    f=0
    chat_title=str(chat_id)
  if f in config.admin_id or force:
    if chat_id != config.channel_id:
      bot.send_message(chat_id, strings.LEAVING)
      bot.leaveChat(chat_id)
      bot.send_message(config.channel_id, (strings.REPORT_BOT_REMOVED % (html.escape(str(chat_title)), 
                                                                         str(chat_id), 
                                                                         str(update.message.chat.type),
                                                                         util.get_hash(int(chat_id)))), parse_mode=ParseMode.HTML)
  
def get_data(bot, update):
  if update.message.from_user.id in config.admin_id:
    chat_id=update.message.chat_id
    if update.message.reply_to_message:
      reply=update.message.reply_to_message
      if reply.forward_from:
        if reply.forward_from.language_code is None:
          lang='en_US'
        else:
          lang=str(reply.forward_from.language_code)
        bot.send_message(config.channel_id, (strings.REPORT_MESSAGE_FORWARD_INFO % (update.message.from_user.name, 
                                                                                    reply.forward_from.username, 
                                                                                    reply.forward_from.first_name, 
                                                                                    reply.forward_from.last_name, 
                                                                                    reply.forward_from.id, lang,
                                                                                    util.get_hash(int(chat_id)),
                                                                                    str(reply.forward_from.is_bot))), parse_mode=ParseMode.HTML)
      else:
        if reply.from_user.language_code is None:
          lang='en_US'
        else:
          lang=str(reply.from_user.language_code)
        bot.send_message(config.channel_id, (strings.REPORT_MESSAGE_INFO % (update.message.from_user.name, 
                                                                            str(reply.message_id), 
                                                                            reply.from_user.name, 
                                                                            reply.from_user.first_name, 
                                                                            reply.from_user.last_name, 
                                                                            reply.from_user.id, lang, 
                                                                            str(reply.from_user.is_bot),
                                                                            util.get_hash(int(chat_id)))), parse_mode=ParseMode.HTML)
    else:
      bot.send_message(config.channel_id, (strings.REPORT_CHAT_INFO % (update.message.from_user.name, 
                                                                       str(update.message.chat.username), 
                                                                       str(update.message.chat.title), 
                                                                       update.message.chat_id, 
                                                                       update.message.chat.type,
                                                                       util.get_hash(int(chat_id)))), parse_mode=ParseMode.HTML)
    bot.delete_message(update.message.chat_id, update.message.message_id)
    
def list_groups(bot, update):
  if update.message.from_user.id in config.admin_id:
    db=MySQLdb.connect(config.database['server'],config.database['user'],config.database['password'],config.database['name'])
    db.autocommit(True)
    cur=db.cursor()
    cur.execute("SELECT * FROM Groups ORDER BY ID DESC, Status")
    groups=""
    for row in cur.fetchall():
      if row[3] == 1:
        status=" [Enabled]"
      else:
        status=" [Disabled]"
      groups=groups+"- ID: "+str(row[0])+" Chat_ID: <code>"+str(row[2])+"</code>"+status+"\n\n"
    update.message.reply_text(str(groups), parse_mode=ParseMode.HTML)
    cur.close()
    db.close()

def configure(bot, update, edit=False):
  if update.message.from_user.id in config.admin_id or edit or bot.get_chat_member(update.message.chat_id, 
                                                                                   update.message.from_user.id).status in ["creator", "administrator"]:
    btns=[]
    db=MySQLdb.connect(config.database['server'],config.database['user'],config.database['password'],config.database['name'])
    db.autocommit(True)
    cur=db.cursor()
    cur.execute("SELECT * FROM Groups WHERE Chat_ID = '"+str(update.message.chat_id)+"'")
    row=cur.fetchone()
    btns.append(InlineKeyboardButton((strings.CONF_ANTISPAM_WORDS % ("On" if row[5] == 1 else "Off")), callback_data='conf_spam_words'))
    btns.append(InlineKeyboardButton((strings.CONF_ANTISPAM_NON_WEST % ("On" if row[11] == 1 else "Off")), callback_data='conf_spam_non_west'))
    btns.append(InlineKeyboardButton((strings.CONF_ANTISPAM_USERNAME % ("On" if row[6] == 1 else "Off")), callback_data='conf_spam_username'))
    btns.append(InlineKeyboardButton((strings.CONF_ANTISPAM_USER % ("On" if row[7] == 1 else "Off")), callback_data='conf_spam_user'))
    btns.append(InlineKeyboardButton((strings.CONF_ANTISCAM % ("On" if row[8] == 1 else "Off")), callback_data='conf_scam'))
    btns.append(InlineKeyboardButton((strings.CONF_BLACKLIST % ("On" if row[9] == 1 else "Off")), callback_data='conf_blacklist'))
    btns.append(InlineKeyboardButton((strings.CONF_HAMMER % ("Open" if row[10] == 1 else "Close")), callback_data='conf_hammer'))
    if update.message.from_user.id in config.super_admin_id:
      btns.append(InlineKeyboardButton(strings.CONF_LEAVE, callback_data='conf_leave'))
    btns.append(InlineKeyboardButton(strings.CONF_CLOSE_MENU, callback_data='conf_close_menu'))
    reply_markup = InlineKeyboardMarkup(util.build_menu(btns, n_cols=1))
    if edit:
      aid=re.search('{{(.*)}}', update.message.text).group(1)
      bot.edit_message_text((strings.CONF_MENU_HEADER % aid), 
                            reply_markup=reply_markup, 
                            parse_mode=ParseMode.HTML, 
                            chat_id=update.message.chat_id, 
                            message_id=update.message.message_id)
    else:
      bot.send_message(update.message.chat_id, (strings.CONF_MENU_HEADER % str(update.message.from_user.id)), 
                       reply_markup=reply_markup, 
                       parse_mode=ParseMode.HTML)
    cur.close()
    db.close()

def disable(bot, update, force=False, chat_id=False, enable=False):
  if update.message is not None:
    if chat_id == False:
      chat_id = update.message.chat_id
    if enable == False:
      scope = 2;
    else:
      scope = 1;
    db=MySQLdb.connect(config.database['server'],config.database['user'],config.database['password'],config.database['name'])
    db.autocommit(True)
    cur=db.cursor()
    cur.execute("UPDATE Groups SET Status = "+str(scope)+" WHERE Chat_ID = '"+str(chat_id)+"'")
    cur.close()
    db.close()

def configure_edit(bot, update):
  query = update.callback_query
  aid = re.search('{{(.*)}}', query.message.text).group(1)
  if str(aid) == str(query.from_user.id):
    print("SI")
    if query.data == 'conf_spam_words':
      col="ConfOffensive"
    elif query.data == 'conf_spam_non_west':
      col="ConfNonWest"
    elif query.data == 'conf_spam_username':
      col="ConfTelegram"
    elif query.data == 'conf_spam_user':
      col="ConfName"
    elif query.data == 'conf_scam':
      col="ConfAntiscam"
    elif query.data == 'conf_blacklist':
      col="ConfBlacklist"
    elif query.data == 'conf_hammer':
      col="ConfHammer"
    elif query.data == 'conf_leave':
      leave(bot, query, True)
    elif query.data == 'conf_close_menu':
      bot.edit_message_text(strings.CONF_MENU_CLOSED, 
                            parse_mode=ParseMode.HTML, 
                            chat_id=query.message.chat_id, 
                            message_id=query.message.message_id)
      if update.message is not None:
        bot.delete_message(query.message.chat_id, query.message.reply_to_message.message_id)
      return False
    util.log_operation('!conf:'+col, query.message.chat_id, aid)
    db=MySQLdb.connect(config.database['server'],config.database['user'],config.database['password'],config.database['name'])
    db.autocommit(True)
    cur=db.cursor()
    cur.execute("UPDATE Groups SET "+col+" = IF("+col+" = 0, 1, 0) WHERE Chat_ID = '"+str(query.message.chat_id)+"'")
    cur.close()
    db.close()
    configure(bot, query, True)

def sign(bot, update):
  if update.message.from_user.id in config.admin_id or bot.get_chat_member(update.message.chat_id, 
                                                                                   update.message.from_user.id).status in ["creator", "administrator"]:
    if update.message.from_user.name is not None:
      user_name=update.message.from_user.name
    else:
      user_name=str(update.message.from_user.first_name)+" "+str(update.message.from_user.last_name)
    db=MySQLdb.connect(config.database['server'],config.database['user'],config.database['password'],config.database['name'])
    db.autocommit(True)
    cur=db.cursor()
    cur.execute("INSERT IGNORE INTO Permissions (User_ID, Group_ID) VALUES ("+str(update.message.from_user.id)+", (SELECT ID FROM Groups WHERE Chat_ID = '"+str(update.message.chat_id)+"'))")
    bot.delete_message(update.message.chat_id, update.message.message_id)
    cur.close()
    db.close()
    
    util.bot_log(strings.DASH_USER_SIGN % (str(user_name), str(update.message.from_user.id), str(update.message.chat.title), str(update.message.chat_id), util.get_hash(int(update.message.chat_id))), bot)
