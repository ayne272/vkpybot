import random
from datetime import date
from vkbottle.bot import BotLabeler, Message
from vkbottle.dispatch.rules.base import PeerRule
from sqlalchemy import select

from src.db.database import AsyncSessionLocal
from src.db.models import Player


labeler = BotLabeler()
labeler.auto_rules = [PeerRule()] 

@labeler.message(text=["/писюн"])
async def growth_handler(message: Message) -> None:
    async with AsyncSessionLocal() as session:
        player = await session.scalar(
            select(Player).where(
                Player.vk_id == message.from_id,
                Player.chat_id == message.peer_id
            )
        )

        today = date.today()
        is_new_player = False

        if not player:
            is_new_player = True

            users_info = await message.ctx_api.users.get(user_ids=[message.from_id])
            first_name = users_info[0].first_name
            last_name = users_info[0].last_name
            base_dick = random.randint(1, 10)
            
            player = Player(
                vk_id=message.from_id, 
                chat_id=message.peer_id, 
                first_name=first_name, 
                last_name=last_name,
                dick=base_dick
            )

            session.add(player)
        
        if player.last_roll_date == today:
            await message.answer(
                f"{player.first_name} {player.last_name}, ти сьогодні вже грав("
            )
            return

        if is_new_player:
            sign = 1
        else:
            sign = random.choice([-1, 1])
        
        change = random.randint(1, 10)
        player.dick += change * sign
        player.last_roll_date = today

        if player.dick < 0:
            player.dick = 0

        await session.commit()

        if is_new_player:
            await message.answer(
                f"{player.first_name} {player.last_name}, Вітаю в грі писюн, ти зіграв в перший раз і зараз твій пісюн має довжину {player.dick} см."
            )
            return
        
        if player.dick == 0:
            await message.answer(
                f"{player.first_name} {player.last_name},  у тебе відвалилася піська("
            )
            return

        if change > 0:
            msg = f"{player.first_name} {player.last_name}, твій пісюн виріс на {change} см. "
        else:
            msg = f"{player.first_name} {player.last_name}, твій пісюн зменшився на {abs(change)} см. "
            
        msg += f"Тепер його довжина {player.dick} см."
        
        await message.answer(msg)

@labeler.message(text=["/топ"])
async def top_handler(message: Message) -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Player)
            .where(Player.chat_id == message.peer_id)
            .order_by(Player.dick.desc())
            .limit(10)
        )

        top_players = result.scalars().all()

        if not top_players:
            await message.answer("Перекотиполе... Здається, ще ніхто не грав.")
            return

        lines =["🏆 Топ 10 хлопців у чаті:\n"]
        medals = ["🥇", "🥈", "🥉"]
    
        for idx, player in enumerate(top_players):
            medal = medals[idx] if idx < 3 else f" {idx + 1}. "
            lines.append(
                f"{medal} {player.first_name} {player.last_name} — "
                f"{player.dick} см."
            )
        
        await message.answer("\n".join(lines))