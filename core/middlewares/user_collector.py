"""
Модуль для middleware, отвечающего за сбор и сохранение данных пользователей в базу данных.

Этот модуль реализует middleware, который перехватывает события от Telegram-бота,
извлекает информацию о пользователе и сохраняет её в базу данных.
Основные функции:
- Извлечение имени и ID пользователя из сообщения.
- Сохранение данных пользователя в базу данных.

Зависимости:
- aiogram: Для работы с Telegram API и middleware.
- database.queries: Для выполнения запросов к базе данных.
"""

from typing import Any, Dict, Callable, Awaitable
from aiogram.types import Message
from aiogram.fsm.middleware import BaseMiddleware
from database.queries import inser_data


class MyMiddlewareDB(BaseMiddleware):
    """
    Middleware для сбора и сохранения данных пользователей в базу данных.

    Атрибуты:
        name (str | None): Имя пользователя.
        id (int | None): ID пользователя в Telegram.
    """

    def __init__(self):
        """
        Инициализирует экземпляр middleware.
        """
        self.name = None
        self.id = None

    async def __call__(self, handler, event, data):
        print(f"[Middleware] Получено событие: {type(event)}")

        # Проверяем, что это Update и в нём есть message
        if hasattr(event, "message") and isinstance(event.message, Message):
            message = event.message
            self.name = message.from_user.full_name
            self.id = message.from_user.id
            print(f"[Middleware] Пользователь: {self.name} (ID: {self.id})")
            try:
                await inser_data(self.name, self.id)
                print(
                    f"[Middleware] Пользователь {self.name} ({self.id}) добавлен в БД!"
                )
            except Exception as e:
                print(f"[Middleware] Ошибка при добавлении в БД: {e}")
        else:
            print(f"[Middleware] В событии нет message или это не Message. Пропускаю.")

        return await handler(event, data)
