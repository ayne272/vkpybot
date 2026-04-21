import random
from datetime import date
from vkbottle.bot import BotLabeler, Message
from vkbottle.dispatch.rules.base import PeerRule
from sqlalchemy import select

from src.db.database import AsyncSessionLocal
from src.db.models import Player

from src.utils.loot import get_loot


labeler = BotLabeler()
labeler.auto_rules = [PeerRule()]
labeler.message_view.replace_mention = True

@labeler.message(text=["/писюн"])
async def dick_handler(message: Message) -> None:
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
        
        player.last_roll_date = today
        
        if is_new_player:
            await message.answer(
                f"{player.first_name} {player.last_name}, Вітаю в грі писюн, ти зіграв в перший раз і зараз твій пісюн має довжину {player.dick} см."
            )
            await session.commit()
            return
        
        if player.dick != 0:
            change = get_loot()
        else:
            change = random.randint(1, 10)

        player.dick += change

        if change > 0:
            msg = f"{player.first_name} {player.last_name}, твій пісюн виріс на {change} см. "
        else:
            msg = f"{player.first_name} {player.last_name}, твій пісюн зменшився на {abs(change)} см. "

            if player.dick < 0:
                player.dick = 0

        await session.commit()

        if player.dick == 0:
            await message.answer(
                f"{player.first_name} {player.last_name},  у тебе відвалилася піська("
            )
            return
            
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
            if player.dick == 0:
                lines.append(
                    f"{medal} {player.first_name} {player.last_name} — відвалилася піська"
                )
            else:
                lines.append(f"{medal} {player.first_name} {player.last_name} — {player.dick} см.")
        
        await message.answer("\n".join(lines))

@labeler.message(text=["/сдр <arg>", "/сдр"])
async def happy_birthday_handler(message: Message, arg: str = None):
    target_id = None

    if message.mention:
        target_id = message.mention.id

    if message.reply_message:
        target_id = message.reply_message.from_id

    if target_id:
         users_info = await message.ctx_api.users.get(user_ids=[target_id], fields=["domain"])
         msg = f"@{users_info[0].domain},"
    elif arg:
        msg = arg
    else:
        msg = ""

    msg += " c др брат в твой день рождения хочу по брацки пожелать тебе чтоб каждый вечер тебе попадался нефор дрыщавый на избиение, чтобы хуй был большой, чтоб овечек было много в твоем гареме, чтобы брат братья всегда были рядом, чтобы брат у тебя здоровье не подводило, чтоб брат хасанил люто брат по ночной махачкале брат, чтоб брат денег было море, чтоб брат когда долбил шлюх - всегда кончал, чтоб брат порнуха попадалась самая ахуенная, чтоб брат в кске летело в голову всегда брат, чтоб брат все твои враги подохли брат, чтоб брат очко твоё брат не продырявилось, чтоб брат ебал тока красивых телок брат брат, чтоб брат поляк не выебывался брат, чтоб брат братья сестры родные были здоровы брат, чтоб счастлив был брат, чтоб тоски не было брат, чтоб брат наркотики бросил брат, чтоб коллапса встретил брат, чтоб брат аллах тебя всегда любил брат, чтоб девушка брат была любимая брат, чтоб брат в доте вак банов не было брат, чтоб брат андреевы брат в елденринке не ныли, чтоб брат в вконтакте брат не банили брат, чтоб брат у тебя всегда стояк был, чтоб брат тебя боялись и уважали все пацаны в городе, чтоб брат амантур брат всегда шел играть брат, чтоб брат было у тебя всё хорошо брат. мой любимый брат братан братишка люблю брат целую нежно брат в засос брат не по гейски а по братски брат. давай обнял приподнял хороше этот день провел брат!!!💥💥\n\u3164\nс днем рождения тибе карочи ооочен многа деняк и чтоби ты был невидимый полёт ренгеновски зрение телекинес сила скорость меф tg skorost_kz187"

    await message.answer(msg)