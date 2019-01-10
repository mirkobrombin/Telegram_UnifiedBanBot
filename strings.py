# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

HELP_MESSAGE = "<b>unified/ban command list</b>\n \
/configure [Open configuration menu]\n \
/check [Check bot permissions]\n \
/safe (group_username) [Add group username to safenames]\n \
/unsafe (group_username) [Remove group username to safenames]\n \
/safenames [Show safenames]\n \
/ban [reply to a message]\n \
/unban [reply to a message]\n \
/rm [reply to a message] to delete\n \
/sign to enable Dashboard"

UNIFIEDBANREPORT_PREFIX = "<b>unified/ban [report]:</b> "

REPORT_HASH_CODE = "\n\nhash_code: #%s"

DASH_USER_SIGN = UNIFIEDBANREPORT_PREFIX+"User %s with User_ID %s signed in Dashboard for Chat (%s) with Chat_ID %s"+REPORT_HASH_CODE

SYNCING_BLACKLIST = "<i>[» Syncing the chat «]</i>\nThis will take a <b>few minutes ..</b>\nThis action is only performed when major changes are made to the Blacklist."
SYNC_COMPLETE = "<b>[Chat synchronized!]</b>\nBlocked %s malicious users.\n<a href='https://t.me/unifiedban_news'>> More info</a>"
DASH_SYNCING_BLACKLIST = "Operation required from Dashboard.\n"+SYNCING_BLACKLIST

SYNC_REPORT = UNIFIEDBANREPORT_PREFIX+"Chat %s synchronized with the Blacklist, added %s User_ID"+REPORT_HASH_CODE

BAN_REPORT = UNIFIEDBANREPORT_PREFIX+"User %s with ID %s in the Blacklist, removed from chat %s."+REPORT_HASH_CODE

VERIFIED_USER = "%s is a verified user of unified/ban.\n<i>He can perform maintenance</i>"

USER_BLACKLIST = "<i>%s added to the Blacklist</i>"
USER_ALREADY_IN_BLACKLIST = "User %s already in Blacklist."
USER_NOT_IN_BLACKLIST = "User %s not in Blacklist."
USER_BAN = "<i>User %s banned!</i>"
USER_UNBAN = "<i>Ban removed for user %s</i>"

BOT_PERMISSIONS = "<b>I have the following permissions:</b>\nDELETE_MESSAGES: %s \nRESTRICT_MEMBERS: %s \n<a href='https://t.me/unifiedban_news/8'>> About permissions</a>"
BOT_PERMISSIONS_NO = "<b>Status:</b> Insufficient permissions."
BOT_PERMISSIONS_OK = "<b>Status:</b> Correct permissions."

DELETE_DELAY_FOOTER = "\nThis message will deleted in 5 seconds .."
SAFE_NAME_SAVED = "New safename: <b>%s</b> created!"+DELETE_DELAY_FOOTER
SAFE_NAME_REMOVED = "Safename: <b>%s</b> removed!"+DELETE_DELAY_FOOTER
INVALID_SAFENAME = "Invalid safename!"
LIST_SAFENAMES = "Here is the list of Safenames for your chat\n%s"
REPORT_BOT_REMOVED = UNIFIEDBANREPORT_PREFIX+"Bot removed from Chat %s (Chat_ID: %s Type: %s)"+REPORT_HASH_CODE
REPORT_NEW_GROUP = UNIFIEDBANREPORT_PREFIX+"New registered group: %s (Chat_ID: %s)"+REPORT_HASH_CODE
REPORT_USER_NAME = UNIFIEDBANREPORT_PREFIX+"The name contains spam:\n<code>%s</code>\n<b>Chat:</b>\n%s\nDeleted."+REPORT_HASH_CODE
REPORT_MESSAGE_TEXT = UNIFIEDBANREPORT_PREFIX+"Deleted a message for spam.\n<b>Message content:</b>\n<code>%s</code>\n<b>Author:</b>%s\n<b>Source:</b>%s"+REPORT_HASH_CODE
REPORT_MESSAGE_URL = REPORT_MESSAGE_TEXT+"\n<b>Spam:</b>\n<code>%s</code>"+REPORT_HASH_CODE
REPORT_DELETED_MESSAGE = UNIFIEDBANREPORT_PREFIX+"%s deleted a message from chat %s\n<b>Message text:</b>\n<code>%s</code>"+REPORT_HASH_CODE
REPORT_MESSAGE_INFO = UNIFIEDBANREPORT_PREFIX+"%s requested message informations:\n<b>Message_ID:</b><code>%s</code>\n<b>Username:</b><code>%s</code>\n<b>Name:</b><code>%s</code>\n<b>Surname:</b><code>%s</code>\n<b>User_ID:</b><code>%s</code>\n<b>Lang:</b> %s\n<b>Is_bot?</b> %s"+REPORT_HASH_CODE
REPORT_MESSAGE_FORWARD_INFO = UNIFIEDBANREPORT_PREFIX+"%s requested forward message informations:\n<b>Username:</b><code>%s</code>\n<b>Name:</b><code>%s</code>\n<b>Surname:</b><code>%s</code>\n<b>User_ID:</b><code>%s</code>\n<b>Lang:</b> %s\n<b>Is_bot?</b> %s"+REPORT_HASH_CODE
REPORT_CHAT_INFO = UNIFIEDBANREPORT_PREFIX+"%s requested chat informations:\n<b>Username:</b><code>%s</code>\n<b>Titolo:</b><code>%s</code>\n<b>ID:</b><code>%s</code>\n<b>Type:</b> %s\n"+REPORT_HASH_CODE
REPORT_NEW_USER_IN_BLACKLIST = UNIFIEDBANREPORT_PREFIX+"%s added new user (%s) to the Blacklist from chat %s"+REPORT_HASH_CODE
REPORT_REMOVED_FROM_BLACKLIST = UNIFIEDBANREPORT_PREFIX+"%s removed user (%s) from the Blacklist and removed ban from chat %s"+REPORT_HASH_CODE
REPORT_USER_BAN = UNIFIEDBANREPORT_PREFIX+"%s banned user: %s with User_ID: %s from Chat %s"+REPORT_HASH_CODE
REPORT_USER_UNBAN = UNIFIEDBANREPORT_PREFIX+"%s removed ban for user: %s with User_ID: %s from Chat %s"+REPORT_HASH_CODE

START_MESSAGE = "Hi! Add me as your group's admin to start!\nCheck my permissions by typing /check in your group and type /configure to configure me.\n\nI will immediately start to block the spam.\nDeveloper: linuxhub.it\n\nRemember to follow my channel for News and Tricks!\n<a href='https://t.me/unifiedban_news'>> Go to Channel</a>"
LEAVING="[@unifiedban_bot removed from this Chat!]"
DEBUG_UPDATE="[DEBUG_MESSAGE] chat_name: %s \n chat_id: %s \n chat_user: %s \n author_id: %s \n author_user: %s \n author_name: %s \n post_text: %s"

CONF_MENU_HEADER = "<b>{{%s}} - 🔧 Group configuration Menu</b>\n\n \
- <b>Bot log:</b> \n<i>Disable log bot operations (deleted spam/scam)</i>\n \
- <b>Spam words:</b> \n<i>Delete messages containing common spam words</i>\n \
- <b>Spam non-west chars:</b> \n<i>Delete messages containing non-west chars</i>\n \
- <b>Spam Telegram:</b> \n<i>Delete messages containing Telegram group link and username</i>\n \
- <b>Spam Username:</b> \n<i>Delete messages from new users with name containing spam</i>\n \
- <b>Blacklist:</b> \n<i>Kick users recognized as malicious</i>\n \
- <b>Antiscam:</b> \n<i>Try to identify and block scams</i>\n \
- <b>Close/Open group:</b> \n<i>Close the group to new members that will be limited until the reopening</i>"
CONF_LOG = "📄 Bot log: [%s]"
CONF_ANTISPAM_WORDS = "🅰️ Spam words: [%s]"
CONF_ANTISPAM_NON_WEST = "🈵 Spam non-west chars: [%s]"
CONF_ANTISPAM_USERNAME = "✈️ Spam Telegram: [%s]"
CONF_ANTISPAM_USER = "📟 Spam username: [%s]"
CONF_BLACKLIST = "🚷 Blacklist: [%s]"
CONF_ANTISCAM = "💯 Antiscam: [%s]"
CONF_HAMMER = "🚪 %s your group [Coming soon..]"
CONF_LEAVE = "Leave this chat"
CONF_CLOSE_MENU = "Close menu"
CONF_MENU_CLOSED = "Menu closed."