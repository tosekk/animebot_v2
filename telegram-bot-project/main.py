# Standard Modules
from datetime import datetime as dt
from time import sleep


# Third Party Modules
from telebot import TeleBot
from telebot.types import (CallbackQuery, InlineKeyboardButton, 
                           InlineKeyboardMarkup, Message)



# Local Modules
import bot_token
import welcome_handler as w_handler


# Bot Initialization
bot = TeleBot(bot_token.token)


# Variables
bot.w_file = "animation"
bot.file_path = "static/w_animation.gif"


@bot.message_handler(commands=["start"])
def welcome(message: Message) -> None:
    
    if bot.w_file != "text":
        with open(bot.file_path, "rb") as file:
            if bot.w_file == "photo":
                bot.send_photo(message.chat.id, file)
            elif bot.w_file == "sticker" or bot.w_file == "animated":
                bot.send_sticker(message.chat.id, file)
            elif bot.w_file == "animation":
                bot.send_animation(message.chat.id, file)
                
    msg_text = w_handler.prep_cmd_msg(message)
    
    bot.send_message(message.chat.id, msg_text)
    

@bot.message_handler(["help"])
def help(message: Message) -> None:
    
    msg_text = w_handler.prep_cmd_msg(message)
    
    bot.send_message(message.chat.id, msg_text)


@bot.message_handler(["config"])
def config(message: Message) -> None:
    
    config_keyboard = InlineKeyboardMarkup(row_width=2)
    
    photo_key = InlineKeyboardButton(text="Фото + Текст", 
                                     callback_data="photo")
    animation_key = InlineKeyboardButton(text="Анимация + Текст", 
                                         callback_data="animation")
    sticker_key = InlineKeyboardButton(text="Стикер + Текст", 
                                       callback_data="sticker")
    text_key = InlineKeyboardButton(text="Только текст", 
                                    callback_data="text")
    
    config_keyboard.add(photo_key, animation_key, 
                        sticker_key, text_key)
    
    bot.send_message(message.chat.id, "Выберите тип приветствия!", 
                     reply_markup=config_keyboard)


def _sticker_type(message: Message) -> None:
    
    sticker_keyboard = InlineKeyboardMarkup(row_width=2)
    
    standard_key = InlineKeyboardButton(text="Простой стикер",
                                        callback_data="standard")
    anim_key = InlineKeyboardButton(text="Анимированный стикер",
                                    callback_data="animated")
    
    sticker_keyboard.add(standard_key, anim_key)
    
    bot.send_message(message.chat.id, "Выберите тип стикера!",
                     reply_markup=sticker_keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call: CallbackQuery) -> None:
    
    bot.answer_callback_query(call.id)
    
    if call.data == "photo":
        bot.w_file = "photo"
        bot.file_path = "static/w_photo.jpg"
        bot.send_message(call.message.chat.id, 
                         "Отправьте мне фото в формате .JPG!")
        bot.register_next_step_handler(call.message, _change_file, call.data)
        
    if call.data == "animation":
        bot.w_file = "animation"
        bot.file_path = "static/w_animation.gif"
        bot.send_message(call.message.chat.id, 
                         "Отправьте мне анимацию в формате .JPG!")
        bot.register_next_step_handler(call.message, _change_file, call.data)

    if call.data == "sticker":
        _sticker_type(call.message)
        
    if call.data == "text":
        bot.w_file = "text"
        bot.register_next_step_handler(call.message,
                                       w_handler.g_change_text)
    
    if call.data == "standard":
        bot.w_file = "sticker"
        bot.file_path = "static/w_sticker.webp"
        bot.send_message(call.message.chat.id, 
                         "Отправьте мне стикер в формате .WEBP")
        bot.register_next_step_handler(call.message, _change_file, call.data)

    if call.data == "animated":
        bot.w_file = "animated"
        bot.file_path = "static/w_anim_sticker.tgs"
        bot.send_message(call.message.chat.id, 
                         "Отправьте мне стикер в формате .TGS")
        bot.register_next_step_handler(call.message, _change_file, call.data)


def _send_done(call: CallbackQuery) -> None:
    
    with open("static/done.webp", "rb") as sticker:
        bot.send_sticker(call.message.chat.id, sticker)
        
def _change_file(message: Message, call_data: str) -> None:

    w_handler.write_file(bot, message, call_data,
                         bot.file_path, bot_token.token)


bot.polling(none_stop=True, interval=0)