from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.club import ClubResponse
from app.services import club_service


router = APIRouter(prefix="/api/clubs", tags=["clubs"])


@router.get("", response_model=list[ClubResponse])
def read_clubs(db: Session = Depends(get_db)):
    return club_service.get_clubs(db)


@router.get("/{club_id}", response_model=ClubResponse)
def read_club(
    club_id: int,
    db: Session = Depends(get_db),
):
    return club_service.get_club_by_id(db, club_id)
