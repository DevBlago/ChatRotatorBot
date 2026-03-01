from src.models import Link
from src.database import db_helper


async def get_link(link_id: int = 1) -> str | None:
    async with db_helper.session_factory() as session:
        async with session.begin():
            link = await session.get(Link, link_id)
            return link.link if link else None
        

async def update_link(link_id: int, new_link: str) -> None:
    async with db_helper.session_factory() as session:
        async with session.begin():
            link = await session.get(Link, link_id)
            
            if link:
                link.link = new_link
            else:
                link = Link(id=link_id, link=new_link)
                session.add(link)