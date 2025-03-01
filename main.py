from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from config import BOT_TOKEN
import asyncio

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Обработчик команды /start
@dp.message()
async def start_command(message: Message):
    await message.answer("Привет! Я твой Telegram-бот.")

# Эхо-обработчик
@dp.message()
async def echo_message(message: Message):
    await message.answer(f"Ты сказал: {message.text}")

# Функция для запуска бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())