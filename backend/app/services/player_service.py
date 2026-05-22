from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.player import Player
from app.repositories import player_repository, team_repository


def get_players(db: Session, team_id: int | None = None) -> list[Player]:
    if team_id is not None:
        team = team_repository.get_team_by_id(db, team_id) #チームをチームidから探す
        if team is None: #チームが見つからなければ
            raise HTTPException(status_code=404, detail="Team not found") #404 not foundエラーを吐く
    
    return player_repository.get_players(db, team_id)


def get_player_by_id(db: Session, player_id: int) -> Player:
    player = player_repository.get_player_by_id(db, player_id) #プレイヤーを探す
    if player is None: #プレイヤーがいなければ
        raise HTTPException(status_code=404, detail="Player not found") #404 not foundエラーを吐く
    
    return player