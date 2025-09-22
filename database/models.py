"""
Модуль для работы с моделями базы данных с использованием SQLAlchemy.

Этот модуль определяет базовые и пользовательские модели для работы с базой данных.
Основные компоненты:
- Базовая модель `Base` для наследования другими моделями.
- Модель `User` для хранения данных о пользователях Telegram.

Зависимости:
- sqlalchemy: Для работы с ORM и определением моделей базы данных.
"""

from sqlalchemy import Integer, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Базовая модель для всех таблиц в базе данных.

    Атрибуты:
        id (Mapped[int]): Первичный ключ, автоинкрементное целое число.
    """
    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True,
                                    index=True)

class User(Base):
    """
    Модель пользователя Telegram.

    Хранит информацию о пользователях, взаимодействующих с ботом.
    Атрибуты:
        name (Mapped[str]): Полное имя пользователя.
        telegram_id (Mapped[int]): Уникальный идентификатор пользователя в Telegram.
        is_active (Mapped[bool]): Флаг активности пользователя.
    """
    __tablename__ = "telegram_user"
    name: Mapped[str] = mapped_column(nullable=False)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    is_active: Mapped[bool]
