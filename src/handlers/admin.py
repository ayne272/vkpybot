from vkbottle.dispatch.rules import ABCRule
from vkbottle.bot import BotLabeler, Message
from sqlalchemy import update

from src.utils.text import mention
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

@labeler.message(text="/изменить_писюн <new_dick>")
async def set_dick_handler(message: Message, new_dick: str) -> None:
    """Устанавливает игроку новый писюн в текущем чате."""

    if not message.reply_message:
        return
        
    try:
        new_height = int(new_dick)
    except ValueError:
        return

    target_id = message.reply_message.from_id
    chat_id = message.peer_id

    async with AsyncSessionLocal() as session:
        stmt = (
            update(Player)
            .where(Player.vk_id == target_id, Player.chat_id == chat_id)
            .values(height=new_height)
        )
        result = await session.execute(stmt)
        await session.commit()
            