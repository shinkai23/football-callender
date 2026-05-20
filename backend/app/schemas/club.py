from pydantic import BaseModel, ConfigDict


class ClubResponse(BaseModel):
    id: int
    name: str
    country: str
    league: str

    model_config = ConfigDict(from_attributes=True)