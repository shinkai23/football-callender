from sqlalchemy.orm import Session

from app.models.team import Team
from app.services.football_api_service import get_competition_matches
from app.services.sync.team_sync_service import sync_teams_from_matches


def fetch_world_cup_matches() -> list[dict]:
    data = get_competition_matches(
        competition_code="WC",
        date_from="2026-06-11",
        date_to="2026-07-19",
    )

    if data is None:
        return []

    return data.get("matches", [])


def sync_world_cup_teams(db: Session) -> list[Team]:
    matches = fetch_world_cup_matches()
    return sync_teams_from_matches(db, matches)
