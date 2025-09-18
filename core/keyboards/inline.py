"""Тут докстринга"""
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_confirm_button_keyboard():
    """Тут докстринга"""
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Добавить кнопку", callback_data="add_button")
    keyboard_builder.button(text="Продолжить без кнопки", callback_data="no_button")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()

async def get_keyboard_for_send(text_button, url_button):
    """Клавиатура для отправки пользователям"""
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text=text_button, url=url_button)
    keyboard_builder.adjust()
    return keyboard_builder.as_markup()

