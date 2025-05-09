from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WetherSchema(BaseModel):
    temperature: float
    city: str
    time_point: datetime
    id: int | None = None
    model_config = ConfigDict(from_attributes=True)
