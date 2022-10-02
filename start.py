from typing import Dict

import telebot
import random
import os
import wikipedia
import re
from telebot import types

bot = telebot.TeleBot('5511590837:AAGvJNJhUP3eFz7_rxnq-2QiwtVKdV45KE4')

wikipedia.set_lang("ru")


def getwiki(s):
    try:
        ny = wikipedia.page(s)
        wikitext = ny.content[:1000]
        wikimas = wikitext.split('.')
        wikimas = wikimas[:-1]
        wikitext2 = ''
        for x in wikimas:
            if not ('==' in x):
                if (len((x.strip())) > 3):
                    wikitext2 = wikitext2 + x + '.'
            else:
                break
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\{[^\{\}]*\}', '', wikitext2)
        return wikitext2
    except Exception as e:
        return 'В энциклопедии нет информации об этом'


members_dict = {
    1: 'Батышкин Владислав',
    8: 'Крайнов Павел',
    9: 'Крыжановский Владислав',
    11: 'Лукьянов Егор',
    18: 'Трохачев Степан',
    13: 'Положий Артём'
}

person_name: str = ''
person_id = 0
variants_list: dict[int, str] = {
    1: 'все ли геи - геи',
    2: 'как понять что перед тобой человек который любит философию',
    3: 'все ли так плохо как кажется',
    4: 'докажи существование бога 0 разрых способов',
    5: 'сколько существует гендеров?'
}


@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.clear_step_handler(m)

    bot.send_message(m.chat.id, 'Давай сделаем это!)')
    bot.send_message(m.chat.id, 'Что бы посмотреть что я умею, напиши /help')
    bot.register_next_step_handler(m, help)


@bot.message_handler(content_types=['text'])
def help(m, res=False):
    if m.text == '/help':
        bot.send_message(m.chat.id, 'Привет!')
    bot.send_message(m.chat.id, 'Я могу сгенериновать тему доклада, для этого напиши /reg')
    bot.send_message(m.chat.id, 'Я могу привести факт из википедии, для этого напиши /wiki')
    bot.register_next_step_handler(m, parse)


@bot.message_handler(content_types=['text'])
def parse(m, res=False):
    if m.text == '/reg':
        bot.register_next_step_handler(m, base)
    elif m.text == '/wiki':
        bot.send_message(m.chat.id, 'Отправь мне любое слово, и я найду его значение на wiki')
        bot.register_next_step_handler(m, wiki)
    else:
        bot.send_message(m.chat.id, 'Я пока этого не умею, напиши /help и я покажу что могу ')
        bot.register_next_step_handler(m, help)


@bot.message_handler(content_types=['text'])
def wiki(m):
    bot.send_message(m.chat.id, getwiki(m.text))
    bot.send_message(m.chat.id, 'посмотри что ещё я могу, напиши /help')
    bot.send_message(m, 'help')


@bot.message_handler(content_types=['text'])
def base(message, res=False):
    global person_id
    person_id = 0
    if message.text == '/reg':
        bot.send_message(message.chat.id, 'Введи свой номер в группе')
        bot.register_next_step_handler(message, registrate_user)
    else:
        bot.send_message(message.chat.id, 'Снова привет!')
        bot.send_message(message.chat.id, 'Напиши /reg')


def registrate_user(message):
    global person_id
    while person_id == 0:
        try:
            person_id = int(message.text)
            if person_id not in list(members_dict):
                bot.send_message(message.chat.id, 'тебя пока не добавили, ожидай обновления!')
                return
        except Exception:
            bot.send_message(message.chat.id, 'Введи свой номер цифрами')
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
        keyboard.add(key_yes)
        key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_no)
        bot.send_message(message.chat.id, text=f"Привет, тебя правда зовут {members_dict.get(person_id)}? ",
                         reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, f"Отлично, {members_dict.get(person_id)}, сейчас я назову твою тему")
        bot.send_message(call.message.chat.id, f'Твоя тема: {variants_list.get(random.choice(list(variants_list)))}')
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Сори ты без темы')
    bot.send_message(call.message.chat.id, 'Если надоест, напиши /stop ')


@bot.message_handler(commands=['stop'])
def stop_command(message):
    bot.send_message(message.chat.id, 'Завершаю')
    bot.stop_polling()


@bot.message_handler(commands=['restart'])
def restart_command(message):
    bot.send_message(message.chat.id, 'Перезапуск бота')

    bot.stop_bot()
    quit(os.system('python3 ~/PycharmProjects/reportsBot/reportBot/start.py'))


bot.polling(none_stop=False, interval=0)
