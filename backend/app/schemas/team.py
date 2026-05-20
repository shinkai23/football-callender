from pydantic import BaseModel, ConfigDict


class TeamResponse(BaseModel):
    id: int
    name: str
    country: str

    model_config = ConfigDict(from_attributes=True)