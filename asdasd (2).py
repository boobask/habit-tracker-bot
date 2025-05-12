from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import database.requests as rq
import key as kb

router = Router()

days=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

class NewHabit(StatesGroup):
    HabitDate=State()
    HabitTime=State()
    HabitText=State()
    DeleteHabit=State()

def correct_time(t):
    rap=t.split(":")
    if len(rap)>1:
        if (rap[0].isdigit() and (rap[1].isdigit() or (rap[1][0]=="0" and rap[1][1].isdigit()))):
            return 4<=len(t)<=5 and 0<=int(rap[0])<=23 and 0<=int(rap[1])<=59
    return 0

def correct_day(d):
    return d in days

@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await rq.Init_Days()
    await message.answer("Привет!", reply_markup=kb.main)
    await message.reply("Как дела?")

@router.message(F.text=="Новая привычка")
async def Creat_Habit(message: Message, state: FSMContext):
    await state.set_state(NewHabit.HabitText)
    await message.answer("Введите текст привычки")

@router.message(NewHabit.HabitText)
async def Habit_day(message: Message, state: FSMContext):
    await state.update_data(HabitText=message.text)
    await state.set_state(NewHabit.HabitTime)
    await message.answer("Введите время (Например 9:00)")

@router.message(NewHabit.HabitTime)
async def Habit_day(message: Message, state: FSMContext):
    if (correct_time(message.text)):
        await state.update_data(HabitTime=message.text)
        await state.set_state(NewHabit.HabitDate)
        await message.answer("Введите день недели (Например Monday)")
    else:
        await message.answer("Время введено некорректно!")
        await message.answer("Введите время (Например 9:00)")

@router.message(NewHabit.HabitDate)
async def AddHabit(message: Message, state: FSMContext):
    if(correct_day(message.text)):
        await state.update_data(HabitDate=message.text)
        await message.answer("Привычка добавлена!")
        data = await state.get_data()
        await rq.New_Habit(message.from_user.id,data["HabitText"],data["HabitTime"],days.index(data["HabitDate"])+1)
        await state.clear()
    else:
        await message.answer("День введён некорректно!")
        await message.answer("Введите день недели (Например Monday)")

@router.message(F.text=="Мои привычки")
async def choose_day(message: Message):
    await message.answer("Выберите день недели",reply_markup=kb.weekHabits)

@router.callback_query(F.data=="1")
async def AllHabits(callback: CallbackQuery):
    allHabits = await rq.get_habits(1,callback.from_user.id)
    cnt=0
    for habit1 in allHabits:
        cnt+=1
        await callback.message.answer(habit1.name)
        await callback.message.answer(habit1.time)
    if cnt==0:
        await callback.message.answer("У вас нет привычек в этот день")

@router.callback_query(F.data=="2")
async def AllHabits(callback: CallbackQuery):
    allHabits = await rq.get_habits(2,callback.from_user.id)
    cnt=0
    for habit1 in allHabits:
        cnt+=1
        await callback.message.answer(habit1.name)
        await callback.message.answer(habit1.time)
    if cnt==0:
        await callback.message.answer("У вас нет привычек в этот день")

@router.callback_query(F.data=="3")
async def AllHabits(callback: CallbackQuery):
    allHabits = await rq.get_habits(3,callback.from_user.id)
    cnt=0
    for habit1 in allHabits:
        cnt+=1
        await callback.message.answer(habit1.name)
        await callback.message.answer(habit1.time)
    if cnt==0:
        await callback.message.answer("У вас нет привычек в этот день")

@router.callback_query(F.data=="4")
async def AllHabits(callback: CallbackQuery):
    allHabits = await rq.get_habits(4,callback.from_user.id)
    cnt=0
    for habit1 in allHabits:
        cnt+=1
        await callback.message.answer(habit1.name)
        await callback.message.answer(habit1.time)
    if cnt==0:
        await callback.message.answer("У вас нет привычек в этот день")

@router.callback_query(F.data=="5")
async def AllHabits(callback: CallbackQuery):
    allHabits = await rq.get_habits(5,callback.from_user.id)
    cnt=0
    for habit1 in allHabits:
        cnt+=1
        await callback.message.answer(habit1.name)
        await callback.message.answer(habit1.time)
    if cnt==0:
        await callback.message.answer("У вас нет привычек в этот день")

@router.callback_query(F.data=="6")
async def AllHabits(callback: CallbackQuery):
    allHabits = await rq.get_habits(6,callback.from_user.id)
    cnt=0
    for habit1 in allHabits:
        cnt+=1
        await callback.message.answer(habit1.name)
        await callback.message.answer(habit1.time)
    if cnt==0:
        await callback.message.answer("У вас нет привычек в этот день")

@router.callback_query(F.data=="7")
async def AllHabits(callback: CallbackQuery):
    allHabits = await rq.get_habits(7,callback.from_user.id)
    cnt=0
    for habit1 in allHabits:
        cnt+=1
        await callback.message.answer(habit1.name)
        await callback.message.answer(habit1.time)
    if cnt==0:
        await callback.message.answer("У вас нет привычек в этот день")

@router.message(F.text=="Удалить привычку")
async def Del_Habit(message: Message, state: FSMContext):
    await state.set_state(NewHabit.DeleteHabit)
    await message.answer("Введите текст привычки, которую вы хотите удалить")

@router.message(NewHabit.DeleteHabit)
async def Del(message: Message, state: FSMContext):
    if(await rq.Delete_Habit(message.from_user.id, message.text)):
        await message.answer("Привычка успешно удалена")
        await state.clear()
    else:
        await message.answer("Такой привычки нет")
        await state.clear()
