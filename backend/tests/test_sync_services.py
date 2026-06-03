from sqlalchemy.orm import Session

from app.repositories import club_repository, player_repository, team_repository
from app.services.sync.club_sync_service import sync_club_from_person_data
from app.services.sync.player_sync_service import (
    sync_player_from_squad_data,
    sync_players_from_team,
)
from app.services.sync.sync_service import fetch_world_cup_matches, sync_world_cup_teams
from app.services.sync.team_sync_service import (
    sync_team_from_api_data,
    sync_teams_from_matches,
)


def test_sync_team_from_api_data_creates_team(db: Session) -> None:
    team = sync_team_from_api_data(
        db,
        {
            "id": 766,
            "name": "Japan",
            "shortName": "Japan",
            "tla": "JPN",
            "crest": "https://example.com/japan.svg",
        },
    )

    assert team is not None
    assert team.id == 766
    assert team_repository.get_team_by_id(db, 766) == team


def test_sync_teams_from_matches_skips_duplicates(db: Session) -> None:
    matches = [
        {
            "homeTeam": {"id": 766, "name": "Japan"},
            "awayTeam": {"id": 769, "name": "Mexico"},
        },
        {
            "homeTeam": {"id": 766, "name": "Japan"},
            "awayTeam": {"id": 769, "name": "Mexico"},
        },
    ]

    teams = sync_teams_from_matches(db, matches)

    assert [team.id for team in teams] == [766, 769]


def test_sync_club_from_person_data_creates_club(db: Session) -> None:
    club = sync_club_from_person_data(
        db,
        {
            "currentTeam": {
                "id": 86,
                "name": "Real Madrid CF",
                "area": {"name": "Spain"},
            }
        },
    )

    assert club is not None
    assert club_repository.get_club_by_id(db, 86).country == "Spain"


def test_sync_player_from_squad_data_without_club(db: Session) -> None:
    team_repository.create_team(db, 766, "Japan", "Japan")

    player = sync_player_from_squad_data(
        db=db,
        player_data={"id": 100, "name": "Sample Player", "position": "Midfielder"},
        team_id=766,
    )

    assert player is not None
    assert player.club_id is None
    assert player_repository.get_player_by_id(db, 100).name == "Sample Player"


def test_sync_players_from_team_uses_team_detail(monkeypatch, db: Session) -> None:
    team_repository.create_team(db, 766, "Japan", "Japan")

    monkeypatch.setattr(
        "app.services.sync.player_sync_service.get_team_detail",
        lambda team_id: {
            "squad": [
                {
                    "id": 100,
                    "name": "Sample Player",
                    "position": "Midfielder",
                }
            ]
        },
    )

    players = sync_players_from_team(db, 766)

    assert [player.name for player in players] == ["Sample Player"]


def test_fetch_world_cup_matches_returns_matches(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.services.sync.sync_service.get_competition_matches",
        lambda **kwargs: {"matches": [{"id": 1}]},
    )

    assert fetch_world_cup_matches() == [{"id": 1}]


def test_sync_world_cup_teams_uses_fetched_matches(monkeypatch, db: Session) -> None:
    monkeypatch.setattr(
        "app.services.sync.sync_service.get_competition_matches",
        lambda **kwargs: {
            "matches": [
                {
                    "homeTeam": {"id": 766, "name": "Japan"},
                    "awayTeam": {"id": 769, "name": "Mexico"},
                }
            ]
        },
    )

    teams = sync_world_cup_teams(db)

    assert [team.name for team in teams] == ["Japan", "Mexico"]
