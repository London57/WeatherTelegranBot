import requests
from bs4 import BeautifulSoup


class DataParserMixin:
    def __init__(self, city):
        self.city = city
        self.soup = BeautifulSoup(requests.get(f'https://pogoda.mail.ru/prognoz/{city}/').text, 'lxml')

    async def get_date(self, day, data={}):
        if day == 0:
            data['date'] = 'Cегодня'
        else:
            data['date'] = self.soup.find_all('div', class_="day day_index")[day-1].find('div',
                                                                class_="day__date").text
        return data

    async def get_temperature(self, day, data={}):
        if day == 0:
            data['day_temp'] = self.soup.find_all('div', class_='information__content__period__temperature')[0].text
            data['night_temp'] = self.soup.find_all('div', class_='information__content__period__temperature')[1].text
        else:
            temp = self.soup.find_all('div', class_="day day_index")[day-1].find('div',
                                                                    class_="day__temperature").text.replace('\n', '').replace('\t', '')
            data['day_temp'] = temp[:4]
            data['night_temp'] = temp[4:]
        return data

    async def get_description(self, day, data={}):
        if day == 0:
            data['description'] = self.soup.find_all('div', class_="information__content__additional information__content__additional_first")[0]\
                                            .find('div', class_='information__content__additional__item').text.replace('\t', '')\
                                                                                                               .replace('\n', '')
        else:
            data['description'] = self.soup.find_all('div', class_="day day_index")[day-1].find('div',
                                                                class_="day__description").text
        return data
        
    async def get_humidity(self, day, data={}):
        if day == 0:
            data['humidity'] = self.soup.find('div', class_='information__content__additional information__content__additional_second')\
                                      .find_all('div', class_='information__content__additional__item')[1]\
                                      .find('span').text[:4].replace('\t', '')\
                                                            .replace('\n', '')
        else:
            data['humidity'] = self.soup.find_all('div', class_="day day_index")[day-1]\
                                    .find_all('div', class_="day__additional")[1].text.replace('\n', '')\
                                                                                       .replace('\t', '')
        return data

    async def get_breeze(self, day, data={}):
        if day == 0:
            data['breeze'] = self.soup.find('div', class_='information__content__additional information__content__additional_second')\
                                      .find_all('div', class_='information__content__additional__item')[2]\
                                      .find('span').text[:6].replace('\t', '')\
                                                         .replace('\n', '')
        else:
            data['breeze'] = self.soup.find_all('div', class_="day day_index")[day-1].find_all('div',
                                                                class_="day__additional")[2].text.replace('\n', '')\
                                                                                                  .replace('\t', '')
        return data

    async def get_precipitation(self, day, data={}):
        data['precipitation'] = self.soup.find_all('div', class_="day day_index")[day-1].find_all('div',
                                                                class_="day__additional")[4].text.replace('\n', '').replace('\t', '')
        return data

    async def get_functions_list(self):
        return [self.get_date, self.get_temperature, self.get_breeze, self.get_description, self.get_humidity, self.get_description, self.get_precipitation] 