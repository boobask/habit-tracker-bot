from sqlalchemy import String, ForeignKey, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url="sqlite+aiosqlite:///db.sqlite3")

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs,DeclarativeBase):
    pass

class User(Base):
    __tablename__="users"

    id: Mapped[int]= mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)

class Day(Base):
    __tablename__="days"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(10))

class Habit(Base):
    __tablename__="habits"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] =  mapped_column(String(20))
    weekday: Mapped[int] = mapped_column(ForeignKey("days.name"))
    time: Mapped[str] = mapped_column(String(20))
    user_id = mapped_column(BigInteger)

async def async_main():
    async with engine.begin() as abd:
        await abd.run_sync(Base.metadata.create_all)