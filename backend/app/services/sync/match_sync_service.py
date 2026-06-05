from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from app.models.match import Match
from app.repositories import match_repository


def sync_match_from_api_data(db: Session, match_data: dict) -> Match | None:
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

    kickoff_utc = datetime.fromisoformat(kickoff_raw.replace("Z", "+00:00"))
    kickoff_at = kickoff_utc.astimezone(ZoneInfo("Asia/Tokyo")).replace(tzinfo=None)

    return match_repository.create_match(
        db=db,
        match_id=match_id,
        kickoff_at=kickoff_at,
        stage=match_data.get("stage") or "UNKNOWN",
        venue=match_data.get("venue") or "UNKNOWN",
        home_team_id=home_team_id,
        away_team_id=away_team_id,
    )


def sync_matches_from_matches(
    db: Session,
    matches: list[dict],
) -> list[Match]:
    synced_matches: list[Match] = []

    for match_data in matches:
        match = sync_match_from_api_data(db, match_data)
        if match is not None:
            synced_matches.append(match)

    return synced_matches
