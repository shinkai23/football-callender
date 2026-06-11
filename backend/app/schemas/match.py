from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.team import TeamResponse


class MatchResponse(BaseModel):
    id: int
    kickoff_at: datetime
    stage: str
    venue: str
    competition_code: str
    status: str
    home_score: int | None
    away_score: int | None
    home_team: TeamResponse
    away_team: TeamResponse

    model_config = ConfigDict(from_attributes=True)
