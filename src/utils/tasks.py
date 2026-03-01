from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

from src.crud import get_all_users, get_user

scheduler = AsyncIOScheduler()


def start_scheduler():
    scheduler.start()



async def kick_user(bot: Bot, chat_id: int, user_id: int):
    user = await get_user(user_id)
    if user.is_admin:
        return

    try:
        await bot.ban_chat_member(chat_id, user_id)
        await bot.unban_chat_member(chat_id, user_id)
    except TelegramBadRequest:
        pass


def schedule_kick(
        bot: Bot,
        chat_id: int,
        user_id: int,
        join_date: datetime,
):
    run_date = join_date + timedelta(days=14)

    if run_date <= datetime.now():
        return

    scheduler.add_job(
        kick_user,
        trigger="date",
        run_date=run_date,
        args=[bot, chat_id, user_id],
        id=f"kick_{chat_id}_{user_id}",
        replace_existing=True,
    )


async def restore_jobs(bot: Bot, chat_id: int):
    users = await get_all_users()

    for user in users:
        schedule_kick(bot, chat_id, user.id, user.join_date)