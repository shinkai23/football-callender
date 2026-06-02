from sqlalchemy.orm import Session

from app.integrations.football_data.client import get_competition_matches
from app.schemas.sync import SyncResult
from app.sync.team_match_sync import sync_teams_and_matches_from_matches


def sync_world_cup_data(db: Session) -> SyncResult:
    """W杯関連のサッカーデータ（試合・チーム、将来は選手・クラブ）を外部APIからDBへ同期する。"""
    data = get_competition_matches(
        competition_code="WC",
        date_from="2026-06-11",
        date_to="2026-07-19",
    )

    if data is None:
        return SyncResult(
            success=False,
            teams_count=0,
            matches_count=0,
            message="API呼び出しに失敗したか、データが空です。",
        )

    synced_teams, synced_matches = sync_teams_and_matches_from_matches(
        db,
        data.get("matches", []),
    )

    teams_count = len(synced_teams)
    matches_count = len(synced_matches)

    return SyncResult(
        success=teams_count > 0 or matches_count > 0,
        teams_count=teams_count,
        matches_count=matches_count,
        message="同期が完了しました。",
    )
