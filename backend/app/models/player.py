from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    position: Mapped[str] = mapped_column(nullable=False)

    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    club_id: Mapped[int] = mapped_column(ForeignKey("clubs.id"), nullable=True)

    team: Mapped["Team"] = relationship(back_populates="players")
    club: Mapped["Club | None"] = relationship(back_populates="players")