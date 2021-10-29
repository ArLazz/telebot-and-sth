import requests
import json
import config


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
