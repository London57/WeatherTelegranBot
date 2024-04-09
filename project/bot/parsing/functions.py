
from bs4 import BeautifulSoup
import requests, asyncio

class Parsing:
    
    
    def __init__(self, city):
        self.city = city
        self.soup = BeautifulSoup(requests.get(f'https://pogoda.mail.ru/prognoz/{city}/').text, 'lxml')
    
    async def dates(self, i):
        data = self.soup.find_all('div', class_="day day_index")[i].find('div',
                                                             class_="day__date").text
        return data

    async def get_date(self, i, data={}):
        data['date'] = self.soup.find_all('div', class_="day day_index")[i].find('div',
                                                                class_="day__date").text
        return data

    async def get_temperature(self, i, data={}):
        temp = self.soup.find_all('div', class_="day day_index")[i].find('div',
                                                                class_="day__temperature").text.replace('\n', '').replace('\t', '')
        data['day_temp'] = temp[:4] + 'C'
        data['night_temp'] = temp[4:] + 'C'
        return data

    async def get_description(self, i, data={}):
        data['description'] = self.soup.find_all('div', class_="day day_index")[i].find('div',
                                                                class_="day__description").text
        return data
        
    async def get_humidity(self, i, data={}):
        data['humidity'] = self.soup.find_all('div', class_="day day_index")[i].find_all('div',
                                                                class_="day__additional")[1].text.replace('\n', '').replace('\t', '')
        return data

    async def get_breeze(self, i, data={}):
        data['breeze'] = self.soup.find_all('div', class_="day day_index")[i].find_all('div',
                                                                class_="day__additional")[2].text.replace('\n', '').replace('\t', '')
        return data

    async def get_precipitation(self, i, data={}):
        data['precipitation'] = self.soup.find_all('div', class_="day day_index")[i].find_all('div',
                                                                class_="day__additional")[4].text.replace('\n', '').replace('\t', '')
        return data
    

    async def get_functions_list(self):
        return [self.get_date, self.get_breeze, self.get_description, self.get_humidity, self.get_description, self.get_precipitation] 

    
    async def get_days_dict_and_list(self, *args, days_list=[], tasks=[]):
        for i in range(7):
            tasks.append(asyncio.create_task(self.dates(i)))
        
        #create task for today day here
        for task in tasks:
            days_list.append(await task)
        days_dict = {days_list[i]: i for i in range(7)}
        return days_dict, days_list
        

# url = f'https://pogoda.mail.ru/prognoz/Almetyevsk/'
# response = requests.get(url)

# soup = BeautifulSoup(response.text, 'lxml')






