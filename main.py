"""Главный файл бота.

Этот модуль содержит основную логику запуска и остановки Telegram-бота,
а также настройку логгирования и обработки сообщений.
Использует aiogram для взаимодействия с Telegram API.

Функции:
    on_startup: Обработчик запуска бота.
    on_shutdown: Обработчик остановки бота.
    main: Основная функция для запуска бота.
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command

from config.config import bot, dp # Импортируем экземпляры бота и диспетчера из конфига

from core.handlers.sender import sender_router
from core.handlers.start import base_router

from core.middlewares.user_collector import MyMiddlewareDB


@dp.startup()
async def on_startup(dispatcher: Dispatcher) -> None:
    """Обработчик события запуска бота.

    Отправляет уведомление администратору о запуске бота и выводит сообщение в консоль.

    Args:
        dispatcher (Dispatcher): Экземпляр диспетчера aiogram.
    """
    await bot.send_message(1975977251, "Я запущен!")
    print("Бот запущен")

@dp.shutdown()
async def on_shutdown(dispatcher: Dispatcher) -> None:
    """Обработчик события остановки бота.

    Выводит сообщение в консоль при остановке бота.

    Args:
        dispatcher (Dispatcher): Экземпляр диспетчера aiogram.
    """
    print("Бот остановлен")

async def main() -> None:
    """Основная функция для запуска бота.

    Настраивает логгирование, удаляет вебхук (если он был установлен),
    и запускает бота в режиме long polling.
    """
    # Настройка логгирования
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s: %(filename)s.%(funcName)s - %(message)s"
    )

    dp.include_router(base_router)  # Приветственная ручка
    dp.include_router(sender_router)  # Регистрация хендлера из sender.py

    dp.update.middleware.register(MyMiddlewareDB()) # Регистрация миддлвари сборки пользователей

    # Удаление вебхука (если был установлен ранее)
    await bot.delete_webhook(drop_pending_updates=True)


    try:
        # Запуск бота в режиме long polling
        await dp.start_polling(bot)
    finally:
        # Закрытие сессии бота при завершении работы
        await bot.session.close()

if __name__ == "__main__":
    # Точка входа для запуска бота
    asyncio.run(main())