import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combined import AndTrigger
from apscheduler.triggers.cron import CronTrigger
from datetime import time
import pytz

# Настройка базы данных
def init_db():
    conn = sqlite3.connect('habits.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            user_id INTEGER,
            habit_name TEXT,
            streak INTEGER DEFAULT 0,
            reminder_days TEXT,  # Дни недели (например, "mon,wed,fri")
            reminder_time TEXT,   # Время (например, "09:00")
            PRIMARY KEY (user_id, habit_name)
        )
    ''')
    conn.commit()
    conn.close()

# Добавление привычки
def add_habit(user_id, habit_name, reminder_days=None, reminder_time=None):
    conn = sqlite3.connect('habits.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO habits (user_id, habit_name, reminder_days, reminder_time)
        VALUES (?, ?, ?, ?)
    ''', (user_id, habit_name, reminder_days, reminder_time))
    conn.commit()
    conn.close()

# Получение привычек с напоминаниями
def get_habits_with_reminders():
    conn = sqlite3.connect('habits.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, habit_name, reminder_days, reminder_time FROM habits WHERE reminder_days IS NOT NULL')
    habits = cursor.fetchall()
    conn.close()
    return habits

# Установка напоминаний
def schedule_reminders(context: CallbackContext):
    habits = get_habits_with_reminders()
    for user_id, habit_name, reminder_days, reminder_time in habits:
        days = [day.strip() for day in reminder_days.split(",")]
        hour, minute = map(int, reminder_time.split(":"))
        
        for day in days:
            trigger = CronTrigger(
                day_of_week=day,
                hour=hour,
                minute=minute,
                timezone=pytz.timezone('Europe/Moscow')  # Укажите свою таймзону
            )
            context.job_queue.run_once(
                callback=lambda ctx: send_reminder(ctx, user_id, habit_name),
                when=trigger,
                name=f"{user_id}_{habit_name}_{day}"
            )

# Отправка напоминания
def send_reminder(context: CallbackContext, user_id: int, habit_name: str):
    context.bot.send_message(
        chat_id=user_id,
        text=f"⏰ Напоминание: пора выполнить привычку '{habit_name}'!"
    )

# Обработчик команды /add
def add(update: Update, context: CallbackContext):
    update.message.reply_text("📝 Введите название привычки:")
    return "GET_HABIT_NAME"

# Обработчик ввода названия привычки
def get_habit_name(update: Update, context: CallbackContext):
    habit_name = update.message.text
    context.user_data['habit_name'] = habit_name
    update.message.reply_text(
        "📅 В какие дни недели напоминать? (Например: mon,wed,fri)\n"
        "Доступные дни: mon, tue, wed, thu, fri, sat, sun"
    )
    return "GET_REMINDER_DAYS"

# Обработчик ввода дней недели
def get_reminder_days(update: Update, context: CallbackContext):
    days_input = update.message.text.lower()
    valid_days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    days = [day.strip() for day in days_input.split(",")]
    
    if not all(day in valid_days for day in days):
        update.message.reply_text("❌ Некорректные дни. Попробуйте ещё раз.")
        return "GET_REMINDER_DAYS"
    
    context.user_data['reminder_days'] = days_input
    update.message.reply_text("⏰ Во сколько напоминать? (Формат: HH:MM, например 09:00)")
    return "GET_REMINDER_TIME"

# Обработчик ввода времени
def get_reminder_time(update: Update, context: CallbackContext):
    time_input = update.message.text
    try:
        hour, minute = map(int, time_input.split(":"))
        if not (0 <= hour < 24 and 0 <= minute < 60):
            raise ValueError
    except ValueError:
        update.message.reply_text("❌ Некорректное время. Попробуйте ещё раз.")
        return "GET_REMINDER_TIME"
    
    habit_name = context.user_data['habit_name']
    reminder_days = context.user_data['reminder_days']
    reminder_time = time_input
    
    add_habit(update.effective_user.id, habit_name, reminder_days, reminder_time)
    update.message.reply_text(
        f"✅ Привычка '{habit_name}' добавлена!\n"
        f"⏰ Напоминания: {reminder_days} в {reminder_time}"
    )
    
    # Перезапускаем планировщик
    schedule_reminders(context)
    return -1

def main():
    init_db()
    updater = Updater(7123542145:AAEGrZPSzbYgVhJihw4dzvsFw5iq6oWTrdo, use_context=True)  # Замените на свой токен
    dp = updater.dispatcher

    # Обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("add", add))
    dp.add_handler(CommandHandler("list", list_habits))
    dp.add_handler(CommandHandler("remove", remove))

    # Обработчики состояний
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, get_habit_name), group=1)
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, get_reminder_days), group=2)
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, get_reminder_time), group=3)

    # Обработчики кнопок
    dp.add_handler(CallbackQueryHandler(button_click, pattern="^complete_"))
    dp.add_handler(CallbackQueryHandler(remove_habit_handler, pattern="^remove_"))

    # Запуск планировщика напоминаний
    updater.job_queue.run_once(schedule_reminders, when=0)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
