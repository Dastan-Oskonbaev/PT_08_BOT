from aiogram import types


main_page_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="AI CHAT"),
            types.KeyboardButton(text="AI IMAGE"),
        ],
        [
            types.KeyboardButton(text="WEATHER"),
            types.KeyboardButton(text="QUESTIONNAIRE")
        ]
    ],
    resize_keyboard = True
)


inline_keyboard_kb = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [
            types.InlineKeyboardButton(text="👍", callback_data="like"),
        ],
        [
            types.InlineKeyboardButton(text="👎", callback_data="dislike"),
        ]
    ]
)