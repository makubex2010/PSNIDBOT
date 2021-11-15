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

def delmsg(bot, update):
    time.sleep(10)
    try:
        bot.delete_message(update.message.chat_id, update.message.message_id + 1)
    except:
        pass

def start(bot, update):
    sendMsg(bot, update, '如果您需要幫助，請使用 /help')

def helpmsg(bot, update):
    sendMsg(bot, update, '發送或回覆 /id 搜索他人的PSNID /change更改您的PSNID')

def searchid(bot, update):
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
        if(liveid == -1):
                psnid = 'Not define'
                msgid = update.message.message_id
                replyMsg(bot, update, str(whose) + str(psnid)
#        delmsg(bot, update)
        _thread.start_new_thread(delmsg,(bot,update) )


                 
def changeid(bot, update, args):
        userid = update.message.from_user.id
        msgid = update.message.message_id
        username = update.message.from_user.username
        msg = ' '.join(args)
        if(len(msg) <= 0):
                replyMsg(bot, update, 'Please tell me your new id')
                return
        if(mysql.searchindb(userid) != -1):
                mysql.changeondb(userid, msg, username)
                replyMsg(bot, update, 'updated')
        else:
                mysql.inserttodb(userid, msg, username)
                replyMsg(bot, update, 'changed')
#        delmsg(bot, update)
        _thread.start_new_thread(delmsg,(bot,update) )

start_handler = CommandHandler('start',start)
createRoll_handler = CommandHandler('createRoll',createRoll, pass_args = True)
rollList_handler = CommandHandler('RollList',rollList)
joinRoll_handler = CommandHandler('join',joinRoll, pass_args = True)
search_handler = CommandHandler('id',searchid, pass_args = True)
change_handler = CommandHandler('change',changeid, pass_args = True)
help_handler = CommandHandler('help',helpmsg)
setAdmins_handler = CommandHandler('setadmins', setAdmins)

dispatcher.add_handler(joinRoll_handler)
dispatcher.add_handler(setAdmins_handler)
dispatcher.add_handler(rollList_handler)
dispatcher.add_handler(createRoll_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(search_handler)
dispatcher.add_handler(change_handler)
dispatcher.add_handler(help_handler)

updater.start_polling()
