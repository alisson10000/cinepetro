from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime

class EpisodeBase(BaseModel):
    title: constr(max_length=255)
    description: Optional[str] = None
    season_number: Optional[int] = None
    episode_number: Optional[int] = None
    duration: Optional[int] = None
    series_id: int
    created_by: Optional[int] = None  # agora em conformidade com o banco

class EpisodeCreate(EpisodeBase):
    pass

class EpisodeUpdate(BaseModel):
    title: Optional[constr(max_length=255)] = None
    description: Optional[str] = None
    season_number: Optional[int] = None
    episode_number: Optional[int] = None
    duration: Optional[int] = None
    # series_id e created_by geralmente não mudam após criação, mas pode adicionar se necessário

class EpisodeOut(EpisodeBase):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
