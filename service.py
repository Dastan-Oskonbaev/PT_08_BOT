from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states import Questionnaire


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
    await message.answer(f"Анкета пользователя {message.from_user.username}\n"
                         f"Пол {data['gender']}\n"
                         f"Возраст {data['age']}\n"
                         f"Профессия {message.text}")
    await state.clear()


async def handle_questionnaire(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == Questionnaire.gender:
        await gender_handler(message, state)
    elif current_state == Questionnaire.age:
        await age_handler(message, state)
    elif current_state == Questionnaire.profession:
        await profession_handler(message, state)
