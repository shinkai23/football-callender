from sqlalchemy.orm import Session

from app.services.football_api_service import get_competition_matches
from app.models.team import Team
from app.repositories import team_repository


def sync_team_from_api_data(db: Session, team_data: dict) -> Team:
    team_id = team_data["id"]
    name = team_data["name"]

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


def sync_teams_from_matches(db: Session, matches: list[dict]) -> list[Team]:
    synced_teams = []
    synced_team_ids = set()

    for match in matches:
        for key in ("homeTeam", "awayTeam"):
            team_data = match.get(key)

            if not team_data:
                continue

            team_id = team_data["id"]

            if team_id in synced_team_ids:
                continue

            team = sync_team_from_api_data(db, team_data)

            if team is None:
                continue

            synced_teams.append(team)
            synced_team_ids.add(team_id)
    
    return synced_teams


def sync_world_cup_teams(db: Session) -> list[Team]:
    data = get_competition_matches(
        competition_code="WC",
        date_from="2026-06-11",
        date_to="2026-07-19",
    )
    
    if data is None:
        return []
    
    return sync_teams_from_matches(db, data.get("matches", []))
