from aiogram.fsm.state import StatesGroup, State


class Questionnaire(StatesGroup):
    gender = State()
    age = State()
    profession = State()


class Order(StatesGroup):
    product = State()
    color = State()
    amount = State()
    address = State()
    payment = State()
