from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


def menu_kb():
    kb = [
        [
            KeyboardButton(text="Student"),
            KeyboardButton(text="Owner")
        ],
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Tanlang"
    )

    return keyboard


def admin_kb():
    kb = [
        [
            KeyboardButton(text="Listings")
        ],
        [
            KeyboardButton(text="Housing")
        ],
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )

    return keyboard


def inline_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Accept", callback_data="accept_housing"),
            InlineKeyboardButton(text="Reject", callback_data="reject_housing")
        ]
    ]
    )
    return kb
