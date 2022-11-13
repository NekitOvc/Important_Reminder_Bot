from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import ConfigTask

import os
import emoji
import logging

#логирование в файл. Происходит перезапись при каждом запуске бота с указанием даты/времени
logging.basicConfig(level=logging.INFO, filename='py_log.log', filemode='w', format='%(asctime)s %(levelname)s %(message)s')

bot = Bot(token=ConfigTask.TOKEN)
dp = Dispatcher(bot)

tasks = {}

#date - дата, task - задача
def add_todo(date, task):
    if date in tasks:
        tasks[date].append(task)
    else:
        tasks[date] = []
        tasks[date].append(task)

#обработка команды /start
@dp.message_handler(commands=['start'])
async def start_send(message: types.Message):
    await bot.send_message(message.from_user.id, ConfigTask.welcome_text)

#обработка команды /help
@dp.message_handler(commands=['help'])
async def help_menu(message: types.Message):
    logging.info(f'Пользователь {message.from_user.full_name} выбрал команду /help')
    await bot.send_message(message.from_user.id, ConfigTask.help_text)

#обработка команды /add - добавление новой задачи в формате /add дата задача
@dp.message_handler(commands=['add'])
async def add(message: types.Message):
    command = message.text.split(maxsplit=2) #полученное сообщение разделяется по пробелам на 2 части
    date = command[1].lower() #2-й элемент - дата в нижнем регистре
    task = command[2] #3-й элемент - задача
    add_todo(date, task) #добавление в общий список задач
    text = f'Задача {task} добавлена на дату {date}'
    logging.info(f'Пользователь {message.from_user.full_name} выбрал команду /add {date} {task}') 
    await bot.send_message(message.from_user.id, text)

#обработка команды /show - отобразить все задачи на выбранную дату в формате /show дата
@dp.message_handler(commands=['show'])
async def show(message: types.Message):
    command = message.text.split(maxsplit=1) 
    date = command[1].lower()
    text = ''
    logging.info(f'Пользователь {message.from_user.full_name} выбрал команду /show {date}')
    if date in tasks:
        text = date.upper() + '\n'
        for task in tasks[date]:
            text = text + emoji.emojize(':heavy_exclamation_mark:', language='alias') + task + '\n'
        logging.info(f'Пользователю {message.from_user.full_name} отобразился список задач на выбранную дату {date}')
    else:
        text = ConfigTask.no_task
        logging.info(f'Нет задач на выбранную дату {date} пользователем {message.from_user.full_name}')
    await bot.send_message(message.from_user.id, text)

executor.start_polling(dp, skip_updates=True)