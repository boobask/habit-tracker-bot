import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from asdasd import router
from database.models import async_main
import requests
import time
import database.requests as rq
from datetime import datetime
from zoneinfo import ZoneInfo

tz = ZoneInfo("Europe/Moscow")
TOKEN='8069296201:AAElkXIabj5EIvY0Bs1ODiR0hfkwEWYD8Z4'
bot = Bot(token=TOKEN)

async def Habit_tracer():
    allHabits = await rq.get_ALLhabits()
    now_=datetime.now(tz).strftime("%H:%M:%S").split(":")
    requests.get(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook").json()
    curtime=int(now_[0])*3600+int(now_[1])*60+int(now_[2])
    curweekday=datetime.now(tz).weekday()+1
    for i in allHabits:
        habit_time=int(i.time.split(":")[0])*3600+int(i.time.split(":")[1])*60
        if habit_time<=curtime<=(habit_time+29) and (int(i.weekday)==curweekday):
            await bot.send_message(i.user_id, i.name)
    print("100")



async def main():
    await async_main()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(Habit_tracer, 'interval', minutes=0.5)
    scheduler.start()
    dp = Dispatcher()
    dp.include_router(router)
    await Habit_tracer()
    await dp.start_polling(bot)
if __name__=="__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
