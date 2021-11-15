#! /usr/bin/python3
import _thread
import threading
import time
import logging
import pymongo
import logging
import json
import sys
from collections import namedtuple
from datetime import datetime, timedelta, time
from functools import wraps
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram import ParseMode

from dbmanager import DBManager as dbm
from extras

# load config
with open("config.json") as f:
    config = json.load(f)

#logging
log_config = config.get("log")

LOGFILE = log_config.get("debug")
BOTLOG = log_config.get("filename")
LOGFORMAT = log_config.get("logformat")
LOGLEVEL = logging.INFO

logging.basicConfig(format=LOGFORMAT, level=LOGLEVEL, filename=LOGFILE)
logger = logging.getLogger(__name__)

#handlers
filehandler = logging.FileHandler(BOTLOG)
filehandler.setLevel(LOGLEVEL)

formatter = logging.Formatter(LOGFORMAT)
filehandler.setFormatter(formatter)

logger.addHandler(filehandler)


PARSEMODE = ParseMode.MARKDOWN

# named tuple for unpacked update
Update = namedtuple('Update', 'username, user_id, text, date')

updater = Updater(token="2132340913:AAGeFSdbISuDcCAZB3q42PXtFfojjB2j1O8")
MONGODB_CLIENT = 'mongodb+srv://makubex2010:306578@cluster0.kjrdp.mongodb.net/psnid?retryWrites=true&w=majority'
DB_NAME = 'psnid'
COLLECTION_NAME = 'PSNID'


client = pymongo.MongoClient(MONGODB_CLIENT)
db = client[DB_NAME]
todo_list = db[COLLECTION_NAME]

dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def replyMsg(update, context, msg):
    context.bot.sendMessage(chat_id=update.message.chat_id, reply_to_message_id = update.message.message_id, text = msg)

def sendMsg(update, context, msg):
    context.bot.sendMessage(chat_id=update.message.chat_id, text = msg)


def start(bot, update):
    sendMsg(bot, update, '如果您需要幫助，請使用 /help')

def helpmsg(bot, update):
    sendMsg(bot, update, '發送 /add 添加PSNID 或 /change 查詢名單')
    sendMsg(bot, update, '添加格式為: KevinChen💫(AzukiMinaduki) 以好辨認!')

def add_task(bot, update):
    upd = up_data(update)
    
    # parse input
    message = upd.text
    message = message.split()[1:]

    parsed = parse_date(message, update)

    if not parsed:
        update.message.reply_text("未找到指定的時間段！")
        return

    message = parsed[1]
    
    day = datetime.strftime(parsed[0], DATEFORMAT)
    
    # add to db
    with dbm(upd.user_id) as db:
        db.add(day, message)

    logger.info(f"Adding '{message}' for user '{upd.user_id}:{upd.username}' to '{day}'")
    update.message.reply_text("正在更新任務列表...")

def get_task(bot, update):
    upd = up_data(update)

    reply = ""
    message = upd.text.split()[1:]
    with dbm(upd.user_id) as db:
        if not message:
            data = db.get()
            day = datetime.strftime(upd.date, DATEFORMAT) # default get today
        else:
            day, _ = parse_date(message, update)
            day = datetime.strftime(day, DATEFORMAT)
            data = db.get(day)
            if not data:
                reply += f"*{day}* - "
    
    if not data:
        reply += "*Todo List* is empty!"
    elif len(data.keys()) == 1:
        reply += f"*{day}*\n"
        try:
            data = data['tasks']
        except KeyError:
            try:
                data = data[day]['tasks']
            except KeyError:
                day, data = list(data.items())[0]
                data = data['tasks']
                reply = f"*{day}*\n"
        
        for num, task in data.items():
            if task['done']:
                reply += f"`{num})` \u2705 "
            else:
                reply += f"`{num})` \u274c "
            reply += f"{task['text']}\n"

    else:
        data = data.items()
        items = [(day, day_data) for day, day_data in data]
        items.sort(key=lambda x: x[0]) # sort by date ascending

        days = []
        for day, data in items:
            reply_piece = f"*{day}*\n"
            for num, task in data['tasks'].items():
                if task['done']:
                    reply_piece += f"`{num})` \u2705 "
                else:
                    reply_piece += f"`{num})` \u274c "
                reply_piece += f"{task['text']}\n"
            days.append(reply_piece)

        reply += "\n".join(days)

    update.message.reply_text(reply, parse_mode=PARSEMODE)
    logger.info(f"Getting tasks for '{upd.user_id}:{upd.username}'")
    
def delete_task(bot, update):
    upd = up_data(update)
    day = datetime.strftime(upd.date, DATEFORMAT)
    reply = ""

    message = upd.text.split()[1:]

    if not message:
        reply += "Tell me what to delete."
        logger.debug("/delete command empty")
        update.message.reply_text(reply)
        return

    with dbm(upd.user_id) as db:
        date_match = re.match(DATEREGEX, message[0])
        if len(message) == 1:
            if message[0] == 'all':
                db.delete(force=True)
                reply += "Deleting database"
                logger.info("Deleting all tasks for '{upd.user_id}:{upd.username}'")

            # Without specifying date default delete task from today
            if message[0].isdigit():
                try:
                    db.delete(day, message[0])
                    reply += f"Deleting task {message[0]} from *today*"
                    logger.info(f"Deleting '{message[0]}' on '{day}' for '{upd.user_id}:{upd.username}'")
                except KeyError:
                    reply += f"Task {message[0]} in list {day} not found!"
                
            if date_match:
                if message[0] in tomorrow:
                    message[0] = datetime.strftime(upd.date+timedelta(days=1), DATEFORMAT)
                try:
                    if message[0] == 'today':
                        db.delete(day)
                        reply += "Deleting *today*"
                    else:
                        db.delete(message[0])
                        reply += f"Deleting day *{message[0]}*"
                    logger.info(f"Deleting '{message[0]}' for '{upd.user_id}:{upd.username}'")
                except KeyError:
                    reply += f"{message[0]} not found!"

            if not reply:
                reply += f"\"{message[0]}\" not found!"

            
        else:
            if not date_match:
                reply += f"{message[0]} not found!"
            else:
                if message[0] in tomorrow:
                    message[0] = datetime.strftime(upd.date+timedelta(days=1), DATEFORMAT)
                if message[1].isdigit():
                    try:
                        db.delete(message[0], message[1])
                        reply += f"Deleting task {message[1]} from {message[0]}"
                        logger.info(f"Deleting '{message[1]}' from '{message[0]}' for '{upd.user_id}:{upd.username}'")
                    except KeyError:
                        reply += f"Task {message[1]} not found in {message[0]}"

        update.message.reply_text(reply, parse_mode=PARSEMODE)


start_handler = CommandHandler('start',start)
help_handler = CommandHandler('help',helpmsg)
add_handler = CommandHandler('add',add_task)
list_handler = CommandHandler('change',get_task)
delete_handler = CommandHandler('delete',delete_task)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(add_handler)
dispatcher.add_handler(list_handler)
dispatcher.add_handler(delete_handler)

updater.start_polling()
