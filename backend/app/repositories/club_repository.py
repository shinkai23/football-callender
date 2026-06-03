from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.club import Club


def get_club_by_id(db: Session, club_id: int) -> Club | None:
    statement = select(Club).where(
        Club.id == club_id,
    )
    return db.scalar(statement)


def create_club(
    db: Session,
    club_id: int,
    name: str,
    country: str,
    league: str = "",
) -> Club:
    club = Club(
        id=club_id,
        name=name,
        country=country,
        league=league,
    )
    db.add(club)
    db.commit()
    db.refresh(club)
    return club


def get_clubs(db: Session) -> list[Club]:
    statement = select(Club)
    return db.scalars(statement).all()
