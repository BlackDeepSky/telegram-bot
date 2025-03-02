from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from config import BOT_TOKEN
from news_parser import get_news
import asyncio
from aiogram.exceptions import RetryAfter

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Список пользователей, которым будут отправляться новости
USER_IDS = [1985969754]  # Замените на ID вашего Telegram аккаунта

# Обработчик команды /start
@dp.message()
async def start_command(message: Message):
    await message.answer("Привет! Я буду присылать тебе новости каждые 60 минут.")

# Функция для отправки новостей
async def send_news():
    while True:
        try:
            news_data = get_news()
            for user_id in USER_IDS:
                for news in news_data:
                    message = f"✨ *{news['category']}*\n\n{news['title']}\n{news['url']}"
                    try:
                        await bot.send_message(user_id, message, parse_mode="Markdown")
                    except RetryAfter as e:
                        print(f" Flood limit exceeded. Sleep {e.timeout} seconds.")
                        await asyncio.sleep(e.timeout)
                    except Exception as ex:
                        print(f"Error sending news to user {user_id}: {ex}")
            await asyncio.sleep(3600)  # Ждём 1 час
        except Exception as e:
            print(f"Error fetching news: {e}")
            await asyncio.sleep(60)  # Повторная попытка через 1 минуту

# Функция для запуска бота
async def main():
    dp.include_router(dp)
    await asyncio.gather(
        dp.start_polling(bot),
        send_news()
    )

if __name__ == '__main__':
    asyncio.run(main())