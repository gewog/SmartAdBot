"""Сборка пользователей в базу"""
from typing import Any, Dict, Callable, Awaitable
from aiogram.types import Message
from aiogram.fsm.middleware import BaseMiddleware
from database.queries import inser_data

class MyMiddlewareDB(BaseMiddleware):
    def __init__(self):
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
                print(f"[Middleware] Пользователь {self.name} ({self.id}) добавлен в БД!")
            except Exception as e:
                print(f"[Middleware] Ошибка при добавлении в БД: {e}")
        else:
            print(f"[Middleware] В событии нет message или это не Message. Пропускаю.")

        return await handler(event, data)