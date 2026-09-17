from pydantic import BaseModel, Field
from typing import Optional


class TravelRequest(BaseModel):
    query: str


class TravelRequirements(BaseModel):
    destination: str = ""
    duration_days: Optional[int] = None
    travelers: Optional[int] = None
    budget: Optional[float] = None
    currency: Optional[str] = None

    preferences: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)