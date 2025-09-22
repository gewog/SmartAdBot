"""
Telegram бот на основе aiogram с поддержкой FSM (finite state machine).

Этот модуль инициализирует бота, диспетчер и загружает конфигурацию из .env файла.
Основные компоненты:
- Bot: Экземпляр бота для взаимодействия с Telegram API.
- Dispatcher: Диспетчер для обработки сообщений и событий.
- MemoryStorage: Хранилище для состояний FSM в оперативной памяти.

Переменные окружения:
- TOKEN: Токен Telegram Bot API.
- ADMIN_ID: Идентификатор администратора бота.
- SQLALCHEMY_URL: URL для подключения к базе данных (если используется).
"""
import os
from pathlib import Path
from aiogram import Bot, Dispatcher
from dotenv import dotenv_values
from aiogram.fsm.storage.memory import MemoryStorage

# Попробуем загрузить из .env (для локальной разработки)
env_path = Path(__file__).parent / ".env"
config = dotenv_values(env_path) if env_path.exists() else {}

# Получаем переменные окружения (из .env или из os.environ)
API_TOKEN = config.get("TOKEN") or os.environ.get("TOKEN")
ADMIN = config.get("ADMIN_ID") or os.environ.get("ADMIN_ID")
SQLALCHEMY_URL = config.get("SQLALCHEMY_URL") or os.environ.get("SQLALCHEMY_URL")

# Проверяем, что все переменные загружены
if not all([API_TOKEN, ADMIN, SQLALCHEMY_URL]):
    raise ValueError(f"Отсутствуют обязательные переменные окружения. API_TOKEN: {API_TOKEN}, ADMIN: {ADMIN}, SQLALCHEMY_URL: {SQLALCHEMY_URL}")

# Инициализация бота
bot: Bot = Bot(token=API_TOKEN)

# Инициализация диспетчера с хранилищем для FSM
dp: Dispatcher = Dispatcher(storage=MemoryStorage())


# from pathlib import Path
#
#
# from aiogram import Bot, Dispatcher
# from dotenv import dotenv_values
#
# from aiogram.fsm.storage.memory import MemoryStorage
#
#
# # Путь к .env файлу
# env_path = Path(__file__).parent / ".env"
# # Загрузка конфигурации
# config = dotenv_values(env_path)
#
#
# # Извлечение токена и других параметров из конфигурации
# API_TOKEN: str = config["TOKEN"]
# ADMIN = int(config["ADMIN_ID"])
# SQLALCHEMY_URL = config["SQLALCHEMY_URL"]
#
# # Инициализация бота
# bot: Bot = Bot(token=API_TOKEN)
#
# # Инициализация диспетчера с хранилищем для FSM
# dp: Dispatcher = Dispatcher(storage=MemoryStorage())
#
# # Для отладки (раскомментировать при необходимости)
# # print("Loaded .env:", config)
