from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.club import Club


def get_clubs(db: Session) -> list[Club]:
    statement = select(Club)
    return db.scalars(statement).all()


def get_club_by_id(db: Session, club_id: int) -> Club | None:
    statement = select(Club).where(
        Club.id == club_id,
    )
    return db.scalar(statement)
