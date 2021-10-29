from telebot import types
import telebot
import datetime
from gtts import gTTS
import os
import random
import requests
import json
import config
import importlib, sys


def load_exchangerate():
    return json.loads(requests.get(config.URL_exchangerate).text)


def load_weather(city):
    if city == '/StPetersburg':
        return json.loads(requests.get(config.URL_weather_with_data_StPetersburg).text)
    elif city == '/Moscow':
        return json.loads(requests.get(config.URL_weather_with_data_Moscow).text)
    elif city == '/London':
        return json.loads(requests.get(config.URL_weather_with_data_London).text)


def data_of_messages(message):
    data = open('data/data.txt', 'a')
    data.write('id : {0},first_name: {1},last_name: {2}, username: {3},text: {4}\n'.format(message.chat.id,
                                                                                           message.chat.first_name,
                                                                                           message.chat.last_name,
                                                                                           message.chat.username,
                                                                                           message.text))


offset = datetime.timezone(datetime.timedelta(hours=3))
now = datetime.datetime.now(offset)
URL_weather_without_data = 'https://www.metaweather.com/api/location/'
URL_weather_with_data_Moscow = URL_weather_without_data + '2122265/' + str(now.year) + '/'\
                               + str(now.month) + '/' + str(now.day)
URL_weather_with_data_StPetersburg = URL_weather_without_data + '2123260/' + str(now.year) + '/'\
                               + str(now.month) + '/' + str(now.day)
URL_weather_with_data_London = URL_weather_without_data + '44418/' + str(now.year) + '/'\
                               + str(now.month) + '/' + str(now.day)
URL_exchangerate = 'https://www.cbr-xml-daily.ru/daily_json.js'
BOT_TOKEN = "1214104407:AAH-TV6IR0kEt6rmOqAmNtlPOhqP1g0KhhA"
admin_id = 412662627
offset = datetime.timezone(datetime.timedelta(hours=3))
now = datetime.datetime.now(offset)
audio_message_toggle = False
bot = telebot.TeleBot(BOT_TOKEN)
markup_help = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_help.add(types.KeyboardButton('/help'))
bot.send_message(admin_id, text='Бот запущен')
with open('data/lesson{0}.json'.format(now.weekday()), 'r') as file_now:
    timetable = json.loads(str(file_now.read()))
    with open('data/lesson{0}_today.json'.format(now.weekday()), 'r') as file_today:
        timetable_today = json.loads(str(file_today.read()))

@bot.message_handler(commands=['time'])
def time_commabd(message):
    importlib.reload(datetime)
    bot.send_message(message.chat.id, text=(str(now.hour) + ':' + str(now.minute) + ':' + str(now.second)))


@bot.message_handler(commands=['audio'])
def audio_command(message):
    data_of_messages(message)
    global audio_message_toggle
    audio_markup = types.ReplyKeyboardRemove()
    audio_message_toggle = True
    bot.send_message(message.chat.id, text="Напиши,что хочешь перевести из текста"
                                           " в речь(поддерживаемые языки:'ru','en')",
                     reply_markup=audio_markup)


@bot.message_handler(commands=['start'])
def start_command(message):
    data_of_messages(message)
    bot.send_message(message.chat.id, text="Напиши /help")


@bot.message_handler(commands=['help', 'Help', 'HELP'])
def help_command(message):
    data_of_messages(message)
    bot.send_chat_action(message.chat.id, 'typing')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.InlineKeyboardButton('/exchangerate'), types.InlineKeyboardButton('/weather'),
                 types.InlineKeyboardButton('/lesson_today'))
    keyboard.add(types.InlineKeyboardButton('/connect'), types.InlineKeyboardButton('/audio'),
                 types.InlineKeyboardButton('/lesson_next'), types.InlineKeyboardButton('/mood'))
    bot.send_message(message.chat.id, text="Я пока что умею:"
                                           "\nРасписание на сегодня(/lesson_today)"
                                           "\nКакой следующий предмет(/lesson_next)"
                                           "\nКурс валют(/exchangerate);"
                                           "\nПогода(/weather)"
                                           "\nПеревод текста в аудио(/audio)"
                                           "\nСвязь с Артуром(/connect)"
                                           "\nУзнать какой я сегодня(/mood)",
                     reply_markup=keyboard)


@bot.message_handler(commands=['exchangerate'])
def exchange_command(message):
    data_of_messages(message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('/USD'), types.KeyboardButton('/EUR'), types.KeyboardButton('/UAH'))
    bot.send_message(message.chat.id, 'Жмякни:', reply_markup=markup)


@bot.message_handler(commands=['weather'])
def weather_command(message):
    data_of_messages(message)
    bot.send_chat_action(message.chat.id, 'typing')
    weather_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itemMoscow = types.KeyboardButton('/Moscow')
    itemStPetersburg = types.KeyboardButton('/StPetersburg')
    itemLondon = types.KeyboardButton('/London')
    weather_markup.add(itemMoscow, itemStPetersburg, itemLondon)
    bot.send_message(message.chat.id, 'Жмякни:', reply_markup=weather_markup)


@bot.message_handler(commands=['Moscow', 'StPetersburg', 'London'])
def cities_command(message):
    data_of_messages(message)
    bot.send_chat_action(message.chat.id, 'typing')
    temp = int(load_weather(message.text)[0]['the_temp'])
    air_pressure = int(load_weather(message.text)[0]['air_pressure'])
    wind_direction_compass = load_weather(message.text)[0]['wind_direction_compass']
    wind_speed = int(load_weather(message.text)[0]['wind_speed'])
    humidity = int(int(load_weather(message.text)[0]['humidity']))
    weather_state_abbr = load_weather(message.text)[0]['weather_state_abbr']
    weather_state_name = load_weather(message.text)[0]['weather_state_name']
    with open('images/{}.jpg'.format(weather_state_abbr), 'rb') as file:
        data = file.read()
    bot.send_photo(message.chat.id, data)
    weather = 'Погода in {0} сегодня:' \
              '\n{1}' \
              '\n{2}°C - Средняя Температура;' \
              '\n{3} - Направление ветра;' \
              '\n{4} м/с - Скорость ветра;' \
              '\n{5}mb - Давление;' \
              '\n{6}% - Влажность.'.format(message.text[1:],
                                           weather_state_name,
                                           temp,
                                           wind_direction_compass,
                                           wind_speed,
                                           air_pressure,
                                           humidity)
    bot.send_message(message.chat.id, text=weather, reply_markup=markup_help)


@bot.message_handler(commands=['mood'])
def mood_command(message):
    data_of_messages(message)
    with open('images/mem{}.jpg'.format(random.randint(1, 10)), 'rb') as file:
        mem = file.read()
    bot.send_message(message.chat.id, text='Сегодня ты:')
    bot.send_photo(message.chat.id, photo=mem, reply_markup=markup_help)


@bot.message_handler(commands=['USD', 'EUR', 'UAH'])
def valute_command(message):
    data_of_messages(message)
    bot.send_chat_action(message.chat.id, 'typing')
    exchange_data = load_exchangerate()["Date"][:10]
    exchange_sell = load_exchangerate()["Valute"]["{}".format(message.text[1:])]["Value"]
    exchange_name = load_exchangerate()["Valute"]["{}".format(message.text[1:])]["Name"]
    exchange = 'Дата: {0}' \
               '\nВалюта: {1}' \
               '\nСтоимость в рублях: {2}'.format(exchange_data, exchange_name, exchange_sell)
    bot.send_message(message.chat.id, text=exchange, reply_markup=markup_help)


@bot.message_handler(commands=['connect'])
def connect_message(message):
    data_of_messages(message)
    bot.send_message(message.chat.id, text='https://t.me/ArLazD', reply_markup=markup_help)


@bot.message_handler(commands=['lesson_next'])
def lesson_next(message):
    data_of_messages(message)
    lesson = 0
    if (0, 0) < (now.hour, now.minute) <= (10, 20):
        lesson = 1
    elif (10, 20) < (now.hour, now.minute) <= (12, 5):
        lesson = 2
    elif (12, 5) < (now.hour, now.minute) <= (13, 50):
        lesson = 3
    elif (13, 50) < (now.hour, now.minute) <= (16, 10):
        lesson = 4
    elif (16, 10) < (now.hour, now.minute) <= (17, 55):
        lesson = 5
    if now.weekday() == 6:
        lesson = 0
    if lesson == 0:
        output = 'На сегодня пар больше нет. Первая пара завтра:\n' \
                     'Предмет: {0}\n' \
                     'Начало пары: {1}\n' \
                     'Конец пары: {2}\n' \
                     'Преподователь: {3}\n' \
                     'Кабинет: {4}\n'.format(timetable["{}_lesson".format(lesson)]["lesson"],
                                             timetable["{}_lesson".format(lesson)]["start_time"],
                                             timetable["{}_lesson".format(lesson)]["end_time"],
                                             timetable["{}_lesson".format(lesson)]["prepod"],
                                             timetable["{}_lesson".format(lesson)]["cabinet"])
    else:
        output = 'Предмет: {0}\n' \
                     'Начало пары: {1}\n' \
                     'Конец пары: {2}\n' \
                     'Преподователь: {3}\n' \
                     'Кабинет: {4}\n'.format(timetable["{}_lesson".format(lesson)]["lesson"],
                                             timetable["{}_lesson".format(lesson)]["start_time"],
                                             timetable["{}_lesson".format(lesson)]["end_time"],
                                             timetable["{}_lesson".format(lesson)]["prepod"],
                                             timetable["{}_lesson".format(lesson)]["cabinet"])

    bot.send_message(message.chat.id, text=output, reply_markup=markup_help)


@bot.message_handler(commands=['lesson_today'])
def lesson_today(message):
    data_of_messages(message)

    for lesson in range(1, 6):
        output = '{5} Предмет: {0}\n' \
                 'Начало пары: {1}\n' \
                 'Конец пары: {2}\n' \
                 'Преподователь: {3}\n' \
                 'Кабинет: {4}\n'.format(timetable_today["{}_lesson".format(lesson)]["lesson"],
                                         timetable_today["{}_lesson".format(lesson)]["start_time"],
                                         timetable_today["{}_lesson".format(lesson)]["end_time"],
                                         timetable_today["{}_lesson".format(lesson)]["prepod"],
                                         timetable_today["{}_lesson".format(lesson)]["cabinet"],
                                         lesson)
        bot.send_message(message.chat.id, text=output, reply_markup=markup_help)


@bot.message_handler(content_types='text')
def audio_answer(message):
    data_of_messages(message)
    global audio_message_toggle
    number = 0
    lang = 'ru'
    if audio_message_toggle:
        if message.text[number] == ' ':
            while message.text[number] == ' ':
                number += 1
        if 'a' <= message.text[number] <= 'z':
            lang = 'en'
        elif 'а' <= message.text[number] <= 'я':
            lang = 'ru'
        audio = gTTS(text=message.text, lang=lang, slow=False)
        audio.save('{}.mp3'.format(message.text[:10]))
        audio_completed = open('{}.mp3'.format(message.text[:10]), 'rb')
        bot.send_audio(message.chat.id, audio_completed, performer='@arlaz_bot', title=message.text[:10],
                       reply_markup=markup_help)
        os.remove('{}.mp3'.format(message.text[:10]))
        audio_message_toggle = False
    else:
        bot.send_message(message.chat.id, text='Я твоя не понимать, напиши /help', reply_markup=markup_help)


bot.polling(none_stop=True, interval=0)
