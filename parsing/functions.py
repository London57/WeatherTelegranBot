from bs4 import BeautifulSoup
import requests
import undetected_chromedriver

# response = driver.get('https://yandex.ru/pogoda/Kazan')
url = f'https://pogoda.mail.ru/prognoz/almetyevsk/'
response = requests.get(url)
# print(response.content)
soup = BeautifulSoup(response.text, 'lxml')


async def get_date(i, data={}):
    data['date'] = soup.find_all('div', class_="day day_index")[i].find('div',
                                                             class_="day__date").text
    return data

async def get_temperature(i, data={}):
    temp = soup.find_all('div', class_="day day_index")[i].find('div',
                                                             class_="day__temperature").text.replace('\n', '').replace('\t', '')
    data['day_temp'] = temp[:4] + 'C'
    data['night_temp'] = temp[4:] + 'C'
    return data

async def get_description(i, data={}):
    data['description'] = soup.find_all('div', class_="day day_index")[i].find('div',
                                                             class_="day__description").text
    return data
    
async def get_humidity(i, data={}):
    data['humidity'] = soup.find_all('div', class_="day day_index")[i].find_all('div',
                                                             class_="day__additional")[1].text.replace('\n', '').replace('\t', '')
    return data

async def get_breeze(i, data={}):
    data['breeze'] = soup.find_all('div', class_="day day_index")[i].find_all('div',
                                                             class_="day__additional")[2].text.replace('\n', '').replace('\t', '')
    return data

async def get_precipitation(i, data={}):
    data['precipitation'] = soup.find_all('div', class_="day day_index")[i].find_all('div',
                                                             class_="day__additional")[4].text.replace('\n', '').replace('\t', '')
    return data

list_of_func = [get_date, get_breeze, get_description, get_humidity, get_description, get_precipitation] 

# print(get_date(1))
# print(data)