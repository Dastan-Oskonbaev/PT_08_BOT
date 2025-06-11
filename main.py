import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv

import keyboards as kb
from service import handle_questionnaire
from states import Questionnaire
from db_interaction import db

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.callback_query()
async def get_callback(callback: CallbackQuery):
    if callback.data == 'like':
        await callback.message.answer("Я рад что вам все понравилось")
    elif callback.data == 'dislike':
        await callback.message.answer("Сожалею")


@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Hello I'm your first BOT", reply_markup=kb.main_page_keyboard)


@dp.message(Command(commands='help'))
async def help_command(message: Message):
    await message.reply("I'm here to help you", reply_markup=kb.main_page_keyboard)


@dp.message(Command(commands='questions'))
async def about_command(message: Message, state: FSMContext):
    await state.set_state(Questionnaire.gender)
    await message.answer("Какой у тебя пол?")


@dp.message()
async def message_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await handle_questionnaire(message, state)
    else:
        if message.text == "AI CHAT":
            await message.answer("<i>Пока что в режиме разработки </i>" , reply_markup=kb.inline_keyboard_kb, parse_mode=ParseMode.HTML)
        elif message.text == "AI IMAGE":
            await message.answer("Пока что в режиме разработки")
        elif message.text == "ORDER":
            await state.set_state(Questionnaire.gender)
            await message.answer("Какой у тебя пол?")
        else:
            await message.answer(f"you typed {message.text}")


@dp.message(F.photo)
async def photo_handler(message: Message):
    await message.reply(f"Nice photo")


async def main():
    try:
        print('Bot started')
        await dp.start_polling(bot)
        await db.connect()
    except Exception as e:
        print(e)
    finally:
        await db.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
