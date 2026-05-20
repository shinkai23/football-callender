from pydantic import BaseModel, ConfigDict

from app.schemas.club import ClubResponse
from app.schemas.team import TeamResponse


class PlayerResponse(BaseModel):
    id: int
    name: str
    position: str
    team: TeamResponse
    club: ClubResponse | None

    model_config = ConfigDict(from_attributes=True)