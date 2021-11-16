#! /usr/bin/python3
import _thread
import threading
import time
import logging
import mysql
from Roll import Roll
from telegram.ext import Updater
from telegram.ext import CommandHandler

admins = []
rolllist = []
rollid = 100
updater = Updater(token="2132340913:AAGeFSdbISuDcCAZB3q42PXtFfojjB2j1O8")
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def replyMsg(update, context, msg):
    context.bot.sendMessage(chat_id=update.message.chat_id, reply_to_message_id = update.message.message_id, text = msg)

def sendMsg(update, context, msg):
    context.bot.sendMessage(chat_id=update.message.chat_id, text = msg)

def delmsg(update, context):
    time.sleep(10)
    try:
        bot.delete_message(update.message.chat_id, update.message.message_id + 1)
    except:
        pass
 
def setAdmins(update, context):
    if(update.message.from_user.id == 894575091):  #Bot Admin's userid
        adm = update.message.chat.get_administrators()
        for a in adm:
            admins.append(a.user.id)
        sendMsg(update, context, '完畢')
    else:
        sendMsg(update, context, "你沒有權限")


def isAdmin(update, context):
    if(update.message.from_user.id in admins):
        return 1
    else:
        sendMsg(update, context, "你沒有權限")
        return 0

def start(update, context):
    sendMsg(update, context, '如果您需要幫助，請使用 /help')

def helpmsg(update, context):
    sendMsg(update, context, '發送或回覆 /id 搜索他人的 PsnID\n/change 可更改以您的 PsnID')
    
def searchid(update, context):
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
#        delmsg(update, context)
        _thread.start_new_thread(delmsg,(bot, update) )

def changeid(update, context):
        userid = update.message.from_user.id
        msgid = update.message.message_id
        username = update.message.from_user.username
        msg = ' '.join(args)
        if(len(msg) <= 0):
                replyMsg(update, context, '請告訴我你的新ID')
                return
        if(mysql.searchindb(userid) != -1):
                mysql.changeondb(userid, msg, username)
                replyMsg(update, context, '更新')
        else:
                mysql.inserttodb(userid, msg, username)
                replyMsg(update, context, '更改完成')
#        delmsg(update, context)
        _thread.start_new_thread(delmsg,(bot, update) )

def createRoll(update, context):
    global rolllist
    global rollid
    if(isAdmin(update, context)):
        if(len(args) < 2):
            sendMsg(update, context, '輸入錯誤')
        else:
            try:
                rolllist.append(Roll(rollid, args[0], float(args[1])))
                sendMsg(update, context, '全部完成，/rolllist 查看滾動列表')
                rollid = rollid + 1
                rolllist[-1].start()
            except:
                sendMsg(update, context, '因未知錯誤而失敗！')
            
def rollList(update, context):
    global rolllist
    global rollid
    Rlist = 'Rollid\t\t\tTitle\t\t\tWinner'
    for rollobj in rolllist:
        Rlist += '\n' + str(rollobj.rollid) + '\t' + rollobj.title + '\t' + rollobj.closetime + '\t' + rollobj.winner
    sendMsg(bot, update ,Rlist)

def joinRoll(update, context):
    for a in rolllist:
        if(str(a.rollid) == args[0]):
            if(update.message.from_user.username != ''):
                a.user.append(update.message.from_user.username)
                sendMsg(update, context, "你已加入")
                return 0
            else:
                sendMsg(update, context, "好像沒有你的用戶名")
                return -1
            sendMsg(update, context, '發生錯誤')
    
start_handler = CommandHandler('start',start)
createRoll_handler = CommandHandler('createRoll',createRoll, args = True)
rollList_handler = CommandHandler('RollList',rollList)
joinRoll_handler = CommandHandler('join',joinRoll, args = True)
search_handler = CommandHandler('id',searchid, args = True)
change_handler = CommandHandler('change',changeid, args = True)
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
