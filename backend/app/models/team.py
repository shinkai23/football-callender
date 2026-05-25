from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)
    short_name: Mapped[str | None] = mapped_column(nullable=True) # 国の略称
    tla: Mapped[str | None] = mapped_column(nullable=True) # 国の3文字表記 JPNとか
    crest: Mapped[str | None] = mapped_column(nullable=True) # 国旗とかの写真url

    players: Mapped[list["Player"]] = relationship(back_populates="team")