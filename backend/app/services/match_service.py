from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.match import Match
from app.repositories import match_repository


def get_matches(db: Session) -> list[Match]:
    return match_repository.get_matches(db)


def get_match_by_id(db: Session, match_id: int) -> Match:
    match = match_repository.get_match_by_id(db, match_id)
    if match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return match
