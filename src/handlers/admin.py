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
        await message.answer("❌ Нужно ответить на сообщение пользователя")
        return

    try:
        new_dick = int(new_dick_str)
    except ValueError:
        await message.answer("❌ Неправильный формат. Используйте: /изменить_писюн 15")
        return

    target_id = message.reply_message.from_id
    chat_id = message.peer_id

    async with AsyncSessionLocal() as session:
        # Попытка обновить существующего игрока
        stmt = (
            update(Player)
            .where(Player.vk_id == target_id, Player.chat_id == chat_id)
            .values(dick=new_dick)
        )
        result = await session.execute(stmt)

        # Если игрок не найден, создать нового
        if result.rowcount == 0:
            # Получить информацию о пользователе
            user_info = await message.ctx_api.users.get(user_ids=[target_id])
            if user_info:
                user = user_info[0]
                new_player = Player(
                    vk_id=target_id,
                    chat_id=chat_id,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    dick=new_dick,
                    last_roll_date=None
                )
                session.add(new_player)

        await session.commit()

    await message.answer(f"✅ Успіх! Новый писюн: {new_dick}")
