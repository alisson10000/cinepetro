from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EpisodeBase(BaseModel):
    title: str
    description: Optional[str] = None
    season_number: Optional[int] = None
    episode_number: Optional[int] = None
    duration: Optional[int] = None
    series_id: int

class EpisodeCreate(EpisodeBase):
    pass

class EpisodeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    season_number: Optional[int] = None
    episode_number: Optional[int] = None
    duration: Optional[int] = None

class EpisodeOut(EpisodeBase):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
