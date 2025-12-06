import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.exceptions import TelegramForbiddenError

TOKEN = "8481219439:AAHew1lz7LDXoSMff-Z3wv7CkbAQJcNe3vw"
CHANNEL = "@MAONIK_gift"
ADMIN_ID = 7955777831  # ТВОЙ Telegram ID !!! обязательно замени


bot = Bot(token=TOKEN)
dp = Dispatcher()


# --- Проверка подписки ---
async def check_sub(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


# --- /start ---
@dp.message(CommandStart())
async def start_cmd(message: Message):
    if not await check_sub(message.from_user.id):
        await message.answer(
            "❗ Чтобы пользоваться ботом — подпишись на канал:\n"
            f"{CHANNEL}"
        )
        return

    await message.answer("Бот активирован! Добавь меня в чат, и я буду следить за выпадением 🎰 777.")


# --- Отслеживание сообщений в чатах ---
@dp.message(F.sticker)
async def slot_check(message: Message):

    # Проверяем подписку
    if not await check_sub(message.from_user.id):
        try:
            await message.reply("❗ Сначала подпишись на канал:\n" + CHANNEL)
        except TelegramForbiddenError:
            pass
        return

    # Проверяем стикер на выпадение 777
    if "777" in (message.sticker.emoji or ""):
        text = (
            f"🎰 *ВЫПАЛИ 777!*\n\n"
            f"👤 Пользователь: {message.from_user.full_name}\n"
            f"🆔 ID: {message.from_user.id}\n"
            f"Чат: {message.chat.title}\n\n"
            f"🔗 [Перейти к сообщению]({message.link})"
        )

        await bot.send_message(ADMIN_ID, text, parse_mode="Markdown")


async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

asyncio.run(main())
