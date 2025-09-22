"""
Базовый роутер для Telegram-бота.

Этот модуль реализует базовые обработчики команд, такие как стартовая команда `/start`.
Основные функции:
- Приветствие пользователя при старте бота.

Зависимости:
- aiogram: Для взаимодействия с Telegram API.
"""

from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import FSInputFile


# Инициализация базового роутера для обработки сообщений
base_router = Router()


@base_router.message(CommandStart())
async def answer_id(mes: types.Message) -> None:
    """
    Обработчик стартовой команды `/start`.

    Отправляет приветственное сообщение пользователю при первом запуске бота.

    Args:
        message (types.Message): Объект сообщения от пользователя.

    Returns:
        None
    """
    await mes.answer(f"Hello (◕‿◕), welcome to sender bot!")
