import emoji
from aiogram.filters.command import Command
from aiogram import types
from config import ConfigTask
from logger import setup_logging

tasks = {}
logger = setup_logging()

def add_todo(date: str, task: str) -> None:
    """Добавляет задачу на указанную дату."""
    tasks.setdefault(date, []).append(task)

def register_handlers(dp):
    @dp.message(Command("start"))
    async def start_send(message: types.Message):
        """Обработка команды /start"""
        await message.answer(ConfigTask.welcome_text)

    @dp.message(Command("help"))
    async def help_menu(message: types.Message):
        """Обработка команды /help"""
        logger.info(f"Пользователь {message.from_user.full_name} выбрал команду /help")
        await message.answer(ConfigTask.help_text)

    @dp.message(Command("add"))
    async def add(message: types.Message):
        """Обработка команды /add"""
        try:
            command = message.text.split(maxsplit=2)
            if len(command) < 3:
                await message.answer("Пожалуйста, укажите дату и задачу в формате '/add дата задача'.")
                return

            date = command[1].lower()
            task = command[2]
            add_todo(date, task)
            text = f"Задача '{task}' добавлена на дату {date}"
            logger.info(f"Пользователь {message.from_user.full_name} выбрал команду /add {date} {task}")
            await message.answer(text)
        except Exception as e:
            logger.error(f"Ошибка при добавлении задачи: {e}")
            await message.answer("Произошла ошибка при добавлении задачи.")

    @dp.message(Command("show"))
    async def show(message: types.Message):
        """Обработка команды /show"""
        command = message.text.split(maxsplit=1)
        if len(command) < 2:
            await message.answer("Пожалуйста, укажите дату в формате '/show дата'.")
            return

        date = command[1].lower()
        text = ""
        logger.info(f"Пользователь {message.from_user.full_name} выбрал команду /show {date}")

        if date in tasks:
            text = date.upper() + "\n"
            for task in tasks[date]:
                text += emoji.emojize(":heavy_exclamation_mark:", language="alias") + task + "\n"
            logger.info(f"Пользователю {message.from_user.full_name} отобразился список задач на выбранную дату {date}")
        else:
            text = ConfigTask.no_task
            logger.info(f"Нет задач на выбранную дату {date} пользователем {message.from_user.full_name}")

        await message.answer(text)
