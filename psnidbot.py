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
    sendMsg(bot, update, '發送或回覆 /id 搜索他人的PSNID /change更改您的PSNID')

@dp.message_handler(commands=['id'])
async def get_all_messages(message: types.Message):
    user = message.from_user
    last_input = mysql.get("users", "last_input", user.id)
    user_notes = eval(mysql.get("users", "notes", user.id))
    user_input_status = eval(mysql.get("users", "input_status", user.id))
    note_kb    = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    if not user_input_status["name_input"] and not user_input_status["description_input"]:
        if message.text == "[添加備註]":
            user_input_status["name_input"] = True
            mysql.set("users", "input_status", user.id, str(user_input_status))
            await message.reply("為你的筆記寫一個名字。")
            return

        if user_notes != {}:
            
            for note in user_notes.keys():
                if note not in message.text:
                    note_kb.add(KeyboardButton(f"{note} | {user_notes[note]['date']}"))
                else:
                    await message.reply(user_notes[note]["description"])
                    return
            note_kb.add(KeyboardButton("[添加備註]"))
                    
            await message.reply(f'這些都是你的筆記。 隨你挑。', reply_markup = note_kb)

        else:
            note_kb.add(KeyboardButton("[添加備註]"))
        
            await message.reply(f"你沒有任何筆記...", reply_markup = note_kb)
    else:
        if user_input_status["description_input"]:
            user_notes[last_input] = {"description" : message.text, "date": str(message.date)}
            mysql.set('users', 'notes', user.id, str(user_notes))
            user_input_status = {"name_input": False, "description_input": False}
            mysql.set('users', 'input_status', user.id, str(user_input_status))

            for note in user_notes.keys():
                note_kb.add(KeyboardButton(f"{note} | {user_notes[note]['date']}"))

            note_kb.add(KeyboardButton("[添加備註]"))

            await message.reply(f"筆記已保存！", reply_markup = note_kb)
            return
    
        if user_input_status["name_input"]:
            mysql.set('users', 'last_input', user.id, message.text)
            user_input_status["description_input"] = True
            mysql.set('users', 'input_status', user.id, str(user_input_status))
            await message.reply(f"筆記的線框已經創建，現在是時候編寫筆記本身了。")
            return

start_handler = CommandHandler('start',start)
help_handler = CommandHandler('help',helpmsg)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)

updater.start_polling()
