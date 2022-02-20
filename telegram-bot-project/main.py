# Standard Modules
from datetime import datetime as dt


# Third Party Modules
from telebot import TeleBot
from telebot.types import (CallbackQuery, InlineKeyboardButton, 
                           InlineKeyboardMarkup, Message)



# Local Modules
import bot_token


# Bot Initialization
bot = TeleBot(bot_token.token)


# Variables
bot.w_file = "animation"


@bot.message_handler(commands=["start"])
def welcome(message: Message) -> None:
    
    file_path = _choose_welcome_file()
    
    if bot.w_file != "text":
        with open(file_path, "rb") as file:
            if bot.w_file == "photo":
                bot.send_photo(message.chat.id, file)
            elif bot.w_file == "sticker" or bot.w_file == "animated":
                bot.send_sticker(message.chat.id, file)
            elif bot.w_file == "animation":
                bot.send_animation(message.chat.id, file)
                
    msg_text = _prep_cmd_msg(message)
    
    bot.send_message(message.chat.id, msg_text)


def _choose_welcome_file() -> str:
    
    if bot.w_file == "photo":
        file_path = "static/w_photo.jpg"
    elif bot.w_file == "sticker":
        file_path = "static/w_sticker.webp"
    elif bot.w_file == "animated":
        file_path = "static/w_anim_sticker.tgs"
    elif bot.w_file == "animation":
        file_path = "static/w_animation.gif"
    else:
        file_path = ""
    
    return file_path
    

@bot.message_handler(["help"])
def help(message: Message) -> None:
    
    msg_text = _prep_cmd_msg(message)
    
    bot.send_message(message.chat.id, msg_text)


def _prep_cmd_msg(message: Message) -> str:
    
    msg_text = ""
    
    with open("static/texts.txt", "r", encoding="utf-8") as welcome_text:
        lines = welcome_text.readlines()
        
        start = f"[{message.text[1:]}]\n"
        stop = f"[{message.text}]\n"
        
        start_index = lines.index(start)
        stop_index = lines.index(stop)
        
        for index in range(start_index, stop_index):
            if start in lines[index] or stop in lines[index]:
                continue
            elif stop in lines[index]:
                break
            if "Доброе утро!" in lines[index]:
                time_index = _check_time()
                greetings = [greeting for greeting in lines[index].split("!")]
                lines[index] = greetings[time_index] + "!\n"
            msg_text += lines[index]
            
    return msg_text


def _check_time() -> int:
    
    curr_time = dt.now()
    curr_hour = curr_time.hour
    
    if 4 <= curr_hour < 12:
        return 0
    elif 12 <= curr_hour < 18:
        return 1
    elif 18 <= curr_hour < 22:
        return 2
    elif 22 <= curr_hour < 0 or 0 <= curr_hour < 4:
        return 3


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
    
    config_keyboard.add(photo_key, animation_key, sticker_key, text_key)
    
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
        _send_done(call)
    if call.data == "animation":
        bot.w_file = "animation"
        _send_done(call)
    if call.data == "sticker":
        _sticker_type(call.message)
    if call.data == "text":
        bot.w_file = "text"
        _send_done(call)
    
    if call.data == "standard":
        bot.w_file = "sticker"
        _send_done(call)
    if call.data == "animated":
        bot.w_file = "animated"
        _send_done(call)


def _send_done(call: CallbackQuery) -> None:
    
    with open("static/done.webp", "rb") as sticker:
        bot.send_sticker(call.message.chat.id, sticker)


bot.polling(none_stop=True, interval=0)