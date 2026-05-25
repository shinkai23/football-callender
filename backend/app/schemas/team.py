from pydantic import BaseModel, ConfigDict


class TeamResponse(BaseModel):
    id: int
    name: str
    country: str
    short_name: str | None
    tla: str | None
    crest: str | None

    model_config = ConfigDict(from_attributes=True)