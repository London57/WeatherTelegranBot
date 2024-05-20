
# def translate_city(city: str):
#     translator = Translator()
#     return translator.translate(city, dest='en').text

from yandex.Translater import Translater
from langdetect import detect
city = 'москва'
translator = Translater(from_lang=detect(city), to_lang='en')

for b in city: 
    print(translator.translate())