#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.error import TelegramError, Unauthorized, BadRequest,TimedOut, ChatMigrated, NetworkError
import logging, urllib, json
import config
import strings
import antispam
import handler
import blacklist
import util
import admin

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def error(bot, update, error):
    logger.warning('unifiedban/log: Update "%s" --- ha causato un errore --- "%s"', update, error)

def start(bot, update):
  if update.message.chat.type == 'private':
    update.message.reply_text(strings.START_MESSAGE, 
                              parse_mode=ParseMode.HTML,
                              disable_web_page_preview=True)

def main():
    updater=Updater(config.bot_token)
    dp = updater.dispatcher
    dp.add_error_handler(error)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("restart", admin.restart))
    dp.add_handler(CommandHandler("help", admin.help_message))
    dp.add_handler(CommandHandler("rm", admin.delete))
    dp.add_handler(CommandHandler("ban", admin.ban))
    dp.add_handler(CommandHandler("unban", admin.unban))
    dp.add_handler(CommandHandler("check", admin.check_permissions))
    dp.add_handler(CommandHandler("get", admin.get_data))
    dp.add_handler(CommandHandler("leave", admin.leave))
    dp.add_handler(CommandHandler("sync", admin.sync))
    dp.add_handler(CommandHandler("configure", admin.configure))
    
    dp.add_handler(CommandHandler("safe", admin.safe))
    dp.add_handler(CommandHandler("unsafe", admin.unsafe))
    dp.add_handler(CommandHandler("safenames", admin.safenames))
    
    dp.add_handler(CommandHandler("black", admin.add_to_blacklist))
    dp.add_handler(CommandHandler("white", admin.remove_from_blacklist))
    dp.add_handler(CommandHandler("sign", admin.sign))
    dp.add_handler(MessageHandler(None, handler.init))
    dp.add_handler(CallbackQueryHandler(admin.configure_edit))
    updater.start_polling()
    updater.idle()

if __name__=='__main__':
    main()
