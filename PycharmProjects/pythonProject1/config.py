import datetime
offset = datetime.timezone(datetime.timedelta(hours=3))
now = datetime.datetime.now(offset)
URL_weather_without_data = 'https://www.metaweather.com/api/location/'
URL_weather_with_data_Moscow = URL_weather_without_data + '2122265/' +  str(now.year) + '/'\
                               + str(now.month) + '/' + str(now.day)
URL_weather_with_data_StPetersburg = URL_weather_without_data + '2123260/' +  str(now.year) + '/'\
                               + str(now.month) + '/' + str(now.day)
URL_weather_with_data_London = URL_weather_without_data + '44418/' +  str(now.year) + '/'\
                               + str(now.month) + '/' + str(now.day)
URL_exchangerate = 'https://www.cbr-xml-daily.ru/daily_json.js'
BOT_TOKEN = "1214104407:AAH-TV6IR0kEt6rmOqAmNtlPOhqP1g0KhhA"
admin_id = 412662627