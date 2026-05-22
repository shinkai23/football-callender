from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.match import MatchResponse
from app.services import match_service

router = APIRouter(prefix="/api/v1/matches", tags=["matches"])


@router.get("", response_model=list[MatchResponse])
def read_matches(db: Session = Depends(get_db)):
    return match_service.get_matches(db)


@router.get("/{match_id}", response_model=MatchResponse)
def read_match(
    match_id: int,
    db: Session = Depends(get_db),
):
    return match_service.get_match_by_id(db, match_id)
