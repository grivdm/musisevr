from Search import get_output
import telebot
import cred

bot = telebot.TeleBot(cred.TOKEN)


@bot.message_handler(commands=['start'])
def welcome_start(message):

    bot.send_message(message.from_user.id, f'Hi, {message.from_user.first_name}. \n'
                                                '\nHow to use it:'
                                                '\nType to the chat:'
                                                '\nArtist\'s name - Name of song '
                                                '\nor \nArtist\'s name'
                                                '\nYou can send any song or artist link (Spotify or Yandex.Music) as well')




@bot.message_handler(content_types=["text"])
def get_msg(message):
    spotyRep, yandRep, ytmRep = get_output(message.text)
    markup = telebot.types.InlineKeyboardMarkup()
    if spotyRep is not None:
        markup.add(telebot.types.InlineKeyboardButton(text='spotify', url=spotyRep['urls']['spotify']))
    if yandRep is not None:
        markup.add(telebot.types.InlineKeyboardButton(text='yandex', url=yandRep))

    bot.send_message(message.chat.id, "Look what I've found: \n" + ytmRep, reply_markup=markup)


if __name__ == '__main__':
    bot.infinity_polling()
