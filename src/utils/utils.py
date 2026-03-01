import logging

from aiogram import Bot
from aiogram.types import ChatInviteLink

from src.lexicon import System
from src.core import settings


logger = logging.getLogger(__name__)


async def create_invite_link(bot: Bot) -> ChatInviteLink:
    new_link = await bot.create_chat_invite_link(
        chat_id=settings.bot.group,
        name=System.name_link,
    )
    logging.info("New link created")

    return new_link.invite_link


async def delete_old_invite_link(bot: Bot, invite_link: str) -> None:
    await bot.revoke_chat_invite_link(
        chat_id=settings.bot.group,
        invite_link=invite_link
    )