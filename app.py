import telebot
from telebot import types
from bs4 import BeautifulSoup
import requests
import os
import datetime

token = '5862200775:AAFWwsV8Or0CKtq6BMX8ka7gDZT7Y03nCJg'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    if os.path.isfile('bot_pogodi_pars' + '.txt'):
        print('')
    else:
        with open('bot_pogodi_pars' + '.txt', 'w', encoding='utf-8') as file:
            file.write('')


@bot.message_handler(commands=['choose_town'])
def town(message):
    try:
        with open('bot_pogodi_pars' + '.txt', 'r', encoding='utf-8') as file:
            l_file = file.readlines()
    except Exception:
        start(message)
        town(message)

    mark = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)

    if len(l_file) < 1:
        with open('bot_pogodi_pars' + '.txt', 'a', encoding='utf-8') as l_file:
            l_file.write('Kazan' + '\n')
            l_file.write('Manchester' + '\n')
            l_file.write('New-York' + '\n')
        with open('bot_pogodi_pars' + '.txt', 'r', encoding='utf-8') as file:
            l_file = file.readlines()
            l1 = []
            for i in l_file:
                i.replace('\n', '')
                l1.append(i)

            item1 = types.KeyboardButton(l_file[0])
            item2 = types.KeyboardButton(l_file[1])
            item3 = types.KeyboardButton(l_file[2])
            mark.add(item1, item2, item3)
    else:
        with open('bot_pogodi_pars' + '.txt', 'r', encoding='utf-8') as file:

            l_file = file.readlines()
            l2 = []
            for i in l_file:
                i.replace('\n', '')
                l2.append(i)
            for i in range(len(l2)):
                item = types.KeyboardButton(l2[i])
                mark.add(item)
    mess_1 = 'Назови город, в котором хочешь узнать погоду (на английском)'
    a = bot.send_message(message.chat.id, mess_1,
                         reply_markup=mark)
    bot.register_next_step_handler(a, get_city)


def get_city(message):
    global city
    city = message.text
    before_weather(message)


@bot.message_handler(commands=['dbdfdfvdfv'])
def before_weather(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
    item1 = types.KeyboardButton('Сегодня')
    item2 = types.KeyboardButton('Завтра')
    item3 = types.KeyboardButton("3-ий день")
    item4 = types.KeyboardButton("4-ый день")
    item5 = types.KeyboardButton("5-ый день")
    item6 = types.KeyboardButton("6-ой день")
    item7 = types.KeyboardButton("7-ой день")
    markup.add(item1, item2, item3, item4, item5, item6, item7)
    a = bot.send_message(message.chat.id, 'На какой день хотите узнать погоду?', reply_markup=markup)
    bot.register_next_step_handler(a, get_day)


def get_day(message):
    global day
    day = message.text
    weather(message)


@bot.message_handler(commands=['dbbdffbndfbdn'])
def weather(message):
    h(message)
    data_weather = []
    data_temp = []
    data_humidity = []
    data_wind = []
    data_temp_feel_like = []
    data_timely_1 = []
    data_timely_2 = []
    url = f'https://yandex.ru/pogoda/{city}/details/10-day-weather?via=ms#10'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    for i in range(28):
        data_temp.append(
            soup.find_all('td', class_="weather-table__body-cell weather-table__body-cell_type_daypart "
                                       "weather-table__body-cell_wrapper")[i].find('span',
                                                                                   class_="a11y-hidden").text.split(
                ', ')[1])

    for i in range(28):
        data_weather.append(soup.find_all('td', class_="weather-table__body-cell "
                                                       "weather-table__body-cell_type_condition")[i].text)

    for i in range(28):
        data_humidity.append(soup.find_all('td', class_="weather-table__body-cell "
                                                        "weather-table__body-cell_type_humidity")[i].text)

    for i in range(28):
        data_wind.append(
            soup.find_all('td', class_="weather-table__body-cell weather-table__body-cell_type_wind "
                                       "weather-table__body-cell_wrapper")[i].find('span',
                                                                                   class_="a11y-hidden").text.split(
                ', '))

    for i in range(28):
        data_temp_feel_like.append(soup.find_all('td', class_="weather-table__body-cell "
                                                              "weather-table__body-cell_type_feels-like")[
                                       i].find(
            'span',
            class_="a11y-hidden").text)

    for i in range(7):
        data_timely_1.append(
            soup.find_all('dl', class_="sunrise-sunset__description sunrise-sunset__description_value_sunrise")[i].find(
                'dd', class_="sunrise-sunset__value").text)

    for i in range(7):
        data_timely_2.append(soup.find_all('dl', class_="sunrise-sunset__description "
                                                        "sunrise-sunset__description_value_sunset")[i].find('dd',
                                                                                                            class_="sunrise-sunset__value").text)

    if day == 'Сегодня':
        bot.send_message(message.chat.id, f'{city}, {datetime.datetime.today().strftime("%d/%m/%Y")}')
        bot.send_message(message.chat.id, f'Восход солнца в {data_timely_1[0]}\n'
                                          f'Закат в {data_timely_2[0]}')
        bot.send_message(message.chat.id, 'Погода утром:')
        bot.send_message(message.chat.id,
                         f'Температура {data_temp[0]}, ощущается как {data_temp_feel_like[0]}\n'
                         f'{data_weather[0]}\n'
                         f'Влажность {data_humidity[0]}\n'
                         f'Ветер {data_wind[0][0]} м/c, {data_wind[0][1]}\n')
        bot.send_message(message.chat.id, 'Погода днём:')
        bot.send_message(message.chat.id,
                         f'Температура {data_temp[1]}, ощущается как {data_temp_feel_like[1]}\n'
                         f'{data_weather[1]}\n'
                         f'Влажность {data_humidity[1]}\n'
                         f'Ветер {data_wind[1][0]} м/c, {data_wind[1][1]}\n')
        bot.send_message(message.chat.id, 'Погода вечером:')
        bot.send_message(message.chat.id,
                         f'Температура {data_temp[2]}, ощущается как {data_temp_feel_like[2]}\n'
                         f'{data_weather[2]}\n'
                         f'Влажность {data_humidity[2]}\n'
                         f'Ветер {data_wind[2][0]} м/c, {data_wind[2][1]}\n')
        print(data_wind)
        bot.send_message(message.chat.id, 'Погода ночью:')
        bot.send_message(message.chat.id,
                         f'Температура {data_temp[3]}, ощущается как {data_temp_feel_like[3]}\n'
                         f'{data_weather[3]}\n'
                         f'Влажность {data_humidity[3]}\n'
                         f'Ветер {data_wind[3][0]} м/c, {data_wind[3][1]}\n')
    elif day == 'Завтра':
        a = datetime.datetime.today().strftime("%d/%m/%Y").split('/')
        a = [int(i) for i in a]
        a[0] += 1
        a = [str(i) for i in a]

        bot.send_message(message.chat.id, f'{city}, {"/".join(a)}')
        bot.send_message(message.chat.id, f'Восход солнца в {data_timely_1[1]}\n'
                                          f'Закат в {data_timely_2[1]}')
        bot.send_message(message.chat.id, 'Погода утром:')
        bot.send_message(message.chat.id,
                         f'Температура {data_temp[4]}, ощущается как {data_temp_feel_like[4]}\n'
                         f'{data_weather[4]}\n'
                         f'Влажность {data_humidity[4]}\n'
                         f'Ветер {data_wind[4][0]} м/c, {data_wind[4][1]}\n')
        bot.send_message(message.chat.id, 'Погода днём:')
        bot.send_message(message.chat.id,
                         f'Температура {data_temp[5]}, ощущается как {data_temp_feel_like[5]}\n'
                         f'{data_weather[5]}\n'
                         f'Влажность {data_humidity[5]}\n'
                         f'Ветер {data_wind[5][0]} м/c, {data_wind[5][1]}\n')
        bot.send_message(message.chat.id, 'Погода вечером:')
        bot.send_message(message.chat.id,
                         f'Температура {data_temp[6]}, ощущается как {data_temp_feel_like[6]}\n'
                         f'{data_weather[6]}\n'
                         f'Влажность {data_humidity[6]}\n'
                         f'Ветер {data_wind[6][0]} м/c, {data_wind[6][1]}\n')
        bot.send_message(message.chat.id, 'Погода ночью:')
        bot.send_message(message.chat.id,
                         f'Температура {data_temp[7]}, ощущается как {data_temp_feel_like[7]}\n'
                         f'{data_weather[7]}\n'
                         f'Влажность {data_humidity[7]}\n'
                         f'Ветер {data_wind[7][0]} м/c, {data_wind[7][1]}\n')
    elif day == '3-ий день':
        a = datetime.datetime.today().strftime("%d/%m/%Y").split('/')
        a = [int(i) for i in a]
        a[0] += 2
        a = [str(i) for i in a]
        bot.send_message(message.chat.id, f'{city}, {"/".join(a)}')
        bot.send_message(message.chat.id, f'Восход солнца в {data_timely_1[2]}\n'
                                          f'Закат в {data_timely_2[2]}')
        bot.send_message(message.chat.id, 'Погода утром:')
        bot.send_message(message.chat.id,
                         f'Температура {data_temp[8]}, ощущается как {data_temp_feel_like[8]}\n'
                         f'{data_weather[8]}\n'
                         f'Влажность {data_humidity[8]}\n'
                         f'Ветер {data_wind[8][0]} м/c, {data_wind[8][1]}\n')
        bot.send_message(message.chat.id, 'Погода днём:')
        bot.send_message(message.chat.id,
                         f'Температура {data_temp[9]}, ощущается как {data_temp_feel_like[9]}\n'
                         f'{data_weather[9]}\n'
                         f'Влажность {data_humidity[9]}\n'
                         f'Ветер {data_wind[9][0]} м/c, {data_wind[9][1]}\n')
        bot.send_message(message.chat.id, 'Погода вечером:')
        bot.send_message(message.chat.id,
                         f'Температура {data_temp[10]}, ощущается как {data_temp_feel_like[10]}\n'
                         f'{data_weather[10]}\n'
                         f'Влажность {data_humidity[10]}\n'
                         f'Ветер {data_wind[10][0]} м/c, {data_wind[10][1]}\n')
        bot.send_message(message.chat.id, 'Погода ночью:')
        bot.send_message(message.chat.id,
                         f'Температура {data_temp[11]}, ощущается как {data_temp_feel_like[11]}\n'
                         f'{data_weather[11]}\n'
                         f'Влажность {data_humidity[11]}\n'
                         f'Ветер {data_wind[11][0]} м/c, {data_wind[11][1]}\n')
    elif day == '4-ий день':
        a = datetime.datetime.today().strftime("%d/%m/%Y").split('/')
        a = [int(i) for i in a]
        a[0] += 3
        a = [str(i) for i in a]
        bot.send_message(message.chat.id, f'{city}, {"/".join(a)}')
        bot.send_message(message.chat.id, f'Восход солнца в {data_timely_1[3]}\n'
                                          f'Закат в {data_timely_2[3]}')
        bot.send_message(message.chat.id, 'Погода утром:')
        bot.send_message(message.chat.id,
                         f'Температура {data_temp[12]}, ощущается как {data_temp_feel_like[12]}\n'
                         f'{data_weather[12]}\n'
                         f'Влажность {data_humidity[12]}\n'
                         f'Ветер {data_wind[12][0]} м/c, {data_wind[12][1]}\n')
        bot.send_message(message.chat.id, 'Погода днём:')
        bot.send_message(message.chat.id,
                         f'Температура {data_temp[13]}, ощущается как {data_temp_feel_like[13]}\n'
                         f'{data_weather[13]}\n'
                         f'Влажность {data_humidity[13]}\n'
                         f'Ветер {data_wind[13][0]} м/c, {data_wind[13][1]}\n')
        bot.send_message(message.chat.id, 'Погода вечером:')
        bot.send_message(message.chat.id,
                         f'Температура {data_temp[14]}, ощущается как {data_temp_feel_like[14]}\n'
                         f'{data_weather[14]}\n'
                         f'Влажность {data_humidity[14]}\n'
                         f'Ветер {data_wind[14][0]} м/c, {data_wind[14][1]}\n')
        bot.send_message(message.chat.id, 'Погода ночью:')
        bot.send_message(message.chat.id,
                         f'Температура {data_temp[15]}, ощущается как {data_temp_feel_like[15]}\n'
                         f'{data_weather[15]}\n'
                         f'Влажность {data_humidity[15]}\n'
                         f'Ветер {data_wind[15][0]} м/c, {data_wind[15][1]}\n')
    elif day == '5-ый день':
        a = datetime.datetime.today().strftime("%d/%m/%Y").split('/')
        a = [int(i) for i in a]
        a[0] += 4
        print(a)
        if a[1] in [1, 3, 5, 7, 8, 10, 12] and a[0] > 26:
            a[1] += 1
            a[0] -= 31

        elif a[1] in [4, 6, 9, 11] and a[0] > 25:
            a[1] += 1
            a[0] -= 30

        elif a[1] == 2 and a[0] > 23:
            a[1] += 1
            a[0] -= 28
        a = [str(i) for i in a]
        bot.send_message(message.chat.id, f'{city}, {"/".join(a)}')
        bot.send_message(message.chat.id, f'Восход солнца в {data_timely_1[4]}\n'
                                          f'Закат в {data_timely_2[4]}')
        bot.send_message(message.chat.id, 'Погода утром:')
        bot.send_message(message.chat.id,
                         f'Температура {data_temp[16]}, ощущается как {data_temp_feel_like[16]}\n'
                         f'{data_weather[16]}\n'
                         f'Влажность {data_humidity[16]}\n'
                         f'Ветер {data_wind[16][0]} м/c, {data_wind[16][1]}\n')
        bot.send_message(message.chat.id, 'Погода днём:')
        bot.send_message(message.chat.id,
                         f'Температура {data_temp[17]}, ощущается как {data_temp_feel_like[17]}\n'
                         f'{data_weather[17]}\n'
                         f'Влажность {data_humidity[17]}\n'
                         f'Ветер {data_wind[17][0]} м/c, {data_wind[17][1]}\n')
        bot.send_message(message.chat.id, 'Погода вечером:')
        bot.send_message(message.chat.id,
                         f'Температура {data_temp[18]}, ощущается как {data_temp_feel_like[18]}\n'
                         f'{data_weather[18]}\n'
                         f'Влажность {data_humidity[18]}\n'
                         f'Ветер {data_wind[18][0]} м/c, {data_wind[18][1]}\n')
        bot.send_message(message.chat.id, 'Погода ночью:')
        bot.send_message(message.chat.id,
                         f'Температура {data_temp[19]}, ощущается как {data_temp_feel_like[19]}\n'
                         f'{data_weather[19]}\n'
                         f'Влажность {data_humidity[19]}\n'
                         f'Ветер {data_wind[19][0]} м/c, {data_wind[19][1]}\n')
    elif day == '6-ой день':
        a = datetime.datetime.today().strftime("%d/%m/%Y").split('/')
        a = [int(i) for i in a]
        a[0] += 5
        a = [str(i) for i in a]
        bot.send_message(message.chat.id, f'{city}, {"/".join(a)}')
        bot.send_message(message.chat.id, f'Восход солнца в {data_timely_1[5]}\n'
                                          f'Закат в {data_timely_2[5]}')
        bot.send_message(message.chat.id, 'Погода утром:')
        bot.send_message(message.chat.id,
                         f'Температура {data_temp[20]}, ощущается как {data_temp_feel_like[20]}\n'
                         f'{data_weather[20]}\n'
                         f'Влажность {data_humidity[20]}\n'
                         f'Ветер {data_wind[20][0]} м/c, {data_wind[20][1]}\n')
        bot.send_message(message.chat.id, 'Погода днём:')
        bot.send_message(message.chat.id,
                         f'Температура {data_temp[21]}, ощущается как {data_temp_feel_like[21]}\n'
                         f'{data_weather[21]}\n'
                         f'Влажность {data_humidity[21]}\n'
                         f'Ветер {data_wind[21][0]} м/c, {data_wind[21][1]}\n')
        bot.send_message(message.chat.id, 'Погода вечером:')
        bot.send_message(message.chat.id,
                         f'Температура {data_temp[22]}, ощущается как {data_temp_feel_like[22]}\n'
                         f'{data_weather[22]}\n'
                         f'Влажность {data_humidity[22]}\n'
                         f'Ветер {data_wind[22][0]} м/c, {data_wind[22][1]}\n')
        bot.send_message(message.chat.id, 'Погода ночью:')
        bot.send_message(message.chat.id,
                         f'Температура {data_temp[23]}, ощущается как {data_temp_feel_like[23]}\n'
                         f'{data_weather[23]}\n'
                         f'Влажность {data_humidity[23]}\n'
                         f'Ветер {data_wind[23][0]} м/c, {data_wind[23][1]}\n')
    elif day == '7-ой день':
        a = datetime.datetime.today().strftime("%d/%m/%Y").split('/')
        a = [int(i) for i in a]
        a[0] += 6
        a = [str(i) for i in a]
        bot.send_message(message.chat.id, f'{city}, {"/".join(a)}')
        bot.send_message(message.chat.id, f'Восход солнца в {data_timely_1[6]}\n'
                                          f'Закат в {data_timely_2[6]}')
        bot.send_message(message.chat.id, 'Погода утром:')
        bot.send_message(message.chat.id,
                         f'Температура {data_temp[24]}, ощущается как {data_temp_feel_like[24]}\n'
                         f'{data_weather[24]}\n'
                         f'Влажность {data_humidity[24]}\n'
                         f'Ветер {data_wind[24][0]} м/c, {data_wind[24][1]}\n')
        bot.send_message(message.chat.id, 'Погода днём:')
        bot.send_message(message.chat.id,
                         f'Температура {data_temp[25]}, ощущается как {data_temp_feel_like[25]}\n'
                         f'{data_weather[25]}\n'
                         f'Влажность {data_humidity[25]}\n'
                         f'Ветер {data_wind[25][0]} м/c, {data_wind[25][1]}\n')
        bot.send_message(message.chat.id, 'Погода вечером:')
        bot.send_message(message.chat.id,
                         f'Температура {data_temp[26]}, ощущается как {data_temp_feel_like[26]}\n'
                         f'{data_weather[26]}\n'
                         f'Влажность {data_humidity[26]}\n'
                         f'Ветер {data_wind[26][0]} м/c, {data_wind[26][1]}\n')
        bot.send_message(message.chat.id, 'Погода ночью:')
        bot.send_message(message.chat.id,
                         f'Температура {data_temp[27]}, ощущается как {data_temp_feel_like[27]}\n'
                         f'{data_weather[27]}\n'
                         f'Влажность {data_humidity[27]}\n'
                         f'Ветер {data_wind[27][0]} м/c, {data_wind[27][1]}\n')

def h(message):
    with open('bot_pogodi_pars' + '.txt', 'r', encoding='utf-8') as file:
        l_file = file.readlines()
        r_file = []
        for i in l_file:
            i.replace("\n", '')
            r_file.append(i)
    result1 = city + '\n'
    if result1 not in r_file:
        with open('bot_pogodi_pars' + '.txt', 'a', encoding='utf-8') as file:
            file.write(result1 + "\n")


bot.polling()
