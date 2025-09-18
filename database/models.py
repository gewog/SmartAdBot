from sqlalchemy import Integer, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True,
                                    index=True)

class User(Base):
    __tablename__ = "telegram_user"
    name: Mapped[str] = mapped_column(nullable=False)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    is_active: Mapped[bool]
