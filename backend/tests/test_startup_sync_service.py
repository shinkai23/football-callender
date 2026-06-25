from app.schemas.sync import SyncResult
from app.services import startup_sync_service


class DummySession:
    closed = False

    def close(self) -> None:
        self.closed = True


def test_run_startup_sync_initializes_db_and_closes_session(monkeypatch) -> None:
    calls = []
    session = DummySession()

    monkeypatch.setattr(
        startup_sync_service,
        "init_db",
        lambda: calls.append("init_db"),
    )
    monkeypatch.setattr(
        startup_sync_service,
        "SessionLocal",
        lambda: session,
    )
    monkeypatch.setattr(
        startup_sync_service,
        "sync_world_cup_data",
        lambda db: SyncResult(
            success=True,
            teams_count=2,
            matches_count=1,
            message="同期が完了しました。",
        ),
    )

    startup_sync_service.run_startup_sync()

    assert calls == ["init_db"]
    assert session.closed is True
