from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.player import PlayerResponse
from app.services import player_service


router = APIRouter(prefix="/api/players", tags=["players"]) # https://football_callender/api/players みたいな(実際のurlとは違うけど)


@router.get("", response_model=list[PlayerResponse]) # https://football_callender/api/players
def read_players(
    team_id: int | None = None,
    db: Session = Depends(get_db), # db = Depends(get_db), Dependsはjavaでいう継承？みたいな概念ぽい 正確には依存性注入
                                    # Deoendsについて (https://note.com/engneer_hino/n/n02a191910992)
):
    return player_service.get_players(db, team_id)

@router.get("/{player_id}", response_model=PlayerResponse) # https://football_callender/api/players/{player_id}
def read_player(
    player_id: int,
    db: Session = Depends(get_db),
):
    return player_service.get_player_by_id(db, player_id)