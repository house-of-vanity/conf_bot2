#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

import logging
import os
import sys
from timer import Reminder

from telegram.ext import Updater, CommandHandler
from database import DataBase

DB = DataBase('data.sql')

TOKEN = os.environ.get('TOKEN')
if TOKEN == None:
  print('Define TOKEN env var!')
  sys.exit(1)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    update.message.reply_text('Hi! Use /set <seconds> to set a timer')


def alarm(rem):
    """Send the alarm message."""
    text = rem['message'][1:]
    text = f"{rem['time_str'][0]}{rem['time_str'][1]}:"\
    f"{rem['time_str'][2]}{rem['time_str'][3]} @xelnagamex @ultradesu @condrix \n" + " ".join(text)
    rem['context'].bot.send_message(rem['chat_id'], text=text)

reminder = Reminder(callback=alarm)

def dota(update, context):
    if len(context.args) == 0:
        update.message.reply_text('Use one of patch, hero, item.')
    if context.args[0] == 'patches':
        patches = DB.get_patch_list()
        update.message.reply_text(f'List of patches {patches}')
    context.bot.send_message(update.message.chat_id, context.args[0])

def set_timer(update, context):
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        reminder.add_reminder(
            msg=context.args,
            context=context,
            chat_id=chat_id)
        update.message.reply_text('Хорошо, я напомню, а теперь иди нахуй.')

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Run bot."""
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(CommandHandler("alert", set_timer,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("dota", dota,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
