from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.match import Match


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
