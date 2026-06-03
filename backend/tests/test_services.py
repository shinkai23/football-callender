import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.services import club_service, match_service, player_service, team_service


def test_team_service_returns_teams(seeded_db: Session) -> None:
    teams = team_service.get_teams(seeded_db)

    assert {team.name for team in teams} == {"Japan", "Mexico"}


def test_club_service_returns_club(seeded_db: Session) -> None:
    club = club_service.get_club_by_id(seeded_db, 86)

    assert club.name == "Real Madrid CF"


def test_club_service_raises_404_for_missing_club(seeded_db: Session) -> None:
    with pytest.raises(HTTPException) as exc_info:
        club_service.get_club_by_id(seeded_db, 999)

    assert exc_info.value.status_code == 404


def test_player_service_filters_by_existing_team(seeded_db: Session) -> None:
    players = player_service.get_players(seeded_db, team_id=766)

    assert [player.name for player in players] == ["Sample Player"]


def test_player_service_raises_404_for_missing_team(seeded_db: Session) -> None:
    with pytest.raises(HTTPException) as exc_info:
        player_service.get_players(seeded_db, team_id=999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Team not found"


def test_player_service_raises_404_for_missing_player(seeded_db: Session) -> None:
    with pytest.raises(HTTPException) as exc_info:
        player_service.get_player_by_id(seeded_db, 999)

    assert exc_info.value.status_code == 404


def test_match_service_returns_match(seeded_db: Session) -> None:
    match = match_service.get_match_by_id(seeded_db, 537327)

    assert match.stage == "GROUP_STAGE"


def test_match_service_raises_404_for_missing_match(seeded_db: Session) -> None:
    with pytest.raises(HTTPException) as exc_info:
        match_service.get_match_by_id(seeded_db, 999)

    assert exc_info.value.status_code == 404
