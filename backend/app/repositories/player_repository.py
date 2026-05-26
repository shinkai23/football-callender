from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.player import Player

def create_player(db: Session, player_id: int, name: str, position: str, team_id: int, club_id: int | None = None) -> Player:
    player = Player(
        id=player_id,
        name=name,
        position=position,
        team_id=team_id,
        club_id=club_id,
    )
    db.add(player)
    db.commit()
    db.refresh(player)
    return player
    

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