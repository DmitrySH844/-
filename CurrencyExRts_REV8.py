import telebot
from telebot import types

from myconfig import *
from myextensions import Converter_ru, Converter_en, APIException

def create_markup_en(base = None):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    buttons = []
    for val in exchanges_en.keys():
        if val != base:
            buttons.append(types.KeyboardButton(val))

    markup.add(*buttons)
    return markup

def create_markup_ru(base = None):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    buttons = []
    for val in exchanges_ru.keys():
        if val != base:
            buttons.append(types.KeyboardButton(val))

    markup.add(*buttons)                                          
    return markup
    
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands = ['start'])
def start(message: telebot.types.Message):
    text = 'Добрый день!\nВыберите язык!\nHello!\nSelect language!'
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('🇷🇺', callback_data='question_1')
    btn2 = types.InlineKeyboardButton('🇺🇸', callback_data='question_2')
    markup.add(btn1, btn2)   
    bot.send_message(message.chat.id, text, reply_markup=markup)
    
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == 'question_2' or call.data == 'question_6':
            msg = bot.send_message(call.message.chat.id, 'Your language is English\nSelect the currency to convert from:', reply_markup = create_markup_en())
            lang_en()
            bot.register_next_step_handler(msg, lang_en.base_handler)
        if call.data == 'question_1' or call.data == 'question_4':
            msg = bot.send_message(call.message.chat.id, 'Ваш язык - Русский\nВыберите валюту, из которой конвертировать:', reply_markup = create_markup_ru())
            lang_ru()
            bot.register_next_step_handler(msg, lang_ru.base_handler)
        if call.data == 'question_3':
            msg = bot.send_message(call.message.chat.id, 'Select the currency to convert from:', reply_markup = create_markup_en())
            bot.register_next_step_handler(msg, lang_en.base_handler)
        if call.data == 'question_5':
            msg = bot.send_message(call.message.chat.id, 'Выберите валюту, из которой конвертировать:', reply_markup = create_markup_ru())
            bot.register_next_step_handler(msg, lang_ru.base_handler)
              
class lang_en:
    def base_handler(message: telebot.types.Message):
        try:
            base = message.text.strip()
        except ValueError as e:
            bot.send_message(message.chat.id, 'Invalid number of parameters!')
            bot.register_next_step_handler(message, lang_en.sym_handler)
        else:
            text = 'Select the currency to convert to:'
            bot.send_message(message.chat.id, text, reply_markup = create_markup_en())
            bot.register_next_step_handler(message, lang_en.sym_handler, base)
    
    def sym_handler(message: telebot.types.Message, base):
        try:
            sym = message.text.strip()
        except ValueError as e:
            bot.send_message(message.chat.id, 'Invalid number of parameters!')
            bot.register_next_step_handler(message, lang_en.sym_handler, sym)
        else:
            text = 'Select the amount of currency to be converted:'
            bot.send_message(message.chat.id, text)
            bot.register_next_step_handler(message, lang_en.amount_handler, base, sym)

    def amount_handler(message: telebot.types.Message, base, sym):
        amount = message.text.strip()
        try:
            new_price = Converter_en.get_price(base, sym, amount)
        except APIException as e:
            bot.send_message(message.chat.id, f"Conversion error: \n{e}\nPlease enter correct currency!")
            bot.register_next_step_handler(message, lang_en.sym_handler, base)
        else:
            text = f"Price {amount} {base} in {sym} : {new_price}"
            bot.send_message(message.chat.id, text)
            text2 = 'Do you want to continue or change the language?'
            markup = types.InlineKeyboardMarkup(row_width=2)
            btn3 = types.InlineKeyboardButton('Continue', callback_data='question_3')
            btn4 = types.InlineKeyboardButton('Change the language', callback_data='question_4')
            markup.add(btn3, btn4)   
            bot.send_message(message.chat.id, text2, reply_markup=markup)
            
    @bot.message_handler(content_types=['text'])
    def converter(message: telebot.types.Message):
        try:
            base, sym, amount = message.text.split(' ')
        except ValueError as e:
            bot.send_message(message.chat.id, 'Invalid number of parameters!')

        try:
            new_price = Converter_en.get_price(base, sym, amount)
            bot.send_message(message.chat.id, f"Price {amount} {base} in {sym} : {new_price}")
        except APIException as e:
            bot.send_message(message.chat.id, f"Command error:\n{e}")

class lang_ru:
    def base_handler(message: telebot.types.Message):
        base = message.text.strip()
        text = 'Выберите валюту, в которую конвертировать:'
        bot.send_message(message.chat.id, text, reply_markup = create_markup_ru())
        bot.register_next_step_handler(message, lang_ru.sym_handler, base)
    

    def sym_handler(message: telebot.types.Message, base):
        sym = message.text.strip()
        text = 'Выберите количество конвертируемой валюты:'
        bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(message, lang_ru.amount_handler, base, sym)

    def amount_handler(message: telebot.types.Message, base, sym):
        amount = message.text.strip()
        try:
            new_price = Converter_ru.get_price(base, sym, amount)
        except APIException as e:
            bot.send_message(message.chat.id, f"Ошибка конвертации: \n{e}\nПожалуйста, введите корректную валюту!")
            bot.register_next_step_handler(message, lang_ru.sym_handler, base)
        else:
            text = f"Цена {amount} {base} в {sym} : {new_price}"
            bot.send_message(message.chat.id, text)
            text2 = 'Вы хотите продолжить или изменить язык?'
            markup = types.InlineKeyboardMarkup(row_width=2)
            btn5 = types.InlineKeyboardButton('Продолжить', callback_data='question_5')
            btn6 = types.InlineKeyboardButton('Изменить язык', callback_data='question_6')
            markup.add(btn5, btn6)   
            bot.send_message(message.chat.id, text2, reply_markup=markup)
    
    @bot.message_handler(content_types=['text'])
    def converter(message: telebot.types.Message):
        try:
            base, sym, amount = message.text.split(' ')
        except ValueError as e:
            bot.send_message(message.chat.id, 'Неверное количество параметров!')

        try:
            new_price = Converter_ru.get_price(base, sym, amount)
            bot.send_message(message.chat.id, f"Цена {amount} {base} в {sym} : {new_price}")
        except APIException as e:
            bot.send_message(message.chat.id, f"Ошибка в команде:\n{e}")
    
bot.polling()
