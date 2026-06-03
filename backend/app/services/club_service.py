from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.club import Club
from app.repositories import club_repository


def get_clubs(db: Session) -> list[Club]:
    return club_repository.get_clubs(db)


def get_club_by_id(db: Session, club_id: int) -> Club:
    club = club_repository.get_club_by_id(db, club_id)
    if club is None:
        raise HTTPException(status_code=404, detail="Club not found")

    return club
