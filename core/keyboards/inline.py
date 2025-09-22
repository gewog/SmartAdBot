"""
Модуль для создания инлайн-клавиатур в Telegram-боте.

Этот модуль предоставляет функции для генерации инлайн-клавиатур,
используемых в различных сценариях взаимодействия с пользователем:
- Клавиатура для подтверждения добавления кнопки.
- Клавиатура для отправки сообщений с кнопками пользователям.

Зависимости:
- aiogram: Для работы с Telegram API и создания клавиатур.
"""

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup


def get_confirm_button_keyboard() -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру для подтверждения добавления кнопки.

    Возвращает клавиатуру с двумя кнопками:
    - "Добавить кнопку" (callback_data="add_button")
    - "Продолжить без кнопки" (callback_data="no_button")

    Returns:
        InlineKeyboardMarkup: Готовая инлайн-клавиатура.
    """
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Добавить кнопку", callback_data="add_button")
    keyboard_builder.button(text="Продолжить без кнопки", callback_data="no_button")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


async def get_keyboard_for_send(text_button, url_button) -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру для отправки сообщения с кнопкой пользователям.

    Args:
        text_button (str): Текст, отображаемый на кнопке.
        url_button (str): Ссылка, на которую ведёт кнопка.

    Returns:
        InlineKeyboardMarkup: Готовая инлайн-клавиатура с одной кнопкой.
    """
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text=text_button, url=url_button)
    keyboard_builder.adjust()
    return keyboard_builder.as_markup()
