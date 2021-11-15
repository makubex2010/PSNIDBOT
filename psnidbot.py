#! /usr/bin/python3
import _thread
import threading
import time
import logging
import pymongo
from collections import namedtuple
from datetime import datetime, timedelta, time
from functools import wraps
from telegram.ext import Updater
from telegram.ext import CommandHandler

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
    
def add(update, context):
    chat_id = update["message"]["chat"]["id"]
    text = " ".join(update["message"]["text"].split(' ')[1:])
    todo_list.find_one_and_update({'chat_id' : chat_id}, {"$push": {"todo_list": text}})
    update.message.reply_text("你的PSNID添加！")
    
def list_items(update, context):
    chat_id = update["message"]["chat"]["id"]
    _list = todo_list.find_one({'chat_id' : chat_id})
    text = ""
    for index, item in enumerate(_list["todo_list"]):
        text += str(index + 1) + "- " + item + "\n"
    update.message.reply_text(text)


start_handler = CommandHandler('start',start)
help_handler = CommandHandler('help',helpmsg)
add_handler = CommandHandler('add',add)
list_handler = CommandHandler('change',list_items)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(add_handler)
dispatcher.add_handler(list_handler)

updater.start_polling()
