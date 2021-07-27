from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import bot_settings
from aiogram import Bot, Dispatcher

bot = Bot(token = bot_settings['TOKEN'])
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)