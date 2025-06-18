import os
import aiohttp

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from dotenv import load_dotenv
from openai import OpenAI
from states import Questionnaire
from db_interaction import db

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENROUTER_API_KEY")

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


async def handle_weather(message: Message):
    url = f"https://api.openweathermap.org/data/2.5/weather?q=Бишкек&appid={WEATHER_API_KEY}&units=metric"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                type_ = data['weather'][0]['main']
                temperature = data['main']['temp']
                feels_like = data['main']['feels_like']
                city = data['name']
                await message.answer(f"Город {city}\n Температура: {temperature}\n Ощущается как {feels_like}\n"
                                     f"{type_}")
            else:
                await message.answer("Sorry . Service does not respond.")


async def chat_with_ai(message: Message):
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=f"{OPENAI_API_KEY}",
        )
        completion = client.chat.completions.create(
            model="deepseek/deepseek-r1-0528-qwen3-8b:free",
            temperature=0.5,
            messages=[
                {
                    "role": "user",
                    "content": f"{message.text}"
                }
                # {
                #     "role": "system",
                #     "content": "Ты помошник по географии. Отвечай на вопросы только по географии"
                # }
            ]
        )
        reply = completion.choices[0].message.content
        await message.answer(reply)
    except Exception as e:
        print(e)


current_dir = "generated_images"
os.makedirs(current_dir, exist_ok=True)


# async def generate_image(message: Message):
#     try:
#         prompt = message.text
#         url = f"https://image.pollinations"


