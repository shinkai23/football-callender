from sqlalchemy.orm import Session

from app.models.player import Player
from app.repositories import player_repository
from app.services.football_api_service import get_person_detail, get_team_detail
from app.services.sync.club_sync_service import sync_club_from_person_data


def sync_player_from_squad_data(
    db: Session,
    player_data: dict,
    team_id: int,
    sync_club: bool = False,
) -> Player | None:
    player_id = player_data.get("id")
    name = player_data.get("name")

    if player_id is None or name is None:
        return None

    existing_player = player_repository.get_player_by_id(db, player_id)
    if existing_player is not None:
        return existing_player

    club_id = None

    if sync_club:
        person_data = get_person_detail(player_id)
        if person_data is not None:
            club = sync_club_from_person_data(db, person_data)
            if club is not None:
                club_id = club.id

    return player_repository.create_player(
        db=db,
        player_id=player_id,
        name=name,
        position=player_data.get("position") or "UNKNOWN",
        team_id=team_id,
        club_id=club_id,
    )


def sync_players_from_team(
    db: Session,
    team_id: int,
    sync_club: bool = False,
) -> list[Player]:
    team_data = get_team_detail(team_id)

    if team_data is None:
        return []

    squad = team_data.get("squad", [])
    synced_players = []

    for player_data in squad:
        player = sync_player_from_squad_data(
            db=db,
            player_data=player_data,
            team_id=team_id,
            sync_club=sync_club,
        )

        if player is None:
            continue

        synced_players.append(player)

    return synced_players
