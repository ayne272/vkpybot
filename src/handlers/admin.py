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
    """Сбрасывает кулдаун всем игрокам в текущем чате."""
    async with AsyncSessionLocal() as session:
        stmt = (
            update(Player)
            .where(Player.chat_id == message.peer_id)
            .values(last_roll_date=None)
            # where(Player.last_roll_date.isnot(None)) # Опционально: можно сбрасывать только у тех, у кого он есть
        )
        result = await session.execute(stmt)
        await session.commit()

    await message.answer(f"Успіх!")

@labeler.message(text="/изменить_писюн <new_dick_str>")
async def set_dick_handler(message: Message, new_dick_str: str) -> None:
    """Устанавливает игроку новый писюн в текущем чате."""
    if not message.reply_message:
        return
        
    try:
        new_dick = int(new_dick_str)
    except ValueError:
        return

    target_id = message.reply_message.from_id
    chat_id = message.peer_id

    async with AsyncSessionLocal() as session:
        stmt = (
            update(Player)
            .where(Player.vk_id == target_id, Player.chat_id == chat_id)
            .values(dick=new_dick)
        )
        result = await session.execute(stmt)
        await session.commit()

    if result.rowcount > 0:
        await message.answer(f"Успіх!")