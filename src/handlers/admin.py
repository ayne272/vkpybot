from vkbottle.dispatch.rules import ABCRule
from vkbottle.bot import BotLabeler, Message
from sqlalchemy import update

from src.db.database import AsyncSessionLocal
from src.db.models import Player

from src.config import ADMIN_IDS

labeler = BotLabeler()

class IsBotAdminRule(ABCRule[Message]):
    """
    Кастомное правило vkbottle. 
    Проверяет, является ли отправитель сообщения администратором бота.
    """

    async def check(self, event: Message) -> bool:
        return event.from_id in ADMIN_IDS

labeler.auto_rules = [IsBotAdminRule()]

@labeler.message(text="/сброс")
async def reset_handler(message: Message) -> None:
    async with AsyncSessionLocal() as session:
        stmt = (
            update(Player)
            .values(last_roll_date=None)
            # where(Player.last_roll_date.isnot(None)) # Опционально: можно сбрасывать только у тех, у кого он есть
        )
        result = await session.execute(stmt)
        await session.commit()

    await message.answer(
        f"✅ Таймеры успешно сброшены!\n"
        f"🔄 Обновлено профилей: {result.rowcount}\n"
    )