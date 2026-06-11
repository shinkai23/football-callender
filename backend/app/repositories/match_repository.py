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
    competition_code: str = "WC",
    status: str = "SCHEDULED",
    home_score: int | None = None,
    away_score: int | None = None,
) -> Match:
    match = Match(
        id=match_id,
        kickoff_at=kickoff_at,
        stage=stage,
        venue=venue,
        home_team_id=home_team_id,
        away_team_id=away_team_id,
        competition_code=competition_code,
        status=status,
        home_score=home_score,
        away_score=away_score,
    )
    db.add(match)
    db.commit()
    db.refresh(match)
    return match


def update_match(
    db: Session,
    match: Match,
    *,
    kickoff_at: datetime,
    stage: str,
    venue: str,
    home_team_id: int,
    away_team_id: int,
    competition_code: str,
    status: str,
    home_score: int | None,
    away_score: int | None,
) -> Match:
    match.kickoff_at = kickoff_at
    match.stage = stage
    match.venue = venue
    match.home_team_id = home_team_id
    match.away_team_id = away_team_id
    match.competition_code = competition_code
    match.status = status
    match.home_score = home_score
    match.away_score = away_score
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
