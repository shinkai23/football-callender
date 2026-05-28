from sqlalchemy.orm import Session

from app.integrations.football_data.client import get_competition_matches
from app.models.match import Match
from app.models.team import Team
from app.sync.team_match_sync import sync_teams_and_matches_from_matches


def sync_world_cup_data(db: Session) -> tuple[list[Team], list[Match]]:
    data = get_competition_matches(
        competition_code="WC",
        date_from="2026-06-11",
        date_to="2026-07-19",
    )

    if data is None:
        return [], []

    return sync_teams_and_matches_from_matches(db, data.get("matches", []))
