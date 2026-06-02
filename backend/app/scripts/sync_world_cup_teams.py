from app.db.session import SessionLocal, init_db
from app.services.sync_service import sync_world_cup_data


def main() -> None:
    init_db()

    db = SessionLocal()
    try:
        result = sync_world_cup_data(db)

        if not result.success:
            print(f"Sync failed: {result.message}")
            return

        print(result.message)
        print(
            f"teams={result.teams_count}, "
            f"matches={result.matches_count}, "
            f"players={result.players_count}, "
            f"clubs={result.clubs_count} "
            f"(total={result.total_count})"
        )
    finally:
        db.close()


if __name__ == "__main__":
    main()
