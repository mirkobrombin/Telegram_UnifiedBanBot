# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.error import TelegramError, Unauthorized, BadRequest,TimedOut, ChatMigrated, NetworkError
import logging, urllib, json, sys, re, html, urllib2, unicodedata, MySQLdb
from requests import get, post, exceptions
import config
import strings
import antispam
import util

reload(sys)  
sys.setdefaultencoding('utf8')
no_spam = dict()

mix_spam_list = config.spam_words+config.telegram_domains
latin_letters = {}
  
def is_latin(t):
  if t not in config.allowed_words:
    try: 
      return latin_letters[t]
    except KeyError:
      return latin_letters.setdefault(t, 'LATIN' in unicodedata.name(t))
  else:
    return True

def text_lang(bot, update):
  try:
    if update.message is not None:
      text=""
      if update.message.text is None:
        if update.message.forward_from_chat:
          text = update.message.caption
      else:
        text=update.message.text
      if update.message.chat.username is not None:
        chat_name = update.message.chat.username
      else:
        chat_name = update.message.chat.title
      if all(is_latin(t) for t in text if t.isalpha()) == False:
        util_bot_log(strings.REPORT_MESSAGE_TEXT % (html.escape(str(update.message.text)), str(update.message.from_user.name), str(chat_name), util.get_hash(int(chat_id))))
        bot.delete_message(update.message.chat_id, update.message.message_id)
        util.log_blocked_content('!non_west', update.message.chat_id, update.message.from_user.id, update.message.text)
  except AttributeError:
    return False

def check_safe_name(name, chat_id):
  db=MySQLdb.connect(config.database['server'],config.database['user'],config.database['password'],config.database['name'])
  db.autocommit(True)
  cur=db.cursor()
  cur.execute("SELECT * FROM SafeNames WHERE Chat_ID='"+str(chat_id)+"' AND Name='"+str(name)+"'")
  row=cur.fetchone()
  if cur.rowcount:
    res=True
  else:
    res=False
  cur.close()
  db.close()
  return res

def is_spam(text, url=False, chat_id=False, check=False):
  if text not in config.safe_names:
    if text in no_spam:
      return no_spam[text]
    if url == False:
      text=text.replace("@", "")
      url='https://telegram.me/'+text
    else:
      url = text
      text=text[13:]
      print(url)
    try:
      res=get(url)
      if res.status_code!=200:
        return False
      else:
        no_spam[text]='members</div>' in res.text
        if chat_id and check_safe_name(text, chat_id) == False:
            return no_spam[text]
        if check:
          return no_spam[text]
    except exceptions.MissingSchema:
      pass

def new_user_name(bot, update):
  if update.message is not None and update.message.new_chat_members is not None:
    for new in update.message.new_chat_members:
      first = str(new.first_name)
      last = str(new.last_name)
      if update.message.chat.username is not None:
        chat_name = update.message.chat.username
      else:
        chat_name = update.message.chat.title
      if str(last) == "None":
        last=""
      if any(s in str(first+last).lower() for s in mix_spam_list):
        chat_id=update.message.chat_id
        util.bot_log(strings.REPORT_USER_NAME % (str(first+last), str(chat_name), util.get_hash(int(chat_id))), bot)
        bot.kick_chat_member(chat_id, new.id)
        bot.delete_message(chat_id, update.message.message_id)
        util.log_blocked_content('!spam_in_username', update.message.chat_id, update.message.from_user.id, str(first+last))

def message_text(bot, update):
  if bot.get_chat_member(update.message.chat_id, update.message.from_user.id).status not in ["creator", "administrator"] or update.message.from_user.id not in config.admin_id:
    if update.message is not None:
      if update.message.text is None:
        if update.message.forward_from_chat:
          update.message.text = update.message.caption
      if update.message.text is not None:
        if any(s in str(update.message.text).lower() for s in config.spam_words):
          if update.message.chat.username is not None:
            chat_name = update.message.chat.username
          else:
            chat_name = update.message.chat.title
          chat_id=update.message.chat_id
          util.bot_log(strings.REPORT_MESSAGE_TEXT % (str(update.message.text), str(update.message.from_user.name), str(chat_name), util.get_hash(int(chat_id))), bot)
          bot.delete_message(chat_id, update.message.message_id)
          util.log_blocked_content('!spam_word', update.message.chat_id, update.message.from_user.id, update.message.text)

def message_entities(bot, update):
  if bot.get_chat_member(update.message.chat_id, update.message.from_user.id).status not in ["creator", "administrator"] or update.message.from_user.id not in config.admin_id:
    if update.message is not None and update.message.entities is not None:
      if update.message.forward_from_chat:
        update.message.text = update.message.caption
      if update.message.chat.username is not None:
        if update.message.chat.username not in config.safe_names:
          config.safe_names.append('@'+update.message.chat.username)
      for entitie in update.message.entities:
        if entitie.type=="mention":
          if update.message.text is not None:
            if update.message.chat.username is not None:
              chat_name = update.message.chat.username
            else:
              chat_name = update.message.chat.title
            e=update.message.text[entitie.offset:entitie.offset+entitie.length]
            if is_spam(e, False, update.message.chat_id):
              chat_id=update.message.chat_id
              util.bot_log(strings.REPORT_MESSAGE_TEXT % (html.escape(str(update.message.text)), str(update.message.from_user.name), str(chat_name), util.get_hash(int(chat_id))), bot)
              bot.delete_message(chat_id, update.message.message_id)
              util.log_blocked_content('!spam_telegram', update.message.chat_id, update.message.from_user.id, update.message.text)

def message_links(bot, update):
  if bot.get_chat_member(update.message.chat_id, update.message.from_user.id).status not in ["creator", "administrator"] or update.message.from_user.id not in config.admin_id:
    if update.message is not None:
      chat_id=update.message.chat_id
      if update.message.text is None:
        if update.message.forward_from_chat:
          update.message.text = update.message.caption
        else:
          return False
      if update.message.chat.username is not None:
        chat_name = update.message.chat.username
        config.safe_urls.append("https://t.me/"+chat_name)
        config.safe_urls.append("https://t.me/@"+chat_name)
      else:
        chat_name = update.message.chat.title
      urls = re.findall(config.regex_web_url, update.message.text)
      for url in urls:
        if url not in config.safe_urls:
          if is_spam(url, True, chat_id):
            util.bot_log(strings.REPORT_MESSAGE_URL % (str(update.message.text), str(update.message.from_user.name), str(chat_name), str(url), util.get_hash(int(chat_id))), bot)
            bot.delete_message(chat_id, update.message.message_id)
            util.log_blocked_content('!spam_domain', update.message.chat_id, update.message.from_user.id, update.message.text)
