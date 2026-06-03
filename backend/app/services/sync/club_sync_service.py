from sqlalchemy.orm import Session

from app.models.club import Club
from app.repositories import club_repository


def sync_club_from_person_data(db: Session, person_data: dict) -> Club | None:
    current_team = person_data.get("currentTeam")

    if not current_team:
        return None

    club_id = current_team.get("id")
    club_name = current_team.get("name")

    if club_id is None or club_name is None:
        return None

    existing_club = club_repository.get_club_by_id(db, club_id)
    if existing_club is not None:
        return existing_club

    area = current_team.get("area") or {}

    return club_repository.create_club(
        db=db,
        club_id=club_id,
        name=club_name,
        country=area.get("name", ""),
        league="",
    )
