
from bs4 import BeautifulSoup
import requests, asyncio

class Parser:

    def __init__(self, city):
        self.city = city
        self.soup = BeautifulSoup(requests.get(f'https://pogoda.mail.ru/prognoz/{city}/').text, 'lxml')
    
    async def dates_to_keyboard(self, day):
        print(day)
        if day == 0:
            data = 'Сегодня'
        else:
            data = self.soup.find_all('div', class_="day day_index")[day-1].find('div',
                                                             class_="day__date").text
        
        return data

    async def get_date(self, day, data={}):
        if day == 0:
            data['data'] = 'Cегодня'
        else:
            data['date'] = self.soup.find_all('div', class_="day day_index")[day-1].find('div',
                                                                class_="day__date").text
        return data

    async def get_temperature(self, day, data={}):
        print('xjjj')
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
                                      .find('span').text[:5].replace('\t', '')\
                                                            .replace('\n', '')
        else:
            data['humidity'] = self.soup.find_all('div', class_="day day_index")[day-1]\
                                    .find_all('div', class_="day__additional")[1].text.replace('\n', '')\
                                                                                       .replace('\t', '')
        return data

    async def get_breeze(self, day, data={}):
        data['breeze'] = self.soup.find_all('div', class_="day day_index")[day-1].find_all('div',
                                                                class_="day__additional")[2].text.replace('\n', '').replace('\t', '')
        return data

    async def get_precipitation(self, day, data={}):
        data['precipitation'] = self.soup.find_all('div', class_="day day_index")[day-1].find_all('div',
                                                                class_="day__additional")[4].text.replace('\n', '').replace('\t', '')
        return data
    

    async def get_functions_list(self):
        return [self.get_date, self.get_temperature, self.get_breeze, self.get_description, self.get_humidity, self.get_description, self.get_precipitation] 


    async def get_result_data(self, day):
        tasks, result_dict = [], {}
        function_list = await asyncio.create_task(self.get_functions_list())
        for index in range(len(function_list)):
            tasks.append(asyncio.create_task(function_list[index](day)))
        for j in tasks:
            result_dict.update(await j)
        return result_dict


    async def get_days_dict_and_list(self):
        days_list, tasks = [], []
        for i in range(9):
            tasks.append(asyncio.create_task(self.dates_to_keyboard(i)))
        
        #create task for today day here
        for task in tasks:
            days_list.append(await task)
        days_dict = {days_list[i]: i for i in range(9)}
        return days_dict, days_list
        







