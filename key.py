from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)
from database.requests import get_habits
main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Мои привычки")],
                                     [KeyboardButton(text="Новая привычка"),
                                     KeyboardButton(text="Удалить привычку")]],
                           resize_keyboard=True,
                           input_field_placeholder="Выберите действие:")
weekHabits = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Monday", callback_data="1")],
                                                   [InlineKeyboardButton(text="Tuesday", callback_data="2")],
                                                   [InlineKeyboardButton(text="Wednesday", callback_data="3")],
                                                   [InlineKeyboardButton(text="Thursday", callback_data="4")],
                                                   [InlineKeyboardButton(text="Friday", callback_data="5")],
                                                   [InlineKeyboardButton(text="Saturday", callback_data="6")],
                                                   [InlineKeyboardButton(text="Sunday", callback_data="7")]])
