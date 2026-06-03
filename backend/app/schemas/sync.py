from dataclasses import dataclass


@dataclass(frozen=True)
class SyncResult:
    """外部API同期の結果。各モデルの同期件数で成功を確認できる。"""

    success: bool
    teams_count: int
    matches_count: int
    players_count: int = 0
    clubs_count: int = 0
    message: str = ""

    @property
    def total_count(self) -> int:
        return (
            self.teams_count
            + self.matches_count
            + self.players_count
            + self.clubs_count
        )
