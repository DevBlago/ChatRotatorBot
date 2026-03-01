from datetime import datetime
from sqlalchemy import select

from src.models import User
from src.database import db_helper


async def create_user(user_id: int, is_admin: bool = False) -> User:
    async with db_helper.session_factory() as session:
        user = await session.get(User, user_id)
        if user:
            return user  # если пользователь уже существует, возвращаем его

        # если не существует, создаём нового
        user = User(
            id=user_id,
            is_admin=is_admin,
            join_date=datetime.now()
        )
        session.add(user)
        await session.commit()  # обязательно делаем commit
        return user
        

async def get_user(user_id: int) -> User | None:
    async with db_helper.session_factory() as session:
        result = await session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()


async def delete_user(user_id: int) -> None:
    async with db_helper.session_factory() as session:
        async with session.begin():
            user = await session.get(User, user_id)
            if user:
                await session.delete(user)


async def set_admin(user_id: int, is_admin: bool) -> None:
    async with db_helper.session_factory() as session:
        async with session.begin():
            user = await session.get(User, user_id)
            if user:
                user.is_admin = is_admin
            else:
                user = User(id=user_id, is_admin=is_admin, join_date=datetime.now())
                session.add(user)


async def get_all_users():
    async with db_helper.session_factory() as session:
        result = await session.execute(select(User))
        return result.scalars().all()