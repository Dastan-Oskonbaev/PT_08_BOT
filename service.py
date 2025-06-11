from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states import Questionnaire
from db_interaction import db


async def gender_handler(message: Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await state.set_state(Questionnaire.age)
    await message.answer("Сколько тебе лет?")


async def age_handler(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(age=message.text)
        await state.set_state(Questionnaire.profession)
        await message.answer("Какая у тебя профессия?")
    else:
        await message.answer("Я же нормально попросил(((")


async def profession_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    await db.add_users_profile(
        message.chat.id, data['age'], data['gender'], message.text
    )
    await message.answer("Вы успешно записаны в базу данных")
    await state.clear()


async def handle_questionnaire(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == Questionnaire.gender:
        await gender_handler(message, state)
    elif current_state == Questionnaire.age:
        await age_handler(message, state)
    elif current_state == Questionnaire.profession:
        await profession_handler(message, state)
