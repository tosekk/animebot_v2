#Third Party Modules
from telebot import TeleBot
from telebot.types import Message


#Local Modules
import bot_token


bot = TeleBot(bot_token.token)


@bot.message_handler(commands=["start"])
def welcome(message: Message) -> None:
    with open("static/w_animation.gif", "rb") as animation:
        bot.send_animation(message.chat.id, animation)
    
    msg_text = ""
    
    with open("static/texts.txt", "r", encoding="utf-8") as welcome_text:
        lines = welcome_text.readlines()
        
        start = f"[{message.text[1:]}]"
        stop = f"[{message.text}]"
        
        for index in range(len(lines)):
            if start in lines[index] or stop in lines[index]:
                continue
            msg_text += lines[index]
    
    bot.send_message(message.chat.id, msg_text)


bot.polling(none_stop=True, interval=0)