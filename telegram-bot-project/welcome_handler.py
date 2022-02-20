# Standard Modules
from datetime import datetime as dt
from requests import get
from time import sleep


# Third Party Module
from telebot import TeleBot
from telebot.types import Message

    
def prep_cmd_msg(message: Message) -> str:
    
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
  
    
def write_file(bot: TeleBot, message: Message, call_data: str,
               file_path: str, token: str) -> None:
    
    files_url = f'https://api.telegram.org/file/bot{token}/'
    
    if call_data == "animation":
        file_info = bot.get_file(message.animation.file_id)
        file = get(files_url + file_info.file_path, allow_redirects=True)
        
        with open(file_path, "wb") as animation:
            animation.write(file.content)
            
    if call_data == "photo":
        file_info = bot.get_file(message.photo[-1].file_id)
        file = get(files_url + file_info.file_path, allow_redirects=True)
        
        with open(file_path, "wb") as photo:
            photo.write(file.content)
            
    if call_data == "standard" or call_data == "animated":
        file_info = bot.get_file(message.sticker.file_id)
        file = get(files_url + file_info.file_path, allow_redirects=True)
        
        with open(file_path, "wb") as sticker:
            sticker.write(file.content)
    
    _file_prep_msg(bot, call_data, message)


def _file_prep_msg(bot: TeleBot, call_data: str, message: Message) -> None:
    
    files = ['Анимация', 'Фото', 'Стикер', 'Анимированный стикер']
    ending = ['а', 'о', '', '']
    
    if call_data == "standard":
        bot.send_message(message.chat.id, f"{files[2]} загружается...")
        sleep(1.5)
        bot.send_message(message.chat.id, 
                         f"{files[2]} успешно установлен{ending[2]}!")
        
    if call_data == "animated":
        bot.send_message(message.chat.id, f"{files[3]} загружается...")
        sleep(1.5)
        bot.send_message(message.chat.id, 
                         f"{files[3]} успешно установлен{ending[2]}!")
        
    if call_data == "photo":
        bot.send_message(message.chat.id, f"{files[1]} загружается...")
        sleep(1.5)
        bot.send_message(message.chat.id, 
                         f"{files[1]} успешно установлен{ending[1]}!")
        
    if call_data == "animation":
        bot.send_message(message.chat.id, f"{files[0]} загружается...")
        sleep(1.5)
        bot.send_message(message.chat.id, 
                         f"{files[0]} успешно установлен{ending[0]}!")

        
def g_change_text(message: Message) -> None:
    
    new_text = _g_text_prep(message.text)
    start = f"[start]\n"
    stop = f"[/start]\n"
    
    with open("static/texts.txt", "r") as file:
        lines = file.readlines()
        
        start_index = lines.index(start)
        stop_index = lines.index(stop)
        
        remaining_lines = lines[stop_index:]
    
    new_text.insert(0, lines[start_index])
    new_text.insert(1, lines[start_index + 1])
    
    with open("static/texts.txt", "w") as file:
        file.writelines(new_text + remaining_lines)

        
def _g_text_prep(text: str) -> list:
    
    new_text = [line for line in text.split("\n")]
    
    for i in range(len(new_text)):
            new_text[i] += "\n"
    
    return new_text