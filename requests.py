from database.models import async_session
from database.models import User, Day, Habit
from sqlalchemy import select, delete

async def set_user(tg_id):
    async with async_session() as sess:
        user=await sess.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            sess.add(User(tg_id=tg_id))
            await sess.commit()

async def Init_Days():
    async with async_session() as sess:
        day=await sess.scalar(select(Day).where(Day.name == "Monday"))
        if not day:
            sess.add(Day(name="Monday"))
            sess.add(Day(name="Tuesday"))
            sess.add(Day(name="Wednesday"))
            sess.add(Day(name="Thursday"))
            sess.add(Day(name="Friday"))
            sess.add(Day(name="Saturday"))
            sess.add(Day(name="Sunday"))
            await sess.commit()

async def get_habits(day,curid):
    async with async_session() as sess:
        return await sess.scalars(select(Habit).where(Habit.weekday==day).where(Habit.user_id==curid))

async def get_ALLhabits():
    async with async_session() as sess:
        return await sess.scalars(select(Habit))

async def New_Habit(usid,tx,time1,day):
    async with async_session() as sess:
        habit=await sess.scalar(select(Habit).where(Habit.id==usid).where(Habit.name == tx).where(Habit.weekday==day).where(Habit.time==time1))
        if not habit:
            sess.add(Habit(name=tx,time=time1,weekday=day,user_id=usid))
            await sess.commit()

async def HabitIsExist(usid,tx):
    async with async_session() as sess:
        habit=await sess.scalar(select(Habit).where(Habit.id==usid and Habit.name == tx))
        if not habit:
            return 0
        return 1

async def Delete_Habit(usid,tx):
    async with async_session() as sess:
        stmt = delete(Habit).where(
            Habit.user_id == usid,
            Habit.name == tx
        )
        print(usid,tx)
        result = await sess.execute(stmt)
        await sess.commit()

        if result.rowcount == 0:
            return 0
        else:
            return 1