from vkbottle.bot import Bot

from src.config import settings
from src.handlers import labelers
from src.db.database import engine
from src.db.models import Base

bot = Bot(token=settings.bot_token)

for custom_labeler in labelers:
    bot.labeler.load(custom_labeler)

async def startup_db():
    """Создает таблицы в БД при старте (если их нет)."""
    print("🚀 Инициализация базы данных...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_db():
    """Безопасное отключение от БД."""
    print("🛑 Закрытие соединения с БД...")
    await engine.dispose()
    print("✅ База данных успешно отключена.")

bot.loop_wrapper.on_startup.append(startup_db())
bot.loop_wrapper.on_shutdown.append(close_db())

if __name__ == "__main__":
    print("🤖 Бот запущен!")
    bot.run_forever()