from datetime import datetime

from sqlalchemy.orm import Session

from app.models.match import Match
from app.models.team import Team
from app.repositories import match_repository, team_repository


def _upsert_team(db: Session, team_data: dict) -> Team | None:
    team_id = team_data.get("id")
    name = team_data.get("name")
    if team_id is None or name is None:
        return None

    existing_team = team_repository.get_team_by_id(db, team_id)
    if existing_team is not None:
        return existing_team

    return team_repository.create_team(
        db=db,
        team_id=team_id,
        name=name,
        country=name,
        short_name=team_data.get("shortName"),
        tla=team_data.get("tla"),
        crest=team_data.get("crest"),
    )


def _upsert_match(db: Session, match_data: dict) -> Match | None:
    match_id = match_data.get("id")
    home_team_id = (match_data.get("homeTeam") or {}).get("id")
    away_team_id = (match_data.get("awayTeam") or {}).get("id")
    kickoff_raw = match_data.get("utcDate")

    if (
        match_id is None
        or home_team_id is None
        or away_team_id is None
        or kickoff_raw is None
    ):
        return None

    existing_match = match_repository.get_match_by_id(db, match_id)
    if existing_match is not None:
        return existing_match

    kickoff_at = datetime.fromisoformat(kickoff_raw.replace("Z", "+00:00"))
    stage = match_data.get("stage") or "UNKNOWN"
    venue = match_data.get("venue") or "UNKNOWN"

    return match_repository.create_match(
        db=db,
        match_id=match_id,
        kickoff_at=kickoff_at,
        stage=stage,
        venue=venue,
        home_team_id=home_team_id,
        away_team_id=away_team_id,
    )


def sync_teams_and_matches_from_matches(
    db: Session,
    matches: list[dict],
) -> tuple[list[Team], list[Match]]:
    synced_teams: list[Team] = []
    synced_matches: list[Match] = []
    synced_team_ids: set[int] = set()

    for match_data in matches:
        for side in ("homeTeam", "awayTeam"):
            team_data = match_data.get(side)
            if not team_data:
                continue

            team_id = team_data.get("id")
            if team_id is None or team_id in synced_team_ids:
                continue

            team = _upsert_team(db, team_data)
            if team is None:
                continue

            synced_teams.append(team)
            synced_team_ids.add(team_id)

        match = _upsert_match(db, match_data)
        if match is not None:
            synced_matches.append(match)

    return synced_teams, synced_matches
