#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

import logging
import os
import sys
from timer import Reminder

from telegram import *
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
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

def build_menu(buttons,
    n_cols,
    header_buttons=None,
    footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu

def dota(update, context):
    if len(context.args) == 0:
        keyboard = [
          [
            InlineKeyboardButton("Patches", callback_data="patches"),
            InlineKeyboardButton("Heroes", callback_data="heroes"),
            InlineKeyboardButton("Items", callback_data="items"),
            InlineKeyboardButton("Close", callback_data="close"),
          ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('What do you wanna know?', reply_markup=reply_markup)

def button(update, context):
    query = update.callback_query
    if query.data.split('_')[0] == 'close':
        query.edit_message_text('Bye')
    if query.data.split('_')[0] == 'dota':
        keyboard = [
          [
            InlineKeyboardButton("Patches", callback_data="patches"),
            InlineKeyboardButton("Heroes", callback_data="heroes"),
            InlineKeyboardButton("Items", callback_data="items"),
            InlineKeyboardButton("Close", callback_data="close"),
          ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text('What do you wanna know?', reply_markup=reply_markup)
    if query.data.split('_')[0] == 'patch':
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data='patches'),]])
        query.edit_message_text(f"Tut ya sdelayoo informatsiy o petche {query.data}", reply_markup=reply_markup)
    if query.data.split('_')[0] == 'item':
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data='items'),]])
        item_name = query.data.split('_')[1]
        item_history = DB.get_item_history(item_name)
        text = f'*{item_name}* update history\n'
        cur_patch = ''
        for upd in item_history:
           if upd[0] != cur_patch:
              text += f"\n{'◀'*1}*{upd[0]}*{'▶'*1}\n"
              cur_patch = upd[0]
           text += f'\t\t 🔹 {upd[1]}\n' 
        query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

    if query.data.split('_')[0] == 'hero':
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data='heroes'),]])
        hero_name = query.data.split('_')[1]
        hero_history = DB.get_hero_history(hero_name)
        text = f'*{hero_name}* update history\n'
        cur_patch = ''
        cur_type = ''
        for upd in hero_history:
            if len(text) > 3900:
                text += '\nMessage too long ...'
                break
            if upd[0] != cur_patch:
               text += f"\n{'◀'*1}*{upd[0]}*{'▶'*1}\n"
               cur_patch = upd[0]
               cur_type = ''
            if upd[1] != cur_type:
               text += f"🔆*{upd[1].capitalize()}*\n"
               cur_type = upd[1]
            text += f'\t\t 🔹 {upd[2]}\n' 
        query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

    if query.data.split('_')[0] == 'patches':
        patches = DB.get_patch_list()
        patches.reverse()
        keyboard = [[]]
        in_a_row = 5
        for patch in patches:
            if len(keyboard[-1]) == in_a_row:
                keyboard.append(list())
            keyboard[-1].append(InlineKeyboardButton(f"{patch}", callback_data=f"patch_{patch}"))
        keyboard.append([InlineKeyboardButton("Back", callback_data='dota')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text="Select patch", reply_markup=reply_markup)
    if query.data.split('_')[0] == 'heroes':
        per_page = 20
        try:
            page = int(query.data.split('_')[1])
        except:
            page = 0
        heroes = DB.get_heroes_list()
        heroes.sort()
        last_hero = page*per_page+per_page
        if len(heroes) <= last_hero - 1:
            last_hero = len(heroes)
        keyboard = [[]]
        in_a_row = 2
        for hero in heroes[page*per_page:last_hero]:
            if len(keyboard[-1]) == in_a_row:
                keyboard.append(list())
            keyboard[-1].append(InlineKeyboardButton(f"{hero}", callback_data=f"hero_{hero}"))
#       prev_page = page-1
#       next_page = page+1
        keyboard.append([])
        if page != 0:
            keyboard[-1].append(
                InlineKeyboardButton("<=", callback_data=f'heroes_{page-1}'),
            )
        if len(heroes) != last_hero:
            keyboard[-1].append(
                InlineKeyboardButton("=>", callback_data=f'heroes_{page+1}'),
            )

        keyboard.append([InlineKeyboardButton("Back", callback_data='dota')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text=f"Select hero {page*per_page}:{page*per_page+per_page}", reply_markup=reply_markup)
    if query.data.split('_')[0] == 'items':
        items = DB.get_items_list()
        keyboard = [[]]
        in_a_row = 2
        for item in items:
            if len(keyboard[-1]) == in_a_row:
                keyboard.append(list())
            keyboard[-1].append(InlineKeyboardButton(f"{item}", callback_data=f"item_{item}"))
        keyboard.append([InlineKeyboardButton("Back", callback_data='dota')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text="Select item", reply_markup=reply_markup)

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
    dp.add_handler(CallbackQueryHandler(button))
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
