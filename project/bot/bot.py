from aiogram import Bot
from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())


bot = Bot(token=os.getenv('TOKEN'))