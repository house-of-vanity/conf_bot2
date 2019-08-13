#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.
#
# THIS EXAMPLE HAS BEEN UPDATED TO WORK WITH THE BETA VERSION 12 OF PYTHON-TELEGRAM-BOT.
# If you're still using version 11.1.0, please see the examples at
# https://github.com/python-telegram-bot/python-telegram-bot/tree/v11.1.0/examples

"""
Simple Bot to send timed Telegram messages.
This Bot uses the Updater class to handle the bot and the JobQueue to send
timed messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Alarm Bot example, sends a message after a set time.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os
import sys
from timer import Reminder

from telegram.ext import Updater, CommandHandler

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
#   job = context.job
    text = rem['message'][1:]
#   text = " ".join(list(map(lambda x: x.encode('utf-8'), text)))
    text = f"{rem['time_str'][0]}{rem['time_str'][1]}:"\
    f"{rem['time_str'][2]}{rem['time_str'][3]} @xelnagamex @ultradesu @condrix \n" + " ".join(text)
    rem['context'].bot.send_message(rem['chat_id'], text=text)

reminder = Reminder(callback=alarm)

def set_timer(update, context):
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
#       due = int(context.args[0])
#       if due < 0:
#           update.message.reply_text('Sorry we can not go back to future!')
#           return

        # Add job to queue
        reminder.add_reminder(
            msg=context.args,
            context=context,
            chat_id=chat_id)
#       job = context.job_queue.run_once(alarm, due, context=chat_id)
#       context.chat_data['job'] = job

        update.message.reply_text('Хорошо, я напомню, а теперь иди нахуй.')

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(CommandHandler("alert", set_timer,
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
