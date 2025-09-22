"""
Модуль для асинхронного взаимодействия с базой данных через SQLAlchemy.

Этот модуль предоставляет функции для:
- Создания подключения к базе данных.
- Создания таблиц.
- Добавления и получения данных о пользователях.

Зависимости:
- sqlalchemy: Для асинхронной работы с базой данных.
- config: Для получения конфигурации подключения к базе данных.
- models: Для работы с моделями базы данных.
"""

import asyncio
from typing import List

from sqlalchemy import text, insert, select

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config.config import config

# from models import User, Base # Раскомментировать для теста
from .models import User, Base

engine = create_async_engine(
    config.get("SQLALCHEMY_URL"), echo=False
)  # Создаем асинхронный движок
session = async_sessionmaker(bind=engine)  # Создаем асинхронную фабрику сессии


async def get_session():
    """
    Контекстный менеджер для получения асинхронной сессии базы данных.

    Yields:
        AsyncSession: Асинхронная сессия базы данных.
    """
    try:
        async with session() as ss:
            yield ss
    finally:
        await ss.close()


async def test_func():
    """
    Тестовая функция для проверки подключения к базе данных.

    Выполняет запрос на получение версии базы данных.
    """
    async with engine.connect() as con:
        res = await con.execute(text("select version();"))
        print(res.one())


async def create_table() -> bool:
    """
    Создает все таблицы в базе данных на основе моделей.

    Returns:
        bool: True, если таблицы успешно созданы, иначе False.
    """
    try:
        async with engine.connect() as con:
            await con.run_sync(Base.metadata.create_all)
            await con.commit()
        return True  # Успешно
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")
        return False  # Неудача


async def inser_data(name, telegram_id) -> None:
    """
    Добавляет нового пользователя в базу данных, если его ещё нет.

    Args:
        name (str): Полное имя пользователя.
        telegram_id (int): Уникальный идентификатор пользователя в Telegram.
    """
    print(f"[DB] Добавляю пользователя: {name}, {telegram_id}")  # Лог начала
    async with session() as ss:
        try:
            get_by_id = await ss.execute(
                select(User.id).filter_by(telegram_id=int(telegram_id))
            )
            get_by_id_res = get_by_id.scalars().one_or_none()
            if get_by_id_res is None:
                await ss.execute(
                    insert(User).values(
                        [
                            {
                                "name": name,
                                "telegram_id": int(telegram_id),
                                "is_active": True,
                            }
                        ]
                    )
                )
                await ss.commit()
                print(
                    f"[DB] Пользователь {name} ({telegram_id}) успешно добавлен!"
                )  # Лог успеха
            else:
                print(
                    f"[DB] Пользователь {name} ({telegram_id}) уже существует!"
                )  # Лог существования
        except Exception as e:
            print(f"[DB] Ошибка при добавлении пользователя: {e}")  # Лог ошибки
            await ss.rollback()


async def get_all_users() -> List[int]:
    """
    Получает список активных пользователей из базы данных.

    Returns:
        List[int]: Список идентификаторов активных пользователей.
    """
    emt_l = []  # Список для добавления id

    async with session() as ss:
        query = await ss.execute(select(User).where(User.is_active == True))
        res = query.scalars().all()

        if res:
            for user in res:
                emt_l.append(user.telegram_id)
    return emt_l


if __name__ == "__main__":
    asyncio.run(get_all_users())
