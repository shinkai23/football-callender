from app.db.session import SessionLocal, init_db
from app.services.sync_service import sync_world_cup_teams


def main() -> None:
    init_db()

    db = SessionLocal()
    try:
        teams = sync_world_cup_teams(db)
        print(f"Synced teams: {len(teams)}")

        for team in teams:
            print(f"- {team.id}: {team.name}")
    finally:
        db.close()


if __name__ == "__main__":
    main()