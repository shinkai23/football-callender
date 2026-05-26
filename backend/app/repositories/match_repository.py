from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.match import Match


def create_match(
    db: Session,
    match_id: int,
    kickoff_at: datetime,
    stage: str,
    venue: str,
    home_team_id: int,
    away_team_id: int,
) -> Match:
    match = Match(
        id=match_id,
        kickoff_at=kickoff_at,
        stage=stage,
        venue=venue,
        home_team_id=home_team_id,
        away_team_id=away_team_id,
    )
    db.add(match)
    db.commit()
    db.refresh(match)
    return match


def get_matches(db: Session) -> list[Match]:
    statement = (
        select(Match)
        .options(
            joinedload(Match.home_team),
            joinedload(Match.away_team),
        )
    )
    return db.scalars(statement).unique().all()


def get_match_by_id(db: Session, match_id: int) -> Match | None:
    statement = (
        select(Match)
        .where(Match.id == match_id)
        .options(
            joinedload(Match.home_team),
            joinedload(Match.away_team),
        )
    )
    return db.scalar(statement)
