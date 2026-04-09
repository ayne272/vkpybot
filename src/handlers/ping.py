from vkbottle.bot import BotLabeler, Message

labeler = BotLabeler()

@labeler.message(text="/пинг")
async def ping_handler(message: Message) -> None:
    await message.answer("понг! 🏓")

@labeler.message(text="/понг")
async def pong_handler(message: Message) -> None:
    await message.answer("иди нахуй")

@labeler.message(text="/крым")
async def crimea_handler(message: Message) -> None:
    await message.answer("Наш!")