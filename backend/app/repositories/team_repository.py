from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.team import Team


def get_teams(db: Session) -> list[Team]:
    statement = select(Team)
    return db.scalars(statement).all()


def get_team_by_id(db: Session, team_id: int) -> Team | None:
    statement = select(Team).where(
        Team.id == team_id,
    )
    return db.scalar(statement)