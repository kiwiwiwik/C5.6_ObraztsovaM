
import telebot
from config import keys, TOKEN
from utils import ConversionException, MessageConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'What? into what? and how many?\n\nPlease input your request in following format:\n<currency that you want to exchange (singular)> \
<currency you want to receive (singular)> \
<amount of currency you are exchanging (number)>\n\nTo get the full list of available currencies: /currencies'
    bot.reply_to(message, text)

@bot.message_handler(commands=['currencies'])
def currencies(message: telebot.types.Message):
    text_list = ['Currencies list:'] + list(keys.keys())
    text = '\n'.join(tuple(text_list))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split()

        if len(values) != 3:
            raise ConversionException('Wrong input format - should be 3 items!')

        currency, base, amount = values
        result = MessageConverter.converter(currency, base, amount)
    except ConversionException as e:
        bot.reply_to(message, f'Failed to process request. \n{e}')
    except Exception as e:
        bot.reply_to(message, 'Failed to process request.')
    else:
        if int(amount) == 1:
            text = f'The price of {amount} {currency} in {base}s is {result}.'
        else:
            text = f'The price of {amount} {currency}s in {base}s is {result}.'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)