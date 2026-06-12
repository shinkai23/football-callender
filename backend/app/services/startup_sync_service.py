from app.db.session import SessionLocal, init_db
from app.services.sync import sync_world_cup_data


def run_startup_sync() -> None:
    init_db()

    db = SessionLocal()
    try:
        result = sync_world_cup_data(db)

        if not result.success:
            print(f"Startup sync skipped: {result.message}")
            return

        print(
            "Startup sync completed: "
            f"teams={result.teams_count}, "
            f"matches={result.matches_count}, "
            f"players={result.players_count}, "
            f"clubs={result.clubs_count}, "
            f"total={result.total_count}"
        )
    finally:
        db.close()
