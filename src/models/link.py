from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer

from src.database import Base

class Link(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    link: Mapped[str] = mapped_column(String)