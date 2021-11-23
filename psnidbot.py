#! /usr/bin/python3
import random, os
import _thread
import threading
import time
import logging
import mysql
from Roll import Roll
from telegram.ext import Updater, CommandHandler

admins = []
updater = Updater(token="2132340913:AAEo1wKZdu6YMJO4X1Xm5wibIjvwnBRFKzo")
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def replyMsg(bot, update, msg):
    bot.sendMessage(chat_id=update.message.chat_id, reply_to_message_id = update.message.message_id, text = msg)

def sendMsg(bot, update, msg):
    bot.sendMessage(chat_id=update.message.chat_id, text = msg)

def delmsg(bot, update):
    time.sleep(300)
    try:
        bot.delete_message(update.message.chat_id, update.message.message_id + 1)
    except:
        pass
    
 
def setAdmins(bot, update):
    if(update.message.from_user.id == 894575091):  #Bot Admin's userid
        adm = update.message.chat.get_administrators()
        for a in adm:
            admins.append(a.user.id)
        sendMsg(bot, update, '完畢')
    else:
        sendMsg(bot, update, "你沒有權限")


def isAdmin(bot, update):
    if(update.message.from_user.id in admins):
        return 1
    else:
        sendMsg(bot, update, "你沒有權限")
        return 0

def start(bot, update):
    sendMsg(bot, update, '如果您需要幫助，請使用 /help')

def helpmsg(bot, update):
    sendMsg(bot, update, '發送@或回覆 /id 搜索他人的 PSNID\n/change 可登記或更改您的 PSNID\n(例如:/change Azuki_Minaduki)\n如果沒有設定username將無法紀錄')
    
def searchid(bot, update, args):
        try:
                msg = ''.join(args)
                if(len(msg) > 0):
                        msg = msg[1:]
                        psnid = mysql.searchname(msg)
                else:
                        user = update.message.reply_to_message.from_user
                        psnid = mysql.searchindb(user.id)
                whose = '他的PSNID是: '
        except:
                user = update.message.from_user
                first_name = update.message.chat.first_name
                psnid = mysql.searchindb(user.id)
                whose = '你的PSNID是: '
        if(psnid == -1):
                psnid = '沒有登錄'
        msgid = update.message.message_id
        replyMsg(bot, update, str(first_name) + str(whose) + str(psnid))
#        delmsg(bot, update)
        _thread.start_new_thread(delmsg,(bot, update) )

def changeid(bot, update, args):
        userid = update.message.from_user.id
        msgid = update.message.message_id
        username = update.message.from_user.username
        msg = ' '.join(args)
        if(len(msg) <= 0):
                replyMsg(bot, update, '請告訴我你的PSNID\n(例如:/change Azuki_Minaduki)\n如果沒有設定username將無法紀錄')
                return
        if(mysql.searchindb(userid) != -1):
                mysql.changeondb(userid, msg, username)
                replyMsg(bot, update, '你的PSNID已登錄')
        else:
                mysql.inserttodb(userid, msg, username)
                replyMsg(bot, update, '你的PSNID已更改完成')
#        delmsg(bot, update)
        _thread.start_new_thread(delmsg,(bot, update) )
    

start_handler = CommandHandler('start',start)
search_handler = CommandHandler('id',searchid, pass_args = True)
change_handler = CommandHandler('change',changeid, pass_args = True)
help_handler = CommandHandler('help',helpmsg)
setAdmins_handler = CommandHandler('setadmins', setAdmins)

dispatcher.add_handler(setAdmins_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(search_handler)
dispatcher.add_handler(change_handler)
dispatcher.add_handler(help_handler)
updater.start_polling()
