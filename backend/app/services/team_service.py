from sqlalchemy.orm import Session

from app.models.team import Team
from app.repositories import team_repository

def get_teams(db: Session) -> list[Team]:
    return team_repository.get_teams(db)