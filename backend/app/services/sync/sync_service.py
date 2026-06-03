from sqlalchemy.orm import Session

from app.models.team import Team
from app.schemas.sync import SyncResult
from app.services.football_api_service import get_competition_matches
from app.services.sync.match_sync_service import sync_matches_from_matches
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


def sync_world_cup_data(db: Session) -> SyncResult:
    matches = fetch_world_cup_matches()

    if not matches:
        return SyncResult(
            success=False,
            teams_count=0,
            matches_count=0,
            message="API呼び出しに失敗したか、データが空です。",
        )

    synced_teams = sync_teams_from_matches(db, matches)
    synced_matches = sync_matches_from_matches(db, matches)

    teams_count = len(synced_teams)
    matches_count = len(synced_matches)

    return SyncResult(
        success=teams_count > 0 or matches_count > 0,
        teams_count=teams_count,
        matches_count=matches_count,
        message="同期が完了しました。",
    )
