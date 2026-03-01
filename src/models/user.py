from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    BigInteger,
    DateTime,
    Boolean,
)

from src.database import Base

class User(Base):
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        index=True,
    )
    is_admin: Mapped[Boolean] = mapped_column(Boolean)
    join_date: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now())