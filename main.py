from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from config import BOT_TOKEN
from news_parser import get_news
import asyncio
from aiogram.exceptions import TelegramAPIError

# Список пользователей, которым будут отправляться новости
USER_IDS = [1985969754]  # Замените на ID вашего Telegram аккаунта

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Обработчик команды /start
@dp.message(commands=['start'])
async def start_command(message: Message):
    await message.answer("Привет! Я буду присылать тебе новости каждые 60 минут.")

# Функция для отправки новостей
async def send_news():
    while True:
        try:
            news_data = get_news()
            for user_id in USER_IDS:
                for news in news_data:
                    message = (
                        f"✨ *{news['category']}*\n\n"
                        f"**Заголовок:** {news['title']}\n\n"
                        f"📝 *Выжимка:* {news['summary']}\n\n"
                        f"📖 [Читать полностью]({news['url']})"
                    )
                    try:
                        # Попытка отправить сообщение с изображением
                        if news["image_url"]:
                            await bot.send_photo(
                                chat_id=user_id,
                                photo=news["image_url"],
                                caption=message,
                                parse_mode="Markdown"
                            )
                        else:
                            await bot.send_message(
                                user_id,
                                message,
                                parse_mode="Markdown",
                                disable_web_page_preview=True
                            )
                    except TelegramAPIError as e:
                        if "FLOOD_WAIT" in str(e):
                            wait_time = int(str(e).split("FLOOD_WAIT_")[-1])
                            print(f"Flood limit exceeded. Sleep {wait_time} seconds.")
                            await asyncio.sleep(wait_time)
                        else:
                            print(f"Telegram API error: {e}")
                    except Exception as ex:
                        print(f"Error sending news to user {user_id}: {ex}")
            await asyncio.sleep(3600)  # Ждём 1 час
        except Exception as e:
            print(f"Error fetching news: {e}")
            await asyncio.sleep(60)  # Повторная попытка через 1 минуту

# Функция для запуска бота
async def main():
    await asyncio.gather(
        dp.start_polling(bot),
        send_news()
    )

if __name__ == '__main__':
    asyncio.run(main())