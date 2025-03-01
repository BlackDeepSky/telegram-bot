from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Привет! Я твой Telegram-бот.")

# Эхо-обработчик
@dp.message_handler()
async def echo_message(message: types.Message):
    await message.answer(f"Ты сказал: {message.text}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)