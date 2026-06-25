from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.team import Team


def create_team(
    db: Session,
    team_id: int,
    name: str,
    country: str,
    short_name: str | None = None,
    tla: str | None = None,
    crest: str | None = None,
) -> Team:
    team = Team(
        id=team_id,
        name=name,
        country=country,
        short_name=short_name,
        tla=tla,
        crest=crest,
    )
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


def get_teams(db: Session) -> list[Team]:
    statement = select(Team)
    return db.scalars(statement).all()


def get_team_by_id(db: Session, team_id: int) -> Team | None:
    statement = select(Team).where(
        Team.id == team_id,
    )
    return db.scalar(statement)


def update_team(
    db: Session,
    team: Team,
    *,
    name: str,
    country: str,
    short_name: str | None,
    tla: str | None,
    crest: str | None,
) -> Team:
    team.name = name
    team.country = country
    team.short_name = short_name
    team.tla = tla
    team.crest = crest

    db.commit()
    db.refresh(team)
    return team
