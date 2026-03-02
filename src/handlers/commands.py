from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    ChatMemberUpdated,
)
from datetime import datetime

from src.lexicon import Messages
from aiogram.enums import ChatType
from src.utils import (
    create_invite_link,
    delete_old_invite_link,
    schedule_kick,
    scheduler,
)
from src.keyboards import admin_keyboard
from src.crud import (
    get_link,
    update_link,
    create_user,
    get_user,
)

router = Router()


@router.message(F.chat.type == ChatType.PRIVATE)
async def process_any_command(message: Message) -> None:
    user = await create_user(user_id=message.from_user.id)
    link = await get_link(link_id=1)

    if not link:
        link = await create_invite_link(message.bot)
        await update_link(link_id=1, new_link=link)

    await message.answer(
        text=Messages.link(link),
        reply_markup=admin_keyboard() if user.is_admin else None,
    )


@router.callback_query(F.data == "refresh_link")
async def process_refresh_link_command(callback: CallbackQuery) -> None:
    await callback.answer()
    user = await get_user(user_id=callback.from_user.id)

    new_link = await create_invite_link(callback.bot)
    old_link = await get_link(link_id=1)
    await delete_old_invite_link(
        bot=callback.bot,
        invite_link=old_link,
    )
    await update_link(link_id=1, new_link=new_link)

    await callback.message.edit_text(
        text=Messages.link(new_link),
        reply_markup=admin_keyboard() if user.is_admin else None,
    )


@router.chat_member()
async def on_user_join(event: ChatMemberUpdated, bot):
    old_status = event.old_chat_member.status
    new_status = event.new_chat_member.status

    if old_status in ("left", "kicked") and new_status == "member":
        user_id = event.new_chat_member.user.id
        user = await get_user(user_id)

        if user.is_admin:
            return

        user = await create_user(user_id=user_id)
        user.join_date = datetime.now()

        schedule_kick(
            bot=bot,
            chat_id=event.chat.id,
            user_id=user_id,
            join_date=user.join_date,
        )


@router.chat_member()
async def on_user_left(event: ChatMemberUpdated):
    old_status = event.old_chat_member.status
    new_status = event.new_chat_member.status

    if old_status == "member" and new_status in ("left", "kicked"):
        job_id = f"kick_{event.chat.id}_{event.old_chat_member.user.id}"

        if scheduler.get_job(job_id):
            scheduler.remove_job(job_id)