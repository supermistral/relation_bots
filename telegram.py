import telebot, config, threading
from interaction_sql import InteractionSQL


bot = telebot.TeleBot(config.tokenTelegram)

sql = InteractionSQL()


@bot.message_handler(commands=['start'])
def start_message(message):
    mess = sql.start_message(message.chat.id)
    bot.send_message(message.chat.id, mess)

@bot.message_handler(commands=['user'])
def update_user(message):
    mess = sql.update_user(message.chat.id, message.text[6:])
    bot.send_message(message.chat.id, mess)

@bot.message_handler(content_types=['text'])
def get_text_message(message):
    sql.get_text_message(message.chat.id, message.text)

def process():
    sql.process(bot.send_message)

def main():
    try:
        thread = threading.Thread(target=process)
        thread.start()
        bot.infinity_polling()
    except Exception as err:
        print(err)
        print()

if __name__ == "__main__":
    main()