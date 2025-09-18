import asyncio

from sqlalchemy import text, insert, select

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config.config import config

# from models import User, Base # Раскомментировать для теста
from .models import User, Base

engine = create_async_engine(config.get("SQLALCHEMY_URL"), echo=False) # Создаем асинхронный движок
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

async def inser_data(name, telegram_id):
    print(f"[DB] Добавляю пользователя: {name}, {telegram_id}")  # Лог начала
    async with session() as ss:
        try:
            get_by_id = await ss.execute(
                select(User.id).filter_by(telegram_id=int(telegram_id))
            )
            get_by_id_res = get_by_id.scalars().one_or_none()
            if get_by_id_res is None:
                await ss.execute(
                    insert(User).values([{
                        "name": name,
                        "telegram_id": int(telegram_id),
                        "is_active": True
                    }])
                )
                await ss.commit()
                print(f"[DB] Пользователь {name} ({telegram_id}) успешно добавлен!")  # Лог успеха
            else:
                print(f"[DB] Пользователь {name} ({telegram_id}) уже существует!")  # Лог существования
        except Exception as e:
            print(f"[DB] Ошибка при добавлении пользователя: {e}")  # Лог ошибки
            await ss.rollback()

async def get_all_users():
    """Функция полученяи всех пользователей"""
    emt_l = [] # Список для добавления id

    async with session() as ss:
        query = await ss.execute(
            select(User).where(User.is_active == True)
        )
        res = query.scalars().all()

        if res:
            for user in res:
                emt_l.append(user.telegram_id)
    return emt_l



if __name__ == "__main__":
    asyncio.run(get_all_users())
