import asyncio

from sqlalchemy import text, insert
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config.config import config

from models import Base, User

engine = create_async_engine(config.get("SQLALCHEMY_URL"), echo=True) # Создаем асинхронный движок
session = async_sessionmaker(bind=engine) # Создаем асинхронную фабрику сессии

async def get_session():
    try:
        async with session() as ss:
            yield ss
    finally:
        await ss.close()


async def test_func():
    """Тестовая функция"""
    async with engine.connect() as con:
        res = await con.execute(text("select version();"))
        print(res.one())

async def create_table():
    try:
        async with engine.connect() as con:
            await con.run_sync(Base.metadata.create_all)
            await con.commit()
        return True  # Успешно
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")
        return False  # Неудача

async def inser_data():
    """Функция вставки пользователя"""
    async with session() as ss:
        query = await ss.execute(
            insert(User).values([{
                "name": "Veronika Tsvetkova",
                "telegram_id": int("1975977251"),
                "is_active": True
            },])
        )
        await ss.commit()
    return "Ok"



if __name__ == "__main__":
    asyncio.run(inser_data())
