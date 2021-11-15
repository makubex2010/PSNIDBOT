#! /usr/bin/python3
import _thread
import threading
import time
import logging
import mysql
from Roll import Roll
from telegram.ext import Updater
from telegram.ext import CommandHandler

updater = Updater(token="2132340913:AAGeFSdbISuDcCAZB3q42PXtFfojjB2j1O8")

dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def replyMsg(update, context, msg):
    context.bot.sendMessage(chat_id=update.message.chat_id, reply_to_message_id = update.message.message_id, text = msg)

def sendMsg(update, context, msg):
    context.bot.sendMessage(chat_id=update.message.chat_id, text = msg)


def start(bot, update):
    sendMsg(bot, update, '如果您需要幫助，請使用 /help')

def helpmsg(bot, update):
    sendMsg(bot, update, '發送或回覆 /id 以搜索某人的 PsnID\n/change更改以設置您的 PsnID')
    
def searchid(bot, update, args):
        try:
                msg = ''.join(args)
                if(len(msg) > 0):
                        msg = msg[1:]
                        psnid = mysql.searchname(msg)
                else:
                        user = update.message.reply_to_message.from_user
                        psnid = mysql.searchindb(user.id)
                whose = 'ID: '
        except:
                user = update.message.from_user
                psnid = mysql.searchindb(user.id)
                whose = '你的PSNID是: '
        if(psnid == -1):
                psnid = 'Not define'
        msgid = update.message.message_id
        replyMsg(bot, update, str(whose) + str(psnid))
#        delmsg(bot, update)
        _thread.start_new_thread(delmsg,(bot,update) )

def changeid(bot, update, args):
        userid = update.message.from_user.id
        msgid = update.message.message_id
        username = update.message.from_user.username
        msg = ' '.join(args)
        if(len(msg) <= 0):
                replyMsg(bot, update, '請告訴我你的新ID')
                return
        if(mysql.searchindb(userid) != -1):
                mysql.changeondb(userid, msg, username)
                replyMsg(bot, update, '更新')
        else:
                mysql.inserttodb(userid, msg, username)
                replyMsg(bot, update, '更改完成')
#        delmsg(bot, update)
        _thread.start_new_thread(delmsg,(bot,update) )


start_handler = CommandHandler('start',start)
search_handler = CommandHandler('id',searchid, pass_args = True)
change_handler = CommandHandler('change',changeid, pass_args = True)
help_handler = CommandHandler('help',helpmsg)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(search_handler)
dispatcher.add_handler(change_handler)
dispatcher.add_handler(help_handler)

updater.start_polling()
