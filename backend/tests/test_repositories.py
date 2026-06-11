from datetime import datetime

from sqlalchemy.orm import Session

from app.repositories import (
    club_repository,
    match_repository,
    player_repository,
    team_repository,
)


def test_team_repository_creates_and_reads_team(db: Session) -> None:
    created = team_repository.create_team(
        db=db,
        team_id=766,
        name="Japan",
        country="Japan",
        short_name="Japan",
        tla="JPN",
        crest="https://example.com/japan.svg",
    )

    found = team_repository.get_team_by_id(db, created.id)

    assert found is not None
    assert found.id == 766
    assert found.tla == "JPN"
    assert team_repository.get_teams(db) == [found]


def test_club_repository_creates_and_reads_club(db: Session) -> None:
    created = club_repository.create_club(
        db=db,
        club_id=86,
        name="Real Madrid CF",
        country="Spain",
        league="Primera Division",
    )

    found = club_repository.get_club_by_id(db, created.id)

    assert found is not None
    assert found.name == "Real Madrid CF"
    assert club_repository.get_clubs(db) == [found]


def test_player_repository_filters_by_team(db: Session) -> None:
    team_repository.create_team(db, 766, "Japan", "Japan")
    team_repository.create_team(db, 769, "Mexico", "Mexico")
    player_repository.create_player(db, 100, "Japan Player", "Forward", 766)
    player_repository.create_player(db, 101, "Mexico Player", "Defender", 769)

    players = player_repository.get_players(db, team_id=766)

    assert [player.name for player in players] == ["Japan Player"]
    assert player_repository.get_player_by_id(db, 100).position == "Forward"


def test_match_repository_loads_teams(db: Session) -> None:
    team_repository.create_team(db, 766, "Japan", "Japan")
    team_repository.create_team(db, 769, "Mexico", "Mexico")
    match_repository.create_match(
        db=db,
        match_id=537327,
        kickoff_at=datetime(2026, 6, 11, 19, 0),
        stage="GROUP_STAGE",
        venue="Estadio Azteca",
        home_team_id=769,
        away_team_id=766,
        competition_code="WC",
        status="SCHEDULED",
    )

    match = match_repository.get_match_by_id(db, 537327)

    assert match is not None
    assert match.home_team.name == "Mexico"
    assert match.away_team.name == "Japan"
    assert match.competition_code == "WC"
    assert match.status == "SCHEDULED"
    assert match.home_score is None
    assert match.away_score is None
    assert len(match_repository.get_matches(db)) == 1


def test_match_repository_updates_match(db: Session) -> None:
    team_repository.create_team(db, 766, "Japan", "Japan")
    team_repository.create_team(db, 769, "Mexico", "Mexico")
    created = match_repository.create_match(
        db=db,
        match_id=537327,
        kickoff_at=datetime(2026, 6, 11, 19, 0),
        stage="GROUP_STAGE",
        venue="Estadio Azteca",
        home_team_id=769,
        away_team_id=766,
        competition_code="WC",
        status="SCHEDULED",
    )

    updated = match_repository.update_match(
        db,
        created,
        kickoff_at=datetime(2026, 6, 11, 20, 0),
        stage="GROUP_STAGE",
        venue="Estadio Azteca",
        home_team_id=769,
        away_team_id=766,
        competition_code="WC",
        status="FINISHED",
        home_score=2,
        away_score=1,
    )

    assert updated.status == "FINISHED"
    assert updated.home_score == 2
    assert updated.away_score == 1
    assert updated.kickoff_at == datetime(2026, 6, 11, 20, 0)
