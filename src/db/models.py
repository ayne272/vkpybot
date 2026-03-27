from datetime import date
from sqlalchemy import BigInteger, String, Date, Integer, PrimaryKeyConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Player(Base):
    __tablename__ = "players"

    vk_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    dick: Mapped[int] = mapped_column(Integer, default=0)
    last_roll_date: Mapped[date] = mapped_column(Date, nullable=True)
    
    __table_args__ = (
        PrimaryKeyConstraint("vk_id", "chat_id", name="pk_player_chat"),
    )