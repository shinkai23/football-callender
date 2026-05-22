from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.team import TeamResponse
from app.services import team_service

router = APIRouter(prefix="/api/teams", tags=["teams"])


@router.get("", response_model=list[TeamResponse])
def read_teams(db: Session = Depends(get_db)):
    return team_service.get_teams(db)