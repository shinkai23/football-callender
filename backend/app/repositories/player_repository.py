from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.player import Player


def get_players(db: Session, team_id: int | None = None) -> list[Player]:
    statement = select(Player)

    if team_id is not None:
        statement = statement.where(
            Player.team_id == team_id,
        )
    return db.scalars(statement).all()


def get_player_by_id(db: Session, player_id: int) -> Player | None:
    statement = select(Player).where(
        Player.id == player_id,
    )
    return db.scalar(statement)