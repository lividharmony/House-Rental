from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from database import create_db_pool


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


async def admin_kb(user_id):
    pool = await create_db_pool()
    async with pool.acquire() as connection:
        user_type = await connection.fetchval(
            "SELECT user_type FROM users WHERE user_id = $1",
            user_id
        )

    if user_type == 'owner':
        kb = [
            [
                KeyboardButton(text="Listings")
            ],
            [
                KeyboardButton(text="Housing")
            ],
        ]
    else:
        kb = [
            [
                KeyboardButton(text="Search")
            ],
            [
                KeyboardButton(text="Application")
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


def cancel_kb():
    kb = [
        [
            KeyboardButton(text="Bekor qilish")
        ]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )

    return keyboard
